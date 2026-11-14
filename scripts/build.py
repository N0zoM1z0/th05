#!/usr/bin/env python3
"""Build the playable TH05 products (OP/MAIN/MAINE/ZUN) from source.

Each product is a cold Borland build of the pinned ReC98 tree with every
configured maintained TH05 source overlaid (config/maintained_sources.toml).
Products are published together to .analysis/build/th05/ only after all four
builds succeed. A product build grants no exactness credit; the per-unit
replays remain the exactness oracle.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import sys
import uuid

from lib.pc98 import digest_file

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = {"op": "OP.EXE", "main": "MAIN.EXE", "maine": "MAINE.EXE", "zun": "ZUN.COM"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", choices=sorted(PRODUCTS), action="append",
                        help="rebuild only these products; others are reused from the published build")
    parser.add_argument("--output", type=Path, default=ROOT / ".analysis/build/th05")
    args = parser.parse_args()
    selected = args.only or list(PRODUCTS)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    work = ROOT / ".analysis/builds" / f"product-{stamp}-{uuid.uuid4().hex[:8]}"
    previous = json.loads((args.output / "build.json").read_text()) if (args.output / "build.json").exists() else {}
    products = {}
    for artifact in PRODUCTS:
        if artifact not in selected:
            if artifact not in previous.get("products", {}):
                parser.error(f"no published {artifact} to reuse; build it first")
            products[artifact] = previous["products"][artifact]
            continue
        out = work / artifact
        print(f"[{artifact}] building", flush=True)
        subprocess.run([sys.executable, str(ROOT / "scripts/build_reference.py"), artifact, "--overlay",
                        "--output", str(out)], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
        receipt = json.loads((out / "receipt.json").read_text())
        products[artifact] = {"file": PRODUCTS[artifact], "build": str((out / receipt["output"]).relative_to(ROOT)),
                              "bytes": (out / receipt["output"]).stat().st_size, "sha256": receipt["sha256"],
                              "original_equal": receipt["raw_file_equal"],
                              "overlays": [o["source"] for o in receipt["overlays"]]}
        print(f"[{artifact}] {products[artifact]['bytes']} bytes, {len(receipt['overlays'])} overlays, "
              f"original-equal={receipt['raw_file_equal']}", flush=True)
    staging = args.output.with_name(args.output.name + ".new")
    shutil.rmtree(staging, ignore_errors=True)
    staging.mkdir(parents=True)
    for artifact, row in products.items():
        shutil.copyfile(ROOT / row["build"], staging / row["file"])
        if digest_file(staging / row["file"]) != row["sha256"]:
            raise RuntimeError(f"{row['file']} changed while publishing")
    (staging / "build.json").write_text(json.dumps({"schema_version": 1, "built": stamp, "products": products},
                                                   indent=2) + "\n")
    shutil.rmtree(args.output, ignore_errors=True)
    staging.rename(args.output)
    print(f"PASS: published {', '.join(r['file'] for r in products.values())} to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
