#!/usr/bin/env python3
"""Source-backed original Master 0.23 BYTE_MASK in OP and MAINE only."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re

from lib.pc98 import parse_mz
from lib.unit_context import UnitContext,load_unit_target
from lib.unit_oracle import relative_fixups
from review_master import need,pinned,sha,stored_lzh
from review_main_master_literal_tables import source_payload
from review_master_bgm_literal_data import actual_data,digest

ROOT=Path(__file__).resolve().parents[1]
SOURCE_PROOF='config/main_master_literal_tables_ownership.json'
CONTEXT_PROOF='config/master_vendor_additions.json'
PROOF='config/master_byte_mask_op_maine_ownership.json'
DECISION='config/reviewed_master_byte_mask_op_maine.json'
COORDS={'op':(0xF800,0xF800,0x0EFE,0x0EFE,0x4D2),
        'maine':(0x1061A,0x1060A,0x1011,0x1010,0xBC)}


def review():
    source=json.loads((ROOT/SOURCE_PROOF).read_text())
    main=next(r for r in source['scope_rows'] if r['member']=='BYTE_MASK')
    context=json.loads((ROOT/CONTEXT_PROOF).read_text())
    upstream=json.loads((ROOT/'config/master_vendor_ownership.json').read_text())
    archive=stored_lzh(pinned(ROOT,upstream['inputs']['inner_archive']))
    body=source_payload(archive['WORDMASK.ASM'],'BYTE_MASK','cp932',undf=100)
    need(len(body)==8 and sha(body)==main['DATA_sha256'],
         'original Master BYTE_MASK is not the already reviewed MAIN table')
    scopes=[]
    for name,(start,cal_start,ds,cal_ds,base) in COORDS.items():
        inputs=context['table_contexts'][name]['inputs']
        pin={'exe':inputs['calibration_exe']['sha256'],
             'map':inputs['calibration_map']['sha256']}
        root=ROOT/context['table_contexts'][name]['source_root']
        native_source=(root/'libs/master.lib/wordmask[data].asm').read_bytes()
        need(source_payload(native_source,'BYTE_MASK','utf8',undf=100)==body,
             'actual Master BYTE_MASK assembler source differs')
        cal_exe=pinned(ROOT,inputs['calibration_exe'])
        cal_map=pinned(ROOT,inputs['calibration_map'])
        obj=pinned(ROOT,inputs['calibration_object'])
        need(sha(cal_exe)==pin['exe'] and sha(cal_map)==pin['map'],
             'retained BYTE_MASK calibration identities differ')
        cal=parse_mz(cal_exe)
        ctx=UnitContext(ROOT,name);art,target,_=load_unit_target(ctx,ctx.config())
        need(target.program_image[start:start+8]==body and
             cal.program_image[cal_start:cal_start+8]==body and
             target.program_image.find(body)==start and
             target.program_image.find(body,start+1)<0,
             'original 8-byte BYTE_MASK is not unique or source-exact')
        need(not relative_fixups(target,start,8) and
             not relative_fixups(cal,cal_start,8),'BYTE_MASK has unexpected relocation')
        map_label=f'{cal_ds:04X}:{cal_start-cal_ds*16:04X}'
        need(len(re.findall(r'(?im)^\s*'+map_label+r'\s+(?:idle\s+)?BYTE_MASK\s*$',
                cal_map.decode('cp437')))==2,'real BYTE_MASK MAP public differs')
        local=cal_start-(cal_ds*16+base)
        chunks=actual_data(obj,local,8)
        need(len(chunks)==1 and chunks[0]['scope_offset']==0 and
             chunks[0]['scope_size']==8 and chunks[0]['scope_content_sha256']==sha(body),
             'native BYTE_MASK has incomplete/relocated OMF source writes')
        scopes.append(dict(id=name+'-master-byte-mask',artifact=art['id'],
                           original_start=start,original_end=start+8,
                           calibration_start=cal_start,source_sha256=sha(native_source),
                           data_sha256=sha(body),actual_OMF_LEDATAs=chunks,
                           target_sha256=art['sha256'],
                           target_payload_sha256=sha(target.program_image),
                           target_size=len(target.program_image),
                           calibration_exe_sha256=sha(cal_exe),
                           calibration_map_sha256=sha(cal_map),
                           calibration_object_sha256=sha(obj),
                           original_ordered_fixups=[],calibration_ordered_fixups=[]))
    return dict(schema_version=1,kind='Master-BYTE_MASK-original-source-linked-DATA',
                classification='third-party-library-initialized-data',
                authored_credit=0,total_bytes=16,
                upstream_source_sha256=sha(archive['WORDMASK.ASM']),
                primary_proof_sha256=digest(SOURCE_PROOF),
                context_proof_sha256=digest(CONTEXT_PROOF),scopes=scopes)


def validate(proof):
    need(proof.get('schema_version')==1 and
         proof.get('kind')=='Master-BYTE_MASK-original-source-linked-DATA' and
         proof.get('classification')=='third-party-library-initialized-data' and
         proof.get('authored_credit')==0 and proof.get('total_bytes')==16 and
         proof.get('primary_proof_sha256')==digest(SOURCE_PROOF) and
         proof.get('context_proof_sha256')==digest(CONTEXT_PROOF),
         'stale source-linked Master BYTE_MASK evidence')
    source=json.loads((ROOT/SOURCE_PROOF).read_text())
    main=next(r for r in source['scope_rows'] if r['member']=='BYTE_MASK')
    need(proof.get('upstream_source_sha256')==main['author_source_sha256'],
         'not original Master author BYTE_MASK')
    context=json.loads((ROOT/CONTEXT_PROOF).read_text())
    scopes=proof.get('scopes',[])
    need(len(scopes)==2,'partial Master BYTE_MASK decision')
    for row,(name,(start,cal_start,ds,cal_ds,base)) in zip(scopes,COORDS.items()):
        inputs=context['table_contexts'][name]['inputs']
        target=context['table_contexts'][name]
        source=ROOT/target['source_root']/'libs/master.lib/wordmask[data].asm'
        chunks=row.get('actual_OMF_LEDATAs',[])
        need(row.get('id')==name+'-master-byte-mask' and
             row.get('artifact')=='th05-'+name and
             row.get('original_start')==start and row.get('original_end')==start+8 and
             row.get('calibration_start')==cal_start and
             row.get('source_sha256')==sha(source.read_bytes()) and
             row.get('data_sha256')==main['DATA_sha256'] and
             row.get('target_sha256')==target['target_sha256'] and
             row.get('target_payload_sha256')==target['target_payload_sha256'] and
             row.get('target_size')==target['target_view']['payload_size'] and
             row.get('calibration_exe_sha256')==inputs['calibration_exe']['sha256'] and
             row.get('calibration_map_sha256')==inputs['calibration_map']['sha256'] and
             row.get('calibration_object_sha256')==inputs['calibration_object']['sha256'] and
             row.get('original_ordered_fixups')==row.get('calibration_ordered_fixups')==[] and
             len(chunks)==1 and chunks[0]['scope_offset']==0 and
             chunks[0]['scope_size']==8 and chunks[0]['scope_content_sha256']==main['DATA_sha256'],
             'Master BYTE_MASK original/context/OMF identities differ')


def reviewed_claims(root,views,*,verify_targets=False):
    if not (root/DECISION).exists():return {},None
    raw=(root/PROOF).read_bytes();proof=json.loads(raw);validate(proof)
    decision_raw=(root/DECISION).read_bytes()
    need(json.loads(decision_raw)==dict(schema_version=1,
         decision='ADOPT_ONLY_OP_MAINE_MASTER_BYTE_MASK',
         classification='third-party-library-initialized-data',authored_credit=0,
         evidence_sha256=sha(raw),scopes=[r['id'] for r in proof['scopes']]),
         'unreviewed Master BYTE_MASK adoption')
    if verify_targets: need(review()==proof,'native byte mask source proof changed')
    claims={}
    for row in proof['scopes']:
        name=row['artifact'].removeprefix('th05-')
        need(views[name]['size']==row['target_size'] and
             views[name]['sha256']==row['target_payload_sha256'],
             'BYTE_MASK original decoded view changed')
        claims[name]=[{'start':row['original_start'],'end':row['original_end'],
            'kind':'verified-vendor-initialized-data','content_kind':'library-initialized-data',
            'instruction_bytes':0,'library':'Master 0.23',
            'member':'BYTE_MASK','scope_id':row['id']}]
    return claims,sha(decision_raw)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    g=p.add_mutually_exclusive_group(required=True)
    for mode in ('write','check','structural-check'):g.add_argument('--'+mode,action='store_true')
    args=p.parse_args()
    if args.write:
        proof=review();(ROOT/PROOF).write_text(json.dumps(proof,indent=2)+'\n')
        (ROOT/DECISION).write_text(json.dumps(dict(schema_version=1,
            decision='ADOPT_ONLY_OP_MAINE_MASTER_BYTE_MASK',
            classification='third-party-library-initialized-data',authored_credit=0,
            evidence_sha256=sha((ROOT/PROOF).read_bytes()),
            scopes=[r['id'] for r in proof['scopes']]),indent=2)+'\n')
    else:proof=json.loads((ROOT/PROOF).read_text())
    validate(proof)
    if args.check:need(review()==proof,'native source-linked BYTE_MASK evidence changed')
    print('PASS: original OP/MAINE Master BYTE_MASK two complete 8-byte DATA sources')


if __name__=='__main__':main()
