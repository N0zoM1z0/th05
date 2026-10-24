#!/usr/bin/env python3
"""Validate the pinned TH05 launcher and write a private structural receipt."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from lib.launcher import LauncherError, parse_launcher
from lib.pc98 import digest_file
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact_id", nargs="?", default="th05-zun")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        manifest_path = ROOT / "config/targets.toml"
        artifact = find_artifact(load_target_manifest(manifest_path), args.artifact_id)
        if artifact["format"] != "com":
            raise LauncherError("launcher inspection requires a pinned plain COM carrier")
        data = read_verified_artifact(ROOT, artifact)
        receipt = parse_launcher(data, expected_sha256=artifact["sha256"])
        receipt.update({"artifact": args.artifact_id,
                        "target_manifest_sha256": digest_file(manifest_path),
                        "observer_sha256": digest_file(Path(__file__)),
                        "parser_sha256": digest_file(ROOT / "scripts/lib/launcher.py")})
        output = (args.output or ROOT / ".analysis/launcher" / args.artifact_id / "receipt.json").resolve()
        try:
            output.relative_to((ROOT / ".analysis").resolve())
        except ValueError as error:
            raise LauncherError("launcher receipt must stay below ignored .analysis") from error
        output.parent.mkdir(parents=True, exist_ok=True)
        temporary = output.with_suffix(output.suffix + ".tmp")
        temporary.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
        temporary.replace(output)
        print(f"PASS {args.artifact_id}: {len(data)} bytes, {receipt['procedure_count']} embedded COM records")
        print("Complete physical partition verified; ownership and authored credit remain unreviewed.")
        print(f"receipt: {output}")
        return 0
    except (LauncherError, OSError, ValueError, KeyError) as error:
        print(f"error: launcher inspection failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
