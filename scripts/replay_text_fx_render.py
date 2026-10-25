#!/usr/bin/env python3
"""Cold replay the original-style self-modifying renderer as separate ASM CODE."""
from __future__ import annotations

import argparse
import fcntl
import json
from pathlib import Path
import re
import shutil
import tomllib

import replay_text_fx_data as data
from lib.omf import describe_omf, parse_omf
from lib.pc98 import digest_bytes, digest_file, parse_mz
from lib.reference_build import Builder
from lib.replay_toolchain import freeze_toolchain, static_toolchain, validate_full_toolchain
from lib.unit_context import UnitContext, freeze_target_view, validate_public_target_view
from lib.unit_oracle import compare_unit, map_publics

ROOT = data.ROOT
CONFIG = ROOT / "config/text_fx_render.toml"
PUBLIC = ROOT / "config/text_fx_render_acceptance.json"
LINK_RESPONSE = b"-c -s -E bindings.obj tfxcode.obj, units.exe, units.map,\r\n"
PUBLIC_OFFSETS = {
    "graph_putsa_fx": 0, "glyph_weight_heavy": 300, "glyph_weight_normal": 306,
    "glyph_weight_black": 307, "glyph_weight_bold": 313, "glyph_bold_and_mask": 330,
    "grppsafx_glyph_func_1": 191, "grppsafx_glyph_func_2": 273,
    "grppsafx_glyph_spacing_1": 222, "grppsafx_glyph_spacing_2": 293,
    "grppsafx_glyph_mask": 343,
}


def classification(config: dict, payload: bytes | None = None) -> dict:
    if (config["size"] != 346 or config["alignment_offsets"] != [299]
            or config["runtime_patch_placeholder_ranges"] != [[222, 224], [293, 295], [343, 345]]
            or config["instruction_nops"] != [173, 261]):
        raise ValueError("complete native CODE classification needs renewed review")
    if payload is not None:
        if len(payload) != 346 or any(payload[o] != 0x90 for o in (173, 261, 299)):
            raise ValueError("native NOP bytes or complete CODE boundary changed")
        if any(payload[start:end] != b"\x34\x12" for start, end in config["runtime_patch_placeholder_ranges"]):
            raise ValueError("native runtime-patched dummy operands changed")
    return {"compared_code_bytes": 346, "semantic_asm_instruction_bytes": 339,
            "checked_alignment_bytes": 1, "checked_runtime_patch_placeholder_bytes": 6,
            "cxx_authored_credit": 0, "global_authored_credit": "unreviewed"}


def snapshots(config: dict, data_config: dict) -> list[dict]:
    paths = {entry["path"] for entry in data.inputs(data_config)}
    paths.update((str(CONFIG.relative_to(ROOT)), "scripts/replay_text_fx_render.py", config["source"],
                  str(data.PUBLIC.relative_to(ROOT))))
    for profile in config["profiles"].values():
        paths.update((profile["bindings"], profile["symbols"]))
    return [{"path": path, "sha256": digest_file(ROOT / path)} for path in sorted(paths)]


def source_bytes(config: dict, negative: bool) -> bytes:
    source = (ROOT / config["source"]).read_bytes()
    if negative:
        before, after = (config[k].encode("ascii") for k in ("negative_find", "negative_replace"))
        if source.count(before) != config["negative_occurrences"] or not before or before == after:
            raise ValueError("renderer semantic loop-height mutation anchor changed")
        source = source.replace(before, after)
    return source


def omf_scope(raw: bytes, config: dict) -> dict:
    """Only one complete ordinary CODE contribution; no initialized DATA."""
    description = describe_omf(raw)
    if description["translator_comments"] != ["Turbo Assembler  Version 5.0"]:
        raise ValueError("renderer requires a genuine pinned assembler producer")
    names, segments = [""], [None]
    records = parse_omf(raw)
    for record in records:
        if record.name in {"LIDATA", "LIDATA32", "COMDAT", "COMDAT32", "BAKPAT", "BAKPAT32",
                           "LEDATA32", "SEGDEF32", "FIXUPP32"}:
            raise ValueError("unsupported ASM CODE producer transform")
        body = record.data
        if record.name == "LNAMES":
            cursor = 0
            while cursor < len(body):
                length = body[cursor]
                cursor += 1
                if cursor + length > len(body):
                    raise ValueError("truncated ASM CODE names")
                names.append(body[cursor:cursor + length].decode("cp437"))
                cursor += length
        elif record.name == "SEGDEF":
            if len(body) < 6 or not body[0] & 0xE0 or body[0] & 2:
                raise ValueError("unsupported ASM CODE SEGDEF")
            name, cursor = data.index(body, 3)
            cl, cursor = data.index(body, cursor)
            overlay, cursor = data.index(body, cursor)
            if (cursor != len(body) or not 0 < name < len(names)
                    or not 0 < cl < len(names) or not 0 <= overlay < len(names)):
                raise ValueError("invalid ASM CODE segment names")
            segments.append((names[name], names[cl], int.from_bytes(body[1:3], "little")))
    matches = [(i, seg) for i, seg in enumerate(segments) if seg and seg[0] == "SHARED"]
    if len(matches) != 1 or matches[0][1][1:] != ("CODE", config["size"]):
        raise ValueError("expected complete reviewed SHARED CODE SEGDEF")
    si = matches[0][0]
    if any(seg and seg[2] and i != si for i, seg in enumerate(segments)):
        raise ValueError("unreviewed initialized/reserved source contribution")
    covered, chunks = bytearray(config["size"]), []
    for record in records:
        if record.name != "LEDATA":
            continue
        owner, cursor = data.index(record.data, 0)
        if owner != si or cursor + 2 > len(record.data):
            raise ValueError("LEDATA outside complete renderer scope")
        start = int.from_bytes(record.data[cursor:cursor + 2], "little")
        payload = record.data[cursor + 2:]
        end = start + len(payload)
        if not payload or end > len(covered) or any(covered[start:end]):
            raise ValueError("ASM CODE overlap or out-of-bounds LEDATA")
        covered[start:end] = b"\1" * len(payload)
        chunks.append({"offset": start, "size": len(payload), "sha256": digest_bytes(payload)})
    if not all(covered):
        raise ValueError("incomplete renderer LEDATA coverage")
    return {"kind": "complete-assembler-code", "segment": "SHARED", "size": len(covered), "ledata": chunks}


def map_scope(path: Path, profile: dict, config: dict) -> int:
    pattern = re.compile(r"\s*([0-9A-F]{4}):([0-9A-F]{4})\s+([0-9A-F]{4})\s+"
                         r"C=(\S+)\s+S=(\S+)\s+G=(\S+)\s+M=(\S+)", re.I)
    found = []
    for line in path.read_text(encoding="cp437").splitlines():
        m = pattern.match(line)
        if m and m[5].upper() == "SHARED" and m[7].lower() == "tfxcode.asm":
            if (m[4].upper() != "CODE" or m[6].lower() != "(none)"
                    or int(m[1], 16) * 16 != profile["cs_base"] or int(m[3], 16) != config["size"]):
                raise ValueError("actual complete CODE class/frame/group/size disagrees")
            found.append(int(m[1], 16) * 16 + int(m[2], 16))
    if found != [profile["code_start"]]:
        raise ValueError("actual complete renderer MAP boundary disagrees")
    return found[0]


def observe(work: Path, config: dict, data_config: dict, name: str, target, negative: bool = False) -> dict:
    source, bindings = work / "source", config["profiles"][name]
    expected = {"tfxcode.asm": source_bytes(config, negative), "build_dumb.bat": b"",
                "bindings.asm": (ROOT / bindings["bindings"]).read_bytes(),
                "symbols.inc": (ROOT / bindings["symbols"]).read_bytes(), "link.rsp": LINK_RESPONSE}
    for path, payload in expected.items():
        if (source / path).read_bytes() != payload:
            raise ValueError("saved assembler/linker inputs disagree with maintained source")
    commands = json.loads((work / "commands.json").read_text())
    expected_argv = [data.ASSEMBLER + ["bindings.asm", "bindings.obj"],
                     data.ASSEMBLER + ["tfxcode.asm", "tfxcode.obj"],
                     ["wine", str(ROOT / "_reference/ReC98/bin/msdos.exe"), "-e", "-x", "tlink", "@link.rsp"]]
    if len(commands) != len(expected_argv):
        raise ValueError("missing actual producer commands")
    for record, command in zip(commands, expected_argv):
        if (record["command"] != command or record["returncode"] != 0
                or record["log_sha256"] != digest_file(work / record["log"])):
            raise ValueError("actual successful argv/log identity changed")
    obj_raw = (source / "tfxcode.obj").read_bytes()
    scope, obj = omf_scope(obj_raw, config), describe_omf(obj_raw)
    binder = describe_omf((source / "bindings.obj").read_bytes())
    if binder["translator_comments"] != ["Turbo Assembler  Version 5.0"]:
        raise ValueError("invalid pinned binding object producer")
    candidate = parse_mz((source / "units.exe").read_bytes())
    profile = data_config["profiles"][name]
    start = map_scope(source / "units.map", profile, config)
    comparison = compare_unit(target, candidate, profile["code_start"], start, config["size"])
    publics = map_publics(source / "units.map")
    offsets = {**PUBLIC_OFFSETS,
               "_graph_putsa_fx_func": profile["state_start"] - start,
               "_graph_putsa_fx_spacing": profile["state_start"] + 2 - start}
    for symbol, offset in offsets.items():
        if {value for value, label in publics if label.lower() == symbol} != {start + offset}:
            raise ValueError("real assembler public/operand/state boundary disagrees")
    # Classify without masking any bytes, including both delay NOPs and all placeholders.
    credit = classification(config, candidate.program_image[start:start + config["size"]])
    return {"comparison": comparison, "omf_scope": scope, "classification": credit,
            "object_sha256": obj["sha256"], "object_normalized_sha256": obj["dependency_timestamp_normalized_sha256"],
            "bindings_sha256": binder["sha256"], "bindings_normalized_sha256": binder["dependency_timestamp_normalized_sha256"],
            "map_sha256": digest_file(source / "units.map"), "mz_sha256": digest_file(source / "units.exe"),
            "commands_sha256": digest_file(work / "commands.json")}


def cold_round(work: Path, config: dict, data_config: dict, name: str, target, negative: bool = False) -> dict:
    source = work / "source"
    source.mkdir(parents=True)
    (source / "tfxcode.asm").write_bytes(source_bytes(config, negative))
    for label in ("symbols", "bindings"):
        shutil.copyfile(ROOT / config["profiles"][name][label], source / ("symbols.inc" if label == "symbols" else "bindings.asm"))
    (source / "build_dumb.bat").touch()
    builder = Builder(source, ROOT / ".analysis/toolchain/wineprefix", ROOT / "_reference/ReC98/bin/msdos.exe")
    builder.execute("bindings", data.ASSEMBLER + ["bindings.asm", "bindings.obj"])
    builder.execute("assemble", data.ASSEMBLER + ["tfxcode.asm", "tfxcode.obj"])
    (source / "link.rsp").write_bytes(LINK_RESPONSE)
    builder.execute("link", ["wine", str(builder.msdos), "-e", "-x", "tlink", "@link.rsp"])
    (work / "commands.json").write_text(json.dumps(data.command_records(builder), indent=2) + "\n")
    return observe(work, config, data_config, name, target, negative)


def check_public(record: dict, config: dict, data_config: dict) -> None:
    data.check_public(json.loads(data.PUBLIC.read_text()), data_config)
    if (config["origin"] != data.ORIGIN or config["global_authored_credit"] != "unreviewed"
            or record["origin"] != data.ORIGIN or record["global_authored_credit"] != "unreviewed"
            or record["inputs"] != snapshots(config, data_config)
            or record["classification_per_artifact"] != classification(config)
            or record["complete_executable_exact"] is not False or set(record["profiles"]) != {"op", "maine"}):
        raise ValueError("ASM source, inputs, classification or separate ownership policy changed")
    for name, profile in record["profiles"].items():
        context = UnitContext(ROOT, name)
        validate_public_target_view(context, context.config(), profile["target_view"], profile["target_sha256"])
        rounds = profile["rounds"]
        if len(rounds) != 2:
            raise ValueError("two independent fresh CODE producers required")
        for field in ("object_normalized_sha256", "bindings_normalized_sha256", "map_sha256", "mz_sha256"):
            if rounds[0][field] != rounds[1][field]:
                raise ValueError("renderer ASM producers are not deterministic")
        for positive in rounds:
            c = positive["comparison"]
            if (c["size"] != config["size"] or c["target_start"] != data_config["profiles"][name]["code_start"]
                    or c["candidate_start"] != c["target_start"] or any(c[k] is not True for k in ("raw_exact", "fixups_exact", "exact"))
                    or c["target_fixups"] != [] or c["candidate_fixups"] != []
                    or c["candidate_sha256"] != c["target_sha256"] or positive["classification"] != classification(config)):
                raise ValueError("incomplete raw/ordered-fixup CODE proof")
        negative = profile["negative_control"]["comparison"]
        if (negative["raw_exact"] is not False or negative["exact"] is not False
                or negative["fixups_exact"] is not True or negative["target_fixups"] != []
                or negative["candidate_fixups"] != [] or negative["size"] != config["size"]):
            raise ValueError("own semantic glyph-loop negative was not rejected")


def accept(path: Path, config: dict, data_config: dict) -> None:
    record = json.loads(path.read_text())
    check_public(record, config, data_config)
    work = path.parent
    for entry in record["inputs"]:
        if digest_file(work / "inputs" / entry["path"]) != entry["sha256"]:
            raise ValueError("frozen source/verifier snapshot changed")
    targets = data.targets_for(data_config, work)
    data.native_review(work / "native-review.json", data_config, targets)
    tool_path, reuse_path = work / "toolchain-attestation.json", work / "toolchain-reuse-proof.json"
    tool, reuse = json.loads(tool_path.read_text()), json.loads(reuse_path.read_text())
    manifest, surfaces = static_toolchain(ROOT)
    validate_full_toolchain(tool, manifest, surfaces)
    if (digest_file(tool_path) != record["toolchain_receipt_sha256"]
            or digest_file(reuse_path) != record["toolchain_reuse_proof_sha256"]
            or reuse["original_full_receipt_sha256"] != record["toolchain_receipt_sha256"]
            or reuse["manifest_sha256"] != manifest or reuse["reused"] != record["toolchain_reused"]):
        raise ValueError("frozen executable toolchain/reuse proof changed")
    for name, profile in record["profiles"].items():
        artifact, target, proof = targets[name]
        if artifact["sha256"] != profile["target_sha256"] or proof != profile["target_view"]:
            raise ValueError("saved target proof differs from pinned identity")
        for i, label in enumerate(("a", "b")):
            if observe(work / name / label, config, data_config, name, target) != profile["rounds"][i]:
                raise ValueError("saved positive complete producer disagrees")
        if observe(work / name / "negative", config, data_config, name, target, True) != profile["negative_control"]:
            raise ValueError("saved own semantic negative producer disagrees")
    PUBLIC.write_text(json.dumps({**record, "replay_receipt_sha256": digest_file(path)}, indent=2) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--output", type=Path)
    group.add_argument("--accept", type=Path)
    group.add_argument("--check", action="store_true")
    parser.add_argument("--native-review", type=Path)
    args = parser.parse_args()
    config, data_config = tomllib.loads(CONFIG.read_text()), tomllib.loads(data.CONFIG.read_text())
    if args.check:
        check_public(json.loads(PUBLIC.read_text()), config, data_config)
        print("PASS: 692 compared ASM CODE bytes; 678 semantic, 12 placeholders, 2 alignment; separate origin")
        return 0
    if args.accept:
        accept(args.accept.resolve(), config, data_config)
        print("PASS: both complete renderer producers revalidated; no C/C++ or global credit")
        return 0
    if args.native_review is None:
        parser.error("--output needs --native-review")
    work = args.output.resolve()
    if work.exists():
        parser.error("replay needs a fresh output directory")
    classification(config)
    data.check_public(json.loads(data.PUBLIC.read_text()), data_config)
    targets = data.targets_for(data_config)
    data.native_review(args.native_review, data_config, targets)
    work.mkdir(parents=True)
    snapshot = snapshots(config, data_config)
    for entry in snapshot:
        destination = work / "inputs" / entry["path"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / entry["path"], destination)
    shutil.copyfile(args.native_review, work / "native-review.json")
    profiles = {}
    with (ROOT / ".analysis/borland.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        tool = freeze_toolchain(ROOT, work / "toolchain-attestation.json")
        for name, (artifact, target, proof) in targets.items():
            classification(config, target.program_image[data_config["profiles"][name]["code_start"]:data_config["profiles"][name]["code_end"]])
            (work / name).mkdir()
            freeze_target_view(UnitContext(ROOT, name), work / name / "target-view")
            rounds = []
            for label in ("a", "b"):
                observed = cold_round(work / name / label, config, data_config, name, target)
                rounds.append(observed)
                if not observed["comparison"]["exact"]:
                    raise ValueError("first complete raw/fixup mismatch; stopped before further builds")
            negative = cold_round(work / name / "negative", config, data_config, name, target, True)
            profiles[name] = {"target_sha256": artifact["sha256"], "target_view": proof,
                              "rounds": rounds, "negative_control": negative}
    record = {"schema_version": 1, "kind": "bounded-self-modifying-asm-code-replay", "inputs": snapshot,
              "origin": data.ORIGIN, "global_authored_credit": "unreviewed",
              "classification_per_artifact": classification(config), "profiles": profiles,
              "complete_executable_exact": False, "toolchain_reused": tool["reused"],
              "toolchain_receipt_sha256": digest_file(work / "toolchain-attestation.json"),
              "toolchain_reuse_proof_sha256": tool["proof_sha256"]}
    check_public(record, config, data_config)
    (work / "receipt.json").write_text(json.dumps(record, indent=2) + "\n")
    print(f"PASS: two fresh complete renderer producers/artifact and own negative: {work / 'receipt.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
