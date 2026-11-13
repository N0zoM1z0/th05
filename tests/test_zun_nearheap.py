from pathlib import Path
import sys
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import review_zun_nearheap as nearheap


class ZunNearheapTests(unittest.TestCase):
    def test_absolute_data_and_relative_external_fixups_resolve(self):
        source = bytes([0x90, 0x02, 0x00, 0x00, 0x00, 0x90])
        fixups = [
            {"site": 1, "location_type": 1, "relative": False,
             "frame_method": 1, "frame_index": 1, "target_method": 0,
             "target_index": 2, "displacement": 0},
            {"site": 3, "location_type": 1, "relative": True,
             "frame_method": 0, "frame_index": 1, "target_method": 2,
             "target_index": 1, "displacement": 0},
        ]
        config = {"data_start_com": 0x2000, "code_start_com": 0x1000,
                  "external_targets": {"___brk": 0x1010}}
        actual, rows = nearheap._resolve_code(source, fixups, config, ["___brk"])
        self.assertEqual(actual[1:3], b"\x02\x20")
        self.assertEqual(actual[3:5], b"\x0b\x00")
        self.assertEqual([row["symbol"] for row in rows], ["_DATA", "___brk"])

    def test_wrong_external_or_frame_target_is_rejected(self):
        source = bytes([0x90, 0, 0])
        fixup = [{"site": 1, "location_type": 1, "relative": True,
                  "frame_method": 0, "frame_index": 1, "target_method": 2,
                  "target_index": 1, "displacement": 0}]
        config = {"data_start_com": 0x2000, "code_start_com": 0x1000,
                  "external_targets": {"___brk": 0x1010}}
        with self.assertRaises(ValueError):
            nearheap._resolve_code(source, [{**fixup[0], "frame_index": 2}], config, ["___brk"])
        with self.assertRaises(ValueError):
            nearheap._resolve_code(source, [{**fixup[0], "target_index": 2}], config, ["___brk"])

    def test_pinned_ctlib_module_relocates_to_original_zun_child(self):
        config = tomllib.loads((ROOT / "config/zun_nearheap.toml").read_text())
        record = nearheap.evidence(config)
        self.assertEqual(record["code"]["size"], 631)
        self.assertEqual(record["code"]["nonrelocation_bytes_exact"], 579)
        self.assertEqual(record["code"]["relocation_count"], 26)
        self.assertEqual(record["code"]["relocation_field_bytes"], 52)
        self.assertEqual(record["code"]["target_sha256"], record["code"]["relocated_sha256"])
        self.assertEqual(record["data"]["size"], 6)
        self.assertTrue(record["data"]["raw_exact"])
        self.assertEqual(record["externals"], ["___brk", "___sbrk"])
        self.assertTrue(record["negative_control"]["nonrelocation_instruction_flip_rejected"])
        self.assertTrue(record["negative_control"]["resolved_relocation_flip_rejected"])


if __name__ == "__main__":
    unittest.main()
