#!/usr/bin/env python3
"""Independent source/OMF proof for MAINE's original 256-byte ATAN8 table.

The following 8 zeros, preceding 1 byte and next BFNT resource are excluded.
MAIN already owns its independent copy. OP does not contain this table.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

from lib.omf import parse_omf
from lib.pc98 import parse_mz
from lib.unit_context import UnitContext,load_unit_target
from lib.unit_extents import _index
from lib.unit_oracle import relative_fixups
from review_main_atan8_data import table
from review_master import pinned,stored_lzh,need,sha

ROOT=Path(__file__).resolve().parents[1]
PROOF=ROOT/'config/reviewed_maine_atan8_initial.json'
PARENT=ROOT/'config/master_vendor_ownership.json'
OTHER=ROOT/'config/master_vendor_additions.json'
SOURCE='libs/master.lib/atan8[data].asm'
START,CAL_START,SIZE=0x101CC,0x101BC,256
MAP_PUBLIC='1010:00BC'


def review():
    parent=json.loads(PARENT.read_text());other=json.loads(OTHER.read_text())
    author=stored_lzh(pinned(ROOT,parent['inputs']['inner_archive']))['ATAN8.ASM']
    authored,rows=table(author,encoding='cp932')
    native_root=ROOT/'.analysis/builds/maine-calibration-a/source'
    native_source=(native_root/SOURCE).read_bytes()
    retained,nativerows=table(native_source,encoding='utf8')
    need(authored==retained and rows==nativerows==16,
         'MAINE retained ATAN8 source differs from archived original Master')
    pins=other['table_contexts']['maine']['inputs']
    obj=pinned(ROOT,pins['calibration_object'])
    mp=pinned(ROOT,pins['calibration_map'])
    exe=pinned(ROOT,pins['calibration_exe'])
    actual=[]
    source_records=parse_omf(obj)
    for r in source_records:
        if r.name not in ('LEDATA','LIDATA'):continue
        si,i=_index(r.data,0)
        off=int.from_bytes(r.data[i:i+2],'little')
        if si==2 and off==0 and r.name=='LEDATA':
            actual.append(r)
    need(len(actual)==1,'original MAINE atan lookup requires one real _DATA LEDATA at local zero')
    rec=actual[0]
    si,i=_index(rec.data,0)
    initializer=rec.data[i+2:]
    need(len(initializer)==258 and initializer[:SIZE]==authored and
         initializer[SIZE:]==b'\0\0',
         'native MAINE atan source includes nonoriginal bytes or lost 2 trailing zeros')
    # The retained TASM emitted two extra zero-filled source contributions
    # before BFNT, but none are attributable to the ATAN 256 literal bytes.
    remaining=[]
    for r in source_records:
        if r.name in ('LEDATA','LIDATA'):
            seg,i=_index(r.data,0)
            off=int.from_bytes(r.data[i:i+2],'little')
            if seg==2 and r.offset!=rec.offset and off<0x108:
                remaining.append((r.name,off,len(r.data)-i-2))
    need(sorted(remaining)==sorted([('LIDATA',0x102,11),('LEDATA',0x106,856)]),
         'original TASM ATAN trailing alignment/BFNT context changed')
    mptext=mp.decode('cp437')
    for name in ('AtanTable8','_AtanTable8'):
        need(len(re.findall(r'(?im)^\s*'+MAP_PUBLIC+r'\s+(?:idle\s+)?'+name+r'\s*$',mptext))==2,
             'original MAINE ATAN8 MAP public relocated')
    cal=parse_mz(exe)
    ctx=UnitContext(ROOT,'maine');art,target,_=load_unit_target(ctx,ctx.config())
    need(cal.valid and target.program_image[START:START+SIZE]==authored and
         cal.program_image[CAL_START:CAL_START+SIZE]==authored,
         'original MAINE/retained calibration ATAN8 differs from original archived source')
    need(target.program_image.find(authored)==START and
         target.program_image.find(authored,START+1)<0,
         'original MAINE ATAN8 source is not unique in decoded payload')
    need(relative_fixups(target,START,SIZE)==relative_fixups(cal,CAL_START,SIZE)==[],
         'MAINE ATAN8 has an unexpected loader segment relocation')
    need(target.program_image[START-1:START]==b'\0' and
         target.program_image[START+SIZE:START+SIZE+8]==b'\0'*8 and
         cal.program_image[CAL_START+SIZE:CAL_START+SIZE+8]==b'\0'*8,
         'excluded original ATAN8 pre/post alignment differs')
    return dict(version=1,kind='source-linked-MAINE-original-Master-ATAN8',
                classification='third-party-library-initialized-data',
                artifact=art['id'],start=START,end=START+SIZE,
                calibration_start=CAL_START,total_bytes=SIZE,authored_credit=0,
                author_sha256=sha(author),native_source_sha256=sha(native_source),
                author_archive_sha256=parent['inputs']['inner_archive']['sha256'],
                native_object_sha256=sha(obj),native_MAP_sha256=sha(mp),
                native_EXE_sha256=sha(exe),target_sha256=art['sha256'],
                target_payload_sha256=sha(target.program_image),
                data_sha256=sha(authored),
                actual_LEDATA_record_offset=rec.offset,
                actual_LEDATA_written_size=len(initializer),
                actual_source_local_offset=0,
                unclaimed_leading_bytes=1,unclaimed_trailing_bytes=8,
                ordered_original_MZ_fixups=[])


def validate(proof):
    parent=json.loads(PARENT.read_text());other=json.loads(OTHER.read_text())
    author=stored_lzh(pinned(ROOT,parent['inputs']['inner_archive']))['ATAN8.ASM']
    value,_=table(author,encoding='cp932')
    ctx=other['table_contexts']['maine'];pins=ctx['inputs']
    src=ROOT/'.analysis/builds/maine-calibration-a/source'/SOURCE
    need(proof.get('version')==1 and proof.get('kind')=='source-linked-MAINE-original-Master-ATAN8' and
         proof.get('classification')=='third-party-library-initialized-data' and
         proof.get('artifact')=='th05-maine' and proof.get('start')==START and proof.get('end')==START+SIZE and
         proof.get('calibration_start')==CAL_START and proof.get('total_bytes')==SIZE and
         proof.get('authored_credit')==0 and proof.get('author_sha256')==sha(author) and
         proof.get('native_source_sha256')==sha(src.read_bytes()) and
         proof.get('author_archive_sha256')==parent['inputs']['inner_archive']['sha256'] and
         proof.get('native_object_sha256')==pins['calibration_object']['sha256'] and
         proof.get('native_MAP_sha256')==pins['calibration_map']['sha256'] and
         proof.get('native_EXE_sha256')==pins['calibration_exe']['sha256'] and
         proof.get('target_sha256')==ctx['target_sha256'] and
         proof.get('target_payload_sha256')==ctx['target_payload_sha256'] and
         proof.get('data_sha256')==sha(value) and
         proof.get('actual_source_local_offset')==0 and
         proof.get('actual_LEDATA_written_size')==258 and
         type(proof.get('actual_LEDATA_record_offset')) is int and
         proof.get('unclaimed_leading_bytes')==1 and proof.get('unclaimed_trailing_bytes')==8 and
         proof.get('ordered_original_MZ_fixups')==[],
         'MAINE ATAN source/native evidence or exact physical boundary changed')


def reviewed_claims(root,views,*,verify_targets=False):
    if not PROOF.exists():return {},None
    raw=PROOF.read_bytes();proof=json.loads(raw);validate(proof)
    need(views['maine']['sha256']==proof['target_payload_sha256'],
         'MAINE original Master ATAN scope applied to another target')
    if verify_targets:need(proof==review(),'original MAINE Master ATAN table verification differs')
    return {'maine':[dict(start=START,end=START+SIZE,
                          kind='verified-vendor-initialized-data',
                          content_kind='library-initialized-data',instruction_bytes=0,
                          library='Master 0.23',member='ATAN8')]},sha(raw)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    g=p.add_mutually_exclusive_group(required=True)
    for m in ('write','check','structural-check'):g.add_argument('--'+m,action='store_true')
    a=p.parse_args()
    if a.write:
        j=review();PROOF.write_text(json.dumps(j,indent=2)+'\n')
    else:j=json.loads(PROOF.read_text())
    validate(j)
    if a.check:need(j==review(),'MAINE ATAN8 original exact source proof changed')
    print('PASS: MAINE original 256-byte Master ATAN8 DATA, 9 neighboring unknown bytes excluded')

if __name__=='__main__':main()
