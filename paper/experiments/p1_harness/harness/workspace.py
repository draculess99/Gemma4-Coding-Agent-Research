"""Per-run workspace creation and deterministic test execution (stdlib only, Windows/Linux)."""
import os, re, shutil, subprocess, sys, time
import xml.etree.ElementTree as ET
from pathlib import Path


def task_name(task: dict) -> str:
    return Path(task["program"]).stem


def make_workspace(qb_root, task: dict, dest) -> Path:
    """Copy ONLY what the agent may see. The reference solution is never copied."""
    n = task_name(task)
    rels = ["conftest.py", f"python_programs/{n}.py", f"python_testcases/test_{n}.py",
            "python_testcases/load_testdata.py", f"json_testcases/{n}.json"]
    dest = Path(dest)
    for r in rels:
        d = dest / r
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(Path(qb_root) / r, d)
    return dest


def run_tests(ws, name: str, timeout: int = 30) -> dict:
    ws = Path(ws)
    xml = ws.parent / f"{ws.name}__junit.xml"
    if xml.exists():
        xml.unlink()
    cmd = [sys.executable, "-B", "-m", "pytest", f"python_testcases/test_{name}.py", "-q",
           "-p", "no:cacheprovider", "--tb=short", f"--junitxml={xml}"]
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    t0 = time.time()
    try:
        subprocess.run(cmd, cwd=ws, capture_output=True, text=True, timeout=timeout, env=env)
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "tests": None, "failed": None, "failures": [],
                "seconds": round(time.time() - t0, 3), "timeout_s": timeout}
    secs = round(time.time() - t0, 3)
    if not xml.exists():
        return {"status": "no_report", "tests": None, "failed": None, "failures": [], "seconds": secs}
    root = ET.parse(xml).getroot()
    suite = root if root.tag == "testsuite" else root.find("testsuite")
    fails = []
    for tc in suite.iter("testcase"):
        bad = tc.find("failure")
        if bad is None:
            bad = tc.find("error")
        if bad is not None:
            fails.append({"name": tc.get("name"), "text": (bad.text or bad.get("message") or "").strip()})
    nf = int(suite.get("failures")) + int(suite.get("errors"))
    return {"status": "ok", "tests": int(suite.get("tests")), "failed": nf, "failures": fails, "seconds": secs}


def feedback_text(res: dict, max_chars: int = 900) -> str:
    """Deterministic, compact test feedback shown to the model (same function for all arms that use it)."""
    if res["status"] == "timeout":
        return f"TEST RESULT: TIMEOUT after {res['timeout_s']}s (possible infinite loop or very slow code)."
    if res["status"] != "ok":
        return "TEST RESULT: test runner produced no report (possible import or syntax error)."
    if res["failed"] == 0:
        return f"TEST RESULT: all {res['tests']} tests pass."
    f = res["failures"][0]
    lines = [l for l in f["text"].splitlines() if l.strip()][-8:]
    body = "\n".join(lines)
    out = f"TEST RESULT: {res['failed']} of {res['tests']} tests fail.\nFirst failing test: {f['name']}\n{body}"
    return out[:max_chars] + ("\n...[truncated]" if len(out) > max_chars else "")
