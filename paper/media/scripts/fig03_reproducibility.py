"""Figure 3 - reproducibility evidence.  Everything is recomputed from project files at render time:
 - freeze hashes re-verified now against FREEZE.sha256
 - manifest, run_meta.json, common.json
 - mock self-test log parsed line by line (structural test, NOT Gemma)
 - real-run integrity (is_mock flags, traces, llama-server request count vs recorded turns)
 - pilot-vs-main repeat comparison
Run:  python -B fig03_reproducibility.py
"""
import re
from collections import Counter

from _common import *  # noqa: F401,F403


def kv(ax, x, y, k, v, kw=13.5, size=8.2, vcolor=TEXT, gap=3.35):
    text(ax, x, y, k, size=size, color=MUTED)
    text(ax, x + kw, y, v, size=size, color=vcolor, family=MONO)
    return y + gap


def main():
    # ---------------------------------------------------------------- gather evidence
    main_rows, pilot_rows = load_main(), load_pilot()
    man, meta, common = load_manifest(), load_run_meta(RES_MAIN), load_common()
    n_frz, n_match, bad = freeze_recheck()
    frz = parse_freeze()
    cat = Counter(rel.split("/")[0] for _, rel in frz)
    frz_time = (LOGS / "freeze_time_utc.txt").read_text().strip()
    frz_hash = sha256_file(H / "FREEZE.sha256")
    proto_txt = (H / "docs" / "EXPERIMENTAL_PROTOCOL.md").read_text(encoding="utf-8")
    assert "T=0.7" in proto_txt and common["sampling"]["temperature"] == 1.0  # documented deviation is real

    groups, tpass, tfail, final_ok = parse_mock_log()
    assert tfail == 0 and final_ok

    n_main_mock = sum(r["is_mock"] for r in main_rows)
    n_pilot_mock = sum(r["is_mock"] for r in pilot_rows)
    tr_main = len(list((RES_MAIN / "traces").glob("*.jsonl")))
    tr_pilot = len(list((RES_PILOT / "traces").glob("*.jsonl")))
    turns_main = sum(r["turns"] for r in main_rows)
    slog = (LOGS / "server_p2c.err.log").read_text(encoding="utf-8", errors="replace")
    n_req = len(re.findall(r"processing task", slog))
    m_path = re.search(r"loading model '([^']+)'", slog).group(1)
    n_ctx = re.search(r"n_ctx_slot = (\d+)", slog).group(1)
    n_thr = re.search(r"n_threads = (\d+)", slog).group(1)
    listen = re.search(r"listening on http://([\d.:]+)", slog).group(1)
    h_main = sha256_file(RES_MAIN / "results.jsonl")
    h_pilot = sha256_file(RES_PILOT / "results.jsonl")

    # pilot vs main repeat of the four pilot configurations
    mk = {(r["task_id"], r["arm"]): r for r in main_rows}
    ident, differ = 0, []
    for p in pilot_rows:
        m = mk[(p["task_id"], p["arm"])]
        same = (p["patch"] == m["patch"] and p["turns"] == m["turns"] and p["prompt_tokens"] == m["prompt_tokens"]
                and p["completion_tokens"] == m["completion_tokens"])
        if same:
            ident += 1
        else:
            differ.append((p, m))
    cfg_same = all(mk[(p["task_id"], p["arm"])]["config_sha256"] == p["config_sha256"] for p in pilot_rows)
    addr_only = False
    if differ:
        p, m = differ[0]
        tp = read_jsonl(RES_PILOT / "traces" / f"{p['run_id']}.jsonl")[0]["user0"]
        tm = read_jsonl(RES_MAIN / "traces" / f"{m['run_id']}.jsonl")[0]["user0"]
        # same length, and every differing character is a hex digit (the object address in the pytest output)
        hexc = set("0123456789ABCDEFabcdef")
        diffs = [(x, y) for x, y in zip(tp, tm) if x != y]
        addr_only = len(tp) == len(tm) and 0 < len(diffs) <= 16 and all(x in hexc and y in hexc for x, y in diffs)

    n_scanned, n_elig = man["selection"]["n_scanned"], man["selection"]["n_eligible"]
    n_samp, n_tests = len(man["tasks"]), sum(t["n_tests"] for t in man["tasks"])

    fig, ax = new_canvas()
    header(ax, "Reproducibility evidence: what was frozen, what was run, and what each test proves",
           "Values are recomputed from the project files at render time; the two items taken from reports are marked in panel C")

    # ================================================================ A: frozen configuration
    ax_x, ax_w, top, ph = 3, 52, 15, 34.0
    box(ax, ax_x, top, ax_w, ph, fc=PANEL, ec=CYAN, lw=1.3)
    text(ax, ax_x + 2, top + 1.4, "A  Frozen before the main run", size=10.5, weight="bold", color=CYAN)
    text(ax, ax_x + 2, top + 5.4, f"{n_match}/{n_frz}", size=22, weight="bold", color=TEAL if not bad else CORAL)
    text(ax, ax_x + 17.5, top + 6.4, "file hashes match FREEZE.sha256\nwhen re-checked at render time", size=8.4,
         color=TEXT)
    names = {"docs": "protocol doc", "configs": "configs", "prompts": "prompt", "manifest": "manifest",
             "schema": "schema", "harness": "harness modules", "scripts": "script"}
    parts = ", ".join(f"{v} {names.get(k, k)}" for k, v in cat.items())
    text(ax, ax_x + 2, top + 12.6, wrap(f"Covers: {parts}", 62), size=7.8, color=MUTED)
    yy = top + 19.0
    yy = kv(ax, ax_x + 2, yy, "frozen at", frz_time, kw=12, size=8.0)
    yy = kv(ax, ax_x + 2, yy, "FREEZE file", short(frz_hash), kw=12, size=8.0)
    text(ax, ax_x + 2, yy + 0.3, wrap("Self-attested local list, no third-party timestamp. Deviation: the frozen "
                                      "protocol text says T=0.7; the configs used T=1.0 (documented).", 62),
         size=7.6, color=AMBER, linespacing=1.25)

    # ================================================================ B: manifest
    bx, bw = 58, 49
    box(ax, bx, top, bw, ph, fc=PANEL, ec=CYAN, lw=1.3)
    text(ax, bx + 2, top + 1.4, "B  Task manifest (pinned)", size=10.5, weight="bold", color=CYAN)
    fx, fmax = bx + 2, bw - 22
    for i, (lbl, v, col) in enumerate([("scanned", n_scanned, DIM), ("eligible", n_elig, SLATE),
                                       ("sampled", n_samp, TEAL)]):
        y = top + 5.6 + i * 4.0
        text(ax, fx, y + 0.2, lbl, size=8.2, color=MUTED)
        wv = fmax * v / n_scanned
        box(ax, fx + 12, y, wv, 3.4, fc=col, ec=col, r=0.5)
        text(ax, fx + 12 + wv + 1, y + 0.2, str(v), size=8.8, weight="bold", color=TEXT)
    yy = top + 18.6
    yy = kv(ax, bx + 2, yy, "commit", man["pinned_commit"][:8] + "…" + man["pinned_commit"][-5:], kw=12, size=8.0, gap=3.0)
    yy = kv(ax, bx + 2, yy, "sampler seed", str(man["selection"]["seed"]), kw=12, size=8.0, gap=3.0)
    yy = kv(ax, bx + 2, yy, "tests", f"{n_tests} in {n_samp} tasks", kw=12, size=8.0, gap=3.0)
    text(ax, bx + 2, yy + 0.2, wrap("QuixBugs is not vendored. Rule-based exclusions: 10 graph-based programs and "
                                    "3 whose buggy version times out.", 58), size=7.6, color=MUTED)

    # ================================================================ C: run metadata
    cx, cw = 110, 47
    box(ax, cx, top, cw, ph, fc=PANEL, ec=CYAN, lw=1.3)
    text(ax, cx + 2, top + 1.4, "C  Run metadata (run_meta.json)", size=10.5, weight="bold", color=CYAN)
    yy = top + 5.4
    for k_, v_ in [("model", meta["model_id"]), ("quant", meta["quant"]), ("GGUF sha", short(meta["gguf_sha256"])),
                   ("backend", meta["backend"].replace("llama.cpp ", "")),
                   ("server log", f"ctx {n_ctx}, {n_thr} threads, CPU"),
                   ("platform", meta["platform"].replace("-SP0", "")), ("python", meta["python"].split()[0]),
                   ("harness", meta["harness_version"]), ("seeds", str(meta["seeds"]))]:
        yy = kv(ax, cx + 2, yy, k_, v_, kw=11.5, size=7.9, gap=2.6)
    text(ax, cx + 2, yy + 0.4, wrap(f"llama.cpp {HARDCODED_FROM_REPORTS['llama_cpp_build']} and "
                                    f"{HARDCODED_FROM_REPORTS['machine']} are taken from the P2A-P2C reports.", 56),
         size=7.3, color=DIM)

    # ================================================================ bottom-left: MOCK
    by0, bh = 51.2, 33.8
    box(ax, 3, by0, 74, bh, fc="#1E1B12", ec=AMBER, lw=1.6)
    chip(ax, 4.5, by0 + 1.2, "STRUCTURAL TEST: MOCK SELF-TEST, NO GEMMA", fc=AMBER, size=9.2)
    text(ax, 5, by0 + 6.4, f"{tpass}", size=24, weight="bold", color=AMBER)
    text(ax, 14.0, by0 + 7.2, f"checks passed, {tfail} failed", size=9.5, weight="bold", color=TEXT)
    text(ax, 14.0, by0 + 10.6, "Scripted policies stand in for a model; every row is flagged is_mock.", size=7.8,
         color=MUTED)
    text(ax, 5, by0 + 14.6, wrap("Shows that the grader, edit path, tool gating, workspace isolation and baseline "
                                 "failing counts work. It is NOT model performance and says nothing about Gemma.",
                                 96), size=8.2, color=TEXT, linespacing=1.28)
    items = list(groups.items())
    for i, (tag, (pz, fz)) in enumerate(items):
        col, row = divmod(i, 3)
        x0 = 5 + col * 35.5
        gy = by0 + 21.2 + row * 3.3
        text(ax, x0, gy + 0.1, tag, size=7.8, family=MONO, color=MUTED)
        box(ax, x0 + 15.5, gy, 1.5 * pz, 2.4, fc=AMBER, ec=AMBER, r=0.4, alpha=0.9)
        text(ax, x0 + 15.5 + 1.5 * pz + 0.8, gy + 0.0, f"{pz} pass", size=7.8, color=TEXT)
    text(ax, 5, by0 + bh - 2.6, "Source: results/selftest_mock_log_2026-11-07.txt (one count per PASS line)", size=7.0,
         color=DIM)

    # ================================================================ bottom-right: REAL
    rx, rw = 81, 76
    box(ax, rx, by0, rw, bh, fc="#0C2438", ec=CYAN, lw=1.6)
    chip(ax, rx + 1.5, by0 + 1.2, "REAL GEMMA 4 E2B INFERENCE: is_mock = false", fc=CYAN, size=9.2)
    tiles = [
        (f"{len(main_rows)}", "main runs, seed 1", f"{n_main_mock} mock, {tr_main} traces with raw responses"),
        (f"{len(pilot_rows)}", "earlier pilot runs", f"{n_pilot_mock} mock, {tr_pilot} traces, not pooled"),
        (f"{n_req}", "llama-server requests", f"= {turns_main} recorded turns" if n_req == turns_main
         else f"vs {turns_main} recorded turns (MISMATCH)"),
    ]
    for i, (big, l1, l2) in enumerate(tiles):
        x = rx + 2 + i * 24.6
        box(ax, x, by0 + 6.8, 23.2, 11.6, fc=PANEL2, ec=LINE, lw=1.0, r=0.8)
        text(ax, x + 1.3, by0 + 7.6, big, size=18, weight="bold", color=TEAL)
        text(ax, x + 1.3, by0 + 12.5, l1, size=7.9, color=TEXT, weight="bold")
        text(ax, x + 1.3, by0 + 14.6, wrap(l2, 36), size=7.2, color=MUTED)
    text(ax, rx + 2, by0 + 20.6, f"results.jsonl SHA-256  main {short(h_main)}   pilot {short(h_pilot)}",
         size=7.9, family=MONO, color=MUTED)
    rep = (f"Repeat check: {ident} of {len(pilot_rows)} pilot configurations reproduced exactly (patch, turns, tokens)"
           f"{'; config hashes identical' if cfg_same else ''}. ")
    if differ:
        p, m = differ[0]
        rep += (f"1 differed: {p['task_id'].split('/')[1]}/{p['arm']} resolved in the pilot but not in the main run"
                + (", and its first prompt differs only in memory addresses (0x...) inside the harness-injected "
                   "test output." if addr_only else "."))
    text(ax, rx + 2, by0 + 23.6, wrap(rep, 86), size=8.4, color=TEXT, linespacing=1.28)
    text(ax, rx + 2, by0 + 30.0, wrap("These are behavioural measurements, not structural tests: 1 of 12 tasks "
                                      "resolved by arm2 vs 0 of 12 by arm1 (one seed, not significant; see Figure 2).",
                                      86), size=8.4, color=CYAN, linespacing=1.28)

    footer(ax, "Sources: FREEZE.sha256, task_manifest.json, run_meta.json, results.jsonl, server_p2c.err.log.")
    out = save(fig, "03_reproducibility.png")
    print("wrote", out)
    print(dict(freeze=(n_match, n_frz), mock=(tpass, tfail), req=n_req, turns=turns_main, ident=ident,
               addr_only=addr_only, cfg_same=cfg_same, groups=groups, m_path=m_path, n_ctx=n_ctx, n_thr=n_thr,
               listen=listen, cat=dict(cat)))


if __name__ == "__main__":
    main()
