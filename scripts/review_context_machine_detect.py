#!/usr/bin/env python3
"""OP/MAINE: four complete source-backed Master machine-detection functions.

Check actual TASM OMF and the original decoded MZ images. The ported
GET_MACHINE_AT retains a native DB near-jump compatibility spelling; this
is real frozen vendor source, not synthesized game C++.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

from lib.pc98 import digest_file, parse_mz
from lib.unit_context import UnitContext, load_unit_target
from lib.unit_oracle import relative_fixups
from review_master import need, pinned, sha, source_blocks, stored_lzh
from review_master_grcg import symbolic_source
from review_context_master_large import ROOT, MASTER, real_omf, native_map, whole_source, rebind

PROOF = ROOT / 'config/context_machine_detect.json'
DECISION = ROOT / 'config/reviewed_context_machine_detect.json'
# Original exported entry addresses and whole function lengths. No isolated
# assembler padding, adjacent machine probe, or raw vector is claimed.
SCOPES = (
    ('GET_MACHINE_AT', 'get_machine_at.asm', 'GETMACAT.ASM', (0x1016, 0x1068), 342, 5),
    ('GET_MACHINE_DOSBOX', 'get_machine_dosbox.asm', 'GETMACDB.ASM', (0x116c, 0x11be), 50, 2),
    ('CHECK_MACHINE_FMR', 'check_machine_fmr.asm', 'GETMACFM.ASM', (0x119e, 0x11f0), 14, 0),
    ('GET_MACHINE', 'get_machine.asm', 'GETMACHI.ASM', (0x11ac, 0x11fe), 28, 0),
)
ARTIFACTS = ('op', 'maine')


def source_derivative(original: str, native: str, name: str) -> str:
    lines = symbolic_source(original)
    actual = symbolic_source(native)
    if name == 'GET_MACHINE_AT':
        changes = {
            'movax,fmr': ['movax,fmr_at'],
            'jeget_at_machine_exit': ['jnzzun1', 'jmpget_at_machine_exit', 'zun1:'],
            'jmpget_machine_dosbox': ['db0e9h,001h,000h'],
        }
        for k in changes:
            need(lines.count(k) == 1, 'original Master probe instruction changed: ' + k)
        need(lines.count('jnznot_dosv') == 2,
             'original machine probe must have exactly two DOS/V exits')
        first, second = ('jzzun2', 'jmpnot_dosv', 'zun2:'), ('jzzun3', 'jmpnot_dosv', 'zun3:')
        n = 0
        expected = []
        for line in lines:
            if line == 'jnznot_dosv':
                expected.extend(first if n == 0 else second)
                n += 1
            else:
                expected.extend(changes.get(line, [line]))
    elif name == 'GET_MACHINE':
        changes = {
            'jeget_machine_98': ['jnzzun1', 'nop', 'nop', 'jmpget_machine_98', 'zun1:'],
            'movax,fmr': ['movax,fmr_machine'],
        }
        for key in changes:
            need(lines.count(key) == 1, 'original machine dispatcher source changed: ' + key)
        expected = [part for line in lines for part in changes.get(line, [line])]
    else:
        expected = lines
    need(expected == actual, 'actual Master machine-detection source has unreviewed opcodes/operands: ' + name)
    return sha('\n'.join(actual).encode('utf8'))


def replay():
    parent = json.loads(MASTER.read_text())
    archive = stored_lzh(pinned(ROOT, parent['inputs']['inner_archive']))
    rows, view_hash = [], {}
    for art in ARTIFACTS:
        root = ROOT / f'.analysis/builds/{art}-calibration-a/source'
        module = 'op' if art == 'op' else 'mainem'
        omf = (root / f'obj/th05/{module}.obj').read_bytes()
        segs, blocks, fixups, groups = real_omf(omf)
        map_raw, offsets, public = native_map(
            art, 'th05_op.asm' if art == 'op' else 'th05_maine_master.asm', segs)
        ctx = UnitContext(ROOT, art)
        target = load_unit_target(ctx, ctx.config())[1]
        cal = parse_mz((root / f'bin/th05/{art}.exe').read_bytes())
        view_hash[art] = sha(target.program_image)
        cg, og = (int.from_bytes(i.program_image[1:3], 'little') for i in (cal, target))
        need(og - cg == (1 if art == 'maine' else 0),
             'original machine probe DGROUP frame differs from native calibration')
        for name, filename, upstream, points, size, count in SCOPES:
            start = points[ARTIFACTS.index(art)]
            need(public.get(name) == {start}, 'real Master machine detection exported source boundary changed')
            native_source = (root / 'libs/master.lib' / filename).read_bytes()
            compiled = [b for b in source_blocks(native_source, 'utf8') if b['name'] == name]
            original = [b for b in source_blocks(archive[upstream], 'cp932') if b['name'] == name]
            need(len(compiled) == len(original) == 1, 'original Master source function absent')
            canonical = source_derivative(original[0]['text'], compiled[0]['text'], name)
            source = whole_source(blocks, start, size)
            actions = [f for f in fixups if start <= f['site'] < start + size]
            need(len(actions) == count, 'original machine-detection OMF fixup count differs: ' + name)
            c, n, action_log, mz = rebind(source, actions, start, offsets, segs, groups, cg, og)
            wanted = target.program_image[start:start+size]
            need(c == cal.program_image[start:start+size] and n == wanted,
                 'complete original machine-detection native CODE differs: ' + name)
            need(mz == relative_fixups(cal, start, size) == relative_fixups(target, start, size),
                 'original machine-probe ordered relocations differ')
            need(target.program_image.find(wanted) == start and
                 target.program_image.find(wanted, start+1) < 0,
                 'complete original machine procedure is not uniquely located')
            rows.append({
                'artifact': 'th05-'+art, 'member': name, 'start': start,
                'end': start+size, 'size': size, 'source': 'libs/master.lib/'+filename,
                'original_archive_member': upstream,
                'original_source_sha256': sha(original[0]['text'].encode('utf8')),
                'actual_source_sha256': sha(native_source),
                'canonical_source_sha256': canonical,
                'real_OMF_sha256': sha(omf), 'real_MAP_sha256': sha(map_raw),
                'original_CODE_sha256': sha(n), 'unlinked_CODE_sha256': sha(source),
                'ordered_original_MZ': mz, 'ordered_OMF_actions': action_log,
                'authored_credit': 0,
            })
    return {
        'schema_version': 1, 'kind': 'OP-MAINE-original-Master-machine-detector-source',
        'scopes': rows, 'source_written_CODE_bytes': sum(r['size'] for r in rows),
        'target_views': view_hash,
        'author_archive_sha256': parent['inputs']['inner_archive']['sha256'],
        'parent_master_sha256': digest_file(MASTER),
        'verifier_sha256': digest_file(ROOT/'scripts/review_context_machine_detect.py'),
        'authored_credit': 0,
    }


def validate(record):
    parent = json.loads(MASTER.read_text())
    expected = [('th05-'+art, n, points[ARTIFACTS.index(art)], size)
                for art in ARTIFACTS for n,_,_,points,size,_ in SCOPES]
    need(record.get('schema_version') == 1 and
         record.get('kind') == 'OP-MAINE-original-Master-machine-detector-source' and
         record.get('source_written_CODE_bytes') == sum(x[3] for x in expected) and
         record.get('author_archive_sha256') == parent['inputs']['inner_archive']['sha256'] and
         record.get('parent_master_sha256') == digest_file(MASTER) and
         record.get('verifier_sha256') == digest_file(ROOT/'scripts/review_context_machine_detect.py') and
         record.get('authored_credit') == 0,
         'original Master machine-detector evidence identity changed')
    v = record.get('target_views', {})
    need(set(v) == set(ARTIFACTS) and all(re.fullmatch('[0-9a-f]{64}',x) for x in v.values()),
         'original machine-detector decoded target identity missing')
    scopes = record.get('scopes', [])
    need([(r['artifact'],r['member'],r['start'],r['size']) for r in scopes] == expected,
         'original Master machine detector complete function boundaries changed')
    for r in scopes:
        spec = next(x for x in SCOPES if x[0] == r['member'])
        need(r['end'] == r['start']+r['size'] and r['authored_credit'] == 0 and
             r['source'] == 'libs/master.lib/'+spec[1] and
             r['original_archive_member'] == spec[2] and
             len(r['ordered_OMF_actions']) == spec[5] and
             r['ordered_original_MZ'] == [a['site'] for a in r['ordered_OMF_actions'] if a['kind'] == 2],
             'source boundaries or ordered original machine CODE fixups differ')
        for key in ('original_source_sha256', 'actual_source_sha256',
                    'canonical_source_sha256', 'real_OMF_sha256',
                    'real_MAP_sha256', 'original_CODE_sha256', 'unlinked_CODE_sha256'):
            need(isinstance(r.get(key),str) and re.fullmatch('[0-9a-f]{64}',r[key]),
                 'missing actual native source/OMF/code evidence')
    if DECISION.exists():
        d = json.loads(DECISION.read_text())
        need(d.get('schema_version') == 1 and
             d.get('decision') == 'ADOPT_COMPLETE_ORIGINAL_MACHINE_PROBE_CODE' and
             d.get('evidence_sha256') == digest_file(PROOF) and
             d.get('scope_names') == [r['member'] for r in scopes] and
             d.get('CODE_bytes') == record['source_written_CODE_bytes'] and
             d.get('authored_credit') == 0,
             'machine-code source adoption decision missing or stale')


def reviewed_claims(root,artifact,view,*,verify_targets=False):
    if not DECISION.exists(): return [],None
    need(root.resolve() == ROOT.resolve(), 'wrong reconstruction checkout')
    proof = json.loads(PROOF.read_text())
    validate(proof)
    need(proof['target_views'][artifact] == view['sha256'],
         'original machine-detection target identity changed')
    if verify_targets: need(replay() == proof, 'original source-linked machine probe differs')
    return ([{'start':r['start'], 'end':r['end'], 'kind':'verified-vendor-code',
              'library':'Master 0.23-derived machine detector',
              'member':r['member'], 'authored_credit':0}
             for r in proof['scopes'] if r['artifact'] == 'th05-'+artifact],
            digest_file(DECISION))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--write',action='store_true')
    g.add_argument('--check',action='store_true')
    g.add_argument('--structural-check',action='store_true')
    a=p.parse_args()
    if a.write:
        need(not PROOF.exists() and not DECISION.exists(), 'cannot overwrite original native proof')
        proof=replay();PROOF.write_text(json.dumps(proof,indent=2)+'\n')
        print('PASS complete original source machine-detector CODE',proof['source_written_CODE_bytes'])
    else:
        data=json.loads(PROOF.read_text());validate(data)
        if a.check:
            need(replay()==data,'original native machine detector CODE changed')
            print('PASS original machine detection CODE and relocations')
        else:print('PASS original machine source provenance')

if __name__=='__main__': main()
