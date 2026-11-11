#!/usr/bin/env python3
"""Original Borland C++ string CODE for the OP/MAINE link contexts.

Use the real CL.LIB OMF LEDATA, FIXUPP, and retained calibration MAP.
OP uses identical native positions. MAINE shifts the C++ _TEXTC segment
six bytes later and its DGROUP 16 bytes later, as independently established
by the source-backed original MAINE linker-frame review. The original
six preceding bytes are not part of any claimed library CODE segment.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

from lib.pc98 import digest_file
from review_context_reserved import native_context
from review_maine_shifted_vendor import actual_link_frames
from review_vendor import need
from review_vendor_context import PINS

ROOT = Path(__file__).resolve().parents[1]
MEMBERS = ('ctor2', 'ctor3', 'strings')
SEGMENTS = ('_TEXT', '_TEXTC')
SIZES = {'ctor2': (96, 233), 'ctor3': (207, 540), 'strings': (587, 2371)}
# OP's three _TEXT contributions were adopted by the earlier library review.
# Never re-adopt or double-count them.
ADOPTED = {'op': (('_TEXTC', 'ctor2'), ('_TEXTC', 'ctor3'), ('_TEXTC', 'strings')),
           'maine': tuple((seg, name) for name in MEMBERS for seg in SEGMENTS)}
MAINE_TEXTC_DELTA = 6
MAINE_DGROUP_DELTA = 16


def proof_path(name):
    return ROOT / f'config/context_string_runtime.{name}.json'


def decision_path(name):
    return ROOT / f'config/reviewed_context_string_runtime.{name}.json'


def scope(review, name, segment):
    rows = [x for x in review.contribs
            if x['module'].casefold() == name and x['segment'] == segment
            and x['cl'] == 'CODE']
    need(len(rows) == 1 and rows[0]['size'] == SIZES[name][SEGMENTS.index(segment)],
         'original complete class-library source segment missing')
    return rows[0]


def translated_view(name, review):
    if name == 'op':
        return review
    need(name == 'maine', 'unsupported Borland string context')
    methods = actual_link_frames(review)
    need(len(methods) == 3 and
         all(row['original_entry'] == row['calibration_entry'] + MAINE_TEXTC_DELTA
             for row in methods.values()),
         'original C++ method entry anchors do not establish the six-byte shift')
    original_group = review.groups['dgroup']
    class_frame = review.segbases['_textc'] // 16 * 16
    native = copy.deepcopy(review)
    native.cal = native.target
    native.groups['dgroup'] += MAINE_DGROUP_DELTA
    native.segbases['_textc'] += MAINE_TEXTC_DELTA
    for row in native.contribs:
        if row['cl'] == 'CODE' and row['segment'].casefold() == '_textc':
            row['start'] += MAINE_TEXTC_DELTA
        if row['group'].casefold() == 'dgroup':
            row['start'] += MAINE_DGROUP_DELTA
            row['frame'] += MAINE_DGROUP_DELTA
    for symbol, rows in native.pubmap.items():
        native.pubmap[symbol] = {
            (f + MAINE_DGROUP_DELTA if f == original_group else f,
             off + MAINE_TEXTC_DELTA if f == class_frame else off)
            for f, off in rows}
    for symbol, rows in native.rawpub.items():
        native.rawpub[symbol] = [
            (f + MAINE_DGROUP_DELTA if f == original_group else f,
             off + MAINE_TEXTC_DELTA if f == class_frame else off, member)
            for f, off, member in rows]
    return native


def replay(name):
    need(name in ADOPTED, 'unsupported original string-library context')
    original, pin = native_context(name)
    calibrated = copy.copy(original)
    calibrated.target = calibrated.cal
    shifted = translated_view(name, original)
    if name == 'op':
        shifted = copy.copy(original)
        shifted.cal = shifted.target
    scopes = []
    for member in MEMBERS:
        mod = original.mods[member]
        for segment in SEGMENTS:
            c = scope(calibrated, member, segment)
            native = scope(shifted, member, segment)
            first = calibrated.verify(mod, c)
            second = shifted.verify(mod, native)
            need((first['member_program_sha256'], first['original_unlinked_CODE_sha256'],
                  first['CODE_LEDATA'], first['ordered_MZ_fixups']) ==
                 (second['member_program_sha256'], second['original_unlinked_CODE_sha256'],
                  second['CODE_LEDATA'], second['ordered_MZ_fixups']),
                 'native original and calibrated class source/relocation disagrees')
            need(len(first['fixup_actions']) == len(second['fixup_actions']) and
                 [(f['site'], f['kind'], f['operation'], f['binding'])
                  for f in first['fixup_actions']] ==
                 [(f['site'], f['kind'], f['operation'], f['binding'])
                  for f in second['fixup_actions']],
                 'original C++ library OMF FIXUPP order or target changed')
            scopes.append({
                'member': member, 'segment': segment, 'size': second['size'],
                'native_start': second['start'], 'native_end': second['end'],
                'original_member_sha256': second['member_program_sha256'],
                'object_CODE_sha256': second['original_unlinked_CODE_sha256'],
                'linked_original_CODE_sha256': second['linked_CODE_sha256'],
                'linked_calibrated_CODE_sha256': first['linked_CODE_sha256'],
                'ordered_native_MZ_fixups': second['ordered_MZ_fixups'],
                'CODE_LEDATA': second['CODE_LEDATA'],
                'ordered_OMF_actions': [
                    {'site': f['site'], 'kind': f['kind'],
                     'operation': f['operation'], 'binding': f['binding'],
                     'write_start': f['write_start'], 'write_size': f['write_size']}
                    for f in second['fixup_actions']],
                'authored_credit': 0,
            })
    selected = [s for s in scopes if (s['segment'], s['member']) in ADOPTED[name]]
    return {
        'schema_version': 1, 'artifact': 'th05-' + name,
        'kind': 'original-CL-CXX-string-CODE-records',
        'context': name, 'original_payload_sha256': pin['payload'],
        'original_packed_sha256': pin['packed'],
        'calibration_map_sha256': pin['calibration_map'],
        'calibration_exe_sha256': pin['calibration_exe'],
        'original_textc_linear_shift': MAINE_TEXTC_DELTA if name == 'maine' else 0,
        'original_dgroup_linear_shift': MAINE_DGROUP_DELTA if name == 'maine' else 0,
        'scopes': scopes, 'source_verified_CODE_bytes': sum(s['size'] for s in scopes),
        'newly_selected_CODE_bytes': sum(s['size'] for s in selected),
        'selected_scopes': [[s['segment'], s['member']] for s in selected],
        'verifier_sha256': digest_file(ROOT / 'scripts/review_context_string_runtime.py'),
        'library_parser_sha256': digest_file(ROOT / 'scripts/review_vendor.py'),
        'native_view_sha256': digest_file(ROOT / 'scripts/review_context_reserved.py'),
        'original_frame_model_sha256': digest_file(ROOT / 'scripts/review_maine_shifted_vendor.py'),
        'authored_credit': 0, 'other_source_bytes_claimed': 0,
    }


def validate_public(record, name):
    need(name in ADOPTED and record.get('schema_version') == 1 and
         record.get('kind') == 'original-CL-CXX-string-CODE-records' and
         record.get('context') == name and record.get('artifact') == 'th05-' + name and
         record.get('original_payload_sha256') == PINS[name]['payload'] and
         record.get('original_packed_sha256') == PINS[name]['packed'] and
         record.get('calibration_map_sha256') == PINS[name]['calibration_map'] and
         record.get('calibration_exe_sha256') == PINS[name]['calibration_exe'] and
         record.get('original_textc_linear_shift') ==
         (MAINE_TEXTC_DELTA if name == 'maine' else 0) and
         record.get('original_dgroup_linear_shift') ==
         (MAINE_DGROUP_DELTA if name == 'maine' else 0) and
         record.get('verifier_sha256') == digest_file(ROOT/'scripts/review_context_string_runtime.py') and
         record.get('library_parser_sha256') == digest_file(ROOT/'scripts/review_vendor.py') and
         record.get('native_view_sha256') == digest_file(ROOT/'scripts/review_context_reserved.py') and
         record.get('original_frame_model_sha256') == digest_file(ROOT/'scripts/review_maine_shifted_vendor.py') and
         record.get('authored_credit') == record.get('other_source_bytes_claimed') == 0,
         'original string source/verifier/target identity changed')
    items = record.get('scopes')
    need(isinstance(items,list) and len(items) == 6 and
         [(r.get('segment'),r.get('member')) for r in items] ==
         [(seg,member) for member in MEMBERS for seg in SEGMENTS],
         'source-linked string segment list has changed')
    for item in items:
        size = SIZES[item['member']][SEGMENTS.index(item['segment'])]
        need(item.get('size') == size and item.get('native_end') == item.get('native_start') + size and
             item.get('authored_credit') == 0 and
             sum(b.get('size',0) for b in item.get('CODE_LEDATA',[])) == size and
             len(item.get('ordered_OMF_actions',[])) > 0 and
             isinstance(item.get('ordered_native_MZ_fixups'), list),
             'original complete string source CODE/FIXUPP record incomplete')
        for key in ('original_member_sha256','object_CODE_sha256',
                    'linked_original_CODE_sha256','linked_calibrated_CODE_sha256'):
            digest = item.get(key)
            need(isinstance(digest,str) and len(digest)==64 and
                 all(x in '0123456789abcdef' for x in digest),
                 'original vendor source or linked digest invalid')
        need([a['site'] for a in item['ordered_OMF_actions']] ==
             [a['site'] for a in item['ordered_OMF_actions'] if
              isinstance(a.get('site'),int) and a['site']>=0],
             'invalid original OMF source site')
        rels = [a['site'] if a['kind']==2 else a['site']+2
                for a in item['ordered_OMF_actions']
                if a['operation'] in ('segment16','far-pointer16:16')]
        need(item['ordered_native_MZ_fixups'] == rels,
             'original ordered linked relocation differs from source')
    selected = [r for r in items if (r['segment'],r['member']) in ADOPTED[name]]
    need(record.get('selected_scopes') == [[r['segment'],r['member']] for r in selected] and
         record.get('source_verified_CODE_bytes') == 4034 and
         record.get('newly_selected_CODE_bytes') == sum(r['size'] for r in selected),
         'original string source/adoption extents changed')
    if decision_path(name).exists():
        d=json.loads(decision_path(name).read_text())
        need(d.get('schema_version')==1 and d.get('artifact')=='th05-'+name and
             d.get('decision')=='ADOPT_ONLY_PREVIOUSLY_UNKNOWN_COMPLETE_CODE' and
             d.get('evidence_sha256')==digest_file(proof_path(name)) and
             d.get('selected_scopes')==record['selected_scopes'] and
             d.get('CODE_bytes')==record['newly_selected_CODE_bytes'] and
             d.get('authored_credit')==d.get('other_source_bytes_claimed')==0,
             'explicit original string CODE decision missing or stale')


def reviewed_claims(root,name,view,*,verify_targets=False):
    if name not in ADOPTED or not decision_path(name).exists():
        return [],None
    need(root.resolve()==ROOT.resolve(),'wrong target-source checkout')
    record=json.loads(proof_path(name).read_text())
    validate_public(record,name)
    need(view['sha256']==record['original_payload_sha256'],
         'string library target payload identity mismatched')
    if verify_targets:
        need(replay(name)==record,'real original string source/target replay changed')
    return ([{'start':r['native_start'],'end':r['native_end'],
              'kind':'verified-vendor-code','member':r['member']+'/'+r['segment'],
              'library':'CL.LIB','authored_credit':0}
             for r in record['scopes']
             if (r['segment'],r['member']) in ADOPTED[name]],
            digest_file(decision_path(name)))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--context',choices=ADOPTED,required=True)
    modes=p.add_mutually_exclusive_group(required=True)
    modes.add_argument('--write',action='store_true')
    modes.add_argument('--check',action='store_true')
    modes.add_argument('--structural-check',action='store_true')
    args=p.parse_args()
    proof=proof_path(args.context)
    if args.write:
        need(not proof.exists() and not decision_path(args.context).exists(),
             'refusing overwrite of original source evidence')
        result=replay(args.context)
        proof.write_text(json.dumps(result,indent=2)+'\n')
        print('PASS: ',args.context,'original string class CODE:',
              result['source_verified_CODE_bytes'],'reviewed,',
              result['newly_selected_CODE_bytes'],'previously unknown')
    else:
        result=json.loads(proof.read_text())
        validate_public(result,args.context)
        if args.check:
            need(replay(args.context)==result,'source-linked native string evidence differs')
            print('PASS: native source and original ordered MZ relocations:',args.context)
        else:print('PASS: source-current string class CODE:',args.context)


if __name__=='__main__':
    main()
