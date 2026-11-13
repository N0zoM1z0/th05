#!/usr/bin/env python3
"""Verify Borland CT.LIB's brk/sbrk entrypoints in the ZUN -S resident child.

The 127-byte tiny-model CODE segment is compared to its pinned CT.LIB member
with all five 16-bit OMF external relocations applied. The only ten differing
bytes are those relocation words; the target resolves them to the already
accepted C0T CRT DATA symbols _errno and ___brklvl. The module also supplies
___brk/___sbrk, the exact two entrypoints called by the adjacent nearheap
member. No compiler replay or authored-code credit is involved.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import tomllib

from lib.pc98 import digest_bytes, digest_file
from lib.toolchain import attest_surface
from replay_zun_crt import reviewed_claims as reviewed_crt_claims
from review_zun_nearheap import _index, _object_from_member, _pascal
from lib.borland_library import library_members
from lib.launcher import parse_launcher
from lib.omf import parse_omf
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/zun_brk.toml"
PUBLIC = ROOT / "config/zun_brk_acceptance.json"
CLAIM_ORIGIN = "reviewed-native-zun-com-reconstruction"


def _module(config: dict) -> dict:
    library = (ROOT / config["library_path"]).read_bytes()
    if digest_bytes(library) != config["library_sha256"]:
        raise ValueError("pinned Borland CT.LIB changed")
    members = [m for m in library_members(library)
               if m.name.casefold() == config["library_member"].casefold()]
    if len(members) != 1:
        raise ValueError("brk library member is missing or ambiguous")
    member = members[0]
    obj = _object_from_member(member)
    if (digest_bytes(member.program_records) != config["module_program_records_sha256"] or
            digest_bytes(obj) != config["module_object_sha256"]):
        raise ValueError("brk member OMF identity changed")

    names = [""]
    segments = {}
    groups = {}
    publics = {}
    externals = []
    ledatas = {}
    fixup_records = []
    fixups = []
    current = None
    for record in parse_omf(obj):
        data = record.data
        if record.name == "LNAMES":
            position = 0
            while position < len(data):
                value, position = _pascal(data, position)
                names.append(value)
        elif record.name == "SEGDEF":
            position = 0
            attributes = data[position]
            position += 1
            if attributes & 1:
                length = int.from_bytes(data[position:position + 4], "little")
                position += 4
            else:
                length = int.from_bytes(data[position:position + 2], "little")
                position += 2
            name_index, position = _index(data, position)
            class_index, position = _index(data, position)
            _, position = _index(data, position)
            if (not 0 < name_index < len(names) or
                    not 0 < class_index < len(names) or position != len(data)):
                raise ValueError("brk SEGDEF has invalid names or trailing data")
            segments[len(segments) + 1] = (
                length, names[name_index], names[class_index]
            )
        elif record.name == "GRPDEF":
            position = 0
            name_index, position = _index(data, position)
            if not 0 < name_index < len(names):
                raise ValueError("brk GRPDEF has an invalid group name")
            members_in_group = []
            while position < len(data):
                if data[position] != 0xFF:
                    raise ValueError("brk GRPDEF has an unsupported component")
                position += 1
                segment_index, position = _index(data, position)
                members_in_group.append(segment_index)
            groups[len(groups) + 1] = (names[name_index], members_in_group)
        elif record.name == "PUBDEF":
            position = 0
            _, position = _index(data, position)  # group
            segment, position = _index(data, position)
            if segment == 0:
                position += 2
            while position < len(data):
                name, position = _pascal(data, position)
                if position + 2 > len(data):
                    raise ValueError("brk PUBDEF is truncated")
                offset = int.from_bytes(data[position:position + 2], "little")
                position += 2
                _, position = _index(data, position)
                if name in publics:
                    raise ValueError("brk PUBDEF repeats a symbol")
                publics[name] = (segment, offset)
        elif record.name == "EXTDEF":
            position = 0
            while position < len(data):
                name, position = _pascal(data, position)
                _, position = _index(data, position)
                externals.append(name)
        elif record.name == "LEDATA":
            segment, position = _index(data, 0)
            if position + 2 > len(data):
                raise ValueError("brk LEDATA is truncated")
            offset = int.from_bytes(data[position:position + 2], "little")
            position += 2
            if segment in ledatas:
                raise ValueError("brk segment unexpectedly has split LEDATA")
            ledatas[segment] = (offset, data[position:])
            current = (segment, offset)
        elif record.name == "FIXUPP":
            if current is None:
                raise ValueError("brk FIXUPP has no preceding LEDATA")
            fixup_records.append(data)
            position = 0
            while position < len(data):
                if position + 3 > len(data):
                    raise ValueError("brk FIXUPP is truncated")
                locat, low, fixdat = data[position:position + 3]
                position += 3
                if not (locat & 0x80) or fixdat & 0x88:
                    raise ValueError("brk FIXUPP uses threaded/unsupported records")
                site = ((locat & 3) << 8) | low
                location_type = (locat >> 2) & 0x0F
                relative = not bool(locat & 0x40)
                frame_method = (fixdat >> 4) & 7
                target_method = fixdat & 3
                no_displacement = bool(fixdat & 4)
                frame_index = None
                if frame_method <= 2:
                    frame_index, position = _index(data, position)
                elif frame_method not in (4, 5, 6, 7):
                    raise ValueError("brk FIXUPP has an unsupported frame method")
                if target_method == 3:
                    raise ValueError("brk FIXUPP has an unsupported absolute target")
                target_index, position = _index(data, position)
                displacement = 0
                if not no_displacement:
                    if position + 2 > len(data):
                        raise ValueError("brk FIXUPP displacement is truncated")
                    displacement = int.from_bytes(data[position:position + 2], "little")
                    position += 2
                fixups.append({
                    "segment": current[0], "site": current[1] + site,
                    "location_type": location_type, "relative": relative,
                    "frame_method": frame_method, "frame_index": frame_index,
                    "target_method": target_method, "target_index": target_index,
                    "displacement": displacement,
                })

    if segments != {
        1: (127, "_TEXT", "CODE"),
        2: (0, "_DATA", "DATA"),
        3: (0, "_BSS", "BSS"),
    }:
        raise ValueError(f"brk OMF segment layout changed: {segments}")
    if groups != {1: ("DGROUP", [3, 2])}:
        raise ValueError(f"brk OMF DGROUP membership changed: {groups}")
    expected_publics = {
        "___brk": (1, 0), "___sbrk": (1, 38),
        "_brk": (1, 91), "_sbrk": (1, 107),
    }
    if publics != expected_publics or externals != ["_errno", "___brklvl"]:
        raise ValueError("brk OMF public/external symbol layout changed")
    if set(ledatas) != {1} or ledatas[1][0] != 0 or len(ledatas[1][1]) != 127:
        raise ValueError("brk OMF source CODE LEDATA changed")
    if (len(fixups) != 5 or [f["site"] for f in fixups] != config["fixup_offsets"] or
            any(f["segment"] != 1 or f["location_type"] != 1 or f["relative"] or
                f["displacement"] != 0 or f["target_method"] != 2 for f in fixups)):
        raise ValueError("brk OMF FIXUPP sites/widths/target types changed")
    for f in fixups:
        if f["target_index"] == 1:
            if (f["frame_method"], f["frame_index"]) != (1, 1):
                raise ValueError("brk _errno fixup no longer uses DGROUP frame")
        elif f["target_index"] == 2:
            if (f["frame_method"], f["frame_index"]) != (5, None):
                raise ValueError("brk ___brklvl fixup no longer uses target frame")
        else:
            raise ValueError("brk FIXUPP references an unknown external")

    return {
        "library_sha256": digest_bytes(library),
        "module_program_records_sha256": digest_bytes(member.program_records),
        "module_object_sha256": digest_bytes(obj),
        "code": ledatas[1][1],
        "segments": segments,
        "groups": groups,
        "publics": publics,
        "externals": externals,
        "fixups": fixups,
        "fixup_records_sha256": digest_bytes(b"".join(fixup_records)),
    }


def _target(config: dict) -> tuple[bytes, bytes]:
    artifact = find_artifact(load_target_manifest(ROOT / "config/targets.toml"), config["artifact"])
    raw = read_verified_artifact(ROOT, artifact)
    if len(raw) != config["container_size"] or artifact["sha256"] != config["target_sha256"]:
        raise ValueError("ZUN container identity changed")
    rows = [row for row in parse_launcher(raw, expected_sha256=artifact["sha256"])["payloads"]
            if row["name"] == config["member"]]
    if len(rows) != 1:
        raise ValueError("original ZUN -S child is missing or ambiguous")
    member = rows[0]
    if (member["file_start"], member["size"], member["sha256"]) != (
            config["member_start"], config["member_size"], config["member_sha256"]):
        raise ValueError("original ZUN -S child identity changed")
    child = raw[member["file_start"]:member["file_end"]]
    code = child[config["code_start_com"] - 0x100:
                 config["code_start_com"] - 0x100 + config["code_size"]]
    if len(code) != config["code_size"]:
        raise ValueError("brk target CODE slice is incomplete")
    return code, child


def _resolve_code(source: bytes, fixups: list[dict], config: dict,
                  external_names: list[str]) -> tuple[bytes, list[dict]]:
    expected = bytearray(source)
    resolved = []
    for fixup in fixups:
        site = fixup["site"]
        if site < 0 or site + 2 > len(source):
            raise ValueError("brk OMF relocation extends beyond CODE")
        if fixup["relative"] or fixup["target_method"] != 2:
            raise ValueError("brk OMF relocation is not an absolute external OFFSET16")
        if not 1 <= fixup["target_index"] <= len(external_names):
            raise ValueError("brk OMF external index is out of range")
        symbol = external_names[fixup["target_index"] - 1]
        if symbol not in config["external_targets"]:
            raise ValueError("brk OMF external target has no pinned original address")
        if symbol == "_errno":
            if (fixup["frame_method"], fixup["frame_index"]) != (1, 1):
                raise ValueError("brk _errno relocation frame is not DGROUP")
        elif symbol == "___brklvl":
            if (fixup["frame_method"], fixup["frame_index"]) != (5, None):
                raise ValueError("brk ___brklvl relocation frame is not TARGET")
        else:
            raise ValueError("brk OMF references an unexpected external")
        addend = int.from_bytes(source[site:site + 2], "little")
        value = (config["external_targets"][symbol] + addend + fixup["displacement"]) & 0xFFFF
        expected[site:site + 2] = value.to_bytes(2, "little")
        resolved.append({"site": site, "symbol": symbol,
                         "source_addend": addend, "resolved_word": value})
    return bytes(expected), resolved


def _verify_target_code(source: bytes, target: bytes, fixups: list[dict],
                        config: dict, external_names: list[str]) -> tuple[list[int], list[dict]]:
    expected, resolved = _resolve_code(source, fixups, config, external_names)
    if expected != target:
        raise ValueError("brk target CODE is not the exact OMF-relocated CT.LIB module")
    relocation_bytes = {f["site"] + delta for f in fixups for delta in range(2)}
    mismatches = [i for i, (left, right) in enumerate(zip(source, target)) if left != right]
    if set(mismatches) != relocation_bytes or len(mismatches) != 10:
        raise ValueError("brk target differs outside its exact five two-byte OMF relocations")
    return mismatches, resolved


def evidence(config: dict) -> dict:
    if (config.get("schema_version") != 1 or
            config.get("origin") != "pinned-borland-ct-library-original-object" or
            config.get("global_authored_credit") != "vendor-zero" or
            config.get("toolchain_manifest_sha256") != digest_file(ROOT / "config/toolchain.toml")):
        raise ValueError("brk source origin or Borland toolchain identity changed")
    toolchain = tomllib.loads((ROOT / "config/toolchain.toml").read_text())
    surfaces = [row for row in toolchain["surfaces"] if row["id"] == "tc40j-lib"]
    if len(surfaces) != 1:
        raise ValueError("pinned TC4J library tree surface is missing or ambiguous")
    surface = attest_surface(ROOT, surfaces[0])
    if (not surface.get("pass") or
            surface.get("actual_sha256") != config["library_tree_sha256"] or
            surface.get("file_count") != config["library_tree_file_count"]):
        raise ValueError("complete pinned Borland library tree no longer verifies")

    module = _module(config)
    target_code, child = _target(config)
    crt_config = tomllib.loads((ROOT / "config/zun_crt.toml").read_text())
    crt_claims, crt_decision_sha = reviewed_crt_claims(
        ROOT, {"size": config["container_size"], "sha256": config["target_sha256"]})
    crt_data = [row for row in crt_claims if row["kind"] == "verified-vendor-initialized-data"]
    if len(crt_data) != 1:
        raise ValueError("original C0T CRT DATA owner is missing or ambiguous")
    for symbol, address in config["external_targets"].items():
        if not crt_config["original_crt_data_start"] <= address < crt_config["original_crt_data_end"]:
            raise ValueError(f"brk external {symbol} is outside the accepted C0T DATA segment")
        file_offset = config["member_start"] + address - 0x100
        if not crt_data[0]["start"] <= file_offset < crt_data[0]["end"]:
            raise ValueError(f"brk external {symbol} does not resolve inside accepted CRT DATA")

    # Cross-check that this exact CT.LIB module supplies the two external
    # function addresses already used by the independently accepted nearheap.
    nearheap_config = tomllib.loads((ROOT / "config/zun_nearheap.toml").read_text())
    import review_zun_nearheap as nearheap
    nearheap_record = nearheap.check()
    for symbol in ("___brk", "___sbrk"):
        actual = config["code_start_com"] + module["publics"][symbol][1]
        if (actual != nearheap_config["external_targets"][symbol] or
                nearheap_record["code"]["target_sha256"] != nearheap_record["code"]["relocated_sha256"]):
            raise ValueError(f"brk public {symbol} disagrees with the nearheap external link")

    code = module["code"]
    if digest_bytes(code) != config["code_sha256"]:
        raise ValueError("brk source CODE hash changed")
    mismatches, resolved = _verify_target_code(
        code, target_code, module["fixups"], config, module["externals"])

    # Both a normal instruction and a linked external address must be rejected
    # if mutated, using the same complete relocated-byte verifier.
    relocation_bytes = {f["site"] + delta for f in module["fixups"] for delta in range(2)}
    nonrelocation = next(i for i in range(len(target_code)) if i not in relocation_bytes)
    bad_instruction = bytearray(target_code)
    bad_instruction[nonrelocation] ^= 1
    try:
        _verify_target_code(code, bytes(bad_instruction), module["fixups"], config, module["externals"])
        rejected_instruction = False
    except ValueError:
        rejected_instruction = True
    bad_relocation = bytearray(target_code)
    bad_relocation[module["fixups"][0]["site"]] ^= 1
    try:
        _verify_target_code(code, bytes(bad_relocation), module["fixups"], config, module["externals"])
        rejected_relocation = False
    except ValueError:
        rejected_relocation = True
    if not rejected_instruction or not rejected_relocation:
        raise ValueError("brk source/target negative control failed")

    file_start = config["member_start"] + config["code_start_com"] - 0x100
    if file_start != config["code_file_start"]:
        raise ValueError("brk outer-file offset changed")
    return {
        "schema_version": 1,
        "kind": "bounded-zun-borland-ctlib-brk-module-ownership-review",
        "manifest_sha256": digest_file(CONFIG),
        "toolchain_manifest_sha256": digest_file(ROOT / "config/toolchain.toml"),
        "library_tree_sha256": surface["actual_sha256"],
        "library_tree_file_count": surface["file_count"],
        "target_artifact_sha256": config["target_sha256"],
        "source_library_sha256": module["library_sha256"],
        "library_member": config["library_member"],
        "module_program_records_sha256": module["module_program_records_sha256"],
        "module_object_sha256": module["module_object_sha256"],
        "fixup_records_sha256": module["fixup_records_sha256"],
        "member_sha256": config["member_sha256"],
        "member_start": config["member_start"],
        "member_size": config["member_size"],
        "origin": config["origin"],
        "global_authored_credit": config["global_authored_credit"],
        "nearheap_acceptance_sha256": digest_file(ROOT / "config/zun_nearheap_acceptance.json"),
        "crt_acceptance_sha256": digest_file(ROOT / "config/zun_crt_acceptance.json"),
        "crt_decision_sha256": crt_decision_sha,
        "code": {
            "runtime_start": config["code_start_com"],
            "file_start": file_start,
            "size": len(code),
            "source_sha256": digest_bytes(code),
            "target_sha256": digest_bytes(target_code),
            "relocated_sha256": digest_bytes(_resolve_code(code, module["fixups"], config, module["externals"])[0]),
            "nonrelocation_bytes_exact": len(code) - len(relocation_bytes),
            "relocation_count": len(module["fixups"]),
            "relocation_field_bytes": len(relocation_bytes),
            "relocation_offsets": [f["site"] for f in module["fixups"]],
            "mismatch_offsets": mismatches,
            "resolved_relocations": resolved,
            "raw_exact": False,
            "exact_after_omf_relocation": True,
        },
        "segments": {str(index): list(row) for index, row in module["segments"].items()},
        "groups": {str(index): [name, members] for index, (name, members) in module["groups"].items()},
        "publics": {name: offset for name, (_, offset) in module["publics"].items()},
        "externals": module["externals"],
        "crt_data_owner": {"start": crt_data[0]["start"], "end": crt_data[0]["end"]},
        "negative_control": {
            "nonrelocation_instruction_flip_rejected": rejected_instruction,
            "resolved_relocation_flip_rejected": rejected_relocation,
        },
        "size": len(code),
        "code_bytes": len(code),
        "authored_credit": 0,
    }


def check() -> dict:
    config = tomllib.loads(CONFIG.read_text())
    expected = evidence(config)
    actual = json.loads(PUBLIC.read_text())
    if actual != expected:
        raise ValueError("brk acceptance is stale or its source/target proof changed")
    return expected


def reviewed_claims(root: Path, view: dict, *, verify_targets: bool = False):
    root = root.resolve()
    if root != ROOT.resolve():
        raise ValueError("brk review is bound to the live repository root")
    config = tomllib.loads(CONFIG.read_text())
    record = check()
    if (view.get("size") != config["container_size"] or
            view.get("sha256") != record["target_artifact_sha256"]):
        raise ValueError("brk ownership view identity changed")
    return [{
        "start": record["code"]["file_start"],
        "end": record["code"]["file_start"] + record["code"]["size"],
        "kind": "verified-vendor-code", "unit": "borland-brk-sbrk",
        "origin": CLAIM_ORIGIN, "source_origin": config["origin"],
        "instruction_bytes": record["code"]["size"], "authored_credit": 0,
        "library": "Borland Turbo C++ 4.0 CT.LIB", "member": config["library_member"],
    }], digest_file(PUBLIC)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write:
        config = tomllib.loads(CONFIG.read_text())
        PUBLIC.write_text(json.dumps(evidence(config), indent=2) + "\n")
    check()
    print("PASS: Borland CT.LIB brk/sbrk: 127 relocated CODE; ___brk/___sbrk/_brk/_sbrk")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
