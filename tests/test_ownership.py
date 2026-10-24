import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from ownership import partition, validate_partition, overlay_vendor


class OwnershipTests(unittest.TestCase):
    def entry(self, start=3, size=8, **extra):
        return {"id": "real-whole-function", "target_start": start, "size": size, **extra}

    def test_entire_unreviewed_view_remains_unknown(self):
        self.assertEqual(partition(100, []), [{"start": 0, "end": 100, "kind": "unknown"}])

    def test_unknown_gaps_and_explicit_classification_are_all_retained(self):
        rows = partition(15, [self.entry(alignment_offsets=[7], code_data_ranges=[
            {"offset": 4, "size": 2, "kind": "compiler-switch-table"}])])
        self.assertEqual([(r["start"], r["end"], r["kind"]) for r in rows], [
            (0, 3, "unknown"), (3, 7, "accepted-cxx-instructions"),
            (7, 9, "accepted-cxx-switch-table"), (9, 10, "accepted-cxx-instructions"),
            (10, 11, "checked-uncredited-padding"), (11, 15, "unknown")])

    def test_contiguous_padding_and_unordered_units(self):
        first = self.entry(0, 5, padding_bytes=[{"offset": 3, "value": 0}, {"offset": 4, "value": 0}])
        second = {**self.entry(5, 2), "id": "second-function"}
        rows = partition(7, [second, first])
        self.assertEqual([(r["start"], r["end"]) for r in rows], [(0, 3), (3, 5), (5, 7)])
        self.assertEqual(rows[-1]["unit"], "second-function")

    def test_out_of_bounds_and_overlapping_claims_are_rejected(self):
        for entries in ([self.entry(-1)], [self.entry(8)], [self.entry(), self.entry(4)]):
            with self.subTest(entries=entries), self.assertRaises(ValueError):
                partition(15, entries)

    def test_a_table_cannot_hide_padding_or_unknown_data(self):
        for table in ({"offset": 0, "size": 2, "kind": "asset"},
                      {"offset": 6, "size": 2, "kind": "compiler-switch-table"}):
            with self.subTest(table=table), self.assertRaises(ValueError):
                partition(15, [self.entry(alignment_offsets=[7], code_data_ranges=[table])])

    def test_missing_suffix_gap_and_overlap_are_rejected(self):
        for pieces in ([], [{"start": 0, "end": 9}], [{"start": 1, "end": 10}],
                       [{"start": 0, "end": 5}, {"start": 4, "end": 10}]):
            with self.subTest(pieces=pieces), self.assertRaises(ValueError):
                validate_partition(10, pieces)

    def test_vendor_replaces_only_its_exact_unknown_range(self):
        pieces = partition(20, [self.entry(10, 5)])
        claims = [{"start": 2, "end": 7, "kind": "verified-vendor-code", "member": "strcmp"}]
        rows = overlay_vendor(20, pieces, claims)
        self.assertEqual([(r["start"], r["end"], r["kind"]) for r in rows], [
            (0, 2, "unknown"), (2, 7, "verified-vendor-code"), (7, 10, "unknown"),
            (10, 15, "accepted-cxx-instructions"), (15, 20, "unknown")])

    def test_vendor_cannot_displace_source_tables_or_padding(self):
        pieces = partition(20, [self.entry(5, 8, alignment_offsets=[7], code_data_ranges=[
            {"offset": 4, "size": 2, "kind": "compiler-switch-table"}])])
        for start in (5, 9, 12):
            with self.subTest(start=start), self.assertRaises(ValueError):
                overlay_vendor(20, pieces, [{"start": start, "end": start + 1,
                    "kind": "verified-vendor-code", "member": "vendor"}])

    def test_duplicate_and_out_of_bounds_vendor_claims_are_rejected(self):
        row = {"start": 0, "end": 4, "kind": "verified-vendor-code", "member": "vendor"}
        for claims in ([row, row], [{**row, "start": -1}], [{**row, "end": 21}]):
            with self.subTest(claims=claims), self.assertRaises(ValueError):
                overlay_vendor(20, partition(20, []), claims)


if __name__ == "__main__":
    unittest.main()
