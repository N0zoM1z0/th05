#!/usr/bin/env python3
"""Review complete native MAIN CL.LIB CODE with independently anchored DATA/BSS.

This replays distributed OMF, not authored source or a new compiler run. The
original target and saved calibration bytes are never edited or normalized.
"""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import struct

import review_vendor as legacy
import review_vendor_data as data_review
from lib.pc98 import parse_mz
from lib.omf import parse_omf
from lib.unit_context import UnitContext, load_unit_target

ROOT = Path(__file__).resolve().parents[1]
PROOF = 'config/main_runtime_ownership.json'
DECISION = 'config/reviewed_main_runtime_units.json'
CRT_SHA256 = '09fe156e5dceb4afa30235e8d9cf7a17a40a91ee646babe16b3286731eb429a2'
# Complete additional members only. Previously adopted31 members stay untouched.
SCOPES = {
    '_abort': (17896, 27), 'atexit': (18004, 49), 'errormsg': (18510, 42),
    'exit': (18552, 170), 'ioerror': (19065, 82), 'lseek': (19168, 45),
    'setupio': (20023, 164), 'toupper': (20187, 48), 'xxv': (20378, 649),
    'cputype': (21027, 92), 'fbrk': (22234, 352), '_pathops': (23414, 208),
    'flushall': (23864, 76), 'fseek': (23940, 492), 'fullpath': (24432, 834),
    'getenv': (25423, 112), 'srchenv': (25802, 71), 'srchstr': (25873, 322),
    'setvbuf': (26195, 289), 'write': (26811, 358), 'writea': (27169, 91),
    'xfflush': (27260, 63), 'xx': (28791, 12622), 'loadprog': (43702, 871),
}
RUNTIME_BSS = [('atexit', 128), ('sigdata', 4), ('xxv', 4), ('signal', 4), ('xx', 10)]
SOURCES = [
    'scripts/review_main_runtime.py', 'scripts/review_vendor.py',
    'scripts/review_vendor_data.py', 'scripts/lib/borland_library.py',
    'scripts/lib/omf.py', 'scripts/lib/pc98.py', 'scripts/lib/unit_context.py',
    'scripts/lib/unit_oracle.py', 'scripts/lib/targets.py', 'scripts/lib/unit_extents.py',
    'config/toolchain.toml', 'config/targets.toml',
    'config/vendor_ownership.json', 'config/vendor_data_ownership.json',
    'config/reviewed_vendor_data_units.json', 'config/cl_data_sources.json',
]
STABLE_ACTION_FIELDS = (
    'segment', 'site', 'kind', 'relative', 'frame_method', 'frame_index',
    'target_method', 'target_index', 'displacement', 'binding', 'operation',
    'write_start', 'write_size',
)


def need(value, message):
    if not value:
        raise ValueError(message)


def sha(raw):
    return legacy.sha(raw)


def identities(root):
    return {path: sha((root / path).read_bytes()) for path in SOURCES}


def startup(image):
    """Read the real C0 large-model DS, zeroing and initializer boundaries."""
    raw = image.program_image
    need(image.valid and image.header.initial_relative_cs == image.header.initial_ip == 0,
         'expected original large-model CRT entry')
    need(raw[:1] == b'\xba' and raw[0x14:0x16] == b'\x8e\xda' and
         raw[0x5d] == 0xbf and raw[0xa4] == 0xb8,
         'startup DGROUP instruction roles differ')
    word = lambda offset: struct.unpack_from('<H', raw, offset)[0]
    dgroup = word(1)
    need(word(0x5e) == word(0xa5) == dgroup, 'startup DGROUP anchors disagree')
    need(raw[0xb0:0xb6] == b'\x2e\x8e\x06\x6d\x02\xbf' and raw[0xb8] == 0xb9 and
         raw[0xbb:0xc0] == b'\x2b\xcf\xfc\xf3\xaa',
         'startup complete zeroing boundary roles differ')
    need(raw[0x11e] == raw[0x14d] == 0xbe and raw[0x121] == raw[0x150] == 0xbf,
         'startup initializer/exit boundaries differ')
    result = dict(dgroup=dgroup * 16, bss_start=word(0xb6), bss_end=word(0xb9),
                  init_start=word(0x11f), init_end=word(0x122),
                  exit_start=word(0x14e), exit_end=word(0x151))
    need(result['init_start'] < result['init_end'] == result['exit_start'] <
         result['exit_end'] == result['bss_start'] < result['bss_end'],
         'startup DATA/INIT/EXIT/BSS topology differs')
    sites = [rel.linear for rel in image.relocations]
    need(all(offset in sites for offset in (1, 0x5e, 0xa5)), 'DGROUP immediates lack real MZ relocations')
    # SS is a different native segment; it is never translated as DGROUP.
    result['initial_ss'] = image.header.initial_relative_ss
    return result


def crt_roles(raw):
    """Verify the pinned C0 OMF binds startup fields to real linker segments."""
    names, segments, groups, last, roles = [''], [None], [None], None, []
    expected = {0xb6: '_BSS', 0xb9: '_BSSEND', 0x11f: '_INIT_',
                0x122: '_INITEND_', 0x14e: '_EXIT_', 0x151: '_EXITEND_'}
    for record in parse_omf(raw):
        data = record.data
        if record.name == 'LNAMES':
            at = 0
            while at < len(data):
                size = data[at]; at += 1
                names.append(data[at:at+size].decode('ascii')); at += size
        elif record.name == 'SEGDEF':
            name, _ = legacy.idx(data, 3)
            segments.append(names[name])
        elif record.name == 'GRPDEF':
            name, _ = legacy.idx(data, 0)
            groups.append(names[name])
        elif record.name == 'LEDATA':
            segment, at = legacy.idx(data, 0)
            last = (segment, int.from_bytes(data[at:at+2], 'little'))
        elif record.name == 'FIXUPP':
            need(last is not None, 'CRT FIXUPP without LEDATA')
            at = 0
            while at < len(data):
                loc = data[at]
                need(loc & 128 and at+3 <= len(data), 'unsupported CRT thread/truncated FIXUPP')
                site = last[1] + ((loc & 3) << 8) + data[at+1]
                kind, relative, flags = (loc >> 2) & 15, not bool(loc & 64), data[at+2]
                at += 3
                need(not flags & 128 and not flags & 8, 'CRT threaded FIXUPP unsupported')
                frame, method = (flags >> 4) & 7, flags & 3
                if frame <= 2:
                    frame_index, at = legacy.idx(data, at)
                else:
                    need(frame in (4, 5), 'CRT absolute FIXUPP unsupported')
                    frame_index = None
                target_index, at = legacy.idx(data, at)
                displacement = 0
                if not flags & 4:
                    displacement = int.from_bytes(data[at:at+2], 'little'); at += 2
                if segments[last[0]] == '_TEXT' and site in expected:
                    need(kind == 1 and not relative and frame == 1 and
                         groups[frame_index] == 'DGROUP' and method == 0 and
                         segments[target_index] == expected[site] and displacement == 0,
                         'CRT startup field is not its reviewed BSS/initializer segment fixup')
                    roles.append(dict(site=site, target_segment=expected[site], frame='DGROUP'))
    need(len(roles) == len(expected) and len({row['site'] for row in roles}) == len(expected),
         'CRT startup segment-role fixups missing or duplicated')
    return sorted(roles, key=lambda row: row['site'])


def binding_model(control, target, review, data_proof):
    """Anchor one layout model; never solve individual CODE operands backwards."""
    before, after = startup(control), startup(target)
    need(before['dgroup'] == review.groups['dgroup'] == 0x209e0 and after['dgroup'] == 0x209d0,
         'native/calibration DGROUP identities differ')
    anchors = [row for row in data_proof['contributions'] if row['context'] == 'main']
    need(len(anchors) == 8 and {row['member'] for row in anchors} ==
         {'_abort', 'files2', 'ioerror', 'ctype', 'signal', 'xx', 'strings', 'loadprog'},
         'complete reviewed CL DATA anchor set differs')
    changes = set()
    for row in anchors:
        mod = review.mods[row['member']]
        indices = [i for i, seg in enumerate(mod['segs']) if seg and seg['cl'] == 'DATA' and seg['size']]
        need(len(indices) == 1, 'ambiguous anchor DATA SEGDEF')
        body, _ = data_review.data_template(mod, indices[0])
        need(sha(body) == row['data_sha256'] and len(body) == row['size'], 'anchor library DATA identity differs')
        data_review.unique_data_match(control, body, row['calibration_start'], before['dgroup'])
        data_review.unique_data_match(target, body, row['start'], after['dgroup'])
        changes.add((row['start'] - after['dgroup']) - (row['calibration_start'] - before['dgroup']))
    need(changes == {-18}, 'whole DATA anchors do not support one fixed offset translation')
    need(all(after[key] - before[key] == -18 for key in
             ('init_start', 'init_end', 'exit_start', 'exit_end', 'bss_start')),
         'independent startup DATA/INIT/EXIT anchors disagree with DATA objects')
    # The retained link's final ordinary BSS suffix consists of whole real
    # library SEGDEFs. Its end is independently read from the native CRT clear.
    cursor = before['bss_end'] - sum(size for _, size in RUNTIME_BSS)
    bss = []
    for name, size in RUNTIME_BSS:
        mod = review.mods[name]
        indices = [i for i, seg in enumerate(mod['segs']) if seg and seg['cl'] == 'BSS' and seg['size']]
        need(len(indices) == 1, 'ambiguous runtime BSS SEGDEF')
        con = review.contribution(mod, indices[0])
        need(mod['segs'][indices[0]]['acbp'] == 0x48 and con['size'] == size and
             con['start'] == before['dgroup'] + cursor, 'complete runtime BSS order/alignment differs')
        bss.append(dict(member=name, size=size, calibration_offset=cursor,
                        native_offset=cursor + after['bss_end'] - before['bss_end']))
        cursor += size
    need(cursor == before['bss_end'] and after['bss_end'] - before['bss_end'] == -20,
         'independent native BSS suffix end differs')
    return dict(kind='fixed-native-runtime-layout', calibration=before, native=after,
                data_offset_change=-18, bss_offset_change=-20,
                data_calibration_start=0x2098, data_calibration_end=before['bss_start'],
                bss_calibration_start=bss[0]['calibration_offset'],
                bss_calibration_end=before['bss_end'],
                data_anchor_ids=[row['id'] for row in anchors], bss_suffix=bss)


def expected_model():
    before = dict(dgroup=0x209e0, bss_start=0x262c, bss_end=0xc748,
                  init_start=0x2608, init_end=0x2626, exit_start=0x2626,
                  exit_end=0x262c, initial_ss=0x2d13)
    after = dict(dgroup=0x209d0, bss_start=0x261a, bss_end=0xc734,
                 init_start=0x25f6, init_end=0x2614, exit_start=0x2614,
                 exit_end=0x261a, initial_ss=0x2d11)
    return dict(kind='fixed-native-runtime-layout', calibration=before, native=after,
                data_offset_change=-18, bss_offset_change=-20,
                data_calibration_start=0x2098, data_calibration_end=0x262c,
                bss_calibration_start=0xc6b2, bss_calibration_end=0xc748,
                data_anchor_ids=['main-cl-data-' + name for name in
                    ('_abort', 'files2', 'ioerror', 'ctype', 'signal', 'xx', 'strings', 'loadprog')],
                bss_suffix=[dict(member=name, size=size, calibration_offset=off, native_offset=off-20)
                    for (name, size), off in zip(RUNTIME_BSS, (0xc6b2, 0xc732, 0xc736, 0xc73a, 0xc73e))])


def translated_offset(value, model):
    if model['bss_calibration_start'] <= value <= model['bss_calibration_end']:
        return value + model['bss_offset_change']
    if model['data_calibration_start'] <= value <= model['data_calibration_end']:
        return value + model['data_offset_change']
    return value


def translate_review(review, target, model):
    """Change symbol addresses only, retaining all distributed OMF and CODE."""
    native = copy.deepcopy(review)
    old, new = model['calibration']['dgroup'], model['native']['dgroup']

    offset = lambda value: translated_offset(value, model)

    native.groups['dgroup'] = new
    dgroup_segments = {con['segment'].casefold() for con in native.contribs
                        if con['group'].casefold() == 'dgroup'}
    for con in native.contribs:
        if con['group'].casefold() == 'dgroup':
            con['start'] = new + offset(con['start'] - old)
            con['frame'] = new
    for name, base in list(native.segbases.items()):
        if name in dgroup_segments:
            native.segbases[name] = new + offset(base - old)
    for name, rows in native.pubmap.items():
        native.pubmap[name] = {(new, offset(off)) if frame == old else (frame, off)
                               for frame, off in rows}
    for name, rows in native.rawpub.items():
        native.rawpub[name] = [(new, offset(off), member) if frame == old else (frame, off, member)
                               for frame, off, member in rows]
    # Legacy's second image is a byte oracle. Calibration is independently
    # reconstructed first; this view compares newly linked expected bytes
    # directly against the actual original, without editing either image.
    native.cal = native.target = target
    return native


def validate_pair(control, native, model=None):
    model = expected_model() if model is None else model
    for key in ('member', 'start', 'end', 'size', 'SEGDEF', 'CODE_LEDATA',
                'complete_gapless_CODE_LEDATA', 'member_program_sha256',
                'original_unlinked_CODE_sha256', 'member_record_counts', 'ordered_MZ_fixups'):
        need(control[key] == native[key], 'CODE ownership/coverage or ordered relocation identity changed')
    need(control['unique_original_occurrence'] is native['unique_original_occurrence'] is True,
         'complete runtime contribution must occur uniquely')
    need(len(control['fixup_actions']) == len(native['fixup_actions']), 'FIXUPP action count differs')
    for left, right in zip(control['fixup_actions'], native['fixup_actions']):
        need(all(left[key] == right[key] for key in STABLE_ACTION_FIELDS),
             'OMF fixup identity/order or real linker transformation changed')
        for key in ('resolved_target_frame', 'resolved_frame'):
            before = left[key]
            after = model['native']['dgroup'] if before == model['calibration']['dgroup'] else before
            need(right[key] == after, 'runtime resolved frame leaves the reviewed binding model')
        wanted = (translated_offset(left['resolved_target_offset'], model)
                  if left['resolved_target_frame'] == model['calibration']['dgroup']
                  else left['resolved_target_offset'])
        need(right['resolved_target_offset'] == wanted,
             'runtime target offset leaves the reviewed DATA/BSS binding model')



def native_review(root=ROOT):
    base = root / '.analysis/builds/main-calibration-b/source'
    paths = {'library_sha256': root / '.analysis/toolchain/installed/tc40j/LIB/CL.LIB',
             'calibration_exe_sha256': base / 'bin/th05/main.exe',
             'calibration_map_sha256': base / 'obj/th05/main.map'}
    raw = {key: path.read_bytes() for key, path in paths.items()}
    crt = (root / '.analysis/toolchain/installed/tc40j/LIB/C0L.OBJ').read_bytes()
    need(sha(crt) == CRT_SHA256, 'pinned real CRT object differs')
    roles = crt_roles(crt)
    need(all(sha(value) == legacy.PINS[key] for key, value in raw.items()), 'pinned private library/link input changed')
    context = UnitContext(root)
    artifact, target, _ = load_unit_target(context, context.config())
    need(artifact['sha256'] == legacy.PINS['target_sha256'] and
         sha(target.program_image) == legacy.PINS['target_payload_sha256'], 'native original identity changed')
    control_image = parse_mz(raw['calibration_exe_sha256'])
    need(control_image.valid, 'retained calibration MZ is invalid')
    control = legacy.VendorReview(raw['library_sha256'], raw['calibration_map_sha256'], control_image, control_image)
    data = json.loads((root / data_review.PROOF).read_text())
    data_review.validate_metadata(data, root=root)
    model = binding_model(control_image, target, control, data)
    need(model == expected_model(), 'native complete binding model drift')
    native = translate_review(control, target, model)
    rows = []
    for name, (start, size) in SCOPES.items():
        cons = [con for con in control.contribs if con['module'].casefold() == name and con['cl'] == 'CODE' and con['size']]
        need(len(cons) == 1 and (cons[0]['start'], cons[0]['size']) == (start, size), 'complete runtime CODE boundary changed')
        left = control.verify(control.mods[name], cons[0])
        right = native.verify(native.mods[name], cons[0])
        validate_pair(left, right)
        rows.append(dict(member=name, calibration=left, native=right))
    result = dict(schema_version=1, kind='native-main-cl-runtime-code-ownership-proposal',
                  artifact='th05-main', decision='PROPOSAL', authored_credit=0,
                  authored_denominator=None, compiler_invocations=0, byte_proof_replayed=True,
                  inputs={**{key: legacy.PINS[key] for key in (*paths, 'target_sha256', 'target_payload_sha256')},
                          'crt_sha256': CRT_SHA256}, crt_segment_roles=roles,
                  identities=identities(root), binding_model=model, contributions=rows,
                  contribution_count=len(rows), bytes=sum(size for _, size in SCOPES.values()))
    validate_metadata(result, root=root)
    return result


def validate_metadata(meta, *, root=ROOT):
    need(type(meta.get('schema_version')) is int and meta['schema_version'] == 1 and
         meta.get('kind') == 'native-main-cl-runtime-code-ownership-proposal' and
         meta.get('artifact') == 'th05-main' and meta.get('decision') == 'PROPOSAL' and
         type(meta.get('authored_credit')) is int and meta['authored_credit'] == 0 and
         meta.get('authored_denominator') is None and
         type(meta.get('compiler_invocations')) is int and meta['compiler_invocations'] == 0 and
         meta.get('byte_proof_replayed') is True, 'runtime proposal origin/credit policy changed')
    need(meta.get('identities') == identities(root), 'runtime verifier/dependency identity drift')
    need(meta.get('inputs') == {**{key: legacy.PINS[key] for key in
         ('library_sha256', 'calibration_exe_sha256', 'calibration_map_sha256', 'target_sha256', 'target_payload_sha256')},
         'crt_sha256': CRT_SHA256},
         'runtime target/library/calibration pin drift')
    need(meta.get('crt_segment_roles') == [dict(site=site, target_segment=name, frame='DGROUP')
         for site, name in ((0xb6, '_BSS'), (0xb9, '_BSSEND'), (0x11f, '_INIT_'),
                           (0x122, '_INITEND_'), (0x14e, '_EXIT_'), (0x151, '_EXITEND_'))],
         'real CRT segment-role evidence differs')
    rows = meta.get('contributions')
    need(isinstance(rows, list) and len(rows) == len(SCOPES) and
         {row.get('member') for row in rows} == set(SCOPES) and
         meta.get('contribution_count') == len(SCOPES) and meta.get('bytes') == 18129,
         'runtime proposal requires exactly the complete reviewed members')
    model = meta.get('binding_model', {})
    need(model == expected_model(), 'runtime native DATA/BSS binding model changed')
    for row in rows:
        left, right = row['calibration'], row['native']
        validate_pair(left, right, model)
        start, size = SCOPES[row['member']]
        need(right['member'] == row['member'] and right['start'] == start and right['size'] == size and
             right['end'] == start + size and right['class_name'] == 'CODE' and
             right['segment'] == '_TEXT' and right['SEGDEF']['size'] == size and
             right['complete_gapless_CODE_LEDATA'] is True, 'runtime complete CODE boundary/coverage changed')
        for evidence in (left, right):
            need(evidence.get('status') == 'proven-complete-vendor-CODE-proposal' and
                 evidence['SEGDEF'] == dict(name='_TEXT', cl='CODE', size=size, acbp=0x28),
                 'runtime ordinary CODE segment identity differs')
            cursor = 0
            for block in sorted(evidence['CODE_LEDATA'], key=lambda block: block['offset']):
                need(type(block['offset']) is int and type(block['size']) is int and
                     block['offset'] == cursor and block['size'] > 0,
                     'runtime CODE LEDATA gap/overlap')
                cursor += block['size']
            need(cursor == size, 'runtime incomplete CODE LEDATA coverage')
            hashes = [evidence[key] for key in ('member_program_sha256',
                      'original_unlinked_CODE_sha256', 'linked_CODE_sha256')]
            hashes += [block['sha256'] for block in evidence['CODE_LEDATA']]
            hashes += [action['expected_bytes_sha256'] for action in evidence['fixup_actions']]
            need(all(isinstance(value, str) and len(value) == 64 and
                     all(c in '0123456789abcdef' for c in value) for value in hashes),
                 'runtime full byte identity digest malformed')
            fixups = evidence['ordered_MZ_fixups']
            need(isinstance(fixups, list) and len(set(fixups)) == len(fixups) and
                 all(type(site) is int and 0 <= site < size-1 for site in fixups),
                 'runtime ordered MZ relocation extent differs')
            writes = set()
            for action in evidence['fixup_actions']:
                begin, count = action['write_start'], action['write_size']
                need(type(begin) is int and type(count) is int and count in (2, 4, 5) and
                     0 <= begin < begin+count <= size and not writes.intersection(range(begin, begin+count)),
                     'runtime overlapping/outside FIXUPP writes')
                writes.update(range(begin, begin+count))

    return dict(kind=meta['kind'], contribution_count=len(rows), bytes=18129,
                byte_proof_replayed=False, authored_credit=0, authored_denominator=None)


def reviewed_claims(root, views, *, verify_targets=False):
    path = root / DECISION
    if not path.exists():
        return [], None
    proof_bytes = (root / PROOF).read_bytes()
    proof = json.loads(proof_bytes)
    validate_metadata(proof, root=root)
    decision = json.loads(path.read_text())
    need(type(decision.get('schema_version')) is int and type(decision.get('authored_credit')) is int and
         decision == dict(schema_version=1, decision='ADOPT_ONLY_LISTED_MEMBERS',
         classification='third-party-library-code', artifact='th05-main',
         evidence_sha256=sha(proof_bytes), members=list(SCOPES), authored_credit=0,
         authored_denominator=None, other_scopes_policy='unknown',
         notes='docs/reconstruction/MAIN_RUNTIME_OWNERSHIP.md'), 'runtime explicit adoption decision differs')
    need((views['main']['size'], views['main']['sha256']) ==
         (145958, legacy.PINS['target_payload_sha256']), 'runtime ownership coordinate view differs')
    if verify_targets:
        need(native_review(root) == proof, 'native runtime byte/fixup replay disagrees')
    return [dict(start=start, end=start+size, kind='verified-vendor-code',
                 library='CL.LIB', member=name) for name, (start, size) in SCOPES.items()], sha(path.read_bytes())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--write', action='store_true')
    modes.add_argument('--check', action='store_true')
    modes.add_argument('--structural-check', action='store_true')
    args = parser.parse_args()
    path = ROOT / PROOF
    if args.structural_check:
        result = validate_metadata(json.loads(path.read_text()))
    else:
        result = native_review()
        rendered = json.dumps(result, indent=2) + '\n'
        if args.write:
            path.write_text(rendered)
        else:
            need(path.read_text() == rendered, 'runtime proposal is stale')
        result = {key: result[key] for key in ('kind', 'contribution_count', 'bytes', 'authored_credit', 'authored_denominator')}
        result['byte_proof_replayed'] = True
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
