"""Figure 2 - measured outcomes of arm1_basic vs arm2_test_guided (seed 1, 12 tasks).
Every number is computed from results/main_seed1/results.jsonl and manifest/task_manifest.json.
Run:  python -B fig02_results.py
"""
from _common import *  # noqa: F401,F403

FAILED = "#B24A5E"      # unresolved
END_CODE = {"submitted": "S", "max_turns": "T", "format_abort": "F"}


def main():
    rows = load_main()
    man = load_manifest()
    pilot = load_pilot()

    # ---------------------------------------------------------------- integrity guards (no mock / no placeholder)
    assert len(rows) == 24 and not any(r["is_mock"] for r in rows) and not any(r["error"] for r in rows)
    assert arms_run(rows) == ["arm1_basic", "arm2_test_guided"]
    tasks = [t["task_id"] for t in man["tasks"]]
    base = {t["task_id"]: (t["n_failing_on_buggy"], t["n_tests"]) for t in man["tasks"]}
    by = {(r["task_id"], r["arm"]): r for r in rows}
    assert all((t, a) in by for t in tasks for a in ("arm1_basic", "arm2_test_guided")), "missing task/arm cell"
    assert {r["seed"] for r in rows} == {1}

    arms = ["arm1_basic", "arm2_test_guided"]
    n = len(tasks)
    res = {a: [by[(t, a)]["resolved_final_state"] for t in tasks] for a in arms}
    k = {a: sum(res[a]) for a in arms}
    ci = {a: clopper_pearson(k[a], n) for a in arms}
    only1 = sum(1 for x, y in zip(res[arms[0]], res[arms[1]]) if x and not y)
    only2 = sum(1 for x, y in zip(res[arms[0]], res[arms[1]]) if y and not x)
    both = sum(1 for x, y in zip(res[arms[0]], res[arms[1]]) if x and y)
    neither = n - both - only1 - only2
    p_sign = exact_sign_p(only1, only2)
    pilot_flat = [r for r in pilot if r["task_id"].endswith("flatten") and r["arm"] == "arm2_test_guided"][0]
    main_flat = by[("quixbugs/flatten", "arm2_test_guided")]
    flatten_diverged = pilot_flat["resolved_final_state"] and not main_flat["resolved_final_state"]
    n_worse = {a: sum(1 for t in tasks if by[(t, a)]["final_tests"]["failed"] > base[t][0]) for a in arms}

    fig, ax = new_canvas()
    header(ax, "Measured outcomes: arm1_basic vs arm2_test_guided",
           f"Gemma 4 E2B · {n} QuixBugs tasks · 1 seed · {len(rows)} real inference runs (0 mock) · "
           "descriptive pilot, not a significance test")

    # ================================================================ LEFT: resolved counts, one block per task
    LX, LW = 3, 76
    box(ax, LX, 15, LW, 59.5, fc=PANEL, ec=CYAN, lw=1.3)
    text(ax, LX + 2, 16.5, "Tasks resolved (final state)", size=11.5, weight="bold", color=CYAN)
    text(ax, LX + 2, 20.6, f"One block per task  ·  denominator = {n} tasks per arm", size=8.6, color=MUTED)
    bx0, bw, bh, gap = LX + 29.5, 3.0, 4.6, 0.55

    def strip(y, states):
        for i, st in enumerate(states):
            x = bx0 + i * (bw + gap)
            if st:
                box(ax, x, y, bw, bh, fc=TEAL, ec=TEAL, lw=0.8, r=0.5)
            else:
                box(ax, x, y, bw, bh, fc=FAILED, ec=FAILED, lw=0.8, r=0.5, alpha=0.85)

    for i, a in enumerate(arms):
        y = 25.5 + i * 11.6
        text(ax, LX + 2, y + 0.9, a, size=9.2, weight="bold", family=MONO,
             color=TEXT if a == "arm2_test_guided" else MUTED)
        strip(y, res[a])
        text(ax, LX + 2, y + 5.6, f"{k[a]} of {n} resolved", size=11, weight="bold",
             color=TEAL if k[a] else CORAL)
        lo, hi = ci[a]
        text(ax, bx0, y + 5.7, f"95% exact interval {100*lo:.1f}% to {100*hi:.1f}%", size=8.6, color=MUTED)

    # untested configurations
    y = 50.0
    ax.plot([LX + 2, LX + LW - 2], [y - 1.6, y - 1.6], color=LINE, lw=1, ls=(0, (4, 3)))
    chip(ax, LX + 2, y, "NOT RUN: no data, no bar", fc=AMBER, size=8.8)
    untested = [("arm2b_agent_initiated_tests", "not run (optional arm)"),
                ("arm3b_test_validated_nograph", "not run (optional ablation)"),
                ("arm3_graph_test_validated", "not run (optional graph arm)"),
                ("seeds 2 and 3, both arms", "not run (protocol specifies 3 seeds)")]
    for i, (nm, why) in enumerate(untested):
        yy = y + 5.2 + i * 4.5
        text(ax, LX + 2, yy + 0.3, nm, size=8.6, family=MONO, color=DIM)
        box(ax, bx0 + 7, yy, 12 * (bw + gap) - gap - 7, 3.2, fc="none", ec=DIM, lw=1.0, ls="--", r=0.6)
        text(ax, bx0 + 9, yy + 1.6, why, size=8.2, color=DIM, style="italic", va="center")

    # ================================================================ RIGHT: per-task matrix
    RX, RW = 83, 74
    box(ax, RX, 15, RW, 59.5, fc=PANEL, ec=TEAL, lw=1.3)
    text(ax, RX + 2, 16.5, "Per-task final state", size=11.5, weight="bold", color=TEAL)
    text(ax, RX + 2, 20.6, "arm1 = arm1_basic, arm2 = arm2_test_guided  ·  number = tests still failing / tests in file", size=8.6,
         color=MUTED)
    cx = [RX + 2, RX + 29.5, RX + 43.5, RX + 59.0]
    cw = [26, 13, 14.5, 14.5]
    hy = 24.2
    for x, lbl in zip(cx, ["task", "buggy", "arm1", "arm2"]):
        text(ax, x if lbl == "task" else x + cw[cx.index(x)] / 2, hy, lbl, size=8.6, weight="bold",
             color=MUTED if lbl in ("task", "buggy") else (TEXT), ha="left" if lbl == "task" else "center")
    rh, y0 = 3.0, 27.0
    for i, t in enumerate(tasks):
        y = y0 + i * (rh + 0.32)
        nm = t.split("/")[1]
        text(ax, cx[0], y + rh / 2, nm, size=8.2, family=MONO, color=TEXT, va='center')
        bf, bt = base[t]
        box(ax, cx[1], y, cw[1], rh, fc=PANEL2, ec="none", r=0.5)
        text(ax, cx[1] + cw[1] / 2, y + rh / 2, f"{bf}/{bt}", size=8.2, color=MUTED, ha="center", va="center")
        for j, a in enumerate(arms):
            r = by[(t, a)]
            f, tt = r["final_tests"]["failed"], r["final_tests"]["tests"]
            ok = r["resolved_final_state"]
            worse = f > bf
            fc = TEAL if ok else FAILED
            x = cx[2 + j]
            box(ax, x, y, cw[2 + j], rh, fc=fc, ec=CORAL if worse else fc, lw=1.6 if worse else 0.8, r=0.5,
                alpha=1.0 if ok else 0.85)
            label = f"{f}/{tt}  {END_CODE[r['end_reason']]}" + ("  ▼" if worse else "")
            text(ax, x + cw[2 + j] / 2, y + rh / 2, label, size=8.2, color=BG if ok else TEXT, ha="center", va="center",
                 weight="bold" if ok else "normal")

    # legend
    ly = 68.4
    items = [(TEAL, "resolved (0 failing)"), (FAILED, "failed (unresolved)")]
    xx = RX + 2
    for fc, lbl in items:
        box(ax, xx, ly, 2.4, 2.4, fc=fc, ec=fc, r=0.4)
        text(ax, xx + 3.2, ly - 0.1, lbl, size=8.0, color=TEXT)
        xx += 25 if "resolved (" in lbl else 27
    text(ax, xx, ly - 0.1, "▼ worse than buggy baseline", size=8.0, color=CORAL)
    text(ax, RX + 2, ly + 3.0, "S = submitted · T = turn limit · F = format abort (3 format errors)", size=8.0, color=MUTED)

    # ================================================================ bottom notes
    box(ax, 3, 76.6, 154, 9.8, fc=BG, ec=LINE, lw=1.1, r=1.0)
    l1 = (f"Paired outcome: both resolved {both}, only arm1 {only1}, only arm2 {only2}, neither {neither}. "
          f"With one discordant task the exact two-sided sign test gives p = {p_sign:.1f}: no detectable effect of "
          "test feedback. Neither arm is shown to be better.")
    l2 = (f"Final state worse than the buggy baseline: arm1 {n_worse[arms[0]]} tasks, arm2 {n_worse[arms[1]]} tasks "
          "(quicksort: both arms made the same edit, 1/13 to 13/13 failing). "
          + ("In the earlier 4-run pilot flatten/arm2 was resolved but it was not in this run; pilot rows are "
             "not pooled." if flatten_diverged else ""))
    text(ax, 4.5, 77.7, wrap(l1, 182), size=8.7, color=TEXT, linespacing=1.3)
    text(ax, 4.5, 82.0, wrap(l2, 182), size=8.7, color=MUTED, linespacing=1.3)

    footer(ax, "Source: results/main_seed1/results.jsonl, task_manifest.json (baseline failing counts).")
    out = save(fig, "02_results_comparison.png")
    print("wrote", out)
    print(dict(k=k, ci=ci, only1=only1, only2=only2, both=both, neither=neither, p=p_sign, worse=n_worse))


if __name__ == "__main__":
    main()
