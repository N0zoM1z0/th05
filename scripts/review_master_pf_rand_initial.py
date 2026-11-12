#!/usr/bin/env python3
"""Verify PF.ASM's five authored DATA bytes and RAND.ASM's four, in three MZs.

The intervening byte is native-side alignment not present in author PF.ASM.
It is expressly not claimed as source data or credited as exact padding.
"""
from __future__ import annotations
import argparse,json,re
from pathlib import Path
from lib.unit_context import UnitContext,load_unit_target
from lib.unit_oracle import relative_fixups
from lib.pc98 import parse_mz
from review_master import pinned,stored_lzh,sha,need
from review_master_bgm_literal_data import actual_data

ROOT=Path(__file__).resolve().parents[1]
PROOF=ROOT/'config/reviewed_master_pf_rand_initial.json'
PARENT=ROOT/'config/master_vendor_ownership.json'
OTHER=ROOT/'config/master_vendor_additions.json'
# Name, retained assembly build, output OBJ, original byte, calibration byte,
# and actual original object-local offset for bbufsiz.
SPECS={'main':('main-calibration-b','main',0x20de2,0x20e04,0x394,'209E:0424'),
       'op':('op-calibration-a','op',0xf566,0xf566,0xb4,'0EFE:0586'),
       'maine':('maine-calibration-a','mainem',0x10380,0x10370,0x1b4,'1010:0270')}


def authored_bytes(archive):
    pf=archive['PF.ASM'].decode('cp932')
    inc=archive['PF.INC'].decode('cp932')
    rand=archive['RAND.ASM'].decode('cp932')
    for text,expression in ((pf,r'(?im)^\s*bbufsiz\s+dw\s+BBUFSIZE\s*$'),
                            (pf,r'(?im)^\s*pferrno\s+dw\s+PFEZERO\s*$'),
                            (pf,r'(?im)^\s*pfkey\s+db\s+0\s*$'),
                            (rand,r'(?im)^\s*random_seed\s+dd\s+1\s*$'),
                            (inc,r'(?im)^\s*BBUFSIZE\s+equ\s+512\s*$'),
                            (inc,r'(?im)^\s*PFEZERO\s*=\s*0\s*(?:;.*)?$')):
        need(re.search(expression,text) is not None, 'original Master PF/RAND author literal changed')
    return b'\x00\x02\x00\x00\x00', b'\x01\x00\x00\x00'


def review():
    parent=json.loads(PARENT.read_text());other=json.loads(OTHER.read_text())
    archive=stored_lzh(pinned(ROOT,parent['inputs']['inner_archive']))
    pf,seed=authored_bytes(archive)
    rows=[]
    for name,(build,objname,original_at,cal_at,local,label) in SPECS.items():
        base=ROOT/'.analysis/builds'/build/'source'
        pf_source=(base/'libs/master.lib/pf[data].asm').read_bytes()
        rand_source=(base/'libs/master.lib/rand[data].asm').read_bytes()
        need(re.search(rb'(?im)^\s*pfkey\s+db\s+0\s*$',pf_source) and
             re.search(rb'(?im)^\s*random_seed\s+dd\s+1\s*$',rand_source),
             'retained original-compiler source has different PF/RAND semantic bytes')
        pins=parent['inputs'] if name=='main' else other['table_contexts'][name]['inputs']
        obj=pinned(ROOT,pins['calibration_object']);exe=pinned(ROOT,pins['calibration_exe']);mp=pinned(ROOT,pins['calibration_map'])
        need(len(re.findall(r'(?im)^\s*'+label+r'\s+(?:idle\s+)?_?bbufsiz\s*$',mp.decode('cp437')))==4,
             'native MAP bbufsiz public is not at source-linked location')
        # RAND follows one native source-side word-alignment byte, unclaimed.
        ds_prefix,offset=label.split(':')
        seed_label=f'{ds_prefix}:{int(offset,16)+6:04X}'
        need(len(re.findall(r'(?im)^\s*'+seed_label+r'\s+(?:idle\s+)?_?random_seed\s*$',mp.decode('cp437')))==4,
             'native MAP random_seed public is not six bytes after PF start')
        ctx=UnitContext(ROOT,name);artifact,target,_=load_unit_target(ctx,ctx.config());cal=parse_mz(exe)
        need(cal.valid, 'invalid calibration MZ')
        for member,off,data,source in (('PF_AUTHORED',0,pf,pf_source),('RAND_SEED',6,seed,rand_source)):
            pieces=actual_data(obj,local+off,len(data))
            need(len(pieces)==1 and pieces[0]['scope_offset']==0 and
                 pieces[0]['scope_size']==len(data) and pieces[0]['scope_content_sha256']==sha(data),
                 'original TASM _DATA LEDATA lacks the complete author source')
            start=original_at+off;calstart=cal_at+off
            need(target.program_image[start:start+len(data)]==data and
                 cal.program_image[calstart:calstart+len(data)]==data,
                 'original or native calibration PF/RAND content differs')
            need(relative_fixups(target,start,len(data))==relative_fixups(cal,calstart,len(data))==[],
                 'PF/RAND has unexpected original MZ relocations')
            rows.append(dict(artifact=artifact['id'],member=member,start=start,end=start+len(data),
                             complete_omf_led=pieces[0],
                             original_payload_sha256=sha(target.program_image),
                             original_artifact_sha256=artifact['sha256'],
                             source_sha256=sha(source),obj_sha256=sha(obj),
                             exe_sha256=sha(exe),map_sha256=sha(mp),
                             source_content_sha256=sha(data),ordered_fixups=[]))
        need(target.program_image[original_at+5]==cal.program_image[cal_at+5]==0,
             'separately excluded PF alignment differs')
    return dict(version=1,kind='source-verified-Master-PF-and-RAND-initialized-data',
                authored_credit=0,total_bytes=27,
                author_pf_sha256=sha(archive['PF.ASM']),author_inc_sha256=sha(archive['PF.INC']),
                author_rand_sha256=sha(archive['RAND.ASM']),
                source_archive_sha256=parent['inputs']['inner_archive']['sha256'],scopes=rows)


def validate(proof):
    parent=json.loads(PARENT.read_text());other=json.loads(OTHER.read_text())
    a=stored_lzh(pinned(ROOT,parent['inputs']['inner_archive']))
    pf,seed=authored_bytes(a)
    need(proof.get('version')==1 and proof.get('kind')=='source-verified-Master-PF-and-RAND-initialized-data' and
         proof.get('authored_credit')==0 and proof.get('total_bytes')==27 and
         proof.get('author_pf_sha256')==sha(a['PF.ASM']) and
         proof.get('author_inc_sha256')==sha(a['PF.INC']) and
         proof.get('author_rand_sha256')==sha(a['RAND.ASM']) and
         proof.get('source_archive_sha256')==parent['inputs']['inner_archive']['sha256'] and
         len(proof.get('scopes',[]))==6,'stale/partial original Master PF/RAND evidence')
    for i,(name,(build,objname,original,cal,local,label)) in enumerate(SPECS.items()):
        pins=parent['inputs'] if name=='main' else other['table_contexts'][name]['inputs']
        info=other['table_contexts'][name] if name!='main' else None
        original_artifact=parent['inputs']['target']['sha256'] if name=='main' else info['target_sha256']
        original_payload=parent['target_payload_sha256'] if name=='main' else info['target_payload_sha256']
        for j,(member,off,payload,source_name) in enumerate((('PF_AUTHORED',0,pf,'pf[data].asm'),('RAND_SEED',6,seed,'rand[data].asm'))):
            row=proof['scopes'][2*i+j]
            src=ROOT/'.analysis/builds'/build/'source/libs/master.lib'/source_name
            led=row.get('complete_omf_led',{})
            need(row.get('artifact')=='th05-'+name and row.get('member')==member and
                 row.get('start')==original+off and row.get('end')==original+off+len(payload) and
                 row.get('source_content_sha256')==sha(payload) and row.get('source_sha256')==sha(src.read_bytes()) and
                 row.get('original_artifact_sha256')==original_artifact and
                 row.get('original_payload_sha256')==original_payload and
                 row.get('obj_sha256')==pins['calibration_object']['sha256'] and
                 row.get('exe_sha256')==pins['calibration_exe']['sha256'] and
                 row.get('map_sha256')==pins['calibration_map']['sha256'] and
                 row.get('ordered_fixups')==[] and led.get('scope_offset')==0 and
                 led.get('scope_size')==len(payload) and led.get('scope_content_sha256')==sha(payload),
                 'unreviewed PF/RAND target, position or source byte')


def reviewed_claims(root,views,*,verify_targets=False):
    if not PROOF.exists():return {},None
    raw=PROOF.read_bytes();proof=json.loads(raw);validate(proof)
    if verify_targets:need(review()==proof,'native PF/RAND source-linked replay changed')
    groups={}
    for r in proof['scopes']:
        n=r['artifact'].removeprefix('th05-')
        need(views[n]['sha256']==r['original_payload_sha256'],'PF/RAND target identity mismatch')
        groups.setdefault(n,[]).append(dict(start=r['start'],end=r['end'],kind='verified-vendor-initialized-data',
                                            content_kind='library-initialized-data',instruction_bytes=0,
                                            library='Master 0.23',member=r['member']))
    return groups,sha(raw)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    g=p.add_mutually_exclusive_group(required=True)
    for mode in ('write','check','structural-check'):g.add_argument('--'+mode,action='store_true')
    opt=p.parse_args()
    if opt.write:proof=review();PROOF.write_text(json.dumps(proof,indent=2)+'\n')
    else:proof=json.loads(PROOF.read_text())
    validate(proof)
    if opt.check:need(review()==proof,'original PF/RAND verification no longer matches')
    print('PASS: PF 5 + RAND 4 source-authored bytes in MAIN/OP/MAINE; padding excluded')

if __name__=='__main__':main()
