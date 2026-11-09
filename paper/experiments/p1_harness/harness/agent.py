"""Agent loop shared by all arms. Arms differ ONLY through the arm config (tools, auto_test, graph, submit_gate, intro)."""
import ast, json, shutil, time
from pathlib import Path
from . import workspace as W
from .graph import CodeGraph, suspects_from_failure
from .grade import grade, diff_lines, unified

TOOL_DOCS = {
    "read_file": ('{"tool":"read_file","args":{"path":"<relative path>"}}', "Show a workspace file with line numbers."),
    "replace_in_file": ('{"tool":"replace_in_file","args":{"path":"<target file>","old":"<exact old text>","new":"<new text>"}}',
                        "Replace exactly ONE occurrence of old with new in the target program (exact match incl. indentation)."),
    "get_code_neighbors": ('{"tool":"get_code_neighbors","args":{"symbol":"<function name>"}}', "Callers/callees of a symbol."),
    "get_code_subgraph": ('{"tool":"get_code_subgraph","args":{"symbol":"<function name>","depth":2}}', "Call subgraph below a symbol."),
    "run_tests": ('{"tool":"run_tests","args":{}}', "Run the test file and show a compact result."),
    "submit": ('{"tool":"submit","args":{}}', "Finish and submit your fix."),
}


def extract_action(text: str):
    """Return the LAST JSON object containing a 'tool' key (robust to reasoning text before the action)."""
    dec, i, found = json.JSONDecoder(), 0, None
    while True:
        j = text.find("{", i)
        if j < 0:
            break
        try:
            obj, end = dec.raw_decode(text[j:])
        except ValueError:
            i = j + 1
            continue
        if isinstance(obj, dict) and isinstance(obj.get("tool"), str):
            found, i = obj, j + end
        else:
            i = j + 1
    return found


def _trim_context(messages, max_chars):
    dropped = 0
    while sum(len(m["content"]) for m in messages) > max_chars and len(messages) > 4:
        del messages[2:4]
        dropped += 1
    return dropped


def run_agent(task, arm, seed, backend, qb_root, work_root, run_id, trace_dir, sampling, harness_version):
    n = W.task_name(task)
    target = f"python_programs/{n}.py"
    ws = W.make_workspace(qb_root, task, Path(work_root) / run_id / "ws")
    tpath = ws / target
    original = tpath.read_text(encoding="utf-8")
    B = arm["budgets"]
    c = dict(turns=0, tool_calls=0, format_errors=0, test_runs=0, edits=0, edit_errors=0, gate_rejections=0,
             prompt_tokens=0, completion_tokens=0, model_seconds=0.0, test_seconds=0.0, context_truncations=0,
             graph_calls=0, reads=0, unknown_tool_calls=0)
    trace, end_reason, submitted, error = [], None, False, None
    t0 = time.time()

    def do_tests():
        r = W.run_tests(ws, n, timeout=B["test_timeout_s"])
        c["test_runs"] += 1
        c["test_seconds"] += r["seconds"]
        return r

    # ---- system + first user message (differences between arms are explicit and config-driven)
    base = Path(arm["_root"], arm["system_prompt"]).read_text(encoding="utf-8")
    tools_txt = "\n".join(f"- {TOOL_DOCS[t][0]}\n  {TOOL_DOCS[t][1]}" for t in arm["tools"])
    system = base.replace("{{TOOLS}}", tools_txt)
    user0 = [f"The file `{target}` contains exactly one bug. Fix it so its tests pass.",
             f"The specification is the docstring at the bottom of the file. Tests: `python_testcases/test_{n}.py` "
             f"(data: `json_testcases/{n}.json`)."]
    graph, initial = None, None
    if arm["auto_test"]:
        initial = do_tests()
        user0.append("The harness runs the tests for you before the first step and after every edit.")
        user0.append("Initial test run:\n" + W.feedback_text(initial))
    else:
        if "run_tests" in arm["tools"]:
            user0.append("You may call the run_tests tool whenever you want to run the tests; the harness will not run them for you.")
        else:
            user0.append("No test runner is available; reason from the code, the docstring and the test data.")
    if arm["graph"]:
        graph = CodeGraph(original)
        user0.append("Code graph of the target file:\n" + graph.overview())
        if initial and initial.get("failures"):
            sus = suspects_from_failure(graph, n, initial["failures"][0]["text"])
            user0.append("Suspect functions (from the failing traceback): " + (", ".join(sus) or "none identified"))
    messages = [{"role": "system", "content": system}, {"role": "user", "content": "\n".join(user0)}]

    for turn in range(B["max_turns"]):
        if time.time() - t0 > B["max_wall_seconds"]:
            end_reason = "wall_timeout"
            break
        c["context_truncations"] += _trim_context(messages, B["max_context_chars"])
        try:
            r = backend.chat(messages, sampling["temperature"], sampling["top_p"], sampling["top_k"],
                             sampling["max_new_tokens"], seed * 1000 + turn)
        except Exception as e:  # noqa: BLE001 - recorded, run ends
            end_reason, error = "backend_error", f"{type(e).__name__}: {e}"[:300]
            break
        c["turns"] += 1
        c["prompt_tokens"] += r.prompt_tokens
        c["completion_tokens"] += r.completion_tokens
        c["model_seconds"] += r.seconds
        messages.append({"role": "assistant", "content": r.text})
        act = extract_action(r.text)
        entry = {"turn": turn, "assistant": r.text, "finish": r.finish_reason}
        if act is None or act.get("tool") not in arm["tools"]:
            if act is None:
                c["format_errors"] += 1
                reply = 'FORMAT ERROR: reply with exactly one JSON object, e.g. {"tool":"read_file","args":{"path":"%s"}}' % target
            else:
                c["unknown_tool_calls"] += 1
                reply = f"ERROR: tool '{act.get('tool')}' is not available. Available: {', '.join(arm['tools'])}"
            entry["result"] = reply
            trace.append(entry)
            messages.append({"role": "user", "content": reply})
            if c["format_errors"] >= B["max_format_errors"]:
                end_reason = "format_abort"
                break
            continue
        c["tool_calls"] += 1
        tool, args = act["tool"], (act.get("args") or {})
        entry["tool"], entry["args"] = tool, args
        if c["tool_calls"] > B["max_tool_calls"]:
            end_reason = "max_tool_calls"
            trace.append(entry)
            break
        out = ""
        if tool == "read_file":
            c["reads"] += 1
            p = (ws / str(args.get("path", ""))).resolve()
            if ws.resolve() not in p.parents or not p.is_file():
                out = "ERROR: file not found inside the workspace."
            else:
                lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
                out = "\n".join(f"{i+1:4d}  {l}" for i, l in enumerate(lines))[:B["max_output_chars"]]
        elif tool == "replace_in_file":
            c["edits"] += 1
            path, old, new = str(args.get("path", "")).replace("\\", "/"), args.get("old"), args.get("new")
            cur = tpath.read_text(encoding="utf-8")
            if path != target:
                out, c["edit_errors"] = f"ERROR: only `{target}` may be edited.", c["edit_errors"] + 1
            elif not isinstance(old, str) or not isinstance(new, str) or old == "":
                out, c["edit_errors"] = "ERROR: 'old' and 'new' must be strings and 'old' must be non-empty.", c["edit_errors"] + 1
            elif cur.count(old) != 1:
                out, c["edit_errors"] = f"ERROR: 'old' matched {cur.count(old)} times; it must match exactly once (check indentation).", c["edit_errors"] + 1
            else:
                cand = cur.replace(old, new)
                try:
                    ast.parse(cand)
                except SyntaxError as e:
                    out, c["edit_errors"] = f"ERROR: edit rejected, result has a syntax error: {e.msg} (line {e.lineno}).", c["edit_errors"] + 1
                else:
                    tpath.write_text(cand, encoding="utf-8", newline="")
                    out = "Edit applied."
                    if arm["auto_test"]:
                        out += "\n" + W.feedback_text(do_tests())
        elif tool == "run_tests":
            out = W.feedback_text(do_tests())
        elif tool in ("get_code_neighbors", "get_code_subgraph"):
            c["graph_calls"] += 1
            g = CodeGraph(tpath.read_text(encoding="utf-8"))
            out = g.neighbors_text(str(args.get("symbol", ""))) if tool == "get_code_neighbors" else \
                g.subgraph_text(str(args.get("symbol", "")), args.get("depth", 1))
        elif tool == "submit":
            if arm["submit_gate"]:
                res = do_tests()
                if res["status"] == "ok" and res["failed"] == 0:
                    submitted, end_reason = True, "submitted"
                elif c["gate_rejections"] < arm["gate_max_rejections"]:
                    c["gate_rejections"] += 1
                    out = "SUBMIT REJECTED: tests still failing. " + W.feedback_text(res)
                else:
                    submitted, end_reason = True, "submitted"  # gate exhausted: accepted as-is, still unresolved
            else:
                submitted, end_reason = True, "submitted"
            if submitted:
                entry["result"] = "submitted"
                trace.append(entry)
                break
        entry["result"] = out[:600]
        trace.append(entry)
        messages.append({"role": "user", "content": "TOOL RESULT:\n" + out})
    if end_reason is None:
        end_reason = "max_turns"

    final = tpath.read_text(encoding="utf-8")
    g = grade(qb_root, task, final, Path(work_root) / run_id)
    rec = {
        "run_id": run_id, "task_id": task["task_id"], "arm": arm["name"], "seed": seed,
        "end_reason": end_reason, "submitted": submitted, "error": error,
        "resolved_final_state": g["resolved"], "resolved_submitted": bool(g["resolved"] and submitted),
        "syntax_error_final": g["syntax_error"], "final_tests": g["final_tests"],
        "ast_equal_reference": g["ast_equal_reference"], "diff_lines_changed": diff_lines(original, final),
        "patch": unified(original, final, target),
        "initial_failed": (initial or {}).get("failed"),
        "wall_seconds": round(time.time() - t0, 2),
        **{k: (round(v, 3) if isinstance(v, float) else v) for k, v in c.items()},
        "is_mock": bool(getattr(backend, "is_mock", False)), "harness_version": harness_version,
    }
    Path(trace_dir).mkdir(parents=True, exist_ok=True)
    with open(Path(trace_dir) / f"{run_id}.jsonl", "w", encoding="utf-8") as f:
        f.write(json.dumps({"system": system, "user0": messages[1]["content"]}) + "\n")
        for e in trace:
            f.write(json.dumps(e) + "\n")
    shutil.rmtree(Path(work_root) / run_id, ignore_errors=True)
    return rec
