#!/usr/bin/env python3
"""Compile Boss BG once and diagnose complete functions; never accept progress.

Run through run_heavy. Symbol-only context holes surround the complete compiler
contribution. Its actual OMF size controls the foreign tail, not target bytes.
This research probe requires the earlier monolithic BOSS_BG_TEXT candidate.
The current maintained owner uses two CODE contributions and is deliberately
outside this probe's accepted shape; use replay_units.py for current evidence.
"""
from __future__ import annotations
import argparse
import fcntl
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import uuid

from lib.omf import describe_omf, parse_omf
from lib.pc98 import parse_mz
from lib.reference_build import Builder
from lib.replay_toolchain import (compiler_dependencies, digest, freeze_toolchain,
    include_closure, snapshot_paths, static_toolchain, validate_snapshot)
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from lib.unit_oracle import (compare_mapped_unit, map_contribution, map_publics,
    map_unit_scope, relative_fixups)
from replay_units import mapped_control_comparison

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "src/main/boss/background.cpp"
MODULE = "th05/boss_bg.cpp"
BINDINGS = "probes/units/boss_background_bindings.asm"
SEGMENT = "BOSS_BG_TEXT"
REVIEW = ".analysis/boss-background-boundary-review.json"
UNIT_START = 0x10A17
FLAGS = ("-c", "-I.", "-O", "-b-", "-3", "-Z", "-d", "-DGAME=5", "-ml", "-DBINARY='M'")


def omf_index(data: bytes, cursor: int) -> tuple[int, int]:
    if cursor >= len(data):
        raise ValueError("truncated OMF index")
    first = data[cursor]
    if first & 0x80:
        if cursor + 1 >= len(data):
            raise ValueError("truncated two-byte OMF index")
        return ((first & 0x7F) << 8) | data[cursor + 1], cursor + 2
    return first, cursor + 1


def compiled_code_size(raw: bytes) -> dict:
    """Read genuine SEGDEF length and prove every CODE byte has compiler LEDATA."""
    records = parse_omf(raw)
    names = [""]
    for record in records:
        if record.record_type == 0x96:
            cursor = 0
            while cursor < len(record.data):
                count = record.data[cursor]
                cursor += 1
                if cursor + count > len(record.data):
                    raise ValueError("truncated OMF LNAMES")
                names.append(record.data[cursor:cursor + count].decode("cp437"))
                cursor += count
    segments = []
    for record in records:
        if record.record_type not in (0x98, 0x99):
            continue
        data = record.data
        if not data or not data[0] >> 5:
            raise ValueError("unexpected absolute or empty compiler SEGDEF")
        width = 4 if record.record_type == 0x99 else 2
        if len(data) < 1 + width:
            raise ValueError("truncated compiler SEGDEF")
        size = int.from_bytes(data[1:1 + width], "little")
        if data[0] & 2:
            size = 1 << (width * 8)
        name, cursor = omf_index(data, 1 + width)
        cls, cursor = omf_index(data, cursor)
        _, cursor = omf_index(data, cursor)
        if cursor != len(data) or max(name, cls) >= len(names):
            raise ValueError("invalid compiler SEGDEF name/class indices")
        segments.append({"index": len(segments) + 1, "name": names[name],
                         "class": names[cls], "size": size,
                         "alignment": data[0] >> 5, "combine": (data[0] >> 2) & 7})
    nonempty = [row for row in segments if row["size"]]
    if not nonempty or any(row["name"] != SEGMENT or row["class"] != "CODE" or
                           row["combine"] != 2 or row["alignment"] != 1 for row in nonempty):
        raise ValueError(f"unexpected additional compiler-owned segments: {nonempty}")
    size = sum(row["size"] for row in nonempty)
    if not 0 < size < 0x10000:
        raise ValueError("unexpected compiler code size")
    extents_by_index = {row["index"]: [] for row in nonempty}
    for record in records:
        if record.record_type not in (0xA0, 0xA1, 0xA2, 0xA3):
            continue
        index, cursor = omf_index(record.data, 0)
        if index not in extents_by_index:
            continue
        if record.record_type in (0xA2, 0xA3):
            raise ValueError("iterated data cannot silently create code holes")
        width = 4 if record.record_type == 0xA1 else 2
        if len(record.data) < cursor + width:
            raise ValueError("truncated CODE LEDATA")
        offset = int.from_bytes(record.data[cursor:cursor + width], "little")
        length = len(record.data) - cursor - width
        if length:
            extents_by_index[index].append((offset, offset + length))
    members, combined, base = [], [], 0
    for segment in nonempty:
        extents = sorted(extents_by_index[segment["index"]])
        cursor = 0
        for start, end in extents:
            if start != cursor or end > segment["size"]:
                raise ValueError("compiler CODE LEDATA has a gap, overlap or overflow")
            cursor = end
        if cursor != segment["size"]:
            raise ValueError("compiler CODE size is not fully covered by LEDATA")
        members.append({**segment, "ledata_extents": extents})
        combined.extend((base + start, base + end) for start, end in extents)
        base += segment["size"]
    return {"name": SEGMENT, "class": "CODE", "size": size, "members": members,
            "segments": segments, "ledata_extents": combined}


def verify_layout(path: Path, size: int) -> list[dict]:
    expected = {
        "_TEXT": (0, 0, 0xAE10),
        SEGMENT: (0xAE1, 0, UNIT_START - 0xAE10),
        "BG_FOREIGN_TAIL": (0xAE1, UNIT_START + size - 0xAE10, 0x14AB0 - UNIT_START - size),
        "SHARED": (0x14AB, 0, 0x3B0),
        "BG_DGROUP_GAP": (0x14E6, 0, 0x209D0 - 0x14E60),
        "_DATA": (0x209D, 0, 0xC692),
    }
    observed = {}
    for line in path.read_text(encoding="cp437").splitlines():
        match = re.match(r"\s*([0-9A-F]{4}):([0-9A-F]{4})\s+([0-9A-F]{4})\s+C=\S+\s+S=(\S+)\s+G=\S+\s+M=(\S+)", line, re.I)
        if match and match[5].lower() == "bindings.asm" and match[4] in expected:
            if match[4] in observed:
                raise ValueError("ambiguous binding segment contribution")
            observed[match[4]] = tuple(int(match[index], 16) for index in (1, 2, 3))
    if observed != expected:
        raise ValueError(f"foreign frame/DS layout drift: expected {expected}; observed {observed}")
    return [{"segment": name, "frame": values[0], "offset": values[1], "size": values[2]}
            for name, values in observed.items()]


def run(output: Path, *, resume_object: Path | None = None) -> dict:
    output = output.resolve()
    output.relative_to((ROOT / ".analysis").resolve())
    output.mkdir(parents=True, exist_ok=False)
    receipt = {"schema_version": 1, "kind": "boss-background-single-producer-diagnostic",
               "reconstruction_accepted": False, "authored_credit": 0,
               "compiler_invocations": 0, "functions": []}
    try:
        with (ROOT / ".analysis/borland.lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            tool = freeze_toolchain(ROOT, output / "toolchain-attestation.json", allow_probes=False)
            receipt["toolchain"] = tool
            shutil.copyfile(ROOT / "config/toolchain.toml", output / "toolchain.toml")
            review = json.loads((ROOT / REVIEW).read_text())
            shutil.copyfile(ROOT / REVIEW, output / "boundary-review.json")
            receipt["review_sha256"] = digest(output / "boundary-review.json")
            artifact = find_artifact(load_target_manifest(ROOT / "config/targets.toml"), "th05-main")
            target = parse_mz(read_verified_artifact(ROOT, artifact))
            span = target.program_image[review["load_start"]:review["load_start"] + review["size"]]
            if (not target.valid or review["target_sha256"] != artifact["sha256"] or
                    review["load_start"] != UNIT_START or hashlib.sha256(span).hexdigest() != review["extent_sha256"] or
                    relative_fixups(target, UNIT_START, review["size"]) !=
                    [row["relative_offset"] for row in review["ordered_mz_fixups"]]):
                raise ValueError("target boundary review does not reproduce pinned original bytes/fixups")
            cursor = UNIT_START
            for function in review["functions"]:
                if function["start"] != cursor or function["end"] != cursor + function["size"]:
                    raise ValueError("original complete function boundaries are not contiguous")
                cursor = function["end"]
            if cursor != UNIT_START + review["size"] or len(review["functions"]) != 19:
                raise ValueError("original complete contribution boundary mismatch")
            paths = include_closure(ROOT, SOURCE) | {BINDINGS}
            source = output / "source"
            origin = None
            if resume_object is not None:
                resume_object = resume_object.resolve()
                resume_object.relative_to((ROOT / ".analysis").resolve())
                origin_path = resume_object.parent / "receipt.json"
                origin = json.loads(origin_path.read_text())
                if (origin["kind"] != receipt["kind"] or
                        origin["toolchain"]["manifest_sha256"] != tool["manifest_sha256"] or
                        digest(resume_object / "boss_bg.obj") != origin["omf"]["sha256"]):
                    raise ValueError("saved object provenance or original toolchain pin disagrees")
                shutil.copytree(resume_object, source)
                receipt["resumed_object"] = {"source_directory": str(resume_object.relative_to(ROOT)),
                                             "original_receipt_sha256": digest(origin_path),
                                             "object_sha256": digest(source / "boss_bg.obj")}
            else:
                source.mkdir()
                for name in paths:
                    destination = source / name
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(ROOT / name, destination)
                wrapper = source / MODULE
                wrapper.parent.mkdir(parents=True)
                wrapper.write_text('#pragma option -zPmain_01\n#include "' + SOURCE + '"\n')
            (source / "build_dumb.bat").touch()
            builder = Builder(source, ROOT / ".analysis/toolchain/wineprefix", ROOT / "_reference/ReC98/bin/msdos.exe")
            receipt["steps"] = builder.records
            dos = ["wine", str(builder.msdos), "-e", "-x"]
            if resume_object is None:
                receipt["compiler_invocations"] = 1
                builder.execute("boss_bg.obj", [*dos, "tcc", *FLAGS, MODULE])
            raw_object = (source / "boss_bg.obj").read_bytes()
            omf = describe_omf(raw_object)
            if not omf["valid"] or omf["translator_comments"] != ["TC86 Borland C++ 4.02"]:
                raise ValueError("unexpected compiler object identity")
            receipt["omf"] = omf
            code = compiled_code_size(raw_object)
            receipt["compiled_code"] = code
            if UNIT_START + code["size"] >= 0x14AAA:
                raise ValueError("compiled contribution collides with the real Louise external context")
            base_entry = {"source": SOURCE, "module": MODULE, "segment": SEGMENT, "bindings_source": BINDINGS}
            consumed = compiler_dependencies(base_entry, [omf])
            if not consumed.issubset(paths):
                raise ValueError("compiler consumed unstaged maintained dependencies")
            if origin is not None:
                historical = {row["path"]: row["sha256"] for row in origin["artifacts"]}
                for name in consumed | {MODULE}:
                    if historical.get("source/" + name) != digest(source / name):
                        raise ValueError("saved compiler source differs from its original diagnostic archive")
                # The binder may be refined after a failed context link. It was
                # not a compiler input, so copy its current reviewed template.
                shutil.copyfile(ROOT / BINDINGS, source / BINDINGS)
            if (source / MODULE).read_text() != '#pragma option -zPmain_01\n#include "' + SOURCE + '"\n':
                raise ValueError("saved compiler wrapper changed")
            for name in consumed:
                if digest(source / name) != digest(ROOT / name):
                    raise ValueError("saved compiler source no longer matches maintained source")
            receipt["source_inputs"] = snapshot_paths(ROOT, consumed | {BINDINGS})
            (source / "bg_size.inc").write_text(f"; Derived only from compiler OMF.\nCOMPILED_BG_SIZE equ {code['size']}\n")
            shutil.copyfile(source / BINDINGS, source / "bindings.asm")
            builder.execute("bindings", ["wine", r"C:\TASM50\bin\TASM32.EXE", "/m", "/mx", "/t", "bindings.asm", "bindings.obj"])
            (source / "link.rsp").write_bytes(b"-c -s -E bindings.obj boss_bg.obj, units.exe, units.map,\r\n")
            builder.execute("link", [*dos, "tlink", "@link.rsp"])
            candidate = parse_mz((source / "units.exe").read_bytes())
            if not candidate.valid:
                raise ValueError(str(candidate.errors))
            map_path = source / "units.map"
            start, size = map_contribution(map_path, MODULE, SEGMENT)
            if (start, size) != (UNIT_START, code["size"]):
                raise ValueError("linked compiler contribution does not match actual OMF extent")
            receipt["layout"] = verify_layout(map_path, size)
            actual_names = [name for address, name in sorted(map_publics(map_path)) if start <= address < start + size]
            if actual_names != [function["name"] for function in review["functions"]]:
                raise ValueError(f"compiler complete function list changed: {actual_names}")
            for index, function in enumerate(review["functions"]):
                entry = {**base_entry, "id": f"diagnostic-boss-bg-{index:02d}", "functions": 1,
                         "target_start": function["start"], "size": function["size"], "function_symbol": function["name"]}
                if index + 1 < len(review["functions"]):
                    entry["function_end_symbol"] = review["functions"][index + 1]["name"]
                scope = map_unit_scope(map_path, entry)
                comparison = (compare_mapped_unit(target, candidate, map_path, entry) if scope["size"] == entry["size"]
                              else mapped_control_comparison(target, candidate, entry, map_path))
                receipt["functions"].append({"name": function["name"], "entry": entry, "comparison": comparison})
            receipt["target_sha256"] = artifact["sha256"]
            receipt["map_sha256"] = digest(map_path)
            receipt["candidate_sha256"] = digest(source / "units.exe")
            receipt["script_sha256"] = digest(Path(__file__))
            validate_snapshot(ROOT, receipt["source_inputs"])
            if digest(ROOT / REVIEW) != receipt["review_sha256"] or static_toolchain(ROOT)[0] != tool["manifest_sha256"]:
                raise ValueError("inputs or toolchain changed during diagnosis")
            receipt["pass"] = True
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as error:
        receipt.update({"pass": False, "error": str(error)[:5000]})
    receipt["matched_functions"] = [row["name"] for row in receipt["functions"] if row["comparison"]["exact"]]
    receipt["all_functions_exact"] = len(receipt["functions"]) == 19 and len(receipt["matched_functions"]) == 19
    receipt["artifacts"] = [{"path": path.relative_to(output).as_posix(), "sha256": digest(path), "size": path.stat().st_size}
                            for path in sorted(output.rglob("*")) if path.is_file()]
    (output / "receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--resume-object", type=Path, help="saved private source directory; skip TCC entirely")
    args = parser.parse_args()
    output = args.output or ROOT / ".analysis/compiler-probes" / ("boss-bg-" + uuid.uuid4().hex)
    receipt = run(output, resume_object=args.resume_object)
    print(json.dumps({"output": str(output.resolve()), "pass": receipt["pass"],
                      "compiled_size": receipt.get("compiled_code", {}).get("size"),
                      "matched_functions": receipt["matched_functions"], "error": receipt.get("error"),
                      "reconstruction_accepted": False}, indent=2))
    return 0 if receipt["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
