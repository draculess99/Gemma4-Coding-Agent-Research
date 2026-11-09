"""Independent cross-check: numbers shown in the figures vs the figures' written sources.
Recomputes from results.jsonl and asserts equality with values stated in reports/P2C_MAIN_EXPERIMENT.md and the draft.
Usage:  python -B verify_against_reports.py     (read-only; prints PASS/FAIL lines)
"""
import re
from _common import *  # noqa: F401,F403

P2C = (PAPER / "reports" / "P2C_MAIN_EXPERIMENT.md").read_text(encoding="utf-8")
DRAFT = (PAPER / "drafts" / "GEMMA4_PAPER_DRAFT_V1.md").read_text(encoding="utf-8")
rows = load_main()
res = []


def check(name, ok):
    res.append(ok)
    print(("PASS  " if ok else "FAIL  ") + name)


a1 = [r for r in rows if r["arm"] == "arm1_basic"]
a2 = [r for r in rows if r["arm"] == "arm2_test_guided"]
check("arm1 resolved 0/12 (P2C: 'BASIC_TASKS_RESOLVED ... 0/12')", sum(r["resolved_final_state"] for r in a1) == 0 and "**0/12**" in P2C)
check("arm2 resolved 1/12 (P2C: '**1/12**')", sum(r["resolved_final_state"] for r in a2) == 1 and "**1/12**" in P2C)
check("rows: 24 total, 0 mock, 0 errors", len(rows) == 24 and not any(r["is_mock"] for r in rows) and not any(r["error"] for r in rows))
check("end reasons arm1 6 max_turns / 1 format_abort (P2C table '6 / 1')", sum(r["end_reason"] == "max_turns" for r in a1) == 6 and sum(r["end_reason"] == "format_abort" for r in a1) == 1 and "6 / 1" in P2C)
check("end reasons arm2 10 max_turns (P2C '10 / 0')", sum(r["end_reason"] == "max_turns" for r in a2) == 10 and "10 / 0" in P2C)
check("format errors 5 / 0", sum(r["format_errors"] for r in a1) == 5 and sum(r["format_errors"] for r in a2) == 0)
check("edits/rejected 24/15 and 43/31 (P2C '24 / 15', '43 / 31')", (sum(r["edits"] for r in a1), sum(r["edit_errors"] for r in a1), sum(r["edits"] for r in a2), sum(r["edit_errors"] for r in a2)) == (24, 15, 43, 31) and "24 / 15" in P2C and "43 / 31" in P2C)
man = load_manifest()
base = {t["task_id"]: t["n_failing_on_buggy"] for t in man["tasks"]}
by = {(r["task_id"], r["arm"]): r for r in rows}
worse = {a: sorted(t.split("/")[1] for t in base if by[(t, a)]["final_tests"]["failed"] > base[t]) for a in ("arm1_basic", "arm2_test_guided")}
check(f"worse-than-baseline sets {worse} match P2C text", worse["arm1_basic"] == ["is_valid_parenthesization", "pascal", "quicksort"] and worse["arm2_test_guided"] == ["kth", "quicksort"] and "is_valid_parenthesization (1→3), pascal (4→5), quicksort (1→13)" in P2C)
check("CI 0-26.5% and 0.2-38.5% match the draft", "0–26.5%" in DRAFT and "0.2–38.5%" in DRAFT and abs(clopper_pearson(0, 12)[1] - 0.2646) < 1e-3 and abs(clopper_pearson(1, 12)[0] - 0.0021) < 1e-3 and abs(clopper_pearson(1, 12)[1] - 0.3848) < 1e-3)
check("sign test p = 1.0 (1 discordant)", exact_sign_p(0, 1) == 1.0)
check("turns 106 + 115 = 221 server requests (P2C 'Turns 106 | 115')", sum(r["turns"] for r in a1) == 106 and sum(r["turns"] for r in a2) == 115)
n, nm, bad = freeze_recheck()
check(f"freeze {nm}/{n} files match (P2C: 'UNCHANGED since freeze', 19 files)", n == 19 and nm == n and "19 files" in P2C)
check("results.jsonl SHA-256 prefix 56a7f4ab (P2C)", sha256_file(RES_MAIN / "results.jsonl").startswith("56a7f4ab") and "56a7f4ab" in P2C)
check("pilot results.jsonl SHA-256 prefix c4b63098 (P2C)", sha256_file(RES_PILOT / "results.jsonl").startswith("c4b63098") and "c4b63098" in P2C)
check("mock log: 23 PASS, 0 FAIL (P2A: '23 PASS / 0 FAIL')", parse_mock_log()[1:3] == (23, 0) and "23 PASS / 0 FAIL" in (PAPER / "reports" / "P2A_LOCAL_VERIFICATION.md").read_text(encoding="utf-8"))
check("manifest 31 scanned / 28 eligible / 12 tasks / seed 20261107", (man["selection"]["n_scanned"], man["selection"]["n_eligible"], len(man["tasks"]), man["selection"]["seed"]) == (31, 28, 12, 20261107))
print("\nALL CHECKS PASSED" if all(res) else "\nSOME CHECKS FAILED")
raise SystemExit(0 if all(res) else 1)
