"""Recompute the headline numbers of the Gemma 4 Paper Track study from the saved result files.

Standard library only. Read-only. No model, network, GPU or QuixBugs clone is needed.
Usage (from anywhere):  python -B paper/scripts/verify_published_metrics.py
Exit code 0 = every check passed; 1 = at least one check failed.

It checks the published numbers against the saved evidence; it does NOT re-run inference.
"""
import hashlib
import json
import math
import sys
from pathlib import Path

PAPER = Path(__file__).resolve().parents[1]
H = PAPER / "experiments" / "p1_harness"
MAIN = H / "results" / "main_seed1"
PILOT = H / "results" / "pilot_p2b"
A1, A2 = "arm1_basic", "arm2_test_guided"

ok_all = True


def check(name, ok, detail=""):
    global ok_all
    ok_all &= bool(ok)
    print(("PASS  " if ok else "FAIL  ") + name + (f"   [{detail}]" if detail else ""))


def rows(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def binom_two_sided(k, n):
    """Exact two-sided sign test, p0 = 0.5 (n = discordant pairs, k = wins of one arm)."""
    if n == 0:
        return 1.0
    pk = [math.comb(n, i) / 2 ** n for i in range(n + 1)]
    return min(1.0, sum(p for p in pk if p <= pk[k] + 1e-12))


def clopper_pearson(k, n, alpha=0.05):
    def cdf(x, p):  # P(X <= x), X ~ Bin(n, p)
        return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(x + 1))

    def solve(f, increasing):
        """Find p in [0, 1] with f(p) = alpha/2 by bisection; f is monotone."""
        lo, hi = 0.0, 1.0
        for _ in range(200):
            mid = (lo + hi) / 2
            if (f(mid) < alpha / 2) == increasing:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2

    # lower bound: P(X >= k) = alpha/2 (increasing in p); upper bound: P(X <= k) = alpha/2 (decreasing in p)
    lo = 0.0 if k == 0 else solve(lambda p: 1 - cdf(k - 1, p), increasing=True)
    hi = 1.0 if k == n else solve(lambda p: cdf(k, p), increasing=False)
    return lo, hi


main, pilot = rows(MAIN / "results.jsonl"), rows(PILOT / "results.jsonl")
a1 = [r for r in main if r["arm"] == A1]
a2 = [r for r in main if r["arm"] == A2]

print("== run inventory (real inference vs mock) ==")
check("main run: 24 rows = 12 tasks x 2 arms x 1 seed", len(main) == 24 and len(a1) == 12 and len(a2) == 12 and {r["seed"] for r in main} == {1})
check("pilot run: 4 rows", len(pilot) == 4)
check("no mock row in main or pilot (is_mock = false for all 28)", not any(r["is_mock"] for r in main + pilot))
check("no backend errors in main or pilot", not any(r.get("error") for r in main + pilot))
check("24 main traces and 4 pilot traces present",
      len(list((MAIN / "traces").glob("*.jsonl"))) == 24 and len(list((PILOT / "traces").glob("*.jsonl"))) == 4)
check("only arm1_basic and arm2_test_guided were run (optional arms 2b, 3b, 3 have no rows)",
      {r["arm"] for r in main + pilot} == {A1, A2})

print("== headline result ==")
k1, k2 = sum(r["resolved_final_state"] for r in a1), sum(r["resolved_final_state"] for r in a2)
check("arm1_basic resolved 0/12", k1 == 0, f"got {k1}")
check("arm2_test_guided resolved 1/12", k2 == 1, f"got {k2}")
solved = [r["task_id"] for r in a2 if r["resolved_final_state"]]
check("the single resolved task is quixbugs/find_in_sorted", solved == ["quixbugs/find_in_sorted"], str(solved))

by = {(r["task_id"], r["arm"]): r for r in main}
tasks = sorted({r["task_id"] for r in main})
only1 = sum(by[(t, A1)]["resolved_final_state"] and not by[(t, A2)]["resolved_final_state"] for t in tasks)
only2 = sum(by[(t, A2)]["resolved_final_state"] and not by[(t, A1)]["resolved_final_state"] for t in tasks)
both = sum(by[(t, A1)]["resolved_final_state"] and by[(t, A2)]["resolved_final_state"] for t in tasks)
check("paired outcome: both 0, only arm1 0, only arm2 1, neither 11", (both, only1, only2, 12 - both - only1 - only2) == (0, 0, 1, 11))
p = binom_two_sided(min(only1, only2), only1 + only2)
check("exact two-sided sign test p = 1.0 (1 discordant task; no evidence of a difference)", abs(p - 1.0) < 1e-9, f"p={p:.3f}")
lo1, hi1 = clopper_pearson(0, 12)
lo2, hi2 = clopper_pearson(1, 12)
check("Clopper-Pearson 95% intervals: 0-26.5% (arm1), 0.2-38.5% (arm2)",
      round(100 * hi1, 1) == 26.5 and round(100 * lo2, 1) == 0.2 and round(100 * hi2, 1) == 38.5 and lo1 == 0.0,
      f"arm1 {100*lo1:.1f}-{100*hi1:.1f}, arm2 {100*lo2:.1f}-{100*hi2:.1f}")

print("== process measures ==")
S = lambda rs, k: sum(r[k] for r in rs)  # noqa: E731
end = lambda rs, e: sum(r["end_reason"] == e for r in rs)  # noqa: E731
check("submitted: arm1 5, arm2 2", (S(a1, "submitted"), S(a2, "submitted")) == (5, 2))
check("end reasons: arm1 5 submitted + 6 max_turns + 1 format_abort; arm2 2 submitted + 10 max_turns",
      (end(a1, "submitted"), end(a1, "max_turns"), end(a1, "format_abort"), end(a2, "submitted"), end(a2, "max_turns")) == (5, 6, 1, 2, 10))
check("format errors 5 / 0", (S(a1, "format_errors"), S(a2, "format_errors")) == (5, 0))
check("edit attempts / rejected: 24 / 15 (arm1), 43 / 31 (arm2)",
      (S(a1, "edits"), S(a1, "edit_errors"), S(a2, "edits"), S(a2, "edit_errors")) == (24, 15, 43, 31))
errs = {"no_match": 0, "syntax": 0, "malformed": 0}
repeated = 0  # no-match calls whose exact `old` string occurs in >= 2 replace_in_file calls of the same run
for tf in (MAIN / "traces").glob("*.jsonl"):
    recs = [json.loads(line) for line in tf.read_text(encoding="utf-8").splitlines()]
    edits = [r for r in recs if r.get("tool") == "replace_in_file"]
    olds = [r["args"].get("old") for r in edits if isinstance(r.get("args"), dict)]
    for rec in edits:
        out = rec.get("result", "")
        if out.startswith("ERROR"):
            kind = "no_match" if "matched 0 times" in out else "syntax" if "syntax" in out.lower() else "malformed"
            errs[kind] += 1
            if kind == "no_match" and olds.count(rec["args"].get("old")) >= 2:
                repeated += 1
check("35 of the 41 no-match calls use an `old` string sent at least twice in the same run (draft wording; counts the failing call itself)",
      repeated == 35, f"got {repeated}")
check("rejected edits recomputed from traces: 46 = 41 no-match + 4 syntax-error + 1 malformed (31 + 15)",
      errs == {"no_match": 41, "syntax": 4, "malformed": 1}, str(errs))
check("tokens prompt/completion: 145,249 / 6,544 (arm1), 187,721 / 6,884 (arm2)",
      (S(a1, "prompt_tokens"), S(a1, "completion_tokens"), S(a2, "prompt_tokens"), S(a2, "completion_tokens")) == (145249, 6544, 187721, 6884))
check("turns 106 + 115 = 221", (S(a1, "turns"), S(a2, "turns")) == (106, 115))

print("== provenance and integrity ==")
check("main results.jsonl SHA-256 begins 56a7f4ab (P2C report)", sha(MAIN / "results.jsonl").startswith("56a7f4ab"))
check("pilot results.jsonl SHA-256 begins c4b63098 (P2C report)", sha(PILOT / "results.jsonl").startswith("c4b63098"))
freeze = [line.split("  ", 1) for line in (H / "FREEZE.sha256").read_text().splitlines() if line.strip()]
bad = [rel for h, rel in freeze if sha(H / rel) != h]
check(f"frozen files unchanged: {len(freeze) - len(bad)}/{len(freeze)} match FREEZE.sha256", len(freeze) == 19 and not bad, ", ".join(bad))
check("FREEZE.sha256 itself hashes to 5f3095c1... (P2C report)", sha(H / "FREEZE.sha256").startswith("5f3095c1"))
meta = json.loads((MAIN / "run_meta.json").read_text())
check("run_meta records the GGUF SHA-256 fa401b55...c6634", meta["gguf_sha256"].startswith("fa401b55") and meta["gguf_sha256"].endswith("c6634"))
mock = (PAPER / "results" / "selftest_mock_log_2026-11-07.txt").read_text().splitlines()
npass, nfail = sum(l.startswith("PASS") for l in mock), sum(l.startswith("FAIL") for l in mock)
check("mock self-test log: 23 PASS / 0 FAIL (structural test, no Gemma involved)", (npass, nfail) == (23, 0), f"{npass}/{nfail}")

print()
print("ALL CHECKS PASSED" if ok_all else "SOME CHECKS FAILED")
sys.exit(0 if ok_all else 1)
