#!/usr/bin/env python3
"""Prove three original 16-bit SUPERPA state words in MAIN, OP and MAINE.

Only source-written DATA is owned; earlier 32-byte uninitialized patdata and
patsize banks remain unknown. No guessed old BSS or filler ownership.
"""
from __future__ import annotations
import argparse,json,re
from pathlib import Path
from lib.pc98 import parse_mz
from lib.unit_context import UnitContext,load_unit_target
from lib.unit_oracle import relative_fixups
from review_master import pinned,stored_lzh,need,sha
from review_master_bgm_literal_data import actual_data

ROOT=Path(__file__).resolve().parents[1]
PROOF=ROOT/'config/reviewed_master_superpa_initial.json'
PARENT=ROOT/'config/master_vendor_ownership.json'
OTHER=ROOT/'config/master_vendor_additions.json'
# Native original / calibration byte extents and actual member-OBJ local DATA.
SPECS={
 'main':('main-calibration-b',0x210ac,0x210ce,0x65e,'209E:06EE'),
 'op':('op-calibration-a',0xf830,0xf830,0x37e,'0EFE:0850'),
 'maine':('maine-calibration-a',0x1064a,0x1063a,0x47e,'1010:053A'),
}
NAMES=('super_buffer','super_patnum','super_charfree')


def author_words(raw:bytes,encoding:str)->bytes:
    txt=raw.decode(encoding)
    for field in NAMES:
        need(len(re.findall(r'(?im)^\s*'+field+r'\s+dw\s+0\s*(?:;.*)?$',txt))==1,
             'Master SUPERPA source does not initialize unique '+field)
    return b'\x00'*6


def review()->dict:
    parent=json.loads(PARENT.read_text());other=json.loads(OTHER.read_text())
    archive=stored_lzh(pinned(ROOT,parent['inputs']['inner_archive']))
    authored=author_words(archive['SUPERPA.ASM'],'cp932')
    rows=[]
    for name,(build,st,cal,local,public) in SPECS.items():
        base=ROOT/'.analysis/builds'/build/'source'
        text=(base/'libs/master.lib/superpa[data].asm').read_bytes()
        need(author_words(text,'utf8')==authored,'retained original SUPERPA source changed')
        pins=parent['inputs'] if name=='main' else other['table_contexts'][name]['inputs']
        obj=pinned(ROOT,pins['calibration_object']);exe=pinned(ROOT,pins['calibration_exe']);mp=pinned(ROOT,pins['calibration_map'])
        for offset,field in enumerate(NAMES):
            addr=public[:-4]+f'{int(public[-4:],16)+offset*2:04X}'
            need(len(re.findall(r'(?im)^\s*'+addr+r'\s+(?:idle\s+)?_?'+field+r'\s*$',
                                mp.decode('cp437')))==4,'SUPERPA MAP public offset changed '+field)
        chunks=actual_data(obj,local,6)
        need(len(chunks)==1 and chunks[0]['scope_offset']==0 and chunks[0]['scope_size']==6 and
             chunks[0]['scope_content_sha256']==sha(authored),
             'SUPERPA complete actual OMF LEDATA missing or relocated')
        ctx=UnitContext(ROOT,name);art,original,_=load_unit_target(ctx,ctx.config())
        image=parse_mz(exe)
        need(image.valid and original.program_image[st:st+6]==authored and
             image.program_image[cal:cal+6]==authored,
             'original/calibration SUPERPA source words differ')
        need(relative_fixups(original,st,6)==relative_fixups(image,cal,6)==[],
             'SUPERPA initialized words should not have segment relocations')
        rows.append(dict(artifact=art['id'],start=st,end=st+6,
                         source_sha256=sha(text),content_sha256=sha(authored),
                         omf_sha256=sha(obj),map_sha256=sha(mp),exe_sha256=sha(exe),
                         target_sha256=art['sha256'],target_payload_sha256=sha(original.program_image),
                         complete_LEDATA=chunks[0],ordered_original_fixups=[]))
    return dict(version=1,kind='source-linked-Master-SUPERPA-initialized-DATA',
                total_bytes=18,authored_credit=0,
                author_sha256=sha(archive['SUPERPA.ASM']),
                archive_sha256=parent['inputs']['inner_archive']['sha256'],rows=rows)


def validate(proof):
    parent=json.loads(PARENT.read_text());other=json.loads(OTHER.read_text())
    archive=stored_lzh(pinned(ROOT,parent['inputs']['inner_archive']))
    content=author_words(archive['SUPERPA.ASM'],'cp932')
    need(proof.get('version')==1 and proof.get('kind')=='source-linked-Master-SUPERPA-initialized-DATA' and
         proof.get('total_bytes')==18 and proof.get('authored_credit')==0 and
         proof.get('author_sha256')==sha(archive['SUPERPA.ASM']) and
         proof.get('archive_sha256')==parent['inputs']['inner_archive']['sha256'] and
         len(proof.get('rows',[]))==3,'partial/stale source-linked SUPERPA initial state')
    for row,(name,(build,at,cal,local,public)) in zip(proof['rows'],SPECS.items()):
        pins=parent['inputs'] if name=='main' else other['table_contexts'][name]['inputs']
        info=other['table_contexts'][name] if name!='main' else None
        artsha=parent['inputs']['target']['sha256'] if name=='main' else info['target_sha256']
        payloadsha=parent['target_payload_sha256'] if name=='main' else info['target_payload_sha256']
        path=ROOT/'.analysis/builds'/build/'source/libs/master.lib/superpa[data].asm'
        led=row.get('complete_LEDATA',{})
        need(row.get('artifact')=='th05-'+name and row.get('start')==at and row.get('end')==at+6 and
             row.get('target_sha256')==artsha and row.get('target_payload_sha256')==payloadsha and
             row.get('source_sha256')==sha(path.read_bytes()) and
             row.get('content_sha256')==sha(content) and
             row.get('omf_sha256')==pins['calibration_object']['sha256'] and
             row.get('map_sha256')==pins['calibration_map']['sha256'] and
             row.get('exe_sha256')==pins['calibration_exe']['sha256'] and
             row.get('ordered_original_fixups')==[] and
             led.get('scope_size')==6 and led.get('scope_offset')==0 and
             led.get('scope_content_sha256')==sha(content),
             'SUPERPA source, TASM or target identity changed')


def reviewed_claims(root,views,*,verify_targets=False):
    if not PROOF.exists():return {},None
    raw=PROOF.read_bytes();proof=json.loads(raw);validate(proof)
    if verify_targets:need(review()==proof,'SUPERPA source/native data proof differs')
    claims={}
    for row in proof['rows']:
        name=row['artifact'].removeprefix('th05-')
        need(views[name]['sha256']==row['target_payload_sha256'],
             'SUPERPA verified DATA belongs to another target')
        claims[name]=[dict(start=row['start'],end=row['end'],kind='verified-vendor-initialized-data',
                           content_kind='library-initialized-data',instruction_bytes=0,
                           library='Master 0.23',member='SUPERPA_INIT')]
    return claims,sha(raw)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    g=parser.add_mutually_exclusive_group(required=True)
    for x in ('write','check','structural-check'):g.add_argument('--'+x,action='store_true')
    a=parser.parse_args()
    if a.write:
        record=review();PROOF.write_text(json.dumps(record,indent=2)+'\n')
    else:record=json.loads(PROOF.read_text())
    validate(record)
    if a.check:need(record==review(),'original source-backed SUPERPA proof changed')
    print('PASS: Master super_buffer, super_patnum, super_charfree initialized in all three MZs')

if __name__=='__main__':main()
