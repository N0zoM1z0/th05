"""Public synthetic fail-closed checks for ZUN.COM's -O ADPCM diagnostic."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from replay_zun_adpcm import CONFIG, PUBLIC, EXPECTED_PUBLICS, check_public, scope


class ZunAdpcmTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = tomllib.loads(CONFIG.read_text())
        cls.record = json.loads(PUBLIC.read_text())

    def test_source_current_and_full_abi(self):
        scope(self.config)
        self.assertEqual(self.config['code_bytes'], 892)
        self.assertEqual(self.config['initialized_data_bytes'], 34)
        self.assertEqual(self.config['bss_bytes'], 42)
        self.assertEqual(self.config['publics'], EXPECTED_PUBLICS)
        self.assertEqual(len(EXPECTED_PUBLICS), 10)
        check_public(self.record, self.config)

    def test_inflating_code_with_data_is_rejected(self):
        altered = copy.deepcopy(self.config)
        altered['code_bytes'] += 34
        altered['initialized_data_bytes'] = 0
        with self.assertRaises(ValueError):
            scope(altered)

    def test_initializing_bss_is_rejected(self):
        altered = copy.deepcopy(self.config)
        altered['bss_bytes'] = 0
        with self.assertRaises(ValueError):
            scope(altered)

    def test_global_credit_is_forbidden(self):
        altered = copy.deepcopy(self.config)
        altered['global_authored_credit'] = 926
        with self.assertRaises(ValueError):
            scope(altered)

    def test_wrong_public_entry_is_rejected(self):
        altered = copy.deepcopy(self.config)
        altered['publics']['ADPCM_SETUP'] += 1
        with self.assertRaises(ValueError):
            scope(altered)

    def test_changed_source_digest_rejected(self):
        altered = copy.deepcopy(self.record)
        altered['source_sha256'] = '0' * 64
        with self.assertRaises(ValueError):
            check_public(altered, self.config)

    def test_second_positive_cannot_be_missing(self):
        altered = copy.deepcopy(self.record)
        altered['rounds'] = altered['rounds'][:1]
        with self.assertRaises(ValueError):
            check_public(altered, self.config)

    def test_negative_must_change_instruction_not_signature(self):
        altered = copy.deepcopy(self.record)
        altered['negative_control']['code_exact'] = True
        with self.assertRaises(ValueError):
            check_public(altered, self.config)
        altered = copy.deepcopy(self.record)
        altered['negative_control']['initialized_data_exact'] = False
        with self.assertRaises(ValueError):
            check_public(altered, self.config)

    def test_no_raw_opcode_payload(self):
        s = (ROOT / self.config['source']).read_text()
        self.assertIn('ADPCM_SETUP proc near', s)
        self.assertIn('repe cmpsb', s)
        self.assertNotIn('include original_binary', s)
        self.assertIn("ram_signature db '*+=-PMD ADPCM RAM Check Data-=+*'", s)


if __name__ == '__main__':
    unittest.main()
