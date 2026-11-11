#!/usr/bin/env python3
"""Recover complete original Master 0.23 file, DOS, and heap CODE in MAIN.

Original author assembly is checked against the actual native TASM
translation unit. Genuine OMF LEDATA/FIXUPP reconstruct the complete
calibration and original code scopes; no executable bytes are copied into
source. This is third-party ASM ownership, not game-authored C++.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

from lib.pc98 import parse_mz, digest_file
from lib.unit_oracle import relative_fixups
from review_master import object_text, source_blocks, stored_lzh, pinned, need, sha
from review_main_runtime import startup
from review_master_bgm import linked_scope

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'config/master_vendor_ownership.json'
PROOF=ROOT/'config/master_io_ownership.json'
DECISION=ROOT/'config/reviewed_master_io.json'
MEMBERS=(
 ('BFNT_HEADER_READ',0x03b4,60),('BFILL',0x0554,60),
 ('BGETC',0x05d0,48),('BSEEK',0x0706,66),('BSEEK_',0x0748,48),
 ('DOS_READ',0x07f2,26),('DOS_SEEK',0x080c,28),
 ('DOS_SETVECT',0x0828,32),
 ('FILE_FLUSH',0x0cc2,108),('FILE_CLOSE',0x0d2e,16),
 ('FILE_READ',0x0d3e,180),('FILE_SEEK',0x0e2e,52),
 ('FILE_TELL',0x0e62,14),('FONTFILE_CLOSE',0x0e70,22),
 ('FONTFILE_OPEN',0x0e86,26),
 ('PFGETC1',0x228c,78),('PFGETX0',0x22da,68),
 ('PFREAD',0x232c,46),('PFREWIND',0x235a,60),
 ('PFSEEK',0x2396,48),
 ('SMEM_RELEASE',0x2432,16),('SMEM_WGET',0x2448,54),
 ('MEM_ASSIGN_DOS',0x27aa,34),('MEM_ASSIGN',0x27cc,38),
 ('MEM_ASSIGN_ALL',0x27f2,40),
 ('HMEM_ALLOC',0x282e,240),('HMEM_FREE',0x291e,168),
 ('SUPER_FREE',0x29ea,48),
)


def semantic_lines(body,name):
    # First-party port uses the named type "memhead" where the original
    # Master memory manager uses the same zero-offset structure directly.
    if name in ('HMEM_ALLOC','HMEM_FREE'):
        body=body.lower().replace('memhead.','')
        body=re.sub(r'es:\[0\]\.(nextseg|using|mem_id)',
                    lambda match:'es:['+match[1]+']',body)
    body=body.lower().replace('@@','')
    return [re.sub(r'\s+','',line.split(';',1)[0])
            for line in body.splitlines() if line.split(';',1)[0].strip()]


def source_evidence(parent):
    archive=stored_lzh(pinned(ROOT,parent['inputs']['inner_archive']))
    original={}
    for file,raw in archive.items():
        if not file.upper().endswith('.ASM'):continue
        try:sections=source_blocks(raw,'cp932')
        except UnicodeDecodeError:continue
        for block in sections:
            original.setdefault(block['name'].casefold(),[]).append((file,block))
    active={row['name']:row for row in parent['active_procedure_inventory']}
    frozen={row['name']:row for row in parent['frozen_source_closure']}
    proof={}
    for name,start,size in MEMBERS:
        row=active[name]
        need((row['start'],row['end'])==(start,start+size),
             'original active file/heap procedure boundary changed')
        file=row['source']
        need(file in frozen,'source file not part of authentic TASM object')
        content=(ROOT/parent['candidate_source_root']/file).read_bytes()
        need(sha(content)==frozen[file]['sha256'],
             'native-compiled file/heap source not pinned')
        candidates=[block for block in source_blocks(content,'utf8')
                    if block['name']==name]
        need(len(candidates)==1,'actual source procedure duplicated/incomplete')
        matches=[(file0,src) for file0,src in original.get(name.casefold(),[])
                 if semantic_lines(src['text'],name)==semantic_lines(candidates[0]['text'],name)]
        need(len(matches)==1,'author Master file/heap instruction identity differs: '+name)
        original_file,upstream=matches[0]
        proof[name]={'upstream_member':original_file,
                     'original_block_sha256':sha(upstream['text'].encode('utf8')),
                     'candidate_source':file,'candidate_file_sha256':sha(content),
                     'candidate_block_sha256':sha(candidates[0]['text'].encode('utf8')),
                     'normalized_source_sha256':sha(
                        '\n'.join(semantic_lines(upstream['text'],name)).encode('utf8')),
                     'candidate_lines':[candidates[0]['start_line'],candidates[0]['end_line']]}
    return proof


def replay():
    parent=json.loads(BASE.read_text())
    obj=pinned(ROOT,parent['inputs']['saved_object'])
    need(obj==pinned(ROOT,parent['inputs']['calibration_object']),
         'real original TASM source CODE and calibrated OMF differ')
    target=parse_mz(pinned(ROOT,parent['inputs']['target']))
    calibrated=parse_mz(pinned(ROOT,parent['inputs']['calibration_exe']))
    before=startup(calibrated);after=startup(target)
    need((before['dgroup'],after['dgroup'],
          after['init_start']-before['init_start'],
          after['bss_start']-before['bss_start']) ==
         (0x209e0,0x209d0,-18,-18),
         'original linker DATA/BSS offsets lack native CRT support')
    sources=source_evidence(parent)
    omf=object_text(obj)
    contributions=[]
    for name,start,size in MEMBERS:
        cal,orig,unlinked,mz,actions=linked_scope(omf,start,size)
        need(cal==calibrated.program_image[start:start+size] and
             orig==target.program_image[start:start+size],
             'original Master source-linked full CODE bytes disagree: '+name)
        need(relative_fixups(calibrated,start,size)==
             relative_fixups(target,start,size)==mz,
             'original ordered CODE/MZ fixups differ: '+name)
        contributions.append({'member':name,'start':start,'end':start+size,'size':size,
                              'source':sources[name],
                              'object_source_CODE_sha256':unlinked,
                              'calibration_linked_CODE_sha256':sha(cal),
                              'original_linked_CODE_sha256':sha(orig),
                              'original_ordered_MZ_relocations':mz,
                              'original_OMF_actions':actions,'authored_credit':0})
    return {'schema_version':1,'kind':'original-master-file-heap-source-CODE',
            'artifact':'th05-main','members':contributions,
            'source_written_CODE_bytes':sum(r['size'] for r in contributions),
            'original_target_sha256':parent['inputs']['target']['sha256'],
            'calibration_exe_sha256':parent['inputs']['calibration_exe']['sha256'],
            'saved_source_OMF_sha256':parent['inputs']['saved_object']['sha256'],
            'original_archive_sha256':parent['inputs']['inner_archive']['sha256'],
            'parent_Master_sha256':digest_file(BASE),
            'linked_source_verifier_sha256':digest_file(ROOT/'scripts/review_master_bgm.py'),
            'verifier_sha256':digest_file(ROOT/'scripts/review_master_io.py'),
            'authored_credit':0,'non_CODE_bytes_claimed':0}


def validate_public(record):
    parent=json.loads(BASE.read_text())
    need(record.get('schema_version')==1 and
         record.get('kind')=='original-master-file-heap-source-CODE' and
         record.get('artifact')=='th05-main' and
         record.get('source_written_CODE_bytes')==sum(size for _,_,size in MEMBERS) and
         record.get('original_target_sha256')==parent['inputs']['target']['sha256'] and
         record.get('calibration_exe_sha256')==parent['inputs']['calibration_exe']['sha256'] and
         record.get('saved_source_OMF_sha256')==parent['inputs']['saved_object']['sha256'] and
         record.get('original_archive_sha256')==parent['inputs']['inner_archive']['sha256'] and
         record.get('parent_Master_sha256')==digest_file(BASE) and
         record.get('linked_source_verifier_sha256')==digest_file(ROOT/'scripts/review_master_bgm.py') and
         record.get('verifier_sha256')==digest_file(ROOT/'scripts/review_master_io.py') and
         record.get('authored_credit')==record.get('non_CODE_bytes_claimed')==0,
         'original Master input/source review changed')
    rows=record.get('members',[])
    need([(r.get('member'),r.get('start'),r.get('size')) for r in rows]==list(MEMBERS),
         'source contribution is not a reviewed complete Master function')
    for row in rows:
        need(row.get('end')==row['start']+row['size'] and
             row.get('authored_credit')==0 and
             isinstance(row.get('original_OMF_actions'),list) and
             row.get('original_ordered_MZ_relocations')==
             [f['source_site'] for f in row['original_OMF_actions']
              if f['original_link_operation']=='original-MZ-segment16'],
             'incomplete CODE/OMF/MZ proof')
        for key in ('object_source_CODE_sha256','calibration_linked_CODE_sha256',
                    'original_linked_CODE_sha256'):
            value=row.get(key)
            need(isinstance(value,str) and re.fullmatch('[0-9a-f]{64}',value),
                 'source-linked original bytes lack digest')
    if DECISION.exists():
        d=json.loads(DECISION.read_text())
        need(d.get('schema_version')==1 and d.get('artifact')=='th05-main' and
             d.get('decision')=='ADOPT_ONLY_ORIGINAL_MASTER_FILE_HEAP_CODE' and
             d.get('evidence_sha256')==digest_file(PROOF) and
             d.get('members')==[name for name,_,_ in MEMBERS] and
             d.get('CODE_bytes')==record['source_written_CODE_bytes'] and
             d.get('authored_credit')==d.get('non_CODE_bytes_claimed')==0,
             'explicit original Master review selection differs')


def reviewed_claims(root,view,*,verify_targets=False):
    if not DECISION.exists():return [],None
    need(root.resolve()==ROOT.resolve(),'wrong native reconstruction checkout')
    record=json.loads(PROOF.read_text());validate_public(record)
    need(view['sha256']==json.loads(BASE.read_text())['target_payload_sha256'],
         'original source CODE target differs')
    if verify_targets:need(replay()==record,'genuine original Master OMF source replay changed')
    return ([{'start':r['start'],'end':r['end'],'kind':'verified-vendor-code',
              'library':'master.lib 0.23','member':r['member'],'authored_credit':0}
             for r in record['members']],digest_file(DECISION))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    mode=p.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write',action='store_true')
    mode.add_argument('--check',action='store_true')
    mode.add_argument('--structural-check',action='store_true')
    args=p.parse_args()
    if args.write:
        need(not PROOF.exists() and not DECISION.exists(),
             'refusing to overwrite native original Master source evidence')
        record=replay();PROOF.write_text(json.dumps(record,indent=2)+'\n')
        print('PASS: source-exact original file/heap CODE',record['source_written_CODE_bytes'])
    else:
        record=json.loads(PROOF.read_text());validate_public(record)
        if args.check:
            need(replay()==record,'actual original source CODE/OMF/MZ differs')
            print('PASS: source-exact Master file/heap OMF CODE and native relocations')
        else:
            print('PASS: structural original Master file/heap CODE proof')


if __name__=='__main__':main()
