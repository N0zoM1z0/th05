#!/usr/bin/env python3
"""Verify exact 256-byte original HFLIP LUT question-mark reserves in three MZs."""
from __future__ import annotations
import argparse,json,re
from pathlib import Path
from lib.pc98 import parse_mz
from lib.unit_context import UnitContext,load_unit_target
from lib.unit_oracle import relative_fixups
from review_master import need,pinned,sha
from review_master_compact_bss import bss_publics

ROOT=Path(__file__).resolve().parents[1]
PROOF=ROOT/'config/reviewed_hflip_lut_reservations.json'
PARENT=ROOT/'config/master_vendor_ownership.json'
OTHER=ROOT/'config/master_vendor_additions.json'
ORIGINAL=ROOT/'_reference/ReC98/th03/formats/hfliplut[bss].asm'
SPECS={
 'main':('main-calibration-b',0x2385e,'209E:2EA0',0x874,0xA080),
 'op':('op-calibration-a',0x12642,'0EFE:3662',0x86C,0x1128),
 'maine':('maine-calibration-a',0x126ee,'1010:25DE',0x86C,0x1114),
}
SIZE=256


def verified_declaration(raw:bytes):
    text=raw.decode('ascii')
    need(len(re.findall(r'(?im)^\s*public\s+_hflip_lut\s*$',text))==1 and
         len(re.findall(r'(?im)^\s*_hflip_lut\s+db\s+100h\s+dup\s*\(\s*\?\s*\)\s*$',text))==1,
         'original HFLIP LUT is not one 256-byte unwritten array')


def review():
    original=ORIGINAL.read_bytes();verified_declaration(original)
    parent=json.loads(PARENT.read_text());other=json.loads(OTHER.read_text());rows=[]
    for n,(build,at,public,local,bss_size) in SPECS.items():
        base=ROOT/'.analysis/builds'/build/'source'
        src=(base/'th03/formats/hfliplut[bss].asm').read_bytes()
        verified_declaration(src)
        need(src==original,'native HFLIP source differs from original ReC98 candidate')
        pins=parent['inputs'] if n=='main' else other['table_contexts'][n]['inputs']
        obj=pinned(ROOT,pins['calibration_object'])
        omf=bss_publics(obj,[('_hflip_lut',local)],bss_size)
        mp=pinned(ROOT,pins['calibration_map'])
        need(len(re.findall(r'(?im)^\s*'+public+r'\s+(?:idle\s+)?_hflip_lut\s*$',mp.decode('cp437')))==2,
             'native HFLIP BSS public is not at expected original DATA offset')
        c=UnitContext(ROOT,n);art,target,_=load_unit_target(c,c.config())
        need(len(target.program_image)>=at+SIZE and target.program_image[at:at+SIZE]==b'\0'*SIZE,
             'original decoded HFLIP LUT is not exactly 256 materialized zero bytes')
        need(relative_fixups(target,at,SIZE)==[],
             'unwritten HFLIP LUT contains original MZ loader fixups')
        cal=parse_mz(pinned(ROOT,pins['calibration_exe']))
        frame,off=public.split(':')
        need(cal.valid and len(cal.program_image)<=(int(frame,16)<<4)+int(off,16),
             'native calibration MZ unexpectedly source-writes HFLIP BSS')
        rows.append(dict(artifact=art['id'],start=at,end=at+SIZE,
                original_artifact_sha256=art['sha256'],
                original_payload_sha256=sha(target.program_image),
                original_source_sha256=sha(original),
                native_source_sha256=sha(src),
                native_omf_sha256=sha(obj),
                native_map_sha256=sha(mp),
                native_exe_sha256=pins['calibration_exe']['sha256'],
                complete_unwritten_BSS=omf,ordered_fixups=[],initialized_source_bytes=0))
    return dict(version=1,kind='ReC98-original-game-HFLIP-unwritten-256-byte-arrays',
          classification='reviewed-uninitialized-game-storage',
          original_source_sha256=sha(original),total_reserve_bytes=768,
          authored_credit=0,scopes=rows)


def validate(proof):
    original=ORIGINAL.read_bytes();verified_declaration(original)
    parent=json.loads(PARENT.read_text());other=json.loads(OTHER.read_text())
    need(proof.get('version')==1 and
         proof.get('kind')=='ReC98-original-game-HFLIP-unwritten-256-byte-arrays' and
         proof.get('classification')=='reviewed-uninitialized-game-storage' and
         proof.get('original_source_sha256')==sha(original) and
         proof.get('total_reserve_bytes')==768 and proof.get('authored_credit')==0 and
         len(proof.get('scopes',[]))==3,
         'stale/partial original HFLIP uninitialized source evidence')
    for row,(n,(build,at,public,local,bss_size)) in zip(proof['scopes'],SPECS.items()):
        pins=parent['inputs'] if n=='main' else other['table_contexts'][n]['inputs']
        info=other['table_contexts'][n] if n!='main' else None
        artsha=parent['inputs']['target']['sha256'] if n=='main' else info['target_sha256']
        payloadsha=parent['target_payload_sha256'] if n=='main' else info['target_payload_sha256']
        src=ROOT/'.analysis/builds'/build/'source/th03/formats/hfliplut[bss].asm'
        obj=pinned(ROOT,pins['calibration_object'])
        need(row.get('artifact')=='th05-'+n and row.get('start')==at and row.get('end')==at+SIZE and
             row.get('original_artifact_sha256')==artsha and
             row.get('original_payload_sha256')==payloadsha and
             row.get('original_source_sha256')==sha(original) and
             row.get('native_source_sha256')==sha(src.read_bytes()) and
             row.get('native_omf_sha256')==pins['calibration_object']['sha256'] and
             row.get('native_map_sha256')==pins['calibration_map']['sha256'] and
             row.get('native_exe_sha256')==pins['calibration_exe']['sha256'] and
             row.get('complete_unwritten_BSS')==bss_publics(obj,[('_hflip_lut',local)],bss_size) and
             row.get('ordered_fixups')==[] and row.get('initialized_source_bytes')==0,
             'original HFLIP source or actual TASM BSS target scope changed')


def reviewed_claims(root,views,*,verify_targets=False):
    if not PROOF.exists():return {},None
    raw=PROOF.read_bytes();proof=json.loads(raw);validate(proof)
    if verify_targets:need(review()==proof,'native HFLIP BSS original source check changed')
    claims={}
    for row in proof['scopes']:
        n=row['artifact'].removeprefix('th05-')
        need(views[n]['sha256']==row['original_payload_sha256'],
             'HFLIP LUT BSS evidence belongs to another target')
        claims[n]=[dict(start=row['start'],end=row['end'],
                    kind='reviewed-uninitialized-game-storage',
                    content_kind='source-question-mark-reserve',
                    source='th03/formats/hfliplut[bss].asm',
                    member='_hflip_lut',instruction_bytes=0,authored_credit=0)]
    return claims,sha(raw)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    group=p.add_mutually_exclusive_group(required=True)
    for x in ('write','check','structural-check'):group.add_argument('--'+x,action='store_true')
    opts=p.parse_args()
    if opts.write:
        result=review();PROOF.write_text(json.dumps(result,indent=2)+'\n')
    else:result=json.loads(PROOF.read_text())
    validate(result)
    if opts.check:need(result==review(),'real original HFLIP source proof changed')
    print('PASS: 3 exact original 256-byte unwritten HFLIP LUTs; zero authored credit')

if __name__=='__main__':main()
