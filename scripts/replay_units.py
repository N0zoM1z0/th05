#!/usr/bin/env python3
"""Two cold C++ unit builds with target link bindings and a compiled negative control.

The symbol-only scaffold supplies fixed external addresses, never target code.
Its unused origin holes are excluded. This proves complete unit bytes, not
whole-program placement, standalone linkage, packing or executable equality.
"""
from __future__ import annotations
import argparse
import fcntl
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tomllib
import uuid

from lib.omf import describe_omf
from lib.pc98 import digest_bytes, digest_file, parse_mz
from lib.reference_build import Builder
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from lib.unit_oracle import compare_unit, map_contribution

ROOT = Path(__file__).resolve().parents[1]


def cold_round(work: Path, inputs: Path, units: list[dict], *, negative: bool = False) -> dict:
    source = work / "source"
    source.mkdir(parents=True)
    shutil.copytree(inputs / "src", source / "src")
    for unit in units:
        wrapper = source / unit["module"]
        wrapper.parent.mkdir(parents=True, exist_ok=True)
        if unit["id"] == "main-player-angle":
            # The original module wrapper sets the group/segment via shared
            # declarations. State them explicitly in this isolated producer.
            prefix = '#pragma option -zCPLAYER_A_TEXT -zPmain_03\n'
        else:
            prefix = ""
        wrapper.write_text(prefix + f'#include "{unit["source"]}"\n')
    if negative:
        path = source / "src/main/bullet/tune.cpp"
        data = path.read_text()
        if data.count("_AL >= 38") != 1:
            raise ValueError("compiled negative-control mutation anchor drifted")
        path.write_text(data.replace("_AL >= 38", "_AL >= 39"))
    shutil.copyfile(inputs / "main_bindings.asm", source / "bindings.asm")
    # Reuse the driver for serialization/logging, not its reference build plan.
    (source / "build_dumb.bat").touch()
    builder = Builder(source, ROOT / ".analysis/toolchain/wineprefix", ROOT / "_reference/ReC98/bin/msdos.exe")
    dos = ["wine", str(builder.msdos), "-e", "-x"]
    builder.execute("bindings", ["wine", r"C:\TASM50\bin\TASM32.EXE", "/m", "/mx", "/t", "bindings.asm", "bindings.obj"])
    objects = []
    omfs = {}
    for unit in units:
        obj = Path(unit["module"]).stem + ".obj"
        builder.execute(obj, [*dos, "tcc", "-c", "-I.", "-O", "-b-", "-3", "-Z", "-d",
                              "-DGAME=5", "-ml", "-DBINARY='M'", unit["module"]])
        objects.append(obj)
        omf = describe_omf((source / obj).read_bytes())
        if not omf["valid"] or omf["translator_comments"] != ["TC86 Borland C++ 4.02"]:
            raise ValueError(f"invalid compiler object {obj}")
        omfs[unit["id"]] = {key: omf[key] for key in
            ("sha256", "dependency_timestamp_normalized_sha256", "module_name", "translator_comments", "dependency_paths")}
    (source / "link.rsp").write_bytes(("-c -s -E bindings.obj " + " ".join(objects) +
                                       ", units.exe, units.map,\r\n").encode("ascii"))
    builder.execute("link", [*dos, "tlink", "@link.rsp"])
    candidate = parse_mz((source / "units.exe").read_bytes())
    if not candidate.valid:
        raise ValueError(str(candidate.errors))
    return {"source": source, "candidate": candidate, "omfs": omfs, "steps": builder.records}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    manifest_bytes = (ROOT / "config/exact_units.toml").read_bytes()
    manifest_sha256 = digest_bytes(manifest_bytes)
    manifest = tomllib.loads(manifest_bytes.decode())
    units = manifest["units"]
    artifact = find_artifact(load_target_manifest(ROOT / "config/targets.toml"), manifest["artifact"])
    target = parse_mz(read_verified_artifact(ROOT, artifact))
    work = (args.output or ROOT / ".analysis/unit-replays" / uuid.uuid4().hex).resolve()
    if work.exists():
        parser.error("cold replay requires a new output directory")
    work.mkdir(parents=True)
    (work / "exact-units.toml").write_bytes(manifest_bytes)
    with (ROOT / ".analysis/borland.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        subprocess.run([sys.executable, str(ROOT / "scripts/attest_toolchain.py")], check=True)
        shutil.copyfile(ROOT / ".analysis/toolchain/attestation.json", work / "toolchain-attestation.json")
        inputs = work / "inputs"
        inputs.mkdir()
        shutil.copytree(ROOT / "src", inputs / "src")
        shutil.copyfile(ROOT / "probes/units/main_bindings.asm", inputs / "main_bindings.asm")
        frozen = [{"path": str(p.relative_to(inputs)), "sha256": digest_file(p)}
                  for p in sorted(inputs.rglob("*")) if p.is_file()]
        rounds = [cold_round(work / label, inputs, units) for label in ("a", "b")]
        results = []
        for unit in units:
            comparisons = []
            for round_ in rounds:
                start, size = map_contribution(round_["source"] / "units.map", unit["module"], unit["segment"])
                if size != unit["size"]:
                    raise ValueError(f"{unit['id']}: complete contribution size mismatch: {size}")
                comparisons.append(compare_unit(target, round_["candidate"], unit["target_start"], start, size))
            object_equal = rounds[0]["omfs"][unit["id"]]["dependency_timestamp_normalized_sha256"] == rounds[1]["omfs"][unit["id"]]["dependency_timestamp_normalized_sha256"]
            results.append({"id": unit["id"], "rounds": comparisons,
                            "object_normalized_equal": object_equal,
                            "omfs": [r["omfs"][unit["id"]] for r in rounds],
                            "exact": object_equal and all(c["exact"] for c in comparisons)})
        negative = cold_round(work / "negative", inputs, units, negative=True)
        tune = next(u for u in units if u["id"] == "main-bullet-tune")
        start, size = map_contribution(negative["source"] / "units.map", tune["module"], tune["segment"])
        control = compare_unit(target, negative["candidate"], tune["target_start"], start, size)
        accepted = all(r["exact"] for r in results) and not control["exact"]
        receipt = {"schema_version": 1, "kind": "bounded-cxx-unit-exact-replay",
                   "target_sha256": artifact["sha256"], "manifest_sha256": manifest_sha256,
                   "toolchain_receipt_sha256": digest_file(work / "toolchain-attestation.json"),
                   "source_inputs": frozen, "results": results, "compiled_negative_control": control,
                   "complete_executable_exact": False, "pass": accepted}
        if digest_file(ROOT / "config/exact_units.toml") != manifest_sha256:
            raise ValueError("unit configuration changed during replay")
        for item in frozen:
            live = (ROOT / "probes/units/main_bindings.asm" if item["path"] == "main_bindings.asm"
                    else ROOT / item["path"])
            if digest_file(live) != item["sha256"]:
                raise ValueError(f"source input changed during replay: {live}")
        (work / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"pass": accepted, "results": [{"id": r["id"], "exact": r["exact"]} for r in results],
                      "compiled_negative_rejected": not control["exact"], "receipt": str(work / "receipt.json")}, indent=2))
    return 0 if accepted else 1


if __name__ == "__main__":
    raise SystemExit(main())
