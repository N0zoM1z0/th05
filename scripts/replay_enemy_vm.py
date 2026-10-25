#!/usr/bin/env python3
"""Replay and explicitly review the complete original-assembly enemy VM family."""
from __future__ import annotations
import argparse
import fcntl
import json
from pathlib import Path
import re
import shutil
import tomllib

from lib.omf import describe_omf, parse_omf
from lib.pc98 import digest_file, digest_bytes, parse_mz
from lib.reference_build import Builder
from lib.replay_toolchain import freeze_toolchain, static_toolchain, validate_full_toolchain
from lib.unit_context import UnitContext, load_unit_target
from lib.unit_oracle import compare_unit, map_publics, relative_fixups
from replay_text_fx_data import ASSEMBLER, index, command_records

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/enemy_vm.toml"
PUBLIC = ROOT / "config/enemy_vm_acceptance.json"
DECISION = ROOT / "config/reviewed_enemy_vm_unit.json"
LINK_RESPONSE = b"-c -s -E bindings.obj script.obj, units.exe, units.map,\r\n"
PUBLIC_OFFSETS = {"enemy_pos_update": 0, "enemy_velocity_set": 45,
                  "enemy_aim_velocity_set": 62, "enemy_bullet_template_copy": 83,
                  "enemy_script_update": 104, "_enemy_script_update": 104,
                  "script_handlers": 1133, "script_handlers_end": 1251,
                  "enemy_vm_family_end": 1252}


def snapshots(config: dict) -> list[dict]:
    paths = {str(CONFIG.relative_to(ROOT)), config["source"], config["types"], config["bindings"], config["symbols"],
             "scripts/replay_enemy_vm.py", "scripts/replay_text_fx_data.py", "scripts/lib/omf.py",
             "scripts/lib/pc98.py", "scripts/lib/reference_build.py", "scripts/lib/replay_toolchain.py",
             "scripts/lib/unit_context.py", "scripts/lib/unit_oracle.py", "scripts/lib/unit_extents.py",
             "config/targets.toml", "config/toolchain.toml", "src/main/enemy/enemy.hpp",
             "src/main/bullet/template.hpp", "src/shared/geometry.hpp", "src/shared/abi.hpp",
             "src/main/enemy/script.md"}
    return [{"path": path, "sha256": digest_file(ROOT / path)} for path in sorted(paths)]


def classification(config: dict) -> dict:
    if (config["target_start"] != 0x1538C or config["size"] != 1252 or config["cs_base"] != 0x15270
            or config["ds_base"] != 0x209D0 or config["alignment_offsets"] != [103, 1251]
            or config["inert_branch_range"] != [1100, 1102] or config["dispatch_range"] != [1133, 1251]):
        raise ValueError("enemy VM complete native classification requires renewed review")
    return {"compared_bytes": 1252, "authored_asm_instruction_bytes": 1130,
            "authored_asm_dispatch_table_bytes": 118, "checked_alignment_bytes": 2,
            "checked_inert_branch_bytes": 2, "cxx_authored_credit": 0}


def source_bytes(config: dict, negative: bool = False) -> bytes:
    source = (ROOT / config["source"]).read_bytes()
    if negative:
        before, after = (config[key].encode("ascii") for key in ("negative_find", "negative_replace"))
        if source.count(before) != 1 or before == after:
            raise ValueError("enemy VM semantic mutation anchor changed")
        source = source.replace(before, after)
    return source


def omf_scope(raw: bytes, config: dict) -> dict:
    """Only one complete ordinary CODE contribution; no initialized DATA."""
    description = describe_omf(raw)
    if description["translator_comments"] != ["Turbo Assembler  Version 5.0"]:
        raise ValueError("enemy VM requires a genuine pinned assembler producer")
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
            name, cursor = index(body, 3)
            cl, cursor = index(body, cursor)
            overlay, cursor = index(body, cursor)
            if (cursor != len(body) or not 0 < name < len(names)
                    or not 0 < cl < len(names) or not 0 <= overlay < len(names)):
                raise ValueError("invalid ASM CODE segment names")
            segments.append((names[name], names[cl], int.from_bytes(body[1:3], "little")))
    matches = [(i, seg) for i, seg in enumerate(segments) if seg and seg[0] == "ENEMY_VM_TEXT"]
    if len(matches) != 1 or matches[0][1][1:] != ("CODE", config["size"]):
        raise ValueError("expected complete reviewed enemy VM CODE SEGDEF")
    si = matches[0][0]
    if any(seg and seg[2] and i != si for i, seg in enumerate(segments)):
        raise ValueError("unreviewed initialized/reserved source contribution")
    covered, chunks = bytearray(config["size"]), []
    for record in records:
        if record.name != "LEDATA":
            continue
        owner, cursor = index(record.data, 0)
        if owner != si or cursor + 2 > len(record.data):
            raise ValueError("LEDATA outside complete enemy VM scope")
        start = int.from_bytes(record.data[cursor:cursor + 2], "little")
        payload = record.data[cursor + 2:]
        end = start + len(payload)
        if not payload or end > len(covered) or any(covered[start:end]):
            raise ValueError("ASM CODE overlap or out-of-bounds LEDATA")
        covered[start:end] = b"\1" * len(payload)
        chunks.append({"offset": start, "size": len(payload), "sha256": digest_bytes(payload)})
    if not all(covered):
        raise ValueError("incomplete enemy VM LEDATA coverage")
    return {"kind": "complete-assembler-code", "segment": "ENEMY_VM_TEXT", "size": len(covered), "ledata": chunks}



def map_scope(path: Path, config: dict) -> int:
    pattern = re.compile(r"\s*([0-9A-F]{4}):([0-9A-F]{4})\s+([0-9A-F]{4})\s+"
                         r"C=(\S+)\s+S=(\S+)\s+G=(\S+)\s+M=(\S+)", re.I)
    found = []
    for line in path.read_text(encoding="cp437").splitlines():
        m = pattern.match(line)
        if m and m[5].upper() == "ENEMY_VM_TEXT" and m[7].lower() == "script.asm":
            if (m[4].upper() != "CODE" or m[6].lower() != "main_03"
                    or int(m[1], 16) * 16 != config["cs_base"] or int(m[3], 16) != config["size"]):
                raise ValueError("complete ASM contribution has wrong frame/group/class/size")
            found.append(int(m[1], 16) * 16 + int(m[2], 16))
    if found != [config["target_start"]]:
        raise ValueError("expected one complete original-frame enemy VM contribution")
    return found[0]


def native_review(path: Path, config: dict, artifact: dict, target) -> None:
    classification(config)
    if digest_file(path) != config["native_review_sha256"]:
        raise ValueError("native enemy VM boundary review changed")
    proof = json.loads(path.read_text())
    start, end = config["target_start"], config["target_start"] + config["size"]
    if (proof["target_sha256"] != artifact["sha256"] or (proof["start"], proof["end"]) != (start, end)
            or digest_bytes(target.program_image[start:end]) != proof["sha256"]
            or (relative_fixups(target, start, end - start) != [909] or proof["ordered_fixups"] != [909])):
        raise ValueError("complete native enemy VM target/ordered fixups disagree")
    starts = set()
    for procedure in proof["procedures"]:
        cursor = procedure["start"]
        for ins in procedure["instructions"]:
            body = bytes.fromhex(ins["bytes"])
            if not body or ins["address"] != cursor or target.program_image[cursor:cursor + len(body)] != body:
                raise ValueError("native complete instruction review differs")
            starts.add(cursor)
            cursor += len(body)
        if cursor != procedure["end"]:
            raise ValueError("native procedure review is incomplete")
    table_start, table_end = (start + offset for offset in config["dispatch_range"])
    handlers = [int.from_bytes(target.program_image[i:i + 2], "little") + config["cs_base"]
                for i in range(table_start, table_end, 2)]
    if (len(handlers) != 59 or len(set(handlers)) != 57 or handlers != proof["dispatch_targets"]
            or any(h not in starts or not start + 104 <= h < table_start for h in handlers)):
        raise ValueError("native symbolic dispatcher escapes actual handler boundaries")
    if any(target.program_image[start + o] != 0x90 for o in config["alignment_offsets"]):
        raise ValueError("native alignment NOP differs")
    left, right = (start + o for o in config["inert_branch_range"])
    if target.program_image[left:right] != b"\x74\0":
        raise ValueError("native inert branch differs")


def observe(work: Path, config: dict, target, negative: bool = False) -> dict:
    source = work / "source"
    expected = {"script.asm": source_bytes(config, negative), "types.inc": (ROOT / config["types"]).read_bytes(),
                "symbols.inc": (ROOT / config["symbols"]).read_bytes(),
                "bindings.asm": (ROOT / config["bindings"]).read_bytes(),
                "link.rsp": LINK_RESPONSE, "build_dumb.bat": b""}
    for path, payload in expected.items():
        if (source / path).read_bytes() != payload:
            raise ValueError("saved actual assembler/linker inputs differ from maintained source")
    commands = json.loads((work / "commands.json").read_text())
    argv = [ASSEMBLER + ["bindings.asm", "bindings.obj"], ASSEMBLER + ["script.asm", "script.obj"],
            ["wine", str(ROOT / "_reference/ReC98/bin/msdos.exe"), "-e", "-x", "tlink", "@link.rsp"]]
    if len(commands) != len(argv):
        raise ValueError("missing actual successful producer argv")
    for record, command in zip(commands, argv):
        if (record["command"] != command or record["returncode"] != 0
                or digest_file(work / record["log"]) != record["log_sha256"]):
            raise ValueError("actual producer command/log identity disagrees")
    raw = (source / "script.obj").read_bytes()
    scope, omf = omf_scope(raw, config), describe_omf(raw)
    binder = describe_omf((source / "bindings.obj").read_bytes())
    if (binder["translator_comments"] != ["Turbo Assembler  Version 5.0"]
            or any(binder["record_counts"].get(kind, 0) for kind in ("LEDATA", "LIDATA", "COMDAT"))):
        raise ValueError("symbol-only binder is invalid or contains initialized payload")
    candidate = parse_mz((source / "units.exe").read_bytes())
    start = map_scope(source / "units.map", config)
    comparison = compare_unit(target, candidate, config["target_start"], start, config["size"])
    publics = map_publics(source / "units.map")
    for symbol, offset in PUBLIC_OFFSETS.items():
        if {address for address, label in publics if label.lower() == symbol} != {start + offset}:
            raise ValueError("actual helper/alias/table public boundaries disagree")
    return {"comparison": comparison, "omf_scope": scope, "classification": classification(config),
            "object_sha256": omf["sha256"], "object_normalized_sha256": omf["dependency_timestamp_normalized_sha256"],
            "bindings_sha256": binder["sha256"], "bindings_normalized_sha256": binder["dependency_timestamp_normalized_sha256"],
            "map_sha256": digest_file(source / "units.map"), "mz_sha256": digest_file(source / "units.exe"),
            "commands_sha256": digest_file(work / "commands.json")}


def cold_round(work: Path, config: dict, target, negative: bool = False) -> dict:
    source = work / "source"
    source.mkdir(parents=True)
    (source / "script.asm").write_bytes(source_bytes(config, negative))
    for key, alias in (("types", "types.inc"), ("symbols", "symbols.inc"), ("bindings", "bindings.asm")):
        shutil.copyfile(ROOT / config[key], source / alias)
    (source / "build_dumb.bat").touch()
    builder = Builder(source, ROOT / ".analysis/toolchain/wineprefix", ROOT / "_reference/ReC98/bin/msdos.exe")
    builder.execute("bindings", ASSEMBLER + ["bindings.asm", "bindings.obj"])
    builder.execute("assemble", ASSEMBLER + ["script.asm", "script.obj"])
    (source / "link.rsp").write_bytes(LINK_RESPONSE)
    builder.execute("link", ["wine", str(builder.msdos), "-e", "-x", "tlink", "@link.rsp"])
    (work / "commands.json").write_text(json.dumps(command_records(builder), indent=2) + "\n")
    return observe(work, config, target, negative)


def check_public(record: dict, config: dict) -> None:
    if (record["inputs"] != snapshots(config) or record["classification"] != classification(config)
            or record["origin"] != "reviewed-native-handwritten-assembly-reconstruction"
            or record["historical_source_recovered"] is not False or record["complete_executable_exact"] is not False):
        raise ValueError("enemy VM source/classification or bounded origin policy changed")
    artifact = next(a for a in tomllib.loads((ROOT / "config/targets.toml").read_text())["artifacts"] if a["id"] == "th05-main")
    if record["target_sha256"] != artifact["sha256"]:
        raise ValueError("enemy VM target identity changed")
    rounds = record["rounds"]
    if len(rounds) != 2:
        raise ValueError("two independent fresh ASM producers required")
    for key in ("object_normalized_sha256", "bindings_normalized_sha256", "map_sha256", "mz_sha256"):
        if rounds[0][key] != rounds[1][key]:
            raise ValueError("enemy VM producers are not deterministic")
    for positive in rounds:
        c = positive["comparison"]
        if (c["size"] != 1252 or c["target_start"] != config["target_start"] or c["candidate_start"] != c["target_start"]
                or any(c[key] is not True for key in ("raw_exact", "fixups_exact", "exact"))
                or c["target_fixups"] != [909] or c["candidate_fixups"] != [909]
                or c["target_sha256"] != c["candidate_sha256"] or positive["classification"] != classification(config)):
            raise ValueError("incomplete whole-family raw/ordered-relocation proof")
    n = record["negative_control"]["comparison"]
    if (n["raw_exact"] is not False or n["exact"] is not False or n["size"] != 1252
            or n["fixups_exact"] is not True or n["target_fixups"] != [909] or n["candidate_fixups"] != [909]):
        raise ValueError("own semantic interval negative was not rejected")


def accept(path: Path, config: dict) -> None:
    record = json.loads(path.read_text())
    check_public(record, config)
    work = path.parent
    for entry in record["inputs"]:
        if digest_file(work / "inputs" / entry["path"]) != entry["sha256"]:
            raise ValueError("frozen enemy VM source/verifier snapshot changed")
    context = UnitContext(ROOT, "main")
    artifact, target, _ = load_unit_target(context, context.config())
    native_review(work / "native-review.json", config, artifact, target)
    tool_path, reuse_path = work / "toolchain-attestation.json", work / "toolchain-reuse-proof.json"
    manifest, surfaces = static_toolchain(ROOT)
    validate_full_toolchain(json.loads(tool_path.read_text()), manifest, surfaces)
    reuse = json.loads(reuse_path.read_text())
    if (digest_file(tool_path) != record["toolchain_receipt_sha256"]
            or digest_file(reuse_path) != record["toolchain_reuse_proof_sha256"]
            or reuse["manifest_sha256"] != manifest or reuse["reused"] != record["toolchain_reused"]
            or reuse["original_full_receipt_sha256"] != record["toolchain_receipt_sha256"]):
        raise ValueError("frozen executable toolchain/reuse proof changed")
    for i, label in enumerate(("a", "b")):
        if observe(work / label, config, target) != record["rounds"][i]:
            raise ValueError("saved complete positive enemy VM producer disagrees")
    if observe(work / "negative", config, target, True) != record["negative_control"]:
        raise ValueError("saved own semantic negative producer disagrees")
    PUBLIC.write_text(json.dumps({**record, "replay_receipt_sha256": digest_file(path)}, indent=2) + "\n")


def reviewed_claims(root: Path, views: dict, *, verify_targets: bool = False) -> tuple[dict, str | None]:
    path = root / DECISION.relative_to(ROOT)
    if not path.exists():
        return {}, None
    config = tomllib.loads(CONFIG.read_text())
    decision, record = json.loads(path.read_text()), json.loads(PUBLIC.read_text())
    check_public(record, config)
    if (decision != {"schema_version": 1, "classification": record["origin"], "unit": "main-enemy-vm-family",
                     "acceptance_sha256": digest_file(PUBLIC), "authored_instruction_bytes": 1130,
                     "authored_dispatch_table_bytes": 118, "checked_uncredited_bytes": 4,
                     "historical_source_recovered": False, "cxx_authored_credit": 0}):
        raise ValueError("missing, broadened or stale explicit enemy VM ownership decision")
    if verify_targets:
        c = UnitContext(root, "main")
        _, target, _ = load_unit_target(c, c.config())
        start = config["target_start"]
        if digest_bytes(target.program_image[start:start + config["size"]]) != record["rounds"][0]["comparison"]["target_sha256"]:
            raise ValueError("reviewed enemy VM complete native bytes differ")
    start = config["target_start"]
    ranges = [(0, 103, "accepted-reviewed-asm-instructions"), (103, 104, "checked-uncredited-asm-alignment"),
              (104, 1100, "accepted-reviewed-asm-instructions"), (1100, 1102, "checked-uncredited-asm-inert-branch"),
              (1102, 1133, "accepted-reviewed-asm-instructions"), (1133, 1251, "accepted-reviewed-asm-dispatch-table"),
              (1251, 1252, "checked-uncredited-asm-alignment")]
    return {"main": [{"start": start + left, "end": start + right, "kind": kind,
                       "unit": "main-enemy-vm-family", "origin": record["origin"]} for left, right, kind in ranges]}, digest_file(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--output", type=Path)
    mode.add_argument("--accept", type=Path)
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--native-review", type=Path)
    args = parser.parse_args()
    config = tomllib.loads(CONFIG.read_text())
    if args.check:
        check_public(json.loads(PUBLIC.read_text()), config)
        print("PASS: enemy VM 1252 compared bytes; 1130 ASM instruction + 118 dispatch + 4 uncredited bytes")
        return 0
    if args.accept:
        accept(args.accept.resolve(), config)
        print("PASS: complete enemy VM sources/producers/native boundaries revalidated; adoption remains explicit")
        return 0
    if args.native_review is None:
        parser.error("--output requires --native-review")
    work = args.output.resolve()
    if work.exists():
        parser.error("replay requires a fresh output directory")
    c = UnitContext(ROOT, "main")
    artifact, target, _ = load_unit_target(c, c.config())
    native_review(args.native_review, config, artifact, target)
    work.mkdir(parents=True)
    frozen = snapshots(config)
    for entry in frozen:
        destination = work / "inputs" / entry["path"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / entry["path"], destination)
    shutil.copyfile(args.native_review, work / "native-review.json")
    with (ROOT / ".analysis/borland.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        tool = freeze_toolchain(ROOT, work / "toolchain-attestation.json")
        rounds = []
        for label in ("a", "b"):
            observed = cold_round(work / label, config, target)
            rounds.append(observed)
            if not observed["comparison"]["exact"]:
                raise ValueError("complete family mismatch; stopped before further builds")
        negative = cold_round(work / "negative", config, target, True)
    record = {"schema_version": 1, "kind": "complete-native-assembly-enemy-vm-replay", "inputs": frozen,
              "origin": "reviewed-native-handwritten-assembly-reconstruction", "classification": classification(config),
              "target_sha256": artifact["sha256"], "historical_source_recovered": False,
              "complete_executable_exact": False, "rounds": rounds, "negative_control": negative,
              "toolchain_reused": tool["reused"], "toolchain_receipt_sha256": digest_file(work / "toolchain-attestation.json"),
              "toolchain_reuse_proof_sha256": tool["proof_sha256"]}
    check_public(record, config)
    (work / "receipt.json").write_text(json.dumps(record, indent=2) + "\n")
    print(f"PASS: two fresh complete enemy VM producers and own semantic negative: {work / 'receipt.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
