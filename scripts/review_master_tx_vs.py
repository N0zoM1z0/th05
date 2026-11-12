#!/usr/bin/env python3
"""Verify Master TX/VS explicitly initialized words, excluding adjacent unknown byte."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

from lib.unit_context import UnitContext, load_unit_target
from lib.unit_oracle import relative_fixups
from lib.pc98 import parse_mz
from review_master import pinned, stored_lzh, sha, need
from review_master_bgm_literal_data import actual_data

ROOT=Path(__file__).resolve().parents[1]
EVIDENCE=ROOT/'config/reviewed_master_tx_vs.json'
PARENT=ROOT/'config/master_vendor_ownership.json'
OTHER=ROOT/'config/master_vendor_additions.json'
SPECS={
 'main':('main-calibration-b','main',0x2106c,0x2108e,0x61e,'209E:06AE'),
 'op':('op-calibration-a','op',0xf7f0,0xf7f0,0x33e,'0EFE:0810'),
 'maine':('maine-calibration-a','mainem',0x1060a,0x105fa,0x43e,'1010:04FA'),
}


def extract(tx:bytes,vs:bytes,encoding:str):
    a=tx.decode(encoding);b=vs.decode(encoding)
    checks=(
        (a,r'TextVramAdr label dword\s+_TextVramAdr label dword\s+dw 0'),
        (a,r'_TextVramSeg\s+dw\s+0a000h'),
        (a,r'_TextVramWidth\s+dw\s+80'),
        (a,r'_TextShown\s+dw\s+1'),
        (b,r'_vsync_Proc\s+dd\s+0'),
        (b,r'_vsync_Delay\s+dw\s+0'),
        (b,r'vsync_OldMask\s+db\s+0\s+EVEN'),
    )
    for raw,pattern in checks:
        need(re.search(pattern,raw,re.I) is not None,'archived Master TX/VS initializer changed')
    text=(0).to_bytes(2,'little')+(0xa000).to_bytes(2,'little')+ (80).to_bytes(2,'little')+(1).to_bytes(2,'little')
    versus=b'\0'*7
    return text,versus


def review():
    parent=json.loads(PARENT.read_text());other=json.loads(OTHER.read_text())
    archive=stored_lzh(pinned(ROOT,parent['inputs']['inner_archive']))
    tx,vs=extract(archive['TX.ASM'],archive['VS.ASM'],'cp932')
    rows=[]
    for name,(build,objname,original_at,cal_at,local,public) in SPECS.items():
        base=ROOT/'.analysis/builds'/build/'source'
        src_tx=(base/'libs/master.lib/tx[data].asm').read_bytes()
        src_vs=(base/'libs/master.lib/vs[data].asm').read_bytes()
        need(extract(src_tx,src_vs,'utf8')==(tx,vs),'retained TX/VS TASM source changed')
        pins=parent['inputs'] if name=='main' else other['table_contexts'][name]['inputs']
        obj=pinned(ROOT,pins['calibration_object'])
        cal_exe=pinned(ROOT,pins['calibration_exe'])
        mp=pinned(ROOT,pins['calibration_map'])
        need(len(re.findall(r'(?im)^\s*'+public+r'\s+(?:idle\s+)?_?TextVramAdr\s*$',mp.decode('cp437')))==4,
             'TEXT public does not match actual calibration MAP')
        frame,ds=public.split(':')
        vs_public=f'{frame}:{int(ds,16)+8:04X}'
        need(len(re.findall(r'(?im)^\s*'+vs_public+r'\s+(?:idle\s+)?_?vsync_Proc\s*$',mp.decode('cp437')))==4,
             'VSYNC source public does not follow TEXT in actual MAP')
        cal=parse_mz(cal_exe)
        ctx=UnitContext(ROOT,name);artifact,original,_=load_unit_target(ctx,ctx.config())
        need(cal.valid,'invalid calibration MZ')
        for member,start,source in (('TextVram',0,tx),('vsync',8,vs)):
            at=original_at+start;cat=cal_at+start
            need(original.program_image[at:at+len(source)]==source and
                 cal.program_image[cat:cat+len(source)]==source,
                 'original or calibration SOURCE words differ')
            need(relative_fixups(original,at,len(source))==relative_fixups(cal,cat,len(source))==[],
                 'original segment relocations inside TX/VS initialized words')
            pieces=actual_data(obj,local+start,len(source))
            need(len(pieces)==1 and pieces[0]['scope_offset']==0 and
                 pieces[0]['scope_size']==len(source) and
                 pieces[0]['scope_content_sha256']==sha(source),
                 'unreviewed DATA LEDATA or incomplete TX/VS source bytes')
            rows.append(dict(artifact=artifact['id'],name=member,start=at,end=at+len(source),
                             source_sha256=sha(source),original_target_sha256=artifact['sha256'],
                             original_payload_sha256=sha(original.program_image),
                             calibration_exe_sha256=sha(cal_exe),
                             calibration_map_sha256=sha(mp),
                             actual_omf_sha256=sha(obj),
                             actual_ledatas=pieces,ordered_fixups=[]))
        # One source-side data-alignment byte disagrees with original. Keep unknown.
        need(original.program_image[original_at+15]==0x90 and
             cal.program_image[cal_at+15]==0,
             'the explicitly excluded original TX/VS alignment byte changed')
    return dict(schema_version=1,kind='original-Master-TX-VS-initialized-source',
                authored_credit=0,total_bytes=45,
                original_archive_sha256=parent['inputs']['inner_archive']['sha256'],
                author_text_sha256=sha(archive['TX.ASM']),
                author_vsync_sha256=sha(archive['VS.ASM']),
                scopes=rows)


def validate(proof):
    parent=json.loads(PARENT.read_text());other=json.loads(OTHER.read_text())
    archive=stored_lzh(pinned(ROOT,parent['inputs']['inner_archive']))
    tx,vs=extract(archive['TX.ASM'],archive['VS.ASM'],'cp932')
    need(proof.get('schema_version')==1 and proof.get('kind')=='original-Master-TX-VS-initialized-source' and
         proof.get('authored_credit')==0 and proof.get('total_bytes')==45 and
         proof.get('original_archive_sha256')==parent['inputs']['inner_archive']['sha256'] and
         proof.get('author_text_sha256')==sha(archive['TX.ASM']) and
         proof.get('author_vsync_sha256')==sha(archive['VS.ASM']),
         'stale Master TX/VS proof')
    rows=proof.get('scopes',[])
    need(len(rows)==6,'partial Master TX/VS source inventory')
    for ix,(name,(build,objname,at,cal_at,local,public)) in enumerate(SPECS.items()):
        pins=parent['inputs'] if name=='main' else other['table_contexts'][name]['inputs']
        expected_target=parent['inputs']['target']['sha256'] if name=='main' else other['table_contexts'][name]['target_sha256']
        expected_payload=parent['target_payload_sha256'] if name=='main' else other['table_contexts'][name]['target_payload_sha256']
        for offset,member,value in ((0,'TextVram',tx),(8,'vsync',vs)):
            r=rows[2*ix+int(offset!=0)];led=r.get('actual_ledatas',[])
            need(r.get('artifact')=='th05-'+name and r.get('name')==member and
                 r.get('start')==at+offset and r.get('end')==at+offset+len(value) and
                 r.get('source_sha256')==sha(value) and
                 r.get('original_target_sha256')==expected_target and
                 r.get('original_payload_sha256')==expected_payload and
                 r.get('calibration_exe_sha256')==pins['calibration_exe']['sha256'] and
                 r.get('calibration_map_sha256')==pins['calibration_map']['sha256'] and
                 r.get('actual_omf_sha256')==pins['calibration_object']['sha256'] and
                 r.get('ordered_fixups')==[] and len(led)==1 and
                 led[0]['scope_size']==len(value) and
                 led[0]['scope_content_sha256']==sha(value),
                 'Master TX/VS source/target or extent identity changed')


def reviewed_claims(root,views,*,verify_targets=False):
    if not EVIDENCE.exists():return {},None
    raw=EVIDENCE.read_bytes();j=json.loads(raw);validate(j)
    if verify_targets:need(review()==j,'actual source-linked Master TX/VS proof changed')
    result={}
    for r in j['scopes']:
        name=r['artifact'].removeprefix('th05-')
        need(views[name]['sha256']==r['original_payload_sha256'],
             'Master TX/VS DATA belongs to another target')
        result.setdefault(name,[]).append(dict(start=r['start'],end=r['end'],kind='verified-vendor-initialized-data',
                                                content_kind='library-initialized-data',instruction_bytes=0,
                                                library='Master 0.23',member=r['name']))
    return result,sha(raw)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    g=p.add_mutually_exclusive_group(required=True)
    for mode in ('write','check','structural-check'):g.add_argument('--'+mode,action='store_true')
    a=p.parse_args()
    if a.write:
        result=review();EVIDENCE.write_text(json.dumps(result,indent=2)+'\n')
    else:result=json.loads(EVIDENCE.read_text())
    validate(result)
    if a.check:need(review()==result,'source-linked TX/VS native comparison changed')
    print('PASS: Master text 8 + VSYNC 7 bytes in each MAIN/OP/MAINE (45 total)')

if __name__=='__main__':main()
