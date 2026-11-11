"""Fail-closed public checks for the final MAIN CL.LIB setenvp CODE extent."""
from __future__ import annotations
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from review_main_setenvp import PROOF,DECISION,validate_public


class OriginalSetenvpTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record=json.loads(PROOF.read_text())

    def test_complete_source_current_original_CODE_and_actual_fixups(self):
        validate_public(self.record)
        self.assertEqual(self.record['source_written_CODE_bytes'],88)
        self.assertEqual([z['own_DATA_offset'] for z in self.record['linked_views']],[0x2576,0x2564])
        self.assertEqual(self.record['initial_DATA_bytes_claimed'],0)
        self.assertEqual(self.record['INIT_bytes_claimed'],0)

    def test_reordered_OMF_FIXUPP_is_rejected(self):
        x=copy.deepcopy(self.record)
        a=x['linked_views'][0]['OMF_source_fixup_actions']
        a[0],a[1]=a[1],a[0]
        with self.assertRaisesRegex(ValueError,'site/order'):validate_public(x)

    def test_real_call_and_jump_rewrites_must_both_exist(self):
        x=copy.deepcopy(self.record)
        x['linked_views'][0]['OMF_source_fixup_actions'][7]['operation']='far-pointer'
        with self.assertRaisesRegex(ValueError,'far-transfer'):validate_public(x)

    def test_wrong_original_DATA_group_is_rejected(self):
        x=copy.deepcopy(self.record)
        x['linked_views'][1]['own_DATA_offset']=0x2576
        with self.assertRaisesRegex(ValueError,'relocation context'):validate_public(x)

    def test_data_or_game_authorship_claim_cannot_be_forged(self):
        for key,value in [('authored_credit',88),('initial_DATA_bytes_claimed',4),('INIT_bytes_claimed',6)]:
            with self.subTest(key=key):
                x=copy.deepcopy(self.record)
                x[key]=value
                with self.assertRaisesRegex(ValueError,'scope|credit'):validate_public(x)

    def test_source_object_identity_cannot_be_substituted(self):
        x=copy.deepcopy(self.record)
        x['source_library_parser_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'verifier identity'):validate_public(x)
        self.assertEqual(json.loads(DECISION.read_text())['code_bytes'],88)


if __name__=='__main__': unittest.main()
