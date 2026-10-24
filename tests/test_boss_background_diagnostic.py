"""The diagnostic's foreign holes must follow actual compiler-owned CODE."""
from pathlib import Path
import struct
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from diagnose_boss_background import compiled_code_size, verify_layout, UNIT_START


def record(kind, data):
    raw = bytes([kind]) + struct.pack("<H", len(data) + 1) + data
    return raw + bytes([-sum(raw) & 255])


def object_bytes(extents=((0, b"abc"),), *, extra_data=0):
    names = (b"", b"BOSS_BG_TEXT", b"CODE", b"_DATA", b"DATA")
    return (record(0x80, b"\x05p.cpp") +
            record(0x96, b"".join(bytes([len(name)]) + name for name in names)) +
            record(0x98, b"\x28\x03\0\x02\x03\x01") +
            record(0x98, b"\x48" + struct.pack("<H", extra_data) + b"\x04\x05\x01") +
            b"".join(record(0xA0, b"\x01" + struct.pack("<H", offset) + data)
                     for offset, data in extents) + record(0x8A, b"\0"))


class BossBackgroundDiagnosticTests(unittest.TestCase):
    def test_size_comes_from_actual_segdef_not_original_extent(self):
        result = compiled_code_size(object_bytes())
        self.assertEqual(result["size"], 3)
        self.assertEqual(result["ledata_extents"], [(0, 3)])

    def test_missing_overlapping_or_additional_compiler_bytes_rejected(self):
        for raw in (object_bytes(((1, b"ab"),)), object_bytes(((0, b"ab"),)),
                    object_bytes(((0, b"ab"), (1, b"bc"))), object_bytes(extra_data=1)):
            with self.assertRaises(ValueError):
                compiled_code_size(raw)

    def test_even_and_odd_natural_sizes_keep_foreign_and_data_frames_fixed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "units.map"
            for size in (3253, 3254):
                rows = {
                    "_TEXT": (0, 0, 0xAE10),
                    "BOSS_BG_TEXT": (0xAE1, 0, UNIT_START - 0xAE10),
                    "BG_FOREIGN_TAIL": (0xAE1, UNIT_START + size - 0xAE10, 0x14AB0 - UNIT_START - size),
                    "SHARED": (0x14AB, 0, 0x3B0),
                    "BG_DGROUP_GAP": (0x14E6, 0, 0x209D0 - 0x14E60),
                    "_DATA": (0x209D, 0, 0xC692),
                }
                path.write_text("\n".join(
                    f" {frame:04X}:{offset:04X} {length:04X} C=CODE S={name} G=MAIN_01 M=bindings.asm"
                    for name, (frame, offset, length) in rows.items()))
                self.assertEqual(len(verify_layout(path, size)), 6)
                path.write_text(path.read_text().replace("209D:0000", "209E:0000"))
                with self.assertRaisesRegex(ValueError, "layout drift"):
                    verify_layout(path, size)


if __name__ == "__main__":
    unittest.main()
