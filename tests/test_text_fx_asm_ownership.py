"""Reviewed ASM cannot absorb compiler code, resources or uncredited bytes."""
import copy
import json
from pathlib import Path
import struct
import sys
import tempfile
import tomllib
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from lib.pc98 import parse_mz, digest_file
from lib.unit_oracle import compare_unit
from ownership import overlay_asm, validate_partition
import replay_text_fx_render as render
import review_text_fx_asm as review


def record(kind, payload):
    raw = bytes([kind]) + struct.pack("<H", len(payload) + 1) + payload
    return raw + bytes([-sum(raw) & 255])


def fixture(*, partial=False, overlap=False, extra_data=False, producer="Turbo Assembler  Version 5.0"):
    names = ["SHARED", "CODE", "_DATA", "DATA", ""]
    raw = record(0x80, b"\x07fixture")
    raw += record(0x88, b"\0\0" + bytes([len(producer)]) + producer.encode())
    raw += record(0x96, b"".join(bytes([len(n)]) + n.encode() for n in names))
    raw += record(0x98, b"\x48" + struct.pack("<H", 346) + b"\1\2\5")
    raw += record(0x98, b"\x48" + struct.pack("<H", 8 if extra_data else 0) + b"\3\4\5")
    raw += record(0xA0, b"\1\0\0" + b"A" * (345 if partial else 346))
    if overlap:
        raw += record(0xA0, b"\1\0\0B")
    return raw + record(0x8A, b"\0")


class TextFxAssemblyOwnershipTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config, cls.data_config = review.configurations()
        cls.proof = json.loads((review.ROOT / review.PROOF).read_text())
        cls.decision = json.loads((review.ROOT / review.DECISION).read_text())

    def test_omf_requires_complete_code_and_no_resource_contribution(self):
        self.assertEqual(render.omf_scope(fixture(), self.config)["size"], 346)
        for patch in ({"partial": True}, {"overlap": True}, {"extra_data": True},
                      {"producer": "TC86 Borland C++ 4.02"}):
            with self.subTest(patch=patch), self.assertRaises(ValueError):
                render.omf_scope(fixture(**patch), self.config)

    def test_map_does_not_accept_prefix_wrong_group_or_foreign_module(self):
        profile = self.data_config["profiles"]["op"]
        good = " 0D30:0136 015A C=CODE S=SHARED G=(none) M=tfxcode.asm ACBP=48\n"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "units.map"
            path.write_text(good)
            self.assertEqual(render.map_scope(path, profile, self.config), 0xD436)
            for bad in (good * 2, good.replace("015A", "0159"), good.replace("(none)", "OTHER"),
                        good.replace("0136", "0137"), good.replace("tfxcode.asm", "bindings.asm")):
                path.write_text(bad)
                with self.subTest(bad=bad), self.assertRaises(ValueError):
                    render.map_scope(path, profile, self.config)

    def test_nops_and_runtime_placeholders_receive_exactly_reviewed_credit(self):
        result = render.classification(self.config)
        self.assertEqual(result["semantic_asm_instruction_bytes"], 339)
        self.assertEqual(result["checked_alignment_bytes"], 1)
        self.assertEqual(result["checked_runtime_patch_placeholder_bytes"], 6)
        for patch in ({"alignment_offsets": []}, {"runtime_patch_placeholder_ranges": []},
                      {"instruction_nops": []}, {"size": 345}):
            with self.subTest(patch=patch), self.assertRaises(ValueError):
                render.classification({**self.config, **patch})

    def test_even_and_dummy_bytes_are_never_masked_from_raw_comparison(self):
        body = bytearray(b"A" * 346)
        def image(payload):
            header = struct.pack("<14H", 0x5A4D, 378, 1, 0, 2, 0, 0xFFFF, 0, 16, 0, 0, 0, 28, 0)
            result = parse_mz(header.ljust(32, b"\0") + payload)
            self.assertTrue(result.valid)
            return result
        target = image(body)
        self.assertTrue(compare_unit(target, image(body), 0, 0, 346)["exact"])
        for offset in (222, 223, 293, 294, 299, 343, 344):
            changed = body.copy()
            changed[offset] ^= 1
            with self.subTest(offset=offset):
                self.assertFalse(compare_unit(target, image(changed), 0, 0, 346)["raw_exact"])

    def test_proposal_cannot_expand_ownership_or_promote_cxx_credit(self):
        review.validate_metadata(self.proof)
        for field, value in (("authored_asm_code_bytes", 692), ("authored_asm_data_bytes", 128),
                             ("cxx_authored_credit", 742), ("historical_source_recovered", True)):
            bad = copy.deepcopy(self.proof)
            bad[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                review.validate_metadata(bad)

    def test_explicit_decision_cannot_add_remove_or_duplicate_scopes(self):
        sha = digest_file(review.ROOT / review.PROOF)
        review.validate_decision(self.proof, self.decision, sha)
        for selection in (self.decision["units"][:-1], self.decision["units"] + ["zun-memory"],
                          self.decision["units"] + self.decision["units"][:1]):
            with self.subTest(selection=selection), self.assertRaises(ValueError):
                review.validate_decision(self.proof, {**self.decision, "units": selection}, sha)
        with self.assertRaises(ValueError):
            review.validate_decision(self.proof, self.decision, "0" * 64)

    def test_code_claims_cover_full_scope_without_crediting_exclusions(self):
        code = next(row for row in self.proof["units"] if row["id"] == "op-text-fx-code")
        claims = review.split_unit(code)
        shifted = [{**row, "start": row["start"] - code["start"], "end": row["end"] - code["start"]} for row in claims]
        validate_partition(346, shifted)
        totals = {}
        for row in claims:
            totals[row["kind"]] = totals.get(row["kind"], 0) + row["end"] - row["start"]
        self.assertEqual(totals, {"accepted-reviewed-asm-instructions": 339,
                                 "checked-uncredited-asm-alignment": 1,
                                 "checked-uncredited-asm-runtime-placeholder": 6})

    def test_overlay_preserves_unknown_resources_and_rejects_overlap(self):
        origin = "reviewed-native-handwritten-assembly-reconstruction"
        original = [{"start": 0, "end": 100, "kind": "unknown"}]
        claim = {"start": 10, "end": 20, "kind": "accepted-reviewed-asm-initialized-data",
                 "unit": "synthetic-data", "origin": origin}
        combined = overlay_asm(100, original, [claim])
        self.assertEqual([(r["start"], r["end"], r["kind"]) for r in combined],
                         [(0, 10, "unknown"), (10, 20, claim["kind"]), (20, 100, "unknown")])
        for patch in ({"kind": "accepted-cxx-instructions"}, {"origin": "inferred"}, {"end": 101}):
            with self.subTest(patch=patch), self.assertRaises(ValueError):
                overlay_asm(100, original, [{**claim, **patch}])
        with self.assertRaises(ValueError):
            overlay_asm(100, combined, [claim])

    def test_renderer_report_needs_two_complete_producers_and_own_negative(self):
        report = json.loads(render.PUBLIC.read_text())
        render.check_public(report, self.config, self.data_config)
        for field, value in (("size", 345), ("raw_exact", False), ("candidate_fixups", [1])):
            bad = copy.deepcopy(report)
            bad["profiles"]["op"]["rounds"][0]["comparison"][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                render.check_public(bad, self.config, self.data_config)
        bad = copy.deepcopy(report)
        bad["profiles"]["op"]["negative_control"]["comparison"]["raw_exact"] = True
        with self.assertRaises(ValueError):
            render.check_public(bad, self.config, self.data_config)


if __name__ == "__main__":
    unittest.main()
