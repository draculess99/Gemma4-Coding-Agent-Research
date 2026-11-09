"""Pre-registration freeze: SHA-256 of protocol, configs, prompts, manifest, harness code, schema.
Run BEFORE any real model run:  python scripts/freeze.py > FREEZE.sha256
After the run, `python scripts/freeze.py --check FREEZE.sha256` shows whether anything changed (report deviations).
Self-attested (no third-party timestamp); say so in the paper.
"""
import hashlib, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATTERNS = ["docs/EXPERIMENTAL_PROTOCOL.md", "configs/*.json", "prompts/*.md", "manifest/task_manifest.json",
            "schema/*.json", "harness/*.py", "scripts/build_manifest.py"]


def digest():
    out = []
    for pat in PATTERNS:
        for p in sorted(ROOT.glob(pat)):
            out.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(ROOT).as_posix()}")
    return out


if __name__ == "__main__":
    cur = digest()
    if len(sys.argv) == 3 and sys.argv[1] == "--check":
        old = set(Path(sys.argv[2]).read_text().splitlines())
        changed = [l for l in cur if l not in old]
        print("UNCHANGED since freeze" if not changed and len(old) == len(cur) else "CHANGED files:\n" + "\n".join(changed))
    else:
        print("\n".join(cur))
