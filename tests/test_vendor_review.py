"""Synthetic OMF/library/link proofs; no proprietary inputs or executable tools."""

import copy
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.borland_library import library_members
from lib.pc98 import parse_mz
from review_vendor import VendorReview, validate_metadata


def record(kind, payload):
    frame = bytes([kind]) + struct.pack("<H", len(payload) + 1) + payload
    return frame + bytes([-sum(frame) & 255])


def library(code, *, fixups=b"", ext=True, ledata=None, attributes=0x28):
    names = b"\x05_TEXT\x04CODE\x00"
    obj = record(0x80, b"\x06sample") + record(0x88, b"\0\xa3\x06sample")
    obj += record(0x96, names) + record(
        0x98, bytes([attributes]) + struct.pack("<H", len(code)) + b"\1\2\3"
    )
    if ext:
        obj += record(0x8C, b"\x07_callee\0")
    for offset, payload in ledata if ledata is not None else [(0, code)]:
        obj += record(0xA0, b"\1" + struct.pack("<H", offset) + payload)
    if fixups:
        obj += record(0x9C, fixups)
    obj += record(0x8A, b"\0")
    page = 16
    cursor = page + ((len(obj) + page - 1) // page) * page
    dictionary = cursor + page
    header = bytearray(page)
    header[0] = 0xF0
    struct.pack_into("<HIH", header, 1, page - 3, dictionary, 0)
    terminator = bytes([0xF1]) + struct.pack("<H", page - 3) + bytes(page - 3)
    return bytes(header) + obj + bytes(cursor - page - len(obj)) + terminator


def mz(body, relocations=()):
    header = bytearray(48)
    size = len(header) + len(body)
    struct.pack_into(
        "<14H",
        header,
        0,
        0x5A4D,
        size % 512,
        (size + 511) // 512,
        len(relocations),
        3,
        1,
        0xFFFF,
        0,
        16,
        0,
        0,
        0,
        28,
        0,
    )
    for index, site in enumerate(relocations):
        struct.pack_into("<HH", header, 28 + 4 * index, site, 0)
    result = parse_mz(bytes(header) + body)
    assert result.valid
    return result


def setup(
    code,
    linked=None,
    *,
    fixups=b"",
    address="0000:0010",
    relocs=(),
    ledata=None,
    attributes=0x28,
    repeat=False,
):
    linked = code if linked is None else linked
    body = bytearray(64)
    body[: len(linked)] = linked
    if repeat:
        body[32 : 32 + len(linked)] = linked
    text = (
        f" 00000H 0003FH 00040H _TEXT CODE\n"
        f" 0000:0000 {len(code):04X} C=CODE S=_TEXT G=(none) M=sample ACBP=28\n"
        f" {address} _callee\n"
    ).encode()
    image = mz(bytes(body), relocs)
    review = VendorReview(
        library(code, fixups=fixups, ledata=ledata, attributes=attributes),
        text,
        image,
        image,
    )
    return review, review.mods["sample"], review.contribs[0]


class VendorNativeTests(unittest.TestCase):
    def test_literal_complete_member_is_not_inferred_from_name(self):
        review, mod, con = setup(b"\x55\x8b\xec\xcb")
        result = review.verify(mod, con)
        self.assertTrue(result["complete_gapless_CODE_LEDATA"])
        self.assertEqual(result["ordered_MZ_fixups"], [])
        bad = copy.deepcopy(mod)
        bad["blocks"][0]["data"] = b"\x90" + bad["blocks"][0]["data"][1:]
        with self.assertRaisesRegex(ValueError, "reconstructed OMF/link bytes differ"):
            review.verify(bad, con)
        duplicate, mod, con = setup(b"\x55\x8b\xec\xcb", repeat=True)
        with self.assertRaisesRegex(ValueError, "nonunique"):
            duplicate.verify(mod, con)

    def test_library_checksum_and_directory_bounds_are_checked(self):
        raw = bytearray(library(b"abcd"))
        raw[20] ^= 1
        with self.assertRaisesRegex(ValueError, "checksum"):
            library_members(bytes(raw))
        raw = bytearray(library(b"abcd"))
        struct.pack_into("<I", raw, 3, len(raw) + 16)
        with self.assertRaisesRegex(ValueError, "dictionary"):
            library_members(bytes(raw))

    def test_complete_extent_cannot_hide_gap_overlap_or_absolute_segment(self):
        for blocks in [[(0, b"abc")], [(0, b"abcd"), (2, b"cd")], [(2, b"abcd")]]:
            with self.assertRaisesRegex(ValueError, "LEDATA"):
                review, mod, con = setup(b"abcd", ledata=blocks)
                review.verify(mod, con)
        with self.assertRaisesRegex(ValueError, "unsupported absolute"):
            setup(b"abcd", attributes=0)
        review, mod, con = setup(b"abcd")
        mod["records"]["LIDATA"] = 1
        with self.assertRaisesRegex(ValueError, "unsupported transformation"):
            review.verify(mod, con)

    def test_fixupp_threads_methods_and_cross_record_writes_reject(self):
        for fixups, message in [
            (b"\0", "thread"),
            (b"\xc4\x03\x56\1", "crosses LEDATA"),
            (b"\xc4\1\x36\1", "frame method"),
        ]:
            with self.subTest(fixups=fixups):
                with self.assertRaisesRegex(ValueError, message):
                    setup(b"abcd", fixups=fixups)
        review, mod, con = setup(b"abcdef", fixups=b"\xc4\1\x56\1\xc4\2\x56\1")
        with self.assertRaisesRegex(ValueError, "overlapping FIXUPP"):
            review.verify(mod, con)

    def test_far_call_rewrite_requires_real_binding_and_exact_opcode_bytes(self):
        # Original 9A far-call field becomes five bytes NOP/PUSHCS/CALL rel16.
        original = b"\x9a\0\0\0\0\xcb"
        linked = b"\x90\x0e\xe8\x0b\0\xcb"
        review, mod, con = setup(original, linked, fixups=b"\xcc\1\x56\1")
        result = review.verify(mod, con)
        self.assertEqual(
            result["fixup_actions"][0]["operation"],
            "TLINK same-segment far-call NOP/PUSHCS/CALL",
        )
        changed, mod, con = setup(
            original, linked, fixups=b"\xcc\1\x56\1", address="0000:0011"
        )
        with self.assertRaisesRegex(ValueError, "reconstructed OMF/link bytes differ"):
            changed.verify(mod, con)
        wrong = bytes([0x91]) + linked[1:]
        changed, mod, con = setup(original, wrong, fixups=b"\xcc\1\x56\1")
        with self.assertRaisesRegex(ValueError, "reconstructed OMF/link bytes differ"):
            changed.verify(mod, con)

    def test_real_segment_fixups_keep_original_order(self):
        code = b"\x9a\0\0\0\0\x9a\0\0\0\0\xcb"
        linked = b"\x9a\0\0\1\0\x9a\0\0\1\0\xcb"
        fix = b"\xcc\1\x56\1\xcc\6\x56\1"
        review, mod, con = setup(
            code, linked, fixups=fix, address="0001:0000", relocs=(3, 8)
        )
        self.assertEqual(review.verify(mod, con)["ordered_MZ_fixups"], [3, 8])
        review.target = mz(review.target.program_image, (8, 3))
        with self.assertRaisesRegex(ValueError, "target ordered MZ"):
            review.verify(mod, con)


class VendorPublicMetadataTests(unittest.TestCase):
    def metadata(self):
        return json.loads((ROOT / "config/vendor_ownership.json").read_text())

    def test_public_structure_check_needs_no_private_inputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative in (
                "scripts/review_vendor.py",
                "scripts/lib/borland_library.py",
                "config/toolchain.toml",
            ):
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes((ROOT / relative).read_bytes())
            self.assertEqual(
                validate_metadata(self.metadata(), root=root)["proposed_bytes"], 2901
            )
            (root / "scripts/review_vendor.py").write_text("# drift")
            with self.assertRaisesRegex(ValueError, "source drift"):
                validate_metadata(self.metadata(), root=root)

    def test_metadata_cannot_invent_boundaries_credit_or_relocation_order(self):
        base = self.metadata()
        for mutate in [
            lambda x: x.update(authored_credit=1),
            lambda x: x["contributions"][0].update(end=145959),
            lambda x: x["contributions"][1].update(
                start=x["contributions"][0]["start"]
            ),
        ]:
            bad = copy.deepcopy(base)
            mutate(bad)
            with self.assertRaises(ValueError):
                validate_metadata(bad)
        bad = copy.deepcopy(base)
        row = next(r for r in bad["contributions"] if len(r["ordered_MZ_fixups"]) > 1)
        row["ordered_MZ_fixups"].reverse()
        with self.assertRaisesRegex(ValueError, "ordered MZ"):
            validate_metadata(bad)
        bad = copy.deepcopy(base)
        bad["deferred"][0]["decision"] = "accepted"
        with self.assertRaisesRegex(ValueError, "deferred policy"):
            validate_metadata(bad)


if __name__ == "__main__":
    unittest.main()
