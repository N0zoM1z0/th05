"""Explicit subset acceptance cannot promote a failed neighbour or hide bad evidence."""
import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from progress import (replay_entries_for_accept, select_accept_units,
                      validate_receipt_aggregate, validate_result)


def result(name="good", *, exact=True):
    fixups = [2, 8]
    comparison = {"target_start": 0, "candidate_start": 32, "size": 16,
                  "target_sha256": "a" * 64, "candidate_sha256": "a" * 64,
                  "target_fixups": fixups, "candidate_fixups": fixups if exact else list(reversed(fixups)),
                  "raw_exact": True, "fixups_exact": exact, "exact": exact}
    omf = {"dependency_timestamp_normalized_sha256": "object",
           "translator_comments": ["TC86 Borland C++ 4.02"]}
    return {"id": name, "exact": exact, "object_normalized_equal": True,
            "rounds": [comparison, copy.deepcopy(comparison)], "omfs": [omf, copy.deepcopy(omf)]}


class AcceptSubsetTests(unittest.TestCase):
    def setUp(self):
        self.results = {"good": result(), "blocked": result("blocked", exact=False)}
        self.control = {"exact": False, "raw_exact": False}
        self.entry = {"id": "blocked", "size": 16, "target_start": 0}

    def test_explicit_subset_accepts_only_real_exact_result_with_control_owner(self):
        self.assertEqual(select_accept_units(self.results, ["good"], "good"), {"good"})
        self.assertFalse(validate_receipt_aggregate({"pass": False}, self.results, self.control))

    def test_default_remains_all_or_nothing(self):
        with self.assertRaisesRegex(ValueError, "exact real replay"):
            select_accept_units(self.results, None, "good")

    def test_unknown_duplicate_empty_and_failed_requested_units_rejected(self):
        for selected in (["missing"], ["good", "good"], [], ["good", "blocked"]):
            with self.subTest(selected=selected), self.assertRaises(ValueError):
                select_accept_units(self.results, selected, "good")

    def test_negative_control_owner_must_belong_to_subset(self):
        self.results["other"] = result("other")
        with self.assertRaisesRegex(ValueError, "negative-control owner"):
            select_accept_units(self.results, ["other"], "good")

    def test_lying_aggregate_cannot_be_used_for_subset_import(self):
        with self.assertRaisesRegex(ValueError, "aggregate pass"):
            validate_receipt_aggregate({"pass": True}, self.results, self.control)
        with self.assertRaisesRegex(ValueError, "aggregate pass"):
            validate_receipt_aggregate({"pass": False}, {"good": self.results["good"]}, self.control)
        with self.assertRaises(ValueError):
            validate_receipt_aggregate({"pass": 0}, self.results, self.control)

    def test_unselected_ordered_fixup_mismatch_must_be_honestly_recorded(self):
        blocked = self.results["blocked"]
        validate_result(self.entry, blocked, require_exact=False)
        with self.assertRaises(ValueError):
            validate_result(self.entry, blocked)
        forged = copy.deepcopy(blocked)
        forged["rounds"][0]["fixups_exact"] = True
        with self.assertRaisesRegex(ValueError, "raw bytes"):
            validate_result(self.entry, forged, require_exact=False)

    def test_unselected_units_keep_identity_determinism_and_boundary_gates(self):
        for mutate in (lambda row: row.update(object_normalized_equal=False),
                       lambda row: row["omfs"][1].update(translator_comments=["other compiler"]),
                       lambda row: row["rounds"][0].update(size=15),
                       lambda row: row["rounds"][0].update(candidate_fixups=[8, 4]),
                       lambda row: row.update(exact=True)):
            bad = copy.deepcopy(self.results["blocked"])
            mutate(bad)
            with self.assertRaises(ValueError):
                validate_result(self.entry, bad, require_exact=False)

    def test_excluded_removed_entry_revalidates_frozen_config_without_becoming_selectable(self):
        frozen = {"good": {"id": "good", "size": 16}, "blocked": self.entry}
        live = {"good": frozen["good"]}
        resolved = replay_entries_for_accept(live, frozen, self.results, ["good"])
        self.assertEqual(resolved["blocked"], frozen["blocked"])
        self.assertEqual(set(live), {"good"})
        with self.assertRaises(ValueError):
            replay_entries_for_accept(live, frozen, self.results, ["good", "blocked"])
        with self.assertRaises(ValueError):
            replay_entries_for_accept(live, frozen, self.results, None)
        with self.assertRaises(ValueError):
            replay_entries_for_accept({"good": {"id": "good", "size": 15}}, frozen, self.results, ["good"])


if __name__ == "__main__":
    unittest.main()
