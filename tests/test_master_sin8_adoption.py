"""Explicit SIN8 vendor DATA adoption cannot become CODE or authored recovery."""
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
import review_master_sin8 as review


class Sin8AdoptionTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup);self.root=Path(temp.name)
        for p in [*review.SOURCES,review.PROOF,review.CONTEXT_PROOF,review.context.BASE_PROOF]:
            destination=self.root/p;destination.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/p,destination)
        self.path=self.root/'config/reviewed_master_sin8.json'
        self.decision=json.loads((ROOT/'config/reviewed_master_sin8.json').read_text())
        self.views=tomllib.loads((ROOT/'config/ownership.toml').read_text())['views']
        self.targets={r['id']:r for r in tomllib.loads((ROOT/'config/targets.toml').read_text())['artifacts']}

    def write(self):self.path.write_text(json.dumps(self.decision))

    def call(self,native=False):
        return ownership.reviewed_master_sin8(self.root,views=self.views,targets=self.targets,verify_targets=native)

    def test_missing_decision_means_no_claims_even_with_native_flag(self):
        with patch.object(review,'review_inputs')as replay:
            self.assertEqual(self.call(True),({},None));replay.assert_not_called()

    def test_exact_three_DATA_claims_use_original_positions_and_zero_instructions(self):
        self.write();claims,digest=self.call();proof=json.loads((ROOT/review.PROOF).read_text())
        self.assertEqual({k:len(v)for k,v in claims.items()},dict(main=1,op=1,maine=1))
        for row in proof['scopes']:
            name=row['artifact'].removeprefix('th05-');claim=claims[name][0]
            self.assertEqual((claim['start'],claim['end']),(row['original_start'],row['original_end']))
            self.assertEqual(claim['kind'],'verified-vendor-initialized-data')
            self.assertEqual(claim['content_kind'],'library-initialized-data')
            self.assertEqual((claim['instruction_bytes'],claim['scope_id']),(0,row['id']))
        self.assertEqual(sum(r['end']-r['start']for values in claims.values()for r in values),1920)
        self.assertEqual(digest,ownership.digest_bytes(self.path.read_bytes()))

    def test_native_replay_once_for_all_three_contexts_never_saved_status(self):
        self.write();result=dict(kind='native-SIN8-initialized-data-review',scopes=3,full_bytes=1920,
            instruction_bytes=0,byte_proof_replayed=True,decision='PROPOSAL',authored_credit=0,
            compiler_invocations=0,authored_denominator=None)
        with patch.object(review,'review_inputs',return_value=result)as replay:
            claims,_=self.call(True);self.assertEqual(len(claims),3)
            replay.assert_called_once();self.assertEqual(replay.call_args.kwargs,{'root':self.root})
        with patch.object(review,'review_inputs',return_value={'status':'PASS'}):
            with self.assertRaisesRegex(ValueError,'actual initialized DATA'):self.call(True)

    def test_stale_proof_and_CODE_kind_or_classification_reject(self):
        for key,value in [('evidence_sha256','0'*64),('claim_kind','verified-vendor-code'),
                          ('classification','third-party-library-code'),('decision','ADOPT_ALL_DATA')]:
            saved=copy.deepcopy(self.decision);self.decision[key]=value;self.write()
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,'stale|kind'):self.call()
            self.decision=saved

    def test_wrong_artifact_packed_payload_size_and_original_view_reject(self):
        for mode in ('context','packed','payload','size','manifest','view','missing'):
            saved=copy.deepcopy((self.decision,self.targets,self.views))
            row=self.decision['artifacts']['main']
            if mode=='context':row['artifact']='th05-maine'
            elif mode=='packed':row['target_sha256']=self.decision['artifacts']['op']['target_sha256']
            elif mode=='payload':row['target_payload_sha256']=row['target_sha256']
            elif mode=='size':row['target_payload_size']+=1
            elif mode=='manifest':self.targets['th05-main']['sha256']='0'*64
            elif mode=='view':self.views['op']['sha256']='0'*64
            else:self.decision['artifacts'].pop('op')
            self.write()
            with self.subTest(mode=mode),self.assertRaisesRegex(ValueError,'context|artifact'):self.call()
            self.decision,self.targets,self.views=saved

    def test_unknown_duplicate_partial_or_CODE_scope_selection_rejects(self):
        original=self.decision['scopes'][:]
        for ids in [original[:-1],original+[original[0]],original[:-1]+['op-rottbl'],original[:-1]+['unknown']]:
            self.decision['scopes']=ids;self.write()
            with self.subTest(ids=ids),self.assertRaisesRegex(ValueError,'three unique'):self.call()

    def test_zero_authored_and_instruction_credit_unknown_gap_policies_are_required(self):
        for key,value in [('authored_credit',1),('authored_credit',False),('authored_denominator',1920),
                          ('instruction_bytes',1920),('instruction_bytes',False),('full_bytes',1280),
                          ('other_scopes_policy','vendor'),('uncovered_gaps_policy','vendor')]:
            saved=copy.deepcopy(self.decision);self.decision[key]=value;self.write()
            with self.subTest(key=key,value=value),self.assertRaises(ValueError):self.call()
            self.decision=saved

    def test_overlay_requires_exact_DATA_content_kind_and_zero_instructions(self):
        self.write();claims,_=self.call();row=claims['op'][0];size=self.views['op']['size']
        for changed in [dict(kind='verified-vendor-code'),dict(kind='unreviewed-data'),
                        dict(content_kind='library-instructions'),dict(content_kind=None),
                        dict(instruction_bytes=640),dict(instruction_bytes=False)]:
            with self.subTest(changed=changed),self.assertRaises(ValueError):
                ownership.overlay_vendor(size,ownership.partition(size,[]),[{**row,**changed}])
        result=ownership.overlay_vendor(size,ownership.partition(size,[]),[row])
        self.assertEqual([r for r in result if r['kind']=='verified-vendor-initialized-data'],[row])

    def test_DATA_cannot_displace_accepted_source_CODE_DATA_or_another_vendor(self):
        self.write();claims,_=self.call();row=claims['main'][0];size=self.views['main']['size']
        for kind in ['accepted-c-initialized-data','accepted-cxx-instructions',
                     'verified-vendor-code','verified-vendor-initialized-data']:
            existing=[dict(start=0,end=row['start'],kind='unknown'),
                      dict(start=row['start'],end=row['end'],kind=kind),
                      dict(start=row['end'],end=size,kind='unknown')]
            with self.subTest(kind=kind),self.assertRaisesRegex(ValueError,'overlap'):
                ownership.overlay_vendor(size,existing,[row])
        with self.assertRaisesRegex(ValueError,'overlap'):
            ownership.overlay_vendor(size,ownership.partition(size,[]),[row,row])


if __name__=='__main__':unittest.main()
