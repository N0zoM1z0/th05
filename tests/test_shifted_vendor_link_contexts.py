"""Fail-closed public checks for original CL.LIB OMF link contexts, not a cold replay."""
from __future__ import annotations
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from review_context_remaining import (
    proof_path as remaining_path, validate_public as remaining_validate,
    reviewed_claims as remaining_claims,
)
from review_maine_shifted_vendor import (
    PROOF as MAINE_PROOF, validate_public as maine_validate,
    reviewed_claims as maine_claims,
)
from review_main_shifted_vendor import (
    PROOF as MAIN_PROOF, SELECTED, validate_public as main_validate,
    reviewed_claims as main_claims,
)


class LinkedVendorSourceReviewTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = json.loads(MAIN_PROOF.read_text())
        cls.maine = json.loads(MAINE_PROOF.read_text())
        cls.remaining = {name:json.loads(remaining_path(name).read_text())
                         for name in ('op','maine')}

    def test_original_native_omf_proofs_public_source_current(self):
        main_validate(self.original)
        maine_validate(self.maine)
        for name,record in self.remaining.items():
            remaining_validate(record,name)
        self.assertEqual(self.original['source_written_CODE_bytes'],2829)
        self.assertEqual(self.maine['source_written_CODE_bytes'],2829)
        self.assertEqual(sum(x['source_written_CODE_bytes'] for x in self.remaining.values()),1088)

    def test_explicit_adoption_does_not_double_count_pathops(self):
        claims,decision = main_claims(
            ROOT, {'sha256':self.original['original_payload_sha256']})
        self.assertTrue(decision)
        self.assertEqual([x['member'] for x in claims],list(SELECTED))
        self.assertEqual(sum(x['end']-x['start'] for x in claims),2621)
        self.assertNotIn('_pathops',[x['member'] for x in claims])
        self.assertTrue(all(x['kind']=='verified-vendor-code' and
                            x['authored_credit']==0 for x in claims))
        maine,_=maine_claims(ROOT,{'sha256':self.maine['original_payload_sha256']})
        self.assertEqual(sum(x['end']-x['start'] for x in maine),2829)
        for name,n in (('op',1000),('maine',88)):
            claims,_=remaining_claims(
                ROOT,name,{'sha256':self.remaining[name]['original_payload_sha256']})
            self.assertEqual(sum(x['end']-x['start'] for x in claims),n)

    def test_target_identity_mismatch_is_rejected(self):
        for caller,view in ((main_claims,self.original),
                            (maine_claims,self.maine)):
            with self.subTest(view=view['artifact']):
                with self.assertRaisesRegex(ValueError,'target|payload'):
                    caller(ROOT,{'sha256':'0'*64})
        with self.assertRaisesRegex(ValueError,'target|payload'):
            remaining_claims(ROOT,'op',{'sha256':'0'*64})

    def test_group_data_bss_and_entry_shifts_are_not_ad_hoc_wildcards(self):
        for key,value in [('original_DGROUP_base',0x209E0),
                          ('original_DATA_offset_delta',0),
                          ('original_BSS_offset_delta',0),
                          ('source_verifier_sha256','0'*64)]:
            with self.subTest(key=key):
                record=copy.deepcopy(self.original)
                record[key]=value
                with self.assertRaises(ValueError):main_validate(record)
        for field in ('original_entry','original_segment_frame'):
            record=copy.deepcopy(self.original)
            method=record['string_method_entries']['@string@$bdtr$qv']
            method[field]+=1
            with self.subTest(field=field),self.assertRaises(ValueError):
                main_validate(record)

    def test_wrong_maine_string_offset_and_source_member_rejected(self):
        bad=copy.deepcopy(self.maine)
        bad['shifted_original_class_methods']['@string@$bdtr$qv']['original_entry']+=1
        with self.assertRaises(ValueError):maine_validate(bad)
        bad=copy.deepcopy(self.maine)
        bad['members'][0]['size']+=1
        with self.assertRaises(ValueError):maine_validate(bad)

    def test_no_other_code_or_game_authored_credit_can_be_claimed(self):
        for record,validator in ((self.original,main_validate),
                                 (self.maine,maine_validate)):
            for field in ('authored_credit','non_CODE_bytes_claimed',
                          'other_source_bytes_claimed'):
                if field not in record:
                    continue
                bad=copy.deepcopy(record);bad[field]=16
                with self.subTest(field=field),self.assertRaises(ValueError):
                    validator(bad)
        op=copy.deepcopy(self.remaining['op'])
        op['source_written_CODE_bytes']+=1
        with self.assertRaises(ValueError):remaining_validate(op,'op')


if __name__ == '__main__':
    unittest.main()
