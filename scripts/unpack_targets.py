#!/usr/bin/env python3
"""Extract hash-attested TH05 decoded images below ignored .analysis/decoded.

OP/MAINE use their own DIET decoder at two independent DOS load segments.
MAIN is a plain MZ image; ZUN is a plain COM container. Generated output is
target evidence, never maintained source or authored reconstruction progress.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import struct
import sys

from lib.diet import DEFAULT_LOAD_SEGMENTS, DietError, DietPolicy, observe, sha256, UNICORN_VERSION
from lib.pc98 import parse_mz
from lib.targets import TargetError, find_artifact, load_target_manifest, read_verified_artifact

ROOT = Path(__file__).resolve().parents[1]

# Target-observed topology, independently reproduced at 1000 and 3333 load
# segments. Payload length comes from the decoder's terminal ES:DI, not a
# reference build's file size. Restore the stack and stop before original CS:IP.
DIET_TOPOLOGY = {
    "th05-op": (77798, 952, 0x141c),
    "th05-maine": (77396, 667, 0x1c68),
}


def decode(artifact: dict, target: bytes, load_segments: tuple[int, ...],
           max_instructions: int) -> tuple[bytes, list[dict], dict]:
    if sha256(target) != artifact["sha256"]:
        raise DietError("target digest changed after attestation")
    artifact_id = artifact["id"]
    if artifact_id in DIET_TOPOLOGY:
        size, count, ss = DIET_TOPOLOGY[artifact_id]
        policy = DietPolicy(artifact["sha256"], size, count, ss)
        payload, runs = observe(target, policy, load_segments, max_instructions)
        relocations = [asdict(item) for item in runs[0].relocations]
        return payload, relocations, {
            "method": "target-owned-diet-decoder",
            "policy": asdict(policy),
            "unicorn_version": UNICORN_VERSION,
            "entry_cs": policy.entry_cs, "entry_ip": policy.entry_ip,
            "initial_ss": ss, "initial_sp": policy.initial_sp,
            "runs": [dict(
                load_segment=run.load_segment, decoded_end=run.decoded_end,
                transfer_site=run.transfer_site,
                final_cs=run.final_cs, final_ip=run.final_ip,
                final_ss=run.final_ss, final_sp=run.final_sp,
                instruction_count=run.instruction_count, dos_version_calls=run.dos_version_calls,
                relocated_payload_sha256=sha256(run.relocated_payload),
            ) for run in runs],
            "checks": {"distinct_load_segments": True, "relocation_stream_load_invariant": True,
                       "complete_decoded_bytes_load_invariant": True,
                       "decoder_output_extent": True, "restored_entry_and_stack": True},
        }
    if artifact_id == "th05-main":
        image = parse_mz(target)
        if not image.valid or image.overlay or target[0x1c:0x20].lower() == b"diet":
            raise DietError("MAIN must remain an ordinary valid MZ without overlay")
        relocations = [dict(segment=r.segment, offset=r.offset, linear=r.linear) for r in image.relocations]
        # Exercise the independent MZ loader at each requested base and undo its
        # additions. No DIET stub exists in this target.
        if len(load_segments) < 2 or len(set(load_segments)) != len(load_segments):
            raise DietError("at least two distinct load segments are required")
        runs = []
        for segment in load_segments:
            relocated = bytearray(image.relocated_program_image(segment))
            loaded_sha = sha256(relocated)
            for item in image.relocations:
                value = struct.unpack_from("<H", relocated, item.linear)[0]
                struct.pack_into("<H", relocated, item.linear, (value - segment) & 0xffff)
            if bytes(relocated) != image.program_image:
                raise DietError("plain MZ relocation roundtrip differs")
            runs.append(dict(load_segment=segment, relocated_payload_sha256=loaded_sha))
        return image.program_image, relocations, {
            "method": "plain-mz-load-module", "header_size": image.header.header_size,
            "entry_cs": image.header.initial_relative_cs, "entry_ip": image.header.initial_ip,
            "initial_ss": image.header.initial_relative_ss, "initial_sp": image.header.initial_sp,
            "runs": runs,
            "checks": {"valid_mz": True, "no_overlay": True, "relocation_roundtrips": True},
        }
    if artifact_id == "th05-zun":
        if target[:2] in (b"MZ", b"ZM"):
            raise DietError("ZUN must remain plain COM")
        return target, [], {"method": "plain-com-container", "entry_ip": 0x100,
                            "address_bias": 0x100, "checks": {"plain_com": True}}
    raise DietError(f"unsupported target {artifact_id}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", nargs="?", default="all",
                        choices=("all", "th05-main", "th05-op", "th05-maine", "th05-zun"))
    parser.add_argument("--output-dir", type=Path, default=ROOT / ".analysis" / "decoded")
    parser.add_argument("--load-segment", type=lambda value: int(value, 0), action="append")
    parser.add_argument("--max-instructions", type=int, default=2_000_000)
    args = parser.parse_args()
    try:
        output = args.output_dir.resolve()
        if not output.is_relative_to((ROOT / ".analysis").resolve()):
            raise DietError("decoded target output must stay below ignored .analysis")
        segments = tuple(args.load_segment or DEFAULT_LOAD_SEGMENTS)
        if args.max_instructions <= 0:
            raise DietError("instruction budget must be positive")
        manifest = load_target_manifest(ROOT / "config" / "targets.toml")
        selected = ([item["id"] for item in manifest["artifacts"]]
                    if args.artifact == "all" else [args.artifact])
        for artifact_id in selected:
            artifact = find_artifact(manifest, artifact_id)
            target = read_verified_artifact(ROOT, artifact)
            payload, relocations, details = decode(artifact, target, segments, args.max_instructions)
            destination = (output / artifact_id).resolve()
            if not destination.is_relative_to((ROOT / ".analysis").resolve()):
                raise DietError("decoded target subdirectory escapes ignored .analysis")
            destination.mkdir(parents=True, exist_ok=True)
            (destination / "payload.bin").write_bytes(payload)
            relocation_bytes = (json.dumps(relocations, sort_keys=True, indent=2) + "\n").encode()
            (destination / "relocations.json").write_bytes(relocation_bytes)
            receipt = dict(
                schema_version=1, artifact=artifact_id, source="hash-attested-original-target",
                target_sha256=sha256(target), target_size=len(target),
                payload_sha256=sha256(payload), payload_size=len(payload),
                relocation_count=len(relocations), relocations_sha256=sha256(relocation_bytes),
                observer_sha256=sha256(Path(__file__).read_bytes()),
                diet_library_sha256=sha256((ROOT / "scripts/lib/diet.py").read_bytes()),
                provenance=manifest["source"]["canonicality"],
                claim="decoded target observation; no reconstruction acceptance", **details,
            )
            (destination / "receipt.json").write_text(json.dumps(receipt, sort_keys=True, indent=2) + "\n")
            print(f"PASS {artifact_id}: {len(payload):,} decoded bytes, {len(relocations)} relocations, "
                  f"sha256={sha256(payload)}", flush=True)
        return 0
    except (DietError, TargetError, OSError, ValueError) as error:
        print(f"error: decoded target observation failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
