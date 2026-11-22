#!/usr/bin/env python3
"""Recheck every accepted C/C++ ledger row against the target and retained producers.

This deliberately avoids scripts/lib: it reparses the original MZ, the
decoded OP/MAINE payloads and each retained producer EXE/COM itself. For every
row it checks that

- the recorded target hash and ordered fixups match the pinned target bytes;
- both retained producers still hold bytes and fixups equal to the target;
- the receipt that the ledger names exists and lists the same unit;
- the compiled negative differs from the target;
- resources/ownership.json files exactly the ledger extents under that unit.

The reviewed-ASM family ledger (config/accepted_asm_families.json) gets the
same checks with its producers `a`, `b` and `negative`.

It needs the private .analysis/ inputs and runs no compiler.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
CXX_KINDS = {"accepted-cxx-instructions", "accepted-cxx-switch-table",
             "accepted-cxx-initialized-data", "accepted-c-initialized-data"}
LEDGERS = {"main": "config/accepted_units.json", "op": "config/accepted_units.op.json",
           "maine": "config/accepted_units.maine.json", "zun": "config/accepted_units.zun.json"}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_mz(data: bytes) -> tuple[bytes, list[int]]:
    if data[:2] not in (b"MZ", b"ZM"):
        raise ValueError("not an MZ file")
    cblp, cp, crlc, cparhdr = struct.unpack_from("<4H", data, 2)
    lfarlc = struct.unpack_from("<H", data, 0x18)[0]
    end = cp * 512 - (512 - cblp if cblp else 0)
    image = data[cparhdr * 16:end]
    sites = []
    for i in range(crlc):
        off, seg = struct.unpack_from("<2H", data, lfarlc + 4 * i)
        sites.append(seg * 16 + off)
    return image, sites


def target_view(artifact: str) -> tuple[bytes, list[int]]:
    if artifact == "main":
        return parse_mz((ROOT / ".analysis/targets/th05/main.exe").read_bytes())
    base = ROOT / f".analysis/decoded/th05-{artifact}"
    receipt = json.loads((base / "receipt.json").read_text())
    payload = (base / "payload.bin").read_bytes()
    if sha(payload) != receipt["payload_sha256"]:
        raise ValueError(f"{artifact} decoded payload differs from its receipt")
    return payload, [r["linear"] for r in json.loads((base / "relocations.json").read_text())]


def fixups(sites: list[int], start: int, size: int) -> list[int]:
    out = []
    for site in sites:
        if site < start + size and site + 2 > start:
            if site < start or site + 2 > start + size:
                raise ValueError("relocation word crosses the unit boundary")
            out.append(site - start)
    return out


def candidate_view(source: Path) -> tuple[bytes, list[int]]:
    if (source / "units.exe").exists():
        return parse_mz((source / "units.exe").read_bytes())
    return (source / "units.com").read_bytes(), []


def receipt_index() -> dict[str, Path]:
    index = {}
    for path in (ROOT / ".analysis").rglob("receipt.json"):
        index.setdefault(sha(path.read_bytes()), path)
    return index


ASM_KINDS = ("accepted-reviewed-asm-", "checked-uncredited-asm-")


def audit_asm(receipts, ownership, problems) -> int:
    ledger = json.loads((ROOT / "config/accepted_asm_families.json").read_text())
    views, checked = {}, 0
    for uid, unit in ledger["units"].items():
        artifact = unit["entry"]["artifact"]
        if artifact not in views:
            views[artifact] = target_view(artifact)
        image, sites = views[artifact]
        def bad(message: str) -> None:
            problems.append(f"asm:{uid}: {message}")
        comparisons = [r["comparison"] for r in unit["rounds"]]
        if len(comparisons) != 2 or not all(c["exact"] for c in comparisons):
            bad("expected two exact producer rounds")
            continue
        start, size = unit["entry"]["target_start"], unit["entry"]["size"]
        target = image[start:start + size]
        target_fixups = fixups(sites, start, size)
        if sha(target) != comparisons[0]["target_sha256"] or comparisons[0]["target_fixups"] != target_fixups:
            bad("recorded target bytes or fixups differ from the pinned target")
        if target_fixups != unit["entry"]["fixups"]:
            bad(f"configured fixups {unit['entry']['fixups']} differ from target {target_fixups}")
        receipt = receipts.get(unit["replay_receipt_sha256"])
        if receipt is None:
            bad("named replay receipt is not retained")
            continue
        for label, comparison in zip("ab", comparisons):
            cimage, csites = candidate_view(receipt.parent / label / "source")
            cs = comparison["candidate_start"]
            if cimage[cs:cs + size] != target or fixups(csites, cs, size) != target_fixups:
                bad(f"retained producer {label} differs from the target")
        nimage, nsites = candidate_view(receipt.parent / "negative" / "source")
        ns = unit["negative_control"]["comparison"]["candidate_start"]
        if nimage[ns:ns + size] == target and fixups(nsites, ns, size) == target_fixups:
            bad("retained negative producer equals the target")
        rows = [(r["start"], r["end"]) for r in ownership["views"][artifact]["intervals"]
                if r.get("unit") == uid and r["kind"].startswith(ASM_KINDS)]
        rows.sort()
        if not rows or rows[0][0] != start or rows[-1][1] != start + size or any(
                a[1] != b[0] for a, b in zip(rows, rows[1:])):
            bad(f"ownership rows do not tile [{start:#x},{start + size:#x})")
        checked += 1
    return checked


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", choices=LEDGERS, action="append")
    args = parser.parse_args()
    receipts = receipt_index()
    ownership = json.loads((ROOT / "resources/ownership.json").read_text())
    problems, checked = [], 0
    for artifact in args.artifact or LEDGERS:
        ledger = json.loads((ROOT / LEDGERS[artifact]).read_text())
        image, sites = target_view(artifact)
        owned, padding = {}, []
        for row in ownership["views"][artifact]["intervals"]:
            if row["kind"] in CXX_KINDS:
                owned.setdefault(row["unit"], []).append((row["start"], row["end"]))
            elif row["kind"] == "checked-uncredited-padding":
                padding.append((row["start"], row["end"]))
        seen = set()
        for unit in ledger["units"]:
            uid, result = unit["id"], unit["result"]
            def bad(message: str) -> None:
                problems.append(f"{artifact}:{uid}: {message}")
            rounds = result["rounds"]
            if len(rounds) != 2 or len(result["producer_paths"]) != 2 or not result["exact"]:
                bad("expected two exact producer rounds")
                continue
            r0 = rounds[0]
            start, size = r0["target_start"], r0["size"]
            if artifact == "zun":
                start_in_view = start  # ZUN rows use outer ZUN.COM offsets
            else:
                start_in_view = start
            target = image[start_in_view:start_in_view + size]
            target_fixups = [] if artifact == "zun" else fixups(sites, start, size)
            if len(target) != size or sha(target) != r0["target_sha256"]:
                bad("recorded target hash differs from the pinned target")
            if r0["target_fixups"] != target_fixups:
                bad(f"recorded target fixups {r0['target_fixups']} differ from target {target_fixups}")
            receipt = receipts.get(unit["replay_receipt_sha256"])
            if receipt is None:
                bad("named replay receipt is not retained")
                continue
            record = json.loads(receipt.read_text())
            listed = [r.get("id") for r in record.get("results", [])]
            listed.append(record.get("entry", {}).get("id"))
            if uid not in listed:
                bad(f"receipt {receipt} does not list the unit")
            for rnd, producer in zip(rounds, result["producer_paths"]):
                if rnd["size"] != size or rnd["target_start"] != start:
                    bad("rounds disagree on the extent")
                source = receipt.parent / producer
                try:
                    cimage, csites = candidate_view(source)
                except FileNotFoundError:
                    bad(f"producer output missing in {source}")
                    continue
                cs = rnd["candidate_start"]
                candidate = cimage[cs:cs + size]
                if artifact == "zun" and sha(candidate) != rnd["candidate_sha256"]:
                    candidate = cimage[cs - 0x100:cs - 0x100 + size]
                if candidate != target:
                    bad(f"retained producer {producer} bytes differ from the target")
                if artifact != "zun" and fixups(csites, cs, size) != target_fixups:
                    bad(f"retained producer {producer} fixups differ from the target")
            negative = unit.get("compiled_negative_control") or ledger.get("compiled_negative_control")
            if not negative or negative.get("exact") is not False or (
                    negative["candidate_sha256"] == negative["target_sha256"]
                    and negative["candidate_fixups"] == negative["target_fixups"]):
                bad("compiled negative does not differ from the target")
            spans = sorted(owned.get(uid, []) + [p for p in padding if start <= p[0] and p[1] <= start + size])
            merged = []
            for a, b in spans:
                if merged and merged[-1][1] == a:
                    merged[-1] = (merged[-1][0], b)
                else:
                    merged.append((a, b))
            if merged != [(start, start + size)]:
                bad(f"ownership rows {merged} differ from ledger extent [{start:#x},{start + size:#x})")
            seen.add(uid)
            checked += 1
        extra = set(owned) - seen
        if extra:
            problems.append(f"{artifact}: ownership credits units missing from the ledger: {sorted(extra)}")
    checked += audit_asm(receipts, ownership, problems)
    for line in problems:
        print("FAIL", line)
    print(f"{'PASS' if not problems else 'FAIL'}: {checked} ledger rows rechecked, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
