"""Explicit seven-scope adoption; proposals and unknown gaps grant no claims."""
import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import tomllib
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import ownership
import review_master_additions as review
from lib.pc98 import digest_bytes


class MasterAdditionsAdoptionTests(unittest.TestCase):
    def setUp(self):
        temporary=tempfile.TemporaryDirectory();self.addCleanup(temporary.cleanup)
        self.root=Path(temporary.name)
        for path in [*review.SOURCES,review.BASE_PROOF,review.PROOF]:
            destination=self.root/path;destination.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ROOT/path,destination)
        self.path=self.root/'config/reviewed_master_additions.json'
        self.decision=json.loads((ROOT/'config/reviewed_master_additions.json').read_text())
        self.views=tomllib.loads((ROOT/'config/ownership.toml').read_text())['views']
        target_rows=tomllib.loads((ROOT/'config/targets.toml').read_text())['artifacts']
        self.targets={row['id']:row for row in target_rows}

    def write(self):self.path.write_text(json.dumps(self.decision))

    def call(self,verify=False):
        return ownership.reviewed_master_additions(self.root,views=self.views,targets=self.targets,verify_targets=verify)

    def test_optional_decision_absence_has_no_claims_or_native_replay(self):
        with patch.object(review,'review_inputs') as replay:
            self.assertEqual(self.call(verify=True),({},None));replay.assert_not_called()

    def test_exact_claims_keep_table_data_distinct_and_original_scope_ids(self):
        self.write();claims,digest=self.call()
        self.assertEqual({k:len(v)for k,v in claims.items()},dict(main=5,op=1,maine=1))
        self.assertEqual(digest,digest_bytes(self.path.read_bytes()))
        self.assertEqual({row['scope_id']for values in claims.values()for row in values},set(self.decision['scopes']))
        for name in ('op','maine'):
            row=claims[name][0]
            self.assertEqual(row['content_kind'],'library-code-data')
            self.assertEqual(row['kind'],'verified-vendor-code')
            self.assertEqual(row['end']-row['start'],1024)
        self.assertTrue(all(row['content_kind']=='library-instructions'for row in claims['main']))
        self.assertEqual(sum(row['end']-row['start']for row in claims['main']),104)

    def test_cross_artifact_private_proof_is_replayed_only_once(self):
        self.write()
        result=dict(kind='native-source-backed-master-additions-review',scopes=7,full_bytes=2152,
            instruction_bytes=103,library_padding_bytes=1,library_code_data_bytes=2048,
            byte_proof_replayed=True,decision='PROPOSAL',authored_credit=0,compiler_invocations=0,authored_denominator=None)
        with patch.object(review,'review_inputs',return_value=result) as replay:
            claims,_=self.call(verify=True)
            self.assertEqual(set(claims),{'main','op','maine'})
            replay.assert_called_once()
            self.assertEqual(replay.call_args.kwargs,{'root':self.root})
        with patch.object(review,'review_inputs',return_value={'saved_status':'PASS'}):
            with self.assertRaisesRegex(ValueError,'actual private replay'):
                self.call(verify=True)

    def test_stale_proof_or_broader_classification_is_rejected(self):
        for key,value in [('evidence_sha256','0'*64),('classification','game-code'),('decision','ADOPT_ALL')]:
            saved=copy.deepcopy(self.decision);self.decision[key]=value;self.write()
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,'stale|classification'):
                self.call()
            self.decision=saved

    def test_original_packed_payload_and_context_pins_cannot_be_swapped(self):
        for change in ('packed','payload','artifact','size','target-manifest','view','contexts'):
            saved=copy.deepcopy((self.decision,self.targets,self.views))
            if change=='packed':self.decision['artifacts']['op']['target_sha256']=self.decision['artifacts']['maine']['target_sha256']
            elif change=='payload':self.decision['artifacts']['op']['target_payload_sha256']=self.decision['artifacts']['op']['target_sha256']
            elif change=='artifact':self.decision['artifacts']['op']['artifact']='th05-maine'
            elif change=='size':self.decision['artifacts']['op']['target_payload_size']+=1
            elif change=='target-manifest':self.targets['th05-main']['sha256']='0'*64
            elif change=='view':self.views['maine']['sha256']='0'*64
            else:self.decision['artifacts'].pop('maine')
            self.write()
            with self.subTest(change=change),self.assertRaisesRegex(ValueError,'artifact|context'):
                self.call()
            self.decision,self.targets,self.views=saved

    def test_duplicate_unknown_deferred_or_partial_selections_are_rejected(self):
        original=self.decision['scopes'][:]
        for selected in (original[:-1],original+[original[0]],original[:-1]+['FILE_TELL'],
                         original[:-1]+['rtc_mod'],original[:-1]+['nonexistent']):
            self.decision['scopes']=selected;self.write()
            with self.subTest(selected=selected),self.assertRaisesRegex(ValueError,'seven unique'):
                self.call()

    def test_authored_credit_denominator_unknown_policies_and_data_accounting_are_fixed(self):
        changes=[('authored_credit',1),('authored_credit',False),('authored_denominator',100),
                 ('other_scopes_policy','vendor'),('uncovered_gaps_policy','vendor'),
                 ('instruction_bytes',2152),('library_code_data_bytes',0),('library_padding_bytes',False)]
        for key,value in changes:
            saved=copy.deepcopy(self.decision);self.decision[key]=value;self.write()
            with self.subTest(key=key,value=value),self.assertRaises(ValueError):self.call()
            self.decision=saved

    def test_new_claims_reject_accepted_source_existing_vendor_and_duplicate_overlap(self):
        self.write();claims,_=self.call();row=claims['op'][0];size=self.views['op']['size']
        for kind in ('accepted-cxx-initialized-data','verified-vendor-code'):
            pieces=[dict(start=0,end=row['start'],kind='unknown'),
                    dict(start=row['start'],end=row['end'],kind=kind),
                    dict(start=row['end'],end=size,kind='unknown')]
            with self.subTest(kind=kind),self.assertRaisesRegex(ValueError,'overlap'):
                ownership.overlay_vendor(size,pieces,[row])
        with self.assertRaisesRegex(ValueError,'overlap'):
            ownership.overlay_vendor(size,ownership.partition(size,[]),[row,row])
        applied=ownership.overlay_vendor(size,ownership.partition(size,[]),[row])
        self.assertEqual([r for r in applied if r['kind']=='verified-vendor-code'],[row])


if __name__=='__main__':unittest.main()
