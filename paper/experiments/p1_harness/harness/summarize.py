"""Aggregate results.jsonl -> per-arm table + paired task-level bootstrap CIs. Refuses mock rows by default.
  python -m harness.summarize results/pilot/results.jsonl
"""
import argparse, json, random, statistics as st
from collections import defaultdict
from pathlib import Path


def task_means(rows, arm, key):
    per = defaultdict(list)
    for r in rows:
        if r["arm"] == arm:
            per[r["task_id"]].append(1.0 if r[key] is True else 0.0 if r[key] is False else float(r[key]))
    return {t: sum(v) / len(v) for t, v in per.items()}


def boot_ci(diffs, n=10000, seed=20261107):
    rng = random.Random(seed)
    k = len(diffs)
    means = sorted(sum(rng.choice(diffs) for _ in range(k)) / k for _ in range(n))
    return means[int(0.025 * n)], means[int(0.975 * n)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("results")
    ap.add_argument("--allow-mock", action="store_true")
    ap.add_argument("--primary", default="resolved_final_state")
    a = ap.parse_args()
    rows = [json.loads(l) for l in Path(a.results).read_text().splitlines() if l.strip()]
    if any(r["is_mock"] for r in rows) and not a.allow_mock:
        raise SystemExit("Refusing to summarise MOCK rows (self-test data). Use --allow-mock only for harness tests.")
    arms = sorted({r["arm"] for r in rows})
    print(f"runs={len(rows)} tasks={len({r['task_id'] for r in rows})} seeds={sorted({r['seed'] for r in rows})}\n")
    print(f"{'arm':32s} {'n':>4s} {'resolved':>9s} {'submitted+ok':>13s} {'turns':>6s} {'ptok':>8s} {'ctok':>7s} {'wall_s':>7s} {'fmt_err':>7s}")
    for arm in arms:
        rs = [r for r in rows if r["arm"] == arm]
        tm = task_means(rows, arm, a.primary)
        print(f"{arm:32s} {len(rs):4d} {100*sum(tm.values())/len(tm):8.1f}% "
              f"{100*sum(r['resolved_submitted'] for r in rs)/len(rs):12.1f}% {st.mean(r['turns'] for r in rs):6.1f} "
              f"{st.mean(r['prompt_tokens'] for r in rs):8.0f} {st.mean(r['completion_tokens'] for r in rs):7.0f} "
              f"{st.mean(r['wall_seconds'] for r in rs):7.0f} {st.mean(r['format_errors'] for r in rs):7.2f}")
    print(f"\nPaired task-level differences in {a.primary} (percentage points; 95% bootstrap CI over tasks):")
    for i, x in enumerate(arms):
        for y in arms[i + 1:]:
            tx, ty = task_means(rows, x, a.primary), task_means(rows, y, a.primary)
            common = sorted(set(tx) & set(ty))
            if len(common) < 2:
                continue
            d = [ty[t] - tx[t] for t in common]
            lo, hi = boot_ci(d)
            print(f"  {y} - {x}: {100*sum(d)/len(d):+6.1f} pp  [{100*lo:+.1f}, {100*hi:+.1f}]  (n_tasks={len(common)})")
    print("\nNote: with ~12 tasks the CIs are wide by construction; report them, do not over-interpret.")


if __name__ == "__main__":
    main()
