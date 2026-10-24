"""Authored credit must reject stale or internally inconsistent acceptance."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from progress import summarize


class ProgressTests(unittest.TestCase):
    def setUp(self):
        self.receipt = json.loads((ROOT / "config/accepted_units.json").read_text())

    def test_percentage_stays_unmeasured(self):
        result = summarize(ROOT, self.receipt)
        self.assertIsNone(result["percentage"])
        self.assertIsNone(result["authored_denominator"])
        self.assertEqual(result["instruction_bytes"], 91)
        self.assertEqual(result["complete_extent_bytes"], 96)

    def test_changed_raw_digest_rejected(self):
        self.receipt["units"][0]["result"]["rounds"][0]["candidate_sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            summarize(ROOT, self.receipt)

    def test_accepted_negative_control_rejected(self):
        self.receipt["compiled_negative_control"]["exact"] = True
        with self.assertRaises(ValueError):
            summarize(ROOT, self.receipt)

    def test_changed_source_digest_rejected(self):
        self.receipt["units"][0]["source_inputs"][0]["sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            summarize(ROOT, self.receipt)

    def test_missing_compiler_dependency_rejected(self):
        self.receipt["units"][0]["source_inputs"] = []
        with self.assertRaises(ValueError):
            summarize(ROOT, self.receipt)

    def test_wrong_target_and_toolchain_rejected(self):
        for key in ("target_sha256", "toolchain_manifest_sha256"):
            receipt = copy.deepcopy(self.receipt)
            receipt[key] = "0" * 64
            with self.assertRaises(ValueError):
                summarize(ROOT, receipt)

    def test_overlapping_credit_rejected(self):
        self.receipt["units"].append(copy.deepcopy(self.receipt["units"][0]))
        with self.assertRaises(ValueError):
            summarize(ROOT, self.receipt)


if __name__ == "__main__":
    unittest.main()
