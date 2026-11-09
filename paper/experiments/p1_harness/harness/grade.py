"""Final grading in a FRESH workspace using the unmodified official QuixBugs pytest file."""
import ast, difflib
from pathlib import Path
from . import workspace as W


def _normalise(src: str) -> str:
    tree = ast.parse(src)
    for node in ast.walk(tree):
        body = getattr(node, "body", None)
        if isinstance(body, list):
            node.body = [b for b in body if not (isinstance(b, ast.Expr) and isinstance(getattr(b, "value", None), ast.Constant)
                                                 and isinstance(b.value.value, str))] or [ast.Pass()]
    return ast.dump(tree)


def diff_lines(a: str, b: str) -> int:
    d = difflib.unified_diff(a.splitlines(), b.splitlines(), lineterm="", n=0)
    return sum(1 for l in d if (l.startswith("+") or l.startswith("-")) and not l.startswith(("+++", "---")))


def unified(a: str, b: str, path: str) -> str:
    return "\n".join(difflib.unified_diff(a.splitlines(), b.splitlines(), f"a/{path}", f"b/{path}", lineterm=""))


def grade(qb_root, task: dict, final_source: str, tmp_dir) -> dict:
    n = W.task_name(task)
    out = {"syntax_error": False, "resolved": False, "final_tests": None, "ast_equal_reference": False}
    try:
        compile(final_source, "<final>", "exec")
    except SyntaxError:
        out["syntax_error"] = True
        return out
    ws = W.make_workspace(qb_root, task, Path(tmp_dir) / "grade_ws")
    (ws / task["program"]).write_text(final_source, encoding="utf-8", newline="")
    res = W.run_tests(ws, n, timeout=60)
    out["final_tests"] = {"status": res["status"], "tests": res["tests"], "failed": res["failed"]}
    out["resolved"] = res["status"] == "ok" and res["failed"] == 0 and res["tests"] == task["n_tests"]
    ref = (Path(qb_root) / task["reference_program"]).read_text(encoding="utf-8")
    try:
        out["ast_equal_reference"] = _normalise(final_source) == _normalise(ref)
    except SyntaxError:
        pass
    return out
