"""Public synthetic controls for launcher bounds, integrity and physical ownership."""

from pathlib import Path
import hashlib
import struct
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from lib.launcher import LauncherError, parse_launcher


def synthetic_launcher() -> tuple[bytes, dict]:
    """Build two synthetic records using the documented on-disk field layout."""
    stub = bytearray(48)
    stub[:2] = bytes.fromhex("eb15")
    stub[23:28] = b"\xfc\x8b\x0e" + struct.pack("<H", 0x130)
    names = b"-A      -B      " + b" " * (30 * 8)
    payloads = [b"synthetic program one", b"a different synthetic program two"]
    first = len(stub) + 327
    entries = [0x100 + first]
    for payload in payloads:
        entries.append(entries[-1] + len(payload))
    helper_start = entries[-1] - 0x100
    call_start = first - 3
    directory = struct.pack("<H", 2) + names + struct.pack("<33H", *entries, *([0] * 30))
    call = b"\xe8" + struct.pack("<h", helper_start - call_start - 3)
    inner = bytes(stub) + directory + call + b"".join(payloads) + bytes.fromhex("f3a458b8000150c3")
    copyright = b"comcstm (c)O.Morikawa 1996"
    usage = b"Synthetic help\r\n"
    header_size = 13 + len(copyright)
    inner_start = header_size + len(usage)
    inner_end = inner_start + len(inner)
    header = b"\xe9" + struct.pack("<hHHHI", inner_end - 3, header_size + 0x100,
                                  len(usage), len(inner), 0x2579af64) + copyright
    data = header + usage + inner + b"synthetic-outer-wrapper".ljust(68, b"!")
    return data, {"inner": inner_start, "stub": len(stub),
                  "names": inner_start + len(stub) + 2,
                  "entries": inner_start + len(stub) + 258,
                  "call": inner_start + call_start,
                  "helper": inner_start + helper_start,
                  "payload": inner_start + first}


class LauncherTests(unittest.TestCase):
    def test_complete_partition_has_no_double_counted_embedded_carrier(self):
        data, _ = synthetic_launcher()
        report = parse_launcher(data, expected_sha256=hashlib.sha256(data).hexdigest())
        self.assertEqual([p["name"] for p in report["payloads"]], ["-A", "-B"])
        self.assertEqual(sum(row["size"] for row in report["partition"]), len(data))
        self.assertEqual(len(report["partition"]), 8)
        self.assertTrue(all(row["origin"] == "unreviewed" for row in report["partition"]))
        for row in report["partition"]:
            self.assertEqual(row["sha256"], hashlib.sha256(
                data[row["file_start"]:row["file_end"]]).hexdigest())

    def test_payload_mutation_requires_pinned_whole_carrier_identity(self):
        data, locations = synthetic_launcher()
        changed = bytearray(data)
        changed[locations["payload"]] ^= 1
        with self.assertRaisesRegex(LauncherError, "SHA-256"):
            parse_launcher(bytes(changed), expected_sha256=hashlib.sha256(data).hexdigest())
        self.assertNotEqual(parse_launcher(data)["payloads"][0]["sha256"],
                            parse_launcher(bytes(changed))["payloads"][0]["sha256"])

    def test_overlapping_records_are_rejected(self):
        data, locations = synthetic_launcher()
        changed = bytearray(data)
        first = struct.unpack_from("<H", changed, locations["entries"])[0]
        struct.pack_into("<H", changed, locations["entries"] + 2, first)
        with self.assertRaisesRegex(LauncherError, "partition"):
            parse_launcher(bytes(changed))

    def test_unused_directory_slots_cannot_hide_another_record(self):
        data, locations = synthetic_launcher()
        for offset, value in [(locations["names"] + 16, ord("X")),
                              (locations["entries"] + 6, 1)]:
            with self.subTest(offset=offset):
                changed = bytearray(data)
                changed[offset] = value
                with self.assertRaisesRegex(LauncherError, "unused"):
                    parse_launcher(bytes(changed))

    def test_duplicate_dispatch_names_are_rejected(self):
        data, locations = synthetic_launcher()
        changed = bytearray(data)
        start = locations["names"]
        changed[start + 8:start + 16] = changed[start:start + 8]
        with self.assertRaisesRegex(LauncherError, "duplicate"):
            parse_launcher(bytes(changed))

    def test_outer_and_inner_transfers_must_reach_their_exact_helpers(self):
        data, locations = synthetic_launcher()
        for offset in (1, locations["call"] + 1, locations["helper"]):
            with self.subTest(offset=offset):
                changed = bytearray(data)
                changed[offset] ^= 1
                with self.assertRaises(LauncherError):
                    parse_launcher(bytes(changed))

    def test_truncation_and_directory_escape_are_rejected(self):
        data, locations = synthetic_launcher()
        for changed in (data[:-1], data[:locations["helper"]]):
            with self.assertRaises(LauncherError):
                parse_launcher(changed)
        changed = bytearray(data)
        struct.pack_into("<H", changed, locations["inner"] + 26, 0xffff)
        with self.assertRaisesRegex(LauncherError, "directory"):
            parse_launcher(bytes(changed))


if __name__ == "__main__":
    unittest.main()
