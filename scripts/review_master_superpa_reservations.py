#!/usr/bin/env python3
"""Recover exact original SUPERPA twin 512-word _BSS reservations in three MZs.

This is ONLY source-backed unwritten vendor storage. It is not source-written
initialized DATA, never game C/C++ authored credit, and not arbitrary zero fill.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

from lib.omf import parse_omf
from lib.unit_extents import _index
from lib.unit_context import UnitContext,load_unit_target
from lib.unit_oracle import relative_fixups
from lib.pc98 import parse_mz
from review_master import need,pinned,sha,stored_lzh

ROOT=Path(__file__).resolve().parents[1]
PROOF=ROOT/'config/reviewed_master_superpa_reservations.json'
PARENT=ROOT/'config/master_vendor_ownership.json'
OTHER=ROOT/'config/master_vendor_additions.json'
# True original decoded MZ offsets, calibration MAP locations and _BSS segment
# local offsets of the two 1024-byte arrays, all directly from native MAP/OMF.
SPECS={
 'main':('main-calibration-b','main',0x2305C,'209E:269E',0x72,0xA080,'th05_main.asm'),
 'op':('op-calibration-a','op',0x11E40,'0EFE:2E60',0x6A,0x1128,'th05_op.asm'),
 'maine':('maine-calibration-a','mainem',0x11EEC,'1010:1DDC',0x6A,0x1114,'th05_maine_master.asm'),
}
NAMES=('super_patdata','super_patsize')
WORD_COUNT=512
BYTES_PER_ARRAY=WORD_COUNT*2


def source_shape(body:bytes,header:bytes,encoding:str)->None:
    text=body.decode(encoding)
    include=header.decode(encoding)
    need(len(re.findall(r'(?im)^\s*MAXPAT\s+EQU\s+512\s*(?:;.*)?$',include))==1,
         'the original SUPERPA pattern capacity is not 512')
    need(re.search(r'(?im)^\s*\.DATA\?\s*$',text) is not None,
         'SUPERPA source no longer declares uninitialized DATA')
    for name in NAMES:
        need(len(re.findall(r'(?im)^\s*'+name+r'\s+DW\s+MAXPAT\s+dup\s*\(\s*\?\s*\)\s*(?:;.*)?$',text))==1,
             'SUPERPA source no longer has one complete ? array: '+name)
        need(len(re.findall(r'(?im)^\s*_?'+name+r'\s+label\s+word\s*$',text))==1,
             'SUPERPA source no longer exports a word-aligned array: '+name)


def parse_true_bss(obj:bytes,local:int,extent:int)->dict:
    records=parse_omf(obj)
    names=[''];segments=[None];pointers={};bytes_written=[]
    for rec in records:
        raw=rec.data
        if rec.name=='LNAMES':
            i=0
            while i<len(raw):
                count=raw[i];i+=1
                need(i+count<=len(raw),'truncated TASM LNAMES')
                names.append(raw[i:i+count].decode('cp437'));i+=count
        elif rec.name=='SEGDEF':
            ni,i=_index(raw,3);ci,i=_index(raw,i);oi,i=_index(raw,i)
            need(ni<len(names) and ci<len(names),'invalid TASM BSS SEGDEF names')
            segments.append((names[ni],names[ci],int.from_bytes(raw[1:3],'little')))
        elif rec.name=='PUBDEF':
            if not 2<=len(raw):continue
            group,si=raw[0],raw[1]
            pos=2
            if si==0:
                pos+=2
            if pos>=len(raw):continue
            length=raw[pos];pos+=1
            if pos+length+2>len(raw):continue
            name=raw[pos:pos+length].decode('cp437');pos+=length
            if name in {k for root in NAMES for k in (root,'_'+root)}:
                pointers[name]=(group,si,int.from_bytes(raw[pos:pos+2],'little'))
        elif rec.name in ('LEDATA','LIDATA'):
            si,pos=_index(raw,0)
            offset=int.from_bytes(raw[pos:pos+2],'little')
            bytes_written.append((rec.name,si,offset,len(raw)-pos-2))
    bss=[(i,x) for i,x in enumerate(segments) if x is not None and x[:2]==('_BSS','BSS')]
    need(len(bss)==1,'expected one original TASM _BSS source segment')
    bss_index,(seg_name,seg_class,bss_size)=bss[0]
    need(local+extent <= bss_size,'SUPERPA twin arrays do not fit real _BSS SEGDEF')
    for name,diff in (('super_patdata',0),('super_patsize',BYTES_PER_ARRAY)):
        for alias in (name,'_'+name):
            need(pointers.get(alias)==(1,bss_index,local+diff),
                 'actual BSS PUBDEF offset differs from canonical source '+alias)
    bss_writes=[row for row in bytes_written if row[1]==bss_index]
    need(not bss_writes,'original TASM object writes initialized bytes to _BSS')
    return dict(bss_segment_index=bss_index,bss_segment_bytes=bss_size,
                first_array_local=local,second_array_local=local+BYTES_PER_ARRAY,
                original_pubdef_offsets={name:pointers[name][2] for name in pointers},
                actual_initialized_bss_records=0)


def review():
    parent=json.loads(PARENT.read_text());other=json.loads(OTHER.read_text())
    author=stored_lzh(pinned(ROOT,parent['inputs']['inner_archive']))
    source_shape(author['SUPERPA.ASM'],author['SUPER.INC'],'cp932')
    scopes=[]
    for name,(build,objname,original_at,public,local,expected_bss_size,module) in SPECS.items():
        base=ROOT/'.analysis/builds'/build/'source'
        retained=(base/'libs/master.lib/superpa[bss].asm').read_bytes()
        include=(base/'libs/master.lib/super.inc').read_bytes()
        # The retained [bss] fragment deliberately only contains the two
        # source reserves, unlike the archived complete module's .DATA block.
        source_shape(b'.DATA?\n'+retained,include,'utf8')
        pins=parent['inputs'] if name=='main' else other['table_contexts'][name]['inputs']
        obj=pinned(ROOT,pins['calibration_object'])
        mp=pinned(ROOT,pins['calibration_map'])
        exe=pinned(ROOT,pins['calibration_exe'])
        actual_bss=parse_true_bss(obj,local,BYTES_PER_ARRAY*2)
        need(actual_bss['bss_segment_bytes']==expected_bss_size,
             'native TASM source _BSS SEGDEF changed')
        maptext=mp.decode('cp437')
        mapframe,first=public.split(':')
        for field,diff in (('super_patdata',0),('super_patsize',BYTES_PER_ARRAY)):
            address=f'{mapframe}:{int(first,16)+diff:04X}'
            for alias in (field,'_'+field):
                need(len(re.findall(r'(?im)^\s*'+address+r'\s+(?:idle\s+)?'+alias+r'\s*$',maptext))==2,
                     'original-compiler MAP does not anchor '+alias+' at '+address)
        # The assembler's one complete _BSS contribution must cover both
        # arrays, and the original segment must be a BSS class, not _DATA.
        bss_lines=[l for l in maptext.splitlines()
                   if re.search(r'(?i)C=BSS\s+S=_BSS\s+G=DGROUP\s+M='+re.escape(module),l)]
        need(len(bss_lines)==1 and
             re.search(r'(?i)\b'+f'{expected_bss_size:04X}'+r'\s+C=BSS',bss_lines[0]),
             'native MAP BSS module extent does not contain complete SUPERPA')
        ctx=UnitContext(ROOT,name);art,target,_=load_unit_target(ctx,ctx.config())
        calibration=parse_mz(exe)
        need(calibration.valid,'retained native calibration MZ invalid')
        # BSS has no source-backed initialized file bytes in the calibration
        # EXE. The original target view does show the zeros loaded at runtime.
        calstart=(int(mapframe,16)<<4)+int(first,16)
        need(len(calibration.program_image)<=calstart,
             'a reconstructed source EXE unexpectedly writes SUPERPA BSS')
        need(len(target.program_image)>=original_at+BYTES_PER_ARRAY*2 and
             target.program_image[original_at:original_at+BYTES_PER_ARRAY*2]==b'\0'*(BYTES_PER_ARRAY*2),
             'original MZ does not materialize complete 2048-byte SUPERPA reserve')
        for diff in (0,BYTES_PER_ARRAY):
            need(relative_fixups(target,original_at+diff,BYTES_PER_ARRAY)==[],
                 'runtime-writable SUPERPA reserve has original MZ relocation')
        scopes.append(dict(artifact=art['id'],first_original_start=original_at,
             second_original_start=original_at+BYTES_PER_ARRAY,
             native_bss_public=public,
             author_header_sha256=sha(author['SUPER.INC']),
             author_source_sha256=sha(author['SUPERPA.ASM']),
             retained_header_sha256=sha(include),retained_bss_source_sha256=sha(retained),
             target_sha256=art['sha256'],target_payload_sha256=sha(target.program_image),
             native_object_sha256=sha(obj),native_map_sha256=sha(mp),
             native_exe_sha256=sha(exe),full_source_omf_bss=actual_bss,
             original_ordered_fixups=[],initialized_source_bytes=0))
    return dict(version=1,kind='original-Master-SUPERPA-unwritten-array-source',
          classification='reviewed-uninitialized-vendor-storage',
          archived_source_sha256=sha(author['SUPERPA.ASM']),
          archived_inc_sha256=sha(author['SUPER.INC']),
          archived_library_sha256=parent['inputs']['inner_archive']['sha256'],
          original_pattern_count=WORD_COUNT,bytes_per_array=BYTES_PER_ARRAY,
          array_count=2,total_reserve_bytes=6144,authored_credit=0,scopes=scopes)


def validate(proof):
    parent=json.loads(PARENT.read_text());other=json.loads(OTHER.read_text())
    author=stored_lzh(pinned(ROOT,parent['inputs']['inner_archive']))
    source_shape(author['SUPERPA.ASM'],author['SUPER.INC'],'cp932')
    need(proof.get('version')==1 and
         proof.get('kind')=='original-Master-SUPERPA-unwritten-array-source' and
         proof.get('classification')=='reviewed-uninitialized-vendor-storage' and
         proof.get('archived_source_sha256')==sha(author['SUPERPA.ASM']) and
         proof.get('archived_inc_sha256')==sha(author['SUPER.INC']) and
         proof.get('archived_library_sha256')==parent['inputs']['inner_archive']['sha256'] and
         proof.get('original_pattern_count')==512 and proof.get('bytes_per_array')==1024 and
         proof.get('array_count')==2 and proof.get('total_reserve_bytes')==6144 and
         proof.get('authored_credit')==0 and len(proof.get('scopes',[]))==3,
         'stale/incomplete Master SUPERPA unwritten array source proof')
    for row,(name,(build,objname,st,pub,local,size,module)) in zip(proof['scopes'],SPECS.items()):
        pins=parent['inputs'] if name=='main' else other['table_contexts'][name]['inputs']
        info=other['table_contexts'][name] if name!='main' else None
        artsha=parent['inputs']['target']['sha256'] if name=='main' else info['target_sha256']
        payloadsha=parent['target_payload_sha256'] if name=='main' else info['target_payload_sha256']
        base=ROOT/'.analysis/builds'/build/'source/libs/master.lib'
        obj=pinned(ROOT,pins['calibration_object'])
        need(row.get('artifact')=='th05-'+name and
             row.get('first_original_start')==st and
             row.get('second_original_start')==st+1024 and
             row.get('native_bss_public')==pub and
             row.get('author_source_sha256')==sha(author['SUPERPA.ASM']) and
             row.get('author_header_sha256')==sha(author['SUPER.INC']) and
             row.get('retained_bss_source_sha256')==sha((base/'superpa[bss].asm').read_bytes()) and
             row.get('retained_header_sha256')==sha((base/'super.inc').read_bytes()) and
             row.get('target_sha256')==artsha and row.get('target_payload_sha256')==payloadsha and
             row.get('native_object_sha256')==pins['calibration_object']['sha256'] and
             row.get('native_map_sha256')==pins['calibration_map']['sha256'] and
             row.get('native_exe_sha256')==pins['calibration_exe']['sha256'] and
             row.get('full_source_omf_bss')==parse_true_bss(obj,local,2048) and
             row.get('original_ordered_fixups')==[] and row.get('initialized_source_bytes')==0,
             'SUPERPA author/source/BSS OMF/native target verification changed')


def reviewed_claims(root,views,*,verify_targets=False):
    if not PROOF.exists():return {},None
    raw=PROOF.read_bytes();proof=json.loads(raw);validate(proof)
    if verify_targets:need(review()==proof,'original source-backed SUPERPA BSS review changed')
    claims={}
    for row in proof['scopes']:
        name=row['artifact'].removeprefix('th05-')
        need(views[name]['sha256']==row['target_payload_sha256'],
             'uninitialized SUPERPA source belongs to another MZ target')
        claims[name]=[dict(start=st,end=st+BYTES_PER_ARRAY,
                           kind='reviewed-uninitialized-vendor-storage',
                           content_kind='source-question-mark-struct',
                           library='Master 0.23',member=member,source='SUPERPA.ASM/MAXPAT',
                           authored_credit=0,instruction_bytes=0)
                      for st,member in ((row['first_original_start'],'SUPER_PATDATA'),
                                        (row['second_original_start'],'SUPER_PATSIZE'))]
    return claims,sha(raw)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    g=p.add_mutually_exclusive_group(required=True)
    for mode in ('write','check','structural-check'):g.add_argument('--'+mode,action='store_true')
    a=p.parse_args()
    if a.write:
        proof=review();PROOF.write_text(json.dumps(proof,indent=2)+'\n')
    else:proof=json.loads(PROOF.read_text())
    validate(proof)
    if a.check:need(proof==review(),'original SUPERPA arrays review changed')
    print('PASS: 6 exact original source SUPERPA 1024-byte BSS reservations, zero authored credit')

if __name__=='__main__':main()
