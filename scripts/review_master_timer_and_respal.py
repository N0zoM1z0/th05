#!/usr/bin/env python3
"""Verify source-backed BGM timer-divider DATA in all MZs and OP palette ID.

The preceding reserved/palette-alignment bytes are intentionally excluded.
"""
from __future__ import annotations
import argparse,json,re
from pathlib import Path
from lib.pc98 import parse_mz
from lib.unit_context import UnitContext,load_unit_target
from lib.unit_oracle import relative_fixups
from review_master import pinned,stored_lzh,sha,need
from review_master_bgm_literal_data import actual_data
ROOT=Path(__file__).resolve().parents[1]
PROOF=ROOT/'config/reviewed_master_timer_and_respal.json'
PARENT=ROOT/'config/master_vendor_ownership.json'
OTHER=ROOT/'config/master_vendor_additions.json'
TIMER={
 'main':('main-calibration-b',0x210b2,0x210d4,0x664,'209E:06F4'),
 'op':('op-calibration-a',0xf842,0xf842,0x390,'0EFE:0862'),
 'maine':('maine-calibration-a',0x10650,0x10640,0x484,'1010:0540'),
}
PALETTE=('op-calibration-a',0xf836,0xf836,0x384,'0EFE:0856')


def review():
    parent=json.loads(PARENT.read_text());other=json.loads(OTHER.read_text())
    archive=stored_lzh(pinned(ROOT,parent['inputs']['inner_archive']))
    authored=archive['B_TMHOOK.ASM'].decode('cp932')
    need(len(re.findall(r'(?im)^\s*intdiv\s+dw\s+1\s*$',authored))==1,
         'original Master timer divider no longer starts at 1')
    rows=[]
    for name,(build,st,calst,local,public) in TIMER.items():
        base=ROOT/'.analysis/builds'/build/'source'
        src=(base/'libs/master.lib/bgm_timerhook[data].asm').read_bytes()
        need(len(re.findall(rb'(?im)^\s*intdiv\s+dw\s+1\s*$',src))==1,
             'retained original BGM timer source changed')
        rows.append(_scope(parent,other,name,build,st,calst,local,public,
                           'BGM_INTDIV',b'\x01\x00',src,'intdiv'))
    build,st,calst,local,public=PALETTE
    source=(ROOT/'.analysis/builds'/build/'source/libs/master.lib/respal_exist[data].asm').read_bytes()
    need(len(re.findall(rb"(?im)^\s*ResPalID\s+db\s+'pal98 grb',\s*0\s*$",source))==1,
         'ReC98 palette ID source changed')
    rows.append(_scope(parent,other,'op',build,st,calst,local,public,
                       'RESPAL_ID',b'pal98 grb\0',source,'ResPalID'))
    # The two bytes between ResPalID and intdiv remain unreviewed (FF FF).
    ctx=UnitContext(ROOT,'op');_,im,_=load_unit_target(ctx,ctx.config())
    need(im.program_image[0xf840:0xf842]==b'\xff\xff',
         'intervening foreign state changed, do not include in ResPalID')
    return dict(version=1,kind='Master-timer-divider-and-OP-palette-ID',
                authored_credit=0,total_bytes=16,
                author_B_TMHOOK_sha256=sha(archive['B_TMHOOK.ASM']),
                original_archive_sha256=parent['inputs']['inner_archive']['sha256'],
                scopes=rows)


def _scope(parent,other,name,build,start,calstart,local,public,member,value,src,symbol):
    base=ROOT/'.analysis/builds'/build/'source'
    pins=parent['inputs'] if name=='main' else other['table_contexts'][name]['inputs']
    obj=pinned(ROOT,pins['calibration_object']);exe=pinned(ROOT,pins['calibration_exe']);mp=pinned(ROOT,pins['calibration_map'])
    need(len(re.findall(r'(?im)^\s*'+public+r'\s+(?:idle\s+)?'+symbol+r'\s*$',
                        mp.decode('cp437')))==2,'actual Master timer/ResPal MAP public not found')
    chunks=actual_data(obj,local,len(value))
    need(len(chunks)==1 and chunks[0]['scope_size']==len(value) and
         chunks[0]['scope_offset']==0 and chunks[0]['scope_content_sha256']==sha(value),
         'native Master source does not write entire timer/palette ID')
    c=UnitContext(ROOT,name);art,original,_=load_unit_target(c,c.config());cal=parse_mz(exe)
    need(cal.valid and original.program_image[start:start+len(value)]==value and
         cal.program_image[calstart:calstart+len(value)]==value,
         'Master timer or palette ID differs in original/calibration')
    need(relative_fixups(original,start,len(value))==relative_fixups(cal,calstart,len(value))==[],
         'timer/ID has unexpected original MZ fixup')
    return dict(artifact=art['id'],start=start,end=start+len(value),member=member,
                value_sha256=sha(value),source_sha256=sha(src),
                original_sha256=art['sha256'],original_payload_sha256=sha(original.program_image),
                omf_sha256=sha(obj),map_sha256=sha(mp),exe_sha256=sha(exe),
                complete_source_LED=chunks[0],ordered_fixups=[])


def validate(proof):
    parent=json.loads(PARENT.read_text());other=json.loads(OTHER.read_text())
    archive=stored_lzh(pinned(ROOT,parent['inputs']['inner_archive']))
    need(proof.get('version')==1 and proof.get('kind')=='Master-timer-divider-and-OP-palette-ID' and
         proof.get('authored_credit')==0 and proof.get('total_bytes')==16 and
         proof.get('author_B_TMHOOK_sha256')==sha(archive['B_TMHOOK.ASM']) and
         proof.get('original_archive_sha256')==parent['inputs']['inner_archive']['sha256'] and
         len(proof.get('scopes',[]))==4,'partial/stale timer and ResPal source proof')
    for row,(name,(build,at,cal,local,public)) in zip(proof['scopes'][:3],TIMER.items()):
        _validate_one(row,name,build,at,2,'BGM_INTDIV',b'\x01\0',
                      ROOT/'.analysis/builds'/build/'source/libs/master.lib/bgm_timerhook[data].asm',parent,other)
    b,st,_,_,_=PALETTE
    _validate_one(proof['scopes'][3],'op',b,st,10,'RESPAL_ID',b'pal98 grb\0',
                  ROOT/'.analysis/builds'/b/'source/libs/master.lib/respal_exist[data].asm',parent,other)


def _validate_one(row,name,build,start,size,member,value,src,parent,other):
    pins=parent['inputs'] if name=='main' else other['table_contexts'][name]['inputs']
    info=other['table_contexts'][name] if name!='main' else None
    artsha=parent['inputs']['target']['sha256'] if name=='main' else info['target_sha256']
    payloadsha=parent['target_payload_sha256'] if name=='main' else info['target_payload_sha256']
    led=row.get('complete_source_LED',{})
    need(row.get('artifact')=='th05-'+name and row.get('start')==start and row.get('end')==start+size and
         row.get('member')==member and row.get('value_sha256')==sha(value) and
         row.get('source_sha256')==sha(src.read_bytes()) and
         row.get('original_sha256')==artsha and row.get('original_payload_sha256')==payloadsha and
         row.get('omf_sha256')==pins['calibration_object']['sha256'] and
         row.get('map_sha256')==pins['calibration_map']['sha256'] and
         row.get('exe_sha256')==pins['calibration_exe']['sha256'] and
         row.get('ordered_fixups')==[] and led.get('scope_offset')==0 and
         led.get('scope_size')==size and led.get('scope_content_sha256')==sha(value),
         'Master timer/palette source/native/target identity changed')


def reviewed_claims(root,views,*,verify_targets=False):
    if not PROOF.exists():return {},None
    raw=PROOF.read_bytes();proof=json.loads(raw);validate(proof)
    if verify_targets:need(proof==review(),'timer/ResPal native review changed')
    claims={}
    for row in proof['scopes']:
        name=row['artifact'].removeprefix('th05-')
        need(views[name]['sha256']==row['original_payload_sha256'],
             'timer/ResPal source applied to wrong original MZ')
        claims.setdefault(name,[]).append(dict(start=row['start'],end=row['end'],
            kind='verified-vendor-initialized-data',content_kind='library-initialized-data',
            instruction_bytes=0,library='Master 0.23',member=row['member']))
    return claims,sha(raw)


def main():
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True)
    for x in ('write','check','structural-check'):g.add_argument('--'+x,action='store_true')
    a=p.parse_args()
    if a.write:proof=review();PROOF.write_text(json.dumps(proof,indent=2)+'\n')
    else:proof=json.loads(PROOF.read_text())
    validate(proof)
    if a.check:need(proof==review(),'timer/ResPal authored source/native replay changed')
    print('PASS: Master BGM timer 2 bytes in 3 MZs and OP palette ID 10 bytes')

if __name__=='__main__':main()
