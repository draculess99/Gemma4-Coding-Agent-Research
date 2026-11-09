# P2A — Local Verification and Experimental Readiness

Date: 2026-11-07 | Machine: Dell Inspiron 15 3535 | Paper Track deadline (per P1 docs, secondary source, unconfirmed): 2026-11-12
**No Gemma inference was run. No model or software was downloaded/installed. No scores or findings are claimed.**

## 1. Files verified
All 33 files listed in `reports/FILE_MANIFEST.md` exist: research feasibility report, next-steps report, literature review, protocol (both copies), paper outline, harness (8 modules), 6 configs, prompt, schema, task manifest, 4 scripts, mock log, P1 source archive. Nothing was moved, overwritten or reorganized.
Only the manifest file itself is not in its own table (expected).

## 2. Checksum results
Recomputed SHA-256 and byte size for all 33 rows: **33/33 match, 0 missing, 0 mismatched** (checked before and after the test run).
Additions made by this phase (not in the manifest): `reports/P2A_LOCAL_VERIFICATION.md` (this file) and `experiments/p1_harness/_scratch/QuixBugs/` (see §4). The `__pycache__` dir created by the self-test run was deleted.

## 3. Machine profile
`scripts/profile_machine.py` output: Windows-11-10.0.26200, AMD64 (Family 25 Model 80), 12 logical CPUs, 63.4 GB RAM, Python 3.12.10.
Additional read-only probes:
| Item | Value |
|---|---|
| CPU | AMD Ryzen 5 7530U (6 cores / 12 threads) |
| RAM | 63.4 GB total, ~27.0 GB free at probe time |
| GPU | AMD Radeon integrated (reported 512 MB adapter RAM); not used |
| Disk | C: 1575.8 GB free; D: 1509.1 GB free |
| Python / pytest / git | 3.12.10 / 9.1.1 / present |
| Local model runtimes | **none**: `llama-server`, `llama-cli`, `ollama`, `lms` not on PATH; no `.ollama`, `.lmstudio`, HF cache dirs; no `*.gguf` under user profile or D: (depth ≤4); nothing listening on 8080/8000/11434 |

## 4. Harness tests
- Command (from `paper/experiments/p1_harness/`): `python scripts/selftest.py --qb-root _scratch/QuixBugs`
- QuixBugs was absent locally, so I cloned it (`git clone` with `core.autocrlf=false`, repo `jkoppel/QuixBugs`, checkout of the pinned commit `4257f44b0ff1181dedaedee6a447e133219fcebf`; `git rev-parse HEAD` confirms; working tree clean) into `_scratch/QuixBugs` inside `paper\` (the documented location). This was a network fetch of benchmark data (not a model); flag if you consider it outside "no downloads".
- Result: **SELFTEST PASSED — 23 PASS / 0 FAIL**, same count as P1 (23). Manifest per-file hashes verified on the Windows checkout (no CRLF drift).
- This is **mock validation only**: scripted policies, every row `is_mock`, no Gemma model involved. It shows the grader, edit path, tool gating and workspace isolation work; it says nothing about model behaviour.

## 5. Windows compatibility findings
- Self-test passes on Windows 11 / Python 3.12 with no code change. **No harness modification was made.**
- `profile_machine.py` runs on Windows (uses ctypes `GlobalMemoryStatusEx`; reports total, not available, RAM).
- Caveats: autocrlf must stay off for the QuixBugs clone; `python -I` ignores `PYTHONDONTWRITEBYTECODE`, so `__pycache__` appears in `harness/` after running (delete or use `-B`). Real-model paths (llama-server, HTTP) are untested on Windows.

## 6. Model availability
- **Not available locally**: no GGUF, no llama.cpp. Real runs require both (needs your authorization to download).
- Harness expects: llama.cpp `llama-server` on loopback (non-loopback URLs are refused in code), OpenAI-compatible `/v1/chat/completions`; context ~8192 tokens (`model_context_tokens_expected`); model id/quant/gguf hash are recorded as CLI args.
- Planned variant (P1 docs): Gemma 4 **E2B** QAT Q4_0 (~3 GB); E4B (~4.5 GB) feasible on this machine (63 GB RAM). Exact official GGUF repo ID/filename is **unverified**. A web search returned only third-party repackagers, not Google's card; use an official source.
- Expected memory (estimate, unverified): weights 3–4.5 GB + KV cache at 8192 ctx well under 1–2 GB → comfortably within ~27 GB free. CPU-only inference on the Ryzen 5 7530U.
- **Sampling discrepancy**: `configs/common.json` uses temperature 0.7 (flagged UNVERIFIED defaults). Secondary sources (Unsloth, GGUF repack cards) cite Google's recommended temperature **1.0**, top_p 0.95, top_k 64. Not changed (protocol says freeze whatever is chosen after checking the primary model card). Decide before `freeze.py`.
- Budgets (from `common.json`): max_turns 10, max_tool_calls 14, max_format_errors 3, max_wall_seconds 900/run, max_new_tokens 700, context 24,000 chars, test timeout 30 s.

## 7. Pilot task selection (prepared, not executed)
- Arms: `arm1_basic` (Agent A: read/replace/submit, no test execution) vs `arm2_test_guided` (Agent B: same tools + deterministic harness-run tests initially and after every applied edit, no submit gate).
- Tasks: the first two in the frozen manifest order (selected by the manifest's seeded random sampler, seed 20261107, not hand-picked by me): `quixbugs/find_in_sorted` (7 tests, 2 failing on buggy) and `quixbugs/flatten` (7 tests, 6 failing). `--max-tasks 2` selects them.
- Seeds: 1. Executions: 2 arms × 2 tasks × 1 seed = **4**. Model-sampling seed per turn is `seed*1000+turn`.
- Time estimate (UNVERIFIED, from P1 docs for a 4-core laptop): ~3–4 min/run → ~12–16 min total; this CPU has 6 cores.

## 8. Exact commands for the next experiment (needs your authorization; none run)
From `D:\KAGGLE_Projects\Gemma4_Developer_Agent\paper\experiments\p1_harness\`:
```
# 1. After you authorize and obtain llama.cpp (CPU Windows build) + the official Gemma 4 E2B QAT Q4_0 GGUF:
certutil -hashfile <gguf> SHA256
llama-server -m <gguf> --host 127.0.0.1 --port 8080 -c 8192 -t 6 --jinja     # verify flags with --help
# 2. Decide/verify sampling from the primary model card; edit configs\common.json if changing; re-run selftest
python scripts\selftest.py --qb-root _scratch\QuixBugs
# 3. Freeze
python scripts\freeze.py > FREEZE.sha256
# 4. Pilot (4 runs)
python -B -m harness.run_experiment --qb-root _scratch\QuixBugs --out results\pilot_p2b --arms arm1_basic arm2_test_guided --seeds 1 --max-tasks 2 --model-id <exact name llama-server loaded> --gguf-sha256 <hash>
# 5. Inspect traces in results\pilot_p2b\traces\ ; pass criteria in NEXT_STEPS_LIMITED_INFERENCE.md §5
```
(NEXT_STEPS §5 uses 2 tasks for the smoke test; the harness README's example uses 3.)

## 9. Outstanding blockers
1. No llama.cpp and no Gemma 4 GGUF locally; download requires your explicit go-ahead.
2. Official GGUF repo ID/filename and llama-server flags unverified.
3. Sampling defaults (T=0.7) disagree with secondary sources (T=1.0); need primary-source decision before freezing.
4. Thinking-mode behaviour under llama-server with 700 max tokens untested.
5. `FREEZE.sha256` not yet created (intentionally).
6. Paper Track rules/deadline/word limit unconfirmed from the official page (P1 note).
7. Literature citations marked FROM MEMORY and the Toeda Zenodo check remain open (P1).

## 10. Status
Local verification complete. Pilot is **prepared but not runnable** until blockers 1–3 are resolved. Phase P2A stops here.
