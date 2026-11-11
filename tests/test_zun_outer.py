"""Synthetic public checks for the exact outer COMCSTM stub and usage."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from replay_zun_outer import CONFIG, PUBLIC, PUBLICS, check_record, scope


class ZunOuterTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config=tomllib.loads(CONFIG.read_text())
        cls.record=json.loads(PUBLIC.read_text())

    def test_complete_source_current(self):
        scope(self.config)
        self.assertEqual(self.config['code_bytes'],71)
        self.assertEqual(self.config['semantic_header_and_usage_bytes'],300)
        self.assertEqual(self.config['publics'],PUBLICS)
        check_record(self.record,self.config)

    def test_inner_program_cannot_be_reclassified(self):
        bad=copy.deepcopy(self.config)
        bad['code_bytes'] += 17745
        bad['foreign_inner_size'] = 0
        with self.assertRaises(ValueError):scope(bad)

    def test_third_party_code_cannot_be_miscredited(self):
        bad=copy.deepcopy(self.config)
        bad['global_authored_credit']=71
        with self.assertRaises(ValueError):scope(bad)

    def test_real_header_linkage_required(self):
        bad=copy.deepcopy(self.config)
        bad['publics']['outer_entry'] += 1
        with self.assertRaises(ValueError):scope(bad)

    def test_missing_second_positive_rejected(self):
        bad=copy.deepcopy(self.record)
        bad['rounds'].pop()
        with self.assertRaises(ValueError):check_record(bad,self.config)

    def test_wrong_readable_text_digest_rejected(self):
        bad=copy.deepcopy(self.record)
        bad['usage_source_sha256']='0'*64
        with self.assertRaises(ValueError):check_record(bad,self.config)

    def test_negative_must_change_code_but_not_text(self):
        bad=copy.deepcopy(self.record)
        bad['negative_control']['code_exact']=True
        with self.assertRaises(ValueError):check_record(bad,self.config)
        bad=copy.deepcopy(self.record)
        bad['negative_control']['usage_exact']=False
        with self.assertRaises(ValueError):check_record(bad,self.config)

    def test_proof_only_include_never_committed(self):
        source=(ROOT/self.config['assembler_source']).read_text()
        self.assertIn('include usage_private.inc',source)
        usage = (ROOT/self.config['usage_source']).read_text(encoding='utf-8')
        self.assertIn('割り込みマスク␠\n',usage)
        self.assertFalse(any(line.endswith(' ') for line in usage.splitlines()))
        self.assertNotIn('incbin',source.lower())
        self.assertFalse((ROOT/'src/zun/launcher/usage_private.inc').exists())


if __name__=='__main__':
    unittest.main()
