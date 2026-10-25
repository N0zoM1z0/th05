#!/usr/bin/env python3
"""Review untouched original GRCG_CIRCLE_X producers, with zero authored credit.

Original source, macro context and flags remain literal. Three foreign WORD
bindings derive independently from complete original DATA initializer records.
This read-only reviewer never assembles, rewrites source or normalizes CODE.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re

import review_master as base
from review_master_primary_circlefill import need, sha, digest, ASM, SOURCE_FLAGS
from lib.omf import describe_omf, parse_omf, normalize_dependency_timestamps
from lib.pc98 import parse_mz
from lib.replay_toolchain import static_toolchain, validate_full_toolchain
from lib.unit_oracle import compare_unit, map_publics

ROOT = Path(__file__).resolve().parents[1]
PROOF = 'config/master_primary_circlex_ownership.json'
DECISION = 'config/reviewed_master_primary_circlex.json'
BASE = 'config/master_vendor_ownership.json'
BASE_SHA = '8b5e9b31ce345df277a31348d49aec9197e4c5c390eec0b9f812516c8287010a'
EVIDENCE_SHA = '95d57279b715fdffb0832008bad942930b2b3dfa4cbcb7ce56e5ac06c72271e9'
START, SIZE = 0x121c, 240
TARGET_SCOPE_SHA = '34d1c8991f308c411c6ab23054f464ba09f60f414183f9587614dad14a35b982'
PRIMARY = {'GC_CIRCX.ASM': '31fd01abd3b8a0e7ac130c8ee9e5f006786fd08475865c53847567daf41729ae',
           'FUNC.INC': '940e80cd776198272eac3d17a1efe0436500fbb4105ca1ed937518957526770a'}
CONTEXT = {'CLIP.ASM': '77df8e03605cb1272c9c282c235bdc4d84e9b391b5b5820b61b69965e4210ffb',
           'GRP.ASM': '78e78c7df4bfdc75164d9857d5aa264303bc05f93ca3daae37eb69307010aeed'}
WORKS = [(label, '.analysis/vendor-review/circlex-primary-'+label) for label in ('a', 'b', 'negative')]
BINDINGS = {name+'.asm': 'probes/units/circlex_primary_'+name+'.asm' for name in ('before', 'after')}
RESPONSE = b'-c -s -E before.obj gc_circx.obj after.obj, units.exe, units.map,\r\n'
MUTATION = (b'inc\tAX', b'dec\tAX')
NOP_OFFSETS = [57, 65, 239]
CHUNKS = [(0, 87), (87, 5), (92, 3), (95, 71), (166, 3), (169, 71)]
SYMBOLS = {'ClipYT': 0x372, 'ClipYT_seg': 0x378, 'graph_VramZoom': 0x3cc}
SOURCES = ['scripts/review_master_primary_circlex.py', 'scripts/review_master_primary_circlefill.py',
           'scripts/review_master.py', 'scripts/lib/omf.py', 'scripts/lib/pc98.py',
           'scripts/lib/unit_oracle.py', 'scripts/lib/replay_toolchain.py', 'scripts/lib/toolchain.py',
           'scripts/lib/reference_build.py']


def primary_inputs(root):
    inherited = json.loads((root/BASE).read_text())
    base.review_inputs(inherited, root=root)
    archive = base.stored_lzh(base.pinned(root, inherited['inputs']['inner_archive']))
    result = {}
    for name, expected in {**PRIMARY, **CONTEXT}.items():
        need(sha(archive[name]) == expected, 'original source/context identity differs')
        result[name] = archive[name]
    return result


def initializer(raw, fields):
    """Parse only complete named DW/DB records with decimal/hex products."""
    text = raw.decode('cp932')
    section = re.search(r'(?im)^\s*\.DATA\s*(?:;[^\r\n]*)?$', text)
    need(section is not None, 'complete original DATA section required')
    text = text[section.end():]
    text = re.split(r'(?im)^\s*(?:\.DATA\?(?:\s|$)|\.CODE\b|END\b)', text)[0]
    rows = []
    for line in text.splitlines():
        code = line.split(';', 1)[0].strip()
        if not code or re.fullmatch(r'(?i)public\s+[a-z_]\w*(?:\s*,\s*[a-z_]\w*)*', code):
            continue
        if re.fullmatch(r'(?i)[a-z_]\w*\s+label\s+(?:word|byte)', code):
            continue
        row = re.fullmatch(r'(?i)([a-z_]\w*)\s+(dw|db)\s+(.+)', code)
        need(row is not None, 'unreviewed original DATA layout directive')
        rows.append(row.groups())
    need([(name, kind.lower()) for name, kind, _ in rows] == fields, 'whole initializer declaration order differs')
    output, offsets = bytearray(), {}
    for name, kind, expression in rows:
        factors = expression.strip().lower().split('*')
        need(factors and all(re.fullmatch(r'(?:[0-9]+|[0-9][0-9a-f]*h)', f) for f in factors),
             'unreviewed initializer expression')
        value = 1
        for factor in factors:
            value *= int(factor[:-1], 16) if factor.endswith('h') else int(factor)
        width = 2 if kind.lower() == 'dw' else 1
        need(value < (1 << (width*8)), 'initializer exceeds declared width')
        offsets[name] = len(output)
        output.extend(value.to_bytes(width, 'little'))
    return bytes(output), offsets


def data_context(original, target):
    layouts = [('CLIP.ASM', [(n, 'dw') for n in
                ('ClipXL', 'ClipXW', 'ClipXR', 'ClipYT', 'ClipYH', 'ClipYB', 'ClipYT_seg', 'ClipYB_adr')],
                0x36c, 16, 'fbdba363a6875408228174f53215b81b7b5f11b8f449266d0e4949386dcd2c9f'),
               ('GRP.ASM', [('_graph_VramSeg', 'dw'), ('_graph_VramWords', 'dw'),
                ('_graph_VramLines', 'dw'), ('_graph_VramWidth', 'dw'), ('_graph_VramZoom', 'dw'),
                ('_graph_MeshByte', 'db')], 0x3c4, 11,
                '76f94dec73b8bddc3f93da96b0cddfe96880b05680b4d8f4899825f2f348e2ab')]
    loaded_end = min(0x209d0+0xc4c8, len(target.program_image))
    data = target.program_image[0x209d0:loaded_end]
    anchors, symbols = [], {}
    for name, fields, expected, size, expected_sha in layouts:
        raw, offsets = initializer(original[name], fields)
        need(len(raw) == size and sha(raw) == expected_sha, 'complete original initializer differs')
        hits = [i for i in range(len(data)-len(raw)+1) if data[i:i+len(raw)] == raw]
        need(hits == [expected], 'whole original DATA record is not uniquely anchored')
        symbols.update({field.lstrip('_'): expected+offset for field, offset in offsets.items()})
        anchors.append(dict(source=name, source_sha256=CONTEXT[name], size=size,
                            sha256=expected_sha, native_DS=0x209d, native_offset=expected,
                            unique_matches=hits, authored_credit=0))
    need({name: symbols[name] for name in SYMBOLS} == SYMBOLS, 'foreign WORD symbol derivation differs')
    return dict(anchors=anchors, foreign_WORD_symbols=SYMBOLS,
                available_loaded_DATA_range=[0x209d0, loaded_end], DATA_ownership_adopted=False)


def source_input(original, negative):
    if not negative:
        return original
    before, after = MUTATION
    need(original.count(before) == 1, 'own original-source negative is not unique')
    return original.replace(before, after)


def object_shape(raw):
    description = describe_omf(raw)
    need(description['module_name'] == 'GC_CIRCX.ASM' and description['translator_comments'] == [] and
         description['dependency_paths'] == [] and description['record_counts'] ==
         dict(COMENT=2, EXTDEF=1, FIXUPP=1, GRPDEF=1, LEDATA=6, LNAMES=4,
              MODEND=1, PUBDEF=1, SEGDEF=2, THEADR=1), 'original quiet OMF profile differs')
    records = parse_omf(raw)
    need([r.name for r in records] == ['THEADR', 'LNAMES', 'COMENT', 'LNAMES', 'SEGDEF',
         'LNAMES', 'SEGDEF', 'LNAMES', 'GRPDEF', 'EXTDEF', 'PUBDEF', 'COMENT', 'LEDATA',
         'FIXUPP', 'LEDATA', 'LEDATA', 'LEDATA', 'LEDATA', 'LEDATA', 'MODEND'],
         'original OMF record/relocation association differs')
    need([r.data for r in records if r.name == 'LNAMES'] ==
         [b'\0', b'\x05_TEXT\x04CODE', b'\x05_DATA\x04DATA', b'\x06DGROUP'], 'segment names differ')
    need([r.data for r in records if r.name == 'SEGDEF'] ==
         [b'\x48\xf0\0\x02\x03\x01', b'\x48\0\0\x04\x05\x01'],
         'whole ordinary word CODE240 and empty DATA required')
    need([r.data for r in records if r.name == 'GRPDEF'] == [b'\x06\xff\x02'] and
         [r.data for r in records if r.name == 'COMENT'] == [b'\x40\xa1', b'\x40\xa2\x01'] and
         [r.data for r in records if r.name == 'MODEND'] == [b'\0'], 'group/comment/no-entry profile differs')
    chunks = [r.data for r in records if r.name == 'LEDATA']
    need([(c[0], int.from_bytes(c[1:3], 'little'), len(c)-3) for c in chunks] ==
         [(1, offset, size) for offset, size in CHUNKS], 'six gapless original CODE records required')
    need([r.data for r in records if r.name == 'EXTDEF'] ==
         [b'\x06ClipYT\0\x0aClipYT_seg\0\x0egraph_VramZoom\0'], 'true foreign DATA names differ')
    need([r.data for r in records if r.name == 'PUBDEF'] ==
         [b'\0\x01\x0dGRCG_CIRCLE_X\0\0\0'], 'complete original far public differs')
    expected = bytes.fromhex('c40e160103c41d160101c424160102c4125401c4165401c4295401c42d5401c4315401')
    need([r.data for r in records if r.name == 'FIXUPP'] == [expected], 'three DATA/five CS-local fixups differ')
    body = b''.join(c[3:] for c in chunks)
    need([int.from_bytes(body[i:i+2], 'little') for i in (85, 93, 167)] == [0x1234]*3 and
         [body[i] for i in (91, 165)] == [9, 9], 'original JMOV/ORG initial operands differ')
    return dict(kind='complete-original-assembler-code', segment='_TEXT', size=SIZE,
                ledata=[dict(offset=offset, size=size, sha256=sha(c[3:]))
                        for c, (offset, size) in zip(chunks, CHUNKS)])


def map_context(path):
    text = path.read_text(encoding='cp437')
    for pattern in (r'^\s*0000:121C\s+00F0\s+C=CODE\s+S=_TEXT\s+G=\(none\)\s+M=GC_CIRCX\.ASM\s',
                    r'^\s*209D:0000\s+0000\s+C=DATA\s+S=_DATA\s+G=DGROUP\s+M=GC_CIRCX\.ASM\s',
                    r'^\s*209D:0000\s+C4C8\s+C=DATA\s+S=_DATA\s+G=DGROUP\s+M=after\.asm\s'):
        need(len(re.findall(pattern, text, re.M | re.I)) == 1, 'actual whole CODE/empty DATA/group frame differs')
    publics = map_publics(path)
    for name, address in {'GRCG_CIRCLE_X': START, **{k: 0x209d0+v for k, v in SYMBOLS.items()}}.items():
        need([value for value, public in publics if public == name] == [address], 'actual public/symbol frame differs')


def observe(root, work, original, target, negative=False):
    source = work/'source'
    expected = {name: original[name] for name in PRIMARY}
    expected.update({alias: (root/path).read_bytes() for alias, path in BINDINGS.items()})
    expected.update({'build_dumb.bat': b'', 'link.rsp': RESPONSE})
    expected['GC_CIRCX.ASM'] = source_input(original['GC_CIRCX.ASM'], negative)
    for name, raw in expected.items():
        need((source/name).read_bytes() == raw, 'actual untouched source/binding alias differs: '+name)
    rows = json.loads((work/'commands.json').read_text())
    argv = [ASM + SOURCE_FLAGS + ['GC_CIRCX.ASM', 'gc_circx.obj']]
    argv += [ASM + ['/m', '/mx', '/t', name+'.asm', name+'.obj'] for name in ('before', 'after')]
    argv += [['wine', str(root/'_reference/ReC98/bin/msdos.exe'), '-e', '-x', 'tlink', '@link.rsp']]
    need(len(rows) == len(argv), 'four actual successful source/binder/link commands required')
    for row, command in zip(rows, argv):
        need(row['command'] == command and row['returncode'] == 0 and
             sha((work/row['log']).read_bytes()) == row['log_sha256'], 'actual successful argv/log differs')
    obj = (source/'gc_circx.obj').read_bytes()
    scope = object_shape(obj)
    for name in ('before', 'after'):
        raw = (source/(name+'.obj')).read_bytes()
        description = describe_omf(raw)
        need(description['translator_comments'] == ['Turbo Assembler  Version 5.0'] and
             not any(description['record_counts'].get(k, 0) for k in ('LEDATA', 'LIDATA', 'COMDAT', 'FIXUPP')),
             'binding supplies initialized payload or fixups')
        need([r.data for r in parse_omf(raw) if r.name == 'MODEND'] == [b'\0'], 'binding supplies entry')
    map_context(source/'units.map')
    candidate = parse_mz((source/'units.exe').read_bytes())
    comparison = compare_unit(target, candidate, START, START, SIZE)
    need(comparison['target_fixups'] == comparison['candidate_fixups'] == [] and comparison['fixups_exact'],
         'original ordered MZ fixups differ')
    need(comparison['exact'] is (not negative), 'complete raw source/negative differs')
    return dict(comparison=comparison, object_scope=scope,
                artifacts={name: sha((source/name).read_bytes()) for name in
                           ['gc_circx.obj', 'before.obj', 'after.obj', 'units.map', 'units.exe']},
                deterministic_identity=dict(original_object_raw=sha(obj),
                    binding_metadata={name: sha(normalize_dependency_timestamps((source/(name+'.obj')).read_bytes()))
                                      for name in ('before', 'after')},
                    map_raw=sha((source/'units.map').read_bytes()), mz_raw=sha((source/'units.exe').read_bytes())),
                input_hashes={name: sha(raw) for name, raw in expected.items()},
                commands_sha256=sha((work/'commands.json').read_bytes()))


def build_metadata(*, root=ROOT):
    original = primary_inputs(root)
    inherited = json.loads((root/BASE).read_text())
    target = parse_mz(base.pinned(root, inherited['inputs']['target']))
    need(sha(target.program_image[START:START+SIZE]) == TARGET_SCOPE_SHA, 'whole native scope differs')
    context = data_context(original, target)
    manifest, surfaces = static_toolchain(root)
    rounds = []
    for label, path in WORKS:
        work = root/path
        tool = json.loads((work/'toolchain-attestation.json').read_text())
        validate_full_toolchain(tool, manifest, surfaces)
        reuse = json.loads((work/'toolchain-reuse-proof.json').read_text())
        need(reuse['manifest_sha256'] == manifest and reuse['reused'] is True and
             reuse['original_full_receipt_sha256'] == sha((work/'toolchain-attestation.json').read_bytes()),
             'successful installed-tool reuse differs')
        rounds.append(dict(label=label, path=path, observation=observe(root, work, original, target, label == 'negative'),
                           toolchain_sha256=sha((work/'toolchain-attestation.json').read_bytes()),
                           reuse_sha256=sha((work/'toolchain-reuse-proof.json').read_bytes())))
    need(rounds[0]['observation']['deterministic_identity'] == rounds[1]['observation']['deterministic_identity'],
         'two original source producers are not deterministic')
    from capstone import Cs, CS_ARCH_X86, CS_MODE_16
    ins = list(Cs(CS_ARCH_X86, CS_MODE_16).disasm(target.program_image[START:START+SIZE], START))
    need(sum(i.size for i in ins) == SIZE and [i.address-START for i in ins if i.mnemonic == 'nop'] == NOP_OFFSETS,
         'complete native instruction/NOP boundaries differ')
    negative = parse_mz((root/WORKS[2][1]/'source/units.exe').read_bytes()).program_image[START:START+SIZE]
    return dict(schema_version=1, kind='original-primary-source-master-circlex-proposal', decision='PROPOSAL',
                authored_credit=0, authored_denominator=None, base_proof_sha256=sha((root/BASE).read_bytes()),
                target_sha256=inherited['inputs']['target']['sha256'], start=START, size=SIZE,
                target_scope_sha256=TARGET_SCOPE_SHA, primary_inputs=PRIMARY, context_inputs=CONTEXT,
                data_context=context, source_flags=SOURCE_FLAGS,
                binding_inputs={path: sha((root/path).read_bytes()) for path in BINDINGS.values()},
                source_assembler_invocations=3, binding_assembler_invocations=6, linker_invocations=3,
                source_transformations=[], first_positive_retained_after_its_successful_new_build=True,
                native_instruction_count=len(ins), instruction_nop_offsets=NOP_OFFSETS, padding_bytes=3,
                ordered_mz_fixups=[], negative_changed_offsets=[i for i, (a, b) in enumerate(zip(
                    target.program_image[START:START+SIZE], negative)) if a != b],
                rounds=rounds, reviewer_sources=[dict(file=name, sha256=sha((root/name).read_bytes())) for name in SOURCES],
                limitations='One unchanged original GC_CIRCX module only; all 240 bytes, including three EVEN NOPs and five self-patched initial operands, compared literally. CLIP/GRP records anchor foreign symbols, granting no DATA credit. Not a historical game project, original assembler identity or whole executable match. Other circle/BSS owners remain unknown. Only empty binder dependency timestamps use existing metadata identity; no original CODE/object/MAP/MZ or relocation normalization. Zero authored credit.')


def validate_metadata(meta, *, root=ROOT):
    need(digest({k: v for k, v in meta.items() if k != 'reviewer_sources'}) == EVIDENCE_SHA,
         'frozen original source/producer evidence differs')
    need(meta['schema_version'] == 1 and meta['kind'] == 'original-primary-source-master-circlex-proposal' and
         meta['decision'] == 'PROPOSAL' and meta['authored_credit'] == 0 and meta['authored_denominator'] is None,
         'original vendor proof cannot grant authored credit')
    need(meta['base_proof_sha256'] == BASE_SHA == sha((root/BASE).read_bytes()), 'frozen base differs')
    need((meta['start'], meta['size'], meta['target_scope_sha256']) == (START, SIZE, TARGET_SCOPE_SHA) and
         meta['primary_inputs'] == PRIMARY and meta['context_inputs'] == CONTEXT and
         meta['source_flags'] == SOURCE_FLAGS and meta['source_transformations'] == [] and
         meta['padding_bytes'] == 3 and meta['ordered_mz_fixups'] == [] and
         meta['instruction_nop_offsets'] == NOP_OFFSETS, 'complete original source/unit policy differs')
    need(meta['reviewer_sources'] == [dict(file=name, sha256=sha((root/name).read_bytes())) for name in SOURCES],
         'reviewer source identity differs')
    need(meta['binding_inputs'] == {path: sha((root/path).read_bytes()) for path in BINDINGS.values()}, 'binding identity differs')
    base.validate_metadata(json.loads((root/BASE).read_text()), root=root)


def review_inputs(meta, *, root=ROOT):
    validate_metadata(meta, root=root)
    need(build_metadata(root=root) == meta, 'actual original producers/native context differs')
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
                    start=START, size=SIZE, procedure='GRCG_CIRCLE_X', authored_credit=0, authored_denominator=None)
    need(json.loads(path.read_text()) == expected, 'separate original-source vendor decision differs')
    need(views['main']['sha256'] == inherited['target_payload_sha256'], 'target payload differs')
    if verify_targets:
        review_inputs(meta, root=root)
    return [dict(start=START, end=START+SIZE, kind='verified-vendor-code',
                 library='master.lib 0.23 original source', member='GRCG_CIRCLE_X')], sha(path.read_bytes())


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
