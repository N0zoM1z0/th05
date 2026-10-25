"""The VM ASM lane must retain complete scope, native ABI and all zero-credit bytes."""
import copy
import json
from pathlib import Path
import struct
import sys
import tempfile
import tomllib
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import replay_enemy_vm as vm
from lib.pc98 import parse_mz
from lib.unit_oracle import compare_unit
from ownership import validate_partition


def record(kind, payload):
    raw = bytes([kind]) + struct.pack("<H", len(payload) + 1) + payload
    return raw + bytes([-sum(raw) & 255])


def fixture(*, partial=False, overlap=False, extra=False, producer="Turbo Assembler  Version 5.0"):
    names = ["ENEMY_VM_TEXT", "CODE", "_DATA", "DATA", ""]
    raw = record(0x80, b"\x07fixture")
    raw += record(0x88, b"\0\0" + bytes([len(producer)]) + producer.encode())
    raw += record(0x96, b"".join(bytes([len(n)]) + n.encode() for n in names))
    raw += record(0x98, b"\x28" + struct.pack("<H", 1252) + b"\1\2\5")
    raw += record(0x98, b"\x48" + struct.pack("<H", 1 if extra else 0) + b"\3\4\5")
    raw += record(0xA0, b"\1\0\0" + b"A" * 1024)
    raw += record(0xA0, b"\1\0\4" + b"B" * (227 if partial else 228))
    if overlap:
        raw += record(0xA0, b"\1\0\0A")
    return raw + record(0x8A, b"\0")


class EnemyVmAssemblyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = tomllib.loads(vm.CONFIG.read_text())
        cls.accepted = json.loads(vm.PUBLIC.read_text())
        cls.views = tomllib.loads((vm.ROOT / "config/ownership.toml").read_text())["views"]

    def test_complete_ordinary_assembler_contribution(self):
        self.assertEqual(vm.omf_scope(fixture(), self.config)["size"], 1252)
        for patch in ({"partial": True}, {"overlap": True}, {"extra": True},
                      {"producer": "TC86 Borland C++ 4.02"}):
            with self.subTest(patch=patch), self.assertRaises(ValueError):
                vm.omf_scope(fixture(**patch), self.config)

    def test_actual_map_cannot_accept_prefix_foreign_group_or_alias_only(self):
        line = " 1527:011C 04E4 C=CODE S=ENEMY_VM_TEXT G=MAIN_03 M=script.asm ACBP=28\n"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "units.map"
            path.write_text(line)
            self.assertEqual(vm.map_scope(path, self.config), 0x1538C)
            for bad in (line * 2, line.replace("04E4", "04E3"), line.replace("MAIN_03", "MAIN_01"),
                        line.replace("011C", "011D"), line.replace("script.asm", "bindings.asm")):
                path.write_text(bad)
                with self.subTest(bad=bad), self.assertRaises(ValueError):
                    vm.map_scope(path, self.config)

    def test_dispatch_and_zero_credit_boundaries_cannot_expand(self):
        credit = vm.classification(self.config)
        self.assertEqual(credit["authored_asm_instruction_bytes"], 1130)
        self.assertEqual(credit["authored_asm_dispatch_table_bytes"], 118)
        self.assertEqual(credit["checked_alignment_bytes"] + credit["checked_inert_branch_bytes"], 4)
        for patch in ({"alignment_offsets": []}, {"dispatch_range": [1132, 1252]},
                      {"inert_branch_range": [1100, 1101]}, {"size": 1133}):
            with self.subTest(patch=patch), self.assertRaises(ValueError):
                vm.classification({**self.config, **patch})

    def test_full_raw_gate_still_covers_padding_inert_branch_and_table(self):
        body = bytearray(b"A" * 1252)
        def image(payload):
            size = 32 + len(payload)
            header = struct.pack("<14H", 0x5A4D, size % 512, (size + 511) // 512,
                                 0, 2, 0, 0xFFFF, 0, 16, 0, 0, 0, 28, 0)
            result = parse_mz(header.ljust(32, b"\0") + payload)
            self.assertTrue(result.valid)
            return result
        target = image(body)
        for offset in (103, 1100, 1101, 1133, 1250, 1251):
            changed = body.copy()
            changed[offset] ^= 1
            with self.subTest(offset=offset):
                self.assertFalse(compare_unit(target, image(changed), 0, 0, 1252)["exact"])

    def test_current_report_requires_full_ordered_producers_and_own_negative(self):
        vm.check_public(self.accepted, self.config)
        for field, value in (("size", 1251), ("raw_exact", False), ("candidate_fixups", []),
                             ("candidate_fixups", [908])):
            bad = copy.deepcopy(self.accepted)
            bad["rounds"][0]["comparison"][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                vm.check_public(bad, self.config)
        bad = copy.deepcopy(self.accepted)
        bad["negative_control"]["comparison"]["raw_exact"] = True
        with self.assertRaises(ValueError):
            vm.check_public(bad, self.config)

    def test_explicit_adoption_and_gapless_separate_table_accounting(self):
        claims, _ = vm.reviewed_claims(vm.ROOT, self.views)
        rows = claims["main"]
        shifted = [{**row, "start": row["start"] - 0x1538C, "end": row["end"] - 0x1538C} for row in rows]
        validate_partition(1252, shifted)
        totals = {}
        for row in rows:
            totals[row["kind"]] = totals.get(row["kind"], 0) + row["end"] - row["start"]
        self.assertEqual(totals, {"accepted-reviewed-asm-instructions": 1130,
                                 "accepted-reviewed-asm-dispatch-table": 118,
                                 "checked-uncredited-asm-alignment": 2,
                                 "checked-uncredited-asm-inert-branch": 2})
        decision = json.loads(vm.DECISION.read_text())
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / vm.DECISION.relative_to(vm.ROOT)
            path.parent.mkdir()
            for patch in ({"unit": "main-enemy-vm-prefix"}, {"authored_instruction_bytes": 1252},
                          {"cxx_authored_credit": 1248}, {"authored_dispatch_table_bytes": 120}):
                path.write_text(json.dumps({**decision, **patch}))
                with self.subTest(patch=patch), self.assertRaises(ValueError):
                    vm.reviewed_claims(root, self.views)


if __name__ == "__main__":
    unittest.main()
