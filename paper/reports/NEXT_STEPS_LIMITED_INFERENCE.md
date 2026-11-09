# Exact Next Steps for a Limited Gemma Inference Experiment (needs your go-ahead)

Nothing below has been run. Everything is local CPU, loopback only, no paid calls. Items marked **(verify)** are things I could not confirm in P1 — check them against the live page/`--help` output before relying on them.

## 0. Decisions needed from you first
1. Join the Paper Track on Kaggle and read the official rules and (for the main track) HARNESS_README. Confirm word limit, deadline and counting rules.
2. Authorize local model download (~3 GB for E2B Q4_0; ~4.5 GB for E4B) and installing llama.cpp. Confirm there are no data-use constraints on your connection.
3. Decide the scope. **Recommendation:** primary confirmatory pair arm1 vs arm2, 12 tasks, 3 seeds (72 runs); arm3 only as a labelled pilot; E2B as the model.

## 1. Profile the machine (2 min)
`python scripts/profile_machine.py > results/machine_profile.json` and send me the output (or read it yourself): the Inspiron 15 3535 ships with different Ryzen/RAM variants, so CPU model and RAM are unknown to me. Rule of thumb: ≥16 GB RAM → E4B possible; 8 GB → E2B only.

## 2. Get QuixBugs at the pinned commit
```
git clone https://github.com/jkoppel/QuixBugs _scratch/QuixBugs
git -C _scratch/QuixBugs checkout 4257f44b0ff1181dedaedee6a447e133219fcebf
pip install pytest
python scripts/selftest.py --qb-root _scratch/QuixBugs    # must print SELFTEST PASSED
```
(This is a clone only; do not push anything.) The harness verifies per-file hashes and stops on mismatch (Windows line-ending changes would trigger that — set `core.autocrlf=false` before cloning.)

## 3. Install llama.cpp and get the model
* Use the official llama.cpp release for Windows (CPU build) **(verify current release name)**.
* Download the Gemma 4 E2B instruction-tuned QAT Q4_0 GGUF from the official Google/ggml-org Hugging Face repo **(verify exact repo ID and filename; do not use an unofficial re-quant)**. Record its SHA-256 (`certutil -hashfile <file> SHA256`).
* Start the server on loopback only, e.g. `llama-server -m <gguf> --host 127.0.0.1 --port 8080 -c 8192 -t 4 --jinja` **(verify every flag with `llama-server --help`; set `-t` to physical cores).** Confirm in the log how Gemma 4's thinking mode behaves and record it.

## 4. Check sampling defaults
Read the Gemma 4 model card for recommended sampling. Edit `configs/common.json` if needed, then re-run the self-test.

## 5. Smoke test (≈15 min)
```
python -m harness.run_experiment --qb-root _scratch/QuixBugs --out results/smoke --arms arm1_basic arm2_test_guided --seeds 1 --max-tasks 2 --model-id <exact model name> --gguf-sha256 <hash>
```
Open two files in `results/smoke/traces/` and read them. Pass criteria: replies are parseable JSON actions (format errors < 20 % of turns), edits apply, no thinking text floods the 700-token limit, `is_mock` is false.

## 6. Timing pilot and go/no-go (≈1 h)
Run 3 tasks × 3 arms × 1 seed. Compute mean wall seconds per run. **Planning estimate, UNVERIFIED:** 3–4 min/run for E2B Q4_0 on a 4-core Zen 3 laptop → 36 runs ≈ 2–3 h, 108 runs ≈ 7 h.
* Go for 3 seeds if mean ≤ 5 min/run for arms 1–2 (≈ 72 runs ≈ 6 h).
* If 5–10 min/run: 1 seed, arms 1–2 only.
* If > 10 min/run or format errors > 50 %: stop and report as a blocker (consider smaller budgets in a re-freeze; never change them silently).

## 7. Freeze, then run
```
python scripts/freeze.py > FREEZE.sha256
python -m harness.run_experiment --qb-root _scratch/QuixBugs --out results/main --arms arm1_basic arm2_test_guided --seeds 1 2 3 --model-id <...> --gguf-sha256 <...>
python -m harness.summarize results/main/results.jsonl
python scripts/freeze.py --check FREEZE.sha256
```
The runner is resumable if the laptop sleeps (plug in power, disable sleep). Do not edit any frozen file mid-run.

## 8. After the run
Hand-audit resolved runs with `ast_equal_reference = false`; write results into the outline with real numbers only; list deviations; finish literature checks; the author writes and submits the paper (I will not submit).

## Timeline against the deadline (2026-11-12 23:59 UTC; today is 2026-11-07)
Day 1: steps 0–6. Day 2: main run (overnight). Day 3: audit + analysis. Day 4: writing. Day 5: buffer and submission. This is tight; if step 6 fails, shrink scope (1 seed) rather than slipping.
