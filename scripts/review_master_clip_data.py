#!/usr/bin/env python3
"""Source-backed eight-word Master CLIP initializer in MAIN/OP/MAINE."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re

from lib.pc98 import parse_mz
from lib.unit_context import UnitContext,load_unit_target
from lib.unit_oracle import relative_fixups
from review_master import pinned,stored_lzh,need,sha
from review_master_bgm_literal_data import actual_data

ROOT=Path(__file__).resolve().parents[1]
PROOF=ROOT/'config/reviewed_master_clip_data.json'
PARENT=ROOT/'config/master_vendor_ownership.json'
OTHER=ROOT/'config/master_vendor_additions.json'
MEMBER='libs/master.lib/clip[data].asm'
FIELDS=('ClipXL','ClipXW','ClipXR','ClipYT','ClipYH','ClipYB','ClipYT_seg','ClipYB_adr')
TARGETS={
    'main':(0x20d3c,0x20d5e,0x2ee,'209E:037E','main-calibration-b','main'),
    'op':(0xf4c0,0xf4c0,0x0e,'0EFE:04E0','op-calibration-a','op'),
    'maine':(0x102da,0x102ca,0x10e,'1010:01CA','maine-calibration-a','mainem'),
}


def clip_values(raw:bytes,encoding:str)->bytes:
    text=raw.decode(encoding)
    rows={}
    for name,raw_value in re.findall(r'(?im)^\s*(Clip\w+)\s+dw\s+([^;\r\n]+)',text):
        if name not in FIELDS:continue
        value=raw_value.strip().lower().replace(' ','')
        if value=='399*80':number=399*80
        elif value.endswith('h'):number=int(value[:-1],16)
        else:number=int(value)
        need(0<=number<=0xffff and name not in rows,'nonconstant or repeated Master clip word')
        rows[name]=number
    need(set(rows)==set(FIELDS),'missing original Master clipping field')
    return b''.join(rows[name].to_bytes(2,'little') for name in FIELDS)


def review()->dict:
    parent=json.loads(PARENT.read_text());other=json.loads(OTHER.read_text())
    author=stored_lzh(pinned(ROOT,parent['inputs']['inner_archive']))['CLIP.ASM']
    values=clip_values(author,'cp932')
    need(len(values)==16 and values==bytes.fromhex('00 00 7f 02 7f 02 00 00 8f 01 8f 01 00 a8 b0 7c'),
         'original Master 16-byte clip initializer changed')
    entries=[]
    for name,(original_start,cal_start,local,label,build,objname) in TARGETS.items():
        base=ROOT/'.analysis/builds'/build/'source'
        source=(base/MEMBER).read_bytes()
        need(clip_values(source,'utf8')==values,
             'retained TASM clipping source differs from original Master archive')
        obj=(base/f'obj/th05/{objname}.obj').read_bytes()
        pieces=actual_data(obj,local,16)
        need(len(pieces)==1 and pieces[0]['scope_offset']==0 and
             pieces[0]['scope_size']==16 and pieces[0]['scope_content_sha256']==sha(values),
             'complete source-written clip segment has unexpected OMF LEDATA')
        if name=='main':
            pins=parent['inputs']
        else:
            pins=other['table_contexts'][name]['inputs']
        exe=pinned(ROOT,pins['calibration_exe'])
        mapping=pinned(ROOT,pins['calibration_map'])
        need(len(re.findall(r'(?im)^\s*'+label+r'\s+(?:idle\s+)?_?ClipXL\s*$',
                            mapping.decode('cp437')))==4,
             'calibration does not export both original clipping public spellings')
        calibration=parse_mz(exe)
        ctx=UnitContext(ROOT,name);artifact,target,_=load_unit_target(ctx,ctx.config())
        need(calibration.valid and
             calibration.program_image[cal_start:cal_start+16]==values and
             target.program_image[original_start:original_start+16]==values,
             'calibration/original complete clipping DATA differs from source')
        need(target.program_image.find(values)==original_start and
             target.program_image.find(values,original_start+1)<0,
             'clipping table is not unique in native image')
        need(relative_fixups(calibration,cal_start,16)==relative_fixups(target,original_start,16)==[],
             'clip words should not contain segment relocations')
        entries.append(dict(artifact=artifact['id'],start=original_start,end=original_start+16,
             calibration_start=cal_start,segment_local=local,source_sha256=sha(source),
             actual_omf_sha256=sha(obj),actual_map_sha256=sha(mapping),
             calibration_exe_sha256=sha(exe),target_sha256=artifact['sha256'],
             target_payload_sha256=sha(target.program_image),
             real_clip_LEDATA=pieces[0], ordered_MZ_fixups=[]))
    return dict(schema_version=1,kind='original-master-clip-initialized-data',
                classification='third-party-library-initialized-data',
                original_author_sha256=sha(author),original_data_sha256=sha(values),
                parent_source_sha256=sha(PARENT.read_bytes()),
                other_source_sha256=sha(OTHER.read_bytes()),
                authored_credit=0,total_bytes=48,scopes=entries)


def validate(data:dict)->None:
    parent=json.loads(PARENT.read_text());other=json.loads(OTHER.read_text())
    author=stored_lzh(pinned(ROOT,parent['inputs']['inner_archive']))['CLIP.ASM']
    vals=clip_values(author,'cp932')
    need(data.get('schema_version')==1 and data.get('kind')=='original-master-clip-initialized-data' and
         data.get('classification')=='third-party-library-initialized-data' and
         data.get('authored_credit')==0 and data.get('total_bytes')==48 and
         data.get('original_author_sha256')==sha(author) and
         data.get('original_data_sha256')==sha(vals) and
         data.get('parent_source_sha256')==sha(PARENT.read_bytes()) and
         data.get('other_source_sha256')==sha(OTHER.read_bytes()),
         'stale Master clipping author/target provenance')
    entries=data.get('scopes',[])
    need(len(entries)==3,'not all three clip tables reviewed')
    for row,(name,(start,cal_start,local,label,build,objname)) in zip(entries,TARGETS.items()):
        base=ROOT/'.analysis/builds'/build/'source'
        pins=parent['inputs'] if name=='main' else other['table_contexts'][name]['inputs']
        need(row.get('artifact')=='th05-'+name and row.get('start')==start and
             row.get('end')==start+16 and row.get('calibration_start')==cal_start and
             row.get('segment_local')==local and row.get('ordered_MZ_fixups')==[] and
             row.get('source_sha256')==sha((base/MEMBER).read_bytes()) and
             row.get('actual_omf_sha256')==pins['calibration_object']['sha256'] and
             row.get('actual_map_sha256')==pins['calibration_map']['sha256'] and
             row.get('calibration_exe_sha256')==pins['calibration_exe']['sha256'] and
             row.get('target_sha256')==(parent['inputs']['target']['sha256'] if name=='main' else other['table_contexts'][name]['target_sha256']) and
             row.get('target_payload_sha256')==(parent['target_payload_sha256'] if name=='main' else other['table_contexts'][name]['target_payload_sha256']) and
             row.get('real_clip_LEDATA',{}).get('scope_offset')==0 and
             row.get('real_clip_LEDATA',{}).get('scope_size')==16 and
             row.get('real_clip_LEDATA',{}).get('scope_content_sha256')==sha(vals),
             'stale clipping source/OMF/target or incomplete DATA extent')


def reviewed_claims(root:Path,views:dict,*,verify_targets=False):
    if not (root/'config/reviewed_master_clip_data.json').exists():return {},None
    raw=(root/'config/reviewed_master_clip_data.json').read_bytes()
    proof=json.loads(raw);validate(proof)
    if verify_targets:need(review()==proof,'native Master 16-byte clipping source replay changed')
    result={}
    for row in proof['scopes']:
        name=row['artifact'].removeprefix('th05-')
        need(views[name]['sha256']==row['target_payload_sha256'],
             'foreign clip DATA belongs to another original target')
        result[name]=[dict(start=row['start'],end=row['end'],kind='verified-vendor-initialized-data',
                           content_kind='library-initialized-data',instruction_bytes=0,
                           library='Master 0.23',member='CLIP_INITIAL')]
    return result,sha(raw)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    g=p.add_mutually_exclusive_group(required=True)
    for action in ('write','check','structural-check'):g.add_argument('--'+action,action='store_true')
    a=p.parse_args()
    if a.write:
        record=review();PROOF.write_text(json.dumps(record,indent=2)+'\n')
    else:record=json.loads(PROOF.read_text())
    validate(record)
    if a.check:need(record==review(),'original Master CLIP source/native bytes have changed')
    print('PASS: 16 source-written clip DATA bytes in each of MAIN, OP, MAINE')

if __name__=='__main__':main()
