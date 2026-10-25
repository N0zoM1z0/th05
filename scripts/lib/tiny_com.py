"""ZUN embedded tiny-COM support; existing MZ/DIET validators stay unchanged.

No target extraction, synthetic headers or candidate-byte edits occur here.
The outer target file and the real linked COM each retain their file offsets.
"""
from __future__ import annotations
import json
from pathlib import Path
import re

from . import unit_context as legacy
from .unit_context import (DecodedUnitImage, freeze_target_view, proof_sha256, sha)
from .targets import find_artifact, load_target_manifest, read_verified_artifact
from .unit_oracle import (compare_mapped_unit as compare_mz_mapped_unit,
    compare_unit, map_unit_scope)


class UnitContext(legacy.UnitContext):
    def __post_init__(self):
        if self.name != "zun":
            super().__post_init__()

    @property
    def binary(self):
        return None if self.name == "zun" else super().binary


class TinyCOMImage:
    def __init__(self, raw: bytes):
        self.program_image = raw
        self.relocations = ()
        self.valid = True
        self.address_bias = 0x100


def unit_binary(entry: dict, default: str | None = "M") -> str | None:
    if default is None:
        if "binary" in entry:
            raise ValueError("tiny COM context does not accept a large-model binary override")
        return None
    return legacy.unit_binary(entry, default)


def compiler_arguments(entry: dict, default: str | None = "M") -> list[str]:
    if default is not None:
        return legacy.compiler_arguments(entry, default)
    unit_binary(entry, default)
    return ["-c", "-I.", "-O", "-b-", "-3", "-Z", "-d", "-DGAME=5", "-mt", entry["module"]]


def validate_public_target_view(context: UnitContext, config: dict, proof: dict, packed_sha: str) -> None:
    if context.name != "zun":
        return legacy.validate_public_target_view(context, config, proof, packed_sha)
    pin = config.get("target_view", {})
    if (not isinstance(proof, dict) or config["artifact"] != context.artifact or
            proof.get("artifact") != context.artifact or proof.get("kind") != "embedded-plain-com-source-view" or
            proof.get("packed_target_sha256") != packed_sha or proof.get("payload_sha256") != packed_sha or
            proof.get("receipt_sha256") != pin.get("receipt_sha256") or
            proof.get("member") != pin.get("member") or proof.get("member_start") != pin.get("member_start") or
            proof.get("member_end") != pin.get("member_end") or proof.get("member_sha256") != pin.get("member_sha256") or
            proof.get("child_address_bias") != 0x100 or proof.get("relocation_count") != 0 or
            not pin.get("proof_sha256") or proof_sha256(proof) != pin["proof_sha256"]):
        raise ValueError("public embedded COM proof differs from its configuration pins")
    for entry in config.get("units", []):
        if not proof["member_start"] <= entry["target_start"] < entry["target_start"] + entry["size"] <= proof["member_end"]:
            raise ValueError("unit leaves the pinned embedded COM member")


TINY_CRT_SHA256 = "27169f062a9b77bf4accfb9550ca4ccbf0fd710d4b1232768630d53bb6305f7c"


def load_unit_candidate(source: Path, binary: str | None):
    """Read the actual linker output; COM files never receive a synthetic header."""
    if binary is not None:
        return legacy.parse_mz((source / "units.exe").read_bytes())
    if sha((source / "c0t.obj").read_bytes()) != TINY_CRT_SHA256:
        raise ValueError("tiny COM startup object differs from the pinned C0T.OBJ")
    arguments = json.loads((source / "compiler-arguments.json").read_text())
    objects = []
    for module, argv in arguments.items():
        if argv != compiler_arguments({"module": module}, None):
            raise ValueError("tiny COM producer flags differ")
        objects.append(Path(module).stem + ".obj")
    expected = ("-c -s -t c0t.obj " + " ".join(objects) + " bindings.obj, units.com, units.map,\r\n").encode("ascii")
    if not objects or len(set(objects)) != len(objects) or (source / "link.rsp").read_bytes() != expected:
        raise ValueError("tiny COM linker order or output format differs")
    lines = (source / "units.map").read_text(encoding="cp437")
    # TLINK omits an entry-point MAP row for -t. The pinned real C0T MODEND
    # and its first position in the actual -t response establish COM entry.
    entry_rows = re.findall(r"Program entry point at (\S+)", lines)
    if entry_rows and entry_rows != ["0000:0100"]:
        raise ValueError("tiny COM entry differs from the real CRT entry at 0000:0100")
    contributions = re.findall(r"^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+([0-9A-F]{4})\s+C=\S+\s+S=(\S+)\s+G=(\S+)\s+M=(\S+)\s+ACBP=([0-9A-F]{2})", lines, re.M | re.I)
    if (not contributions or any(row[0] != "0000" or row[4] != "DGROUP" for row in contributions) or
            ("0000", "0000", "0367", "_TEXT", "DGROUP", "c0.ASM", "28") not in contributions or
            ("0000", "1650", "006E", "_DATA", "DGROUP", "c0.ASM", "68") not in contributions):
        raise ValueError("tiny COM CRT segment layout or DGROUP frame differs")
    raw = (source / "units.com").read_bytes()
    if not 0 < len(raw) <= 0xff00 or raw[:2] in (b"MZ", b"ZM"):
        raise ValueError("invalid raw tiny COM output")
    return TinyCOMImage(raw)

def load_unit_target(context: UnitContext, config: dict, *, cache: Path | None = None):
    if context.name != "zun":
        return legacy.load_unit_target(context, config, cache=cache)
    if config["artifact"] != context.artifact:
        raise ValueError("comparison target belongs to a different artifact context")
    artifact = find_artifact(load_target_manifest(context.root / "config/targets.toml"), context.artifact)
    raw = read_verified_artifact(context.root, artifact)
    cache = context.cache if cache is None else cache
    receipt_bytes = (cache / "receipt.json").read_bytes()
    pin = config.get("target_view", {}).get("receipt_sha256")
    if not pin or sha(receipt_bytes) != pin:
        raise ValueError("retained plain COM receipt differs from its configuration pin")
    receipt = json.loads(receipt_bytes)
    payload = (cache / "payload.bin").read_bytes()
    relocation_bytes = (cache / "relocations.json").read_bytes()
    rows = json.loads(relocation_bytes)
    from .launcher import parse_launcher
    if (receipt.get("artifact") != context.artifact or receipt.get("target_sha256") != artifact["sha256"] or
            receipt.get("target_size") != len(raw) or receipt.get("method") != "plain-com-container" or
            receipt.get("checks", {}).get("plain_com") is not True or receipt.get("address_bias") != 0x100 or
            receipt.get("entry_ip") != 0x100 or payload != raw or receipt.get("payload_size") != len(raw) or
            receipt.get("payload_sha256") != sha(raw) or rows != [] or receipt.get("relocation_count") != 0 or
            receipt.get("relocations_sha256") != sha(relocation_bytes)):
        raise ValueError("retained plain COM receipt or original bytes disagree")
    pin = config["target_view"]
    members = [row for row in parse_launcher(raw, expected_sha256=artifact["sha256"])["payloads"] if row["name"] == pin["member"]]
    if len(members) != 1:
        raise ValueError("embedded COM member is missing or ambiguous")
    member = members[0]
    proof = dict(artifact=context.artifact, kind="embedded-plain-com-source-view",
                 packed_target_sha256=artifact["sha256"], receipt_sha256=sha(receipt_bytes),
                 payload_sha256=sha(payload), payload_size=len(payload),
                 relocations_sha256=sha(relocation_bytes), relocation_count=0,
                 member=member["name"], member_start=member["file_start"], member_end=member["file_end"],
                 member_sha256=member["sha256"], child_address_bias=0x100)
    validate_public_target_view(context, config, proof, artifact["sha256"])
    return artifact, DecodedUnitImage(raw, ()), proof


def compare_mapped_unit(target, candidate, path: Path, entry: dict) -> dict:
    if not getattr(candidate, "address_bias", 0):
        return compare_mz_mapped_unit(target, candidate, path, entry)
    if candidate.address_bias != 0x100:
        raise ValueError("unsupported COM address bias")
    scope = map_unit_scope(path, entry)
    if scope["size"] != entry["size"]:
        raise ValueError(f"{entry['id']}: {scope['kind']} size mismatch: {scope['size']}")
    comparison = compare_unit(target, candidate, entry["target_start"], scope["start"] - 0x100, scope["size"])
    return {**comparison, "candidate_address_bias": 0x100, "map_scope": scope}
