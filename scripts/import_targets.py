#!/usr/bin/env python3
"""Read the pinned Japanese HDI without modifying it; import private TH05 files."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile
import tomllib

from lib.pc98 import digest_file, find_fat_boot_sectors, parse_fat_boot_sector
from lib.targets import read_verified_artifact

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("hdi", type=Path)
    args = parser.parse_args()
    manifest = tomllib.loads((ROOT / "config/targets.toml").read_text())
    source = manifest["source"]
    hdi = args.hdi.resolve()
    if digest_file(hdi) != source["hdi_sha256"]:
        parser.error("HDI SHA-256 differs from the pinned Japanese image")
    data = hdi.read_bytes()
    reserved, _, header_size, size, sector, *_ = struct.unpack_from("<8I", data)
    if reserved or header_size != source["hdi_header_size"] or header_size + size != len(data):
        parser.error("invalid Anex86 HDI geometry")
    offset = source["fat_partition_offset"]
    boot = parse_fat_boot_sector(data, offset)
    if boot.volume_label != source["fat_volume_label"] or offset not in {
        b.offset for b in find_fat_boot_sectors(data, header_size, sector)
    }:
        parser.error("FAT partition disagrees with the pinned layout")
    if not shutil.which("mcopy"):
        parser.error("mtools (mcopy) is required")
    analysis = ROOT / ".analysis"
    analysis.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="import-", dir=analysis) as temp:
        staging = Path(temp)
        for artifact in manifest["artifacts"]:
            dest = staging / artifact["private_path"]
            dest.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(
                ["mcopy", "-i", f"{hdi}@@{offset}", f"::{artifact['dos_path']}", str(dest)],
                env={**os.environ, "MTOOLS_SKIP_CHECK": "1"}, check=True,
            )
            read_verified_artifact(staging, artifact)
        for artifact in manifest["artifacts"]:
            dest = ROOT / artifact["private_path"]
            dest.parent.mkdir(parents=True, exist_ok=True)
            os.replace(staging / artifact["private_path"], dest)
    receipt = {"hdi": str(hdi), "sha256": source["hdi_sha256"],
               "canonicality": source["canonicality"], "artifacts": manifest["artifacts"]}
    (analysis / "target-import.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"PASS: {len(manifest['artifacts'])} hash-attested TH05 artifacts imported")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
