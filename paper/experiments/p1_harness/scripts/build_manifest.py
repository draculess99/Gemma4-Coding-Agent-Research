"""Build the task manifest from a pinned local clone of QuixBugs.

Eligibility is decided by MEASUREMENT, not by hand:
  1. single-file, non-graph program with a pytest file (python_testcases/test_<name>.py)
  2. buggy version FAILS at least one test, reference (--correct) version PASSES all tests
  3. both runs finish within the per-run timeout (default 20 s)
Then a seeded random sample of N tasks is drawn from the eligible set, so the
selection is reproducible and not cherry-picked.

Usage (Windows or Linux):
  python scripts/build_manifest.py --quixbugs <path-to-clone> --out manifest/task_manifest.json
"""
import argparse, hashlib, json, random, shutil, subprocess, sys, tempfile, time
import xml.etree.ElementTree as ET
from pathlib import Path

# Programs the QuixBugs README marks as graph-based (need Node objects; tests live next to program).
GRAPH_BASED = {
    "breadth_first_search", "depth_first_search", "detect_cycle", "minimum_spanning_tree",
    "reverse_linked_list", "shortest_path_length", "shortest_path_lengths",
    "shortest_paths", "topological_ordering", "node",
}


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run_pytest(root: Path, name: str, correct: bool, timeout: int):
    xml = root / f"_junit_{name}_{'c' if correct else 'b'}.xml"
    cmd = [sys.executable, "-m", "pytest", f"python_testcases/test_{name}.py", "-q", "-p", "no:cacheprovider",
           f"--junitxml={xml}"]
    if correct:
        cmd.append("--correct")
    t0 = time.time()
    try:
        subprocess.run(cmd, cwd=root, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "seconds": round(time.time() - t0, 2)}
    secs = round(time.time() - t0, 2)
    if not xml.exists():
        return {"status": "no_report", "seconds": secs}
    suite = ET.parse(xml).getroot()
    s = suite if suite.tag == "testsuite" else suite.find("testsuite")
    tests, fails, errs = int(s.get("tests")), int(s.get("failures")), int(s.get("errors"))
    return {"status": "ok", "tests": tests, "failed": fails + errs, "seconds": secs}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quixbugs", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=12)
    ap.add_argument("--seed", type=int, default=20261107)
    ap.add_argument("--timeout", type=int, default=20)
    a = ap.parse_args()

    src = Path(a.quixbugs).resolve()
    work = Path(tempfile.mkdtemp(prefix="qb_scan_"))
    root = work / "QuixBugs"
    shutil.copytree(src, root, ignore=shutil.ignore_patterns(".git"))

    commit = "unknown"
    try:
        commit = subprocess.run(["git", "-C", str(src), "rev-parse", "HEAD"], capture_output=True,
                                text=True).stdout.strip() or "unknown"
    except Exception:
        pass

    names = sorted(p.stem for p in (root / "python_programs").glob("*.py")
                   if not p.stem.endswith("_test") and p.stem not in GRAPH_BASED)
    scan, eligible = [], []
    for n in names:
        if not (root / "python_testcases" / f"test_{n}.py").exists() or not (root / "correct_python_programs" / f"{n}.py").exists():
            scan.append({"task": n, "eligible": False, "reason": "missing test or reference"})
            continue
        b, c = run_pytest(root, n, False, a.timeout), run_pytest(root, n, True, a.timeout)
        ok = b.get("status") == "ok" and c.get("status") == "ok" and b["failed"] > 0 and c["failed"] == 0
        reason = "ok" if ok else f"buggy={b} correct={c}"
        scan.append({"task": n, "eligible": ok, "buggy": b, "reference": c, "reason": reason if not ok else "ok"})
        if ok:
            eligible.append(n)
        print(f"{n:28s} eligible={ok} buggy={b.get('failed')}/{b.get('tests')} ref_fail={c.get('failed')} t={b.get('seconds')}+{c.get('seconds')}s")

    rng = random.Random(a.seed)
    chosen = sorted(rng.sample(eligible, min(a.n, len(eligible))))
    tasks = []
    for n in chosen:
        info = next(s for s in scan if s["task"] == n)
        tasks.append({
            "task_id": f"quixbugs/{n}",
            "program": f"python_programs/{n}.py",
            "reference_program": f"correct_python_programs/{n}.py",
            "test_file": f"python_testcases/test_{n}.py",
            "testcases_json": f"json_testcases/{n}.json",
            "n_tests": info["buggy"]["tests"],
            "n_failing_on_buggy": info["buggy"]["failed"],
            "sha256_buggy": sha256(root / "python_programs" / f"{n}.py"),
            "sha256_reference": sha256(root / "correct_python_programs" / f"{n}.py"),
            "sha256_test": sha256(root / "python_testcases" / f"test_{n}.py"),
            "measured_seconds_buggy": info["buggy"]["seconds"],
            "license": "MIT-style text in repo LICENSE; see legal_notes.txt for Quixey provenance caveat",
        })
    manifest = {
        "benchmark": "QuixBugs (Python)", "repo": "https://github.com/jkoppel/QuixBugs", "pinned_commit": commit,
        "selection": {"rule": "seeded random sample from measured-eligible set", "seed": a.seed, "n_requested": a.n,
                      "per_run_timeout_s": a.timeout, "n_scanned": len(names), "n_eligible": len(eligible),
                      "excluded_graph_based": sorted(GRAPH_BASED)},
        "tasks": tasks, "scan": scan,
    }
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(manifest, indent=2))
    shutil.rmtree(work, ignore_errors=True)
    print(f"\nscanned={len(names)} eligible={len(eligible)} chosen={len(chosen)} -> {a.out}")


if __name__ == "__main__":
    main()
