#!/usr/bin/env python3
"""Review one registered embedded font resource; never grant source credit."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct

from lib.launcher import parse_launcher
from lib.targets import load_target_manifest, find_artifact, read_verified_artifact

ROOT = Path(__file__).resolve().parents[1]
PROOF = "config/font_resource.json"
DECISION = "config/reviewed_font_resource.json"
MODEL = "th05-zun-cg-256-glyphs-16x16-1bpp"
GEOMETRY = {"width": 256, "height": 256, "bits_per_pixel": 1,
            "glyph_width": 16, "glyph_height": 16, "glyph_count": 256,
            "columns": 16, "row_bytes": 2, "size": 8192}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def integer(value):
    return type(value) is int and value >= 0


def file_identity(root, row):
    path = Path(row["path"])
    need(not path.is_absolute() and ".." not in path.parts,
         "resource input must use a repository-relative path")
    need(integer(row["size"]) and isinstance(row["sha256"], str) and
         re.fullmatch(r"[0-9a-f]{64}", row["sha256"]), "invalid resource input identity")
    return root / path


def read_input(root, row):
    raw = file_identity(root, row).read_bytes()
    need((len(raw), sha(raw)) == (row["size"], row["sha256"]), "resource input identity changed")
    return raw


def validate_metadata(meta, view, target, *, root=ROOT):
    need(meta.get("schema_version") == 1 and meta.get("kind") == "native-font-resource-proposal",
         "unsupported resource proof")
    need(meta.get("id") == "zun-cg-font" and meta.get("model") == MODEL and
         meta.get("artifact") == "th05-zun", "unregistered resource model or artifact")
    need(meta.get("authored_credit") == 0 and type(meta["authored_credit"]) is int and
         meta.get("authored_denominator") is None and meta.get("compiler_invocations") == 0 and
         meta.get("decision") == "PROPOSAL", "a resource proof cannot grant authored credit")
    need(view["kind"] == "com-file" and target["format"] == "com" and
         (meta.get("target_size"), meta.get("target_sha256")) ==
         (view["size"], view["sha256"]) == (target["size"], target["sha256"]),
         "resource proof has stale target/container coordinates")
    need(meta.get("geometry") == GEOMETRY and
         all(type(value) is int for value in meta["geometry"].values()),
         "unregistered bitmap geometry")
    for name in ("member_start", "member_end", "reader_end", "bitmap_start", "bitmap_end"):
        need(integer(meta.get(name)), "invalid resource boundary")
    need(0 <= meta["member_start"] < meta["reader_end"] < meta["bitmap_start"] <
         meta["bitmap_end"] == meta["member_end"] <= view["size"], "invalid complete resource bounds")
    need(meta["reader_end"] - meta["member_start"] == 75 and
         meta["bitmap_end"] - meta["bitmap_start"] == GEOMETRY["size"],
         "wrong reader or complete bitmap extent")
    need(meta.get("member") == "-G" and meta.get("required_entry_df") == 0 and
         type(meta["required_entry_df"]) is int and meta.get("instruction_nops") == [] and
         meta.get("ordered_fixups") == [], "unsupported native reader contract")
    for name in ("member_sha256", "reader_sha256", "bitmap_sha256"):
        need(isinstance(meta.get(name), str) and re.fullmatch(r"[0-9a-f]{64}", meta[name]),
             "invalid resource scope digest")
    for name in ("reference_bitmap", "independent_review", "launcher_parser", "verifier"):
        file_identity(root, meta[name])
    # The current verifier and parser must be the versions that were reviewed.
    need(meta["verifier"]["path"] == "scripts/review_font_resource.py" and
         meta["launcher_parser"]["path"] == "scripts/lib/launcher.py", "wrong resource verifier paths")
    read_input(root, meta["verifier"])
    read_input(root, meta["launcher_parser"])


def bitmap_tiles(raw):
    """Read a strict bottom-up 1bpp BMP as 256 row-major 16x16 glyphs."""
    need(len(raw) >= 62 and raw[:2] == b"BM", "not an admitted BMP")
    size, reserved, pixels = struct.unpack_from("<III", raw, 2)
    header, width, height, planes, bpp, compression, image_size = struct.unpack_from("<IiiHHII", raw, 14)
    need(size == len(raw) and reserved == 0 and pixels == 62 and header == 40 and
         (width, height, planes, bpp, compression) == (256, 256, 1, 1, 0) and
         image_size in (0, 8192) and len(raw) == pixels + 8192,
         "unsupported complete bitmap layout")
    result = bytearray()
    for glyph in range(256):
        for row in range(16):
            offset = pixels + (255 - ((glyph // 16) * 16 + row)) * 32 + (glyph % 16) * 2
            result.extend(raw[offset:offset + 2])
    need(len(result) == GEOMETRY["size"], "incomplete glyph model")
    return bytes(result)


def validate_reader(raw, font_offset, child_size):
    """Check native control/loop/read bounds, without executing the target."""
    import capstone
    from capstone import Cs, CS_ARCH_X86, CS_MODE_16
    from capstone.x86 import X86_OP_REG, X86_OP_IMM
    need(capstone.__version__ == "5.0.6", "use requirements-analysis.txt's pinned decoder")
    decoder = Cs(CS_ARCH_X86, CS_MODE_16)
    decoder.detail = True
    instructions = list(decoder.disasm(raw, 0x100))
    need(len(raw) == 75 and sum(i.size for i in instructions) == len(raw),
         "incomplete native font reader")
    by_offset = {i.address - 0x100: i for i in instructions}

    def role(offset, mnemonic, operands):
        ins = by_offset.get(offset)
        need(ins is not None and ins.mnemonic == mnemonic, "native reader role changed")
        actual = []
        for op in ins.operands:
            if op.type == X86_OP_REG:
                actual.append(("reg", ins.reg_name(op.reg)))
            elif op.type == X86_OP_IMM:
                actual.append(("imm", op.imm))
            else:
                actual.append(("memory", None))
        need(actual == operands, "native reader operand/loop bound changed")

    # These are role/bound checks, not reconstructed game instructions or credit.
    role(7, "mov", [("reg", "si"), ("imm", 0x100 + font_offset)])
    role(14, "xor", [("reg", "dx"), ("reg", "dx")])
    role(16, "mov", [("reg", "ax"), ("reg", "dx")])
    role(18, "add", [("reg", "ax"), ("imm", 0x5680)])
    role(21, "and", [("reg", "al"), ("imm", 0x7F)])
    role(25, "mov", [("reg", "al"), ("reg", "ah")])
    role(29, "mov", [("reg", "cx"), ("imm", 16)])
    role(32, "xor", [("reg", "bl"), ("reg", "bl")])
    role(34, "mov", [("reg", "al"), ("reg", "bl")])
    role(36, "or", [("reg", "al"), ("imm", 0x20)])
    role(43, "mov", [("reg", "al"), ("reg", "bl")])
    role(47, "mov", [("reg", "al"), ("reg", "ah")])
    role(51, "inc", [("reg", "bl")])
    role(53, "loop", [("imm", 0x122)])
    role(55, "inc", [("reg", "dl")])
    role(57, "jne", [("imm", 0x110)])
    role(10, "mov", [("reg", "al"), ("imm", 0x0B)])
    role(59, "mov", [("reg", "al"), ("imm", 0x0A)])
    role(70, "mov", [("reg", "ax"), ("imm", 0x4C00)])
    role(73, "int", [("imm", 0x21)])
    need([i.address - 0x100 for i in instructions if i.mnemonic == "lodsw"] == [40],
         "font reader must load one word per row")
    need([(i.mnemonic, i.address - 0x100) for i in instructions if i.mnemonic.startswith("loop") or
          i.group(capstone.CS_GRP_JUMP) or i.group(capstone.CS_GRP_CALL) or
          i.group(capstone.CS_GRP_RET)] == [("loop", 53), ("jne", 57)],
         "unreviewed font-reader control flow")
    output = [i for i in instructions if i.mnemonic == "out"]
    need(all(len(i.operands) == 2 and i.operands[0].type == X86_OP_IMM and
             i.operands[1].type == X86_OP_REG and i.reg_name(i.operands[1].reg) == "al"
             for i in output), "unreviewed CG-RAM output source")
    ports = [i.operands[0].imm for i in output]
    need(ports == [0x68, 0xA1, 0xA3, 0xA5, 0xA9, 0xA5, 0xA9, 0x68],
         "CG-RAM port sequence changed")
    need(not any(i.mnemonic in ("nop", "std", "call", "ret", "retf", "jmp") for i in instructions),
         "unreviewed font-reader operation")
    need(font_offset + 256 * 16 * 2 == child_size and child_size + 0x100 < 0x10000,
         "font reads do not reach the exact child end without wrapping")
    return {"instruction_bytes": 75, "bitmap_words_read": 4096,
            "bitmap_bytes_read": 8192, "required_entry_df": 0}


def validate_dispatch_df(blob, layout):
    """Check the admitted launcher's CLD-to-copy path without executing it."""
    import capstone
    from capstone import Cs, CS_ARCH_X86, CS_MODE_16
    from capstone.x86 import X86_OP_IMM
    decoder = Cs(CS_ARCH_X86, CS_MODE_16)
    decoder.detail = True
    pieces = {row["name"]: row for row in layout["partition"]}
    dispatcher, helper, directory = (pieces[name] for name in
        ("inner-dispatcher", "inner-copy-helper", "inner-directory"))
    inner = dispatcher["file_start"]
    stub = blob[inner:dispatcher["file_end"]]
    entry = 2 + int.from_bytes(stub[1:2], "little", signed=True)
    body = list(decoder.disasm(stub[entry:], 0x100 + entry))
    need(body and sum(i.size for i in body) == len(stub) - entry and
         body[0].mnemonic == "cld" and not any(i.mnemonic == "std" for i in body),
         "dispatcher does not preserve the admitted forward direction")
    addresses = {i.address for i in body}
    transfer = directory["file_end"] - inner - 3 + 0x100
    for ins in body:
        need(not ins.group(capstone.CS_GRP_CALL) and not ins.group(capstone.CS_GRP_RET),
             "unreviewed dispatcher call/return path")
        if ins.group(capstone.CS_GRP_JUMP) or ins.mnemonic.startswith("loop"):
            need(len(ins.operands) == 1 and ins.operands[0].type == X86_OP_IMM and
                 ins.operands[0].imm in addresses | {transfer}, "dispatcher branches outside reviewed path")
    copying = blob[helper["file_start"]:helper["file_end"]]
    instructions = list(decoder.disasm(copying, 0x100 + helper["file_start"] - inner))
    need(sum(i.size for i in instructions) == len(copying) and
         not any(i.mnemonic == "std" for i in instructions), "copy helper changes the admitted DF")
    return {"dispatcher_instruction_bytes": len(stub) - entry,
            "copy_helper_bytes": len(copying), "direction_flag": 0,
            "runtime_execution_observed": False}


def review_inputs(meta, *, root=ROOT):
    config = load_target_manifest(root / "config/targets.toml")
    artifact = find_artifact(config, meta["artifact"])
    blob = read_verified_artifact(root, artifact)
    layout = parse_launcher(blob, expected_sha256=meta["target_sha256"])
    members = [row for row in layout["partition"] if row["name"] == meta["member"]]
    need(len(members) == 1, "font child missing or ambiguous")
    member = members[0]
    need((member["file_start"], member["file_end"], member["sha256"]) ==
         (meta["member_start"], meta["member_end"], meta["member_sha256"]), "font child changed")
    reader = blob[meta["member_start"]:meta["reader_end"]]
    bitmap = blob[meta["bitmap_start"]:meta["bitmap_end"]]
    need(sha(reader) == meta["reader_sha256"] and sha(bitmap) == meta["bitmap_sha256"],
         "native reader/bitmap digest changed")
    model = validate_reader(reader, meta["bitmap_start"] - meta["member_start"], member["size"])
    dispatch_df = validate_dispatch_df(blob, layout)
    modeled = bitmap_tiles(read_input(root, meta["reference_bitmap"]))
    need(modeled == bitmap, "full BMP tile model differs from native resource")
    independent = json.loads(read_input(root, meta["independent_review"]))
    need(independent["target"]["sha256"] == meta["target_sha256"] and
         independent["font_child"]["geometry_model"]["modeled_sha256"] == meta["bitmap_sha256"],
         "independent review does not cover this resource")
    return {"kind": "native-embedded-font-resource-review", "size": len(bitmap),
            "native_reader": model, "launcher_df_path": dispatch_df, "full_reference_tile_equality": True,
            "authored_credit": 0, "compiler_invocations": 0, "authored_denominator": None}


def validate_decision(decision, meta, proof_sha):
    need(decision.get("schema_version") == 1 and
         decision.get("decision") == "ADOPT_ONLY_LISTED_RESOURCE_BYTES" and
         decision.get("scopes") == [meta["id"]] and
         decision.get("evidence_sha256") == proof_sha and
         decision.get("authored_credit") == 0 and type(decision["authored_credit"]) is int and
         decision.get("authored_denominator") is None and
         decision.get("other_scopes_policy") == "unknown", "invalid explicit resource decision")


def reviewed_claims(root, views, *, verify_targets=False):
    proof_path, decision_path = root / PROOF, root / DECISION
    if not proof_path.exists() and not decision_path.exists():
        return {}, None
    need(proof_path.exists() and decision_path.exists(), "incomplete resource adoption")
    proof_bytes, decision_bytes = proof_path.read_bytes(), decision_path.read_bytes()
    meta, decision = json.loads(proof_bytes), json.loads(decision_bytes)
    target = find_artifact(load_target_manifest(root / "config/targets.toml"), "th05-zun")
    validate_metadata(meta, views["zun"], target, root=root)
    validate_decision(decision, meta, sha(proof_bytes))
    if verify_targets:
        review_inputs(meta, root=root)
    return {"zun": [{"start": meta["bitmap_start"], "end": meta["bitmap_end"],
                     "kind": "reviewed-embedded-font-bitmap", "resource": meta["id"],
                     "model": MODEL, "instruction_bytes": 0, "authored_credit": 0}]}, sha(decision_bytes)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--native-check", action="store_true",
                        help="rehash actual target/reference and recheck reader; no target execution")
    args = parser.parse_args()
    import tomllib
    views = tomllib.loads((ROOT / "config/ownership.toml").read_text())["views"]
    claims, _ = reviewed_claims(ROOT, views, verify_targets=args.native_check)
    print(json.dumps({"kind": "native-resource-review" if args.native_check else
                     "public-resource-metadata-only", "claims": claims,
                     "byte_proof_replayed": args.native_check, "authored_credit": 0,
                     "authored_denominator": None}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
