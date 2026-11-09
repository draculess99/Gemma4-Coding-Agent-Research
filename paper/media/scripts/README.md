# media\scripts — rendering scripts for the Media Gallery figures

| Script | Output | Reads (read-only) |
|---|---|---|
| `fig01_methodology.py` | `..\01_research_methodology.png` | `experiments\p1_harness\configs\*.json`, `manifest\task_manifest.json`, `results\main_seed1\run_meta.json` + `results.jsonl` (arm guard) |
| `fig02_results.py` | `..\02_results_comparison.png` | `results\main_seed1\results.jsonl`, `results\pilot_p2b\results.jsonl`, `manifest\task_manifest.json` |
| `fig03_reproducibility.py` | `..\03_reproducibility.png` | `FREEZE.sha256` + the frozen files, `runtime\logs\freeze_time_utc.txt`, `runtime\logs\server_p2c.err.log`, `results\selftest_mock_log_2026-11-07.txt`, both `results.jsonl` files, trace files, `run_meta.json`, `common.json` |
| `_common.py` | — | shared palette, drawing helpers, loaders, exact statistics |
| `render_all.py` | all three | — |
| `verify_against_reports.py` | stdout PASS/FAIL | recomputes figure numbers and compares them with `reports\P2C_MAIN_EXPERIMENT.md`, `P2A_LOCAL_VERIFICATION.md` and the paper draft |

## Run
From this folder, with Python 3.10+ and matplotlib:

```
python -B render_all.py
python -B verify_against_reports.py
```

Developed with matplotlib 3.9.2 / numpy 2.x in a throw-away virtual environment kept outside the project (matplotlib was not installed on the machine). Fonts are DejaVu Sans / DejaVu Sans Mono (bundled with matplotlib), so rendering does not depend on system fonts. Use `-B` so no `__pycache__` is written.

No network access, model, GPU or paid service is used. The scripts never write outside `paper\media\`. Each figure script asserts that its inputs are what the figure claims (e.g. no mock rows, only arm1 and arm2 have results, mock log has 0 failures); if the data change, the script stops instead of drawing a misleading picture.

## Values that are not read from a machine-readable file
Only three: llama.cpp build `b12192 (commit 9f0e5098a)`, the hardware label, and the machine name. They come from `reports\P2A…` / `P2B…` / `P2C…` and are marked as report-sourced in Figure 3 (panel C). The server log confirms model file, context size 8192, 6 threads and the 127.0.0.1 listener.
