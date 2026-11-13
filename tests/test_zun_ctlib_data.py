from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import review_zun_ctlib_data as data


class ZunCtlibDataTests(unittest.TestCase):
    def test_complete_resident_tail_omf_data_partition(self):
        record = data.check()
        self.assertEqual(record["verified_data_bytes"], 52)
        self.assertEqual(record["initialized_data_bytes"], 42)
        self.assertEqual(record["uninitialized_storage_bytes"], 10)
        self.assertEqual(record["unclassified_bytes"], 0)
        self.assertEqual(record["ambiguous_candidates"], [])
        self.assertTrue(record["negative_control"]["nonrelocation_data_flip_rejected"])
        self.assertTrue(record["negative_control"]["relocation_word_flip_rejected"])

    def test_setargv_unwritten_data_suffix_is_not_initialized_data(self):
        record = data.check()
        row = next(item for item in record["segments"]
                   if item["member"] == "setargv" and item["segment"] == 2)
        self.assertEqual((row["base_com"], row["segment_end_com"], row["end_com"]),
                         (0x1A86, 0x1A94, 0x1A94))
        self.assertEqual(row["verification"]["initialized_spans"], [[0, 4]])
        self.assertEqual(row["verification"]["uninitialized_spans"], [[4, 14]])

    def test_claims_separate_initialized_data_from_zero_fill_storage(self):
        record = data.check()
        view = {"size": 18116, "sha256": record["target_artifact_sha256"]}
        claims, _ = data.reviewed_claims(ROOT, view)
        initialized = [row for row in claims
                       if row["kind"] == "verified-vendor-initialized-data"]
        uninitialized = [row for row in claims
                         if row["kind"] == "reviewed-uninitialized-vendor-storage"]
        self.assertEqual(sum(row["end"] - row["start"] for row in initialized), 42)
        self.assertEqual(sum(row["end"] - row["start"] for row in uninitialized), 10)
        self.assertEqual({row["member"] for row in uninitialized}, {"setargv"})
        self.assertTrue(all(row["authored_credit"] == 0 for row in claims))


if __name__ == "__main__":
    unittest.main()
