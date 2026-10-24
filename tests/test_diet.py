"""Decoder contracts with generated real-mode fixtures; no game files required."""

from dataclasses import replace
from pathlib import Path
import struct
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from lib.diet import DietError, DietPolicy, DietRun, Relocation, emulate_once, normalize_payload, observe, sha256, verify_runs


def fixture() -> tuple[bytes, DietPolicy]:
    """A tiny synthetic decoder restoring a relocated word and entry transfer.

    Its code lives above the decoded payload, as the real DIET stub does. It
    exercises the observed end/relocation/transfer protocol without using or
    redistributing any target bytes.
    """
    code = bytearray.fromhex("8cc8 2d0001 50 8ec0 26c70600001111 bf6000")
    code += bytes.fromhex("5d0e1f 012e8000 012e0000 eb00 b90100")
    final_cs_fixup = len(code) - 7  # word following second ADD's 01 2E
    code += bytes.fromhex("bb0000 26012f 89e8 8ed0 bc8000")
    jump_offset = len(code)
    code += bytes.fromhex("ea00000000")
    struct.pack_into("<H", code, final_cs_fixup, jump_offset + 3)
    module = bytearray(0x1100)
    module[0x1000:0x1000 + len(code)] = code
    file_size = len(module) + 32
    header = struct.pack("<14H", 0x5a4d, file_size % 512, (file_size + 511) // 512,
                         0, 2, 0, 0xffff, 0x100, 0x80, 0, 0, 0x100, 0x1c, 0)
    data = header + b"diet" + module
    return data, DietPolicy(sha256(data), 0x60, 1, 0)


class DietTests(unittest.TestCase):
    def test_relocation_roundtrip_and_bounds(self):
        relocations = (Relocation(0, 2, 2),)
        self.assertEqual(normalize_payload(b"ab\x11\x21", relocations, 0x1000), b"ab\x11\x11")
        for bad in (Relocation(0, -1, -1), Relocation(0, 3, 3), Relocation(1, 0, 2)):
            with self.assertRaises(DietError):
                normalize_payload(b"abcd", (bad,), 0x1000)

    def test_duplicate_load_segments_rejected(self):
        data, policy = fixture()
        with self.assertRaisesRegex(DietError, "distinct"):
            observe(data, policy, (0x1000, 0x1000))

    def test_modified_target_rejected_before_emulation(self):
        data, policy = fixture()
        with self.assertRaisesRegex(DietError, "SHA-256"):
            emulate_once(data[:-1] + b"x", policy, 0x1000)

    def test_missing_marker_rejected(self):
        data, policy = fixture()
        data = data[:0x1c] + b"nope" + data[0x20:]
        with self.assertRaisesRegex(DietError, "marker"):
            emulate_once(data, replace(policy, target_sha256=sha256(data)), 0x1000)

    def test_load_dependent_nonrelocation_change_rejected(self):
        a = DietRun(0x1000, b"abcd", (), 4, 100, 0x1000, 0, 0x1000, 0x80, 1, 0)
        b = replace(a, load_segment=0x3333, relocated_payload=b"abcx")
        with self.assertRaisesRegex(DietError, "decoded bytes"):
            verify_runs([a, b])

    def test_changed_relocation_stream_rejected(self):
        a = DietRun(0x1000, b"abcd", (), 4, 100, 0x1000, 0, 0x1000, 0x80, 1, 0)
        b = replace(a, load_segment=0x3333, relocations=(Relocation(0, 0, 0),))
        with self.assertRaisesRegex(DietError, "relocation stream"):
            verify_runs([a, b])


try:
    import unicorn
    HAS_UNICORN = unicorn.__version__ == "1.0.2"
except ImportError:
    HAS_UNICORN = False


@unittest.skipUnless(HAS_UNICORN, "requires optional pinned Unicorn 1.0.2")
class DecoderExecutionTests(unittest.TestCase):
    def test_two_loads_restore_complete_payload(self):
        data, policy = fixture()
        payload, runs = observe(data, policy)
        self.assertEqual(payload, b"\x11\x11" + bytes(0x5e))
        self.assertEqual(runs[0].relocations, (Relocation(0, 0, 0),))
        self.assertNotEqual(runs[0].relocated_payload, runs[1].relocated_payload)

    def test_wrong_output_extent_rejected(self):
        data, policy = fixture()
        with self.assertRaisesRegex(DietError, "output extent"):
            emulate_once(data, replace(policy, payload_size=0x61), 0x1000)

    def test_wrong_relocation_count_rejected(self):
        data, policy = fixture()
        with self.assertRaisesRegex(DietError, "relocation count"):
            emulate_once(data, replace(policy, relocation_count=2), 0x1000)

    def test_wrong_restored_stack_rejected(self):
        data, policy = fixture()
        with self.assertRaisesRegex(DietError, "restored stack"):
            emulate_once(data, replace(policy, initial_ss=1), 0x1000)

    def test_wrong_entry_rejected(self):
        data, policy = fixture()
        with self.assertRaisesRegex(DietError, "far transfer"):
            emulate_once(data, replace(policy, entry_ip=1), 0x1000)

    def test_instruction_budget_rejected(self):
        data, policy = fixture()
        with self.assertRaisesRegex(DietError, "instruction budget"):
            emulate_once(data, policy, 0x1000, max_instructions=3)


if __name__ == "__main__":
    unittest.main()
