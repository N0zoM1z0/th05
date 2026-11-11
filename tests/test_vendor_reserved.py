"""Fail-closed public tests for large CL.LIB OMF runtime-state reservations."""
from __future__ import annotations
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from review_vendor_reserved import PROOF,DECISION,SCOPE,reviewed_claims,validate_public


class VendorReservedReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proof=json.loads(PROOF.read_text())
        cls.decision=json.loads(DECISION.read_text())

    def test_exact_original_Omf_source_record_inventory(self):
        validate_public(self.proof)
        self.assertEqual(self.proof['source_written_total'],2040)
        self.assertEqual(self.proof['unwritten_total'],8)
        self.assertEqual([(r['member'],r['source_written_bytes']) for r in self.proof['members']],
                         [('farheap',1109),('exec',931)])

    def test_verified_source_spans_leave_actual_runtime_words_unowned(self):
        claims,proof_sha=reviewed_claims(ROOT,
            view={'sha256':self.proof['native_inputs']['target_payload_sha256']})
        self.assertEqual(len(claims),4)
        self.assertEqual(sum(x['end']-x['start'] for x in claims),2040)
        self.assertEqual([(x['start'],x['end']) for x in claims],[
            (0x527f,0x5285),(0x528b,0x56da),(0xa2fc,0xa460),(0xa462,0xa6a1)])
        self.assertTrue(proof_sha)
        self.assertTrue(all(x['authored_credit']==0 for x in claims))

    def test_claiming_unwritten_CS_runtime_slot_is_rejected(self):
        bad=copy.deepcopy(self.proof)
        bad['members'][0]['source_spans'][0]['end']=0x528b
        bad['members'][0]['source_spans'][0]['size']=12
        with self.assertRaisesRegex(ValueError,'unwritten runtime variables|source spans'):
            validate_public(bad)

    def test_falsified_LIDATA_source_record_is_rejected(self):
        bad=copy.deepcopy(self.proof)
        rec=next(x for x in bad['members'][1]['CODE_records'] if x['kind']=='LIDATA')
        rec['sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'OMF source writes'):
            validate_public(bad)

    def test_falsified_FIXUPP_site_order_and_gap_target_are_rejected(self):
        bad=copy.deepcopy(self.proof)
        bad['members'][1]['fixup_actions'][0],bad['members'][1]['fixup_actions'][1]=(
            bad['members'][1]['fixup_actions'][1],bad['members'][1]['fixup_actions'][0])
        with self.assertRaisesRegex(ValueError,'FIXUPP location/order'):
            validate_public(bad)
        bad=copy.deepcopy(self.proof)
        # Set first existing FIXUPP write to the uninitialized 2-byte CS slot.
        bad['members'][1]['fixup_actions'][0]['write_start']=356
        with self.assertRaisesRegex(ValueError,'unwritten runtime state slot'):
            validate_public(bad)

    def test_missing_original_reloc_or_source_evidence_fails_closed(self):
        bad=copy.deepcopy(self.proof)
        bad['members'][1]['ordered_MZ_fixups']=[11]
        with self.assertRaisesRegex(ValueError,'FIXUPP location/order'):
            validate_public(bad)
        bad=copy.deepcopy(self.proof)
        bad['members'][0]['member_program_sha256']='f'*64
        with self.assertRaisesRegex(ValueError,'member/source identity'):
            validate_public(bad)

    def test_user_selected_original_vendor_identity_is_pinned(self):
        bad=copy.deepcopy(self.proof)
        bad['members'][0]['member']='exec'
        with self.assertRaisesRegex(ValueError,'member selection'):
            validate_public(bad)
        self.assertEqual(set(SCOPE),{'exec','farheap'})
        self.assertEqual(self.decision['unwritten_bytes_claimed'],0)
        self.assertEqual(self.decision['authored_credit'],0)

    def test_old_vendor_review_is_unchanged(self):
        # The 31 old complete members keep their original evidence/digest.
        previous=json.loads((ROOT/'config/vendor_ownership.json').read_text())
        self.assertEqual(previous['proposed_contribution_count'],31)
        self.assertEqual(len(previous['deferred']),2)
        self.assertEqual(previous['proposed_bytes'],2901)


if __name__=='__main__':
    unittest.main()
