# P2C — Controlled 12-Task Experiment (seed 1)

Date: 2026-11-07 (work 18:02–19:01 ET, cutoff 19:15 respected). Local CPU only. No GPU, paid API, Kaggle submission, Git, or Developer Agent changes. Server stopped and verified exited (0 `llama-server` processes; port 8080 closed).

**Single seed, 12 tasks, one small model. Preliminary descriptive results only; no confirmed improvement is claimed.**

- EXPERIMENT_FROZEN: YES, at 2026-11-07T23:03:43Z (self-attested local list; no third-party timestamp) — `experiments\p1_harness\FREEZE.sha256` (19 files, SHA-256 of that file `5f3095c1…fbe35`), created by `python scripts/freeze.py > FREEZE.sha256` *before* the main run. Post-run `freeze.py --check`: **UNCHANGED since freeze**.
  Recorded decisions: (1) `--reasoning off` (llama-server default `auto` produced a reasoning trace that consumes the 700-token budget; see P2B); (2) temperature 0.7 → **1.0** per the Google model card (P2B; original in `runtime\p1_originals\`); top_p 0.95, top_k 64 unchanged. Caveat: `docs\EXPERIMENTAL_PROTOCOL.md` (frozen, unmodified) still states T=0.7 and the `common.json` `_note` documents the change; the paper must state the actual value used (1.0). `FILE_MANIFEST.md` hash for `common.json` is superseded.
- MODEL_AND_RUNTIME: Google `gemma-4-E2B-it-qat-q4_0-gguf` (`gemma-4-E2B_q4_0-it.gguf`, SHA-256 `fa401b55…c6634`, re-verified before the run, identical to P2B); llama.cpp b12192 (commit 9f0e5098a), CPU, command line verified from the process: `-m models\gemma-4-E2B_q4_0-it.gguf --host 127.0.0.1 --port 8080 -c 8192 -t 6 -np 1 -ngl 0 --no-webui --reasoning off --alias gemma-4-e2b-it-qat-q4_0` (same alias/options as P2B; `/v1/models` reports n_ctx 8192, Q4_0). Budgets identical across arms: 10 turns, 14 tool calls, 3 format errors, 700 new tokens, 900 s.
- P2B preserved: `results\pilot_p2b\` untouched (results.jsonl SHA-256 `c4b63098…d25e`, 4 traces), all 4 rows `is_mock=false` (genuine llama-server inference). New outputs in `results\main_seed1\` (`results.jsonl` SHA-256 `56a7f4ab…48eb`, `run_meta.json`, 24 traces with raw responses and patches).
- RUNS_COMPLETED: 24/24 (12 tasks × 2 arms × seed 1); all `is_mock=false`; no backend errors.
- BASIC_TASKS_RESOLVED (arm1_basic): **0/12**.
- TEST_GUIDED_TASKS_RESOLVED (arm2_test_guided): **1/12** (`find_in_sorted`; final tests 7/7, AST equal to reference, submitted).
- PAIRED_COMPARISON: both resolved 0; only arm1 0; only arm2 1; neither 11. With 1 discordant pair out of 12 this is statistically uninformative (no test is meaningful). Both arms are at floor for this model/budget on most tasks.

## Per-task outcomes (final tests failing / total, end reason)
| Task | arm1 | arm2 |
|---|---|---|
| find_in_sorted | 2/7 fail, submitted | **0/7 pass**, submitted |
| flatten | 6/7, max_turns | 6/7, max_turns |
| get_factors | 10/11, submitted | 10/11, max_turns |
| is_valid_parenthesization | 3/3, max_turns | 1/3, submitted |
| kheapsort | 3/4, max_turns | 3/4, max_turns |
| kth | 4/7, max_turns | 5/7, max_turns |
| lis | 4/12, max_turns | 4/12, max_turns |
| max_sublist_sum | 4/6, submitted | 4/6, max_turns |
| pascal | 5/5, max_turns | 4/5, max_turns |
| possible_change | 9/10, submitted | 9/10, max_turns |
| powerset | 4/5, format_abort | 4/5, max_turns |
| quicksort | 13/13, submitted | 13/13, max_turns |

Baseline failing counts on the unmodified buggy programs (from `task_manifest.json`): find_in_sorted 2/7, flatten 6/7, get_factors 10/11, is_valid_parenthesization 1/3, kheapsort 3/4, kth 4/7, lis 4/12, max_sublist_sum 4/6, pascal 4/5, possible_change 9/10, powerset 4/5, quicksort 1/13. Comparing final to baseline: unresolved runs mostly equal the baseline (no net progress), but several runs **made things worse** — arm1: is_valid_parenthesization (1→3), pascal (4→5), quicksort (1→13); arm2: kth (4→5), quicksort (1→13). No unresolved run improved on baseline. (This comparison was added after an initial draft that used wrong baselines; verify against `results.jsonl` `final_tests`.)

## Aggregate measures
| Measure | arm1_basic | arm2_test_guided |
|---|---|---|
| Resolved (final state) / submitted-and-resolved | 0 / 0 | 1 / 1 |
| AST-equal to reference | 0 | 1 |
| Submitted (called `submit`) | 5 | 2 |
| End: max_turns / format_abort | 6 / 1 | 10 / 0 |
| Final-state syntax errors | 0 | 0 |
| Format errors (no parseable JSON) | **5** (3 aborted `powerset`) | **0** |
| Unknown-tool calls | 0 | 0 |
| Test executions | 0 (by design) | 24 (initial + after-edit, harness-triggered) |
| Tool calls | 101 | 115 |
| Edit attempts / failed edits | 24 / 15 | 43 / 31 |
| Runs with non-empty final diff | 4 | 6 |
| Turns | 106 | 115 |
| Wall time total / mean per run | 519 s / 43.3 s | 576 s / 48.0 s |
| Tokens prompt / completion | 145,249 / 6,544 | 187,721 / 6,884 |
| Context truncations | 0 | 0 |
Runtime: arm2 ≈ 11% more wall time (extra turns, test runs of ~0.4–0.9 s each are negligible); whole experiment ≈ 18 min. All numbers computed from `results.jsonl`; script `runtime\analyze_p2c.py`.

## Failure analysis
- Dominant failure for both arms: **edit application**. 41 of 47 error messages were "`old` matched 0 times; must match exactly once (check indentation)" — the E2B model's `old` text frequently did not reproduce the file exactly (whitespace/indent), and arm2's extra edit attempts mostly failed this way (31/43). Four more were edits rejected for creating a syntax error; one lacked `new`.
- Arm2 tends to keep editing until the turn budget ends (10/12 hit `max_turns`) while arm1 more often submits an unverified or no-op change (e.g., `find_in_sorted`: `return -1`→`return -1`, 0 diff lines). Arm2 submitted only twice.
- Final test success vs reference equivalence: the single resolved run is AST-equal to the reference (`mid + 1`); no run passed tests without matching the reference, so no "plausible but different fix" cases occurred.
- Context was never truncated; format errors occurred only in arm1 (is_valid_parenthesization 1, kth 1, powerset 3 → abort).

## Reproducibility observation (not a planned test)
The main run repeated the four P2B pilot configurations under identical settings and seed. **Three of four were byte-identical** (same patch, same turns). **One differed**: `flatten`/arm2 resolved in the pilot (6 turns) but not in the main run (10 turns, `max_turns`). So single-seed outcomes on this setup are not fully reproducible (likely CPU/threading or prompt-cache numerics; cause not investigated), and the headline "arm2 solved 2/2 pilot tasks" did not hold. Seed-to-seed variance must be measured before any claim.

## Validity checks
- Reference solutions: `make_workspace` copies only `conftest.py`, the buggy program, the test file, `load_testdata.py` and the test JSON; `read_file` is confined to the workspace. A scan of all 24 traces found no reference-solution content shown to the model. Two scan hits were checked and are false positives: `correct_python_programs` appears only as an import line inside the test file the model read (directory not copied, no content), and `first, *rest = arr` is in the buggy `powerset.py` itself.
- Information parity: both arms get identical system-prompt base, task text, workspace files and budgets. The test file and test data are readable by **both** arms (the prompt names them; arm1 is told to reason from them). Intentional difference: arm2 additionally receives harness-run test output (pass/fail counts and the first failure's last ≤8 traceback lines) before the first step and after every applied edit, via the same `feedback_text` function; it cannot skip or alter it. Arm1 never executes tests. Note arm2's initial test result also reveals which tests fail, and prompt lengths differ accordingly (prompt tokens +29%).
- No fabricated or substituted results: all rows come from the harness against the live llama-server, `is_mock=false`, with raw traces; mock outputs were not used.
- Freeze: UNCHANGED after the run.

- FORMAT_ERRORS: arm1 5, arm2 0 (see above).
- RUNTIME: 24 runs, 1,095 s summed wall time (arm1 519 s, arm2 576 s), ~18 min wall.
- PROTOCOL_DEVIATIONS: (a) T=1.0 vs protocol-document 0.7 (documented; protocol doc not edited); (b) `--reasoning off` server flag (not default); (c) arms 2b/3/3b not run (this phase specified arm1 vs arm2 only; protocol's 3-seed design not executed); (d) 1 seed instead of 3; (e) harness-order randomisation per task is the harness default (not a deviation); (f) peak memory not measured; (g) `llama-server` b12192 pre-release build; (h) the P2B pilot used the unfrozen config (same values), documented in P2B.
- RECOMMENDATION_FOR_ADDITIONAL_SEEDS: YES — run seeds 2 and 3 for the same two arms (~36 min for both, estimated from this run) before any inference, because (i) one pilot case was non-reproducible, (ii) the effect is 1/12 vs 0/12, and (iii) the protocol specifies 3 seeds. Consider as separate, labelled changes (not mid-experiment): a higher turn budget or an edit-format change, since 41 edit failures suggest the budget/tool interface, not test feedback, bounds this model.
- READY_FOR_PAPER_ANALYSIS: PARTIALLY. Data and integrity checks are sound for a descriptive single-seed table and failure analysis. Not sufficient for any comparative claim; needs ≥3 seeds, a paired test, and a hand audit of resolved runs (only one so far, already AST-equal).
- NEXT_ACTION: With your approval, restart the same server command and run `python -B -m harness.run_experiment --qb-root _scratch\QuixBugs --out results\main_seed23 --arms arm1_basic arm2_test_guided --seeds 2 3 --model-id gemma-4-e2b-it-qat-q4_0 --quant q4_0-gguf --gguf-sha256 fa401b55b07ee70a54c6dae3903c783a6e65064312529ea57175cb5f8dec6634` from `paper\experiments\p1_harness\` (frozen files unchanged), then `python -B -m harness.summarize` and a re-check with `freeze.py --check`.
