# Experimental Protocol — "Does Deterministic Test Feedback Improve Small Coding Agents?"

Version 0.1 (P1 draft, 2026-11-07). **Status: DRAFT, not yet frozen. No real-model run has been made.**
Freeze with `python scripts/freeze.py > FREEZE.sha256` *before* the first real run; any later edit is a reported deviation.
The freeze is self-attested (a local SHA-256 list, no third-party timestamp) — say so in the paper.

## 1. Question and hypotheses

Question: for a small, locally run Gemma 4 model acting as a code-repair agent, does *harness-enforced, deterministic test feedback* change the repair rate, and at what cost in tokens and wall-clock time?

| ID | Hypothesis | Comparison | Status |
|----|-----------|-----------|--------|
| H1 (primary) | Harness-triggered test feedback raises the resolve rate. | arm2 − arm1, paired by task | confirmatory |
| H2 | A submit gate (submit rejected while tests fail) adds resolves beyond feedback alone. | arm3b − arm2 | exploratory |
| H3 | An AST code graph adds resolves beyond gate+feedback. | arm3 − arm3b | exploratory; **expected to be vacuous on single-function QuixBugs files** |
| H4 | Feedback costs more tokens/time per run; cost per resolved task is reported, not assumed. | all arms | descriptive |
| H5 (optional) | Forced feedback differs from merely *available* testing. | arm2b − arm2 | exploratory |

H1 is the only confirmatory test. All others are labelled exploratory in the paper. A null or negative H1 is a reportable result.

## 2. Arms (all share model, sampling, budgets, system prompt; they differ only in the listed fields)

| Arm | Tools | Harness runs tests? | Submit gate | Graph |
|-----|-------|---------------------|-------------|-------|
| arm1_basic | read_file, replace_in_file, submit | no (no test execution of any kind) | no | no |
| arm2_test_guided | same | yes: initial + after every applied edit | no | no |
| arm2b_agent_initiated_tests (optional) | + run_tests | only if the agent calls run_tests | no | no |
| arm3b_test_validated_nograph (optional ablation) | as arm1 | yes | yes (≤3 rejections) | no |
| arm3_graph_test_validated | + get_code_neighbors, get_code_subgraph | yes | yes (≤3 rejections) | yes (overview + suspects) |

Recommendation for the paper: **run arm1 and arm2 as the confirmatory pair, and arm3 only as a clearly labelled pilot** (see §9). Everything is in `configs/`.

## 3. Model and inference

* Primary: Gemma 4 **E2B** instruction-tuned, QAT Q4_0 GGUF, served by local `llama.cpp` `llama-server` on loopback only (the backend refuses non-loopback URLs). E4B only if RAM is adequate (see NEXT_STEPS).
* One model for all arms. Record exact model file name, GGUF SHA-256, llama.cpp commit/build, flags (`--model-id`, `--gguf-sha256` in `run_experiment`).
* **Threat to validity:** the competition uses `*-qat-w4a16-ct` weights on vLLM; this study uses a GGUF Q4_0. Same model family, different quantised artefact and runtime. Conclusions are about the local GGUF setup.
* Action protocol: one JSON object per turn parsed from plain text (not native function calling), so that all arms behave identically on any runtime. This deviates from Gemma 4's native tool-call format and is a stated limitation.
* Sampling: `configs/common.json` (T=0.7, top_p=0.95, top_k=64, 700 new tokens). **These values are UNVERIFIED defaults** — check the Gemma 4 model card before freezing, then freeze whatever is chosen.
* Thinking mode: handling in llama-server is **unverified**; the smoke test (NEXT_STEPS §5) must establish what the server does and the paper must report it.

## 4. Tasks

* `manifest/task_manifest.json`: 12 QuixBugs Python programs sampled with a recorded seed (20261107) from the 28 programs that were *measured* eligible (buggy fails its pytest file; the reference passes; each under a 20 s timeout) out of 31 scanned. 10 graph-based programs (need Node classes) were excluded by rule. Three further programs (`bitcount`, `find_first_in_sorted`, `sqrt`) were excluded because the buggy version hit the 20 s timeout (infinite loop); the `scan` array logs every program and reason.
* Pinned commit `4257f44b0ff1181dedaedee6a447e133219fcebf`; per-file SHA-256 verified before every run (`verify_pin`).
* License: QuixBugs repository text is MIT with a Quixey provenance note — re-read `legal_notes.txt` and `LICENSE` before redistributing anything; this repo does **not** vendor QuixBugs.
* Selection effect to report: programs whose buggy version hangs were excluded, which removes infinite-loop bugs.
* **Contamination:** QuixBugs is old and public; Gemma 4 has plausibly seen it. Absolute rates are not comparable to unseen benchmarks; only paired arm differences are interpreted, and even those may be compressed by memorisation.
* Agent sees: the buggy file, its docstring, the pytest file and JSON test data. The reference solution is never in the workspace (checked by self-test).

## 5. Budgets (per run, identical across arms)

max 10 turns, 14 tool calls, 3 format errors, 900 s wall, 3000 chars per tool output, 24 000 chars of context (oldest turn pairs dropped, counted), 30 s per test run. Exceeding a budget ends the run; the file's final state is still graded.

## 6. Metrics

Primary: `resolved_final_state` (official QuixBugs pytest file passes on the final file). Reported per task as the mean over seeds, then averaged over tasks.
Secondary: `resolved_submitted`; `ast_equal_reference`; turns; tool calls; prompt/completion tokens; model seconds; wall seconds; test runs; format errors; edit errors; gate rejections; end_reason distribution; diff size.
Audit: every resolved run with `ast_equal_reference = false` is read by hand and labelled correct / test-adequate-but-wrong; counts are reported.
Schema: `schema/results_schema.json`. Mock rows carry `is_mock = true` and are rejected by `summarize.py`.

## 7. Statistics

Unit = task. Paired task-level differences (percentage points) with 95 % bootstrap CI over tasks (10 000 resamples, seed 20261107). With 12 tasks the CIs will be wide; the paper reports them and does not use significance language beyond what the CI supports. No multiple-comparison claims: only H1 is confirmatory. Seeds (1–3) are repeated sampling of the same tasks; they reduce sampling noise but do **not** add independent tasks.

## 8. Execution rules

* Arm order is shuffled per (seed, task) with a recorded seed to spread thermal/background drift.
* Runs are resumable (`run_id` hash); results append to `results.jsonl`; full traces are saved per run.
* Local CPU only. No GPU, no cloud, no paid API, no network except to the loopback server.
* Stage 0 (smoke test, 1–3 tasks, arms 1–2) and Stage 1 (timing pilot) precede the full run; go/no-go thresholds are in NEXT_STEPS. Pilot rows are not pooled into the final results unless the config hash is unchanged and this is stated.

## 9. Known weaknesses (to carry into the paper)

1. 12 single-function tasks → low power, wide CIs; one model; one runtime; one benchmark.
2. Graph arm is nearly vacuous on single-file, single-function tasks. Honest options: report it as a pilot with that caveat, or evaluate it only on repository-scale tasks (the competition dev tasks) **with the user's authorization** and the official harness docs read.
3. Contamination; GGUF vs competition format; JSON protocol; unverified sampling/thinking handling; CPU speed unmeasured; Windows untested.
4. Arm 2 changes information *and* control flow (the model is told test results it cannot skip); arm 2b exists to separate "tests available" from "tests forced".

## 10. Deviations and claims policy

* Any change after freeze is listed in the paper with its reason (`freeze.py --check`).
* No result is stated unless it is in a `results.jsonl` produced by a non-mock run of the frozen harness.
* No novelty claim beyond what LITERATURE_AND_OVERLAP.md supports; no Kaggle leaderboard claims; no claim that local findings transfer to the competition harness.
* The paper text itself must be written and checked by the author.
