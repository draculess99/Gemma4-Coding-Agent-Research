"""Experiment runner.  Examples:
  python -m harness.run_experiment --qb-root <QuixBugs clone> --out results/pilot --arms arm1_basic arm2_test_guided --seeds 1 --max-tasks 3
Real model runs need a local llama-server (loopback only). No cloud, no GPU assumptions.
"""
import argparse, hashlib, json, platform, random, sys, tempfile, time
from datetime import datetime, timezone
from pathlib import Path
from . import HARNESS_VERSION
from .agent import run_agent
from .llm import LlamaServerBackend

ROOT = Path(__file__).resolve().parent.parent


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def load_arm(name: str):
    common = json.loads((ROOT / "configs" / "common.json").read_text())
    arm = json.loads((ROOT / "configs" / f"{name}.json").read_text())
    merged = {**common, **arm, "_root": str(ROOT)}
    merged["_sha256"] = sha256_bytes(json.dumps({k: v for k, v in merged.items() if k != "_root"}, sort_keys=True).encode())
    return merged


def verify_pin(qb_root: Path, manifest: dict):
    """Fail loudly if the local QuixBugs copy differs from the manifest (hash check per task file)."""
    for t in manifest["tasks"]:
        for key, rel in (("sha256_buggy", t["program"]), ("sha256_test", t["test_file"]), ("sha256_reference", t["reference_program"])):
            h = sha256_bytes((qb_root / rel).read_bytes())
            if h != t[key]:
                raise SystemExit(f"Manifest mismatch for {rel}: expected {t[key][:12]}, got {h[:12]}. Wrong QuixBugs checkout/line endings?")


def execute(backend, qb_root, out_dir, arm_names, seeds, manifest, max_tasks=None, shuffle_seed=0, log=print):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    res_path = out_dir / "results.jsonl"
    done = set()
    if res_path.exists():
        done = {json.loads(l)["run_id"] for l in res_path.read_text().splitlines() if l.strip()}
    arms = {a: load_arm(a) for a in arm_names}
    tasks = manifest["tasks"][:max_tasks] if max_tasks else manifest["tasks"]
    mhash = sha256_bytes(json.dumps(manifest["tasks"], sort_keys=True).encode())
    plan = []
    for seed in seeds:
        for t in tasks:
            order = list(arm_names)
            random.Random(f"{shuffle_seed}-{seed}-{t['task_id']}").shuffle(order)  # spread drift/thermal effects across arms
            for a in order:
                rid = hashlib.sha1(f"{t['task_id']}|{a}|{seed}|{arms[a]['_sha256']}|{mhash}".encode()).hexdigest()[:16]
                plan.append((rid, t, a, seed))
    todo = [p for p in plan if p[0] not in done]
    log(f"{len(plan)} planned runs, {len(plan) - len(todo)} already done, {len(todo)} to run")
    work = Path(tempfile.mkdtemp(prefix="g4work_"))
    t_start = time.time()
    for i, (rid, t, a, seed) in enumerate(todo, 1):
        arm = arms[a]
        rec = run_agent(t, arm, seed, backend, qb_root, work, rid, out_dir / "traces", arm["sampling"], HARNESS_VERSION)
        rec.update({"config_sha256": arm["_sha256"], "manifest_sha256": mhash,
                    "sampling": arm["sampling"], "budgets": arm["budgets"],
                    "timestamp_utc": datetime.now(timezone.utc).isoformat()})
        with open(res_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")
        el = time.time() - t_start
        log(f"[{i}/{len(todo)}] {t['task_id']:34s} {a:30s} seed={seed} resolved={rec['resolved_final_state']} "
            f"end={rec['end_reason']} turns={rec['turns']} wall={rec['wall_seconds']}s  eta~{el/i*(len(todo)-i)/60:.0f}min")
    return res_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--qb-root", required=True)
    ap.add_argument("--manifest", default=str(ROOT / "manifest" / "task_manifest.json"))
    ap.add_argument("--out", required=True)
    ap.add_argument("--arms", nargs="+", default=["arm1_basic", "arm2_test_guided", "arm3_graph_test_validated"])
    ap.add_argument("--seeds", nargs="+", type=int, default=[1])
    ap.add_argument("--max-tasks", type=int)
    ap.add_argument("--base-url", default="http://127.0.0.1:8080")
    ap.add_argument("--model-id", required=True, help="e.g. gemma-4-e2b-it-qat-q4_0 (record exactly what llama-server loaded)")
    ap.add_argument("--quant", default="q4_0-gguf")
    ap.add_argument("--gguf-sha256", default="")
    a = ap.parse_args()
    manifest = json.loads(Path(a.manifest).read_text())
    qb = Path(a.qb_root).resolve()
    verify_pin(qb, manifest)
    backend = LlamaServerBackend(a.base_url, a.model_id)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "run_meta.json").write_text(json.dumps({
        "model_id": a.model_id, "quant": a.quant, "gguf_sha256": a.gguf_sha256, "backend": "llama.cpp llama-server",
        "base_url": a.base_url, "arms": a.arms, "seeds": a.seeds, "harness_version": HARNESS_VERSION,
        "platform": platform.platform(), "python": sys.version, "processor": platform.processor(),
        "manifest_pinned_commit": manifest["pinned_commit"]}, indent=2))
    execute(backend, qb, out, a.arms, a.seeds, manifest, a.max_tasks)


if __name__ == "__main__":
    main()
