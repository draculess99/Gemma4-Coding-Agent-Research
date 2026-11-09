"""Shared style, drawing helpers and READ-ONLY data loaders for the Media Gallery figures.

Nothing here writes into experiments/, results/, reports/ or drafts/.  Every number shown in a figure is parsed
from a project file at render time (or computed from such numbers); the few values that exist only in prose
reports are listed explicitly in HARDCODED_FROM_REPORTS below and cross-checked where a log allows it.
"""
from __future__ import annotations

import hashlib
import json
import re
import textwrap
from math import comb
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

# ----------------------------------------------------------------------------- paths
PAPER = Path(__file__).resolve().parents[2]
MEDIA = PAPER / "media"
H = PAPER / "experiments" / "p1_harness"
RES_MAIN = H / "results" / "main_seed1"
RES_PILOT = H / "results" / "pilot_p2b"
LOGS = PAPER / "runtime" / "logs"

# ----------------------------------------------------------------------------- style
BG = "#0A1330"        # dark navy
PANEL = "#111F47"
PANEL2 = "#16285A"
LINE = "#2B427F"
CYAN = "#22D3EE"
TEAL = "#14B8A6"
TEXT = "#E8F0FB"
MUTED = "#93A6C6"
DIM = "#5F7399"
AMBER = "#F5B83D"     # used for MOCK / structural-only / caution
CORAL = "#F87171"     # failed / worse than baseline
SLATE = "#3A4D78"     # unresolved but not worse
FONT = "DejaVu Sans"  # bundled with matplotlib -> identical rendering on any machine
MONO = "DejaVu Sans Mono"

plt.rcParams["font.family"] = FONT
plt.rcParams["savefig.facecolor"] = BG

W, HT = 160.0, 90.0   # drawing units (16:9); 1 unit = 0.1 inch at figsize (16, 9)
DPI = 200             # -> 3200 x 1800 px

DISCLAIMER = ("Independent research figure from the Gemma 4 Paper Track project. Not an official Google or Kaggle "
              "result; no competition score is implied.")

# Values that appear only in prose reports (not in a machine-readable project file).  Shown in figures with a
# source tag; see MEDIA_VERIFICATION.md for how each was cross-checked.
HARDCODED_FROM_REPORTS = {
    "llama_cpp_build": "b12192 (commit 9f0e5098a)",     # reports/P2B_INITIAL_INFERENCE.md, P2C_MAIN_EXPERIMENT.md
    "hardware": "AMD Ryzen 5 7530U (6C/12T), 63.4 GB RAM",  # reports/P2A_LOCAL_VERIFICATION.md
    "machine": "Dell Inspiron 15 3535",                  # reports/P2A_LOCAL_VERIFICATION.md
}


def new_canvas():
    fig = plt.figure(figsize=(16, 9), dpi=DPI, facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(HT, 0)  # y grows downward, like a page
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), W, HT, fc=BG, ec="none", zorder=0))
    return fig, ax


def box(ax, x, y, w, h, fc=PANEL, ec=LINE, lw=1.2, ls="-", r=1.2, alpha=1.0, z=1):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw, ls=ls,
                       alpha=alpha, zorder=z)
    ax.add_patch(p)
    return p


def text(ax, x, y, s, size=10, color=TEXT, weight="normal", ha="left", va="top", family=None, z=5, style="normal",
         alpha=1.0, linespacing=1.25):
    kw = dict(fontsize=size, color=color, fontweight=weight, ha=ha, va=va, zorder=z, fontstyle=style, alpha=alpha,
              linespacing=linespacing)
    if family:
        kw["family"] = family
    return ax.text(x, y, s, **kw)


def wrap(s: str, width: int) -> str:
    return "\n".join(textwrap.fill(p, width) for p in s.split("\n"))


def stack(ax, x, y, items, width):
    """Place wrapped text blocks top-down.  items = (string, size_pt, color, weight, gap_after_units).
    Line height in drawing units = size_pt * 1.28 / 7.2 (1 unit = 7.2 pt).  Returns the y below the last block."""
    for s, size, color, weight, gap in items:
        s = wrap(s, width)
        text(ax, x, y, s, size=size, color=color, weight=weight, linespacing=1.28)
        y += (s.count(chr(10)) + 1) * size * 1.28 / 7.2 + gap
    return y


def chip(ax, x, y, label, fc=CYAN, tc=BG, size=8.5, pad=0.9, weight="bold", ec=None):
    """Small label chip; returns its right edge (approx)."""
    t = ax.text(x + pad, y + pad * 0.55, label, fontsize=size, color=tc, fontweight=weight, ha="left", va="top",
                zorder=7)
    ax.figure.canvas.draw()
    bb = t.get_window_extent().transformed(ax.transData.inverted())
    wd = abs(bb.x1 - bb.x0) + 2 * pad
    ht = abs(bb.y1 - bb.y0) + 1.3 * pad
    box(ax, x, y, wd, ht, fc=fc, ec=ec or fc, lw=0.8, r=0.7, z=6)
    return x + wd


def arrow(ax, x1, y1, x2, y2, color=CYAN, lw=1.8, rad=0.0, ls="-", head=9, z=4):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=head, lw=lw, color=color,
                        connectionstyle=f"arc3,rad={rad}", ls=ls, zorder=z, shrinkA=0, shrinkB=0)
    ax.add_patch(a)
    return a


def header(ax, title, subtitle):
    text(ax, 3, 2.6, title, size=21, weight="bold", color=TEXT)
    text(ax, 3, 8.0, subtitle, size=11, color=MUTED)
    ax.plot([3, 157], [12.2, 12.2], color=CYAN, lw=1.6, zorder=3, solid_capstyle="round")
    ax.plot([3, 28], [12.2, 12.2], color=TEAL, lw=3.2, zorder=4, solid_capstyle="round")


def footer(ax, extra=""):
    s = DISCLAIMER + ("  " + extra if extra else "")
    text(ax, 3, 87.6, s, size=7.6, color=DIM)


def save(fig, name: str):
    out = MEDIA / name
    fig.savefig(out, dpi=DPI, facecolor=BG)
    plt.close(fig)
    return out


# ----------------------------------------------------------------------------- data loaders (read-only)
def read_jsonl(p: Path):
    with open(p, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def sha256_file(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def short(h: str, a=8, b=5) -> str:
    return f"{h[:a]}…{h[-b:]}"


def load_main():
    return read_jsonl(RES_MAIN / "results.jsonl")


def load_pilot():
    return read_jsonl(RES_PILOT / "results.jsonl")


def load_manifest():
    return json.loads((H / "manifest" / "task_manifest.json").read_text(encoding="utf-8"))


def load_run_meta(d: Path):
    return json.loads((d / "run_meta.json").read_text(encoding="utf-8"))


def load_common():
    return json.loads((H / "configs" / "common.json").read_text(encoding="utf-8"))


def load_arm(name: str):
    return json.loads((H / "configs" / f"{name}.json").read_text(encoding="utf-8"))


ARM_FILES = ["arm1_basic", "arm2_test_guided", "arm2b_agent_initiated_tests", "arm3b_test_validated_nograph",
             "arm3_graph_test_validated"]


def arms_run(rows):
    return sorted({r["arm"] for r in rows})


# ----------------------------------------------------------------------------- statistics (exact, stdlib only)
def _cdf(k, n, p):
    return sum(comb(n, i) * p**i * (1 - p) ** (n - i) for i in range(k + 1))


def clopper_pearson(k, n, a=0.05):
    lo = 0.0
    if k > 0:
        l, h = 0.0, 1.0
        for _ in range(80):
            m = (l + h) / 2
            if 1 - _cdf(k - 1, n, m) < a / 2:
                l = m
            else:
                h = m
        lo = l
    hi = 1.0
    if k < n:
        l, h = 0.0, 1.0
        for _ in range(80):
            m = (l + h) / 2
            if _cdf(k, n, m) > a / 2:
                l = m
            else:
                h = m
        hi = l
    return lo, hi


def exact_sign_p(b, c):
    """Two-sided exact binomial (McNemar) p for b vs c discordant pairs."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    return min(1.0, 2 * _cdf(k, n, 0.5))


# ----------------------------------------------------------------------------- freeze / mock-log parsing
def parse_freeze():
    lines = [l for l in (H / "FREEZE.sha256").read_text(encoding="utf-8").splitlines() if l.strip()]
    out = []
    for l in lines:
        h, rel = l.split("  ", 1)
        out.append((h, rel))
    return out


def freeze_recheck():
    """Recompute the SHA-256 of every frozen file *now*; returns (n_files, n_match, mismatches)."""
    ent = parse_freeze()
    bad = []
    for h, rel in ent:
        p = H / rel
        if not p.exists() or sha256_file(p) != h:
            bad.append(rel)
    return len(ent), len(ent) - len(bad), bad


def parse_mock_log():
    """Parse PASS/FAIL lines of the saved mock self-test log.  Returns dict(tag -> [pass, fail]) and totals."""
    txt = (PAPER / "results" / "selftest_mock_log_2026-11-07.txt").read_text(encoding="utf-8")
    groups = {}
    tp = tf = 0
    for l in txt.splitlines():
        m = re.match(r"^(PASS|FAIL)\s+(?:\[(\w+)\]\s+)?(.*)$", l)
        if not m:
            continue
        status, tag, _ = m.groups()
        tag = tag or "workspace / baselines"
        g = groups.setdefault(tag, [0, 0])
        if status == "PASS":
            g[0] += 1
            tp += 1
        else:
            g[1] += 1
            tf += 1
    final = "SELFTEST PASSED" in txt
    return groups, tp, tf, final
