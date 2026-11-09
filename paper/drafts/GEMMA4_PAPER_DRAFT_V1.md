<!-- DRAFT-STATUS-BEGIN (excluded from paper word count)
GEMMA4_PAPER_DRAFT_V1 — written in Phase P3A from saved results only (results/main_seed1, results/pilot_p2b).
Author must read, verify and own every sentence. [AUTHOR] markers = needs author input. See reports/P3A_SUBMISSION_READINESS.md.
DRAFT-STATUS-END -->

# Does Harness-Triggered Test Feedback Help a Small Local Code-Repair Agent? A Single-Seed Pilot with Gemma 4 E2B

[AUTHOR]

## Abstract

Small language models can run locally, but it is unclear which scaffolding helps them act as coding agents. We ask whether deterministic, harness-triggered test feedback changes the repair rate of Gemma 4 E2B (QAT Q4_0 GGUF, llama.cpp, CPU only) on QuixBugs Python bugs. We compared a basic agent that never runs tests with a test-guided agent that receives test output before its first step and after every applied edit. Both used the same prompt, tools and budgets. We ran 12 tasks with one seed, using a protocol and harness hashed before the run.

The basic agent repaired 0 of 12 tasks and the test-guided agent repaired 1 of 12. Only one task differs between the arms, so these data show no detectable effect of test feedback: an exact sign test gives p = 1.0, and the 95% bootstrap interval for the paired difference has a lower bound of zero. Most failures came from the edit interface: 41 of 46 rejected edits were exact-string mismatches, and 39 of those differed from the file only in whitespace. A four-run pilot that suggested 2/2 versus 0/2 did not reproduce, because one pilot trajectory diverged in the main run. We report this as a descriptive, inconclusive pilot, not as evidence of improvement.

## 1. Research question and motivation

Locally run models are attractive for private, offline and low-cost development work, but small models are unreliable agents. Execution feedback is a cheap, deterministic signal that needs no extra model calls. Prior work shows that it can help larger models, and that its value depends on how good the feedback is [1–3]. It is unknown whether the same holds for the smallest Gemma 4 variant under a strict token and turn budget.

Our primary hypothesis (H1) was that harness-triggered test feedback raises the final-state resolve rate relative to an agent that gets no test execution. It was the only confirmatory hypothesis, and a null or negative result was declared reportable in advance. The contribution of this paper is deliberately modest: a small, fully traced and reproducible comparison, plus a failure analysis that identifies where a very small model breaks down.

## 2. Related work

Self-Debug shows that execution feedback and self-explanation improve code generation, with the largest gains when unit tests are available [1]. Reflexion uses verbal reflection on feedback signals, including unit-test results, to improve later attempts [2]. Olausson et al. find that once the cost of extra samples is counted, self-repair gains are modest, uneven and limited by feedback quality [3]. This motivates our focus on a cost-aware, descriptive account. SWE-agent shows that the design of the agent–computer interface strongly affects outcomes [4], and Agentless shows that a simple localise–repair–validate pipeline can compete with complex agents [5]. Our finding that the edit interface dominates failure is consistent with the former, though we did not test it.

The closest work is Toeda's pre-registered study of scaffolding across Gemma 4 capacities on public competition tasks [6]. According to its Zenodo record, the study covers E4B, 12B and 26B-A4B (not E2B), uses 104 tasks and five seeds, and reports that a maximal scaffold raised E4B from 10.0% to 15.4% resolved. We did not obtain the study's scaffold details, so we do not claim novelty over it. Our work differs in model (E2B), benchmark (single-function QuixBugs repair), intervention (test feedback only) and scale (one seed). We make no claim that our results agree or disagree with [6].

## 3. Methodology

**Tasks.** We used QuixBugs [7] at pinned commit `4257f44b…`. Ten graph-based programs were excluded by rule. Of 31 programs scanned, 28 were measured eligible (the buggy version fails its tests and the reference passes, each within 20 s); three were excluded because the buggy version hit the timeout (infinite loops). We drew 12 programs with a seeded sampler (seed 20261107). The 12 tasks have 90 tests in total. The agent sees the buggy file, its docstring, the pytest file and the JSON test data. Reference solutions are never in the workspace; a scan of all 24 traces found none shown to the model.

**Arms.** Both arms use the same system prompt, task text, workspace and tools (`read_file`, `replace_in_file`, `submit`) and the same budgets: 10 turns, 14 tool calls, 3 format errors, 700 new tokens per turn, 900 s per run.

| Arm | Test execution |
|---|---|
| basic (arm 1) | None |
| test-guided (arm 2) | Harness runs tests before the first step and after every applied edit; the agent cannot skip or alter the result |

Arm 2 therefore changes both the information available and the control flow. The agent is shown the pass/fail count and the last lines of the first failure. A separate arm with agent-initiated testing was specified but not run.

**Agent protocol.** The model emits one JSON object per turn, parsed from plain text rather than native function calling, so that the arms behave identically on any runtime. Edits are exact-string replacements that must match once; edits that create a syntax error are rejected.

**Metric.** The primary outcome is `resolved_final_state`: the official QuixBugs tests pass on the final file. We also record abstract-syntax-tree equality with the reference, end reason, edits, tokens and wall time.

**Pre-specification.** Protocol, configurations, prompts, task manifest, schema and harness code (19 files) were hashed into `FREEZE.sha256` at 2026-11-07T23:03:43Z, before the main run. This is a self-attested local list with no third-party timestamp. A post-run check reports all 19 files unchanged. Two decisions preceded the freeze and followed the pilot: `--reasoning off` (the default produced a reasoning trace that consumed the token budget) and temperature 1.0 (the model card's recommendation). The frozen protocol document still states temperature 0.7; the value actually used was 1.0.

## 4. Experimental environment

Model: Google `gemma-4-E2B-it-qat-q4_0-gguf` [8], file `gemma-4-E2B_q4_0-it.gguf` (SHA-256 `fa401b55…c6634`). Runtime: llama.cpp `llama-server` build b12192 (commit 9f0e5098a) [9], CPU only, with `-c 8192 -t 6 -np 1 -ngl 0 --reasoning off`. Hardware: Dell Inspiron 15 3535, AMD Ryzen 5 7530U (6 cores/12 threads), 63.4 GB RAM, Windows 11. Sampling: temperature 1.0, top-p 0.95, top-k 64; the per-turn seed is `seed × 1000 + turn`. We used one seed (1). No GPU, cloud service or paid API was used. The whole experiment took about 18 minutes (24 runs, 1,095 s summed wall time). The 4-run pilot used the same settings before the freeze.

## 5. Results

All 24 runs completed with real inference and no backend errors.

**Headline.** Arm 1 resolved 0/12 tasks and arm 2 resolved 1/12 (`find_in_sorted`; 7/7 tests pass, AST-equal to the reference fix `mid + 1`). Cross-tabulation: both resolved 0, only arm 1 0, only arm 2 1, neither 11. Exact (Clopper–Pearson) 95% intervals are 0–26.5% for arm 1 and 0.2–38.5% for arm 2. The protocol's paired bootstrap gives +8.3 percentage points with a 95% interval of [0.0, +25.0]; with one discordant task, this interval is a property of the resampling, not evidence. An exact two-sided sign test with one discordant pair gives p = 1.0. We draw no conclusion about the direction or size of any effect.

**Per-task final state** (failing tests / total; baseline = unmodified buggy file).

| Task | Baseline | Arm 1 | Arm 2 |
|---|---|---|---|
| find_in_sorted | 2/7 | 2/7 | **0/7** |
| flatten | 6/7 | 6/7 | 6/7 |
| get_factors | 10/11 | 10/11 | 10/11 |
| is_valid_parenthesization | 1/3 | 3/3 | 1/3 |
| kheapsort | 3/4 | 3/4 | 3/4 |
| kth | 4/7 | 4/7 | 5/7 |
| lis | 4/12 | 4/12 | 4/12 |
| max_sublist_sum | 4/6 | 4/6 | 4/6 |
| pascal | 4/5 | 5/5 | 4/5 |
| possible_change | 9/10 | 9/10 | 9/10 |
| powerset | 4/5 | 4/5 | 4/5 |
| quicksort | 1/13 | 13/13 | 13/13 |

**Process measures** (totals over 12 runs).

| Measure | Arm 1 | Arm 2 |
|---|---|---|
| Resolved / AST-equal | 0 / 0 | 1 / 1 |
| Called `submit` | 5 | 2 |
| Ended by turn limit / format abort | 6 / 1 | 10 / 0 |
| Format errors | 5 | 0 |
| Edit attempts / rejected | 24 / 15 | 43 / 31 |
| Prompt / completion tokens | 145,249 / 6,544 | 187,721 / 6,884 |
| Wall time | 519 s | 576 s |

Arm 2 used about 29% more prompt tokens and 11% more wall time. Arm 1 had all 5 format errors (three ended a `powerset` run); arm 2 had none. No run ended in a syntax error or truncated context.

**Pilot versus main run.** The pilot (first two manifest tasks, both arms) gave arm 2 two resolved tasks and arm 1 none. The main run repeated those four configurations with the same seed and settings. Three runs were byte-identical. `flatten` with arm 2, resolved in six turns in the pilot, was not resolved in the main run (10 turns, turn limit). The initial pilot result therefore did not hold, and the `flatten` pilot success cannot be treated as evidence of an effect.

## 6. Failure analysis

**Edit application dominates.** Of 46 rejected edits, 41 reported that `old` matched zero times, four created a syntax error, and one was malformed. Comparing the failed `old` strings with the actual files after collapsing whitespace, 39 of the 41 no-match calls differ from the file only in whitespace; two contain text absent from the file. In 35 of the 41 calls, the failing `old` string was one the model sent at least twice within the same run. For example, on `lis` arm 2 sent the same `old` line, with more leading spaces than the file has, five times; both arms on `lis` ended at the turn limit. The error message ("check indentation") did not lead to a corrected retry. Because arm 2 applies more edits (43 vs 24), it also suffers more failures (31 vs 15). The binding constraint on this model and interface appears to be the edit format and the turn budget, not the availability of test results. We did not test this by changing the interface.

**Arm behaviour differs.** Arm 2 kept trying until the turn limit (10 of 12 runs) and submitted twice. Arm 1 more often submitted an unverified or empty change; on `find_in_sorted` it submitted `return -1` → `return -1` (zero changed lines).

**Regressions.** Relative to the buggy baseline, the final state was worse in three arm 1 runs (`is_valid_parenthesization`, `pascal`, `quicksort`) and two arm 2 runs (`kth`, `quicksort`); only one run (arm 2, `find_in_sorted`) improved. On `quicksort`, both arms made the identical edit (`pivot = arr[0]` → `arr[len(arr) // 2]`), raising failures from 1/13 to 13/13. In arm 2 the model saw the failing tests after the edit but ended the run at the turn limit without recovering (5 of its 6 edits were rejected). In arm 1, `is_valid_parenthesization` renamed the loop variable without updating its use, so all 3 of 3 tests failed.

**Where the nondeterminism came from.** The one non-reproduced run, `flatten` with arm 2, has a first prompt that differs from the pilot's only in memory addresses (`0x…`) inside the harness-injected failure message (a generator object's repr). It is the only one of the 24 runs whose traces contain such addresses. Identical sampling seeds therefore met different prompts. This shows a source of run-to-run variation inside our own harness. We did not run an experiment to confirm it is the cause of the divergent trajectory.

## 7. Limitations and threats to validity

- **Statistical power.** One seed, 12 tasks, one model, one benchmark. Seeds repeat sampling on the same tasks and do not add independent tasks. A single seed cannot show that one arm is better: at T = 1.0, an identical configuration already produced a different outcome on one task.
- **Floor effect.** Both arms are near zero on most tasks, so the comparison has little room to show a difference.
- **Contamination.** QuixBugs has been public since 2017 and Gemma 4's training data are unknown. Absolute rates are not comparable to unseen benchmarks, and even the single success (a well-known off-by-one) may be memorised.
- **Confounded arm.** Arm 2 differs in information and control flow, and it receives more prompt text. We cannot separate "tests available" from "tests forced".
- **Pilot-informed settings.** The reasoning-off and temperature choices followed the pilot, which used two of the 12 main tasks. Neither was tuned for outcome, but the pilot was not independent of the main run.
- **Self-attested freeze.** The hash list has no external timestamp, and one frozen document (temperature) disagrees with the configuration used.
- **Interface and runtime.** A JSON-in-text protocol rather than native tool calls; a GGUF Q4_0 build on llama.cpp rather than other quantised runtimes; CPU only. The harness is Windows-tested only, and peak memory was not measured. The llama.cpp build is a rolling pre-release.
- **Selection.** Programs with infinite-loop bugs and graph-based programs were excluded.
- **Harness defect.** Process-specific addresses in test feedback (Section 6) make arm 2 runs not exactly reproducible across processes for some tasks.

## 8. Conclusions

In this pilot, harness-triggered test feedback produced no detectable improvement for Gemma 4 E2B on QuixBugs: 1 of 12 tasks was resolved versus 0 of 12, with a single discordant task. The result is compatible with no effect, a small effect and a moderate effect. The more informative finding is where the small model fails. Rejected exact-string edits, most of which were whitespace mismatches that the model repeated, dominated both arms, and several runs made the program worse. An early pilot success did not reproduce. Establishing any effect would require more seeds, a hand audit of resolved runs, and a more tolerant edit interface evaluated as a separately labelled change. All traces, hashes and the harness are available for inspection. [AUTHOR: confirm release location and any AI-assistance disclosure.]

## References

1. X. Chen, M. Lin, N. Schärli, D. Zhou. Teaching Large Language Models to Self-Debug. arXiv:2304.05128 (2023).
2. N. Shinn, F. Cassano, E. Berman, A. Gopinath, K. Narasimhan, S. Yao. Reflexion: Language Agents with Verbal Reinforcement Learning. NeurIPS 2023; arXiv:2303.11366.
3. T. X. Olausson, J. P. Inala, C. Wang, J. Gao, A. Solar-Lezama. Is Self-Repair a Silver Bullet for Code Generation? ICLR 2024; arXiv:2306.09896.
4. J. Yang, C. E. Jimenez, A. Wettig, K. Lieret, S. Yao, K. Narasimhan, O. Press. SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering. NeurIPS 2024; arXiv:2405.15793.
5. C. S. Xia, Y. Deng, S. Dunn, L. Zhang. Agentless: Demystifying LLM-based Software Engineering Agents. arXiv:2407.01489 (2024).
6. T. Toeda. Scaffolding Helps the Smallest Gemma 4 Agent, Not the Larger Ones: run records, pre-registration and analysis code. Zenodo dataset, v1.0.2, 31 Oct 2026. doi:10.5281/zenodo.23813680.
7. D. Lin, J. Koppel, A. Chen, A. Solar-Lezama. QuixBugs: A Multi-Lingual Program Repair Benchmark Set Based on the Quixey Challenge. SPLASH Companion 2017, pp. 55–56. doi:10.1145/3135932.3135941.
8. Google. gemma-4-E2B-it-qat-q4_0-gguf (model card). Hugging Face, revision 675cff42a74c774d6cb76f76d8eacb49b48c9b93.
9. ggml-org. llama.cpp, release b12192. https://github.com/ggml-org/llama.cpp.
