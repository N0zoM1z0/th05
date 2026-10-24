"""Negative controls for complete extent, fixup and MAP contribution checks."""
from pathlib import Path
import struct
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from lib.pc98 import parse_mz
from lib.unit_oracle import compare_unit, map_contribution


def fixture(relocation: bool = False, mutation: bool = False):
    header = struct.pack("<14H", 0x5a4d, 48, 1, int(relocation), 2,
                         1, 0xffff, 0, 16, 0, 0, 0, 28, 0)
    table = struct.pack("<HH", 2, 0) if relocation else bytes(4)
    body = bytes([int(mutation)]) + bytes(15)
    return parse_mz(header + table + body)


class OracleTests(unittest.TestCase):
    def test_raw_equality_and_changed_byte(self):
        self.assertTrue(compare_unit(fixture(), fixture(), 0, 0, 16)["exact"])
        self.assertFalse(compare_unit(fixture(), fixture(mutation=True), 0, 0, 16)["exact"])

    def test_same_bytes_different_fixups_rejected(self):
        result = compare_unit(fixture(True), fixture(False), 0, 0, 16)
        self.assertTrue(result["raw_exact"])
        self.assertFalse(result["exact"])

    def test_truncated_extent_rejected(self):
        with self.assertRaises(ValueError):
            compare_unit(fixture(), fixture(), 0, 0, 17)

    def test_boundary_splitting_fixup_rejected(self):
        with self.assertRaises(ValueError):
            compare_unit(fixture(True), fixture(True), 3, 3, 10)

    def test_map_exact_module_and_segment(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "unit.map"
            path.write_text(" 1000:0020 001E C=CODE S=PLAYER_A_TEXT G=MAIN_03 M=th05/player_a.cpp ACBP=28\n")
            self.assertEqual(map_contribution(path, "th05/player_a.cpp", "PLAYER_A_TEXT"), (0x10020, 30))
            with self.assertRaises(ValueError):
                map_contribution(path, "wrong.cpp", "PLAYER_A_TEXT")
            path.write_text(path.read_text() * 2)
            with self.assertRaises(ValueError):
                map_contribution(path, "th05/player_a.cpp", "PLAYER_A_TEXT")


if __name__ == "__main__":
    unittest.main()
