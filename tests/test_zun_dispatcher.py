"""Synthetic, fail-closed tests for ZUN's source-owned inner dispatcher."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from replay_zun_dispatcher import (CONFIG, PUBLIC, CODE_SPANS, DATA_SPANS,
                                   MEMBER_ORDER, check_record, scope)


class ZunDispatcherTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = tomllib.loads(CONFIG.read_text())
        cls.record = json.loads(PUBLIC.read_text())

    def test_exact_source_current_scope(self):
        scope(self.config)
        self.assertEqual(sum(e-s for s,e in CODE_SPANS), 213)
        self.assertEqual(sum(e-s for s,e in DATA_SPANS), 345)
        self.assertEqual(self.config['child_hole_bytes'], 17187)
        check_record(self.record, self.config)

    def test_all_children_have_distinct_real_boundaries(self):
        self.assertEqual(list(MEMBER_ORDER), ['-O','-I','-S','-G','-M'])
        self.assertEqual(list(self.config['child_sizes'].values()), [926,1009,6564,8377,311])
        self.assertEqual(self.config['publics']['inner_moveup'], 0x4649)

    def test_fake_authorship_rejected(self):
        bad = copy.deepcopy(self.config)
        bad['global_authored_credit'] = 558
        with self.assertRaises(ValueError):
            scope(bad)

    def test_no_payload_reclassification(self):
        bad = copy.deepcopy(self.config)
        bad['code_bytes'] = 558 + 17187
        bad['initialized_data_bytes'] = 0
        with self.assertRaises(ValueError):
            scope(bad)

    def test_changed_foreign_child_size_rejected(self):
        bad = copy.deepcopy(self.config)
        bad['child_sizes']['-S'] += 1
        with self.assertRaises(ValueError):
            scope(bad)

    def test_stale_source_rejected(self):
        bad = copy.deepcopy(self.record)
        bad['source_sha256'] = '0'*64
        with self.assertRaises(ValueError):
            check_record(bad,self.config)

    def test_second_positive_required(self):
        bad = copy.deepcopy(self.record)
        bad['rounds'].pop()
        with self.assertRaises(ValueError):
            check_record(bad,self.config)

    def test_negative_must_mutate_instructions_not_catalog(self):
        bad = copy.deepcopy(self.record)
        bad['negative_control']['code_exact'] = True
        with self.assertRaises(ValueError):
            check_record(bad,self.config)
        bad = copy.deepcopy(self.record)
        bad['negative_control']['data_exact'] = False
        with self.assertRaises(ValueError):
            check_record(bad,self.config)

    def test_no_foreign_child_binaries_in_source(self):
        source = (ROOT/self.config['source']).read_text()
        self.assertIn('org $+O_BYTES',source)
        self.assertIn('org $+S_BYTES',source)
        self.assertNotIn('incbin ',source.lower())
        self.assertNotIn('include original',source.lower())


if __name__ == '__main__':
    unittest.main()
