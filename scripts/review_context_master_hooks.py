#!/usr/bin/env python3
"""Bounded original OP/MAINE Master-derived display and file-hook CODE.

Five complete procedures plus both source-written parts of PFEND per artifact,
all from actual TASM OMF LEDATA/FIXUPP and decoded original target bytes.
PFEND's two-byte runtime CS: slot and GRAPH_PACK's unreviewed origin remain unknown.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

from lib.pc98 import digest_file, parse_mz
from lib.unit_context import UnitContext, load_unit_target
from lib.unit_oracle import relative_fixups
from review_master import pinned, need, sha, stored_lzh, source_blocks
from review_master_bgm import source_lines as bgm_lines
from review_context_master_large import ROOT, MASTER, real_omf, native_map, whole_source, rebind

PROOF = ROOT / 'config/context_master_hooks.json'
DECISION = ROOT / 'config/reviewed_context_master_hooks.json'
# Original native MAP publics and reviewed whole end boundaries. PFEND's
# split source-written spans are added separately below. GRAPH_PACK origin
# remains unreviewed and outside these claims.
SCOPES = (
    ('BGM_STOP_SOUND', 'libs/master.lib/bgm_stop_sound.asm', 'B_SP_SND.ASM',
     {'op': (0x3590, 32), 'maine': (0x3758, 32)}, 'equivalent-original'),
    ('GRAPH_GAIJI_PUTS', 'libs/master.lib/graph_gaiji_puts.asm', 'GRPGPUTS.ASM',
     {'op': (0x3674, 170), 'maine': (0x383c, 170)}, 'game5-gaiji-port'),
    ('GRAPH_GAIJI_PUTC', 'libs/master.lib/graph_gaiji_putc.asm', 'GRPGJPUT.ASM',
     {'op': (0x371e, 154), 'maine': (0x38e6, 154)}, 'game5-gaiji-port'),
    ('PFSTART', 'libs/master.lib/pfint21.asm', 'PFINT21.ASM',
     {'op': (0x37b8, 160), 'maine': (0x3980, 160)}, 'game5-archive-port'),
    ('PFOPEN', 'th03/formats/pfopen.asm', 'PFOPEN.ASM',
     {'op': (0x39f0, 296), 'maine': (0x3bb8, 296)}, 'game5-archive-port'),
)
ARTIFACTS = ('op', 'maine')
# PFEND is one original 408-byte procedure but has an actual two-byte
# unwritten CS: runtime dispatch slot. Only the two real LEDATA extents count.
PFEND_PARENT = {'op': 0x3858, 'maine': 0x3a20}
PFEND_SIZE = 408
PFEND_WRITTEN = (('PFEND_SOURCE_HEAD', 0, 156),
                 ('PFEND_SOURCE_TAIL', 158, 250))
PFEND_UNWRITTEN = (156, 2)


def upstream_procedure(archive, filename, name):
    blocks = [b for b in source_blocks(archive[filename], 'cp932')
              if b['name'].casefold() == name.casefold()]
    need(len(blocks) == 1, 'original author Master procedure absent: ' + name)
    return blocks[0]


def source_linked():
    parent = json.loads(MASTER.read_text())
    archive = stored_lzh(pinned(ROOT, parent['inputs']['inner_archive']))
    results = []
    target_views = {}
    for art in ARTIFACTS:
        root = ROOT / f'.analysis/builds/{art}-calibration-a/source'
        module = 'op' if art == 'op' else 'mainem'
        source_filename = 'th05_op.asm' if art == 'op' else 'th05_maine_master.asm'
        obj_path = root / f'obj/th05/{module}.obj'
        object_bytes = obj_path.read_bytes()
        segments, blocks, fixups, groups = real_omf(object_bytes)
        map_data, offsets, publics = native_map(art, source_filename, segments)
        c = UnitContext(ROOT, art)
        original = load_unit_target(c, c.config())[1]
        target_views[art] = sha(original.program_image)
        calibration = parse_mz((root / f'bin/th05/{art}.exe').read_bytes())
        cg = int.from_bytes(calibration.program_image[1:3], 'little')
        og = int.from_bytes(original.program_image[1:3], 'little')
        need(og - cg == (1 if art == 'maine' else 0), 'unexpected artifact CRT group')
        for name, source, author, positions, adaptation in SCOPES:
            start, size = positions[art]
            need(publics.get(name) == {start}, 'native public entry ambiguity: '+name)
            path = root / source
            content = path.read_bytes()
            live = [b for b in source_blocks(content, 'utf8') if b['name'] == name]
            need(len(live) == 1, 'missing native full procedure source: '+name)
            upstream = upstream_procedure(archive, author, name)
            # Only the BGM NOPCALL is exactly the author's unchanged semantic
            # source: TLINK's call relaxation produces its actual NOP. The
            # remaining GAME>=4 / GAME=5 edits are acknowledged explicitly,
            # not erased through opcode normalization.
            if adaptation == 'equivalent-original':
                need(bgm_lines(live[0]['text'], name) == bgm_lines(upstream['text'], name),
                     'BGM original procedure source differs')
            elif adaptation == 'game5-gaiji-port':
                need('if GAME ge 4' in live[0]['text'] and
                     'add' in live[0]['text'].lower() and
                     'adc' in upstream['text'].lower(),
                     'missing explicit GAME>=4 Master GAIJI adaptation')
            else:
                need('if GAME eq 5' in live[0]['text'] and
                     ('pf' in live[0]['text'].lower()),
                     'missing actual GAME=5 original Master file-port branch')
            # All source is from the real native compilation object. Compare
            # source LEDATA, every ordered FIXUPP and both MZ images, whole.
            blob = whole_source(blocks, start, size)
            actions = [x for x in fixups if start <= x['site'] < start + size]
            cal, native, linked, mz = rebind(blob, actions, start, offsets, segments,
                                            groups, cg, og)
            need(cal == calibration.program_image[start:start+size] and
                 native == original.program_image[start:start+size],
                 'complete linked native Master function differs: '+art+':'+name)
            need(relative_fixups(calibration, start, size) ==
                 relative_fixups(original, start, size) == mz,
                 'original ordered MZ relocations differ: '+name)
            need(original.program_image.find(native) == start and
                 original.program_image.find(native, start+1) == -1,
                 'original complete CODE occurrence not unique: '+name)
            results.append({
                'artifact': 'th05-'+art, 'member': name, 'start': start,
                'end': start + size, 'size': size, 'source': source,
                'original_archive_member': author, 'source_adaptation': adaptation,
                'native_OMF_sha256': sha(object_bytes), 'native_MAP_sha256': sha(map_data),
                'native_source_sha256': sha(content),
                'native_procedure_sha256': sha(live[0]['text'].encode('utf8')),
                'original_procedure_sha256': sha(upstream['text'].encode('utf8')),
                'unlinked_CODE_sha256': sha(blob), 'calibrated_CODE_sha256': sha(cal),
                'native_CODE_sha256': sha(native), 'original_ordered_MZ': mz,
                'ordered_OMF_actions': linked, 'authored_credit': 0,
            })
        # The full PFEND native procedure is 408 bytes but has two *real*
        # unwritten runtime state bytes. Determine those bytes from the
        # original OMF LEDATA coverage, not from target content or a guessed
        # gap. Every remaining byte and FIXUPP must be source-linked exactly.
        parent_start = PFEND_PARENT[art]
        parent_offset = parent_start - 0x272
        written = bytearray(PFEND_SIZE)
        for pos, data in blocks:
            low = max(parent_offset, pos)
            high = min(parent_offset + PFEND_SIZE, pos + len(data))
            if low >= high:
                continue
            begin, end = low - parent_offset, high - parent_offset
            need(not any(written[begin:end]), 'PFEND source LEDATA overlaps')
            written[begin:end] = b'\1' * (end - begin)
        expected_mask = bytearray(PFEND_SIZE)
        for _, begin, length in PFEND_WRITTEN:
            expected_mask[begin:begin+length] = b'\1' * length
        need(written == expected_mask,
             'complete PFEND CODE source-written / runtime slot split changed')
        gap_at = parent_start + PFEND_UNWRITTEN[0]
        need(calibration.program_image[gap_at:gap_at+2] ==
             original.program_image[gap_at:gap_at+2] == b'\0\0',
             'PFEND runtime-written dispatch words differ from original zero state')
        need(publics.get('PFEND') == {parent_start} and
             publics.get('PFOPEN') == {parent_start + PFEND_SIZE},
             'original PFEND whole-function public boundaries changed')
        pf_source = 'libs/master.lib/pfint21.asm'
        pf_content = (root / pf_source).read_bytes()
        pf_live = [b for b in source_blocks(pf_content, 'utf8') if b['name'] == 'PFEND']
        need(len(pf_live) == 1 and 'if GAME eq 5' in pf_live[0]['text'],
             'real GAME=5 PFEND source not preserved')
        pf_author = upstream_procedure(archive, 'PFINT21.ASM', 'PFEND')
        for role, begin, length in PFEND_WRITTEN:
            start = parent_start + begin
            blob = whole_source(blocks, start, length)
            actions = [x for x in fixups if start <= x['site'] < start+length]
            cal, native, linked, mz = rebind(blob, actions, start,
                                            offsets, segments, groups, cg, og)
            need(cal == calibration.program_image[start:start+length] and
                 native == original.program_image[start:start+length],
                 'native original PFEND source-written CODE differs: '+art+':'+role)
            need(relative_fixups(calibration, start, length) ==
                 relative_fixups(original, start, length) == mz,
                 'PFEND ordered source-written MZ relocations differ')
            need(original.program_image.find(native) == start and
                 original.program_image.find(native, start+1) == -1,
                 'original PFEND full source-written subextent not unique')
            results.append({
                'artifact': 'th05-'+art, 'member': role, 'start': start,
                'end': start+length, 'size': length, 'source': pf_source,
                'original_archive_member': 'PFINT21.ASM',
                'source_adaptation': 'game5-archive-port-omf-written',
                'complete_parent': [parent_start, PFEND_SIZE],
                'unwritten_slot': [gap_at, 2],
                'native_OMF_sha256': sha(object_bytes), 'native_MAP_sha256': sha(map_data),
                'native_source_sha256': sha(pf_content),
                'native_procedure_sha256': sha(pf_live[0]['text'].encode('utf8')),
                'original_procedure_sha256': sha(pf_author['text'].encode('utf8')),
                'unlinked_CODE_sha256': sha(blob), 'calibrated_CODE_sha256': sha(cal),
                'native_CODE_sha256': sha(native), 'original_ordered_MZ': mz,
                'ordered_OMF_actions': linked, 'authored_credit': 0,
            })
    return {
        'schema_version': 1, 'kind': 'original-OP-MAINE-Master-derived-file-and-display',
        'scopes': results, 'source_written_CODE_bytes': sum(x['size'] for x in results),
        'target_view_sha256': target_views,
        'author_archive_sha256': parent['inputs']['inner_archive']['sha256'],
        'parent_Master_sha256': digest_file(MASTER),
        'verifier_sha256': digest_file(ROOT/'scripts/review_context_master_hooks.py'),
        'authored_credit': 0, 'non_CODE_claimed': 0,
    }


def validate(record):
    parent = json.loads(MASTER.read_text())
    expected = [row for art in ARTIFACTS
                for row in ([('th05-'+art, name, positions[art][0], positions[art][1])
                             for name, _, _, positions, _ in SCOPES] +
                            [('th05-'+art, role, PFEND_PARENT[art]+start, length)
                             for role, start, length in PFEND_WRITTEN])]
    need(record.get('schema_version') == 1 and
         record.get('kind') == 'original-OP-MAINE-Master-derived-file-and-display' and
         record.get('source_written_CODE_bytes') == sum(t[3] for t in expected) and
         record.get('author_archive_sha256') == parent['inputs']['inner_archive']['sha256'] and
         record.get('parent_Master_sha256') == digest_file(MASTER) and
         record.get('verifier_sha256') == digest_file(ROOT/'scripts/review_context_master_hooks.py') and
         record.get('authored_credit') == record.get('non_CODE_claimed') == 0,
         'source-linked Master review metadata changed')
    views = record.get('target_view_sha256', {})
    need(set(views) == set(ARTIFACTS) and all(
         isinstance(views[a], str) and re.fullmatch('[0-9a-f]{64}', views[a])
         for a in ARTIFACTS), 'native decoded artifact identities absent')
    rows = record.get('scopes', [])
    need([(r['artifact'],r['member'],r['start'],r['size']) for r in rows] == expected,
         'source-listed original complete Master function extents changed')
    for r in rows:
        known = next((scope for scope in SCOPES if scope[0] == r['member']), None)
        if known is None:
            art = r['artifact'].removeprefix('th05-')
            role = next((x for x in PFEND_WRITTEN if x[0] == r['member']), None)
            need(role is not None and art in ARTIFACTS and
                 r['complete_parent'] == [PFEND_PARENT[art], PFEND_SIZE] and
                 r['unwritten_slot'] == [PFEND_PARENT[art]+PFEND_UNWRITTEN[0], 2] and
                 r['source'] == 'libs/master.lib/pfint21.asm' and
                 r['original_archive_member'] == 'PFINT21.ASM',
                 'PFEND source-write provenance / excluded runtime hole changed')
        else:
            need(r['source'] == known[1] and r['original_archive_member'] == known[2],
                 'Master source/author member changed')
        need(r['end'] == r['start']+r['size'] and r['authored_credit'] == 0 and
             r['original_ordered_MZ'] ==
             [a['site'] for a in r['ordered_OMF_actions'] if a['kind'] == 2] and
             r['source_adaptation'] == (known[4] if known else
                                         'game5-archive-port-omf-written'),
             'source FIXUPP/complete boundary or GAME port declaration differs')
        for k in ('native_OMF_sha256','native_MAP_sha256','native_source_sha256',
                  'native_procedure_sha256','original_procedure_sha256',
                  'unlinked_CODE_sha256','calibrated_CODE_sha256','native_CODE_sha256'):
            need(isinstance(r.get(k), str) and re.fullmatch('[0-9a-f]{64}',r[k]),
                 'Master original source evidence missing')
    if DECISION.exists():
        d = json.loads(DECISION.read_text())
        need(d.get('schema_version') == 1 and
             d.get('decision') == 'ADOPT_ONLY_COMPLETE_MASTER_FILE_DISPLAY_CODE' and
             d.get('evidence_sha256') == digest_file(PROOF) and
             d.get('scopes') == [[r['artifact'],r['member']] for r in rows] and
             d.get('CODE_bytes') == record['source_written_CODE_bytes'] and
             d.get('authored_credit') == 0 and d.get('other_claims') == 0,
             'master context original CODE decision changed')


def reviewed_claims(root, artifact, view, *, verify_targets=False):
    if not DECISION.exists():
        return [], None
    need(root.resolve() == ROOT.resolve(), 'wrong Master source checkout')
    record = json.loads(PROOF.read_text()); validate(record)
    need(record['target_view_sha256'][artifact] == view['sha256'],
         'decoded original target identity changed')
    if verify_targets:
        need(source_linked() == record, 'original native Master code differs')
    rows = [r for r in record['scopes'] if r['artifact'] == 'th05-'+artifact]
    return ([{'start':r['start'],'end':r['end'], 'kind':'verified-vendor-code',
              'library':'Master 0.23-derived GAME=5', 'member':r['member'],
              'authored_credit':0} for r in rows],digest_file(DECISION))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    m = p.add_mutually_exclusive_group(required=True)
    m.add_argument('--write', action='store_true')
    m.add_argument('--check', action='store_true')
    m.add_argument('--structural-check', action='store_true')
    a = p.parse_args()
    if a.write:
        need(not PROOF.exists() and not DECISION.exists(),
             'will not overwrite accepted original source evidence')
        result = source_linked()
        PROOF.write_text(json.dumps(result, indent=2)+'\n')
        print('PASS original Master file/display scope',result['source_written_CODE_bytes'])
    else:
        record=json.loads(PROOF.read_text());validate(record)
        if a.check:
            need(source_linked()==record, 'original source-linked Master CODE changed')
            print('PASS original Master hooks native bytes and ordered fixups')
        else:print('PASS original Master hook source-current structural proof')

if __name__ == '__main__':
    main()
