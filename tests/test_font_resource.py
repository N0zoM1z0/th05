import copy
import json
from pathlib import Path
import struct
import sys
import tempfile
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import review_font_resource as fonts
from lib.targets import find_artifact, load_target_manifest
from ownership import overlay_resources, partition


class FontResourceTests(unittest.TestCase):
    def setUp(self):
        self.meta = json.loads((ROOT / fonts.PROOF).read_text())
        self.decision = json.loads((ROOT / fonts.DECISION).read_text())
        self.view = tomllib.loads((ROOT / "config/ownership.toml").read_text())["views"]["zun"]
        self.target = find_artifact(load_target_manifest(ROOT / "config/targets.toml"), "th05-zun")

    def bitmap(self):
        # Synthetic numbered words identify display rows and tile columns.
        # No game bitmap or font pixels are included in this fixture.
        data = bytearray(62 + 8192)
        data[:2] = b"BM"
        struct.pack_into("<III", data, 2, len(data), 0, 62)
        struct.pack_into("<IiiHHII", data, 14, 40, 256, 256, 1, 1, 0, 8192)
        for display_row in range(256):
            for column in range(16):
                offset = 62 + (255 - display_row) * 32 + column * 2
                struct.pack_into("<H", data, offset, display_row * 16 + column)
        return bytes(data)

    def test_complete_bottom_up_bmp_becomes_row_major_glyphs_without_inversion(self):
        result = fonts.bitmap_tiles(self.bitmap())
        self.assertEqual(len(result), 8192)
        # First/last rows in top-left, top-right and bottom-right glyphs.
        for glyph, row, expected in ((0, 0, 0), (0, 15, 240), (15, 0, 15),
                                     (16, 0, 256), (255, 0, 3855), (255, 15, 4095)):
            self.assertEqual(struct.unpack_from("<H", result, glyph * 32 + row * 2)[0], expected)
        self.assertEqual(sorted(struct.unpack("<4096H", result)), list(range(4096)))

    def test_wrong_bitmap_geometry_compression_offset_and_missing_pixels_fail(self):
        for offset, fmt, value in ((10, "I", 64), (14, "I", 108), (18, "i", 512),
                                   (22, "i", -256), (26, "H", 2), (28, "H", 8),
                                   (30, "I", 1), (34, "I", 4096)):
            raw = bytearray(self.bitmap())
            struct.pack_into("<" + fmt, raw, offset, value)
            with self.subTest(offset=offset), self.assertRaises(ValueError):
                fonts.bitmap_tiles(raw)
        for raw in (b"", self.bitmap()[:-1], self.bitmap() + b"\0"):
            with self.assertRaises(ValueError):
                fonts.bitmap_tiles(raw)

    def test_public_metadata_and_decision_need_no_private_game_or_bitmap(self):
        fonts.validate_metadata(self.meta, self.view, self.target)
        fonts.validate_decision(self.decision, self.meta, fonts.sha((ROOT / fonts.PROOF).read_bytes()))
        claims, digest = fonts.reviewed_claims(ROOT, {"zun": self.view})
        self.assertEqual(len(digest), 64)
        self.assertEqual(claims["zun"][0]["authored_credit"], 0)
        self.assertEqual(claims["zun"][0]["instruction_bytes"], 0)
        self.assertEqual(claims["zun"][0]["end"] - claims["zun"][0]["start"], 8192)

    def test_unregistered_model_credit_geometry_or_container_coordinate_fails(self):
        mutations = [dict(model="opaque-bank"), dict(artifact="th05-main"),
                     dict(authored_credit=8192), dict(authored_credit=False),
                     dict(authored_denominator=8192), dict(target_sha256="0" * 64),
                     dict(bitmap_start=self.meta["bitmap_start"] - 1),
                     dict(bitmap_end=self.meta["bitmap_end"] + 1),
                     dict(member_start=True), dict(instruction_nops=[1]),
                     dict(ordered_fixups=[0]), dict(required_entry_df=1)]
        geometry = copy.deepcopy(self.meta["geometry"])
        geometry["bits_per_pixel"] = True
        mutations.append(dict(geometry=geometry))
        for changed in mutations:
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                fonts.validate_metadata({**self.meta, **changed}, self.view, self.target)

    def test_stale_verifier_or_escape_path_cannot_be_adopted(self):
        for name, changed in (("verifier", {"sha256": "0" * 64}),
                              ("independent_review", {"path": "../outside.json"}),
                              ("launcher_parser", {"path": "/outside.py"})):
            meta = copy.deepcopy(self.meta)
            meta[name].update(changed)
            with self.subTest(name=name), self.assertRaises(ValueError):
                fonts.validate_metadata(meta, self.view, self.target)

    def test_missing_wrong_or_overbroad_decision_cannot_classify_resource(self):
        digest = fonts.sha((ROOT / fonts.PROOF).read_bytes())
        for changed in (dict(scopes=[]), dict(scopes=["zun-cg-font", "other-child"]),
                        dict(evidence_sha256="0" * 64), dict(authored_credit=1),
                        dict(authored_credit=False), dict(authored_denominator=8192),
                        dict(other_scopes_policy="vendor")):
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                fonts.validate_decision({**self.decision, **changed}, self.meta, digest)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.assertEqual(fonts.reviewed_claims(root, {}), ({}, None))
            (root / "config").mkdir()
            (root / fonts.PROOF).write_text("{}")
            with self.assertRaises(ValueError):
                fonts.reviewed_claims(root, {})

    def claim(self, **changes):
        return {"start": 1000, "end": 9192, "kind": "reviewed-embedded-font-bitmap",
                "resource": "zun-cg-font", "model": fonts.MODEL,
                "instruction_bytes": 0, "authored_credit": 0, **changes}

    def test_resource_overlay_preserves_unknown_neighbors_and_source_credit(self):
        source = {"id": "source", "target_start": 12000, "size": 5}
        result = overlay_resources(15000, partition(15000, [source]), [self.claim()])
        self.assertEqual([(r["start"], r["end"], r["kind"]) for r in result], [
            (0, 1000, "unknown"), (1000, 9192, "reviewed-embedded-font-bitmap"),
            (9192, 12000, "unknown"), (12000, 12005, "accepted-cxx-instructions"),
            (12005, 15000, "unknown")])
        self.assertEqual(result[3]["unit"], "source")

    def test_resource_cannot_replace_code_tables_padding_or_other_resource(self):
        source = {"id": "source", "target_start": 1000, "size": 8,
                  "alignment_offsets": [7], "code_data_ranges": [
                      {"offset": 4, "size": 2, "kind": "compiler-switch-table"}]}
        pieces = partition(15000, [source])
        for start in (1000, 1004, 1007):
            with self.subTest(start=start), self.assertRaises(ValueError):
                overlay_resources(15000, pieces, [self.claim(start=start, end=start + 8192)])
        with self.assertRaises(ValueError):
            overlay_resources(15000, partition(15000, []), [self.claim(), self.claim()])

    def test_resource_overlay_rejects_partial_extent_and_any_authored_credit(self):
        for changes in (dict(authored_credit=1), dict(authored_credit=False),
                        dict(instruction_bytes=8192), dict(kind="accepted-cxx-instructions"),
                        dict(start=-1), dict(start=True), dict(end=9191), dict(end=15001)):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                overlay_resources(15000, partition(15000, []), [self.claim(**changes)])


if __name__ == "__main__":
    unittest.main()
