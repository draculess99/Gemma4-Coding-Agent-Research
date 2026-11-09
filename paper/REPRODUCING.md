# Methodology, environment and reproducibility

This file describes how the published numbers were produced, what can be verified without a model, and what is needed to re-run the inference. Every statement here comes from the saved reports (`reports/P2A…P2C`), configs and logs in this repository; where something was **not** recorded it says so.

## 1. Study design (summary)

- **Question:** does harness-enforced, deterministic test feedback change the repair rate of a small local model acting as a code-repair agent, and at what token/time cost?
- **Model:** Google `gemma-4-E2B-it-qat-q4_0-gguf` (file `gemma-4-E2B_q4_0-it.gguf`, 3,349,516,256 bytes, SHA-256 `fa401b55b07ee70a54c6dae3903c783a6e65064312529ea57175cb5f8dec6634`). Hugging Face revision `675cff42a74c774d6cb76f76d8eacb49b48c9b93`; licence stated on the model card as Apache 2.0 (read in P2B; not independently verified here).
- **Tasks:** 12 QuixBugs Python programs, drawn by a seeded sampler (seed 20261107) from the 28 programs measured eligible out of 31 scanned (10 graph-based programs excluded by rule); 90 tests in total. QuixBugs commit `4257f44b0ff1181dedaedee6a447e133219fcebf`. The selection is frozen in `experiments/p1_harness/manifest/task_manifest.json`.
- **Arms run:** `arm1_basic`, `arm2_test_guided` (see the root README). **Specified but not run:** `arm2b_agent_initiated_tests`, `arm3b_test_validated_nograph`, `arm3_graph_test_validated`.
- **Agent protocol:** the model answers each turn with one JSON object calling `read_file`, `replace_in_file` or `submit` (JSON in text, not native tool calling). `replace_in_file` needs `old` to match the file exactly once; edits that create a syntax error are rejected. The reference solution is never copied into the workspace.
- **Budgets (both arms):** 10 turns, 14 tool calls, 3 format errors, 900 s wall, 700 new tokens per turn, context 8192.
- **Sampling:** temperature 1.0, top-p 0.95, top-k 64; per-turn seed = `seed*1000 + turn`; `--reasoning off` on the server.
- **Primary metric:** `resolved_final_state` = the official QuixBugs pytest file passes on the final file. Secondary: AST equality with the reference, end reason, edits and rejected edits, tokens, wall time.
- **Protocol document:** `experiments/p1_harness/docs/EXPERIMENTAL_PROTOCOL.md` (copy in `methodology/`). Only the comparison arm 2 vs arm 1 (H1) is confirmatory.

## 2. Deviations and caveats (read before citing)

| Item | What happened |
|---|---|
| Temperature | The frozen protocol text still says T = 0.7. `configs/common.json` was changed to **1.0** in P2B to match the model card, **before** the freeze; the original is `runtime/p1_originals/common.json.P1_original`. All published runs used 1.0. |
| Reasoning mode | llama-server's default (`--reasoning auto`) produced a reasoning trace that consumes the 700-token budget, so every run used `--reasoning off`. |
| Freeze | `FREEZE.sha256` lists SHA-256 hashes of 19 files (protocol, configs, prompt, manifest, schema, harness code, manifest builder), created 2026-11-07T23:03:43Z, before the main run. It is **self-attested**: no third-party timestamp. `freeze.py --check` reports "UNCHANGED since freeze". |
| Main-run command | The exact command line was not saved verbatim. §4 gives the equivalent command, reconstructed from `run_meta.json` (arms, seeds, model id, GGUF hash) and the pilot command. |
| Pilot vs main | The 4 pilot configurations were repeated in the main run: 3 of 4 reproduced exactly (patch, turns, tokens); `flatten`/`arm2_test_guided` did not (resolved in the pilot, not in the main run). The first prompts of that pair differ in 8 hexadecimal characters: the harness-injected pytest failure text contains process-specific memory addresses. This shows the prompts were not identical; it is **not proven** to be the cause. |
| Tool versions | pytest was not recorded in `run_meta.json`; 9.1.1 is installed on the authoring machine. Peak memory was not measured. |
| Platform | Everything was run on Windows 11 only. Linux/macOS behaviour of the harness is untested. |

## 3. Verify the published numbers (no model, no GPU, no network)

From the repository root, Python 3.10+ (3.12.10 used), standard library only:

```
python -B paper/scripts/verify_published_metrics.py
python -B paper/experiments/p1_harness/scripts/freeze.py --check paper/experiments/p1_harness/FREEZE.sha256
```

The first recomputes the headline results, paired outcome, sign test, intervals, process measures, rejected-edit categories (from traces), results-file hashes and the freeze from the saved files (26 checks). Expected final line: `ALL CHECKS PASSED`. The second must print `UNCHANGED since freeze`.

Harness self-test with scripted **mock** policies (no model; needs `pytest` and a QuixBugs clone, see §5):

```
cd paper/experiments/p1_harness
python -B scripts/selftest.py --qb-root _scratch/QuixBugs        # expected: SELFTEST PASSED, 23 PASS / 0 FAIL
```

Figures (needs `matplotlib==3.9.2`; developed with its numpy dependency):

```
cd paper/media/scripts
python -B render_all.py              # rewrites the three PNGs in paper/media/
python -B verify_against_reports.py  # figure numbers vs reports and draft; expected ALL CHECKS PASSED
```

Re-rendering with matplotlib 3.9.2 produced byte-identical PNGs on the authoring machine.

## 4. Re-run the inference (optional; needs the model)

Requirements: a CPU machine (the authoring machine: Dell Inspiron 15 3535, AMD Ryzen 5 7530U 6C/12T, 63.4 GB RAM; 6 threads used; no GPU). The weights file is 3.3 GB; peak memory use was **not measured**, so no minimum RAM is claimed. The 24 main runs took about 18 minutes of wall time (1,095 s summed per-run time) on that machine.

1. Get llama.cpp release **b12192** (`llama-b12192-bin-win-cpu-x64.zip`; asset SHA-256 `b465952e4df16e77dc74a45224c4bbbed4bb20c05ecadc311c65d9f3ca84eb22`, matching the GitHub release digest). Version string `0.9.0-dev (build 12192, commit 9f0e5098a)`.
2. Download only `gemma-4-E2B_q4_0-it.gguf` from the Hugging Face repository `google/gemma-4-E2B-it-qat-q4_0-gguf` and check its SHA-256 against the value above.
3. Start the server (loopback only; the harness refuses non-loopback URLs):
   ```
   llama-server -m models\gemma-4-E2B_q4_0-it.gguf --host 127.0.0.1 --port 8080 -c 8192 -t 6 -np 1 -ngl 0 --no-webui --reasoning off --alias gemma-4-e2b-it-qat-q4_0
   ```
4. Run, from `paper/experiments/p1_harness/` and with a **new** output directory (an existing one makes the harness skip rows it already has):
   ```
   python -B -m harness.run_experiment --qb-root _scratch\QuixBugs --out results\my_rerun --arms arm1_basic arm2_test_guided --seeds 1 --model-id gemma-4-e2b-it-qat-q4_0 --gguf-sha256 fa401b55b07ee70a54c6dae3903c783a6e65064312529ea57175cb5f8dec6634
   python -B -m harness.summarize results\my_rerun\results.jsonl
   ```
5. Do **not** edit `configs/`, `prompts/`, `harness/`, `manifest/`, `schema/`, `docs/` or `scripts/build_manifest.py`, or `freeze.py --check` will report changes.

Expect differences: outcomes are not guaranteed to be identical across runs, even with the same seeds (see §2, Pilot vs main). A re-run is a replication attempt, not a bit-exact reproduction.

## 5. Environment and dependencies

| Component | Version / source | Needed for |
|---|---|---|
| Python | 3.12.10 (3.10+ should work; only 3.12.10 was tested) | everything |
| harness | `0.1.0-p1`, standard library only | inference runs, self-test |
| pytest | 9.1.1 on the authoring machine | grading, self-test, test-guided arm |
| QuixBugs | **not included**; MIT; `git clone https://github.com/jkoppel/QuixBugs paper/experiments/p1_harness/_scratch/QuixBugs` then `git -C paper/experiments/p1_harness/_scratch/QuixBugs checkout 4257f44b0ff1181dedaedee6a447e133219fcebf` (the harness verifies file hashes against the manifest) | self-test, inference runs |
| llama.cpp | b12192, CPU build, **not included** | inference runs |
| Gemma 4 E2B QAT Q4_0 GGUF | **not included** | inference runs |
| matplotlib | 3.9.2 (+ numpy) | figures only |
| OS | Windows 11 Pro 10.0.26200 | tested platform |

## 6. Provenance of every published number

| Claim | Source of truth | Independent recomputation |
|---|---|---|
| 0/12 and 1/12 resolved, paired outcome, process measures | `experiments/p1_harness/results/main_seed1/results.jsonl` (SHA-256 `56a7f4ab64a65b7ea3ea9aea6f8cd3c21d8bbd69ef5c0b4ad8a5df244e1648eb`), described in `reports/P2C_MAIN_EXPERIMENT.md` | `scripts/verify_published_metrics.py` |
| Rejected-edit categories (41 / 4 / 1) | the 24 traces in `results/main_seed1/traces/` | `scripts/verify_published_metrics.py` |
| 4-run pilot | `results/pilot_p2b/results.jsonl` (SHA-256 `c4b630984b5a40eb88e5a4bf4386d9632945a6a6683a7631fa54665a5d87d25e`), `reports/P2B_INITIAL_INFERENCE.md` | hash and row count in the verifier |
| 221 llama-server requests = 221 recorded turns | `runtime/logs/server_p2c.err.log` | `media/scripts/fig03_reproducibility.py` |
| Mock self-test 23 PASS / 0 FAIL | `results/selftest_mock_log_2026-11-07.txt` (the saved log starts with three comment lines added at transfer time; its body is identical to a fresh run) | `selftest.py` |
| Freeze | `experiments/p1_harness/FREEZE.sha256`, `runtime/logs/freeze_time_utc.txt` | `freeze.py --check` |
| Exact 95% intervals, sign test | computed arithmetic (Clopper-Pearson, exact binomial) | `scripts/verify_published_metrics.py`; the harness's own bootstrap interval (+8.3 pp, [0.0, +25.0]) is degenerate with one discordant task and is not used |

## 7. Data handling notes

- `results/*/traces/*.jsonl` contain the full prompts shown to the model and its raw replies. They contain QuixBugs program text (MIT; see `THIRD_PARTY_NOTICES.md`) and model output, no credentials and no personal data (scanned before publication).
- `.gitattributes` stores `paper/experiments/p1_harness/**`, `paper/results/**` and `paper/runtime/**` byte-exactly (no line-ending conversion), because the frozen hashes were computed on Windows CRLF files. If you copy the files out of Git by other means, preserve the bytes.
