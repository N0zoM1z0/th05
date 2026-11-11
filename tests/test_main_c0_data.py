"""Public fail-closed checks for authentic Borland C0L 144-byte DATA."""
from __future__ import annotations
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from review_main_c0_data import PROOF,DECISION,validate_public,reviewed_claims


class OriginalC0DataTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proof=json.loads(PROOF.read_text())

    def test_complete_original_source_records(self):
        validate_public(self.proof)
        self.assertEqual(sum(z['size'] for z in self.proof['source_records']),144)
        self.assertEqual(self.proof['real_BSSEND_fixup_offset'],0x82)

    def test_only_vendor_data_and_no_executable_credit(self):
        claims,_=reviewed_claims(ROOT,view={'sha256':self.proof['original_payload_sha256']})
        self.assertEqual(len(claims),1)
        self.assertEqual((claims[0]['start'],claims[0]['end']), (0x209d0,0x20a60))
        self.assertEqual(claims[0]['kind'],'verified-vendor-initialized-data')
        self.assertEqual(claims[0]['instruction_bytes'],0)
        self.assertEqual(claims[0]['authored_credit'],0)

    def test_code_or_authored_credit_is_rejected(self):
        for field in ('CODE_bytes_claimed','authored_credit','CODE_instruction_bytes'):
            bad=copy.deepcopy(self.proof)
            bad[field]=144
            with self.subTest(field=field),self.assertRaises(ValueError):
                validate_public(bad)

    def test_source_omf_coverage_must_be_complete(self):
        bad=copy.deepcopy(self.proof)
        bad['source_records'][3]['size']+=1
        with self.assertRaisesRegex(ValueError,'DATA records'):validate_public(bad)

    def test_real_linker_BSSEND_is_required(self):
        bad=copy.deepcopy(self.proof)
        bad['linked_views'][1]['bss_end']+=1
        with self.assertRaisesRegex(ValueError,'BSSEND'):validate_public(bad)

    def test_source_and_adoption_identity_is_pinned(self):
        bad=copy.deepcopy(self.proof)
        bad['verifier_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'verifier input identity'):validate_public(bad)
        self.assertEqual(json.loads(DECISION.read_text())['authored_credit'],0)


if __name__=='__main__':unittest.main()
