#!/usr/bin/env python3
"""Source-backed complete Master 0.23 GRCG geometry CODE in original MAIN.

The original author archive and the native TASM OMF are independent
provenance. Relink whole function CODE from LEDATA and actual ordered FIXUPP
through original C0L DGROUP; never copy observed target bytes into source.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

from lib.pc98 import parse_mz, digest_file
from lib.unit_oracle import relative_fixups
from review_master import object_text, source_blocks, stored_lzh, pinned, need, sha
from review_master_bgm import linked_scope
from review_main_runtime import startup

ROOT = Path(__file__).resolve().parents[1]
PROOF = ROOT / 'config/master_grcg_ownership.json'
DECISION = ROOT / 'config/reviewed_master_grcg.json'
BASE = ROOT / 'config/master_vendor_ownership.json'
MEMBERS = (
    ('BFNT_EXTEND_HEADER_ANALYSIS', 0x3f0, 96),
    ('cutline', 0x778, 116),
    ('GRCG_BOXFILL', 0xea6, 208),
    ('GRCG_BYTEBOXFILL_X', 0xf76, 152),
    ('GRCG_CIRCLE', 0x10ae, 152),
    ('GRC_SETCLIP', 0x130c, 146),
    ('GRC_CLIP_POLYGON_N', 0x139e, 754),
    ('GRCG_HLINE', 0x1690, 134),
    ('GRCG_LINE', 0x1716, 414),
    ('GRCG_POLYGON_CX', 0x18b4, 400),
    ('GRCG_PSET', 0x1a44, 68),
    ('GRCG_SETCOLOR', 0x1a88, 42),
    ('GRCG_VLINE', 0x1ab8, 134),
    ('GAIJI_PUTSA', 0x1dbe, 86),
    ('GRAPH_400LINE', 0x1e14, 78),
    ('GRAPH_EXTMODE', 0x1e86, 86),
    ('GRAPH_SCROLLUP', 0x1ee2, 88),
    ('IATAN2', 0x1f3a, 108),
    ('draw_trapezoidx', 0x1fac, 140),
    ('SUPER_LARGE_PUT', 0x2048, 148),
    ('PALETTE_SHOW', 0x2158, 266),
    ('TEXT_BOXFILLA', 0x24a8, 78),
    ('TEXT_PUTCA', 0x2540, 88),
)


def symbolic_source(raw):
    """Only contextual local-label namespace/comment/whitespace spelling."""
    content = raw.lower().replace('@@', '')
    content = content.replace('grcg_boxfill_return', 'return')
    # The circle's original self-modifying CODE words use local names.
    content = content.replace('gc_circl_vramzoom', '_vramzoom')
    content = content.replace('gc_circl_', '')
    # Display-facing Master ports only add namespaced self-modifying labels
    # or typed structure field names. The hardware operands stay unchanged.
    for old,new in (
        ('largeput_di_', '_di_'),('largeput_ch_', '_ch_'),
        ('largeput_', ''),('koizoidx_', ''),('palshow_', ''),
    ):
        content = content.replace(old,new)
    return [re.sub(r'\s+', '', line.split(';', 1)[0])
            for line in content.splitlines() if line.split(';', 1)[0].strip()]


def source_evidence(parent):
    upstream = stored_lzh(pinned(ROOT, parent['inputs']['inner_archive']))
    originals = {}
    for filename, raw in upstream.items():
        if not filename.upper().endswith('.ASM'):
            continue
        try:
            blocks = source_blocks(raw, 'cp932')
        except UnicodeDecodeError:
            continue
        for block in blocks:
            originals.setdefault(block['name'].casefold(), []).append((filename, block))
    inventory = {r['name']:r for r in parent['active_procedure_inventory']}
    frozen = {r['name']:r for r in parent['frozen_source_closure']}
    rows = {}
    for name, start, size in MEMBERS:
        active = inventory[name]
        need((active['start'], active['end']) == (start, start+size),
             'original active Master listing function extent changed')
        filename = active['source']
        need(filename in frozen, 'original GRCG source file absent from actual TASM OMF closure')
        source = (ROOT/parent['candidate_source_root']/filename).read_bytes()
        need(sha(source) == frozen[filename]['sha256'],
             'actual native-built Master source file changed')
        candidates = [b for b in source_blocks(source, 'utf8') if b['name'] == name]
        need(len(candidates) == 1, 'actual source procedure incomplete/duplicated')
        matching = [(f,b) for f,b in originals.get(name.casefold(), [])
                    if symbolic_source(candidates[0]['text']) == symbolic_source(b['text'])]
        need(len(matching) == 1,
             'original Master geometry instruction or operand mismatch: ' + name)
        vendor_file, vendor_block = matching[0]
        rows[name] = {
            'candidate_source': filename, 'source_file_sha256': sha(source),
            'original_archive_member': vendor_file,
            'original_source_block_sha256': sha(vendor_block['text'].encode('utf8')),
            'candidate_source_block_sha256': sha(candidates[0]['text'].encode('utf8')),
            'canonical_instruction_sha256': sha(
                '\n'.join(symbolic_source(vendor_block['text'])).encode('utf8')),
            'candidate_source_lines': [candidates[0]['start_line'],
                                       candidates[0]['end_line']],
        }
    return rows


def replay():
    parent = json.loads(BASE.read_text())
    real_obj = pinned(ROOT, parent['inputs']['saved_object'])
    need(real_obj == pinned(ROOT, parent['inputs']['calibration_object']),
         'actual assembly source and calibrated OMF differ')
    calibrated = parse_mz(pinned(ROOT, parent['inputs']['calibration_exe']))
    original = parse_mz(pinned(ROOT, parent['inputs']['target']))
    before, after = startup(calibrated), startup(original)
    need((before['dgroup'], after['dgroup'],
          after['init_start']-before['init_start'],
          after['bss_start']-before['bss_start']) ==
         (0x209e0, 0x209d0, -18, -18),
         'original CRT DATA/GROUP binding is not independently anchored')
    source = source_evidence(parent)
    obj = object_text(real_obj)
    rows = []
    for name, start, size in MEMBERS:
        cal, native, unlinked, mz, fixes = linked_scope(obj,start,size)
        observed = original.program_image[start:start+size]
        need(cal == calibrated.program_image[start:start+size] and native == observed,
             'original linked complete geometry CODE differs: ' + name)
        need(relative_fixups(calibrated,start,size) ==
             relative_fixups(original,start,size) == mz,
             'original ordered GRCG MZ relocations do not match source FIXUPP')
        need(original.program_image.find(observed) == start and
             original.program_image.find(observed,start+1) < 0,
             'complete original graphics CODE extent not uniquely located')
        rows.append({
            'member': name,'start':start,'end':start+size,'size':size,
            'source':source[name],'original_unlinked_CODE_sha256':unlinked,
            'source_calibrated_CODE_sha256':sha(cal),
            'source_original_CODE_sha256':sha(native),
            'ordered_original_MZ_relocations':mz,
            'ordered_OMF_actions':fixes,
            'authored_credit':0,
        })
    return {
        'schema_version':1,'kind':'original-Master-GRCG-native-source-and-MZ',
        'artifact':'th05-main','members':rows,
        'newly_verified_CODE_bytes':sum(r['size'] for r in rows),
        'original_target_sha256':parent['inputs']['target']['sha256'],
        'source_OMF_sha256':parent['inputs']['saved_object']['sha256'],
        'calibration_exe_sha256':parent['inputs']['calibration_exe']['sha256'],
        'author_source_archive_sha256':parent['inputs']['inner_archive']['sha256'],
        'parent_Master_sha256':digest_file(BASE),
        'source_link_verifier_sha256':digest_file(ROOT/'scripts/review_master_bgm.py'),
        'verifier_sha256':digest_file(ROOT/'scripts/review_master_grcg.py'),
        'authored_credit':0,'non_CODE_bytes_claimed':0,
    }


def validate_public(proof):
    parent = json.loads(BASE.read_text())
    need(proof.get('schema_version')==1 and
         proof.get('kind')=='original-Master-GRCG-native-source-and-MZ' and
         proof.get('artifact')=='th05-main' and
         proof.get('newly_verified_CODE_bytes')==sum(n for _,_,n in MEMBERS) and
         proof.get('original_target_sha256')==parent['inputs']['target']['sha256'] and
         proof.get('source_OMF_sha256')==parent['inputs']['saved_object']['sha256'] and
         proof.get('calibration_exe_sha256')==parent['inputs']['calibration_exe']['sha256'] and
         proof.get('author_source_archive_sha256')==parent['inputs']['inner_archive']['sha256'] and
         proof.get('parent_Master_sha256')==digest_file(BASE) and
         proof.get('source_link_verifier_sha256')==
         digest_file(ROOT/'scripts/review_master_bgm.py') and
         proof.get('verifier_sha256')==digest_file(ROOT/'scripts/review_master_grcg.py') and
         proof.get('authored_credit')==proof.get('non_CODE_bytes_claimed')==0,
         'original GRCG source or native verifier identity changed')
    rows = proof.get('members',[])
    need([(x.get('member'),x.get('start'),x.get('size')) for x in rows] ==
         list(MEMBERS), 'GRCG source scopes missing/reordered')
    for row in rows:
        need(row.get('end')==row['start']+row['size'] and
             row.get('authored_credit')==0 and
             isinstance(row.get('ordered_OMF_actions'),list) and
             row.get('ordered_original_MZ_relocations')==
             [f['source_site'] for f in row['ordered_OMF_actions']
              if f['original_link_operation']=='original-MZ-segment16'],
             'original complete CODE or ordered OMF evidence missing')
        for field in ('original_unlinked_CODE_sha256','source_calibrated_CODE_sha256',
                      'source_original_CODE_sha256'):
            h=row.get(field)
            need(isinstance(h,str) and re.fullmatch('[0-9a-f]{64}',h),
                 'original GRCG CODE source digest invalid')
    if DECISION.exists():
        adopted=json.loads(DECISION.read_text())
        need(adopted.get('schema_version')==1 and
             adopted.get('artifact')=='th05-main' and
             adopted.get('decision')=='ADOPT_ONLY_ORIGINAL_COMPLETE_GRCG_CODE' and
             adopted.get('members')==[name for name,_,_ in MEMBERS] and
             adopted.get('evidence_sha256')==digest_file(PROOF) and
             adopted.get('CODE_bytes')==proof['newly_verified_CODE_bytes'] and
             adopted.get('authored_credit')==adopted.get('other_bytes_claimed')==0,
             'source-reviewed original GRCG adoption absent or stale')


def reviewed_claims(root,view,*,verify_targets=False):
    if not DECISION.exists():
        return [],None
    need(root.resolve()==ROOT.resolve(),'wrong original reconstruction checkout')
    proof=json.loads(PROOF.read_text())
    validate_public(proof)
    need(view['sha256']==json.loads(BASE.read_text())['target_payload_sha256'],
         'original MAIN GRCG review belongs to a different binary')
    if verify_targets:
        need(replay()==proof,'actual original source-linked GRCG differs')
    return ([{'start':r['start'],'end':r['end'],'kind':'verified-vendor-code',
              'library':'master.lib 0.23','member':r['member'],'authored_credit':0}
             for r in proof['members']],digest_file(DECISION))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write',action='store_true')
    mode.add_argument('--check',action='store_true')
    mode.add_argument('--structural-check',action='store_true')
    args=parser.parse_args()
    if args.write:
        need(not PROOF.exists() and not DECISION.exists(),
             'cannot overwrite reviewed original Master source')
        proof=replay();PROOF.write_text(json.dumps(proof,indent=2)+'\n')
        print('PASS: original complete Master geometry CODE:',
              proof['newly_verified_CODE_bytes'])
    else:
        proof=json.loads(PROOF.read_text());validate_public(proof)
        if args.check:
            need(replay()==proof,'original source-linked native GRCG differs')
            print('PASS: original Master GRCG native CODE and ordered fixups')
        else:
            print('PASS: public GRCG original source-current proof')


if __name__=='__main__':
    main()
