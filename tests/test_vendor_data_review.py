import copy
import json
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from review_vendor_data import (ROOT, PROOF, data_template, reviewed_claims,
                                unique_data_match, validate_metadata)
from ownership import overlay_vendor


class VendorDataReviewTests(unittest.TestCase):
    def proof(self):
        return json.loads((ROOT / PROOF).read_text())

    def template(self):
        # Synthetic ordinary OMF payload; no proprietary input needed.
        return {"records": {"SEGDEF": 1, "LEDATA": 1},
                "segs": [None, {"name": "_DATA", "cl": "DATA", "size": 3}],
                "blocks": [{"segment": 1, "offset": 0, "data": b"abc"}], "fixups": []}

    def test_public_proof_is_current_and_has_no_authored_credit(self):
        proof = self.proof()
        validate_metadata(proof)
        self.assertEqual((proof["contribution_count"], proof["bytes"], proof["authored_credit"]),
                         (24, 1857, 0))

    def test_exact_library_and_calibration_boundaries_are_not_transferable(self):
        for field, value in (("start", 0), ("end", 1), ("size", 2),
                             ("calibration_start", 0), ("data_sha256", "0" * 64),
                             ("member_program_sha256", "0" * 64), ("context", "zun"),
                             ("segment", "_BSS")):
            proof = self.proof()
            proof["contributions"][0][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_metadata(proof)

    def test_relocated_or_partial_public_evidence_is_rejected(self):
        for field, value in (("ordered_fixups", [0]), ("omf_fixup_count", 1),
                             ("complete_ledatas", False), ("ledatas", [])):
            proof = self.proof()
            proof["contributions"][0][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_metadata(proof)
        for field, value in (("authored_credit", 1857), ("authored_denominator", 1857),
                             ("compiler_invocations", 2), ("decision", "ACCEPTED")):
            proof = self.proof()
            proof[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_metadata(proof)

    def test_duplicate_sources_and_stale_tool_identities_are_rejected(self):
        proof = self.proof()
        proof["contributions"][1] = copy.deepcopy(proof["contributions"][0])
        with self.assertRaises(ValueError):
            validate_metadata(proof)
        proof = self.proof()
        proof["identities"]["scripts/lib/omf.py"] = "0" * 64
        with self.assertRaises(ValueError):
            validate_metadata(proof)
        proof = self.proof()
        proof["targets"]["op"]["target_view"] = None
        with self.assertRaises(ValueError):
            validate_metadata(proof)

    def test_native_template_requires_gapless_unmodified_ledatas(self):
        self.assertEqual(data_template(self.template(), 1)[0], b"abc")
        for change in ("gap", "overlap", "outside", "fixup", "transformation", "bss"):
            mod = self.template()
            if change == "gap":
                mod["blocks"][0]["data"] = b"ab"
            elif change == "overlap":
                mod["blocks"].append(copy.deepcopy(mod["blocks"][0]))
            elif change == "outside":
                mod["blocks"][0]["offset"] = 1
            elif change == "fixup":
                mod["fixups"].append({"segment": 1})
            elif change == "transformation":
                mod["records"]["LIDATA"] = 1
            else:
                mod["segs"][1]["cl"] = "BSS"
            with self.subTest(change=change), self.assertRaises(ValueError):
                data_template(mod, 1)

    def test_native_whole_comparison_rejects_mutation_ambiguity_and_fixups(self):
        image = SimpleNamespace(program_image=b"--abc-", relocations=[])
        unique_data_match(image, b"abc", 2, 1)
        for body, raw, relocs, start in ((b"abd", image.program_image, [], 2),
                                       (b"abc", b"--abcabc", [], 2),
                                       (b"abc", image.program_image,
                                        [SimpleNamespace(linear=3)], 2),
                                       (b"abc", image.program_image, [], 0)):
            with self.subTest(raw=raw, start=start), self.assertRaises(ValueError):
                unique_data_match(SimpleNamespace(program_image=raw, relocations=relocs),
                                  body, start, 1)

    def test_reviewed_claims_retain_all_other_ownership_and_unknowns(self):
        proof = self.proof()
        views = {name: {"size": row["size"], "sha256": row["payload_sha256"]}
                 for name, row in proof["targets"].items()}
        claims, decision_sha = reviewed_claims(ROOT, views)
        self.assertEqual(len(decision_sha), 64)
        for name, rows in claims.items():
            self.assertEqual(len(rows), 8)
            self.assertEqual(sum(r["end"] - r["start"] for r in rows), 619)
            self.assertTrue(all(r["kind"] == "verified-vendor-initialized-data" for r in rows))
            size = views[name]["size"]
            partition = overlay_vendor(size, [{"start": 0, "end": size, "kind": "unknown"}], rows)
            self.assertEqual(sum(r["end"] - r["start"] for r in partition
                                 if r["kind"] == "unknown"), size - 619)
            # No reviewed vendor DATA may replace previously authored source.
            start = rows[0]["start"]
            with self.assertRaises(ValueError):
                overlay_vendor(size, [{"start": 0, "end": start, "kind": "unknown"},
                                      {"start": start, "end": start + 1,
                                       "kind": "accepted-cxx-instructions"},
                                      {"start": start + 1, "end": size, "kind": "unknown"}], rows)
        views["main"]["sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            reviewed_claims(ROOT, views)


if __name__ == "__main__":
    unittest.main()
