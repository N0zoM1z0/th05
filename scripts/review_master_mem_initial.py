#!/usr/bin/env python3
"""Prove the actual initialized four-word Master MEM.ASM prefix in each MZ."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path
from lib.pc98 import parse_mz
from lib.unit_context import UnitContext,load_unit_target
from lib.unit_oracle import relative_fixups
from review_master import pinned,stored_lzh,need,sha
from review_master_bgm_literal_data import actual_data

ROOT=Path(__file__).resolve().parents[1]
PROOF=ROOT/'config/reviewed_master_mem_initial.json'
PARENT=ROOT/'config/master_vendor_ownership.json'
OTHER=ROOT/'config/master_vendor_additions.json'
SPECS={'main':('main-calibration-b','main',0x21084,0x210a6,0x636,'209E:06C6'),
       'op':('op-calibration-a','op',0xf808,0xf808,0x356,'0EFE:0828'),
       'maine':('maine-calibration-a','mainem',0x10622,0x10612,0x456,'1010:0512')}
FIELDS=('mem_TopSeg','mem_MyOwn','mem_AllocID','mem_Reserve')


def member_bytes(raw:bytes,encoding:str)->bytes:
    text=raw.decode(encoding)
    words={}
    for field in FIELDS:
        m=re.findall(r'(?im)^\s*'+field+r'\s+dw\s+([0-9]+)\s*(?:;.*)?$',text)
        need(len(m)==1,'Master MEM scalar is not uniquely sourced: '+field)
        words[field]=int(m[0])
    need(tuple(words[f] for f in FIELDS)==(0,0,0,256),
         'Master memory allocator default values have changed')
    return b''.join(words[f].to_bytes(2,'little') for f in FIELDS)


def review():
    parent=json.loads(PARENT.read_text());others=json.loads(OTHER.read_text())
    archive=stored_lzh(pinned(ROOT,parent['inputs']['inner_archive']))
    author=archive['MEM.ASM'];data=member_bytes(author,'cp932')
    rows=[]
    for name,(build,obj,orig,cal,local,label) in SPECS.items():
        base=ROOT/'.analysis/builds'/build/'source'
        src=(base/'libs/master.lib/mem[data].asm').read_bytes()
        need(member_bytes(src,'utf8')==data,'retained TASM memory source differs')
        pin=parent['inputs'] if name=='main' else others['table_contexts'][name]['inputs']
        objdata=pinned(ROOT,pin['calibration_object']);exe=pinned(ROOT,pin['calibration_exe']);mp=pinned(ROOT,pin['calibration_map'])
        need(len(re.findall(r'(?im)^\s*'+label+r'\s+(?:idle\s+)?_?mem_TopSeg\s*$',mp.decode('cp437')))==4,
             'MEM top public not anchored to expected DATA frame')
        chunks=actual_data(objdata,local,8)
        need(len(chunks)==1 and chunks[0]['scope_offset']==0 and chunks[0]['scope_size']==8 and
             chunks[0]['scope_content_sha256']==sha(data),'MEM allocator words lack a complete TASM LEDATA')
        target_ctx=UnitContext(ROOT,name);artifact,target,_=load_unit_target(target_ctx,target_ctx.config())
        image=parse_mz(exe)
        need(image.valid and target.program_image[orig:orig+8]==data and
             image.program_image[cal:cal+8]==data,'MEM target or calibration bytes differ')
        need(relative_fixups(target,orig,8)==relative_fixups(image,cal,8)==[],
             'source constant DATA unexpectedly has MZ relocations')
        rows.append(dict(artifact=artifact['id'],start=orig,end=orig+8,
                         original_payload_sha256=sha(target.program_image),
                         original_artifact_sha256=artifact['sha256'],
                         source_sha256=sha(src),
                         omf_sha256=sha(objdata),map_sha256=sha(mp),exe_sha256=sha(exe),
                         complete_LEDATA=chunks[0],ordered_fixups=[]))
    return dict(version=1,kind='source-linked-Master-memory-defaults',author_source_sha256=sha(author),
                source_archive_sha256=parent['inputs']['inner_archive']['sha256'],
                authored_credit=0,total_bytes=24,rows=rows)


def validate(data):
    parent=json.loads(PARENT.read_text());others=json.loads(OTHER.read_text())
    author=stored_lzh(pinned(ROOT,parent['inputs']['inner_archive']))['MEM.ASM']
    byteset=member_bytes(author,'cp932')
    need(data.get('version')==1 and data.get('kind')=='source-linked-Master-memory-defaults' and
         data.get('author_source_sha256')==sha(author) and
         data.get('source_archive_sha256')==parent['inputs']['inner_archive']['sha256'] and
         data.get('authored_credit')==0 and data.get('total_bytes')==24 and len(data.get('rows',[]))==3,
         'stale/partial original Master allocator defaults')
    for row,(name,(build,obj,at,cal,local,label)) in zip(data['rows'],SPECS.items()):
        pin=parent['inputs'] if name=='main' else others['table_contexts'][name]['inputs']
        info=others['table_contexts'][name] if name!='main' else None
        expected_target=parent['inputs']['target']['sha256'] if name=='main' else info['target_sha256']
        expected_payload=parent['target_payload_sha256'] if name=='main' else info['target_payload_sha256']
        src=ROOT/'.analysis/builds'/build/'source/libs/master.lib/mem[data].asm'
        led=row.get('complete_LEDATA',{})
        need(row.get('artifact')=='th05-'+name and row.get('start')==at and row.get('end')==at+8 and
             row.get('original_payload_sha256')==expected_payload and row.get('original_artifact_sha256')==expected_target and
             row.get('source_sha256')==sha(src.read_bytes()) and row.get('omf_sha256')==pin['calibration_object']['sha256'] and
             row.get('map_sha256')==pin['calibration_map']['sha256'] and row.get('exe_sha256')==pin['calibration_exe']['sha256'] and
             led.get('scope_size')==8 and led.get('scope_offset')==0 and led.get('scope_content_sha256')==sha(byteset) and
             row.get('ordered_fixups')==[], 'wrong MEM source or OMF/target extent')


def reviewed_claims(root,views,*,verify_targets=False):
    if not PROOF.exists():return {},None
    raw=PROOF.read_bytes();data=json.loads(raw);validate(data)
    if verify_targets:need(review()==data,'actual Master memory source/native review differs')
    result={}
    for row in data['rows']:
        name=row['artifact'].removeprefix('th05-')
        need(views[name]['sha256']==row['original_payload_sha256'],'MEM source applied to a wrong target')
        result[name]=[dict(start=row['start'],end=row['end'],kind='verified-vendor-initialized-data',
                           content_kind='library-initialized-data',instruction_bytes=0,library='Master 0.23',member='MEM_INIT')]
    return result,sha(raw)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    group=p.add_mutually_exclusive_group(required=True)
    for mode in ('write','check','structural-check'):group.add_argument('--'+mode,action='store_true')
    a=p.parse_args()
    if a.write:
        proof=review();PROOF.write_text(json.dumps(proof,indent=2)+'\n')
    else:proof=json.loads(PROOF.read_text())
    validate(proof)
    if a.check:need(review()==proof,'source-linked allocator default proof changed')
    print('PASS: eight true Master allocator initialization bytes per MAIN/OP/MAINE')

if __name__=='__main__':main()
