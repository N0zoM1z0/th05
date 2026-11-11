"""Public fail-closed, resource-safe tests for the exact ZUN -G child."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from replay_zun_gaiji import CONFIG, PUBLIC, check_record, scope


class ZunGaijiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = tomllib.loads(CONFIG.read_text())
        cls.record = json.loads(PUBLIC.read_text())

    def test_source_current_exact_scope(self):
        rows = scope(self.config)
        self.assertEqual([(r['kind'], r['start'], r['end']) for r in rows], [
            ('code_bytes', 0, 75), ('alignment_bytes', 75, 76),
            ('initialized_message_bytes', 76, 185), ('external_resource_bytes', 185, 8377)])
        check_record(self.record, self.config)

    def test_external_glyphs_are_not_source_code(self):
        bad = copy.deepcopy(self.config)
        bad['code_bytes'] += 8192
        bad['external_resource_bytes'] = 0
        with self.assertRaises(ValueError):
            scope(bad)

    def test_no_global_authored_byte_credit(self):
        bad = copy.deepcopy(self.config)
        bad['global_authored_credit'] = 8377
        with self.assertRaises(ValueError):
            scope(bad)

    def test_wrong_source_digest_is_rejected(self):
        bad = copy.deepcopy(self.record)
        bad['source_sha256'] = '0' * 64
        with self.assertRaises(ValueError):
            check_record(bad, self.config)

    def test_stale_external_resource_proof_is_rejected(self):
        bad = copy.deepcopy(self.record)
        bad['font_proof_sha256'] = 'f' * 64
        with self.assertRaises(ValueError):
            check_record(bad, self.config)

    def test_negative_must_not_modify_external_font(self):
        bad = copy.deepcopy(self.record)
        bad['negative_control']['content_exact']['external_resource_bytes'] = False
        with self.assertRaises(ValueError):
            check_record(bad, self.config)

    def test_missing_second_producer_rejected(self):
        bad = copy.deepcopy(self.record)
        bad['rounds'].pop()
        with self.assertRaises(ValueError):
            check_record(bad, self.config)

    def test_public_source_has_no_font_pixel_bank(self):
        source = (ROOT / self.config['source']).read_text()
        self.assertIn('include gaiji_private_asset.inc', source)
        self.assertNotIn('db 080h,', source)
        self.assertFalse((ROOT / 'src/zun/gaiji/gaiji_private_asset.inc').exists())


if __name__ == '__main__':
    unittest.main()
