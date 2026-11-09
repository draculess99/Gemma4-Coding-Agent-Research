# MEDIA_VERIFICATION — Media Gallery figures

Date: 2026-11-08. All work in `paper\media\`. No Kaggle submission, GPU run, new inference, model download or paid API. No existing research, experiment data, report or draft file was modified (a file-timestamp scan found no changed file outside `media\`; `freeze.py --check` still reports **UNCHANGED since freeze**).

**Tooling note (disclosure):** matplotlib was not installed anywhere on the machine. Because the task requires matplotlib, I installed `matplotlib==3.9.2` (and its dependency numpy, a PyPI package download, not a model) into a throw-away virtual environment **outside the project** (session scratchpad). Nothing was installed globally. A reader reproducing the figures needs matplotlib (see `scripts\README.md`).

## Files

| # | Image | Size | Script |
|---|---|---|---|
| 1 | `paper\media\01_research_methodology.png` | 3200×1800 (16:9), 586 KB | `scripts\fig01_methodology.py` |
| 2 | `paper\media\02_results_comparison.png` | 3200×1800 (16:9), 412 KB | `scripts\fig02_results.py` |
| 3 | `paper\media\03_reproducibility.png` | 3200×1800 (16:9), 500 KB | `scripts\fig03_reproducibility.py` |

Other files: `scripts\_common.py`, `scripts\render_all.py`, `scripts\verify_against_reports.py`, `scripts\README.md`. `02_results_unavailable.md` was **not** created: genuine, comparable outcome data exist (24 real runs, 12 tasks × 2 arms, 0 mock), so Figure 2 is drawn from them.

**Automated cross-check:** `python -B scripts\verify_against_reports.py` → 16/16 PASS (results recomputed from `results.jsonl` and compared with the numbers stated in `P2C_MAIN_EXPERIMENT.md`, `P2A_LOCAL_VERIFICATION.md` and the paper draft). All three images were also inspected visually after the final render; overflow/overlap problems found in earlier renders were fixed.

## Figure 1 — Research methodology

**Shows:** task input → agent turn → exact-string edit → (arm 2 only) harness-run tests → run end → recorded outcome, for `arm1_basic` and `arm2_test_guided`, plus the three optional arms labelled "NOT run".

| Claim in figure | Source |
|---|---|
| arm1: tools read_file/replace_in_file/submit, no test execution; arm2: same tools, `auto_test: true`; no submit gate, no graph in either | `configs\arm1_basic.json`, `arm2_test_guided.json` (script asserts these) |
| Budgets 10 turns / 14 tool calls / 3 format errors / 900 s; T 1.0, top-p 0.95, top-k 64, ≤700 new tokens | `configs\common.json` (read at render time) |
| Tests run "before the 1st step and after every applied edit"; model sees fail count + first failure, last ≤8 lines; cannot skip | `P2C…` validity checks; `harness\workspace.py::feedback_text` (`[-8:]`, ≤900 chars); `agent.py` (initial run, then after edits) |
| Exact-string replace, 'old' must match once; syntax-error edits rejected | `P2C…` failure analysis (41 no-match, 4 syntax-rejected); protocol §3 |
| 12 tasks, seed 20261107, 28 eligible of 31 scanned, 90 tests, pinned commit `4257f44b…` | `manifest\task_manifest.json` (read at render time) |
| Reference solution not in workspace; trace scan found none | `workspace.py::make_workspace` (copies only 5 files); `P2C…` validity checks; self-test |
| Optional arms 2b/3b/3 specified, not run | protocol §2 and `configs\`; script asserts only arm1/arm2 have result rows |
| `--reasoning off`, JSON-in-text actions, 1 seed, hash-frozen before main run | `P2B…`, protocol §3, `run_meta.json`, `FREEZE.sha256` |
| Primary metric `resolved_final_state`; paired by task; only H1 confirmatory | protocol §1, §6, §7 |

**Limitations:** it is a diagram of the *design as implemented*; the one text sentence "expected near-vacuous on single-function files" for arm 3 is the protocol's own prediction (H3), not a result. Context size "8192" is from `common.json` (`model_context_tokens_expected`) and the server log. The figure does not show the temperature mismatch in the frozen protocol document (T=0.7 text vs 1.0 used); that deviation is shown in Figure 3.
**Ready for Kaggle upload:** yes (content).

## Figure 2 — Results comparison

**Shows:** resolved-task blocks (12 per arm), counts with exact 95% intervals, the four configurations that were **not run** as dashed empty placeholders with no values, a 12-task × 2-arm table of final failing/total tests with end reason, and a paired-outcome note.

| Value in figure | Source / recomputation |
|---|---|
| arm1 0/12, arm2 1/12 resolved (`find_in_sorted`) | `results\main_seed1\results.jsonl`, recomputed; matches P2C |
| 24 runs, 0 mock, 0 errors, seed 1 | same file; script asserts |
| per-cell "failing/total" and S/T/F end code | `final_tests`, `end_reason` per row; compared with the P2C per-task table |
| "buggy" column | `task_manifest.json` `n_failing_on_buggy` / `n_tests` |
| ▼ worse than baseline: arm1 3 tasks, arm2 2 tasks | recomputed; matches P2C text (`is_valid_parenthesization`, `pascal`, `quicksort`; `kth`, `quicksort`) |
| 95% exact intervals 0.0–26.5% and 0.2–38.5% | Clopper–Pearson computed in `_common.py`; same values as in the paper draft |
| Paired outcome 0/0/1/11; sign test p = 1.0 | counted from rows; exact two-sided binomial on 1 discordant pair |
| Pilot flatten/arm2 resolved, not in main run | `results\pilot_p2b\results.jsonl` vs main (computed, not hand-entered) |

**Limitations / honest framing:**
- Single seed, 12 tasks, one model: the figure states "no detectable effect" and "neither arm is shown to be better"; it does not claim superiority.
- The sign-test p-value and Clopper–Pearson intervals are computed by the figure script (simple exact arithmetic), not by `harness.summarize`. The harness' bootstrap interval (+8.3 pp, [0.0, +25.0]) is deliberately not drawn, as it is degenerate with one discordant task.
- "Untested configurations" are shown only as labelled empty placeholders; no bar, number or estimate is attached to them.
- Pilot runs are mentioned in text but not plotted or pooled.
**Ready for Kaggle upload:** yes (content).

## Figure 3 — Reproducibility evidence

**Shows:** (A) freeze check, (B) manifest funnel, (C) run metadata, then two visually separated evidence classes: the **mock self-test** (amber, "structural test, no Gemma") and **real Gemma inference** (cyan, `is_mock=false`).

| Value in figure | Source / recomputation |
|---|---|
| 19/19 frozen files match | SHA-256 of every file recomputed at render time against `FREEZE.sha256` |
| frozen at 2026-11-07T23:03:43Z; FREEZE file hash `5f3095c1…fbe35` | `runtime\logs\freeze_time_utc.txt`; SHA-256 of `FREEZE.sha256` (matches P2C) |
| T=0.7 in frozen protocol text vs T=1.0 in configs | script asserts both strings (`EXPERIMENTAL_PROTOCOL.md`, `common.json`) |
| 31 scanned → 28 eligible → 12 sampled, 90 tests, seed 20261107, commit `4257f44b…fcebf` | `task_manifest.json` |
| model alias, quant, GGUF SHA `fa401b55…c6634`, platform, Python, harness version, seeds | `run_meta.json` |
| ctx 8192, 6 threads, CPU, model file path, 127.0.0.1 | parsed from `runtime\logs\server_p2c.err.log` |
| Mock: 23 PASS / 0 FAIL, per-policy counts (oracle 6, noop 5, garbage 2, graphprobe 3, runtests 3, other 4) | parsed line by line from `results\selftest_mock_log_2026-11-07.txt` |
| 24 main runs / 4 pilot runs, 0 mock, 24 / 4 traces | `results.jsonl` flags, trace file counts |
| 221 llama-server requests = 221 recorded turns | count of "processing task" lines in `server_p2c.err.log` vs sum of `turns` (106 + 115) |
| results.jsonl hashes `56a7f4ab…648eb`, `c4b63098…7d25e` | recomputed; match P2B/P2C |
| 3 of 4 pilot configs reproduced exactly (patch, turns, tokens); config hashes identical; the 4th differs only in memory addresses in the first prompt | recomputed: same-length prompts differing in exactly 8 characters, all hex digits |

**Limitations:**
- The freeze is a self-attested local hash list, as the figure says; it proves the files did not change after the list was made, not when the list was made.
- The mock log was produced in P1 on the relocated layout; I did not re-run the self-test. The P2A report records a fresh Windows run with the same 23/0 count, but only the saved log file is the figure's source.
- The "workspace / baselines" bar groups the four untagged PASS lines (no-reference check and three baseline failing counts).
- The request-count check covers the main run only (the pilot used another server session).
- llama.cpp `b12192 (commit 9f0e5098a)` and the hardware/machine label come from the P2A–P2C reports, not a machine-readable file (marked in panel C). Peak memory was never measured.
- The figure makes clear that mock = structural test, not model performance; the only behavioural measurement shown is the 1/12 vs 0/12 result with "not significant". No terminal screenshot or log excerpt was fabricated; the visuals are tables, bars and counts built from parsed values.
**Ready for Kaggle upload:** yes (content).

## Cross-cutting checks

- **No endorsement/score claims:** every figure carries the footer "Independent research figure … Not an official Google or Kaggle result; no competition score is implied." No Google or Kaggle logos or branding are used; "Gemma 4" appears only as the model name.
- **Style:** dark-navy background, cyan/teal accents, amber for mock/not-run/caution, coral/red-muted for failed; DejaVu Sans; 16:9.
- **Consistency with the draft (`GEMMA4_PAPER_DRAFT_V1.md`):** counts, intervals, p-value and regression lists agree.

## Open items before upload

1. **Kaggle Media Gallery upload specs are unverified** (accepted formats, maximum file size, whether a 16:9 ratio or a particular cover-image size is required). A web search returned nothing from Kaggle, and the competition pages are not readable by automated fetch (see P3A). Check the upload dialog in a logged-in Kaggle session. If a size cap applies, re-export at a lower resolution (change `DPI` in `scripts\_common.py`) or convert to JPEG.
2. Author review of all captions and the figure titles; decide which figure is the cover image (Figure 1 is the most self-explanatory).
3. If the draft changes (e.g. seeds 2–3 are run), re-render: Figure 2 and 3 update from the files automatically, but Figure 1's guard will stop if optional arms ever get result rows, and the text of Figure 2's footnote assumes the numbers above.
4. Stale statements elsewhere (not edited, per the restrictions): `paper\results\README.md` and `experiments\p1_harness\README.md` still say "No experimental results exist / no real-model results yet"; they predate P2B/P2C. Figures do not rely on those sentences, but the claim should not be copied into the submission.

## Verdict

| Image | Content verified against sources | Ready for Kaggle upload |
|---|---|---|
| 01_research_methodology.png | yes | **Yes**, pending the unverified upload specs |
| 02_results_comparison.png | yes (16/16 automated checks + visual) | **Yes**, pending the unverified upload specs |
| 03_reproducibility.png | yes | **Yes**, pending the unverified upload specs |
