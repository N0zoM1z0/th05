#!/usr/bin/env python3
"""Source-verify complete private Master RTC register-modification leaf in OP/MAINE."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

from lib.pc98 import parse_mz
from lib.unit_context import UnitContext, load_unit_target
from lib.unit_oracle import relative_fixups
from review_master import need, pinned, sha, stored_lzh, source_blocks
from review_context_master_large import ROOT, MASTER, real_omf, whole_source, native_map

PROOF = ROOT / 'config/reviewed_context_rtc_mod.json'
PARENT = ROOT / 'config/context_memory_vsync.json'
NAME = 'rtc_mod'
START, SIZE = 0x04e5, 19
ARTIFACTS = ('op', 'maine')


def replay() -> dict:
    parent = json.loads(MASTER.read_text())
    prev = json.loads(PARENT.read_text())
    need(prev['rtc_unknown_gap'] == [START, START+SIZE],
         'original RTC leaf gap is no longer 19 bytes')
    archive = stored_lzh(pinned(ROOT, parent['inputs']['inner_archive']))
    source = [r for r in source_blocks(archive['ATRTCMOD.ASM'], 'cp932') if r['name'] == NAME]
    need(len(source) == 1 and len(source[0]['text']) >= 150 and
         source[0]['text'].count('call') == 0 and
         source[0]['text'].count('out\tRTC_') == 3 and
         source[0]['text'].count('in\tAL,RTC_DATA') == 1,
         'original private RTC hardware helper changed')
    scopes = []
    for art in ARTIFACTS:
        base = ROOT / f'.analysis/builds/{art}-calibration-a/source'
        objname = 'op' if art == 'op' else 'mainem'
        module = 'th05_op.asm' if art == 'op' else 'th05_maine_master.asm'
        src = (base / 'libs/master.lib/atrtcmod.asm').read_bytes()
        written = [r for r in source_blocks(src, 'utf8') if r['name'] == NAME]
        need(len(written) == 1 and written[0]['text'].strip() == source[0]['text'].strip(),
             'retained source for native RTC register helper differs from Master author')
        obj = (base / f'obj/th05/{objname}.obj').read_bytes()
        segs,blocks,fixups,groups = real_omf(obj)
        native_source = whole_source(blocks, START, SIZE)
        need(not any(START <= x['site'] < START+SIZE for x in fixups),
             'private RTC register helper gained a real CODE relocation')
        map_raw, offsets, publics = native_map(art, module, segs)
        need(publics.get('rtc_int_set') == {0x0454} and
             publics.get('BCLOSER') == {0x053c},
             'native RTC context before/after the helper changed')
        ctx = UnitContext(ROOT, art)
        artifact, original, _ = load_unit_target(ctx, ctx.config())
        cal = parse_mz((base / f'bin/th05/{art}.exe').read_bytes())
        need(cal.valid and original.program_image[START:START+SIZE] == native_source ==
             cal.program_image[START:START+SIZE],
             'real RTC private 19-byte body does not match original and calibration')
        need(relative_fixups(original, START, SIZE) ==
             relative_fixups(cal, START, SIZE) == [],
             'private RTC helper has an unexpected ordered MZ relocation')
        need(original.program_image.find(native_source) == START and
             original.program_image.find(native_source,START+1) < 0,
             'private RTC instruction sequence is not unique in original')
        scopes.append(dict(artifact=artifact['id'],start=START,end=START+SIZE,size=SIZE,
                           member=NAME,author_source_sha256=sha(source[0]['text'].encode()),
                           native_source_sha256=sha(src),
                           real_TASM_object_sha256=sha(obj),
                           real_MAP_sha256=sha(map_raw),
                           original_sha256=artifact['sha256'],
                           original_payload_sha256=sha(original.program_image),
                           complete_CODE_sha256=sha(native_source),
                           ordered_original_fixups=[],instruction_bytes=SIZE,
                           authored_credit=0))
    return {'schema_version':1,'kind':'Master-RTC-private-source-leaf',
            'classification':'third-party-library-CODE',
            'old_rtc_source_proof_sha256':sha(PARENT.read_bytes()),
            'author_archive_sha256':parent['inputs']['inner_archive']['sha256'],
            'total_bytes':2*SIZE,'authored_credit':0,'scopes':scopes}


def validate(proof: dict) -> None:
    old = json.loads(PARENT.read_text())
    parent = json.loads(MASTER.read_text())
    need(proof.get('schema_version') == 1 and proof.get('kind') == 'Master-RTC-private-source-leaf' and
         proof.get('classification') == 'third-party-library-CODE' and
         proof.get('old_rtc_source_proof_sha256') == sha(PARENT.read_bytes()) and
         proof.get('author_archive_sha256') == parent['inputs']['inner_archive']['sha256'] and
         proof.get('total_bytes') == 2*SIZE and proof.get('authored_credit') == 0 and
         old['rtc_unknown_gap'] == [START,START+SIZE],
         'private RTC leaf source proof is stale or mislabeled')
    rows = proof.get('scopes',[])
    need(len(rows) == len(ARTIFACTS), 'missing an RTC helper from OP or MAINE')
    for row, art in zip(rows, ARTIFACTS):
        ancestor = next(x for x in old['scopes'] if
                        x['artifact'] == 'th05-'+art and x['member'] == 'rtc_int_set')
        need(row.get('artifact') == 'th05-'+art and row.get('start') == START and
             row.get('end') == START+SIZE and row.get('size') == SIZE and
             row.get('member') == NAME and row.get('authored_credit') == 0 and
             row.get('instruction_bytes') == SIZE and
             row.get('ordered_original_fixups') == [] and
             row.get('original_payload_sha256') == old['original_view_sha256'][art] and
             row.get('real_TASM_object_sha256') == ancestor['actual_OMF_sha256'] and
             row.get('real_MAP_sha256') == ancestor['actual_MAP_sha256'] and
             all(isinstance(row.get(k),str) and len(row[k]) == 64 for k in
                 ('author_source_sha256','native_source_sha256','original_sha256','complete_CODE_sha256')),
             'native original RTC leaf identity/extent/source differs')


def reviewed_claims(root: Path, name: str, view: dict, *,verify_targets=False):
    if not (root / 'config/reviewed_context_rtc_mod.json').exists():
        return [], None
    raw = (root / 'config/reviewed_context_rtc_mod.json').read_bytes()
    proof = json.loads(raw)
    validate(proof)
    row = next(x for x in proof['scopes'] if x['artifact'] == 'th05-'+name)
    need(view['sha256'] == row['original_payload_sha256'],
         'RTC leaf proof belongs to a different decoded target')
    if verify_targets:
        need(replay() == proof, 'original linked RTC leaf source proof changed')
    return ([dict(start=START,end=START+SIZE,kind='verified-vendor-code',
                  library='Master 0.23',member=NAME,instruction_bytes=SIZE,
                  authored_credit=0)],sha(raw))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    flag=parser.add_mutually_exclusive_group(required=True)
    for name in ('write','check','structural-check'):
        flag.add_argument('--'+name,action='store_true')
    opt=parser.parse_args()
    if opt.write:
        data=replay()
        PROOF.write_text(json.dumps(data,indent=2)+'\n')
    else:
        data=json.loads(PROOF.read_text())
    validate(data)
    if opt.check:need(replay()==data,'RTC native source/byte evidence changed')
    print('PASS: OP and MAINE source-linked complete rtc_mod, 19 bytes each')


if __name__ == '__main__':main()
