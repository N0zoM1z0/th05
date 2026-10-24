#!/usr/bin/env python3
"""Verify every private target and report its actual DOS topology."""
import json
from pathlib import Path

from lib.pc98 import describe_blob
from lib.targets import load_target_manifest, read_verified_artifact

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    manifest = load_target_manifest(ROOT / "config/targets.toml")
    for artifact in manifest["artifacts"]:
        data = read_verified_artifact(ROOT, artifact)
        print(f"PASS {artifact['id']}: {len(data):,} bytes / {artifact['format']} / {artifact['sha256']}")
        dest = ROOT / ".analysis/targets" / (artifact["id"] + ".json")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(describe_blob(data), indent=2, sort_keys=True) + "\n")
    print("Provenance: " + manifest["source"]["canonicality"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
