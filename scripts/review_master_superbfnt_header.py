#!/usr/bin/env python3
"""Original Master SUPERBFT BFNT header: 32 source-unwritten bytes per EXE.

The author declared `header bfnt_header <>`, all 32 structure bytes '?' in
SUPER.INC. The monolithic native TASM _DATA has a 32-byte LEDATA gap.
"""
from __future__ import annotations
import argparse,json,re
from pathlib import Path
from lib.omf import parse_omf
from lib.unit_extents import _index
from lib.pc98 import parse_mz
from lib.unit_context import UnitContext,load_unit_target
from lib.unit_oracle import relative_fixups
from review_master import pinned,stored_lzh,sha,need

ROOT=Path(__file__).resolve().parents[1]
PROOF=ROOT/'config/reviewed_master_superbfnt_header.json'
PARENT=ROOT/'config/master_vendor_ownership.json'
OTHER=ROOT/'config/master_vendor_additions.json'
SPECS={
    'main':('main-calibration-b','main',0x2108c,0x210ae,0x63e),
    'op':('op-calibration-a','op',0xf810,0xf810,0x35e),
    'maine':('maine-calibration-a','mainem',0x1062a,0x1061a,0x45e),
}
SIZE=32


def original_layout(author:dict):
    text=author['SUPERBFT.ASM'].decode('cp932')
    header=author['SUPER.INC'].decode('cp932')
    need(len(re.findall(r'(?im)^\s*header\s+bfnt_header\s*<>\s*$',text))==1,
         'original Master BFNT source no longer declares its template')
    begin=re.search(r'(?ims)^\s*bfnt_header\s+STRUC\s*(.*?)^\s*bfnt_header\s+ENDS\s*$',header)
    need(begin is not None,'original Master BFNT header type is missing')
    fields=[]
    for line in begin[1].splitlines():
        row=line.split(';',1)[0].strip()
        if not row:continue
        m=re.fullmatch(r'([A-Za-z][\w]*)\s+(DB|DW|DD)\s+(?:([0-9]+)\s+dup\s*\(\s*\?\s*\)|\?)',row,re.I)
        need(m is not None,'BFNT header contains a written initializer: '+row)
        fields.append((m[1],m[2].upper(),int(m[3] or 1)))
    width=sum({'DB':1,'DW':2,'DD':4}[typ]*count for _,typ,count in fields)
    need(width==SIZE and len(fields)==12 and
         len(re.findall(r'(?im)^\s*BFNT_HEADER_SIZE\s+EQU\s+32\s*$',header))==1,
         'BFNT header no longer consists of 32 uninitialized bytes')
    return [list(field) for field in fields]


def original_omf_gap(data:bytes,at:int)->dict:
    before=[];after=[]
    for rec in parse_omf(data):
        if rec.name not in ('LEDATA','LIDATA'):continue
        seg,i=_index(rec.data,0);start=int.from_bytes(rec.data[i:i+2],'little')
        if seg != 2:continue  # original _DATA, not the separate _BSS
        if rec.name!='LEDATA':
            need(not (at<=start<at+SIZE),'unexpected LIDATA in BFNT unwritten header')
            continue
        end=start+len(rec.data)-i-2
        need(end<=at or start>=at+SIZE,
             'TASM LEDATA writes inside original BFNT header reserve')
        if end==at:before.append(rec.offset)
        if start==at+SIZE:after.append(rec.offset)
    need(len(before)==len(after)==1,
         'no exact 32-byte native TASM LEDATA gap at header')
    return {'start':at,'end':at+SIZE,'prior_LED_record':before[0],
            'following_LED_record':after[0],'initialized_source_bytes':0}


def review():
    parent=json.loads(PARENT.read_text());other=json.loads(OTHER.read_text())
    author=stored_lzh(pinned(ROOT,parent['inputs']['inner_archive']))
    fields=original_layout(author)
    rows=[]
    for name,(build,stobj,at,calstart,local) in SPECS.items():
        base=ROOT/'.analysis/builds'/build/'source'
        src=(base/'libs/master.lib/super_entry_bfnt[data].asm').read_bytes()
        inc=(base/'libs/master.lib/super.inc').read_bytes()
        need(len(re.findall(rb'(?im)^\s*header\s+bfnt_header\s*<>\s*$',src))==1,
             'native TASM source did not retain the unwritten SUPERBFT template')
        need(re.search(rb'(?im)^\s*BFNT_HEADER_SIZE\s+EQU\s+32\s*$',inc),
             'native TASM SUPER.INC no longer identifies 32-byte BFNT')
        pins=parent['inputs'] if name=='main' else other['table_contexts'][name]['inputs']
        obj=pinned(ROOT,pins['calibration_object'])
        gap=original_omf_gap(obj,local)
        cal=parse_mz(pinned(ROOT,pins['calibration_exe']))
        ctx=UnitContext(ROOT,name);art,target,_=load_unit_target(ctx,ctx.config())
        need(cal.valid and target.program_image[at:at+SIZE]==b'\0'*SIZE and
             cal.program_image[calstart:calstart+SIZE]==b'\0'*SIZE,
             'original/calibration BFNT reserve is not complete zeroed storage')
        need(relative_fixups(target,at,SIZE)==relative_fixups(cal,calstart,SIZE)==[],
             'original BFNT unwritten header has unexpected loader relocation')
        rows.append({'artifact':art['id'],'start':at,'end':at+SIZE,
                     'original_artifact_sha256':art['sha256'],
                     'original_payload_sha256':sha(target.program_image),
                     'native_source_sha256':sha(src),'native_inc_sha256':sha(inc),
                     'native_omf_sha256':sha(obj),
                     'native_exe_sha256':pins['calibration_exe']['sha256'],
                     'actual_unwritten_OMF':gap,'original_MZ_fixups':[]})
    return {'version':1,'kind':'original-Master-SUPERBFT-unwritten-header',
            'classification':'reviewed-uninitialized-vendor-storage',
            'author_archive_sha256':parent['inputs']['inner_archive']['sha256'],
            'author_module_sha256':sha(author['SUPERBFT.ASM']),
            'author_layout_sha256':sha(author['SUPER.INC']),
            'fields':fields,'reserve_bytes':96,'authored_credit':0,'scopes':rows}


def validate(proof):
    parent=json.loads(PARENT.read_text());other=json.loads(OTHER.read_text())
    author=stored_lzh(pinned(ROOT,parent['inputs']['inner_archive']))
    need(proof.get('version')==1 and
         proof.get('kind')=='original-Master-SUPERBFT-unwritten-header' and
         proof.get('classification')=='reviewed-uninitialized-vendor-storage' and
         proof.get('author_archive_sha256')==parent['inputs']['inner_archive']['sha256'] and
         proof.get('author_module_sha256')==sha(author['SUPERBFT.ASM']) and
         proof.get('author_layout_sha256')==sha(author['SUPER.INC']) and
         proof.get('fields')==original_layout(author) and
         proof.get('reserve_bytes')==96 and proof.get('authored_credit')==0 and
         len(proof.get('scopes',[]))==3,'stale/incomplete Master BFNT header proof')
    for row,(name,(build,objname,at,calstart,local)) in zip(proof['scopes'],SPECS.items()):
        pins=parent['inputs'] if name=='main' else other['table_contexts'][name]['inputs']
        info=other['table_contexts'][name] if name!='main' else None
        artsha=parent['inputs']['target']['sha256'] if name=='main' else info['target_sha256']
        payloadsha=parent['target_payload_sha256'] if name=='main' else info['target_payload_sha256']
        base=ROOT/'.analysis/builds'/build/'source/libs/master.lib'
        obj=pinned(ROOT,pins['calibration_object'])
        need(row.get('artifact')=='th05-'+name and row.get('start')==at and
             row.get('end')==at+SIZE and
             row.get('original_artifact_sha256')==artsha and
             row.get('original_payload_sha256')==payloadsha and
             row.get('native_source_sha256')==sha((base/'super_entry_bfnt[data].asm').read_bytes()) and
             row.get('native_inc_sha256')==sha((base/'super.inc').read_bytes()) and
             row.get('native_omf_sha256')==pins['calibration_object']['sha256'] and
             row.get('native_exe_sha256')==pins['calibration_exe']['sha256'] and
             row.get('actual_unwritten_OMF')==original_omf_gap(obj,local) and
             row.get('original_MZ_fixups')==[],
             'Master BFNT source, original target or 32-byte OMF gap changed')


def reviewed_claims(root,views,*,verify_targets=False):
    if not PROOF.exists():return {},None
    raw=PROOF.read_bytes();proof=json.loads(raw);validate(proof)
    if verify_targets:need(review()==proof,'native Master BFNT source proof changed')
    claims={}
    for row in proof['scopes']:
        n=row['artifact'].removeprefix('th05-')
        need(views[n]['sha256']==row['original_payload_sha256'],
             'BFNT reserve belongs to a different original target')
        claims[n]=[{'start':row['start'],'end':row['end'],
                    'kind':'reviewed-uninitialized-vendor-storage',
                    'content_kind':'source-question-mark-struct',
                    'library':'Master 0.23','member':'BFNT_HEADER',
                    'source':'SUPERBFT.ASM/SUPER.INC',
                    'authored_credit':0,'instruction_bytes':0}]
    return claims,sha(raw)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    g=p.add_mutually_exclusive_group(required=True)
    for a in ('write','check','structural-check'):g.add_argument('--'+a,action='store_true')
    args=p.parse_args()
    if args.write:
        proof=review();PROOF.write_text(json.dumps(proof,indent=2)+'\n')
    else:proof=json.loads(PROOF.read_text())
    validate(proof)
    if args.check:need(proof==review(),'original BFNT source/OMF verification differs')
    print('PASS: three original 32-byte Master BFNT header reserves, no initialized DATA credit')

if __name__=='__main__':main()
