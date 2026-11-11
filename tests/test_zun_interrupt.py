"""Public, synthetic fail-closed checks for the focused -I COM acceptance."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from replay_zun_interrupt import CONFIG, PUBLIC, scope, check_record


class InterruptScopeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = tomllib.loads(CONFIG.read_text())
        cls.saved = json.loads(PUBLIC.read_text())

    def test_complete_source_current(self):
        self.assertEqual(len(scope(self.config)), 4)
        check_record(self.saved, self.config)

    def test_table_as_code_rejected(self):
        altered = copy.deepcopy(self.config)
        altered['code_spans'][0]['size'] += 1
        altered['data_spans'][0]['start'] += 1
        altered['data_spans'][0]['size'] -= 1
        with self.assertRaises(ValueError):
            scope(altered)

    def test_unreviewed_credit_must_not_change(self):
        altered = copy.deepcopy(self.config)
        altered['global_authored_credit'] = 1009
        with self.assertRaises(ValueError):
            scope(altered)

    def test_wrong_original_digest_rejected(self):
        altered = copy.deepcopy(self.saved)
        altered['source_sha256'] = '0' * 64
        with self.assertRaises(ValueError):
            check_record(altered, self.config)

    def test_incomplete_second_positive_rejected(self):
        altered = copy.deepcopy(self.saved)
        altered['rounds'][1]['code_exact'] = False
        with self.assertRaises(ValueError):
            check_record(altered, self.config)

    def test_unchanged_negative_rejected(self):
        altered = copy.deepcopy(self.saved)
        altered['negative_control']['raw_exact'] = True
        with self.assertRaises(ValueError):
            check_record(altered, self.config)


if __name__ == '__main__':
    unittest.main()
