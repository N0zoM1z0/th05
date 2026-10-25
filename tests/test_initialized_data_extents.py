"""Opt-in semantic initializer boundaries. No core oracle changes or tools."""

import copy
from pathlib import Path
import struct
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from lib.unit_extents import (
    classify_data_extent,
    data_map_scope,
    initialized_data_omf_scope,
    unit_extent_kind,
    validate_data_scope_evidence,
)
from lib.pc98 import parse_mz
from lib.unit_oracle import compare_unit
from progress import validate_control


def entry():
    return {
        "id": "semantic-data",
        "source": "src/owner.cpp",
        "module": "th05/owner.cpp",
        "segment": "_DATA",
        "size": 8,
        "target_start": 0x1100,
        "functions": 0,
        "extent_kind": "initialized-data",
        "origin": "compiler-generated-cxx",
        "data_semantics": ["state", "filenames", "function-pointers"],
    }


def record(kind, data):
    body = bytes([kind]) + struct.pack("<H", len(data) + 1) + data
    return body + bytes([-sum(body) & 255])


def omf(*, class_name="DATA", chunks=None, size=8, duplicate_segment=False, extra=b""):
    # One code contribution and one complete actual DATA contribution. CODE
    # bytes are irrelevant to DATA proof and can differ independently.
    names = (
        b"\x05_TEXT\x04CODE\x05_DATA"
        + bytes([len(class_name)])
        + class_name.encode()
        + b"\x00"
    )
    out = record(0x80, b"\x05owner") + record(0x96, names)
    out += record(0x98, b"\x28\x01\x00\1\2\5")
    out += record(0x98, b"\x48" + struct.pack("<H", size) + b"\3\4\5")
    if duplicate_segment:
        out += record(0x98, b"\x48" + struct.pack("<H", size) + b"\3\4\5")
    out += record(0xA0, b"\1\0\0\xcb")
    for offset, payload in chunks if chunks is not None else [(0, b"\x01\x00name\0\0")]:
        out += record(0xA0, b"\2" + struct.pack("<H", offset) + payload)
    return out + extra + record(0x8A, b"\0")


class InitializedDataExtentTests(unittest.TestCase):
    def test_data_control_must_change_data_and_keep_original_fixup_order(self):
        def image(*, change_data=False, change_code=False, reverse=False):
            body = bytearray(32)
            body[0] = 0xC3 if change_code else 0xCB
            body[16:28] = b"\0" * 8 + (b"cfh\0" if change_data else b"cfg\0")
            sites = (18, 22) if reverse else (22, 18)
            header = struct.pack(
                "<14H", 0x5A4D, 80, 1, 2, 3, 1, 0xFFFF, 0, 16, 0, 0, 0, 28, 0
            )
            header += b"".join(struct.pack("<HH", site, 0) for site in sites)
            result = parse_mz(header.ljust(48, b"\0") + body)
            self.assertTrue(result.valid)
            return result

        target = image()
        positive = compare_unit(target, image(), 16, 16, 12)
        self.assertTrue(positive["exact"])
        self.assertEqual(positive["target_fixups"], [6, 2])
        negative = compare_unit(target, image(change_data=True), 16, 16, 12)
        validate_control(negative)
        self.assertEqual(
            target.program_image[:16], image(change_data=True).program_image[:16]
        )
        code_only = compare_unit(target, image(change_code=True), 16, 16, 12)
        with self.assertRaisesRegex(ValueError, "negative control was not rejected"):
            validate_control(code_only)
        reordered = compare_unit(target, image(reverse=True), 16, 16, 12)
        self.assertTrue(reordered["raw_exact"])
        self.assertFalse(reordered["fixups_exact"])
        self.assertFalse(reordered["exact"])

    def test_saved_data_scope_cannot_hide_partial_or_wrong_class_evidence(self):
        value = entry()
        scope = initialized_data_omf_scope(omf(), value)
        comparison = {
            "size": 8,
            "candidate_start": 0x1100,
            "map_scope": {
                "kind": "complete-initialized-data-contribution",
                "map_class": "DATA",
                "start": 0x1100,
                "size": 8,
                "module": value["module"],
                "segment": "_DATA",
            },
        }
        validate_data_scope_evidence(value, comparison, scope)
        for patch in ({"map_class": "BSS"}, {"kind": "complete-function"}, {"size": 7}):
            bad = copy.deepcopy(comparison)
            bad["map_scope"].update(patch)
            with self.assertRaisesRegex(ValueError, "DATA MAP evidence"):
                validate_data_scope_evidence(value, bad, scope)
        bad = copy.deepcopy(scope)
        bad["ledata"][0]["size"] = 7
        with self.assertRaisesRegex(ValueError, "incomplete"):
            validate_data_scope_evidence(value, comparison, bad)
        bad = copy.deepcopy(scope)
        bad["ledata"] *= 2
        with self.assertRaisesRegex(ValueError, "bounds/hash"):
            validate_data_scope_evidence(value, comparison, bad)

    def test_old_code_identity_does_not_need_new_fields(self):
        self.assertEqual(unit_extent_kind({"size": 8}), "code")
        self.assertNotIn("extent_kind", {"size": 8})

    def test_c_initializers_keep_complete_data_and_zero_function_gates(self):
        value = {**entry(), "origin": "compiler-generated-c-semantic-data",
                 "source": "src/owner.c", "module": "th05/owner.c"}
        self.assertEqual(unit_extent_kind(value), "initialized-data")
        self.assertEqual(initialized_data_omf_scope(omf(), value)["size"], 8)
        for patch in ({"extent_kind": "code"}, {"functions": 1},
                      {"source": "src/owner.cpp"}, {"module": "th05/owner.cpp"}):
            with self.subTest(patch=patch), self.assertRaises(ValueError):
                unit_extent_kind({**value, **patch})
        # Changing producer language cannot bypass incomplete archive bytes.
        with self.assertRaises(ValueError):
            initialized_data_omf_scope(omf(chunks=[(0, b"name\0")]), value)

    def test_semantic_data_counts_do_not_inflate_code_or_functions(self):
        value = entry()
        result = classify_data_extent(value)
        self.assertEqual(
            result,
            {
                "authored_code_bytes": 0,
                "code_data_bytes": 0,
                "instruction_bytes": 0,
                "padding_bytes": 0,
                "authored_data_bytes": 8,
                "authored_bytes": 8,
            },
        )
        value["padding_bytes"] = [{"offset": 7, "value": 0}]
        self.assertEqual(
            classify_data_extent(value, target_bytes=b"\1\0name\0\0")[
                "authored_data_bytes"
            ],
            7,
        )
        with self.assertRaisesRegex(ValueError, "padding disagrees"):
            classify_data_extent(value, target_bytes=b"\1\0name\0\1")
        value["padding_bytes"] *= 2
        with self.assertRaisesRegex(ValueError, "duplicate"):
            classify_data_extent(value)

    def test_code_tables_assets_bss_and_function_slices_are_rejected(self):
        for patch in [
            {"extent_kind": "bss"},
            {"functions": 1},
            {"functions": False},
            {"function_symbol": "some_function()"},
            {"function_end_symbol": "next()"},
            {
                "code_data_ranges": [
                    {"offset": 0, "size": 8, "kind": "compiler-switch-table"}
                ]
            },
            {"alignment_offsets": [0]},
            {"alignment_offsets": None},
            {"data_semantics": ["assets"]},
            {"data_semantics": ["raw-byte-payload"]},
            {"data_semantics": []},
            {"data_semantics": ["state", "state"]},
            {"origin": "asset-derived"},
        ]:
            value = {**entry(), **patch}
            with self.subTest(patch=patch):
                with self.assertRaises(ValueError):
                    unit_extent_kind(value)

    def test_actual_map_class_and_complete_contribution_are_required(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "units.map"
            line = " 0100:0100 0008 C={} S=_DATA G=DGROUP M=th05/owner.cpp ACBP=48\n"
            path.write_text(line.format("DATA"))
            scope = data_map_scope(path, entry())
            self.assertEqual(scope["kind"], "complete-initialized-data-contribution")
            self.assertEqual(
                (scope["start"], scope["size"], scope["map_class"]), (0x1100, 8, "DATA")
            )
            for cl in ("BSS", "CODE", "CONST"):
                path.write_text(line.format(cl))
                with self.assertRaisesRegex(ValueError, "C=DATA"):
                    data_map_scope(path, entry())
            path.write_text(line.format("DATA") * 2)
            with self.assertRaisesRegex(ValueError, "one complete"):
                data_map_scope(path, entry())

    def test_omf_proves_real_initialized_bytes_not_map_names_only(self):
        scope = initialized_data_omf_scope(omf(), entry())
        self.assertEqual(
            (scope["segment_index"], scope["class"], scope["size"]), (2, "DATA", 8)
        )
        for raw in [
            omf(class_name="BSS"),
            omf(class_name="CODE"),
            omf(duplicate_segment=True),
        ]:
            with self.assertRaisesRegex(ValueError, "real compiler initialized DATA"):
                initialized_data_omf_scope(raw, entry())
        for chunks in [
            [(0, b"1234")],
            [(0, b"12345678"), (4, b"5678")],
            [(4, b"12345678")],
        ]:
            with self.subTest(chunks=chunks):
                with self.assertRaisesRegex(ValueError, "unwritten|overlaps|escapes"):
                    initialized_data_omf_scope(omf(chunks=chunks), entry())
        with self.assertRaisesRegex(ValueError, "size disagrees"):
            initialized_data_omf_scope(omf(size=9), entry())

    def test_unproved_lidata_or_patch_transform_is_not_ignored(self):
        for kind in (0xA2, 0xB2, 0xC2, 0x9D):
            with self.subTest(record=kind):
                with self.assertRaisesRegex(ValueError, "unsupported initialized DATA"):
                    initialized_data_omf_scope(omf(extra=record(kind, b"\0")), entry())
        raw = bytearray(omf())
        raw[8] ^= 1
        with self.assertRaisesRegex(ValueError, "checksum"):
            initialized_data_omf_scope(bytes(raw), entry())


if __name__ == "__main__":
    unittest.main()
