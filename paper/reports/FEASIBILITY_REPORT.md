# P1 Feasibility Report — Gemma 4 Developer Agent Paper Track

Date: 2026-11-07. Scope: research design and feasibility only. No real-model run, no GPU/cloud use, no submission, no Git push; MRI Vision Core and AI Agent Security untouched.

## Bottom line
**Feasible but tight, with a narrow claim.** A fully local, CPU-only, pre-specified comparison of *no-test* vs *harness-triggered-test* Gemma 4 E2B agents on 12 QuixBugs tasks is built and self-tested. Whether it can be *run* in time depends on two things I cannot see from here: your actual CPU/RAM and real inference speed. About 5 days remain before the 2026-11-12 23:59 UTC deadline (as I understand it — verify on Kaggle).

**Recommendation:** run arm1 vs arm2 (E2B, 12 tasks, up to 3 seeds) as the paper's confirmatory core; treat the graph arm as a labelled pilot; state the Toeda overlap openly and make the contribution about *isolating deterministic test feedback with paired statistics*, including a null result if that is what you get. Do not claim novelty beyond that.

## 1. Confirmed (I saw it or measured it)
* Harness runs end-to-end under a scripted mock policy: **SELFTEST PASSED, 23 checks** (oracle resolves every arm; no-op resolves nothing; arm-3 gate rejects 3×; garbage replies end in `format_abort`; graph/test tools are unavailable where they should be; the workspace never contains the reference solution; baseline failure counts match the manifest). *These say nothing about Gemma.*
* Task manifest measured, not assumed: 31 QuixBugs programs scanned at the pinned commit; 28 eligible; 3 excluded for hanging buggy versions (`bitcount`, `find_first_in_sorted`, `sqrt`); 10 graph-based programs excluded by rule; 12 sampled with a recorded seed. Per-file SHA-256 recorded and verified at run time.
* The related Zenodo record by Toeda exists and reports E4B 10.0 % → 15.4 % with code-graph tools + analyzer sub-agent (abstract-level reading).
* Local backend refuses non-loopback URLs; summaries refuse mock rows.

## 2. Estimates (planning numbers, UNVERIFIED)
* E2B Q4_0 weights ≈ 2.9 GB, E4B ≈ 4.5 GB (weights only; add KV cache and runtime).
* Speed on a 4-core Zen 3 CPU: ~5–10 generated tok/s, ~40–100 prompt tok/s → ~3–4 min per run → 36 runs ≈ 2–3 h; 72 runs ≈ 5–6 h; 108 runs ≈ 7 h. Could be off by 2× either way.

## 3. Not verified / unknown
* Official Kaggle Paper Track rules and the main-track HARNESS_README were not readable through my tools; word limit, criteria, deadline and file rules come from secondary descriptions.
* Whether Toeda's scaffolds include test feedback; their task set and harness.
* Exact Hugging Face repo/filenames for official Gemma 4 GGUFs; llama-server flags; how llama-server handles Gemma 4 thinking mode; recommended sampling values.
* Harness behaviour on Windows (developed and tested on Linux).
* Several literature citations are from memory (flagged in LITERATURE_AND_OVERLAP.md).

## 4. Blockers and decisions (in priority order)
1. **You must read the official rules** (and join the Paper Track) — I could not. Also confirm how the 3,000-word limit counts tables/references.
2. **Authorization** to download ~3 GB of model weights and install llama.cpp, and to run local CPU inference.
3. **Machine profile** (`scripts/profile_machine.py`) — RAM decides E2B vs E4B; speed decides 1 vs 3 seeds.
4. **Novelty is weak.** The Toeda record covers "scaffolding helps small Gemma 4 agents". Our angle is narrower and may overlap if their scaffolds include test feedback. Read their record before writing the contribution statement.
5. **Graph arm is nearly vacuous on QuixBugs** (single-function files). Options: pilot-only (recommended), or repository-scale tasks from the competition dev data — which needs your authorization and the official docs.
6. **Validity gaps:** GGUF/llama.cpp ≠ competition w4a16-ct/vLLM; JSON text protocol ≠ native function calling; QuixBugs contamination; 12 tasks → wide CIs.
7. **Deadline risk:** 5 days with an unmeasured inference speed. Step 6 of NEXT_STEPS is the go/no-go gate; shrink scope rather than miss the deadline.

## 5. Deliverables map
| Requested | File |
|---|---|
| Feasibility report | docs/FEASIBILITY_REPORT.md |
| Experimental protocol | docs/EXPERIMENTAL_PROTOCOL.md |
| Baseline agent configuration | configs/*.json, prompts/system_base.md |
| Metrics + task manifest | schema/results_schema.json, manifest/task_manifest.json, scripts/build_manifest.py |
| Paper outline | docs/PAPER_OUTLINE.md |
| Overlap with published research | docs/LITERATURE_AND_OVERLAP.md |
| Next steps for limited inference | docs/NEXT_STEPS_LIMITED_INFERENCE.md |
| Local CPU harness | harness/, scripts/selftest.py |
