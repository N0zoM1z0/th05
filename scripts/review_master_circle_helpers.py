#!/usr/bin/env python3
"""Three complete Master circle helper procedures in original TH05 MAIN.

Use the author's GC_CIRCL.ASM, the saved real TASM object and original ordered
OMF fixups. The trailing 121B alignment byte is deliberately not a procedure.
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
from review_master_grcg import symbolic_source
from review_main_runtime import startup

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'config/master_vendor_ownership.json'
PROOF = ROOT / 'config/master_circle_helpers_ownership.json'
DECISION = ROOT / 'config/reviewed_master_circle_helpers.json'
SOURCE = 'libs/master.lib/grcg_circle.asm'
MEMBERS = (
    # Native source label, original author source label, start, complete size.
    ('GC_CIRCL_ALLIN', 'ALLIN', 0x10a4, 10),
    ('GC_CIRCL_PSET4Q', 'PSET4Q', 0x1146, 2),
    ('GC_CIRCL_PSET4', 'PSET4', 0x1148, 211),
)


def replay():
    parent = json.loads(BASE.read_text())
    original_source = stored_lzh(pinned(ROOT, parent['inputs']['inner_archive']))['GC_CIRCL.ASM']
    candidate_file = ROOT / parent['candidate_source_root'] / SOURCE
    candidate = candidate_file.read_bytes()
    pinned_sources = {x['name']: x for x in parent['frozen_source_closure']}
    need(sha(candidate) == pinned_sources[SOURCE]['sha256'],
         'native circle source differs from the actual TASM producer')
    author_blocks = {b['name']: b for b in source_blocks(original_source, 'cp932')}
    candidate_blocks = {b['name']: b for b in source_blocks(candidate, 'utf8')}
    listing = {row['name']: row for row in parent['active_procedure_inventory']}
    # The three helpers live in one already confirmed original module, with
    # GRCG_CIRCLE between ALLIN and PSET4Q and GRCG_CIRCLE_X immediately after.
    for name, start, end in [('GRCG_CIRCLE', 0x10ae, 0x1146),
                             ('GRCG_CIRCLE_X', 0x121c, 0x130c)]:
        need((listing[name]['start'], listing[name]['end']) == (start, end),
             'surrounding original circle function boundary changed')
    real_obj = pinned(ROOT, parent['inputs']['saved_object'])
    need(real_obj == pinned(ROOT, parent['inputs']['calibration_object']),
         'saved source-linked circle OMF differs from calibration')
    obj = object_text(real_obj)
    control = parse_mz(pinned(ROOT, parent['inputs']['calibration_exe']))
    original = parse_mz(pinned(ROOT, parent['inputs']['target']))
    before, after = startup(control), startup(original)
    need((before['dgroup'], after['dgroup'],
          after['init_start'] - before['init_start']) == (0x209e0, 0x209d0, -18),
         'original circle DATA/CRT frame not independently anchored')
    rows = []
    for name, author_name, start, size in MEMBERS:
        scope = listing[name]
        need((scope['start'], scope['end'], scope['source']) ==
             (start, start + size, SOURCE), 'original helper source procedure boundary changed')
        authored = author_blocks[author_name]
        maintained = candidate_blocks[name]
        need(symbolic_source(authored['text']) == symbolic_source(maintained['text']),
             'original Master helper changed an instruction or operand: ' + name)
        cal, native, unlinked, mz, actions = linked_scope(obj, start, size)
        observed = original.program_image[start:start + size]
        need(cal == control.program_image[start:start + size] and native == observed,
             'native complete circle helper CODE differs: ' + name)
        need(relative_fixups(control, start, size) ==
             relative_fixups(original, start, size) == mz,
             'circle helper original ordered relocations differ')
        if size > 10:
            need(original.program_image.find(observed) == start and
                 original.program_image.find(observed, start + 1) < 0,
                 'full helper CODE is not uniquely located')
        rows.append({
            'member': name, 'author_source_label': author_name,
            'start': start, 'end': start + size, 'size': size,
            'source': SOURCE, 'author_block_sha256': sha(authored['text'].encode('utf8')),
            'candidate_block_sha256': sha(maintained['text'].encode('utf8')),
            'canonical_source_sha256': sha('\n'.join(symbolic_source(authored['text'])).encode('utf8')),
            'source_unlinked_CODE_sha256': unlinked,
            'native_CODE_sha256': sha(native), 'calibration_CODE_sha256': sha(cal),
            'ordered_original_MZ_relocations': mz, 'ordered_OMF_actions': actions,
            'authored_credit': 0,
        })
    # At 121B, the saved calibration has EVEN/NOP (90), while the original
    # has zero. This byte is neither part of PSET4's RET nor owned by us.
    boundary = 0x121b
    need(control.program_image[boundary] == 0x90 and
         original.program_image[boundary] == 0 and
         listing['GC_CIRCL_PSET4']['end'] == boundary and
         listing['GRCG_CIRCLE_X']['start'] == boundary + 1,
         'circle helper has an unreviewed final alignment byte')
    return {
        'schema_version': 1, 'kind': 'original-master-circle-helper-source-and-MZ',
        'artifact': 'th05-main', 'members': rows,
        'CODE_bytes': sum(n for _, _, _, n in MEMBERS),
        'excluded_alignment_offset': boundary,
        'original_target_sha256': parent['inputs']['target']['sha256'],
        'calibration_exe_sha256': parent['inputs']['calibration_exe']['sha256'],
        'source_OMF_sha256': parent['inputs']['saved_object']['sha256'],
        'author_archive_sha256': parent['inputs']['inner_archive']['sha256'],
        'circle_source_sha256': sha(candidate),
        'parent_master_sha256': digest_file(BASE),
        'verifier_sha256': digest_file(ROOT / 'scripts/review_master_circle_helpers.py'),
        'authored_credit': 0,
    }


def validate_public(proof):
    parent = json.loads(BASE.read_text())
    need(proof.get('schema_version') == 1 and
         proof.get('kind') == 'original-master-circle-helper-source-and-MZ' and
         proof.get('artifact') == 'th05-main' and
         proof.get('CODE_bytes') == sum(n for _, _, _, n in MEMBERS) and
         proof.get('excluded_alignment_offset') == 0x121b and
         proof.get('authored_credit') == 0 and
         proof.get('original_target_sha256') == parent['inputs']['target']['sha256'] and
         proof.get('calibration_exe_sha256') == parent['inputs']['calibration_exe']['sha256'] and
         proof.get('source_OMF_sha256') == parent['inputs']['saved_object']['sha256'] and
         proof.get('author_archive_sha256') == parent['inputs']['inner_archive']['sha256'] and
         proof.get('parent_master_sha256') == digest_file(BASE) and
         proof.get('verifier_sha256') == digest_file(ROOT / 'scripts/review_master_circle_helpers.py'),
         'circle helper evidence/target/source verifier identity changed')
    rows = proof.get('members', [])
    need([(r.get('member'), r.get('author_source_label'), r.get('start'), r.get('size'))
          for r in rows] == list(MEMBERS), 'circle source helper boundaries missing/reordered')
    for row in rows:
        need(row.get('end') == row['start'] + row['size'] and
             row.get('source') == SOURCE and row.get('authored_credit') == 0 and
             row.get('ordered_original_MZ_relocations') ==
             [f['source_site'] for f in row['ordered_OMF_actions']
              if f['original_link_operation'] == 'original-MZ-segment16'],
             'incomplete helper source extent or ordered fixup record')
        for k in ('author_block_sha256', 'candidate_block_sha256', 'canonical_source_sha256',
                  'source_unlinked_CODE_sha256', 'native_CODE_sha256', 'calibration_CODE_sha256'):
            need(isinstance(row.get(k), str) and re.fullmatch('[0-9a-f]{64}', row[k]),
                 'circle source evidence digest missing')
    if DECISION.exists():
        adopted = json.loads(DECISION.read_text())
        need(adopted.get('schema_version') == 1 and
             adopted.get('artifact') == 'th05-main' and
             adopted.get('decision') == 'ADOPT_ONLY_THREE_COMPLETE_CIRCLE_HELPERS' and
             adopted.get('members') == [name for name, _, _, _ in MEMBERS] and
             adopted.get('evidence_sha256') == digest_file(PROOF) and
             adopted.get('CODE_bytes') == proof['CODE_bytes'] and
             adopted.get('excluded_alignment_offset') == 0x121b and
             adopted.get('authored_credit') == 0,
             'circle source helper adoption is absent or stale')


def reviewed_claims(root, view, *, verify_targets=False):
    if not DECISION.exists():
        return [], None
    need(root.resolve() == ROOT.resolve(), 'wrong original reconstruction checkout')
    proof = json.loads(PROOF.read_text())
    validate_public(proof)
    need(view['sha256'] == json.loads(BASE.read_text())['target_payload_sha256'],
         'original circle helper target differs')
    if verify_targets:
        need(replay() == proof, 'original native source-linked circle helper differs')
    return ([{'start': r['start'], 'end': r['end'], 'kind': 'verified-vendor-code',
              'library': 'master.lib 0.23', 'member': r['member'], 'authored_credit': 0}
             for r in proof['members']], digest_file(DECISION))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--write', action='store_true')
    group.add_argument('--check', action='store_true')
    group.add_argument('--structural-check', action='store_true')
    args = parser.parse_args()
    if args.write:
        need(not PROOF.exists() and not DECISION.exists(), 'cannot overwrite reviewed circle evidence')
        proof = replay()
        PROOF.write_text(json.dumps(proof, indent=2) + '\n')
        print('PASS original Master circle helper CODE', proof['CODE_bytes'])
    else:
        proof = json.loads(PROOF.read_text())
        validate_public(proof)
        if args.check:
            need(replay() == proof, 'source-linked circle helper complete bytes differ')
            print('PASS Master circle helpers: complete bytes and ordered fixups')
        else:
            print('PASS circle helper public evidence')


if __name__ == '__main__':
    main()
