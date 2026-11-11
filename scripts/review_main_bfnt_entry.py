#!/usr/bin/env python3
"""Complete source-derived Master BFNT font-entry functions in TH05 MAIN.

The original BFTENTRY.ASM is changed only by two equivalent long-error
branches and private-label names. Every actual TASM LEDATA byte/FIXUPP is
resolved by the unchanged original MAIN link model, without target patching.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
from lib.pc98 import parse_mz,digest_file
from lib.unit_oracle import relative_fixups
from review_master import object_text,source_blocks,stored_lzh,pinned,need,sha
from review_master_bgm import linked_scope
from review_master_grcg import symbolic_source
from review_main_runtime import startup

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'config/master_vendor_ownership.json'
PROOF=ROOT/'config/main_bfnt_entry_ownership.json'
DECISION=ROOT/'config/reviewed_main_bfnt_entry.json'
FILE='libs/master.lib/bfnt_entry_pat.asm'
ORIG='BFTENTRY.ASM'
MEMBERS=(('BFTENTRY_INVAL','INVAL',0x272,20),
         ('BFNT_ENTRY_PAT','BFNT_ENTRY_PAT',0x286,302))
FIXUP_COUNTS={'BFTENTRY_INVAL':1,'BFNT_ENTRY_PAT':10}


def derived_source(author,actual,name):
    if name=='BFTENTRY_INVAL':
        need(author.count('retfuncinval')==author.count('fault:mreturn')==1,
             'missing original BFNT near-err exit and local fault label')
        expected=[v.replace('retfuncinval','retfuncbftentry_inval')
                    .replace('fault:mreturn','bftentry_fault:mreturn') for v in author]
    elif name=='BFNT_ENTRY_PAT':
        need(author.count('jcshortfault')==2 and
             author.count('jcinval')==author.count('jneinval')==1,
             'original BFNT entry error branches changed')
        expected=[v.replace('jcshortfault','jcshortbftentry_fault') for v in author]
        at=expected.index('jcinval')
        expected[at:at+1]=['ifldata','jnbnext_pattern_1','jmpbftentry_inval',
                           'else','jbbftentry_inval','endif','next_pattern_1:']
        at=expected.index('jneinval')
        expected[at:at+1]=['jznext_pattern_2','jmpbftentry_inval','next_pattern_2:']
    else:
        raise ValueError('unreviewed original BFNT procedure')
    need(expected==actual,'TH05 BFNT source differs outside original label and error-branch adaptation')
    return sha('\n'.join(expected).encode('utf8'))


def replay():
    p=json.loads(BASE.read_text())
    author_archive=stored_lzh(pinned(ROOT,p['inputs']['inner_archive']))
    upstream={b['name']:b for b in source_blocks(author_archive[ORIG],'cp932')}
    frozen={x['name']:x for x in p['frozen_source_closure']}
    raw=(ROOT/p['candidate_source_root']/FILE).read_bytes()
    need(sha(raw)==frozen[FILE]['sha256'],'real TASM BFNT entry source hash changed')
    compiled={b['name']:b for b in source_blocks(raw,'utf8')}
    inventory={v['name']:v for v in p['active_procedure_inventory']}
    obj_bytes=pinned(ROOT,p['inputs']['saved_object'])
    need(obj_bytes==pinned(ROOT,p['inputs']['calibration_object']),
         'original BFNT source assembly and calibration object differ')
    obj=object_text(obj_bytes)
    cal=parse_mz(pinned(ROOT,p['inputs']['calibration_exe']))
    native=parse_mz(pinned(ROOT,p['inputs']['target']))
    before,after=startup(cal),startup(native)
    need((before['dgroup'],after['dgroup'],after['init_start']-before['init_start'])==
         (0x209e0,0x209d0,-18),'original BFNT MAIN CRT data frame changed')
    rows=[]
    for name,orig,start,size in MEMBERS:
        need((inventory[name]['start'],inventory[name]['end'],inventory[name]['source'])==
             (start,start+size,FILE),'real linked BFNT procedure boundaries differ')
        old,new=upstream[orig],compiled[name]
        canonical=derived_source(symbolic_source(old['text']),symbolic_source(new['text']),name)
        cb,nb,unlinked,mz,fixups=linked_scope(obj,start,size)
        observed=native.program_image[start:start+size]
        need(cb==cal.program_image[start:start+size] and nb==observed,
             'original BFNT complete native CODE differs: '+name)
        need(relative_fixups(cal,start,size)==relative_fixups(native,start,size)==mz,
             'original BFNT MZ relocation order differs')
        need(native.program_image.find(observed)==start and
             native.program_image.find(observed,start+1)==-1,
             'original BFNT complete routine not uniquely located')
        rows.append({'member':name,'original_author_name':orig,'start':start,
                     'end':start+size,'size':size,'source':FILE,
                     'original_archive_source':ORIG,'original_block_sha256':sha(old['text'].encode('utf8')),
                     'actual_source_sha256':sha(new['text'].encode('utf8')),
                     'derived_source_sha256':canonical,
                     'unlinked_CODE_sha256':unlinked,'calibrated_CODE_sha256':sha(cb),
                     'native_CODE_sha256':sha(nb),'ordered_original_MZ':mz,
                     'ordered_OMF_actions':fixups,'authored_credit':0})
    return {'schema_version':1,'kind':'original-master-BFNT-game-port-source-linked',
            'artifact':'th05-main','members':rows,
            'CODE_bytes':sum(r['size'] for r in rows),
            'actual_TASM_source_sha256':sha(raw),
            'original_target_sha256':p['inputs']['target']['sha256'],
            'real_OMF_sha256':p['inputs']['saved_object']['sha256'],
            'calibration_sha256':p['inputs']['calibration_exe']['sha256'],
            'author_archive_sha256':p['inputs']['inner_archive']['sha256'],
            'parent_Master_sha256':digest_file(BASE),
            'verifier_sha256':digest_file(ROOT/'scripts/review_main_bfnt_entry.py'),
            'authored_credit':0,'non_CODE_claimed':0}


def validate(j):
    p=json.loads(BASE.read_text())
    need(j.get('schema_version')==1 and j.get('kind')=='original-master-BFNT-game-port-source-linked' and
         j.get('artifact')=='th05-main' and j.get('CODE_bytes')==322 and
         j.get('original_target_sha256')==p['inputs']['target']['sha256'] and
         j.get('real_OMF_sha256')==p['inputs']['saved_object']['sha256'] and
         j.get('calibration_sha256')==p['inputs']['calibration_exe']['sha256'] and
         j.get('author_archive_sha256')==p['inputs']['inner_archive']['sha256'] and
         j.get('parent_Master_sha256')==digest_file(BASE) and
         j.get('verifier_sha256')==digest_file(ROOT/'scripts/review_main_bfnt_entry.py') and
         j.get('authored_credit')==j.get('non_CODE_claimed')==0,
         'BFNT original source/OMF or verifier identity differs')
    items=j.get('members',[])
    need([(x.get('member'),x.get('original_author_name'),x.get('start'),x.get('size'))
          for x in items]==list(MEMBERS),'original full BFNT functions changed')
    need(isinstance(j.get('actual_TASM_source_sha256'),str) and
         re.fullmatch('[0-9a-f]{64}',j['actual_TASM_source_sha256']),
         'missing source-backed native TASM file identity')
    for x in items:
        need(x.get('end')==x['start']+x['size'] and x.get('source')==FILE and
             x.get('original_archive_source')==ORIG and x.get('authored_credit')==0 and
             len(x.get('ordered_OMF_actions',[]))==FIXUP_COUNTS[x['member']] and
             x.get('ordered_original_MZ')==
             [f['source_site'] for f in x['ordered_OMF_actions']
              if f['original_link_operation']=='original-MZ-segment16'],
             'original BFNT whole extent or FIXUPP sequence differs')
        for field in ('original_block_sha256','actual_source_sha256','derived_source_sha256',
                      'unlinked_CODE_sha256','calibrated_CODE_sha256','native_CODE_sha256'):
            need(isinstance(x.get(field),str) and re.fullmatch('[0-9a-f]{64}',x[field]),
                 'missing original BFNT source or CODE SHA')
    if DECISION.exists():
        d=json.loads(DECISION.read_text())
        need(d.get('schema_version')==1 and d.get('decision')=='ADOPT_TWO_ORIGINAL_MASTER_BFNT_PROCEDURES' and
             d.get('evidence_sha256')==digest_file(PROOF) and
             d.get('members')==[name for name,_,_,_ in MEMBERS] and
             d.get('CODE_bytes')==322 and
             d.get('authored_credit')==d.get('other_claims')==0,
             'explicit original BFNT adoption missing or stale')


def reviewed_claims(root,view,*,verify_targets=False):
    if not DECISION.exists():return [],None
    need(root.resolve()==ROOT.resolve(),'wrong source checkout')
    proof=json.loads(PROOF.read_text());validate(proof)
    need(view['sha256']==json.loads(BASE.read_text())['target_payload_sha256'],
         'wrong original MAIN target identity')
    if verify_targets:need(replay()==proof,'real original BFNT source-linked CODE differs')
    return ([{'start':r['start'],'end':r['end'],'kind':'verified-vendor-code',
              'library':'master.lib 0.23-derived BFNT','member':r['member'],
              'authored_credit':0} for r in proof['members']],digest_file(DECISION))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    modes=parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--write',action='store_true')
    modes.add_argument('--check',action='store_true')
    modes.add_argument('--structural-check',action='store_true')
    args=parser.parse_args()
    if args.write:
        need(not PROOF.exists() and not DECISION.exists(),'will not overwrite reviewed native BFNT code')
        j=replay();PROOF.write_text(json.dumps(j,indent=2)+'\n')
        print('PASS original BFNT source-linked CODE',j['CODE_bytes'])
    else:
        j=json.loads(PROOF.read_text());validate(j)
        if args.check:
            need(replay()==j,'actual original BFNT OMF/MZ differs')
            print('PASS original complete BFNT functions and ordered MZ relocations')
        else:print('PASS original BFNT source/decision structural proof')

if __name__=='__main__':main()
