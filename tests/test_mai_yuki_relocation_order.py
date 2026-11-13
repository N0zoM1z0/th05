"""Pin the non-address-sorted MZ relocation order of Mai/Yuki's later patterns."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact


class MaiYukiRelocationOrderTests(unittest.TestCase):
    UNIT_START = 97142  # MAIN 0x17B76
    UNIT_SIZE = 1125
    COMBINED_START = 0x17957
    INITIAL_PREFIX_SIZE = 543

    @classmethod
    def setUpClass(cls):
        manifest = load_target_manifest(ROOT / "config/targets.toml")
        artifact = find_artifact(manifest, "th05-main")
        cls.target = parse_mz(read_verified_artifact(ROOT, artifact))

    def test_later_pattern_contribution_follows_the_initial_prefix(self):
        self.assertEqual(self.UNIT_START - self.COMBINED_START, self.INITIAL_PREFIX_SIZE)
        self.assertEqual(self.UNIT_START, 0x17B76)
        self.assertEqual(self.COMBINED_START + self.INITIAL_PREFIX_SIZE, self.UNIT_START)
        self.assertEqual(len(self.target.program_image[self.UNIT_START:self.UNIT_START + self.UNIT_SIZE]), self.UNIT_SIZE)

    def test_target_mz_relocations_keep_the_original_non_sorted_order(self):
        sites = [
            relocation.linear - self.UNIT_START
            for relocation in self.target.relocations
            if self.UNIT_START <= relocation.linear < self.UNIT_START + self.UNIT_SIZE
        ]
        self.assertEqual(sites, [38, 1106, 1019, 648, 322, 130])
        # Each far-call's segment-word relocation is two bytes into its
        # 4-byte far pointer; preserve this order instead of sorting by site.
        self.assertEqual([site - 2 for site in sites], [36, 1104, 1017, 646, 320, 128])
        self.assertEqual(len(set(sites)), 6)


if __name__ == "__main__":
    unittest.main()
