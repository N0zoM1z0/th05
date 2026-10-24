#!/usr/bin/env python3
"""Cold build only one TH05 reference executable as untrusted linking scaffold."""
from __future__ import annotations
import argparse
import fcntl
import json
from pathlib import Path
import shutil
import subprocess
import tarfile
import tomllib
import uuid

from lib.pc98 import digest_file, parse_mz
from lib.reference_build import Builder
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact

ROOT = Path(__file__).resolve().parents[1]
REVISION = "b6ba5b0a529edbb31efdf8c0e939263804f8ee47"


def materialize(destination: Path) -> None:
    destination.mkdir(parents=True)
    archive = destination.parent / "source.tar"
    subprocess.run(["git", "-C", str(ROOT / "_reference/ReC98"), "archive",
                    f"--output={archive}", REVISION], check=True)
    with tarfile.open(archive) as stream:
        stream.extractall(destination, filter="data")
    archive.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", choices=["main", "op", "maine"])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--overlay", action="store_true", help="overlay configured maintained sources")
    args = parser.parse_args()
    target = find_artifact(load_target_manifest(ROOT / "config/targets.toml"), f"th05-{args.artifact}")
    target_data = read_verified_artifact(ROOT, target)
    work = (args.output or ROOT / ".analysis/builds" / uuid.uuid4().hex).resolve()
    if work.exists():
        parser.error("output exists; use a fresh path for a cold build")
    work.mkdir(parents=True)
    with (ROOT / ".analysis/borland.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        source = work / "source"
        materialize(source)
        overlays = []
        if args.overlay:
            config = tomllib.loads((ROOT / "config/maintained_sources.toml").read_text())
            shutil.copytree(ROOT / "src", source / "src")
            for entry in config.get("sources", []):
                if entry["artifact"] != args.artifact:
                    continue
                data = (ROOT / entry["source"]).read_bytes()
                (source / entry["reference_path"]).write_bytes(data)
                overlays.append({**entry, "sha256": digest_file(ROOT / entry["source"])})
        builder = Builder(source, ROOT / ".analysis/toolchain/wineprefix", ROOT / "_reference/ReC98/bin/msdos.exe")
        result = builder.build(f"bin/th05/{args.artifact}.exe")
        image = parse_mz(result.read_bytes())
        if not image.valid:
            raise RuntimeError(str(image.errors))
        receipt = {"kind": "untrusted-reference-scaffold", "revision": REVISION,
                   "artifact": args.artifact, "overlays": overlays,
                   "output": str(result.relative_to(work)), "sha256": digest_file(result),
                   "target_sha256": target["sha256"], "raw_file_equal": result.read_bytes() == target_data,
                   "steps": builder.records}
        (work / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"PASS: {len(builder.records)} serial steps; scaffold only: {work}")
    print(f"Raw complete-file equality: {receipt['raw_file_equal']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
