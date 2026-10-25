"""General ASM gates: complete extents, native tables, incremental evidence, atomic imports."""
import copy
import hashlib
import json
from pathlib import Path
import struct
import sys
import tempfile
import tomllib
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import replay_asm_family as asm
from lib.pc98 import parse_mz, digest_bytes
from lib.unit_oracle import compare_unit
from ownership import validate_partition


def record(kind, payload):
    raw = bytes([kind]) + struct.pack("<H", len(payload) + 1) + payload
    return raw + bytes([-sum(raw) & 255])


def object_fixture(size, *, partial=False, overlap=False, data=False, producer="Turbo Assembler  Version 5.0"):
    names = ["BULLET_A_TEXT", "CODE", "_DATA", "DATA", ""]
    raw = record(0x80, b"\x07fixture")
    raw += record(0x88, b"\0\0" + bytes([len(producer)]) + producer.encode())
    raw += record(0x96, b"".join(bytes([len(n)]) + n.encode() for n in names))
    raw += record(0x98, b"\x48" + struct.pack("<H", size) + b"\1\2\5")
    raw += record(0x98, b"\x48" + struct.pack("<H", 1 if data else 0) + b"\3\4\5")
    raw += record(0xA0, b"\1\0\0" + b"A" * (size - (1 if partial else 0)))
    if overlap:
        raw += record(0xA0, b"\1\0\0B")
    return raw + record(0x8A, b"\0")


def image(payload):
    size = 32 + len(payload)
    header = struct.pack("<14H", 0x5A4D, size % 512, (size + 511) // 512,
                         0, 2, 1, 0xFFFF, 0, 16, 0, 0, 0, 28, 0)
    result = parse_mz(header.ljust(32, b"\0") + payload)
    if not result.valid:
        raise ValueError(result.errors)
    return result


class AsmFamilyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entries = asm.configuration()
        cls.records = asm.ledger(cls.entries)["units"]
        cls.entry = cls.entries["main-bullet-spawn-groups"]

    def test_only_complete_assembler_code_omf(self):
        self.assertEqual(asm.omf_scope(object_fixture(500), self.entry)["size"], 500)
        for bad in ({"partial": True}, {"overlap": True}, {"data": True},
                    {"producer": "TC86 Borland C++ 4.02"}):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                asm.omf_scope(object_fixture(500, **bad), self.entry)

    def test_map_requires_real_group_frame_module_and_complete_size(self):
        code = " 1527:1F7A 01F4 C=CODE S=BULLET_A_TEXT G=MAIN_03 M=unit.asm ACBP=48\n"
        data = " 209D:0000 C4C8 C=DATA S=_DATA G=DGROUP M=bindings.asm ACBP=48\n"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "units.map"
            path.write_text(code + data)
            self.assertEqual(asm.map_scope(path, self.entry), 0x171EA)
            asm.map_ds(path, 0x209D0)
            for bad in (code * 2, code.replace("01F4", "01F3"), code.replace("MAIN_03", "MAIN_01"),
                        code.replace("1527:", "1528:"), code.replace("unit.asm", "bindings.asm")):
                path.write_text(bad + data)
                with self.subTest(bad=bad), self.assertRaises(ValueError):
                    asm.map_scope(path, self.entry)
            for bad in (data * 2, data.replace("209D:", "209E:"), data.replace("DGROUP", "OTHER")):
                path.write_text(code + bad)
                with self.subTest(bad=bad), self.assertRaises(ValueError):
                    asm.map_ds(path, 0x209D0)

    def test_per_owner_inputs_avoid_unrelated_replay(self):
        real = asm.producer_inputs
        def changed(entry):
            rows = copy.deepcopy(real(entry))
            if entry["id"] == self.entry["id"]:
                next(r for r in rows if r["path"] == entry["source"])["sha256"] = "0" * 64
            return rows
        with patch.object(asm, "producer_inputs", side_effect=changed):
            with self.assertRaises(ValueError):
                asm.check_record(self.records[self.entry["id"]], self.entry)
            other = self.entries["main-bullet-spawn-raw"]
            asm.check_record(self.records[other["id"]], other)
        # Verifier evolution is separate from actual assembler/semantic inputs.
        with patch.object(asm, "verifier_inputs", return_value=[{"path": "new.py", "sha256": "0" * 64}]):
            asm.check_record(self.records[self.entry["id"]], self.entry)

    def test_tables_and_all_uncredited_bytes_still_undergo_raw_gate(self):
        entry = self.entries["main-bullet-spawn-raw"]
        payload = bytearray(b"A" * entry["size"])
        original = image(payload)
        for offset in (178, 179, 193, 212, 393, 394, 405, 484, 493, 555, 556, 569):
            changed = payload.copy()
            changed[offset] ^= 1
            with self.subTest(offset=offset):
                self.assertFalse(compare_unit(original, image(changed), 0, 0, entry["size"])["raw_exact"])
        bad = copy.deepcopy(entry)
        bad["uncredited"].append({"offset": 394, "size": 2, "kind": "alignment"})
        with self.assertRaises(ValueError):
            asm.layout(bad)

    def test_native_tables_cannot_point_into_unknown_or_table_bytes(self):
        # Synthetic tiny original-ASM scope: RET, EVEN, one handler word.
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "native.json"
            body = b"\xc3\x90\0\0"
            proof = {"target_sha256": "a" * 64, "start": 0, "size": 4, "cs_base": 0,
                     "sha256": digest_bytes(body), "ordered_fixups": [],
                     "instructions": [{"address": 0, "bytes": "c3", "mnemonic": "ret"},
                                      {"address": 1, "bytes": "90", "mnemonic": "nop"}],
                     "tables": [{"offset": 2, "size": 2, "targets": [0]}]}
            entry = {"target_start": 0, "size": 4, "cs_base": 0, "target_scope_sha256": digest_bytes(body),
                     "fixups": [], "tables": [{"offset": 2, "size": 2}], "instruction_nops": [],
                     "uncredited": [{"offset": 1, "size": 1, "kind": "alignment"}]}
            def check(value, data=body):
                path.write_text(json.dumps(value))
                current = {**entry, "native_review_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                           "target_scope_sha256": digest_bytes(data)}
                asm.native_review(path, current, {"sha256": "a" * 64}, image(data))
            check(proof)
            bad = copy.deepcopy(proof)
            bad["instructions"].pop()
            with self.assertRaises(ValueError):
                check(bad)
            bad = copy.deepcopy(proof)
            bad["tables"][0]["targets"] = [3]
            data = b"\xc3\x90\3\0"
            bad["sha256"] = digest_bytes(data)
            with self.assertRaises(ValueError):
                check(bad, data)

    def test_own_negative_and_original_fixups_are_mandatory(self):
        for key, record in self.records.items():
            entry = self.entries[key]
            asm.check_record(record, entry)
            bad = copy.deepcopy(record)
            bad["negative_control"]["comparison"]["raw_exact"] = True
            with self.subTest(unit=key), self.assertRaises(ValueError):
                asm.check_record(bad, entry)
            bad = copy.deepcopy(record)
            bad["rounds"][0]["comparison"]["candidate_fixups"] = [1]
            with self.assertRaises(ValueError):
                asm.check_record(bad, entry)

    def test_semantic_keyboard_table_cannot_be_an_asset_or_arbitrary_words(self):
        model = {"offset": 1, "size": 24, "role": "piano-key-horizontal-positions",
                 "left": 400, "key_width": 4}
        expected = [400, 402, 404, 406, 408, 412, 414, 416, 418, 420, 422, 424]
        self.assertEqual(asm.semantic_table_values(model), expected)
        # Coordinates contain 90h bytes, which must never be decoded as NOPs.
        body = b"\xc3" + b"".join(v.to_bytes(2, "little") for v in expected)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "native.json"
            proof = {"target_sha256": "a" * 64, "start": 0, "size": 25, "cs_base": 0,
                     "sha256": digest_bytes(body), "ordered_fixups": [], "tables": [],
                     "instructions": [{"address": 0, "bytes": "c3", "mnemonic": "ret"}],
                     "semantic_tables": [{**model, "values": expected}]}
            entry = {"target_start": 0, "size": 25, "cs_base": 0,
                     "target_scope_sha256": digest_bytes(body), "fixups": [],
                     "tables": [], "semantic_tables": [model], "instruction_nops": [], "uncredited": []}
            def check(value, data=body):
                path.write_text(json.dumps(value))
                current = {**entry, "native_review_sha256": digest_bytes(path.read_bytes()),
                           "target_scope_sha256": digest_bytes(data)}
                asm.native_review(path, current, {"sha256": "a" * 64}, image(data))
            check(proof)
            self.assertEqual(asm.counts(entry)["instructions"], 1)
            self.assertEqual(asm.counts(entry)["semantic-code-table"], 24)
            bad = copy.deepcopy(proof)
            bad["semantic_tables"][0]["values"][1] += 1
            with self.assertRaises(ValueError):
                check(bad)
            changed = body[:3] + b"\x93" + body[4:]
            bad = copy.deepcopy(proof)
            bad["sha256"] = digest_bytes(changed)
            with self.assertRaises(ValueError):
                check(bad, changed)
            bad = {**entry, "semantic_tables": [{**model, "offset": 0}]}
            bad["uncredited"] = [{"offset": 0, "size": 1, "kind": "alignment"}]
            with self.assertRaises(ValueError):
                asm.layout(bad)
        for mutation in ({"role": "sprite-pixels"}, {"key_width": 3}, {"left": 65530}, {"size": 22}, {"values": expected}):
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                asm.semantic_table_values({**model, **mutation})

    def test_explicit_adoption_cannot_broaden_or_mask_scopes(self):
        views = tomllib.loads((asm.ROOT / "config/ownership.toml").read_text())["views"]
        claims, _ = asm.reviewed_claims(asm.ROOT, views)
        for entry in self.entries.values():
            rows = [r for r in claims[entry["artifact"]] if r["unit"] == entry["id"]]
            validate_partition(entry["size"], [{**r, "start": r["start"] - entry["target_start"],
                                                "end": r["end"] - entry["target_start"]} for r in rows])
        totals = {}
        for rows in claims.values():
            for row in rows:
                totals[row["kind"]] = totals.get(row["kind"], 0) + row["end"] - row["start"]
        self.assertEqual(totals, {"accepted-reviewed-asm-instructions": 4542,
                                 "accepted-reviewed-asm-dispatch-table": 92,
                                 "accepted-reviewed-asm-semantic-code-table": 24,
                                 "checked-uncredited-asm-alignment": 31,
                                 "checked-uncredited-asm-inert-branch": 6,
                                 "checked-uncredited-asm-runtime-placeholder": 10})
        decision = json.loads(asm.DECISION.read_text())
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / asm.DECISION.relative_to(asm.ROOT)
            path.parent.mkdir()
            bad = copy.deepcopy(decision)
            bad["units"][0]["acceptance_sha256"] = "0" * 64
            path.write_text(json.dumps(bad))
            with self.assertRaises(ValueError):
                asm.reviewed_claims(root, views)
            bad = copy.deepcopy(decision)
            bad["units"].append(bad["units"][0])
            path.write_text(json.dumps(bad))
            with self.assertRaises(ValueError):
                asm.reviewed_claims(root, views)

    def test_failed_batch_does_not_write_partial_acceptance(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "acceptance.json"
            before = json.dumps({"schema_version": 1, "units": {}})
            path.write_text(before)
            with patch.object(asm, "PUBLIC", path), patch.object(sys, "argv", ["replay", "--accept", "a", "--accept", "b"]), \
                    patch.object(asm, "validate_receipt", side_effect=[next(iter(self.records.values())), ValueError("stale source")]):
                with self.assertRaises(ValueError):
                    asm.main()
            self.assertEqual(path.read_text(), before)


if __name__ == "__main__":
    unittest.main()
