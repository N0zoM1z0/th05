"""Public fail-closed checks for large OP/MAINE CL.LIB OMF CODE members."""
from __future__ import annotations
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from review_context_reserved import CONTEXTS,proof_path,decision_path,reviewed_claims,validate_public


class OriginalContextReservedTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proofs={name:json.loads(proof_path(name).read_text()) for name in CONTEXTS}

    def test_both_complete_native_scope_models_are_source_current(self):
        for name,proof in self.proofs.items():
            with self.subTest(name=name):
                validate_public(proof,name)
                self.assertEqual(proof['source_written_total'],2040)
                self.assertEqual(proof['unwritten_total'],8)
                self.assertEqual([(x['member'],x['size']) for x in proof['members']],
                                 [('farheap',1115),('exec',933)])

    def test_exact_owner_scopes_do_not_claim_eight_runtime_CS_bytes(self):
        for name,proof in self.proofs.items():
            with self.subTest(name=name):
                claims,_=reviewed_claims(ROOT,name,{'sha256':proof['original_payload_sha256']})
                self.assertEqual(len(claims),4)
                self.assertEqual(sum(x['end']-x['start'] for x in claims),2040)
                self.assertTrue(all(z['authored_credit']==0 for z in claims))
                for member in proof['members']:
                    slot=member['runtime_CS_slot']
                    self.assertEqual(slot['authored_credit'],0)
                    self.assertFalse(slot['source_written'])
                    self.assertFalse(any(c['start']<slot['end'] and c['end']>slot['start'] for c in claims))

    def test_forced_gap_ownership_rejected(self):
        for name,proof in self.proofs.items():
            bad=copy.deepcopy(proof)
            bad['members'][0]['source_written_spans'][0][1]+=6
            with self.subTest(name=name),self.assertRaisesRegex(ValueError,'source-written CODE intervals'):
                validate_public(bad,name)

    def test_original_LIDATA_model_cannot_be_falsified(self):
        for name,proof in self.proofs.items():
            bad=copy.deepcopy(proof)
            record=next(r for r in bad['members'][1]['source_records'] if r['kind']=='LIDATA')
            record['sha256']='0'*64
            with self.subTest(name=name),self.assertRaisesRegex(ValueError,'LEDATA/LIDATA source bytes'):
                validate_public(bad,name)

    def test_real_FIXUPP_order_must_agree_with_pinned_library(self):
        for name,proof in self.proofs.items():
            bad=copy.deepcopy(proof)
            rows=bad['members'][0]['OMF_fixup_actions']
            rows[0],rows[1]=rows[1],rows[0]
            with self.subTest(name=name),self.assertRaisesRegex(ValueError,'FIXUPP site/order'):
                validate_public(bad,name)

    def test_game_authored_credit_or_original_context_cannot_be_changed(self):
        for name,proof in self.proofs.items():
            for field,value in [('authored_credit',2040),('unwritten_total',0),('packed_target_sha256','0'*64)]:
                bad=copy.deepcopy(proof)
                bad[field]=value
                with self.subTest(name=name,field=field),self.assertRaises(ValueError):
                    validate_public(bad,name)

    def test_independent_original_review_decision(self):
        for name in CONTEXTS:
            row=json.loads(decision_path(name).read_text())
            self.assertEqual(row['members'],['farheap','exec'])
            self.assertEqual(row['authored_credit'],0)
            self.assertEqual(row['unwritten_CS_bytes_claimed'],0)


if __name__=='__main__':unittest.main()
