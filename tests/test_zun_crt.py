"""Public, fail-closed checks for the real original Borland tiny CRT OMF."""
from __future__ import annotations
import copy
import json
from pathlib import Path
import sys
import tomllib
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from replay_zun_crt import CONFIG,PUBLIC,TINY_CRT_SHA256,check_record,reviewed_claims,scope


class OriginalTinyCrtTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config=tomllib.loads(CONFIG.read_text())
        cls.record=json.loads(PUBLIC.read_text())

    def test_source_current_two_original_producers(self):
        scope(self.config)
        check_record(self.record,self.config)
        self.assertEqual(self.record['CRT_object_sha256'],TINY_CRT_SHA256)
        self.assertEqual([z['code_raw_exact'] for z in self.record['rounds']],[True,True])
        self.assertTrue(all(z['DATA_exact'] for z in self.record['rounds']))

    def test_only_source_written_CRT_bytes_get_vendor_ownership(self):
        import tomllib as tl
        manifest=tl.loads((ROOT/'config/targets.toml').read_text())
        target=next(x for x in manifest['artifacts'] if x['id']=='th05-zun')
        claims,_=reviewed_claims(ROOT,{'sha256':target['sha256'],'size':target['size']})
        self.assertEqual([(c['start'],c['end']) for c in claims],
                         [(0xae4,0xd47),(0xd49,0xd4b),(0x2034,0x20a2)])
        self.assertEqual(sum(z['end']-z['start'] for z in claims),723)
        self.assertEqual([c['kind'] for c in claims],
                         ['verified-vendor-code','verified-vendor-code','verified-vendor-initialized-data'])
        self.assertTrue(all(c['authored_credit']==0 for c in claims))

    def test_writable_original_cs_gap_cannot_be_reclassified(self):
        bad=copy.deepcopy(self.config)
        bad['source_written_code_bytes']=615
        bad['unwritten_code_runtime_slot_size']=0
        with self.assertRaisesRegex(ValueError,'scope changed|accounting'):
            scope(bad)

    def test_original_INIT_and_BSS_geometry_is_required(self):
        bad=copy.deepcopy(self.config)
        bad['original_INIT_size']=0x10
        with self.assertRaises(ValueError):scope(bad)
        bad=copy.deepcopy(self.record)
        bad['rounds'][0]['real_INIT_BSS_layout']=False
        with self.assertRaisesRegex(ValueError,'double-positive'):
            check_record(bad,self.config)

    def test_compiled_negative_must_modify_code_and_data_not_cfg(self):
        for field,wrong in [('code_raw_exact',True),('DATA_exact',True),
                            ('accepted_cfg_exact',False),('code_runtime_slot_unwritten',False),
                            ('real_INIT_BSS_layout',True)]:
            bad=copy.deepcopy(self.record)
            bad['negative_control'][field]=wrong
            with self.subTest(field=field), self.assertRaisesRegex(ValueError,'negative'):
                check_record(bad,self.config)

    def test_cfg_object_provenance_cannot_be_substituted(self):
        bad=copy.deepcopy(self.record)
        bad['accepted_cfg_objects_sha256'][0]='0'*64
        with self.assertRaisesRegex(ValueError,'accepted C\\+\\+ source identity'):
            check_record(bad,self.config)

    def test_two_independent_positive_rounds_required(self):
        bad=copy.deepcopy(self.record)
        bad['rounds'].pop()
        with self.assertRaises(ValueError):check_record(bad,self.config)

    def test_no_original_startup_code_or_crt_data_in_binder(self):
        source=(ROOT/self.config['source']).read_text()
        self.assertIn('INIT_TABLE_SIZE equ 012h',source)
        self.assertIn('RUNTIME_BSS_SIZE equ 054h',source)
        self.assertNotIn('incbin ',source.lower())
        self.assertNotIn('db 0',source.lower())
        self.assertNotIn('dw 0',source.lower())


if __name__=='__main__':
    unittest.main()
