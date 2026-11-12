#!/usr/bin/env python3
"""Original-source and native-TASM proof for the two still-unknown BGM note tables.

MAIN's identical 176 bytes already belong to an accepted Master data scope.
This verifies only OP and MAINE. The unwritten BGM global state is excluded.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re

from lib.omf import parse_omf
from lib.pc98 import parse_mz
from lib.unit_context import UnitContext, load_unit_target
from lib.unit_oracle import relative_fixups
from review_main_master_literal_tables import source_payload
from review_master import need, pinned, sha, stored_lzh

ROOT = Path(__file__).resolve().parents[1]
PROOF = 'config/master_bgm_literal_op_maine_ownership.json'
DECISION = 'config/reviewed_master_bgm_literal_op_maine.json'
PARENT = 'config/master_vendor_additions.json'
SOURCE_PROOF = 'config/main_master_literal_tables_ownership.json'
CONFIGS = {
    'op': dict(start=0xF844, cal_start=0xF844, ds=0xEFE, cal_ds=0xEFE,
               segment_base=0x4D2, obj='op.obj', module='th05_op.asm'),
    'maine': dict(start=0x10652, cal_start=0x10642, ds=0x1011, cal_ds=0x1010,
                  segment_base=0xBC, obj='mainem.obj', module='th05_maine_master.asm'),
}


def digest(path: str) -> str:
    return sha((ROOT / path).read_bytes())


def actual_data(obj: bytes, start: int, size: int) -> list[dict]:
    """Prove entire scope is written by real normal _DATA LEDATA, without FIXUPP."""
    names = ['']
    segments = [None]
    records = parse_omf(obj)
    found, cover = [], bytearray(size)
    for index, rec in enumerate(records):
        b = rec.data
        if rec.name == 'LNAMES':
            pos = 0
            while pos < len(b):
                count = b[pos]; pos += 1
                need(pos + count <= len(b), 'truncated original object names')
                names.append(b[pos:pos + count].decode('ascii')); pos += count
        elif rec.name == 'SEGDEF':
            from review_master import idx
            ni, pos = idx(b, 3); ci, pos = idx(b, pos); oi, pos = idx(b, pos)
            need(pos == len(b) and ni < len(names) and ci < len(names), 'bad real SEGDEF')
            segments.append((names[ni], names[ci], int.from_bytes(b[1:3], 'little')))
        elif rec.name in ('LEDATA', 'LIDATA'):
            from review_master import idx
            si, pos = idx(b, 0)
            need(si < len(segments) and pos + 2 <= len(b), 'bad data segment index')
            at = int.from_bytes(b[pos:pos + 2], 'little'); pos += 2
            if segments[si][:2] != ('_DATA', 'DATA'):
                continue
            if rec.name == 'LIDATA':
                # It must not intersect this scope; native LIDATA is used for
                # other Master tables and is intentionally not credited here.
                need(not (at <= start < at + 2), 'iterated data at BGM table')
                continue
            payload = b[pos:]
            low, high = max(at, start), min(at + len(payload), start + size)
            if low >= high:
                continue
            need(records[index + 1].name != 'FIXUPP' and not any(cover[low - start: high - start]),
                 'relocated or overlapping BGM table LEDATA')
            chunk = payload[low - at:high - at]
            found.append({'record_offset': rec.offset, 'segment_offset': at,
                          'record_size': len(payload), 'scope_offset': low - start,
                          'scope_size': len(chunk), 'record_sha256': sha(payload),
                          'scope_content_sha256': sha(chunk)})
            cover[low - start: high - start] = b'\1' * len(chunk)
    need(len([s for s in segments if s and s[:2] == ('_DATA', 'DATA')]) == 1,
         'not a unique actual compiler DATA segment')
    need(all(cover) and found, 'source did not write all original BGM bytes')
    return found


def review() -> dict:
    primary = json.loads((ROOT / SOURCE_PROOF).read_text())
    main = [r for r in primary['scope_rows'] if r['member'] == 'BGM_NOTE_AND_LENGTH']
    need(len(main) == 1 and main[0]['size'] == 176, 'missing previously accepted MAIN BGM source proof')
    context = json.loads((ROOT / PARENT).read_text())
    main_parent = json.loads((ROOT / 'config/master_vendor_ownership.json').read_text())
    archive = stored_lzh(pinned(ROOT, main_parent['inputs']['inner_archive']))
    body = source_payload(archive['B_DATA.ASM'], 'BGM_NOTE_AND_LENGTH', 'cp932', undf=100)
    need(len(body) == 176 and sha(body) == main[0]['DATA_sha256'], 'author BGM source changed')
    rows = []
    for name, pin in CONFIGS.items():
        inputs = context['table_contexts'][name]['inputs']
        cal_obj = pinned(ROOT, inputs['calibration_object'])
        cal = parse_mz(pinned(ROOT, inputs['calibration_exe']))
        mp = pinned(ROOT, inputs['calibration_map']).decode('cp437')
        ctx = UnitContext(ROOT, name)
        artifact, original, view = load_unit_target(ctx, ctx.config())
        raw = (ROOT / context['table_contexts'][name]['source_root'] /
               'libs/master.lib/bgm[data].asm').read_bytes()
        need(source_payload(raw, 'BGM_NOTE_AND_LENGTH', 'utf8', undf=100) == body,
             'retained native BGM assembler source changed')
        start, cal_start = pin['start'], pin['cal_start']
        need(original.program_image[start:start + 176] == body and
             cal.program_image[cal_start:cal_start + 176] == body and
             original.program_image.find(body) == start and
             original.program_image.find(body, start + 1) < 0,
             'native/actual original complete BGM note/duration bytes differ')
        need(not relative_fixups(original, start, 176) and
             not relative_fixups(cal, cal_start, 176),
             'BGM note words unexpectedly have MZ relocations')
        for label, offset in (('note_dat', 0), ('lcount', 48)):
            # Require both the by-name and by-value native MAP public rows.
            address = f'{pin["cal_ds"]:04X}:{cal_start - pin["cal_ds"] * 16 + offset:04X}'
            hits = re.findall(r'(?im)^\s*' + address + r'\s+(?:idle\s+)?' + label + r'\s*$', mp)
            need(len(hits) == 2, f'{name} actual MAP {label} address differs')
        local = cal_start - (pin['cal_ds'] * 16 + pin['segment_base'])
        ledatas = actual_data(cal_obj, local, 176)
        # The only ordinary LEDATA slice is compared to the actual source and
        # linked table; no bytes are inferred from target zeros or padding.
        need(len(ledatas) == 1 and ledatas[0]['scope_offset'] == 0 and
             ledatas[0]['scope_size'] == 176 and
             ledatas[0]['scope_content_sha256'] == sha(body),
             'incomplete or unexpected BGM OMF LEDATA content')
        rows.append({'id': name + '-master-bgm-note-length', 'artifact': artifact['id'],
                     'start': start, 'end': start + 176, 'size': 176,
                     'original_ds': pin['ds'], 'calibration_ds': pin['cal_ds'],
                     'calibration_start': cal_start, 'data_sha256': sha(body),
                     'actual_omf_ledatas': ledatas, 'original_ordered_fixups': [],
                     'calibration_ordered_fixups': [],
                     'source_sha256': sha(raw),
                     'calibration_object_sha256': sha(cal_obj),
                     'calibration_map_sha256': inputs['calibration_map']['sha256'],
                     'target_sha256': artifact['sha256'],
                     'target_payload_sha256': sha(original.program_image),
                     'target_size': len(original.program_image)})
    return {'schema_version': 1, 'kind': 'source-linked-Master-BGM-note-and-length',
            'classification': 'third-party-library-initialized-data', 'authored_credit': 0,
            'instruction_bytes': 0, 'total_bytes': 352,
            'primary_proof_sha256': digest(SOURCE_PROOF),
            'context_proof_sha256': digest(PARENT),
            'primary_BGM_source_sha256': sha(archive['B_DATA.ASM']),
            'rows': rows}


def validate(proof: dict) -> None:
    need(proof.get('schema_version') == 1 and proof.get('kind') ==
         'source-linked-Master-BGM-note-and-length' and proof.get('classification') ==
         'third-party-library-initialized-data' and proof.get('authored_credit') == 0 and
         proof.get('instruction_bytes') == 0 and proof.get('total_bytes') == 352 and
         proof.get('primary_proof_sha256') == digest(SOURCE_PROOF) and
         proof.get('context_proof_sha256') == digest(PARENT), 'stale Master BGM source proof')
    primary = json.loads((ROOT / SOURCE_PROOF).read_text())
    main = next(r for r in primary['scope_rows'] if r['member'] == 'BGM_NOTE_AND_LENGTH')
    need(proof.get('primary_BGM_source_sha256') == main['author_source_sha256'],
         'not the original Master BGM author file')
    rows = proof.get('rows', [])
    need(len(rows) == 2 and [r.get('id') for r in rows] ==
         [name + '-master-bgm-note-length' for name in CONFIGS], 'incomplete Master BGM scope')
    parent = json.loads((ROOT / PARENT).read_text())
    for r, (name, pin) in zip(rows, CONFIGS.items()):
        inputs = parent['table_contexts'][name]['inputs']
        target = parent['table_contexts'][name]
        need(r['start'] == pin['start'] and r['end'] == pin['start'] + 176 and
             r['size'] == 176 and r['original_ds'] == pin['ds'] and
             r['calibration_ds'] == pin['cal_ds'] and
             r['calibration_start'] == pin['cal_start'] and
             r['data_sha256'] == main['DATA_sha256'] and
             r['artifact'] == 'th05-' + name and
             r['source_sha256'] == sha((ROOT / target['source_root'] /
                                    'libs/master.lib/bgm[data].asm').read_bytes()) and
             r['target_payload_sha256'] == target['target_payload_sha256'] and
             r['target_sha256'] == target['target_sha256'] and
             r['target_size'] == target['target_view']['payload_size'] and
             r['calibration_object_sha256'] == inputs['calibration_object']['sha256'] and
             r['calibration_map_sha256'] == inputs['calibration_map']['sha256'] and
             r['original_ordered_fixups'] == r['calibration_ordered_fixups'] == [] and
             len(r['actual_omf_ledatas']) == 1 and
             r['actual_omf_ledatas'][0]['scope_offset'] == 0 and
             r['actual_omf_ledatas'][0]['scope_size'] == 176 and
             r['actual_omf_ledatas'][0]['scope_content_sha256'] == main['DATA_sha256'],
             'unverified native Master BGM linked identity/source or scope')


def reviewed_claims(root: Path, views: dict, *, verify_targets=False):
    if not (root / DECISION).exists():
        return {}, None
    proof_bytes = (root / PROOF).read_bytes()
    proof = json.loads(proof_bytes)
    validate(proof)
    decision_bytes = (root / DECISION).read_bytes()
    decision = json.loads(decision_bytes)
    need(decision == {'schema_version': 1, 'decision': 'ADOPT_ONLY_OP_MAINE_BGM_NOTE_LENGTH',
                      'classification': 'third-party-library-initialized-data',
                      'authored_credit': 0, 'evidence_sha256': sha(proof_bytes),
                      'scopes': [r['id'] for r in proof['rows']]},
         'unreviewed BGM initialized DATA decision')
    if verify_targets:
        need(review() == proof, 'native linked BGM source replay differs')
    result = {}
    for row in proof['rows']:
        name = row['artifact'].removeprefix('th05-')
        need(views[name]['size'] == row['target_size'] and
             views[name]['sha256'] == row['target_payload_sha256'],
             'BGM literal scope belongs to another decoded target')
        result[name] = [{'start': row['start'], 'end': row['end'],
                         'kind': 'verified-vendor-initialized-data',
                         'content_kind': 'library-initialized-data',
                         'instruction_bytes': 0, 'library': 'Master 0.23',
                         'member': 'BGM_NOTE_AND_LENGTH', 'scope_id': row['id']}]
    return result, sha(decision_bytes)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    exclusive = parser.add_mutually_exclusive_group(required=True)
    exclusive.add_argument('--write', action='store_true')
    exclusive.add_argument('--check', action='store_true')
    exclusive.add_argument('--structural-check', action='store_true')
    args = parser.parse_args()
    if args.write:
        proof = review()
        (ROOT / PROOF).write_text(json.dumps(proof, indent=2) + '\n')
        decision = {'schema_version': 1, 'decision': 'ADOPT_ONLY_OP_MAINE_BGM_NOTE_LENGTH',
                    'classification': 'third-party-library-initialized-data',
                    'authored_credit': 0, 'evidence_sha256': digest(PROOF),
                    'scopes': [r['id'] for r in proof['rows']]}
        (ROOT / DECISION).write_text(json.dumps(decision, indent=2) + '\n')
    else:
        proof = json.loads((ROOT / PROOF).read_text())
    validate(proof)
    if args.check:
        need(review() == proof, 'original Master BGM source/linked evidence changed')
    print('PASS: OP/MAINE BGM source-backed 2 x 176-byte Master DATA',
          '(native checked)' if args.write or args.check else '(structural)')


if __name__ == '__main__':
    main()
