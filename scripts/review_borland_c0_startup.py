#!/usr/bin/env python3
"""Check Borland C0L startup's entire 621-byte written CODE prefix in three MZs.

The real C0L _TEXT continues with a two-byte unwritten CS slot and two later
written bytes; neither tail nor the following alignment earns CODE credit.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re

from lib.omf import parse_omf
from lib.pc98 import parse_mz
from lib.unit_context import UnitContext, load_unit_target
from lib.unit_extents import _index
from lib.unit_oracle import relative_fixups
from review_main_runtime import crt_roles
from review_master import need, sha

ROOT = Path(__file__).resolve().parents[1]
OBJECT = '.analysis/toolchain/installed/tc40j/LIB/C0L.OBJ'
PROOF = 'config/borland_c0_startup_ownership.json'
DECISION = 'config/reviewed_borland_c0_startup.json'
BASES = {
    'main': dict(directory='main-calibration-b', frame=0x209d, frame_delta=-1,
                 data_delta=-18, bss_end_delta=-20),
    'op': dict(directory='op-calibration-a', frame=0x0efe, frame_delta=0,
               data_delta=0, bss_end_delta=0),
    'maine': dict(directory='maine-calibration-a', frame=0x1011, frame_delta=1,
                  data_delta=0, bss_end_delta=0),
}
DGROUP_WORDS = (0x1, 0x5e, 0xa5)
SHIFT_DATA_WORDS = (0x65, 0x73, 0xac, 0xb6, 0xc2, 0xe5,
                    0x11f, 0x122, 0x14e, 0x151)
SHIFT_BSS_END_WORDS = (0xb9,)
RELAXED_FAR_CALLS = (0x7e, 0x10b, 0x113, 0x141, 0x168, 0x173)
ORDERED_LOADER_SEGMENTS = (1, 0x5e, 0xa5, 0x13e)


def object_scope(raw: bytes):
    written = {}
    fixups = []
    last = None
    for rec in parse_omf(raw):
        b = rec.data
        if rec.name == 'LEDATA':
            si, pos = _index(b, 0)
            offset = int.from_bytes(b[pos:pos+2], 'little'); pos += 2
            if si == 1:
                need(not any(i in written for i in range(offset, offset + len(b[pos:]))),
                     'overlapping C0L CODE source writes')
                written.update({offset+i: byte for i, byte in enumerate(b[pos:])})
            last = offset if si == 1 else None
        elif rec.name == 'FIXUPP' and last is not None:
            at = 0
            while at < len(b):
                loc = b[at]
                need(loc & 0x80 and at + 3 <= len(b), 'unsupported C0L threaded fixup')
                flags = b[at+2]
                site = last + ((loc & 3) << 8) + b[at+1]
                kind = (loc >> 2) & 15
                at += 3
                frame = (flags >> 4) & 7
                if frame <= 2:
                    _, at = _index(b, at)
                else:
                    need(frame == 5, 'unreviewed C0L frame fixup')
                _, at = _index(b, at)
                if not flags & 4:
                    at += 2
                need(kind in (1, 2, 3) and not flags & 0x88 and at <= len(b),
                     'unreviewed C0L fixup encoding')
                fixups.append((site, 4 if kind == 3 else 2))
    need(set(written) == (set(range(621)) | set(range(623, 625))),
         'C0L _TEXT source has an unreviewed initialized CODE shape')
    need(written[620] == 0xc3,
         'C0L first complete code extent no longer ends in RET')
    need(bytes(written[i] for i in range(623,625)) == b'\x04\xc0',
         'C0L trailing foreign CS initialized values changed')
    need(len(fixups) == 57 and len({site for site,_ in fixups}) == 57,
         'original C0L OMF FIXUPP count/ordering differs')
    need(all(site + size <= 621 for site,size in fixups),
         'C0L tail has a new relocation')
    need(all(site in {off for p,size in fixups for off in range(p,p+size)}
             for site in (*DGROUP_WORDS,*SHIFT_DATA_WORDS,*SHIFT_BSS_END_WORDS)),
         'native startup binding changes are not genuine C0L OMF fixups')
    # Six legitimate TLINK relaxation sites have source-level CALL FAR (9Ah).
    need(all(written[p] == 0x9a for p in RELAXED_FAR_CALLS),
         'C0L far-call relocation/relaxation source changed')
    return bytes(written[i] for i in range(621)), fixups


def calibration_pin(name: str) -> dict:
    if name == 'main':
        parent = json.loads((ROOT/'config/master_vendor_ownership.json').read_text())
        return {'exe': parent['inputs']['calibration_exe']['sha256'],
                'map': parent['inputs']['calibration_map']['sha256']}
    parent = json.loads((ROOT/'config/master_vendor_additions.json').read_text())
    inputs = parent['table_contexts'][name]['inputs']
    return {'exe': inputs['calibration_exe']['sha256'],
            'map': inputs['calibration_map']['sha256']}


def review():
    object_raw = (ROOT/OBJECT).read_bytes()
    expected_source, fixups = object_scope(object_raw)
    crt_roles(object_raw)
    relocation_sites = {at+i for at,size in fixups for i in range(size)}
    rows = []
    for name, layout in BASES.items():
        base = ROOT/'.analysis/builds'/layout['directory']/'source'
        raw = (base/f'bin/th05/{name}.exe').read_bytes()
        map_raw = (base/f'obj/th05/{name}.map').read_bytes()
        pin = calibration_pin(name)
        need(sha(raw) == pin['exe'] and sha(map_raw) == pin['map'],
             'retained C0L calibration executable/MAP identity changed')
        cal = parse_mz(raw)
        c = UnitContext(ROOT,name)
        artifact, native, _ = load_unit_target(c,c.config())
        need(cal.valid and len(native.program_image)>=626 and
             len(cal.program_image)>=626, 'invalid source/native original MZ')
        # Independently observed MAP says this is a complete 625-byte C0L
        # CODE contribution, not a guessed 626-byte prefix including EVEN.
        regex = r'(?im)^\s*0000:0000\s+0271\s+C=CODE\s+S=_TEXT\s+G=\(none\)\s+M=c0\.ASM\s+ACBP=28\s*$'
        need(len(re.findall(regex,map_raw.decode('cp437'))) == 1,
             'native C0L _TEXT CODE contribution is not 625 bytes at start')
        actual = bytearray(cal.program_image[:621])
        # OMF proves precisely which compiled bytes were fixed up. Linker
        # relaxation is the only allowed change outside original OMF fixups.
        for pos, byte in enumerate(expected_source):
            if pos not in relocation_sites:
                expected = 0x90 if pos in RELAXED_FAR_CALLS else byte
                need(actual[pos] == expected,
                     f'retained C0L linked nonfixup CODE byte differs: {name} {pos:04X} source={byte:02X} expected={expected:02X} cal={actual[pos]:02X}')
        expected = bytearray(actual)
        for pos in DGROUP_WORDS:
            word=int.from_bytes(expected[pos:pos+2],'little')+layout['frame_delta']
            expected[pos:pos+2]=word.to_bytes(2,'little')
        for pos in SHIFT_DATA_WORDS:
            word=int.from_bytes(expected[pos:pos+2],'little')+layout['data_delta']
            expected[pos:pos+2]=word.to_bytes(2,'little')
        for pos in SHIFT_BSS_END_WORDS:
            word=int.from_bytes(expected[pos:pos+2],'little')+layout['bss_end_delta']
            expected[pos:pos+2]=word.to_bytes(2,'little')
        need(int.from_bytes(expected[1:3],'little') == layout['frame'] and
             native.program_image[:621] == bytes(expected),
             'complete C0L original CODE differs from OMF-linked startup model')
        need(relative_fixups(native,0,621)==list(ORDERED_LOADER_SEGMENTS) and
             relative_fixups(cal,0,621)==list(ORDERED_LOADER_SEGMENTS),
             'original C0L segment relocations wrong/order changed')
        need(native.program_image[621:623] == cal.program_image[621:623] == b'\0\0' and
             native.program_image[623:625] == cal.program_image[623:625] == b'\x04\xc0',
             'C0L runtime-writable/initialized CODE tail changed')
        rows.append({'artifact': artifact['id'], 'start': 0,'end':621,
                     'content_sha256': sha(native.program_image[:621]),
                     'target_sha256':artifact['sha256'],
                     'target_payload_sha256': sha(native.program_image),
                     'size':len(native.program_image),
                     'calibration_exe_sha256':sha(raw),
                     'calibration_map_sha256':sha(map_raw),
                     'original_ordered_fixups':list(ORDERED_LOADER_SEGMENTS),
                     'calibration_ordered_fixups':list(ORDERED_LOADER_SEGMENTS),
                     'link_delta':{k:layout[k] for k in ('frame_delta','data_delta','bss_end_delta')},
                     'native_frame':layout['frame']})
    return {'schema_version':1,'kind':'source-object-linked-Borland-C0L-startup',
            'classification':'third-party-library-code','original_OMF_sha256':sha(object_raw),
            'native_C0L_OMF_fixups': len(fixups),'omf_written_CODE_bytes':623,
            'reviewed_CODE_prefix_bytes':621,'unknown_runtime_tail_bytes_per_program':5,
            'authored_credit':0,'rows':rows}


def validate(proof):
    need(proof.get('schema_version')==1 and
         proof.get('kind')=='source-object-linked-Borland-C0L-startup' and
         proof.get('classification')=='third-party-library-code' and
         proof.get('authored_credit')==0 and proof.get('omf_written_CODE_bytes')==623 and
         proof.get('native_C0L_OMF_fixups')==57 and
         proof.get('reviewed_CODE_prefix_bytes')==621 and
         proof.get('unknown_runtime_tail_bytes_per_program')==5 and
         proof.get('original_OMF_sha256')==sha((ROOT/OBJECT).read_bytes()),
         'stale Borland C0L CODE provenance')
    rows=proof.get('rows',[])
    need(len(rows)==3, 'incomplete three-program Borland C0L CODE review')
    for row,(name,layout) in zip(rows,BASES.items()):
        pin=calibration_pin(name)
        need(row.get('artifact')=='th05-'+name and row.get('start')==0 and
             row.get('end')==621 and row.get('native_frame')==layout['frame'] and
             row.get('link_delta')=={k:layout[k] for k in ('frame_delta','data_delta','bss_end_delta')} and
             row.get('original_ordered_fixups')==list(ORDERED_LOADER_SEGMENTS) and
             row.get('calibration_ordered_fixups')==list(ORDERED_LOADER_SEGMENTS) and
             row.get('calibration_exe_sha256')==pin['exe'] and
             row.get('calibration_map_sha256')==pin['map'] and
             all(isinstance(row.get(k),str) and len(row[k])==64
                 for k in ('content_sha256','target_sha256','target_payload_sha256')),
             'Borland C0L member/source/frame/relocation review changed')


def reviewed_claims(root: Path, views: dict, *,verify_targets=False):
    if not (root/DECISION).exists():return {},None
    raw=(root/PROOF).read_bytes()
    proof=json.loads(raw);validate(proof)
    decision_raw=(root/DECISION).read_bytes()
    need(json.loads(decision_raw)=={
        'schema_version':1,'classification':'third-party-library-code',
        'decision':'ADOPT_ONLY_C0L_WRITTEN_CODE_PREFIX','authored_credit':0,
        'evidence_sha256':sha(raw),
        'artifacts':[r['artifact'] for r in proof['rows']]},
        'unreviewed/stale C0L source claim')
    if verify_targets:need(review()==proof,'real native C0L source/link replay changed')
    result={}
    for row in proof['rows']:
        name=row['artifact'].removeprefix('th05-')
        need(views[name]['size']==row['size'] and
             views[name]['sha256']==row['target_payload_sha256'],
             'Borland C0L ownership has a stale decoded target')
        result[name]=[{'start':0,'end':621,'kind':'verified-vendor-code',
                       'library':'Borland C++ 4.02','member':'C0L.OBJ/_TEXT'}]
    return result,sha(decision_raw)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    g=p.add_mutually_exclusive_group(required=True)
    for mode in ('write','check','structural-check'):g.add_argument('--'+mode,action='store_true')
    args=p.parse_args()
    if args.write:
        proof=review();(ROOT/PROOF).write_text(json.dumps(proof,indent=2)+'\n')
        (ROOT/DECISION).write_text(json.dumps({
            'schema_version':1,'classification':'third-party-library-code',
            'decision':'ADOPT_ONLY_C0L_WRITTEN_CODE_PREFIX','authored_credit':0,
            'evidence_sha256':sha((ROOT/PROOF).read_bytes()),
            'artifacts':[r['artifact'] for r in proof['rows']]},indent=2)+'\n')
    else:proof=json.loads((ROOT/PROOF).read_text())
    validate(proof)
    if args.check:need(review()==proof,'original-source C0L startup changed')
    print('PASS: C0L startup CODE 621 x 3; 5-byte unknown tail preserved per MZ')


if __name__=='__main__':main()
