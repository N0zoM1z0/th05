#!/usr/bin/env python3
"""Classify one complete vendor routine built from unchanged primary source.

The original .186 / FAR macro context is retained. No private-name, operand,
instruction or byte substitutions turn the candidate text into primary source.
Two actual source producers and an assembled negative are re-read; no game
authored credit or whole-executable acceptance is granted.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re

import review_master as base
from lib.omf import describe_omf, parse_omf, normalize_dependency_timestamps
from lib.pc98 import parse_mz
from lib.replay_toolchain import static_toolchain, validate_full_toolchain
from lib.unit_oracle import compare_unit

ROOT = Path(__file__).resolve().parents[1]
PROOF = 'config/master_primary_circlefill_ownership.json'
DECISION = 'config/reviewed_master_primary_circlefill.json'
BASE = 'config/master_vendor_ownership.json'
BASE_SHA = '8b5e9b31ce345df277a31348d49aec9197e4c5c390eec0b9f812516c8287010a'
EVIDENCE_SHA = '0ec2f44786ffd1d23b04eb93fcc9b0b37ef828f3bb326cabcc379d710bfcc86e'
START, SIZE = 0x100e, 150
TARGET_SCOPE_SHA = 'b15c3ea64d3ecc0a30c173ccff95c138f0f9be7a816f1e4bdc020f1fc37583c5'
PRIMARY = {'GC_CIRCF.ASM': 'e2147c9cd744ba51efbb82ac3ba119f0803462724f34a458f0ba06a3c8940e0b',
           'FUNC.INC': '940e80cd776198272eac3d17a1efe0436500fbb4105ca1ed937518957526770a'}
WORKS = [('a', '.analysis/vendor-review/circlefill-primary-first-a'),
         ('b', '.analysis/vendor-review/circlefill-primary-b'),
         ('negative', '.analysis/vendor-review/circlefill-primary-negative')]
BINDINGS = {name+'.asm': 'probes/units/circlefill_primary_'+name+'.asm' for name in ('before', 'after')}
ASM = ['wine', r'C:\TASM50\bin\TASM32.EXE']
SOURCE_FLAGS = ['/mx', '/t', '/q', '/w2', '/jJUMPS', '/DFARMODEL']
RESPONSE = b'-c -s -E before.obj gc_circf.obj after.obj, units.exe, units.map,\r\n'
MUTATION = (b'mov\tDI,0', b'mov\tDI,1')
SOURCES = ['scripts/review_master_primary_circlefill.py', 'scripts/review_master.py',
           'scripts/lib/omf.py', 'scripts/lib/pc98.py',
           'scripts/lib/unit_oracle.py', 'scripts/lib/replay_toolchain.py', 'scripts/lib/toolchain.py',
           'scripts/lib/reference_build.py']


def need(value, message):
    if not value:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def digest(value):
    return sha(json.dumps(value, sort_keys=True, separators=(',', ':')).encode())


def primary_inputs(root):
    inherited = json.loads((root / BASE).read_text())
    base.review_inputs(inherited, root=root)
    archive = base.stored_lzh(base.pinned(root, inherited['inputs']['inner_archive']))
    result = {}
    for name, expected in PRIMARY.items():
        need(sha(archive[name]) == expected, 'primary archive source identity differs')
        result[name] = archive[name]
    return result


def source_input(original, negative):
    if not negative:
        return original
    before, after = MUTATION
    need(original.count(before) == 1, 'own original-source negative is not unique')
    return original.replace(before, after)


def object_shape(raw):
    # This original command profile produces no translator-version COMENT.
    # Keep the generic game-ASM gate unchanged and bind this separate profile
    # to the actual pinned executable, command/log and complete OMF structure.
    description = describe_omf(raw)
    need(description['module_name'] == 'GC_CIRCF.ASM' and description['translator_comments'] == [] and
         description['dependency_paths'] == [] and description['record_counts'] ==
         dict(COMENT=2, EXTDEF=1, FIXUPP=1, GRPDEF=1, LEDATA=1, LNAMES=4,
              MODEND=1, PUBDEF=1, SEGDEF=2, THEADR=1), 'original command OMF profile differs')
    records = parse_omf(raw)
    names = ['']
    for record in records:
        if record.name == 'LNAMES':
            at = 0
            while at < len(record.data):
                size = record.data[at]
                need(at+1+size <= len(record.data), 'original OMF name bounds')
                names.append(record.data[at+1:at+1+size].decode('ascii'))
                at += size+1
    need(names == ['', '', '_TEXT', 'CODE', '_DATA', 'DATA', 'DGROUP'], 'original segment names differ')
    need([r.data for r in records if r.name == 'SEGDEF'] ==
         [b'\x48\x96\0\x02\x03\x01', b'\x48\0\0\x04\x05\x01'],
         'one whole150 CODE and empty DATA ordinary16-bit SEGDEFs required')
    need([r.data for r in records if r.name == 'GRPDEF'] == [b'\x06\xff\x02'] and
         [r.data for r in records if r.name == 'COMENT'] == [b'\x40\xa1', b'\x40\xa2\x01'] and
         [r.data for r in records if r.name == 'MODEND'] == [b'\0'], 'original group/comment/no-entry profile differs')
    chunks = [r.data for r in records if r.name == 'LEDATA']
    need(len(chunks) == 1 and len(chunks[0]) == SIZE+3 and chunks[0][:3] == b'\x01\0\0',
         'one complete150-byte CODE LEDATA with no holes required')
    ext = [r.data for r in records if r.name == 'EXTDEF']
    need(ext == [b'\x0aGRCG_HLINE\0\x09GRCG_PSET\0'], 'original far helper names differ')
    pubs = [r.data for r in records if r.name == 'PUBDEF']
    need(pubs == [b'\0\x01\x0fGRCG_CIRCLEFILL\0\0\0'], 'complete primary public/offset differs')
    # Five genuine self-relative16 EXTDEF offset fixups framed by current _TEXT.
    expected = b''.join(bytes([0x84, at, 0x06, 1, target])
                        for at, target in [(40, 1), (61, 1), (92, 1), (113, 1), (142, 2)])
    need([r.data for r in records if r.name == 'FIXUPP'] == [expected],
         'original four-byte far-call FIXUPP context differs')
    return dict(kind='complete-original-assembler-code', segment='_TEXT', size=SIZE,
                ledata=[dict(offset=0, size=SIZE, sha256=sha(chunks[0][3:]))])


def map_context(raw):
    text = raw.decode('cp437')
    pattern = r'^\s*0000:100E\s+0096\s+C=CODE\s+S=_TEXT\s+G=\(none\)\s+M=GC_CIRCF\.ASM\s'
    need(len(re.findall(pattern, text, re.M | re.I)) == 1, 'whole original CODE MAP scope differs')
    for address, name in [('0000:100E', 'GRCG_CIRCLEFILL'), ('0000:1690', 'GRCG_HLINE'), ('0000:1A44', 'GRCG_PSET')]:
        need(re.search(r'^\s*'+address+r'\s+(?:idle\s+)?'+name+r'\s*$', text, re.M | re.I),
             'actual far source/helper public differs')
    need(re.search(r'^\s*209D:0000\s+C4C8\s+C=DATA\s+S=_DATA\s+G=DGROUP\s+M=after\.asm\s',
                   text, re.M | re.I), 'actual foreign DATA frame differs')


def observe(root, work, original, target, negative=False):
    source = work / 'source'
    expected = {**original, **{alias: (root/path).read_bytes() for alias, path in BINDINGS.items()},
                'build_dumb.bat': b'', 'link.rsp': RESPONSE}
    expected['GC_CIRCF.ASM'] = source_input(original['GC_CIRCF.ASM'], negative)
    for name, raw in expected.items():
        need((source/name).read_bytes() == raw, 'actual primary/binding input differs: '+name)
    rows = json.loads((work/'commands.json').read_text())
    argv = [ASM + SOURCE_FLAGS + ['GC_CIRCF.ASM', 'gc_circf.obj']]
    argv += [ASM + ['/m', '/mx', '/t', name+'.asm', name+'.obj'] for name in ('before', 'after')]
    argv += [['wine', str(root/'_reference/ReC98/bin/msdos.exe'), '-e', '-x', 'tlink', '@link.rsp']]
    need(len(rows) == len(argv), 'four actual successful source/binder/link commands required')
    for row, command in zip(rows, argv):
        need(row['command'] == command and row['returncode'] == 0 and
             sha((work/row['log']).read_bytes()) == row['log_sha256'], 'successful argv/log differs')
    obj = (source/'gc_circf.obj').read_bytes()
    scope = object_shape(obj)
    for name in ('before', 'after'):
        raw = (source/(name+'.obj')).read_bytes()
        description = describe_omf(raw)
        need(description['translator_comments'] == ['Turbo Assembler  Version 5.0'] and
             not any(description['record_counts'].get(k, 0) for k in ('LEDATA', 'LIDATA', 'COMDAT', 'FIXUPP')),
             'binding object supplies payload or fixups')
        need([r.data for r in parse_omf(raw) if r.name == 'MODEND'] == [b'\0'], 'binding supplies an entry')
    map_context((source/'units.map').read_bytes())
    candidate = parse_mz((source/'units.exe').read_bytes())
    comparison = compare_unit(target, candidate, START, START, SIZE)
    need(comparison['fixups_exact'] and comparison['target_fixups'] == comparison['candidate_fixups'] == [],
         'original ordered MZ fixups differ')
    need(comparison['exact'] is (not negative), 'complete raw source comparison/negative differs')
    return dict(comparison=comparison, object_scope=scope,
                artifacts={name: sha((source/name).read_bytes()) for name in
                           ['gc_circf.obj', 'before.obj', 'after.obj', 'units.map', 'units.exe']},
                deterministic_identity={
                    'original_object_raw': sha(obj),
                    'binding_metadata': {name: sha(normalize_dependency_timestamps((source/(name+'.obj')).read_bytes()))
                                         for name in ('before', 'after')},
                    'map_raw': sha((source/'units.map').read_bytes()),
                    'mz_raw': sha((source/'units.exe').read_bytes())},
                input_hashes={name: sha(raw) for name, raw in expected.items()},
                commands_sha256=sha((work/'commands.json').read_bytes()))


def build_metadata(*, root=ROOT):
    original = primary_inputs(root)
    inherited = json.loads((root/BASE).read_text())
    target = parse_mz(base.pinned(root, inherited['inputs']['target']))
    need(sha(target.program_image[START:START+SIZE]) == TARGET_SCOPE_SHA, 'original whole scope differs')
    manifest, surfaces = static_toolchain(root)
    rounds = []
    for label, path in WORKS:
        work = root/path
        tool = json.loads((work/'toolchain-attestation.json').read_text())
        validate_full_toolchain(tool, manifest, surfaces)
        reuse = json.loads((work/'toolchain-reuse-proof.json').read_text())
        need(reuse['manifest_sha256'] == manifest and reuse['reused'] is True and
             reuse['original_full_receipt_sha256'] == sha((work/'toolchain-attestation.json').read_bytes()),
             'successful installed tool reuse differs')
        rounds.append(dict(label=label, path=path, observation=observe(root, work, original, target, label == 'negative'),
                           toolchain_sha256=sha((work/'toolchain-attestation.json').read_bytes()),
                           reuse_sha256=sha((work/'toolchain-reuse-proof.json').read_bytes())))
    need(rounds[0]['observation']['deterministic_identity'] == rounds[1]['observation']['deterministic_identity'],
         'two independent primary producers are not deterministic')
    from capstone import Cs, CS_ARCH_X86, CS_MODE_16
    ins = list(Cs(CS_ARCH_X86, CS_MODE_16).disasm(target.program_image[START:START+SIZE], START))
    need(sum(i.size for i in ins) == SIZE and not any(i.mnemonic == 'nop' for i in ins),
         'native complete instruction/NOP boundary differs')
    return dict(schema_version=1, kind='original-primary-source-master-circlefill-proposal', decision='PROPOSAL',
                authored_credit=0, authored_denominator=None, base_proof_sha256=sha((root/BASE).read_bytes()),
                target_sha256=inherited['inputs']['target']['sha256'], start=START, size=SIZE,
                target_scope_sha256=TARGET_SCOPE_SHA, primary_inputs=PRIMARY, source_flags=SOURCE_FLAGS,
                binding_inputs={path: sha((root/path).read_bytes()) for path in BINDINGS.values()},
                source_assembler_invocations=3, binding_assembler_invocations=6, linker_invocations=3,
                source_transformations=[], first_positive_retained_after_its_successful_new_build=True,
                native_instruction_count=len(ins), instruction_nop_offsets=[], padding_bytes=0,
                ordered_mz_fixups=[], negative_changed_offsets=[i for i, (a, b) in enumerate(zip(
                    target.program_image[START:START+SIZE], parse_mz((root/WORKS[2][1]/'source/units.exe').read_bytes()).program_image[START:START+SIZE])) if a != b],
                rounds=rounds, reviewer_sources=[dict(file=name, sha256=sha((root/name).read_bytes())) for name in SOURCES],
                limitations='One original primary GC_CIRCF module only, .186 / MODEL SMALL / FAR macros unchanged. Not a reconstructed historical game project or distribution. Other circle procedures and their DS/BSS differences remain unknown. Raw original object/MAP/MZ deterministic; only dependency timestamps in empty binding-object metadata are normalized for identity, retaining raw hashes. No authored credit, linked-byte/fixup normalization or whole executable equality.')


def validate_metadata(meta, *, root=ROOT):
    need(digest({k: v for k, v in meta.items() if k != 'reviewer_sources'}) == EVIDENCE_SHA, 'frozen primary producer evidence differs')
    need(meta['schema_version'] == 1 and meta['kind'] == 'original-primary-source-master-circlefill-proposal' and
         meta['decision'] == 'PROPOSAL' and meta['authored_credit'] == 0 and meta['authored_denominator'] is None,
         'original source proof cannot grant authored credit')
    need(meta['base_proof_sha256'] == BASE_SHA == sha((root/BASE).read_bytes()), 'frozen base differs')
    need((meta['start'], meta['size'], meta['target_scope_sha256']) == (START, SIZE, TARGET_SCOPE_SHA) and
         meta['primary_inputs'] == PRIMARY and meta['source_flags'] == SOURCE_FLAGS and
         meta['source_transformations'] == [] and meta['padding_bytes'] == 0 and
         meta['ordered_mz_fixups'] == meta['instruction_nop_offsets'] == [], 'whole source/unit policy differs')
    need(meta['reviewer_sources'] == [dict(file=name, sha256=sha((root/name).read_bytes())) for name in SOURCES],
         'reviewer source identity differs')
    need(meta['binding_inputs'] == {path: sha((root/path).read_bytes()) for path in BINDINGS.values()}, 'binding identity differs')
    base.validate_metadata(json.loads((root/BASE).read_text()), root=root)


def review_inputs(meta, *, root=ROOT):
    validate_metadata(meta, root=root)
    need(build_metadata(root=root) == meta, 'actual primary producers/native proof differ')
    return dict(full_bytes=SIZE, procedures=1, byte_proof_replayed=True, authored_credit=0, new_builds=0)


def reviewed_claims(root, views, *, verify_targets=False):
    path = root/DECISION
    if not path.exists():
        return [], None
    raw = (root/PROOF).read_bytes()
    meta = json.loads(raw)
    validate_metadata(meta, root=root)
    inherited = json.loads((root/BASE).read_text())
    expected = dict(schema_version=1, decision='ADOPT', classification='verified-vendor-code',
                    proof_sha256=sha(raw), base_proof_sha256=BASE_SHA, target_sha256=meta['target_sha256'],
                    start=START, size=SIZE, procedure='GRCG_CIRCLEFILL', authored_credit=0, authored_denominator=None)
    need(json.loads(path.read_text()) == expected, 'explicit original-source vendor decision differs')
    need(views['main']['sha256'] == inherited['target_payload_sha256'], 'target payload differs')
    if verify_targets:
        review_inputs(meta, root=root)
    return [dict(start=START, end=START+SIZE, kind='verified-vendor-code',
                 library='master.lib 0.23 original source', member='GRCG_CIRCLEFILL')], sha(path.read_bytes())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    for name in ('write', 'check', 'structural-check'):
        modes.add_argument('--'+name, action='store_true')
    args = parser.parse_args()
    meta = build_metadata() if args.write else json.loads((ROOT/PROOF).read_text())
    validate_metadata(meta)
    if args.write:
        (ROOT/PROOF).write_text(json.dumps(meta, indent=2)+'\n')
    print(json.dumps(review_inputs(meta) if args.check else dict(full_bytes=SIZE, procedures=1,
          byte_proof_replayed=args.write, authored_credit=0, new_builds=0), indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
