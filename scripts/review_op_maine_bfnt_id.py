#!/usr/bin/env python3
"""Verify original six-byte Master BFNT identifier in OP and MAINE only.

MAIN already has independent BFNT ownership. All source-side padding before
these two symbols is excluded rather than credited as initialized DATA.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

from lib.pc98 import parse_mz
from lib.unit_context import UnitContext, load_unit_target
from lib.unit_oracle import relative_fixups
from review_main_master_literal_tables import source_payload
from review_master import need,pinned,sha,stored_lzh
from review_master_bgm_literal_data import actual_data

ROOT=Path(__file__).resolve().parents[1]
PROOF=ROOT/'config/reviewed_op_maine_bfnt_id.json'
PARENT=ROOT/'config/master_vendor_ownership.json'
OTHER=ROOT/'config/master_vendor_additions.json'
SOURCE='libs/master.lib/bfnt_id[data].asm'
ROWS={
 'op':('op-calibration-a','op.obj',0xF4BA,0xF4BA,0x08,'0EFE:04DA'),
 'maine':('maine-calibration-a','mainem.obj',0x102D4,0x102C4,0x108,'1010:01C4'),
}
DATA=b'BFNT\x1a\x00'


def review():
    parent=json.loads(PARENT.read_text());other=json.loads(OTHER.read_text())
    archive=stored_lzh(pinned(ROOT,parent['inputs']['inner_archive']))
    author=archive['BFNTID.ASM']
    need(source_payload(author,'BFNT_ID','cp932',undf=100)==DATA,
         'original Master BFNT header identity changed')
    scopes=[]
    for name,(build,objname,start,calstart,local,public) in ROWS.items():
        root=ROOT/'.analysis/builds'/build/'source'
        source=(root/SOURCE).read_bytes()
        need(source_payload(source,'BFNT_ID','utf8',undf=100)==DATA,
             'retained native BFNT identifier differs from original author')
        pins=other['table_contexts'][name]['inputs']
        obj=pinned(ROOT,pins['calibration_object'])
        mapping=pinned(ROOT,pins['calibration_map'])
        exe=pinned(ROOT,pins['calibration_exe'])
        for label in ('BFNT_ID','_BFNT_ID'):
            need(len(re.findall(r'(?im)^\s*'+public+r'\s+(?:idle\s+)?'+label+r'\s*$',
                                mapping.decode('cp437')))==2,
                 'real original BFNT MAP public differs: '+name+' '+label)
        led=actual_data(obj,local,len(DATA))
        need(len(led)==1 and led[0]['scope_offset']==0 and
             led[0]['scope_size']==len(DATA) and led[0]['scope_content_sha256']==sha(DATA),
             'native TASM object lacks one complete BFNT initialized source scope')
        ctx=UnitContext(ROOT,name)
        art,target,_=load_unit_target(ctx,ctx.config())
        cal=parse_mz(exe)
        need(cal.valid and target.program_image[start:start+len(DATA)]==DATA and
             cal.program_image[calstart:calstart+len(DATA)]==DATA,
             'original or calibrated BFNT header differs')
        need(target.program_image.find(DATA)==start and
             target.program_image.find(DATA,start+1)<0,
             'original BFNT identifier is not unique at the proven address')
        need(relative_fixups(target,start,len(DATA))==relative_fixups(cal,calstart,len(DATA))==[],
             'BFNT header is not relocation-free original initialized DATA')
        scopes.append(dict(artifact=art['id'],start=start,end=start+len(DATA),
                           calibration_start=calstart,source_sha256=sha(source),
                           exact_BFNT_sha256=sha(DATA),
                           original_target_sha256=art['sha256'],
                           original_payload_sha256=sha(target.program_image),
                           actual_omf_sha256=sha(obj),actual_map_sha256=sha(mapping),
                           calibration_exe_sha256=sha(exe),
                           genuine_LED=led[0],ordered_original_fixups=[]))
    return dict(version=1,kind='original-Master-BFNT-header-op-maine',
                classification='third-party-library-initialized-data',
                authored_credit=0,newly_reviewed_bytes=12,
                previous_MAIN_BFNT_copy_not_claimed=True,
                original_author_sha256=sha(author),
                archive_sha256=parent['inputs']['inner_archive']['sha256'],
                scopes=scopes)


def validate(proof):
    parent=json.loads(PARENT.read_text());other=json.loads(OTHER.read_text())
    author=stored_lzh(pinned(ROOT,parent['inputs']['inner_archive']))['BFNTID.ASM']
    need(source_payload(author,'BFNT_ID','cp932',undf=100)==DATA and
         proof.get('version')==1 and proof.get('kind')=='original-Master-BFNT-header-op-maine' and
         proof.get('classification')=='third-party-library-initialized-data' and
         proof.get('authored_credit')==0 and proof.get('newly_reviewed_bytes')==12 and
         proof.get('previous_MAIN_BFNT_copy_not_claimed') is True and
         proof.get('original_author_sha256')==sha(author) and
         proof.get('archive_sha256')==parent['inputs']['inner_archive']['sha256'] and
         len(proof.get('scopes',[]))==2,
         'stale/partial Master BFNT header source review')
    existing=json.loads((ROOT/'config/main_master_literal_tables_ownership.json').read_text())
    previous=[r for r in existing['scope_rows'] if r['member']=='BFNT_ID']
    need(len(previous)==1 and previous[0]['DATA_sha256']==sha(DATA) and
         previous[0]['start']==0x20D36 and previous[0]['end']==0x20D3C,
         'MAIN BFNT source owner must remain distinct and unchanged')
    for row,(name,(build,startobj,st,cal,local,public)) in zip(proof['scopes'],ROWS.items()):
        pins=other['table_contexts'][name]['inputs']
        context=other['table_contexts'][name]
        led=row.get('genuine_LED',{})
        src=ROOT/'.analysis/builds'/build/'source'/SOURCE
        need(row.get('artifact')=='th05-'+name and row.get('start')==st and
             row.get('end')==st+6 and row.get('calibration_start')==cal and
             row.get('source_sha256')==sha(src.read_bytes()) and
             row.get('exact_BFNT_sha256')==sha(DATA) and
             row.get('original_target_sha256')==context['target_sha256'] and
             row.get('original_payload_sha256')==context['target_payload_sha256'] and
             row.get('actual_omf_sha256')==pins['calibration_object']['sha256'] and
             row.get('actual_map_sha256')==pins['calibration_map']['sha256'] and
             row.get('calibration_exe_sha256')==pins['calibration_exe']['sha256'] and
             led.get('scope_offset')==0 and led.get('scope_size')==6 and
             led.get('scope_content_sha256')==sha(DATA) and
             row.get('ordered_original_fixups')==[],
             'wrong Master BFNT source or actual MZ/TASM extent')


def reviewed_claims(root,views,*,verify_targets=False):
    if not PROOF.exists():return {},None
    raw=PROOF.read_bytes();proof=json.loads(raw);validate(proof)
    if verify_targets:need(proof==review(),'original OP/MAINE BFNT source review differs')
    result={}
    for row in proof['scopes']:
        name=row['artifact'].removeprefix('th05-')
        need(views[name]['sha256']==row['original_payload_sha256'],
             'BFNT source was verified against a different original program')
        result[name]=[dict(start=row['start'],end=row['end'],
                           kind='verified-vendor-initialized-data',
                           content_kind='library-initialized-data',instruction_bytes=0,
                           library='Master 0.23',member='BFNT_ID')]
    return result,sha(raw)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    g=p.add_mutually_exclusive_group(required=True)
    for flag in ('write','check','structural-check'):g.add_argument('--'+flag,action='store_true')
    a=p.parse_args()
    if a.write:j=review();PROOF.write_text(json.dumps(j,indent=2)+'\n')
    else:j=json.loads(PROOF.read_text())
    validate(j)
    if a.check:need(j==review(),'original BFNT source and native link proof changed')
    print('PASS: six source-authored BFNT marker bytes in OP and MAINE, no MAIN duplicate')

if __name__=='__main__':main()
