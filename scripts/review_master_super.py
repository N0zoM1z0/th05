#!/usr/bin/env python3
"""Bounded original Master SUPER assembly CODE, with original DATA relocations.

The original 0.23 archive and the pinned TASM-built MAIN OMF are independent
source evidence. Normalization in this review is limited to local-symbol
namespacing in the maintained port, comments and layout whitespace, never
instruction syntax or arbitrary operand values. Source-authorship credit is 0.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

from lib.pc98 import parse_mz, digest_file
from lib.unit_oracle import relative_fixups
from review_master import object_text, source_blocks, stored_lzh, need, sha
from review_main_runtime import startup

ROOT = Path(__file__).resolve().parents[1]
PROOF = ROOT/'config/master_super_ownership.json'
DECISION = ROOT/'config/reviewed_master_super.json'
BASE = ROOT/'config/master_vendor_ownership.json'
MEMBERS = (
    ('SUPER_ENTRY_PAT', 0x2a2e, 172),
    ('SUPER_PUT_1PLANE', 0x2ada, 456),
    ('SUPER_ENTRY_AT', 0x2ca2, 116),
    ('SUPER_CANCEL_PAT', 0x2da0, 80),
    ('SUPER_CLEAN', 0x2df0, 42),
    ('SUPER_ROLL_PUT_1PLANE', 0x2e1a, 454),
    ('SUPER_PUT', 0x33f0, 240),
    ('SUPER_CONVERT_TINY', 0x35a2, 156),
)
BIAS = 0x272
# The real map gives the _DATA 90h and _BSS 262Ch segment offsets.
# The original C0L/startup and eight independently verified CL DATA anchors
# establish -12h for all corresponding original target words.
CALIBRATED_OFFSETS = {1: BIAS, 2: 0x90, 54: 0x262c}
GROUP_TARGETS = {2, 54}
DATA_DELTA = -18


def source_lines(body):
    """Explicit namespaces of local data/labels, not opcode normalization."""
    body = body.lower().replace('@@','')
    for old,new in (('superl1p_', ''),('superput_', ''),
                    ('superpat_no_memory', 'no_memory')):
        body = body.replace(old,new)
    return [re.sub(r'\s+','',row.split(';',1)[0])
            for row in body.splitlines() if row.split(';',1)[0].strip()]


def original_source_proof(base):
    archive = ROOT/base['inputs']['inner_archive']['file']
    upstream = stored_lzh(archive.read_bytes())
    # Do not silently substitute a different copied ReC98 source or archive.
    candidates = {}
    for row in base['frozen_source_closure']:
        source = row['name']
        if not source.startswith('libs/master.lib/') or not source.endswith('.asm'):
            continue
        path=ROOT/base['candidate_source_root']/source
        if not path.exists():continue
        need(sha(path.read_bytes())==row['sha256'],'actual native-compiled Master source changed')
        candidates[source] = path.read_bytes()
    original = {}
    for filename,raw in upstream.items():
        if not filename.upper().endswith('.ASM'):continue
        try: blocks = source_blocks(raw,'cp932')
        except UnicodeDecodeError:continue
        for block in blocks:
            original.setdefault(block['name'].casefold(),[]).append(
                (filename, block))
    context = {row['name']:row for row in base['active_procedure_inventory']}
    proven = {}
    for member,start,size in MEMBERS:
        row=context[member]
        need((row['start'],row['end'])==(start,start+size),
             'original active TASM listing function boundaries drifted')
        need(row['source'] in candidates,'original source file not in actual compiled OMF closure')
        native_blocks=[z for z in source_blocks(candidates[row['source']],'utf8')
                       if z['name']==member]
        archive_blocks=original.get(member.casefold(),[])
        same = [(filename,src,native_blocks[0]) for filename,src in archive_blocks
                if len(native_blocks)==1 and
                source_lines(src['text'])==source_lines(native_blocks[0]['text'])]
        need(len(same)==1,'complete original author source differs in nonlocal instructions')
        archive_file,up,local=same[0]
        canonical='\n'.join(source_lines(up['text']))
        proven[member]={'upstream_member':archive_file,
                        'upstream_source_block_sha256':sha(up['text'].encode('utf8')),
                        'candidate_file':row['source'],
                        'candidate_source_file_sha256':sha(candidates[row['source']]),
                        'candidate_source_block_sha256':sha(local['text'].encode('utf8')),
                        'semantic_source_sha256':sha(canonical.encode('utf8')),
                        'source_line_span':[local['start_line'],local['end_line']],
                        'original_language':'TASM-8086-source-with-local-symbol-namespace'}
    return proven


def code_scope(obj,start,size,*,delta=DATA_DELTA):
    lo=start-BIAS
    out=bytearray(size);cover=bytearray(size)
    for row in obj['blocks']:
        a=max(lo,row['offset'])
        b=min(lo+size,row['offset']+len(row['content']))
        if a>=b:continue
        sa=a-lo;sb=b-lo
        need(not any(cover[sa:sb]),'original TASM CODE source LEDATA overlap')
        out[sa:sb]=row['content'][a-row['offset']:b-row['offset']]
        cover[sa:sb]=b'\1'*(sb-sa)
    need(all(cover),'incomplete original full function CODE source')
    unlinked_sha=sha(out)
    control=bytearray(out);native=bytearray(out)
    actions=[];written=set()
    for f in obj['fixups']:
        abs_site=f['offset']+BIAS
        width={1:2,2:2,3:4}[f['kind']]
        if abs_site+width<=start or abs_site>=start+size:continue
        need(start<=abs_site and abs_site+width<=start+size,
             'original OMF FIXUPP crosses complete function boundary')
        ti=f['target_index'];fm=f['frame_method']
        need(f['kind']==1 and f['absolute'] and f['target_method']==0 and
             f['displacement']==0 and ti in CALIBRATED_OFFSETS and
             ((ti==1 and fm==5) or (ti==2 and fm in (1,5)) or
              (ti==54 and fm in (0,1))) and
             ((fm==0 and f['frame_index']==2) or
              (fm==1 and f['frame_index']==1) or fm==5),
             'unmodeled native TASM original symbol/FIXUPP type')
        index=abs_site-start
        need(not written.intersection(range(index,index+2)),
             'original real FIXUPP double writes source words')
        written.update(range(index,index+2))
        old=int.from_bytes(out[index:index+2],'little')
        cal_add=CALIBRATED_OFFSETS[ti]
        orig_add=cal_add+(delta if ti in GROUP_TARGETS else 0)
        c=(old+cal_add)&65535;n=(old+orig_add)&65535
        control[index:index+2]=c.to_bytes(2,'little')
        native[index:index+2]=n.to_bytes(2,'little')
        actions.append({'site':index,'kind':1,'source_target_SEGDEF':ti,
                        'frame_method':fm,'frame_index':f['frame_index'],
                        'original_group_offset_delta':delta if ti in GROUP_TARGETS else 0,
                        'calibrated_word_sha256':sha(c.to_bytes(2,'little')),
                        'original_word_sha256':sha(n.to_bytes(2,'little'))})
    return bytes(control),bytes(native),unlinked_sha,actions


def replay():
    base=json.loads(BASE.read_text())
    paths=base['inputs']
    from review_master import pinned
    # Source and TASM object producer identities are inherited from the
    # earlier pinned 17,270-byte original-assembly calibration.
    raw_obj=pinned(ROOT,paths['saved_object'])
    need(raw_obj==pinned(ROOT,paths['calibration_object']),
         'actual source OMF differs from original native calibration')
    control=parse_mz(pinned(ROOT,paths['calibration_exe']))
    native=parse_mz(pinned(ROOT,paths['target']))
    model_cal=startup(control);model_native=startup(native)
    need(model_cal['dgroup']==0x209e0 and model_native['dgroup']==0x209d0 and
         model_native['bss_start']-model_cal['bss_start']==DATA_DELTA and
         model_native['init_start']-model_cal['init_start']==DATA_DELTA,
         'independent original CRT DATA linker model differs')
    source=original_source_proof(base)
    obj=object_text(raw_obj)
    rows=[]
    for name,start,size in MEMBERS:
        a,b,unlinked,fixups=code_scope(obj,start,size)
        original=native.program_image[start:start+size]
        calibration=control.program_image[start:start+size]
        need(a==calibration and b==original,
             'source-linked full native SUPER CODE does not match: '+name)
        need(relative_fixups(control,start,size)==relative_fixups(native,start,size)==[],
             'original source-written near SUPER ASM has unexpected ordered MZ fixups')
        need(native.program_image.find(original)==start and
             native.program_image.find(original,start+1)<0,
             'complete original SUPER function is not unique')
        rows.append({'name':name,'start':start,'end':start+size,'size':size,
                     'source':source[name],'source_unlinked_CODE_sha256':unlinked,
                     'source_calibrated_CODE_sha256':sha(a),
                     'source_original_CODE_sha256':sha(b),
                     'ordered_MZ_fixups':[], 'original_OMF_actions':fixups,
                     'authored_credit':0})
    return {'schema_version':1,'kind':'original-master-super-code-source-OMF-rebind',
            'artifact':'th05-main','members':rows,
            'source_written_CODE_bytes':sum(x['size'] for x in rows),
            'source_assembler':'pinned TASM32 native calibration, one retained producer',
            'original_DGROUP':model_native['dgroup'],
            'calibration_DGROUP':model_cal['dgroup'],
            'original_BSS_init_delta':DATA_DELTA,
            'upstream_archive_sha256':paths['inner_archive']['sha256'],
            'saved_object_sha256':paths['saved_object']['sha256'],
            'calibration_exe_sha256':paths['calibration_exe']['sha256'],
            'original_target_sha256':paths['target']['sha256'],
            'parent_review_sha256':digest_file(BASE),
            'verifier_sha256':digest_file(ROOT/'scripts/review_master_super.py'),
            'author_credit':0,'other_source_bytes_claimed':0}


def validate_public(record):
    base=json.loads(BASE.read_text())
    need(record.get('schema_version')==1 and
         record.get('kind')=='original-master-super-code-source-OMF-rebind' and
         record.get('artifact')=='th05-main' and
         record.get('source_written_CODE_bytes')==sum(n for _,_,n in MEMBERS) and
         record.get('original_DGROUP')==0x209d0 and
         record.get('calibration_DGROUP')==0x209e0 and
         record.get('original_BSS_init_delta')==DATA_DELTA and
         record.get('upstream_archive_sha256')==base['inputs']['inner_archive']['sha256'] and
         record.get('saved_object_sha256')==base['inputs']['saved_object']['sha256'] and
         record.get('calibration_exe_sha256')==base['inputs']['calibration_exe']['sha256'] and
         record.get('original_target_sha256')==base['inputs']['target']['sha256'] and
         record.get('parent_review_sha256')==digest_file(BASE) and
         record.get('verifier_sha256')==digest_file(ROOT/'scripts/review_master_super.py') and
         record.get('author_credit')==record.get('other_source_bytes_claimed')==0,
         'original Master source scope or verifier identity changed')
    rows=record.get('members')
    need(isinstance(rows,list) and
         [(r.get('name'),r.get('start'),r.get('size')) for r in rows]==list(MEMBERS),
         'unknown or incomplete original SUPER source extent')
    for row in rows:
        need(row.get('end')==row['start']+row['size'] and
             row.get('authored_credit')==0 and row.get('ordered_MZ_fixups')==[] and
             isinstance(row.get('original_OMF_actions'),list) and
             row['original_OMF_actions'], 'unreviewed original source/relocations')
        for f in row['original_OMF_actions']:
            need(f.get('source_target_SEGDEF') in CALIBRATED_OFFSETS and
                 f.get('original_group_offset_delta') ==
                 (DATA_DELTA if f['source_target_SEGDEF'] in GROUP_TARGETS else 0) and
                 isinstance(f.get('site'),int) and 0<=f['site']<row['size']-1,
                 'unreviewed original OMF source fixup/target site')
        for key in ('source_unlinked_CODE_sha256','source_calibrated_CODE_sha256',
                    'source_original_CODE_sha256'):
            need(isinstance(row.get(key),str) and
                 re.fullmatch(r'[0-9a-f]{64}',row[key]),'original source digest invalid')
    if DECISION.exists():
        d=json.loads(DECISION.read_text())
        need(d.get('schema_version')==1 and d.get('artifact')=='th05-main' and
             d.get('decision')=='ADOPT_ONLY_COMPLETE_NATIVE_SUPER_CODE' and
             d.get('members')==[name for name,_,_ in MEMBERS] and
             d.get('evidence_sha256')==digest_file(PROOF) and
             d.get('code_bytes')==record['source_written_CODE_bytes'] and
             d.get('authored_credit')==d.get('other_source_bytes_claimed')==0,
             'original large Master CODE adoption differs from native source evidence')


def reviewed_claims(root,view,*,verify_targets=False):
    if not DECISION.exists():return [],None
    need(root.resolve()==ROOT.resolve(),'wrong original source checkout')
    proof=json.loads(PROOF.read_text())
    validate_public(proof)
    need(view['sha256']==json.loads(BASE.read_text())['target_payload_sha256'],
         'original MAIN SUPER CODE belongs to another payload')
    if verify_targets: need(replay()==proof,'actual source-linked original Master differs')
    return ([{'start':r['start'],'end':r['end'],
              'kind':'verified-vendor-code','library':'master.lib 0.23',
              'member':r['name'],'authored_credit':0} for r in proof['members']],
            digest_file(DECISION))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    mode=p.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write',action='store_true')
    mode.add_argument('--check',action='store_true')
    mode.add_argument('--structural-check',action='store_true')
    args=p.parse_args()
    if args.write:
        need(not PROOF.exists() and not DECISION.exists(),
             'cannot overwrite original reviewed source')
        r=replay()
        PROOF.write_text(json.dumps(r,indent=2)+'\n')
        print('PASS: exact native original Master SUPER source CODE',r['source_written_CODE_bytes'])
    else:
        r=json.loads(PROOF.read_text());validate_public(r)
        if args.check:
            need(replay()==r,'original source OMF/layout rebind disagrees')
            print('PASS: original source OMF, complete SUPER CODE and ordered fixups')
        else:print('PASS: original Master SUPER source proof current')


if __name__=='__main__':main()
