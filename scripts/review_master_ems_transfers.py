#!/usr/bin/env python3
"""Two source-backed EMS transfer wrappers; five fixed private frame equates.

Keep the literal-source and EGC proofs unchanged. No instructions, constants,
comments or linked bytes are rewritten. This vendor review grants no authored
credit and does not establish the global denominator.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re

import review_master as base
from lib.omf import parse_omf
from lib.pc98 import parse_mz

ROOT = Path(__file__).resolve().parents[1]
PROOF = 'config/master_ems_transfers_ownership.json'
DECISION = 'config/reviewed_master_ems_transfers.json'
BASE = 'config/master_vendor_ownership.json'
BASE_SHA = '8b5e9b31ce345df277a31348d49aec9197e4c5c390eec0b9f812516c8287010a'
EVIDENCE_SHA = '6b03412ccef6890883e11e74367bd0aac287b5b5182ff0f4deb4de7fe60b2cbd'
SOURCES = ['scripts/review_master_ems_transfers.py', 'scripts/review_master.py',
           'scripts/lib/omf.py', 'scripts/lib/pc98.py']
SCOPES = [('READ', 0x3f6a, 0x3fcc), ('WRITE', 0x406c, 0x40ce)]
FRAME = {'handle': '(RETSIZE+7)*2', 'offs': '(RETSIZE+5)*2',
         'mem': '(RETSIZE+3)*2', 'len': '(RETSIZE+1)*2', 'block': '-18'}
RENAMES = {name: '@@'+name for name in FRAME}
OCCURRENCES = {'handle': 2, 'offs': 3, 'mem': 3, 'len': 3, 'block': 12}
TOKEN = re.compile(r'(?<![\w@$?])[A-Za-z_@$?][\w@$?]*')
CALLEES = {'EMS_MOVEMEMORYREGION': 0x403c, 'EMS_ENABLEPAGEFRAME': 0x3ff2}


def need(value, message):
    if not value:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def rename_frame_equates(text):
    """Only the five one-definition, fixed-expression frame symbols may change."""
    definitions = {name: [] for name in FRAME}
    identifiers, counts, lines = set(), dict.fromkeys(FRAME, 0), []
    for line in text.split('\n'):
        code = line.split(';', 1)[0]
        need('"' not in code and "'" not in code, 'quoted code is outside this frame proof')
        identifiers.update(TOKEN.findall(code))
        for name, expression in FRAME.items():
            match = re.fullmatch(r'\s*'+name+r'\s*=\s*(.*?)\s*', code)
            if match:
                definitions[name].append(match[1])
        lines.append(line)
    need(all(definitions[name] == [expression] for name, expression in FRAME.items()),
         'exactly one fixed frame-equate definition required for each private name')
    need(not set(RENAMES.values()) & identifiers, 'private destination collides with original source')
    result = []
    for line in lines:
        code, marker, comment = line.partition(';')
        def replace(match):
            name = match[0]
            if name in counts:
                counts[name] += 1
            return RENAMES.get(name, name)
        result.append(TOKEN.sub(replace, code) + marker + comment)
    need(counts == OCCURRENCES, 'fixed definition/reference occurrence inventory differs')
    return '\n'.join(result), counts


def verify_frame_equivalence(original, candidate):
    transformed, counts = rename_frame_equates(original)
    need(transformed == candidate, 'complete source differs beyond five private frame names')
    return counts


def digest(meta):
    return sha(json.dumps(meta, sort_keys=True, separators=(',', ':')).encode())


def validate_metadata(meta, *, root=ROOT):
    # Exclude the verifier's own hash list from this fixed observation digest;
    # the separate adoption pins the complete proof, including those hashes.
    need(digest({k: v for k, v in meta.items() if k != 'reviewer_sources'}) == EVIDENCE_SHA,
         'frozen two-procedure evidence differs')
    need(meta['schema_version'] == 1 and meta['kind'] == 'source-backed-master-ems-transfer-proposal',
         'proof schema differs')
    need(meta['decision'] == 'PROPOSAL' and meta['authored_credit'] == 0 and
         meta['authored_denominator'] is None and meta['compiler_invocations'] == 0,
         'vendor proof cannot grant source credit')
    need(sha((root / BASE).read_bytes()) == meta['base_proof_sha256'] == BASE_SHA,
         'frozen original proof differs')
    need(meta['full_bytes'] == meta['nonpadding_bytes'] == 196 and meta['padding_bytes'] == 0,
         'whole vendor accounting differs')
    need(len(meta['procedures']) == 2, 'exactly two complete procedures required')
    for row, (direction, start, end) in zip(meta['procedures'], SCOPES):
        need((row['name'], row['start'], row['end'], row['size']) ==
             ('EMS_'+direction, start, end, end-start), 'complete procedure boundary differs')
        need(row['candidate_file'] == 'libs/master.lib/ems_'+direction.lower()+'.asm' and
             row['upstream_file'] == 'EMS'+direction+'.ASM', 'source owner differs')
        need(row['renames'] == RENAMES and row['frame_equates'] == FRAME and
             row['rename_occurrences'] == OCCURRENCES, 'unreviewed frame-symbol substitution')
        need(row['distance'] == 'far-by-large-model' and not row['inline_data'] and
             row['ordered_mz_fixups'] == row['object_link_actions'] == row['padding'] ==
             row['instruction_nop_offsets'] == [], 'native/link/data/padding context differs')
        need(row['instruction_count'] == 40 and row['return_kind'] == 'retf' and
             row['return_cleanup'] == 14 and row['return_offset'] == 95,
             'far Pascal frame or full native decode differs')
        need(row['calls'] == [{'offset': 80, 'target': 0x403c}, {'offset': 88, 'target': 0x3ff2}],
             'actual common-code far-call context differs')
    need(meta['reviewer_sources'] == [dict(file=name, sha256=sha((root/name).read_bytes()))
         for name in SOURCES], 'reviewer source identity differs')
    base.validate_metadata(json.loads((root / BASE).read_text()), root=root)


def native_observations(raw, start):
    from capstone import Cs, CS_ARCH_X86, CS_MODE_16
    ins = list(Cs(CS_ARCH_X86, CS_MODE_16).disasm(raw, start))
    need(sum(i.size for i in ins) == len(raw), 'native decode incomplete')
    returns = [i for i in ins if i.mnemonic.startswith('ret')]
    need(len(returns) == 1 and returns[0].mnemonic == 'retf' and returns[0].op_str == '0xe',
         'native RETF14 differs')
    starts, calls = {i.address for i in ins}, []
    for index, i in enumerate(ins):
        if i.mnemonic.startswith('j'):
            need(int(i.op_str, 16) in starts, 'native branch escapes instruction boundaries')
        if i.mnemonic.startswith('call'):
            need(i.mnemonic == 'call' and i.size == 3 and index > 0 and
                 ins[index-1].mnemonic == 'push' and ins[index-1].op_str == 'cs' and
                 ins[index-1].address+1 == i.address, 'expected actual PUSH CS/near CALL pair')
            calls.append(dict(offset=i.address-start, target=int(i.op_str, 16)))
    return dict(instruction_count=len(ins), instruction_nop_offsets=[i.address-start for i in ins if i.mnemonic == 'nop'],
                return_kind='retf', return_cleanup=14, return_offset=returns[0].address-start, calls=calls)


def build_metadata(*, root=ROOT):
    inherited = json.loads((root / BASE).read_text())
    # Reuse, but fully re-read, the primary archive/source/macro/OMF/link proof.
    base.review_inputs(inherited, root=root)
    raw = {key: base.pinned(root, value) for key, value in inherited['inputs'].items()}
    upstream = base.stored_lzh(raw['inner_archive'])
    active = base.listing_procedures(raw['listing'])
    original, linked = parse_mz(raw['target']), parse_mz(raw['calibration_exe'])
    obj = base.object_text(raw['saved_object'])
    publics = [r.data for r in parse_omf(raw['saved_object']) if r.name == 'PUBDEF']
    for name, start in CALLEES.items():
        need(len([p for p in inherited['procedures'] if p['name'] == name and p['start'] == start]) == 1,
             'common-code helper context lacks inherited source/native proof')
    rows = []
    for direction, start, end in SCOPES:
        name, source, upstream_name = 'EMS_'+direction, 'libs/master.lib/ems_'+direction.lower()+'.asm', 'EMS'+direction+'.ASM'
        procedures = [p for p in active if p['name'] == name and p['local_start']+0x272 == start]
        need(len(procedures) == 1, 'unique complete active listing procedure required')
        proc = procedures[0]
        need(proc['local_end']+0x272 == end and not proc['inline_data'] and not proc['padding'] and
             proc['source'] == source, 'complete listing boundary/owner/data differs')
        candidate = (root / inherited['candidate_source_root'] / source).read_bytes()
        originals = [b for b in base.source_blocks(upstream[upstream_name], 'cp932') if b['name'] == name]
        candidates = [b for b in base.source_blocks(candidate, 'utf8') if b['name'] == name]
        need(len(originals) == len(candidates) == 1, 'unique complete source blocks required')
        before, after = originals[0], candidates[0]
        occurrences = verify_frame_equivalence(before['text'], after['text'])
        need(all(new.encode() not in record for new in RENAMES.values() for record in publics),
             'renamed private frame equate exported')
        _, actions = base.linked_object_procedure(obj, start, end-start)
        row = dict(name=name, start=start, end=end, size=end-start, candidate_file=source,
                   candidate_lines=[after['start_line'], after['end_line']], upstream_file=upstream_name,
                   upstream_lines=[before['start_line'], before['end_line']],
                   upstream_block_sha256=sha(before['text'].encode()), candidate_block_sha256=sha(after['text'].encode()),
                   renames=RENAMES, frame_equates=FRAME, rename_occurrences=occurrences,
                   distance=proc['distance'], inline_data=False,
                   start_listing_line=proc['start_listing_line'], end_listing_line=proc['end_listing_line'],
                   padding=[], linked_sha256=sha(linked.program_image[start:end]),
                   ordered_mz_fixups=[], object_link_actions=actions,
                   **native_observations(original.program_image[start:end], start))
        base.verify_raw_procedure(row, original, linked, obj)
        rows.append(row)
    return dict(schema_version=1, kind='source-backed-master-ems-transfer-proposal', decision='PROPOSAL',
                authored_credit=0, authored_denominator=None, compiler_invocations=0,
                base_proof_sha256=sha((root / BASE).read_bytes()), full_bytes=196,
                padding_bytes=0, nonpadding_bytes=196, procedures=rows,
                reviewer_sources=[dict(file=name, sha256=sha((root/name).read_bytes())) for name in SOURCES],
                limitations='Two complete primary-source-derived large-FAR EMS wrappers only. Secondary NEAR-model library objects are not claimed. No source instructions, linked bytes or fixup order changed. Zero authored credit; no new builds or global denominator.')


def review_inputs(meta, *, root=ROOT):
    validate_metadata(meta, root=root)
    need(build_metadata(root=root) == meta, 'current primary/native observations differ from proposal')
    return dict(procedures=2, full_bytes=196, byte_proof_replayed=True, authored_credit=0, compiler_invocations=0)


def reviewed_claims(root, views, *, verify_targets=False):
    path = root / DECISION
    if not path.exists():
        return [], None
    raw, decision = (root / PROOF).read_bytes(), json.loads(path.read_text())
    meta = json.loads(raw)
    validate_metadata(meta, root=root)
    inherited = json.loads((root / BASE).read_text())
    expected = dict(schema_version=1, decision='ADOPT', classification='verified-vendor-code',
                    proof_sha256=sha(raw), base_proof_sha256=BASE_SHA,
                    target_sha256=inherited['inputs']['target']['sha256'], full_bytes=196,
                    authored_credit=0, authored_denominator=None, procedures=[r['name'] for r in meta['procedures']])
    need(decision == expected, 'explicit EMS transfer vendor adoption differs')
    need(views['main']['sha256'] == inherited['target_payload_sha256'], 'adoption target payload differs')
    if verify_targets:
        review_inputs(meta, root=root)
    return [dict(start=r['start'], end=r['end'], kind='verified-vendor-code',
                 library='master.lib 0.23 source', member=r['name']) for r in meta['procedures']], sha(path.read_bytes())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    for name in ('write', 'check', 'structural-check'):
        modes.add_argument('--'+name, action='store_true')
    args = parser.parse_args()
    if args.write:
        meta = build_metadata()
        validate_metadata(meta)
        (ROOT / PROOF).write_text(json.dumps(meta, indent=2)+'\n')
    else:
        meta = json.loads((ROOT / PROOF).read_text())
    validate_metadata(meta)
    result = review_inputs(meta) if args.check else dict(procedures=2, full_bytes=196,
             byte_proof_replayed=args.write, authored_credit=0, compiler_invocations=0)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
