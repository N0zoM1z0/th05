#!/usr/bin/env python3
"""Adopt only independently accepted ZUN.COM source scopes into its ownership map.

This is a coordinate overlay, not a new reconstruction or global authored-credit
claim. Each module is checked against its current manifest/acceptance and the
pinned original COM child. Existing CRT, C++ resident, and bitmap owners remain
separate and are deliberately not duplicated here.
"""
from __future__ import annotations

import json
from pathlib import Path
import tomllib

from lib.launcher import parse_launcher
from lib.pc98 import digest_bytes, digest_file
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "reviewed-native-zun-com-reconstruction"


def _manifest(name: str) -> dict:
    return tomllib.loads((ROOT / f"config/{name}.toml").read_text())


def _record(name: str) -> dict:
    return json.loads((ROOT / f"config/{name}_acceptance.json").read_text())


def _child(raw: bytes, artifact: dict, member: str, start: int, size: int, sha256: str) -> bytes:
    layout = parse_launcher(raw, expected_sha256=artifact["sha256"])
    rows = [row for row in layout["payloads"] if row["name"] == member]
    if len(rows) != 1:
        raise ValueError(f"ZUN {member} child is missing or ambiguous")
    row = rows[0]
    if (row["file_start"], row["size"], row["sha256"]) != (start, size, sha256):
        raise ValueError(f"ZUN {member} child identity differs from its accepted manifest")
    return raw[row["file_start"]:row["file_end"]]


def _claim(start: int, end: int, kind: str, unit: str, source_origin: str,
           *, instruction_bytes: int | None = None, **extra) -> dict:
    if instruction_bytes is None:
        instruction_bytes = end - start if kind == "accepted-zun-com-instructions" else 0
    return {"start": start, "end": end, "kind": kind, "unit": unit,
            "origin": ORIGIN, "source_origin": source_origin,
            "instruction_bytes": instruction_bytes, **extra}


def _code_with_padding(base: int, size: int, offsets: list[int], unit: str,
                       source_origin: str, *, vendor: bool = False) -> list[dict]:
    if offsets != sorted(set(offsets)) or any(type(x) is not int or not 0 <= x < size for x in offsets):
        raise ValueError(f"invalid {unit} alignment offsets")
    kind = "verified-vendor-code" if vendor else "accepted-zun-com-instructions"
    rows = []
    cursor = 0
    for offset in offsets:
        if cursor < offset:
            rows.append(_claim(base + cursor, base + offset, kind, unit, source_origin,
                               instruction_bytes=offset - cursor,
                               library="Master 0.23", member=unit) if vendor else
                        _claim(base + cursor, base + offset, kind, unit, source_origin))
        rows.append(_claim(base + offset, base + offset + 1,
                           "checked-uncredited-zun-com-alignment", unit, source_origin,
                           instruction_bytes=0, authored_credit=0))
        cursor = offset + 1
    if cursor < size:
        rows.append(_claim(base + cursor, base + size, kind, unit, source_origin,
                           instruction_bytes=size - cursor,
                           library="Master 0.23", member=unit) if vendor else
                    _claim(base + cursor, base + size, kind, unit, source_origin))
    return rows


def reviewed_claims(root: Path, view: dict, *, verify_targets: bool = False):
    """Return exact accepted non-CRT ZUN claims and their evidence fingerprint."""
    root = root.resolve()
    if root != ROOT.resolve():
        raise ValueError("ZUN ownership review is bound to the live repository root")
    artifact = find_artifact(load_target_manifest(root / "config/targets.toml"), "th05-zun")
    raw = read_verified_artifact(root, artifact)
    if (len(raw), digest_bytes(raw)) != (view.get("size"), view.get("sha256")):
        raise ValueError("ZUN ownership view differs from the pinned original COM")

    # Run the same source-current acceptance validators used by each focused
    # replay. These are metadata/target checks only; no cold replay is launched.
    import replay_zun_outer as outer
    import replay_zun_dispatcher as dispatcher
    import replay_zun_adpcm as adpcm
    import replay_zun_interrupt as interrupt
    import replay_zun_gaiji as gaiji
    import replay_zun_memory as memory
    import replay_zun_resdata as resdata
    import replay_zun_file_native as file_native

    configs = {name: _manifest(f"zun_{name}") for name in (
        "outer", "dispatcher", "adpcm", "interrupt", "gaiji", "memory",
        "resdata", "file_native")}
    records = {name: _record(f"zun_{name}") for name in configs}

    outer.scope(configs["outer"])
    outer.check_record(records["outer"], configs["outer"])
    header, usage, wrapper = outer.real_target(configs["outer"])
    if (len(header), len(usage), len(wrapper)) != (39, 264, 68):
        raise ValueError("ZUN outer header/help/wrapper extents changed")

    dispatcher.scope(configs["dispatcher"])
    dispatcher.check_record(records["dispatcher"], configs["dispatcher"])
    prefix, transfer = dispatcher.original(configs["dispatcher"])
    if (len(prefix), len(transfer)) != (550, 8):
        raise ValueError("ZUN inner dispatcher prefix/transfer extent changed")

    adpcm.scope(configs["adpcm"])
    adpcm.check_public(records["adpcm"], configs["adpcm"])
    adpcm_child = adpcm.target_child(configs["adpcm"])
    interrupt_spans = interrupt.scope(configs["interrupt"])
    interrupt.check_record(records["interrupt"], configs["interrupt"])
    interrupt_child = interrupt.target_child(configs["interrupt"])
    gaiji_spans = gaiji.scope(configs["gaiji"])
    gaiji.check_record(records["gaiji"], configs["gaiji"])
    gaiji_child = gaiji.original(configs["gaiji"])
    memory.check_public(records["memory"], configs["memory"])
    memory_child = memory.target_child(configs["memory"])

    resdata.check_scope(configs["resdata"])
    resdata.check_record(records["resdata"], configs["resdata"])
    resdata_child = resdata.native(configs["resdata"])
    file_native.scope(configs["file_native"])
    file_native.check(records["file_native"], configs["file_native"])
    file_child = file_native.original(configs["file_native"])

    # The child helpers above validate the actual payload hashes and launcher
    # offsets; explicitly bind the two Master source fragments to the same -S.
    s = [row for row in parse_launcher(raw, expected_sha256=artifact["sha256"])["payloads"]
         if row["name"] == "-S"]
    if len(s) != 1:
        raise ValueError("ZUN -S child is missing")
    member = s[0]
    for config, size in ((configs["resdata"], 226), (configs["file_native"], 830)):
        if (config["member_start"], config["member_size"]) != (member["file_start"], member["size"]):
            raise ValueError("ZUN Master source family is bound to a different -S child")
    if len(resdata_child) != 226 or len(file_child) != 830:
        raise ValueError("ZUN Master source family target extent changed")

    claims: list[dict] = []

    # COMCSTM's outer three-byte JMP, semantic header/help data, and final
    # 68-byte relocation wrapper; the entire 17,745-byte inner program is foreign.
    c = configs["outer"]
    claims.append(_claim(0, 3, "accepted-zun-com-instructions", "zun-outer", c["origin"]))
    claims.append(_claim(3, c["inner_start"], "accepted-zun-com-initialized-data",
                         "zun-outer", c["origin"], instruction_bytes=0))
    claims.append(_claim(c["wrapper_start"], c["wrapper_start"] + c["wrapper_size"],
                         "accepted-zun-com-instructions", "zun-outer", c["origin"]))

    # Source-owned dispatcher prefix and the separated eight-byte copy-up
    # helper. Five embedded child payloads remain their own independent owners.
    c = configs["dispatcher"]
    for start, end in dispatcher.CODE_SPANS:
        claims.append(_claim(c["inner_start"] + start, c["inner_start"] + end,
                             "accepted-zun-com-instructions", "zun-dispatcher", c["origin"]))
    for start, end in dispatcher.DATA_SPANS:
        claims.append(_claim(c["inner_start"] + start, c["inner_start"] + end,
                             "accepted-zun-com-initialized-data", "zun-dispatcher",
                             c["origin"], instruction_bytes=0))

    # Standalone -O ADPCM child: the original 892-byte CODE segment followed
    # by 34 initialized bytes; its 42-byte BSS is runtime storage, not file data.
    c = configs["adpcm"]
    base = c["container_start"]
    claims.append(_claim(base, base + c["code_bytes"], "accepted-zun-com-instructions",
                         "zun-adpcm", c["origin"]))
    claims.append(_claim(base + c["code_bytes"], base + c["size"],
                         "accepted-zun-com-initialized-data", "zun-adpcm",
                         c["origin"], instruction_bytes=0))

    # Standalone -I child: preserve its four independently reviewed CODE/DATA
    # spans and split the two actual EVEN NOPs out of instruction credit.
    c = configs["interrupt"]
    base = c["container_start"]
    for span in interrupt_spans:
        if span["kind"] == "code_spans":
            claims.extend(_code_with_padding(base + span["start"], span["size"],
                                              [n - span["start"] for n in c["uncredited_alignment_offsets"]
                                               if span["start"] <= n < span["start"] + span["size"]],
                                              "zun-interrupt", c["origin"]))
        else:
            claims.append(_claim(base + span["start"], base + span["start"] + span["size"],
                                 "accepted-zun-com-initialized-data", "zun-interrupt",
                                 c["origin"], instruction_bytes=0))

    # Standalone -G child: 75 instructions, one EVEN alignment byte, 109
    # initialized message bytes, then the independently reviewed 8 KiB font.
    c = configs["gaiji"]
    base = c["container_start"]
    for span in gaiji_spans:
        kind = span["kind"]
        if kind == "code_bytes":
            claims.append(_claim(base + span["start"], base + span["end"],
                                 "accepted-zun-com-instructions", "zun-gaiji", c["origin"]))
        elif kind == "alignment_bytes":
            claims.append(_claim(base + span["start"], base + span["end"],
                                 "checked-uncredited-zun-com-alignment", "zun-gaiji", c["origin"],
                                 instruction_bytes=0, authored_credit=0))
        elif kind == "initialized_message_bytes":
            claims.append(_claim(base + span["start"], base + span["end"],
                                 "accepted-zun-com-initialized-data", "zun-gaiji",
                                 c["origin"], instruction_bytes=0))
        elif kind != "external_resource_bytes":
            raise ValueError("unknown accepted -G content span")
    if len(gaiji_child) != c["size"]:
        raise ValueError("ZUN -G child extent changed")

    # Standalone -M memory check; CODE and initialized messages are distinct.
    c = configs["memory"]
    base = c["container_start"]
    claims.append(_claim(base, base + c["code_bytes"], "accepted-zun-com-instructions",
                         "zun-memory", c["origin"]))
    claims.append(_claim(base + c["code_bytes"], base + c["size"],
                         "accepted-zun-com-initialized-data", "zun-memory",
                         c["origin"], instruction_bytes=0))

    # Two source-exact Master 0.23 procedures families. Preserve every
    # alignment NOP as zero-credit; only the 224/823 real instruction bytes
    # receive the third-party vendor classification.
    c = configs["resdata"]
    base = c["member_start"] + c["scope_start_com"] - 0x100
    claims.extend(_code_with_padding(base, c["scope_bytes"], c["uncredited_alignment_offsets"],
                                     "master-resdata", c["origin"], vendor=True))
    c = configs["file_native"]
    base = c["member_start"] + c["start_com"] - 0x100
    claims.extend(_code_with_padding(base, c["scope_size"], c["uncredited_alignment_offsets"],
                                     "master-file-family", c["origin"], vendor=True))

    # Prove the claims form exactly the independently accepted 4,416-byte
    # complement of the existing CRT/C++/font owners; the 2-byte writable CRT
    # CS slot and all still-unreviewed -S bytes remain unknown.
    expected = 4416
    if sum(row["end"] - row["start"] for row in claims) != expected:
        raise ValueError("ZUN accepted module ownership total changed")
    if verify_targets:
        # Recheck all target child byte slices without recompiling any module.
        for child, config in ((adpcm_child, configs["adpcm"]),
                              (interrupt_child, configs["interrupt"]),
                              (gaiji_child, configs["gaiji"]),
                              (memory_child, configs["memory"])):
            if digest_bytes(child) != config["sha256"]:
                raise ValueError("ZUN child payload changed during target verification")

    evidence = {}
    for name in configs:
        evidence[name] = {
            "manifest": digest_file(root / f"config/zun_{name}.toml"),
            "acceptance": digest_file(root / f"config/zun_{name}_acceptance.json"),
        }
    return claims, digest_bytes(json.dumps(evidence, sort_keys=True, separators=(",", ":")).encode())
