#!/usr/bin/env python3
"""Review complete Borland string-library CODE; grant zero authored credit."""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path

import review_main_runtime as runtime
import review_vendor as vendor
from lib.pc98 import parse_mz
from lib.unit_context import UnitContext, load_unit_target

ROOT = Path(__file__).resolve().parents[1]
PROOF = 'config/string_runtime_ownership.json'
DECISION = 'config/reviewed_string_runtime_units.json'
NOTES = 'docs/reconstruction/STRING_RUNTIME_OWNERSHIP.md'
SCOPES = (
    ('ctor2', '_TEXT', 0xa73c, 96), ('ctor2', '_TEXTC', 0x1fd7a, 233),
    ('ctor3', '_TEXT', 0xa79c, 207), ('ctor3', '_TEXTC', 0x1fe63, 540),
    ('strings', '_TEXT', 0xa86b, 587), ('strings', '_TEXTC', 0x2007f, 2371),
)
MODEL = dict(calibration_start=0x1fd8d, native_start=0x1fd7a,
             calibration_frame=0x1fd80, native_frame=0x1fd70,
             linear_change=-19, frame_change=-16, offset_change=-3)
SOURCES = ('scripts/review_string_runtime.py', 'scripts/review_main_runtime.py',
           'scripts/review_vendor.py', 'scripts/review_vendor_data.py',
           'scripts/lib/borland_library.py', 'scripts/lib/omf.py', 'scripts/lib/pc98.py',
           'scripts/lib/unit_context.py', 'scripts/lib/unit_oracle.py',
           'scripts/lib/unit_extents.py', 'config/main_runtime_ownership.json',
           'config/reviewed_main_runtime_units.json', 'config/vendor_ownership.json',
           'config/vendor_data_ownership.json', 'config/reviewed_vendor_data_units.json',
           'config/cl_data_sources.json', 'config/targets.toml', 'config/toolchain.toml')
need, sha = vendor.need, vendor.sha


def identities(root):
    return {p: sha((root / p).read_bytes()) for p in SOURCES}


def translate(review, target):
    """Rebind symbols only; never change an object byte or target image."""
    native = runtime.translate_review(review, target, runtime.expected_model())
    need(native.segbases['_textc'] == MODEL['calibration_start'], 'string CODE base drift')
    native.segbases['_textc'] = MODEL['native_start']
    for con in native.contribs:
        if con['segment'].casefold() == '_textc':
            con['start'] += MODEL['linear_change']
            con['frame'] = MODEL['native_frame']
    old, new = MODEL['calibration_frame'], MODEL['native_frame']
    for name, rows in native.pubmap.items():
        native.pubmap[name] = {(new, off - 3) if frame == old else (frame, off)
                               for frame, off in rows}
    for name, rows in native.rawpub.items():
        native.rawpub[name] = [(new, off - 3, member) if frame == old else (frame, off, member)
                               for frame, off, member in rows]
    return native


def changed_frame(value):
    if value == runtime.expected_model()['calibration']['dgroup']:
        return runtime.expected_model()['native']['dgroup']
    return MODEL['native_frame'] if value == MODEL['calibration_frame'] else value


def validate_pair(left, right):
    for key in ('member', 'size', 'segment', 'class_name', 'SEGDEF', 'CODE_LEDATA',
                'member_program_sha256', 'original_unlinked_CODE_sha256',
                'complete_gapless_CODE_LEDATA', 'member_record_counts', 'ordered_MZ_fixups'):
        need(left[key] == right[key], 'string member/OMF/ordered relocation identity differs')
    delta = MODEL['linear_change'] if left['segment'] == '_TEXTC' else 0
    need(right['start'] == left['start'] + delta and right['end'] == left['end'] + delta,
         'string complete CODE translation differs')
    need(left['unique_original_occurrence'] is right['unique_original_occurrence'] is True,
         'string complete occurrence is not unique')
    need(len(left['fixup_actions']) == len(right['fixup_actions']), 'string fixup action count differs')
    for a, b in zip(left['fixup_actions'], right['fixup_actions']):
        need(all(a[k] == b[k] for k in runtime.STABLE_ACTION_FIELDS),
             'string original fixup action/order/transformation changed')
        for key in ('resolved_target_frame', 'resolved_frame'):
            need(b[key] == changed_frame(a[key]), 'unreviewed string fixup frame')
        wanted = a['resolved_target_offset']
        if a['resolved_target_frame'] == MODEL['calibration_frame']:
            wanted -= 3
        elif a['resolved_target_frame'] == runtime.expected_model()['calibration']['dgroup']:
            wanted = runtime.translated_offset(wanted, runtime.expected_model())
        need(b['resolved_target_offset'] == wanted, 'unreviewed string fixup offset')


def native_nops(image, evidence):
    """Every 90 byte is either a proven relaxation NOP or a reviewed nonopcode."""
    raw = image.program_image[evidence['start']:evidence['end']]
    nops = sorted(a['write_start'] for a in evidence['fixup_actions']
                  if a['operation'] == 'TLINK same-segment far-call NOP/PUSHCS/CALL')
    for off in nops:
        need(raw[off:off+3] == b'\x90\x0e\xe8', 'string relaxation NOP sequence differs')
    nonop = []
    if (evidence['member'], evidence['segment']) == ('ctor3', '_TEXTC'):
        need(raw[200] == 0xcb and raw[203] == 0x90, 'constructor return/embedded metadata differs')
        nonop = [dict(offset=203, role='embedded compiler metadata after constructor RETF at200')]
    if (evidence['member'], evidence['segment']) == ('strings', '_TEXT'):
        need(523 in nops and raw[526] == 0x90, 'string relaxed CALL operand differs')
        nonop = [dict(offset=526, role='relative CALL operand inside relaxation at523')]
    need([i for i, b in enumerate(raw) if b == 0x90] == sorted(nops + [r['offset'] for r in nonop]),
         'unreviewed string 90 byte')
    return dict(instruction_nop_offsets=nops, uncredited=True, nonopcode_90=nonop)


def native_review(root=ROOT):
    base = root / '.analysis/builds/main-calibration-b/source'
    paths = dict(library_sha256=root / '.analysis/toolchain/installed/tc40j/LIB/CL.LIB',
                 calibration_exe_sha256=base / 'bin/th05/main.exe',
                 calibration_map_sha256=base / 'obj/th05/main.map')
    raw = {k: p.read_bytes() for k, p in paths.items()}
    need(all(sha(v) == vendor.PINS[k] for k, v in raw.items()), 'pinned string library/calibration differs')
    _, target, _ = load_unit_target(UnitContext(root), UnitContext(root).config())
    need(sha(target.program_image) == vendor.PINS['target_payload_sha256'], 'native string view differs')
    cal = parse_mz(raw['calibration_exe_sha256'])
    control = vendor.VendorReview(raw['library_sha256'], raw['calibration_map_sha256'], cal, cal)
    # Reuse the independently verified CRT/DATA/BSS layout, including all eight anchors.
    data = json.loads((root / 'config/vendor_data_ownership.json').read_text())
    runtime.data_review.validate_metadata(data, root=root)
    need(runtime.binding_model(cal, target, control, data) == runtime.expected_model(),
         'string native DATA/BSS anchors differ')
    native = translate(control, target)
    rows, negatives = [], []
    for member, segment, start, size in SCOPES:
        con = [c for c in control.contribs if (c['module'].casefold(), c['segment'], c['cl']) ==
               (member, segment, 'CODE') and c['size']]
        need(len(con) == 1, 'missing/duplicate complete string CODE')
        nc = native.contribution(native.mods[member], next(i for i, s in enumerate(native.mods[member]['segs'])
                                 if s and s['name'] == segment))
        need((nc['start'], nc['size']) == (start, size), 'native complete string scope differs')
        left, right = control.verify(control.mods[member], con[0]), native.verify(native.mods[member], nc)
        validate_pair(left, right)
        rows.append(dict(member=member, segment=segment, calibration=left, native=right,
                         native_nops=native_nops(target, right)))
        mutant = copy.deepcopy(control.mods[member])
        si = next(i for i, s in enumerate(mutant['segs']) if s and s['name'] == segment)
        block = next(b for b in mutant['blocks'] if b['segment'] == si and b['offset'] == 0)
        need(not any(a['write_start'] == 0 for a in left['fixup_actions']), 'negative byte is a relocation')
        block['data'] = bytes([block['data'][0] ^ 1]) + block['data'][1:]
        try:
            control.verify(mutant, con[0])
        except ValueError as error:
            need('reconstructed OMF/link bytes differ (1 bytes)' in str(error), 'unexpected negative rejection')
        else:
            raise ValueError('string object-payload mutation was accepted')
        negatives.append(dict(member=member, segment=segment, offset=0, xor=1, rejected=True,
                              kind='decoded-distributed-OMF-model-mutation; no compilation'))
    anchors = []
    for rel in target.relocations:
        site = rel.linear
        if site >= 3 and target.program_image[site-3] == 0x9a:
            frame = int.from_bytes(target.program_image[site:site+2], 'little') * 16
            off = int.from_bytes(target.program_image[site-2:site], 'little')
            if frame == MODEL['native_frame'] and MODEL['native_start'] <= frame+off < 0x209c2:
                anchors.append(dict(call_site=site-3, frame=frame, offset=off, destination=frame+off))
    need(anchors and {0x1fd7a, 0x1fe63}.issubset({a['destination'] for a in anchors}),
         'native string constructor far-call anchors missing')
    result = dict(schema_version=1, kind='complete-distributed-string-runtime-CODE',
                  artifact='th05-main', authored_credit=0, authored_denominator=None,
                  compiler_invocations=0, inputs={k: vendor.PINS[k] for k in
                  (*paths, 'target_sha256', 'target_payload_sha256')}, identities=identities(root),
                  binding_model=MODEL, runtime_binding_model=runtime.expected_model(),
                  contributions=rows, negatives=negatives, native_far_call_anchors=anchors,
                  contribution_count=6, bytes=4034)
    validate_metadata(result, root=root)
    return result


def validate_metadata(meta, *, root=ROOT):
    need(type(meta.get('schema_version')) is int and meta['schema_version'] == 1
         and meta.get('kind') == 'complete-distributed-string-runtime-CODE'
         and meta.get('artifact') == 'th05-main' and type(meta.get('authored_credit')) is int
         and meta['authored_credit'] == 0 and meta.get('authored_denominator') is None
         and type(meta.get('compiler_invocations')) is int and meta['compiler_invocations'] == 0,
         'string origin/zero-credit policy differs')
    need(meta.get('inputs') == {k: vendor.PINS[k] for k in ('library_sha256', 'calibration_exe_sha256',
         'calibration_map_sha256', 'target_sha256', 'target_payload_sha256')}
         and meta.get('identities') == identities(root), 'string input/verifier identities differ')
    need(meta.get('binding_model') == MODEL and meta.get('runtime_binding_model') == runtime.expected_model(),
         'string binding model differs')
    rows = meta.get('contributions', [])
    need(meta.get('contribution_count') == len(rows) == 6 and meta.get('bytes') == 4034,
         'string complete contribution selection differs')
    for row, (member, segment, start, size) in zip(rows, SCOPES):
        need((row['member'], row['segment']) == (member, segment), 'string member selection differs')
        left, right = row['calibration'], row['native']
        validate_pair(left, right)
        for evidence in (left, right):
            need(evidence['member'] == member and evidence['segment'] == segment and
                 evidence['class_name'] == 'CODE' and evidence['size'] == size and
                 evidence['SEGDEF'] == dict(name=segment, cl='CODE', size=size, acbp=0x28)
                 and evidence['complete_gapless_CODE_LEDATA'] is True, 'string whole CODE SEGDEF differs')
            cursor = 0
            for block in sorted(evidence['CODE_LEDATA'], key=lambda b: b['offset']):
                need(type(block['size']) is int and block['size'] > 0 and block['offset'] == cursor,
                     'string CODE LEDATA gap/overlap')
                cursor += block['size']
            need(cursor == size, 'string CODE LEDATA incomplete')
            hashes = [evidence[k] for k in ('member_program_sha256', 'original_unlinked_CODE_sha256',
                                           'linked_CODE_sha256')]
            hashes += [b['sha256'] for b in evidence['CODE_LEDATA']]
            writes, ordered = set(), []
            for action in evidence['fixup_actions']:
                begin, count, site = action['write_start'], action['write_size'], action['site']
                need(type(begin) is type(count) is type(site) is int and count in (2, 4, 5)
                     and 0 <= begin < begin+count <= size and 0 <= site < size-1
                     and not writes.intersection(range(begin, begin+count)),
                     'string FIXUPP write overlaps or escapes CODE')
                writes.update(range(begin, begin+count))
                op = action['operation']
                if op == 'far-pointer16:16':
                    need(action['kind'] == 3 and count == 4 and begin == site, 'invalid string far pointer')
                    ordered.append(site+2)
                elif op == 'segment16':
                    need(action['kind'] == 2 and count == 2 and begin == site, 'invalid string segment word')
                    ordered.append(site)
                elif op == 'TLINK same-segment far-call NOP/PUSHCS/CALL':
                    need(action['kind'] == 3 and count == 5 and begin == site-1,
                         'invalid string relaxed call')
                else:
                    need(op in ('offset16', 'self-relative16') and action['kind'] == 1
                         and count == 2 and begin == site, 'invalid string offset fixup')
                hashes.append(action['expected_bytes_sha256'])
            need(evidence['ordered_MZ_fixups'] == ordered, 'string MZ order differs from OMF actions')
            need(all(isinstance(h, str) and len(h) == 64 and all(c in '0123456789abcdef' for c in h)
                     for h in hashes), 'malformed string byte digest')
            fixes = evidence['ordered_MZ_fixups']
            need(len(fixes) == len(set(fixes)) and all(type(x) is int and 0 <= x < size-1 for x in fixes),
                 'string relocation outside whole contribution')
        need((right['start'], right['end']) == (start, start+size), 'string native boundary differs')
        nops = row['native_nops']
        need(nops['instruction_nop_offsets'] == sorted(a['write_start'] for a in right['fixup_actions']
             if a['operation'] == 'TLINK same-segment far-call NOP/PUSHCS/CALL') and nops['uncredited'] is True,
             'string instruction NOP ownership differs')
        expected_nonop = []
        if (member, segment) == ('ctor3', '_TEXTC'):
            expected_nonop = [dict(offset=203, role='embedded compiler metadata after constructor RETF at200')]
        elif (member, segment) == ('strings', '_TEXT'):
            expected_nonop = [dict(offset=526, role='relative CALL operand inside relaxation at523')]
        need(nops['nonopcode_90'] == expected_nonop, 'string nonopcode 90 classification differs')
    need(meta.get('negatives') == [dict(member=m, segment=s, offset=0, xor=1, rejected=True,
         kind='decoded-distributed-OMF-model-mutation; no compilation') for m, s, _, _ in SCOPES],
         'string own model negatives missing')
    anchors = meta['native_far_call_anchors']
    need(isinstance(anchors, list) and anchors and len({a['call_site'] for a in anchors}) == len(anchors),
         'string native anchor duplication')
    for anchor in anchors:
        need(all(type(v) is int for v in anchor.values())
             and anchor['frame'] == MODEL['native_frame']
             and anchor['destination'] == anchor['frame'] + anchor['offset']
             and 0 <= anchor['call_site'] < 145958-4
             and MODEL['native_start'] <= anchor['destination'] < 0x209c2,
             'string native anchor frame/extent differs')
    need({0x1fd7a, 0x1fe63}.issubset({a['destination'] for a in anchors}),
         'string constructor anchors missing')
    return dict(contributions=6, bytes=4034, authored_credit=0, byte_proof_replayed=False)


def reviewed_claims(root, views, *, verify_targets=False):
    path = root / DECISION
    if not path.exists():
        return [], None
    raw = (root / PROOF).read_bytes()
    proof = json.loads(raw)
    validate_metadata(proof, root=root)
    decision = json.loads(path.read_text())
    need(decision == dict(schema_version=1, classification='third-party-library-code',
         artifact='th05-main', decision='ADOPT_ONLY_LISTED_CONTRIBUTIONS', evidence_sha256=sha(raw),
         scopes=[dict(member=m, segment=s, start=a, size=n) for m, s, a, n in SCOPES],
         authored_credit=0, authored_denominator=None, other_scopes_policy='unknown', notes=NOTES,
         notes_sha256=sha((root / NOTES).read_bytes())), 'string explicit adoption differs')
    need((views['main']['size'], views['main']['sha256']) == (145958, vendor.PINS['target_payload_sha256']),
         'string coordinate view differs')
    if verify_targets:
        need(native_review(root) == proof, 'native string object/fixup replay differs')
    return [dict(start=a, end=a+n, kind='verified-vendor-code', library='CL.LIB', member=m,
                 segment=s) for m, s, a, n in SCOPES], sha(path.read_bytes())


def main():
    p = argparse.ArgumentParser(description=__doc__)
    modes = p.add_mutually_exclusive_group(required=True)
    modes.add_argument('--write', action='store_true')
    modes.add_argument('--check', action='store_true')
    modes.add_argument('--structural-check', action='store_true')
    args = p.parse_args()
    if args.structural_check:
        print(json.dumps(validate_metadata(json.loads((ROOT / PROOF).read_text())), indent=2))
    else:
        result = native_review()
        if args.write:
            (ROOT / PROOF).write_text(json.dumps(result, indent=2) + '\n')
        else:
            need(json.loads((ROOT / PROOF).read_text()) == result, 'saved string evidence differs')
        print('PASS: six complete distributed CODE contributions /4034 bytes; zero authored credit')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
