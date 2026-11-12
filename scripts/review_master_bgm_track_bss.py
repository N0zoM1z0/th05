#!/usr/bin/env python3
"""Review three complete 198-byte Master BGM track/effect _BSS reserves.

Original author SPART and SESOUND structs are entirely question-mark fields;
this review deliberately assigns no initialized or C/C++ authored credit.
"""
from __future__ import annotations
import argparse,json,re
from pathlib import Path
from review_master import need,pinned,sha,stored_lzh
from review_master_compact_bss import bss_publics
from lib.unit_context import UnitContext,load_unit_target
from lib.unit_oracle import relative_fixups

ROOT=Path(__file__).resolve().parents[1]
PROOF=ROOT/'config/reviewed_master_bgm_track_bss.json'
PARENT=ROOT/'config/master_vendor_ownership.json'
OTHER=ROOT/'config/master_vendor_additions.json'
SPECS={
 'main':('main-calibration-b','main',0x23960,0x976,0xA080,'209E:2FA2'),
 'op':('op-calibration-a','op',0x12744,0x96E,0x1128,'0EFE:3764'),
 'maine':('maine-calibration-a','mainem',0x127F0,0x96E,0x1114,'1010:26E0'),
}
SIZE=198


def authored_structure(body:bytes,header:bytes,encoding='cp932',original=True):
    src=body.decode(encoding);types=header.decode(encoding)
    if original:
        need(re.search(r'(?im)^\s*\.DATA\?\s*$',src),
             'Master BGM sound state no longer appears in author uninitialized DATA')
    for expr in (r'timerorg\s+dd\s+\?',
                 r'part\s+SPART\s+PMAX\s+dup\s*\(<>\)',
                 r'esound\s+SESOUND\s+SMAX\s+dup\s*\(< >\)'.replace(' ','')):
        need(re.search(r'(?im)^\s*'+expr+r'\s*(?:;.*)?$',src),
             'Master track/effect BSS author declaration changed: '+expr)
    def fields(which):
        match=re.search(r'(?ims)^\s*'+which+r'\s+struc\s*(.*?)^\s*'+which+r'\s+ends\s*$',types)
        need(match is not None,'Master sound structure missing: '+which)
        out=[]
        for line in match[1].splitlines():
            row=line.split(';',1)[0].strip()
            if not row:continue
            found=re.fullmatch(r'\w+\s+(dd|dw)\s+\?',row,re.I)
            need(found is not None,'BGM sound member is not a question-mark field')
            out.append(4 if found[1].lower()=='dd' else 2)
        return out
    p=fields('SPART');s=fields('SESOUND')
    need(len(p)==9 and sum(p)==22 and len(s)==2 and sum(s)==8 and
         re.search(r'(?im)^\s*PMAX\s+equ\s+3\s*',types) and
         re.search(r'(?im)^\s*SMAX\s+equ\s+16\s*',types),
         'original sound state is not 4 + 3*22 + 16*8 = 198 bytes')


def review():
    p=json.loads(PARENT.read_text());other=json.loads(OTHER.read_text())
    archive=stored_lzh(pinned(ROOT,p['inputs']['inner_archive']))
    authored_structure(archive['B_DATA.ASM'],archive['BGM.INC'])
    rows=[]
    for name,(build,objname,at,local,bss_size,public) in SPECS.items():
        base=ROOT/'.analysis/builds'/build/'source'
        source=(base/'libs/master.lib/bgm[bss].asm').read_bytes()
        header=(base/'libs/master.lib/bgm.inc').read_bytes()
        authored_structure(source,header,'utf8',False)
        pins=p['inputs'] if name=='main' else other['table_contexts'][name]['inputs']
        obj=pinned(ROOT,pins['calibration_object'])
        mapraw=pinned(ROOT,pins['calibration_map'])
        bss=bss_publics(obj,[('timerorg',local),('part',local+4),('_bgm_part',local+4),
                                ('esound',local+70),('_bgm_esound',local+70)],bss_size)
        frame,start=public.split(':')
        for symbol,offset in [('timerorg',0),('part',4),('_bgm_part',4),('esound',70),('_bgm_esound',70)]:
            addr=f'{frame}:{int(start,16)+offset:04X}'
            need(len(re.findall(r'(?im)^\s*'+addr+r'\s+(?:idle\s+)?'+symbol+r'\s*$',mapraw.decode('cp437')))==2,
                 'original Master BGM MAP public at wrong address: '+symbol)
        ctx=UnitContext(ROOT,name);art,target,_=load_unit_target(ctx,ctx.config())
        need(target.program_image[at:at+SIZE]==b'\0'*SIZE and
             relative_fixups(target,at,SIZE)==[],
             'original BGM track/effect reserve differs from 198 zero materialized bytes')
        rows.append(dict(artifact=art['id'],start=at,end=at+SIZE,
                         target_sha256=art['sha256'],payload_sha256=sha(target.program_image),
                         native_source_sha256=sha(source),native_header_sha256=sha(header),
                         object_sha256=sha(obj),map_sha256=sha(mapraw),
                         bss=bss,ordered_original_fixups=[],initialized_source_bytes=0))
    return dict(version=1,kind='original-Master-BGM-track-effect-reserves',
                author_source_sha256=sha(archive['B_DATA.ASM']),
                author_header_sha256=sha(archive['BGM.INC']),
                total_reserve_bytes=3*SIZE,authored_credit=0,rows=rows)


def validate(proof):
    p=json.loads(PARENT.read_text());other=json.loads(OTHER.read_text())
    archive=stored_lzh(pinned(ROOT,p['inputs']['inner_archive']))
    authored_structure(archive['B_DATA.ASM'],archive['BGM.INC'])
    need(proof.get('version')==1 and proof.get('kind')=='original-Master-BGM-track-effect-reserves' and
         proof.get('author_source_sha256')==sha(archive['B_DATA.ASM']) and
         proof.get('author_header_sha256')==sha(archive['BGM.INC']) and
         proof.get('total_reserve_bytes')==594 and proof.get('authored_credit')==0 and
         len(proof.get('rows',[]))==3,'stale BGM sound storage review')
    for row,(name,(build,objname,at,local,size,public)) in zip(proof['rows'],SPECS.items()):
        pins=p['inputs'] if name=='main' else other['table_contexts'][name]['inputs']
        info=other['table_contexts'][name] if name!='main' else None
        expected_art=p['inputs']['target']['sha256'] if name=='main' else info['target_sha256']
        expected_payload=p['target_payload_sha256'] if name=='main' else info['target_payload_sha256']
        base=ROOT/'.analysis/builds'/build/'source/libs/master.lib'
        omf=pinned(ROOT,pins['calibration_object'])
        expected=bss_publics(omf,[('timerorg',local),('part',local+4),('_bgm_part',local+4),
                                 ('esound',local+70),('_bgm_esound',local+70)],size)
        need(row.get('artifact')=='th05-'+name and row.get('start')==at and
             row.get('end')==at+SIZE and row.get('target_sha256')==expected_art and
             row.get('payload_sha256')==expected_payload and
             row.get('native_source_sha256')==sha((base/'bgm[bss].asm').read_bytes()) and
             row.get('native_header_sha256')==sha((base/'bgm.inc').read_bytes()) and
             row.get('object_sha256')==pins['calibration_object']['sha256'] and
             row.get('map_sha256')==pins['calibration_map']['sha256'] and
             row.get('bss')==expected and row.get('ordered_original_fixups')==[] and
             row.get('initialized_source_bytes')==0,
             'BGM track/effect source, true _BSS PUBDEF or target extent changed')


def reviewed_claims(root,views,*,verify_targets=False):
    if not PROOF.exists():return {},None
    raw=PROOF.read_bytes();proof=json.loads(raw);validate(proof)
    if verify_targets:need(review()==proof,'BGM sound source/native review changed')
    out={}
    for row in proof['rows']:
        n=row['artifact'].removeprefix('th05-')
        need(views[n]['sha256']==row['payload_sha256'],'BGM sound data belongs to another target')
        out[n]=[dict(start=row['start'],end=row['end'],
                     kind='reviewed-uninitialized-vendor-storage',
                     content_kind='source-question-mark-struct',
                     library='Master 0.23',member='BGM_TRACK_EFFECT',source='B_DATA.ASM/SPART/SESOUND',
                     authored_credit=0,instruction_bytes=0)]
    return out,sha(raw)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    group=p.add_mutually_exclusive_group(required=True)
    for key in ('write','check','structural-check'):group.add_argument('--'+key,action='store_true')
    args=p.parse_args()
    if args.write:
        value=review();PROOF.write_text(json.dumps(value,indent=2)+'\n')
    else:value=json.loads(PROOF.read_text())
    validate(value)
    if args.check:need(review()==value,'BGM native sound source proof differs')
    print('PASS: original 3x198-byte Master track/effect _BSS, no initialized credit')

if __name__=='__main__':main()
