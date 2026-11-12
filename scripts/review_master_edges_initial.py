#!/usr/bin/env python3
"""Source-link Master 0.23's original 17-word EDGES raster mask table in all MZs.

The table lies between previously accepted CLIP and FIL contributions and
contains initialized semantic bitmasks, not machine-code instructions.
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
PROOF=ROOT/'config/reviewed_master_edges_initial.json'
PARENT=ROOT/'config/master_vendor_ownership.json'
OTHER=ROOT/'config/master_vendor_additions.json'
SPECS={
 'main':('main-calibration-b',0x20d4c,0x20d6e,0x2fe,'209E:038E'),
 'op':('op-calibration-a',0xf4d0,0xf4d0,0x1e,'0EFE:04F0'),
 'maine':('maine-calibration-a',0x102ea,0x102da,0x11e,'1010:01DA'),
}


def words(raw:bytes,encoding:str)->bytes:
    text=raw.decode(encoding)
    data=[]
    for l in text.splitlines():
        head=l.split(';',1)[0].strip()
        m=re.fullmatch(r'(?:EDGES\s+)?dw\s+([01]{16})b',head,re.I)
        if m:data.append(int(m.group(1),2))
    expected=[0]+[((0xff<<(8-k))&0xff) for k in range(1,9)]+\
             [((((0xff<<(16-k))&0xff)<<8)|0xff) for k in range(9,17)]
    need(data==expected and len(data)==17,
         'Master left/right raster clipping masks no longer have 17 source words')
    need(len(re.findall(r'(?im)^\s*public\s+EDGES\s*$',text))==1,
         'Master EDGES exported label missing')
    return b''.join(v.to_bytes(2,'little') for v in data)


def review():
    parent=json.loads(PARENT.read_text());other=json.loads(OTHER.read_text())
    archive=stored_lzh(pinned(ROOT,parent['inputs']['inner_archive']))
    author=archive['EDGES.ASM'];data=words(author,'cp932')
    scopes=[]
    for name,(build,st,calst,local,public) in SPECS.items():
        base=ROOT/'.analysis/builds'/build/'source'
        src=(base/'libs/master.lib/edges[data].asm').read_bytes()
        need(words(src,'utf8')==data,'retained EDGES TASM source differs from Master archive')
        pins=parent['inputs'] if name=='main' else other['table_contexts'][name]['inputs']
        obj=pinned(ROOT,pins['calibration_object']);exe=pinned(ROOT,pins['calibration_exe']);mp=pinned(ROOT,pins['calibration_map'])
        need(len(re.findall(r'(?im)^\s*'+public+r'\s+(?:idle\s+)?EDGES\s*$',mp.decode('cp437')))==2,
             'real native MAP does not export EDGES at its target DATA location')
        chunks=actual_data(obj,local,len(data))
        need(len(chunks)==1 and chunks[0]['scope_offset']==0 and
             chunks[0]['scope_size']==len(data) and chunks[0]['scope_content_sha256']==sha(data),
             'native original TASM object does not write all 34 EDGES bytes')
        c=UnitContext(ROOT,name);art,target,_=load_unit_target(c,c.config());cal=parse_mz(exe)
        need(cal.valid and target.program_image[st:st+len(data)]==data and
             cal.program_image[calst:calst+len(data)]==data,
             'original EDGES masks differ in real EXE or calibration MZ')
        need(relative_fixups(target,st,len(data))==relative_fixups(cal,calst,len(data))==[],
             'EDGES bitmask table unexpectedly contains an MZ relocation')
        scopes.append(dict(artifact=art['id'],start=st,end=st+len(data),
                           source_sha256=sha(src),data_sha256=sha(data),
                           omf_sha256=sha(obj),map_sha256=sha(mp),exe_sha256=sha(exe),
                           target_sha256=art['sha256'],target_payload_sha256=sha(target.program_image),
                           complete_LED=chunks[0],ordered_fixups=[]))
    return dict(version=1,kind='source-linked-Master-EDGES-raster-data',
                authored_credit=0,total_bytes=102,
                original_author_sha256=sha(author),
                archive_sha256=parent['inputs']['inner_archive']['sha256'],
                scopes=scopes)


def validate(proof):
    parent=json.loads(PARENT.read_text());other=json.loads(OTHER.read_text())
    archive=stored_lzh(pinned(ROOT,parent['inputs']['inner_archive']))
    author=archive['EDGES.ASM'];data=words(author,'cp932')
    need(proof.get('version')==1 and proof.get('kind')=='source-linked-Master-EDGES-raster-data' and
         proof.get('authored_credit')==0 and proof.get('total_bytes')==102 and
         proof.get('original_author_sha256')==sha(author) and
         proof.get('archive_sha256')==parent['inputs']['inner_archive']['sha256'] and
         len(proof.get('scopes',[]))==3,'partial/stale original Master EDGES provenance')
    for row,(name,(build,st,cal,local,label)) in zip(proof['scopes'],SPECS.items()):
        pins=parent['inputs'] if name=='main' else other['table_contexts'][name]['inputs']
        info=other['table_contexts'][name] if name!='main' else None
        artsha=parent['inputs']['target']['sha256'] if name=='main' else info['target_sha256']
        payloadsha=parent['target_payload_sha256'] if name=='main' else info['target_payload_sha256']
        src=ROOT/'.analysis/builds'/build/'source/libs/master.lib/edges[data].asm'
        led=row.get('complete_LED',{})
        need(row.get('artifact')=='th05-'+name and row.get('start')==st and row.get('end')==st+34 and
             row.get('data_sha256')==sha(data) and row.get('source_sha256')==sha(src.read_bytes()) and
             row.get('omf_sha256')==pins['calibration_object']['sha256'] and
             row.get('map_sha256')==pins['calibration_map']['sha256'] and
             row.get('exe_sha256')==pins['calibration_exe']['sha256'] and
             row.get('target_sha256')==artsha and row.get('target_payload_sha256')==payloadsha and
             row.get('ordered_fixups')==[] and led.get('scope_offset')==0 and
             led.get('scope_size')==34 and led.get('scope_content_sha256')==sha(data),
             'wrong EDGES source, TASM object, MZ target or complete table extent')


def reviewed_claims(root,views,*,verify_targets=False):
    if not PROOF.exists():return {},None
    raw=PROOF.read_bytes();proof=json.loads(raw);validate(proof)
    if verify_targets:need(proof==review(),'native Master EDGES source-linked replay differs')
    result={}
    for row in proof['scopes']:
        n=row['artifact'].removeprefix('th05-')
        need(views[n]['sha256']==row['target_payload_sha256'],
             'Master EDGES proof belongs to another decoded executable')
        result[n]=[dict(start=row['start'],end=row['end'],kind='verified-vendor-initialized-data',
                        content_kind='library-initialized-data',instruction_bytes=0,
                        library='Master 0.23',member='EDGES')]
    return result,sha(raw)


def main():
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True)
    for mode in ('write','check','structural-check'):g.add_argument('--'+mode,action='store_true')
    args=p.parse_args()
    if args.write:
        proof=review();PROOF.write_text(json.dumps(proof,indent=2)+'\n')
    else:proof=json.loads(PROOF.read_text())
    validate(proof)
    if args.check:need(proof==review(),'Master EDGES original source/target proof differs')
    print('PASS: exact 17-word Master EDGES initialized raster masks in MAIN/OP/MAINE')

if __name__=='__main__':main()
