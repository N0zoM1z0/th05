"""Three explicit TH05 unit ledgers and verified retained DIET comparison views.

No decoding, emulation, synthetic MZ headers, or relocation sorting occurs here.
"""
from __future__ import annotations
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import shutil
import struct
import tomllib

from .pc98 import MZRelocation, parse_mz
from .targets import find_artifact, load_target_manifest, read_verified_artifact


@dataclass(frozen=True)
class UnitContext:
    root: Path
    name: str = "main"

    def __post_init__(self):
        if self.name not in ("main", "op", "maine"):
            raise ValueError("unsupported unit artifact context")

    @property
    def artifact(self):
        return "th05-" + self.name

    @property
    def manifest(self):
        return self.root / ("config/exact_units.toml" if self.name == "main" else f"config/exact_units.{self.name}.toml")

    @property
    def ledger(self):
        return self.root / ("config/accepted_units.json" if self.name == "main" else f"config/accepted_units.{self.name}.json")

    @property
    def binary(self):
        return {"main": "M", "op": "O", "maine": "E"}[self.name]

    @property
    def cache(self):
        return self.root / ".analysis/decoded" / self.artifact

    def config(self):
        config = tomllib.loads(self.manifest.read_text())
        if config["artifact"] != self.artifact:
            raise ValueError("unit manifest belongs to a different artifact context")
        return config


@dataclass(frozen=True)
class DecodedUnitImage:
    program_image: bytes
    relocations: tuple[MZRelocation, ...]
    valid: bool = True


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def proof_sha256(proof: dict) -> str:
    return sha(json.dumps(proof, sort_keys=True, separators=(",", ":")).encode())


def validate_public_target_view(context: UnitContext, config: dict, proof: dict, packed_sha: str) -> None:
    """Public summaries verify the pinned historical proof without private files."""
    pin = config.get("target_view", {})
    if (not isinstance(proof, dict) or config["artifact"] != context.artifact or
            proof.get("artifact") != context.artifact or proof.get("kind") != "decoded-load-module-only" or
            proof.get("packed_target_sha256") != packed_sha or
            proof.get("receipt_sha256") != pin.get("receipt_sha256") or
            not pin.get("proof_sha256") or proof_sha256(proof) != pin["proof_sha256"]):
        raise ValueError("public decoded target comparison proof differs from its configuration pins")


def unit_binary(entry: dict, default: str = "M") -> str:
    value = entry.get("binary", default)
    if value not in ("M", "O", "E"):
        raise ValueError("unit binary must be M, O or E")
    return value


def compiler_arguments(entry: dict, default: str = "M") -> list[str]:
    return ["-c", "-I.", "-O", "-b-", "-3", "-Z", "-d", "-DGAME=5", "-ml",
            f"-DBINARY='{unit_binary(entry, default)}'", entry["module"]]


def load_unit_target(context: UnitContext, config: dict, *, cache: Path | None = None):
    if config["artifact"] != context.artifact:
        raise ValueError("comparison target belongs to a different artifact context")
    artifact = find_artifact(load_target_manifest(context.root / "config/targets.toml"), context.artifact)
    raw = read_verified_artifact(context.root, artifact)
    if context.name == "main":
        return artifact, parse_mz(raw), None
    cache = context.cache if cache is None else cache
    receipt_bytes = (cache / "receipt.json").read_bytes()
    pin = config.get("target_view", {}).get("receipt_sha256")
    if not pin or sha(receipt_bytes) != pin:
        raise ValueError("retained decoded receipt differs from its explicit configuration pin")
    receipt = json.loads(receipt_bytes)
    payload = (cache / "payload.bin").read_bytes()
    relocation_bytes = (cache / "relocations.json").read_bytes()
    rows = json.loads(relocation_bytes)
    checks = ("distinct_load_segments", "relocation_stream_load_invariant", "complete_decoded_bytes_load_invariant",
              "decoder_output_extent", "restored_entry_and_stack")
    if (receipt.get("artifact") != context.artifact or receipt.get("target_sha256") != artifact["sha256"] or
            receipt.get("target_size") != len(raw) or receipt.get("method") != "target-owned-diet-decoder" or
            receipt.get("payload_size") != len(payload) or receipt.get("payload_sha256") != sha(payload) or
            receipt.get("relocations_sha256") != sha(relocation_bytes) or
            receipt.get("relocation_count") != len(rows) or not all(receipt.get("checks", {}).get(key) is True for key in checks)):
        raise ValueError("retained decoded target hashes, topology or original identity disagree")
    relocations = []
    for row in rows:
        if (set(row) != {"offset", "segment", "linear"} or any(type(row[key]) is not int for key in row) or
                not 0 <= row["offset"] <= 0xFFFF or not 0 <= row["segment"] <= 0xFFFF or
                row["linear"] != row["segment"] * 16 + row["offset"] or
                not 0 <= row["linear"] <= len(payload) - 2):
            raise ValueError("decoded relocation frame, offset or extent is invalid")
        relocations.append(MZRelocation(offset=row["offset"], segment=row["segment"]))
    if len({row.linear for row in relocations}) != len(relocations):
        raise ValueError("duplicate decoded relocation sites")
    policy = receipt.get("policy", {})
    for field in ("target_sha256", "payload_size", "relocation_count", "entry_cs", "entry_ip", "initial_ss", "initial_sp"):
        if policy.get(field) != receipt.get(field):
            raise ValueError("decoded target policy disagrees with its receipt")
    runs = receipt.get("runs", [])
    if len(runs) < 2 or len({run["load_segment"] for run in runs}) != len(runs):
        raise ValueError("decoded proof requires two independent load segments")
    for run in runs:
        load = run["load_segment"]
        if (type(load) is not int or not 0x100 <= load <= 0x7000 or run["decoded_end"] != len(payload) or
                run["final_cs"] != load + receipt["entry_cs"] or run["final_ip"] != receipt["entry_ip"] or
                run["final_ss"] != load + receipt["initial_ss"] or run["final_sp"] != receipt["initial_sp"] or
                run["transfer_site"] != runs[0]["transfer_site"] or run["instruction_count"] <= 0):
            raise ValueError("decoded two-load transfer/stack proof disagrees")
        relocated = bytearray(payload)
        for fixup in relocations:  # Preserve the target's actual observed order.
            value = struct.unpack_from("<H", relocated, fixup.linear)[0]
            struct.pack_into("<H", relocated, fixup.linear, (value + load) & 0xFFFF)
        if sha(relocated) != run["relocated_payload_sha256"]:
            raise ValueError("decoded payload does not reproduce historical two-load byte hashes")
    proof = {"artifact": context.artifact, "kind": "decoded-load-module-only", "packed_target_sha256": artifact["sha256"],
             "receipt_sha256": pin, "payload_sha256": sha(payload), "relocations_sha256": sha(relocation_bytes),
             "payload_size": len(payload), "relocation_count": len(relocations), "runs": runs}
    validate_public_target_view(context, config, proof, artifact["sha256"])
    return artifact, DecodedUnitImage(payload, tuple(relocations)), proof


def freeze_target_view(context: UnitContext, destination: Path) -> None:
    destination.mkdir()
    for name in ("receipt.json", "payload.bin", "relocations.json"):
        shutil.copyfile(context.cache / name, destination / name)
