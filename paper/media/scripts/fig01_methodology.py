"""Figure 1 - research methodology (arm1_basic vs arm2_test_guided).  Run:  python -B fig01_methodology.py"""
from _common import *  # noqa: F401,F403


def main():
    common = load_common()
    man = load_manifest()
    meta = load_run_meta(RES_MAIN)
    main_rows = load_main()
    arm1, arm2 = load_arm("arm1_basic"), load_arm("arm2_test_guided")
    b = common["budgets"]
    s = common["sampling"]

    # ---- consistency guards: the diagram must not claim more than the files say
    assert arm1["auto_test"] is False and arm2["auto_test"] is True
    assert arm1["tools"] == arm2["tools"] == ["read_file", "replace_in_file", "submit"]
    assert not arm1["submit_gate"] and not arm2["submit_gate"] and not arm1["graph"] and not arm2["graph"]
    assert arms_run(main_rows) == ["arm1_basic", "arm2_test_guided"], "an optional arm has result rows - update figure"
    assert meta["arms"] == ["arm1_basic", "arm2_test_guided"]
    n_tasks = len(man["tasks"])
    sel = man["selection"]
    n_tests = sum(t["n_tests"] for t in man["tasks"])
    commit = man["pinned_commit"]
    n_traces = len(list((RES_MAIN / "traces").glob("*.jsonl")))
    opt = {a: load_arm(a) for a in ["arm2b_agent_initiated_tests", "arm3b_test_validated_nograph",
                                    "arm3_graph_test_validated"]}
    assert opt["arm2b_agent_initiated_tests"]["tools"][2] == "run_tests"
    assert opt["arm3b_test_validated_nograph"]["submit_gate"] and not opt["arm3b_test_validated_nograph"]["graph"]
    assert opt["arm3_graph_test_validated"]["graph"] and opt["arm3_graph_test_validated"]["submit_gate"]

    fig, ax = new_canvas()
    header(ax, "Research methodology: does deterministic test feedback help a small local agent?",
           f"Gemma 4 E2B (QAT Q4_0 GGUF) via llama.cpp on CPU  ·  {n_tasks} QuixBugs Python bug-fix tasks  ·  "
           "same prompt, tools and budgets in both arms")

    LY0, LY1 = 15.5, 63.0  # top / bottom of the three columns

    # ------------------------------------------------------------------ INPUT column
    box(ax, 3, LY0, 30, LY1 - LY0, fc=PANEL, ec=CYAN, lw=1.4)
    text(ax, 5, LY0 + 1.5, "TASK INPUT", size=11, weight="bold", color=CYAN)
    stack(ax, 5, LY0 + 5.3, [
        (f"QuixBugs, Python\npinned commit {commit[:8]}…", 9.6, TEXT, "normal", 1.2),
        (f"{n_tasks} tasks drawn with a seeded sampler (seed {sel['seed']}) from the {sel['n_eligible']} programs "
         f"measured eligible out of {sel['n_scanned']} scanned; {n_tests} tests in total", 9.0, TEXT, "normal", 2.2),
        ("Agent can see", 9.6, TEAL, "bold", 0.5),
        ("the buggy file and its docstring, the pytest file, the JSON test data", 9.0, TEXT, "normal", 2.2),
        ("Never in the workspace", 9.6, AMBER, "bold", 0.5),
        (f"the reference solution (a scan of all {n_traces} traces found none shown to the model)", 9.0, TEXT, "normal", 0),
    ], width=32)

    # ------------------------------------------------------------------ lanes
    def lane(y, h, arm_label, sub, accent, feedback_on):
        box(ax, 37, y, 91.5, h, fc=PANEL, ec=accent, lw=1.5)
        e = chip(ax, 38.2, y + 1.0, arm_label, fc=accent, size=9.5)
        text(ax, e + 1.6, y + 1.5, sub, size=9.2, color=MUTED)
        sy, sh = y + 4.8, h - 7.0
        xs = [39, 62, 85, 108]
        wd = 19.6
        steps = [
            ("1  Agent turn", "Gemma 4 E2B returns one JSON tool call: read_file, replace_in_file or submit",
             PANEL2, LINE, TEXT),
            ("2  Edit applied", "Exact-string replace: 'old' must match exactly once; an edit that creates a "
             "syntax error is rejected", PANEL2, LINE, TEXT),
        ]
        if feedback_on:
            steps.append(("3  Test feedback", "Harness runs pytest before the 1st step and after every applied edit. "
                          "Model sees fail count + first failure (≤8 lines); not skippable",
                          "#0E3A52", CYAN, TEXT))
        else:
            steps.append(("3  Test feedback: none", "No test execution of any kind. The test file is readable, "
                          "but the model never gets run results", BG, DIM, MUTED))
        steps.append(("4  Run ends", f"submit, or a budget is hit: {b['max_turns']} turns, {b['max_tool_calls']} "
                      f"tool calls, {b['max_format_errors']} format errors, {b['max_wall_seconds']} s", PANEL2, LINE,
                      TEXT))
        for i, (ttl, body, fc, ec, tc) in enumerate(steps):
            x = xs[i]
            box(ax, x, sy, wd, sh, fc=fc, ec=ec, lw=1.3 if ec != DIM else 1.0, ls="--" if ec == DIM else "-", r=1.0)
            text(ax, x + 1.0, sy + 0.9, ttl, size=9.2, weight="bold", color=CYAN if (i == 2 and feedback_on) else tc)
            text(ax, x + 1.0, sy + 3.9, wrap(body, 28), size=8.8, color=tc, linespacing=1.28)
            if i < 3:
                arrow(ax, x + wd + 0.15, sy + sh / 2, xs[i + 1] - 0.15, sy + sh / 2, color=accent, lw=1.5, head=8)
        # loop-back (steps 3 -> 1)
        ly = sy + sh + 1.45
        ax.plot([xs[2] + wd / 2, xs[2] + wd / 2], [sy + sh, ly], color=DIM, lw=1.2, zorder=3)
        ax.plot([xs[2] + wd / 2, xs[0] + wd / 2], [ly, ly], color=DIM, lw=1.2, zorder=3)
        arrow(ax, xs[0] + wd / 2, ly, xs[0] + wd / 2, sy + sh + 0.1, color=DIM, lw=1.2, head=7)
        t = text(ax, (xs[0] + xs[2]) / 2 + wd / 2, ly, "repeat until submit or budget end", size=7.4, color=MUTED,
                 ha="center", va="center", z=6)
        t.set_bbox(dict(fc=PANEL, ec="none", pad=1.2))
        return sy + sh / 2

    LH = 22.5
    ymid1 = lane(LY0, LH, "arm1_basic", "Basic agent: no tests", MUTED, False)
    ymid2 = lane(LY1 - LH, LH, "arm2_test_guided", "Test-guided agent: forced, deterministic feedback", CYAN, True)
    for ym in (ymid1, ymid2):
        arrow(ax, 33.2, ym, 36.8, ym, color=CYAN, lw=1.5, head=8)
        arrow(ax, 128.7, ym, 131.3, ym, color=CYAN, lw=1.5, head=8)

    # ------------------------------------------------------------------ OUTCOME column
    box(ax, 131.5, LY0, 25.5, LY1 - LY0, fc=PANEL, ec=TEAL, lw=1.4)
    text(ax, 133.3, LY0 + 1.5, "RECORDED OUTCOME", size=11, weight="bold", color=TEAL)
    stack(ax, 133.3, LY0 + 5.3, [
        ("Final file graded by the official QuixBugs pytest file", 9.0, TEXT, "normal", 1.4),
        ("Primary metric", 9.4, TEAL, "bold", 0.3),
        ("resolved_final_state", 9.0, TEXT, "normal", 1.4),
        ("Also logged", 9.4, TEAL, "bold", 0.3),
        ("AST-equal to reference, end reason, edits and rejected edits, tokens, wall time", 9.0, TEXT, "normal", 1.4),
        ("Per run", 9.4, TEAL, "bold", 0.3),
        ("one results.jsonl row and a full trace with raw model responses", 9.0, TEXT, "normal", 1.4),
        ("Statistics", 9.4, TEAL, "bold", 0.3),
        ("paired by task; only H1 (arm2 vs arm1) is confirmatory", 9.0, TEXT, "normal", 0),
    ], width=26)

    # ------------------------------------------------------------------ optional ablations
    ay, ah = 65.2, 11.2
    box(ax, 3, ay, 154, ah, fc=BG, ec=DIM, lw=1.1, ls="--", r=1.0)
    chip(ax, 4.2, ay + 1.0, "OPTIONAL ABLATION ARMS: specified in the protocol, NOT run", fc=AMBER, size=9.2)
    cols = [
        ("arm2b_agent_initiated_tests", "adds a run_tests tool; the agent decides when to test"),
        ("arm3b_test_validated_nograph", "arm2 + submit gate (up to 3 rejections while tests fail)"),
        ("arm3_graph_test_validated", "arm3b + AST code-graph tools (expected near-vacuous on single-function files)"),
    ]
    for (nm, d), x in zip(cols, [4.5, 56.0, 106.0]):
        text(ax, x, ay + 5.4, nm, size=9.0, weight="bold", color=MUTED, family=MONO)
        text(ax, x, ay + 7.6, wrap(d, 62), size=8.2, color=DIM)

    # ------------------------------------------------------------------ shared settings strip
    sy = 78.4
    box(ax, 3, sy, 154, 6.2, fc=PANEL, ec=LINE, lw=1.0, r=0.9)
    shared = (f"Shared by both arms:  temperature {s['temperature']}, top-p {s['top_p']}, top-k {s['top_k']}, "
              f"up to {s['max_new_tokens']} new tokens per turn, context 8192, llama-server --reasoning off, "
              f"JSON-in-text actions (not native tool calls), {len(meta['seeds'])} seed (seed {meta['seeds'][0]}). "
              "Protocol, configs, prompts, manifest and harness code were hashed before the main run.")
    text(ax, 4.5, sy + 1.2, wrap(shared, 168), size=8.8, color=TEXT, linespacing=1.3)

    footer(ax, "Sources: configs/*.json, task_manifest.json, run_meta.json, experimental protocol.")
    out = save(fig, "01_research_methodology.png")
    print("wrote", out)


if __name__ == "__main__":
    main()
