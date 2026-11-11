#!/usr/bin/env python3
"""Seventeen complete, previously unknown source-backed Master functions.

The original Master 0.23 archive, unchanged native TASM OMF and real MAIN MZ
must all agree. Accept only explicitly named full procedures, never nearby
alignment or game-authored bytes.
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
BASE = ROOT / 'config/master_vendor_ownership.json'
PROOF = ROOT / 'config/master_gap_functions_ownership.json'
DECISION = ROOT / 'config/reviewed_master_gap_functions.json'
# Original listing boundaries, not discovered from matching target bytes.
MEMBERS = (
    ('rtc_int_set',       0x0454, 145),
    ('RTC_INT',           0x04f8, 68),
    ('BFNT_PALETTE_SET',  0x0590, 64),
    ('GAIJI_PUTCA',      0x1d7a, 68),
    ('GRAPH_CLEAR',      0x1e62, 36),
    ('IRAND',            0x23c6, 42),
    ('TEXT_FILLCA',      0x2508, 56),
    ('TEXT_PUTSA',       0x2598, 114),
    ('VSYNC_START',      0x260e, 106),
    ('VSYNC_COUNT',      0x2682, 58),
    ('VSYNC_END',        0x26bc, 72),
    ('VSYNC_WAIT',       0x2704, 38),
    ('PALETTE_WHITE_IN', 0x272a, 64),
    ('PALETTE_WHITE_OUT',0x276a, 64),
    ('EMS_EXIST',        0x4000, 34),
    ('EMS_SETNAME',      0x4052, 26),
    ('EMS_SPACE',        0x40ce, 24),
)


def source_spelling(raw):
    """Only equivalent Master macro, typed-offset and private-label spellings.

    ReC98's NOPCALL explicitly expresses TLINK's original near-FAR call
    relaxation. The other substitutions name the same I/O ports, fields and
    local branch destinations as the author's original assembler source.
    """
    content = raw.lower().replace('@@', '').replace('nopcall', 'call')
    for before, after in (
        ('rtc_timerorg', 'timerorg'), ('rtc_imr', 'imr'),
        ('vsync_imr', 'imr'),
        ('vsync_leavelabel proc', 'vsync_leavelabel callmodel'),
        ('bfnt_header.col', 'col'),
        ('skipslot11', 'skipslot1'),
    ):
        content = content.replace(before, after)
    lines = [re.sub(r'\s+', '', line.split(';', 1)[0])
             for line in content.splitlines() if line.split(';', 1)[0].strip()]
    return [line.replace('pushwordptr[bp+atrb]', 'push[bp+atrb]')
                .replace('vsync_leavelabelproc', 'vsync_leavelabelcallmodel')
            for line in lines]


def replay():
    parent = json.loads(BASE.read_text())
    frozen = {row['name']: row for row in parent['frozen_source_closure']}
    inventory = {row['name']: row for row in parent['active_procedure_inventory']}
    author_archive = stored_lzh(pinned(ROOT, parent['inputs']['inner_archive']))
    author = {}
    for filename, raw in author_archive.items():
        if not filename.upper().endswith('.ASM'):
            continue
        try:
            blocks = source_blocks(raw, 'cp932')
        except UnicodeDecodeError:
            continue
        for item in blocks:
            author.setdefault(item['name'].casefold(), []).append((filename, item))
    real_obj = pinned(ROOT, parent['inputs']['saved_object'])
    need(real_obj == pinned(ROOT, parent['inputs']['calibration_object']),
         'actual native source object differs from calibration')
    obj = object_text(real_obj)
    cal = parse_mz(pinned(ROOT, parent['inputs']['calibration_exe']))
    native = parse_mz(pinned(ROOT, parent['inputs']['target']))
    before, after = startup(cal), startup(native)
    need((before['dgroup'], after['dgroup'],
          after['init_start']-before['init_start']) == (0x209e0, 0x209d0, -18),
         'original Master native CRT/DGROUP frames not independently anchored')
    rows = []
    source_cache = {}
    for member, start, size in MEMBERS:
        listing = inventory[member]
        need((listing['start'], listing['end']) == (start, start + size),
             'original Master function listing boundary changed: ' + member)
        filename = listing['source']
        need(filename in frozen, 'actual TASM source file missing')
        if filename not in source_cache:
            content = (ROOT / parent['candidate_source_root'] / filename).read_bytes()
            need(sha(content) == frozen[filename]['sha256'],
                 'actual native Master producer source changed')
            source_cache[filename] = (sha(content), source_blocks(content, 'utf8'))
        source_hash, blocks = source_cache[filename]
        same = [b for b in blocks if b['name'] == member]
        need(len(same) == 1, 'whole original procedure absent/ambiguous: ' + member)
        canonical = source_spelling(same[0]['text'])
        matches = [(fn, block) for fn, block in author.get(member.casefold(), [])
                   if source_spelling(block['text']) == canonical]
        need(len(matches) == 1, 'original author source differs from native routine: ' + member)
        original_filename, original_block = matches[0]
        control, linked, unlinked_hash, mz, actions = linked_scope(obj, start, size)
        observed = native.program_image[start:start+size]
        need(control == cal.program_image[start:start+size] and linked == observed,
             'complete original Master code differs from compiled source: ' + member)
        need(relative_fixups(cal, start, size) ==
             relative_fixups(native, start, size) == mz,
             'ordered original MZ relocations differ: ' + member)
        need(native.program_image.find(observed) == start and
             native.program_image.find(observed, start+1) < 0,
             'complete Master CODE extent not uniquely located: ' + member)
        rows.append({
            'member': member, 'start': start, 'end': start + size, 'size': size,
            'candidate_source': filename, 'source_file_sha256': source_hash,
            'original_archive_member': original_filename,
            'original_block_sha256': sha(original_block['text'].encode('utf8')),
            'candidate_block_sha256': sha(same[0]['text'].encode('utf8')),
            'canonical_source_sha256': sha('\n'.join(canonical).encode('utf8')),
            'source_unlinked_CODE_sha256': unlinked_hash,
            'calibrated_CODE_sha256': sha(control),
            'original_CODE_sha256': sha(linked),
            'ordered_original_MZ_relocations': mz,
            'ordered_OMF_actions': actions, 'authored_credit': 0,
        })
    return {
        'schema_version': 1, 'kind': 'original-master-gap-functions-source-and-MZ',
        'artifact': 'th05-main', 'members': rows,
        'CODE_bytes': sum(n for _, _, n in MEMBERS),
        'original_target_sha256': parent['inputs']['target']['sha256'],
        'source_OMF_sha256': parent['inputs']['saved_object']['sha256'],
        'calibration_exe_sha256': parent['inputs']['calibration_exe']['sha256'],
        'author_archive_sha256': parent['inputs']['inner_archive']['sha256'],
        'parent_master_sha256': digest_file(BASE),
        'verifier_sha256': digest_file(ROOT / 'scripts/review_master_gap_functions.py'),
        'authored_credit': 0, 'other_bytes_claimed': 0,
    }


def validate_public(proof):
    parent = json.loads(BASE.read_text())
    need(proof.get('schema_version') == 1 and
         proof.get('kind') == 'original-master-gap-functions-source-and-MZ' and
         proof.get('artifact') == 'th05-main' and
         proof.get('CODE_bytes') == sum(n for _, _, n in MEMBERS) and
         proof.get('authored_credit') == proof.get('other_bytes_claimed') == 0 and
         proof.get('original_target_sha256') == parent['inputs']['target']['sha256'] and
         proof.get('source_OMF_sha256') == parent['inputs']['saved_object']['sha256'] and
         proof.get('calibration_exe_sha256') == parent['inputs']['calibration_exe']['sha256'] and
         proof.get('author_archive_sha256') == parent['inputs']['inner_archive']['sha256'] and
         proof.get('parent_master_sha256') == digest_file(BASE) and
         proof.get('verifier_sha256') == digest_file(ROOT / 'scripts/review_master_gap_functions.py'),
         'Master source/binary provenance changed')
    rows = proof.get('members', [])
    need([(r.get('member'), r.get('start'), r.get('size')) for r in rows] == list(MEMBERS),
         'complete Master source function list changed')
    for row in rows:
        need(row.get('end') == row['start'] + row['size'] and
             row.get('authored_credit') == 0 and
             isinstance(row.get('ordered_OMF_actions'), list) and
             row.get('ordered_original_MZ_relocations') ==
             [f['source_site'] for f in row['ordered_OMF_actions']
              if f['original_link_operation'] == 'original-MZ-segment16'],
             'incomplete CODE extent or ordered relocation record')
        for field in ('source_file_sha256', 'original_block_sha256',
                      'candidate_block_sha256', 'canonical_source_sha256',
                      'source_unlinked_CODE_sha256', 'calibrated_CODE_sha256',
                      'original_CODE_sha256'):
            need(isinstance(row.get(field), str) and re.fullmatch('[0-9a-f]{64}', row[field]),
                 'original Master source/CODE evidence missing')
    if DECISION.exists():
        adopted = json.loads(DECISION.read_text())
        need(adopted.get('schema_version') == 1 and adopted.get('artifact') == 'th05-main' and
             adopted.get('decision') == 'ADOPT_ONLY_COMPLETE_ORIGINAL_MASTER_GAP_FUNCTIONS' and
             adopted.get('evidence_sha256') == digest_file(PROOF) and
             adopted.get('members') == [name for name, _, _ in MEMBERS] and
             adopted.get('CODE_bytes') == proof['CODE_bytes'] and
             adopted.get('authored_credit') == adopted.get('other_bytes_claimed') == 0,
             'original Master source decision missing or stale')


def reviewed_claims(root, view, *, verify_targets=False):
    if not DECISION.exists():
        return [], None
    need(root.resolve() == ROOT.resolve(), 'wrong reconstruction checkout')
    proof = json.loads(PROOF.read_text())
    validate_public(proof)
    need(view['sha256'] == json.loads(BASE.read_text())['target_payload_sha256'],
         'Master native source target identity changed')
    if verify_targets:
        need(replay() == proof, 'native original Master complete CODE no longer matches')
    return ([{'start': row['start'], 'end': row['end'], 'kind': 'verified-vendor-code',
              'library': 'master.lib 0.23', 'member': row['member'], 'authored_credit': 0}
             for row in proof['members']], digest_file(DECISION))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--write', action='store_true')
    group.add_argument('--check', action='store_true')
    group.add_argument('--structural-check', action='store_true')
    args = parser.parse_args()
    if args.write:
        need(not PROOF.exists() and not DECISION.exists(),
             'cannot overwrite accepted Master evidence')
        proof = replay()
        PROOF.write_text(json.dumps(proof, indent=2) + '\n')
        print('PASS original source-backed Master CODE', proof['CODE_bytes'])
    else:
        proof = json.loads(PROOF.read_text())
        validate_public(proof)
        if args.check:
            need(replay() == proof, 'original native Master byte comparison changed')
            print('PASS Master original gap functions: complete raw CODE and fixups')
        else:
            print('PASS Master gap functions public evidence')


if __name__ == '__main__':
    main()
