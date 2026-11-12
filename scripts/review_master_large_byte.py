#!/usr/bin/env python3
"""Recover Master LARGE_BYTE's 16-bit-pair expansion lookup in MAIN CODE.

This is a CODE-class constant table, never sixteen machine instructions.
Only the previously unowned [2038,2048) table is selected.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

from lib.omf import parse_omf
from lib.pc98 import parse_mz
from lib.unit_context import UnitContext, load_unit_target
from lib.unit_extents import _index
from lib.unit_oracle import relative_fixups
from review_master import need, pinned, sha

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'config/master_vendor_ownership.json'
EVIDENCE = ROOT / 'config/reviewed_master_large_byte.json'
SOURCE = 'libs/master.lib/large_byte.asm'
START, SIZE = 0x2038, 16


def source_bytes(raw: bytes) -> bytes:
    text = raw.decode('cp932')
    need(len(re.findall(r'(?im)^\s*public\s+LARGE_BYTE\s*$', text)) == 1,
         'Master LARGE_BYTE no longer has one public source label')
    rows = []
    for line in text.splitlines():
        body = line.split(';', 1)[0].strip()
        match = re.fullmatch(r'(?:LARGE_BYTE\s+)?DB\s+(.+)', body, re.I)
        if match:
            values = match[1].split(',')
            need(len(values) == 8 and all(re.fullmatch(r'\s*[0-9a-f]{3}h\s*', x, re.I)
                                           for x in values), 'unreviewed literal table source')
            rows.extend(int(x.strip()[:-1], 16) for x in values)
    need(len(rows) == SIZE, 'Master expansion table is not two 8-byte rows')
    expanded = [((i & 1) * 3) | ((i & 2) * 6) | ((i & 4) * 12) | ((i & 8) * 24)
                for i in range(16)]
    need(rows == expanded, 'source no longer expands each nibble to 2-bit pixels')
    return bytes(rows)


def review() -> dict:
    parent = json.loads(BASE.read_text())
    source_record = [r for r in parent['frozen_source_closure'] if r['name'] == SOURCE]
    need(len(source_record) == 1, 'Master calibration has no unique source file')
    src = (ROOT / parent['calibration_source_root'] / SOURCE).read_bytes()
    need(len(src) == source_record[0]['size'] and sha(src) == source_record[0]['sha256'],
         'actual TASM source differs from the frozen Master closure')
    data = source_bytes(src)
    obj = pinned(ROOT, parent['inputs']['calibration_object'])
    map_raw = pinned(ROOT, parent['inputs']['calibration_map'])
    cal = parse_mz(pinned(ROOT, parent['inputs']['calibration_exe']))
    ctx = UnitContext(ROOT, 'main')
    artifact, native, _ = load_unit_target(ctx, ctx.config())
    need(native.program_image[START:START + SIZE] == data ==
         cal.program_image[START:START + SIZE],
         'original and linked calibration disagree with the source table')
    need(native.program_image.find(data) == START and
         native.program_image.find(data, START + 1) < 0,
         'nonunique Master LARGE_BYTE target occurrence')
    need(relative_fixups(native, START, SIZE) == relative_fixups(cal, START, SIZE) == [],
         'Master LARGE_BYTE unexpectedly contains MZ relocations')
    need(len(re.findall(r'(?im)^\s*0000:2038\s+(?:idle\s+)?LARGE_BYTE\s*$',
                        map_raw.decode('cp437'))) == 2,
         'actual native MAP does not name LARGE_BYTE at 2038')
    records = parse_omf(obj)
    pub = [r for r in records if r.name == 'PUBDEF' and b'LARGE_BYTE' in r.data]
    need(len(pub) == 1 and pub[0].data == b'\x00\x01\x0aLARGE_BYTE\xc6\x1d\x00',
         'original TASM near public does not bind _TEXT+1DC6')
    # C0L's complete 625-byte _TEXT plus its following align byte precedes
    # the main source segment, giving genuine local 1DC6 to linked 2038.
    local = START - 0x272
    need(local == 0x1dc6, 'Borland C0L _TEXT source frame changed')
    chunks = []
    for rec in records:
        if rec.name != 'LEDATA':
            continue
        si, pos = _index(rec.data, 0)
        at = int.from_bytes(rec.data[pos:pos + 2], 'little')
        body = rec.data[pos + 2:]
        if si == 1 and at <= local and local + SIZE <= at + len(body):
            need(body[local - at:local - at + SIZE] == data,
                 'actual CODE-class LEDATA lookup differs from source')
            chunks.append((rec.offset, at, len(body)))
    need(len(chunks) == 1, 'LARGE_BYTE lacks a single complete TASM CODE LEDATA')
    return {'schema_version': 1, 'classification': 'foreign-CODE-class-lookup-table',
            'artifact': artifact['id'], 'start': START, 'end': START + SIZE,
            'size': SIZE, 'instruction_bytes': 0, 'authored_credit': 0,
            'library': 'Master 0.23', 'member': 'LARGE_BYTE',
            'source_sha256': sha(src), 'table_sha256': sha(data),
            'original_target_sha256': artifact['sha256'],
            'original_payload_sha256': sha(native.program_image),
            'calibration_object_sha256': sha(obj),
            'calibration_map_sha256': sha(map_raw),
            'calibration_exe_sha256': parent['inputs']['calibration_exe']['sha256'],
            'source_object_local': local, 'linked_source_public': START,
            'actual_CODE_LEDATA_record_offset': chunks[0][0],
            'actual_CODE_LEDATA_local_offset': chunks[0][1],
            'actual_CODE_LEDATA_size': chunks[0][2],
            'ordered_original_MZ_fixups': []}


def validate(record: dict) -> None:
    parent = json.loads(BASE.read_text())
    sources = [r for r in parent['frozen_source_closure'] if r['name'] == SOURCE]
    need(len(sources) == 1 and
         record.get('schema_version') == 1 and
         record.get('classification') == 'foreign-CODE-class-lookup-table' and
         record.get('artifact') == 'th05-main' and
         record.get('start') == START and record.get('end') == START + SIZE and
         record.get('size') == SIZE and record.get('instruction_bytes') == 0 and
         record.get('authored_credit') == 0 and
         record.get('library') == 'Master 0.23' and record.get('member') == 'LARGE_BYTE' and
         record.get('source_sha256') == sources[0]['sha256'] and
         record.get('calibration_object_sha256') == parent['inputs']['calibration_object']['sha256'] and
         record.get('calibration_map_sha256') == parent['inputs']['calibration_map']['sha256'] and
         record.get('calibration_exe_sha256') == parent['inputs']['calibration_exe']['sha256'] and
         record.get('original_target_sha256') == parent['inputs']['target']['sha256'] and
         record.get('original_payload_sha256') == parent['target_payload_sha256'] and
         record.get('source_object_local') == 0x1dc6 and
         record.get('linked_source_public') == START and
         record.get('actual_CODE_LEDATA_local_offset') == 0x1dba and
         record.get('actual_CODE_LEDATA_size') == 533 and
         record.get('ordered_original_MZ_fixups') == [] and
         isinstance(record.get('table_sha256'), str) and len(record['table_sha256']) == 64,
         'Master CODE-class LARGE_BYTE ownership proof has changed')


def reviewed_claims(root: Path, views: dict, *, verify_targets=False):
    if not (root / 'config/reviewed_master_large_byte.json').exists():
        return {}, None
    raw = (root / 'config/reviewed_master_large_byte.json').read_bytes()
    record = json.loads(raw)
    validate(record)
    need(views['main']['size'] >= START + SIZE and
         views['main']['sha256'] == record['original_payload_sha256'],
         'Master lookup source belongs to a different target')
    if verify_targets:
        need(review() == record, 'actual Master CODE-class lookup source changed')
    return {'main': [{'start': START, 'end': START + SIZE,
                      'kind': 'verified-vendor-code',
                      'content_kind': 'CODE-class-lookup-table', 'instruction_bytes': 0,
                      'library': 'Master 0.23', 'member': 'LARGE_BYTE'}]}, sha(raw)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    group = p.add_mutually_exclusive_group(required=True)
    for name in ('write', 'check', 'structural-check'):
        group.add_argument('--' + name, action='store_true')
    args = p.parse_args()
    if args.write:
        result = review()
        EVIDENCE.write_text(json.dumps(result, indent=2) + '\n')
    else:
        result = json.loads(EVIDENCE.read_text())
    validate(result)
    if args.check:
        need(review() == result, 'native Master LARGE_BYTE proof differs')
    print('PASS: Master 16-byte CODE lookup from original TASM source, zero instructions credited')


if __name__ == '__main__':
    main()
