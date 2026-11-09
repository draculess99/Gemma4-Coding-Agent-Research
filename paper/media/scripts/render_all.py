"""Render all three Media Gallery figures.   Usage (from this folder):  python -B render_all.py
Requires Python 3.10+ and matplotlib (developed with matplotlib 3.9.2, numpy 2.x).  No network access, no model, no GPU.
Reads (never writes) paper/experiments/p1_harness/**, paper/runtime/logs/*, paper/results/*.  Writes ../*.png only.
"""
import fig01_methodology, fig02_results, fig03_reproducibility

for m in (fig01_methodology, fig02_results, fig03_reproducibility):
    m.main()
