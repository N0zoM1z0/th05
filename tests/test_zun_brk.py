from pathlib import Path
import sys
import tomllib
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

    def test_pinned_ctlib_brk_module_relocates_and_links_to_nearheap(self):
        config = tomllib.loads((ROOT / "config/zun_brk.toml").read_text())
        record = brk.evidence(config)
        self.assertEqual(record["code"]["size"], 127)
        self.assertEqual(record["code"]["nonrelocation_bytes_exact"], 117)
        self.assertEqual(record["code"]["relocation_count"], 5)
        self.assertEqual(record["code"]["relocation_field_bytes"], 10)
        self.assertEqual(record["code"]["target_sha256"], record["code"]["relocated_sha256"])
        self.assertEqual(record["publics"]["___brk"], 0)
        self.assertEqual(record["publics"]["___sbrk"], 38)
        self.assertEqual(record["externals"], ["_errno", "___brklvl"])
        self.assertTrue(record["negative_control"]["nonrelocation_instruction_flip_rejected"])
        self.assertTrue(record["negative_control"]["resolved_relocation_flip_rejected"])


if __name__ == "__main__":
    unittest.main()
