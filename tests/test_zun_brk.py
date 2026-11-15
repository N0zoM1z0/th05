from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import review_zun_brk as brk


class ZunBrkTests(unittest.TestCase):
    def test_absolute_external_fixups_resolve_to_crt_data(self):
        source = bytes([0x90, 0x00, 0x00, 0x90])
        fixups = [{
            "site": 1, "relative": False, "target_method": 2,
            "target_index": 2, "frame_method": 5, "frame_index": None,
            "displacement": 0,
        }]
        config = {"external_targets": {"___brklvl": 0x16B0}}
        actual, rows = brk._resolve_code(source, fixups, config, ["_errno", "___brklvl"])
        self.assertEqual(actual[1:3], b"\xb0\x16")
        self.assertEqual(rows[0]["symbol"], "___brklvl")

    def test_unsupported_external_frame_is_rejected(self):
        source = bytes([0x90, 0, 0])
        fixups = [{
            "site": 1, "relative": False, "target_method": 2,
            "target_index": 2, "frame_method": 1, "frame_index": 2,
            "displacement": 0,
        }]
        config = {"external_targets": {"___brklvl": 0x16B0}}
        with self.assertRaises(ValueError):
            brk._resolve_code(source, fixups, config, ["_errno", "___brklvl"])

if __name__ == "__main__":
    unittest.main()
