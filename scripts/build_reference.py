#!/usr/bin/env python3
"""Cold build only one TH05 reference executable as untrusted linking scaffold."""
from __future__ import annotations
import argparse
import re
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
from lib.replay_toolchain import freeze_toolchain

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



CALIBRATION_MAPS = {"main": ".analysis/builds/main-calibration-b/source/obj/th05/main.map",
                    "op": ".analysis/builds/op-calibration-a/source/obj/th05/op.map",
                    "maine": ".analysis/builds/maine-calibration-a/source/obj/th05/maine.map"}


def code_order_anchor(artifact: str, extra: list[tuple[str, str]] = ()) -> str:
    """Empty SEGDEF/GRPDEF anchor keeping overlay context segments inside their group.

    TLINK orders segments by first appearance. Maintained headers declare foreign
    functions under empty context segments (e.g. SMALL_MAIN01_CONTEXT in main_01);
    first seen late, they would stretch main_01 over every main_03 segment.
    """
    order, group_of = [], {}
    for line in (ROOT / CALIBRATION_MAPS[artifact]).read_text(encoding="cp437").splitlines():
        m = re.match(r"\s*[0-9A-F]{4}:[0-9A-F]{4}\s+[0-9A-F]{4}\s+C=CODE\s+S=(\S+)\s+G=(\S+)", line)
        if m and m[1] not in group_of:
            order.append(m[1])
            group_of[m[1]] = m[2].lower()
    contexts = {}
    for path in (ROOT / "src").rglob("*"):
        if path.suffix not in (".cpp", ".c", ".hpp", ".h", ".inl"):
            continue
        for m in re.finditer(r"^#pragma codeseg[ \t]+(\w+)[ \t]+(\w+)", path.read_text(errors="replace"), re.M):
            if m[1] not in group_of and m[2].lower() in set(group_of.values()):
                contexts.setdefault(m[1], m[2].lower())
    for name, group in extra:  # segments of integrated unit objects
        if name not in group_of and group.lower() in set(group_of.values()):
            contexts.setdefault(name, group.lower())
    for name, group in sorted(contexts.items()):
        last = max((i for i, seg in enumerate(order) if group_of[seg] == group), default=len(order) - 1)
        order.insert(last + 1, name)
        group_of[name] = group
    lines = [f"{seg} segment byte public 'CODE' use16\n{seg} ends" for seg in order]
    groups = {}
    for seg in order:
        if group_of[seg] != "(none)":
            groups.setdefault(group_of[seg], []).append(seg)
    for g, segs in groups.items():  # repeated GROUP statements keep TASM lines short
        lines += [f"{g} group {', '.join(segs[i:i + 8])}" for i in range(0, len(segs), 8)]
    return ".386\n" + "\n".join(lines) + "\nend\n"

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", choices=["main", "op", "maine", "zun"])
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
        tool = freeze_toolchain(ROOT, work / "toolchain-attestation.json", allow_probes=False)
        shutil.copyfile(ROOT / "config/toolchain.toml", work / "toolchain.toml")
        source = work / "source"
        materialize(source)
        overlays = []
        if args.overlay:
            config = tomllib.loads((ROOT / "config/maintained_sources.toml").read_text())
            shutil.copytree(ROOT / "src", source / "src")
            from lib.replay_toolchain import include_closure
            encodings = {}
            for suffix in ("", ".op", ".maine", ".zun"):
                for unit in tomllib.loads((ROOT / f"config/exact_units{suffix}.toml").read_text())["units"]:
                    if unit.get("source_encoding") == "cp932":
                        encodings[unit["source"]] = "cp932"
            converted = set()
            for entry in config.get("sources", []):
                if entry["artifact"] != args.artifact:
                    continue
                if encodings.get(entry["source"]) == "cp932":
                    # Same staging as the exact replays: UTF-8 sources become Shift-JIS.
                    for name in include_closure(ROOT, entry["source"]):
                        if name.startswith("src/") and name not in converted:
                            path = source / name
                            path.write_bytes(path.read_bytes().decode("utf-8").encode("cp932"))
                            converted.add(name)
                if entry.get("wrapper"):
                    # Same form as the exact replay wrapper: unit pragmas, then the source.
                    prefix = f"#pragma option {entry['wrapper_options']}\n" if entry.get("wrapper_options") else ""
                    # ReC98 shares some th04 objects compiled with GAME=4; these owners are TH05's.
                    data = (prefix + "#undef GAME\n#define GAME 5\n"
                            f'#include "{entry["source"]}"\n').encode("ascii")
                else:
                    data = (ROOT / entry["source"]).read_bytes()
                (source / entry["reference_path"]).write_bytes(data)
                overlays.append({**entry, "sha256": digest_file(ROOT / entry["source"])})
        builder = Builder(source, ROOT / ".analysis/toolchain/wineprefix", ROOT / "_reference/ReC98/bin/msdos.exe")
        if args.overlay and args.artifact != "zun":
            from lib.reference_build import Rule
            (source / "anchor.asm").write_text(code_order_anchor(args.artifact))
            exe = f"bin/th05/{args.artifact}.exe"
            link = builder.rules[exe]
            if "c0l.obj " not in link.response:
                raise RuntimeError("unexpected linker response")
            builder.rules["obj/th05/anchor.obj"] = Rule("tasm32", ("/m", "/mx", "/t", "anchor.asm", "obj\\th05\\anchor.obj"),
                                                        ("anchor.asm",))
            builder.rules[exe] = Rule("tlink", (), ("obj/th05/anchor.obj", *link.dependencies),
                                      link.response.replace("c0l.obj ", "c0l.obj obj\\th05\\anchor.obj ", 1))
        suffix = "com" if args.artifact == "zun" else "exe"
        result = builder.build(f"bin/th05/{args.artifact}.{suffix}")
        integration = None
        if args.overlay and args.artifact in ("main", "maine"):
            # Replace dump procedures with the accepted units that reproduce them.
            from integrate_product import integrate
            integration = integrate(source, args.artifact)
            (work / "integration.json").write_text(json.dumps(integration, indent=2) + "\n")
        if suffix == "exe":
            image = parse_mz(result.read_bytes())
            if not image.valid:
                raise RuntimeError(str(image.errors))
        receipt = {"kind": "untrusted-reference-scaffold", "revision": REVISION,
                   "artifact": args.artifact, "overlays": overlays,
                   "integrated_units": integration["integrated_units"] if integration else [],
                   "output": str(result.relative_to(work)), "sha256": digest_file(result),
                   "target_sha256": target["sha256"], "raw_file_equal": result.read_bytes() == target_data,
                   "toolchain_receipt_sha256": tool["receipt_sha256"],
                   "toolchain_manifest_sha256": tool["manifest_sha256"],
                   "toolchain_reused": tool["reused"], "toolchain_reuse_proof_sha256": tool["proof_sha256"],
                   "steps": builder.records}
        (work / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"PASS: {len(builder.records)} serial steps; scaffold only: {work}")
    print(f"Raw complete-file equality: {receipt['raw_file_equal']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
