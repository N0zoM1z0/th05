from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import review_zun_resident_data as data


class ZunResidentDataTests(unittest.TestCase):
    def test_ctlib_and_master_omf_data_are_separate_complete_sources(self):
        record = data.check()
        self.assertEqual(record["resident_data"]["source_written_bytes"], 610)
        self.assertEqual(record["resident_data"]["ctlib_data_bytes"], 492)
        self.assertEqual(record["resident_data"]["master_data_bytes"], 118)
        self.assertEqual({row["name"] for row in record["ctlib_modules"]},
                         {"_abort", "atexit", "exit", "files", "files2", "ioerror"})
        self.assertEqual({row["name"] for row in record["master_modules"]},
                         {"version", "grp", "resdata", "fil"})
        self.assertTrue(all(row["data"]["exact_after_omf_relocation"]
                            for row in record["ctlib_modules"] + record["master_modules"]))

    def test_master_header_is_a_crosscheck_not_a_second_claim(self):
        record = data.check()
        header = record["master_header"]
        version = next(row for row in record["master_modules"] if row["name"] == "version")
        self.assertEqual(header["size"], 93)
        self.assertTrue(header["raw_exact"])
        self.assertEqual(header["source_sha256"], version["data"]["source_sha256"])
        self.assertEqual(header["target_sha256"], version["data"]["target_sha256"])
        self.assertEqual(record["resident_data"]["master_header_crosscheck_bytes"], 93)

    def test_master_public_symbol_relationship_is_retained(self):
        record = data.check()
        symbol = record["master_external_symbol_definitions"]["_Master_Version"]
        self.assertEqual((symbol["member"], symbol["segment"], symbol["offset"]),
                         ("version", 2, 20))
        self.assertEqual(symbol["address"], 0x17FE + 20)


if __name__ == "__main__":
    unittest.main()
