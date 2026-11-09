"""Harness self-test with SCRIPTED MOCK policies (no model, no GPU, no network). Results are flagged is_mock and
written to a temp dir; they say NOTHING about Gemma. Usage:  python scripts/selftest.py --qb-root <QuixBugs clone>
"""
import argparse, difflib, json, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from harness.llm import MockBackend            # noqa: E402
from harness.run_experiment import execute, verify_pin   # noqa: E402

ARMS = ["arm1_basic", "arm2_test_guided", "arm2b_agent_initiated_tests", "arm3_graph_test_validated", "arm3b_test_validated_nograph"]
J = lambda tool, **args: json.dumps({"tool": tool, "args": args})  # noqa: E731


def hunk(buggy: str, ref: str):
    a, b = buggy.splitlines(keepends=True), ref.splitlines(keepends=True)
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b).get_opcodes():
        old, new = "".join(a[i1:i2]), "".join(b[j1:j2])
        if tag == "equal" or (not old.strip() and not new.strip()):
            continue  # skip identical and whitespace-only differences
        k = 0 if old.strip() else 1  # pure insertion needs at least one anchor line
        while i1 - k >= 0:           # widen with preceding context until the match is unique
            o, n = "".join(a[i1 - k:i2]), "".join(b[j1 - k:j2])
            if buggy.count(o) == 1:
                return o, n
            k += 1
    raise AssertionError("no unique hunk")


def make_policy(kind, qb, task):
    n = Path(task["program"]).stem
    old, new = hunk((qb / task["program"]).read_text(), (qb / task["reference_program"]).read_text())

    def policy(messages, st):
        step = st.get("step", 0)
        st["step"] = step + 1
        if kind == "oracle":
            return [J("read_file", path=task["program"]), J("replace_in_file", path=task["program"], old=old, new=new), J("submit")][min(step, 2)]
        if kind == "noop":
            return J("submit")
        if kind == "garbage":
            return "I think the bug is somewhere in the loop."
        if kind == "graphprobe":
            return [J("get_code_neighbors", symbol=n), J("submit")][min(step, 1)]
        if kind == "runtests":
            return [J("run_tests"), J("submit")][min(step, 1)]
    return policy


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--qb-root", required=True)
    a = ap.parse_args()
    qb = Path(a.qb_root).resolve()
    manifest = json.loads((ROOT / "manifest" / "task_manifest.json").read_text())
    verify_pin(qb, manifest)
    sub = {"tasks": manifest["tasks"][:3]}
    fails = []

    def check(cond, msg):
        print(("PASS  " if cond else "FAIL  ") + msg)
        if not cond:
            fails.append(msg)

    for kind in ("oracle", "noop", "garbage", "graphprobe", "runtests"):
        rows = []
        for t in sub["tasks"]:
            out = Path(tempfile.mkdtemp(prefix=f"selftest_{kind}_"))
            be = MockBackend(None)
            # fresh policy state per run: wrap so each run gets its own counter
            def chat(messages, *args, _t=t, _be=be, **kw):
                if len(messages) == 2:
                    _be.state = {}
                    _be.policy = make_policy(kind, qb, _t)
                return MockBackend.chat(_be, messages, *args, **kw)
            be.chat = chat
            p = execute(be, qb, out, ARMS, [1], {"tasks": [t], "pinned_commit": manifest["pinned_commit"]}, log=lambda *_: None)
            rows += [json.loads(l) for l in p.read_text().splitlines()]
        by = lambda arm: [r for r in rows if r["arm"] == arm]  # noqa: E731
        check(all(r["is_mock"] for r in rows), f"[{kind}] all rows flagged is_mock")
        if kind == "oracle":
            check(all(r["resolved_final_state"] and r["resolved_submitted"] for r in rows), "[oracle] resolves every task in every arm (grader + edit path work)")
            check(all(r["ast_equal_reference"] for r in rows), "[oracle] AST equals reference")
            check(all(r["test_runs"] == 0 for r in by("arm1_basic")), "[oracle] arm1 performs ZERO test runs")
            check(all(r["test_runs"] >= 2 for r in by("arm2_test_guided")), "[oracle] arm2 test runs = initial + after-edit (>=2)")
            check(all(r["gate_rejections"] == 0 for r in rows), "[oracle] no gate rejections when fix is correct")
        if kind == "noop":
            check(not any(r["resolved_final_state"] for r in rows), "[noop] unresolved everywhere (grader does not hallucinate passes)")
            check(all(r["gate_rejections"] == 0 for r in by("arm1_basic") + by("arm2_test_guided")), "[noop] arm1/arm2 have no submit gate")
            check(all(r["gate_rejections"] == 3 for r in by("arm3_graph_test_validated")), "[noop] arm3 gate rejects 3x then accepts as-is")
            check(all(r["submitted"] and not r["resolved_submitted"] for r in rows), "[noop] submitted but not resolved")
        if kind == "garbage":
            check(all(r["end_reason"] == "format_abort" and r["format_errors"] == 3 for r in rows), "[garbage] format_abort after 3 format errors")
        if kind == "runtests":
            check(all(r["unknown_tool_calls"] == 1 and r["test_runs"] == 0 for r in by("arm1_basic")), "[runtests] run_tests unavailable in arm1")
            check(all(r["test_runs"] == 1 for r in by("arm2b_agent_initiated_tests")), "[runtests] arm2b run_tests tool executes tests on demand")
        if kind == "graphprobe":
            check(all(r["unknown_tool_calls"] == 1 and r["graph_calls"] == 0 for r in by("arm1_basic")), "[graphprobe] graph tool unavailable in arm1")
            check(all(r["graph_calls"] == 1 for r in by("arm3_graph_test_validated")), "[graphprobe] graph tool works in arm3")
    # workspace must never contain the reference solution
    from harness.workspace import make_workspace
    w = make_workspace(qb, manifest["tasks"][0], Path(tempfile.mkdtemp()) / "ws")
    check(not any("correct_python_programs" in str(p) for p in w.rglob("*")), "workspace contains no reference solution")
    # baseline integrity: buggy file must fail exactly as recorded in the manifest
    from harness.workspace import run_tests, task_name
    for t in manifest["tasks"][:3]:
        w = make_workspace(qb, t, Path(tempfile.mkdtemp()) / "ws")
        r = run_tests(w, task_name(t))
        check(r["tests"] == t["n_tests"] and r["failed"] == t["n_failing_on_buggy"], f"baseline {t['task_id']}: {r['failed']}/{r['tests']} failing matches manifest")
    print("\nSELFTEST", "FAILED" if fails else "PASSED")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
