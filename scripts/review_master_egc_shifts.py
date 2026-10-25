#!/usr/bin/env python3
"""Four source-backed vendor procedures with enumerated private-symbol edits.

The older literal-source proof stays frozen. This separate proof permits only
its named local-label substitutions, never instruction or linked-byte edits.
No compilation, authored credit or global denominator is supplied.
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
PROOF = 'config/master_egc_shifts_ownership.json'
DECISION = 'config/reviewed_master_egc_shifts.json'
BASE = 'config/master_vendor_ownership.json'
BASE_SHA = '8b5e9b31ce345df277a31348d49aec9197e4c5c390eec0b9f812516c8287010a'
EVIDENCE_SHA = '4ae02c61f3f460c273baced8c8a66e9f0a6783a339fc80d116cb4350e6f9011d'
SOURCES = ['scripts/review_master_egc_shifts.py', 'scripts/review_master.py',
           'scripts/lib/omf.py', 'scripts/lib/pc98.py']
SCOPES = [
    ('DOWN', 'D', 0x8aa, 0x9b0, {'diff': 'egcsftd_diff', 'sub_si': 'egcsftd_sub_si', 'sub_di': 'egcsftd_sub_di'}),
    ('LEFT', 'L', 0x9b0, 0xab2, {'start_di': 'egcsftl_start_di', 'add_si': 'egcsftl_add_si', 'add_di': 'egcsftl_add_di'}),
    ('RIGHT', 'R', 0xab2, 0xbc2, {'start_di': 'egcsftr_start_di', 'sub_si': 'egcsftr_sub_si', 'sub_di': 'egcsftr_sub_di'}),
    ('UP', 'U', 0xbc2, 0xcc2, {'diff': 'egcsftu_diff', 'add_si': 'egcsftu_add_si', 'add_di': 'egcsftu_add_di'}),
]
TOKEN = re.compile(r'(?<![\w@$?])[A-Za-z_@$?][\w@$?]*')


def need(value, message):
    if not value:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def rename_map(patch_symbols):
    return {**{name: '@@'+name for name in ('none', 'less', 'plus', 'next_line')}, **patch_symbols}


def rename_private_symbols(text, replacements):
    """Change only defined labels/self-patch EQU names, outside comments.

    All nonidentifier characters, whitespace, comments and instruction/data
    tokens survive literally. There is no case folding or pretty printing.
    """
    need(isinstance(replacements, dict) and replacements, 'missing explicit symbol edits')
    need(all(TOKEN.fullmatch(x) for pair in replacements.items() for x in pair), 'invalid symbol spelling')
    need(len(set(replacements.values())) == len(replacements), 'symbol edits must be bijective')
    definitions, identifiers, counts = set(), set(), dict.fromkeys(replacements, 0)
    for line in text.split('\n'):
        code = line.split(';', 1)[0]
        need('"' not in code and "'" not in code, 'quoted code is outside this narrow source proof')
        identifiers.update(TOKEN.findall(code))
        definition = re.match(r'\s*([A-Za-z_@$?][\w@$?]*)(?:\s*:|\s+EQU\s+\$-[12]\s*$)', code)
        if definition:
            definitions.add(definition[1])
    need(set(replacements) <= definitions, 'only defined private labels and self-patch symbols may change')
    need(not set(replacements.values()) & identifiers, 'new symbol collides with original source')
    out = []
    for line in text.split('\n'):
        code, marker, comment = line.partition(';')
        def replace(match):
            name = match[0]
            if name in replacements:
                counts[name] += 1
            return replacements.get(name, name)
        out.append(TOKEN.sub(replace, code) + marker + comment)
    need(all(n >= 2 for n in counts.values()), 'each edited symbol needs its definition and a reference')
    return '\n'.join(out), counts


def verify_private_symbol_equivalence(original, candidate, replacements):
    transformed, counts = rename_private_symbols(original, replacements)
    need(transformed == candidate, 'complete source differs beyond enumerated private symbols')
    return counts


def digest(meta):
    return sha(json.dumps(meta, sort_keys=True, separators=(',', ':')).encode())


def validate_metadata(meta, *, root=ROOT):
    # The source list includes this verifier; exclude that list from the fixed
    # observation digest to avoid a self-hash cycle. Adoption pins the entire
    # proof file, including those reviewer hashes, separately.
    need(digest({k: v for k, v in meta.items() if k != 'reviewer_sources'}) == EVIDENCE_SHA,
         'frozen four-procedure evidence differs')
    need(meta['schema_version'] == 1 and meta['kind'] == 'source-backed-master-egc-shift-proposal', 'proof schema')
    need(meta['decision'] == 'PROPOSAL' and meta['authored_credit'] == 0 and
         meta['authored_denominator'] is None and meta['compiler_invocations'] == 0, 'proof cannot grant source credit')
    need(sha((root / BASE).read_bytes()) == meta['base_proof_sha256'] == BASE_SHA, 'frozen original proof differs')
    need(meta['full_bytes'] == 1048 and meta['padding_bytes'] == 11 and
         meta['nonpadding_bytes'] == 1037, 'whole vendor accounting')
    need(len(meta['procedures']) == 4, 'exactly four complete procedures')
    for row, (direction, letter, start, end, patches) in zip(meta['procedures'], SCOPES):
        need((row['name'], row['start'], row['end'], row['size']) ==
             ('EGC_SHIFT_'+direction, start, end, end-start), 'reviewed complete procedure boundary')
        need(row['candidate_file'] == 'libs/master.lib/egc_shift_'+direction.lower()+'.asm' and
             row['upstream_file'] == 'EGCSFT'+letter+'.ASM', 'source owner differs')
        need(row['renames'] == rename_map(patches), 'unreviewed symbol substitution')
        need(row['distance'] == 'far-by-large-model' and row['ordered_mz_fixups'] == [] and
             row['inline_data'] is False, 'native ABI or relocation context differs')
        pads = [p['start']-start for p in row['padding']]
        need(pads == row['instruction_nop_offsets'] and len(set(pads)) == len(pads) and
             all(0 <= x < end-start for x in pads), 'instruction NOP/alignment enumeration differs')
        need(row['return_kind'] == 'retf' and row['return_cleanup'] == 10 and
             0 <= row['return_offset'] < row['size'], 'real far Pascal return')
    need(sum(len(x['padding']) for x in meta['procedures']) == 11, 'padding sum differs')
    need(meta['reviewer_sources'] == [dict(file=name, sha256=sha((root/name).read_bytes()))
         for name in SOURCES], 'reviewer source identity differs')
    base.validate_metadata(json.loads((root / BASE).read_text()), root=root)


def native_observations(raw):
    from capstone import Cs, CS_ARCH_X86, CS_MODE_16
    ins = list(Cs(CS_ARCH_X86, CS_MODE_16).disasm(raw, 0))
    need(sum(i.size for i in ins) == len(raw), 'native decode incomplete')
    returns = [i for i in ins if i.mnemonic.startswith('ret')]
    need(len(returns) == 1 and returns[0].mnemonic == 'retf' and returns[0].op_str == '0xa', 'native RETF10 differs')
    starts = {i.address for i in ins}
    for i in ins:
        if i.mnemonic.startswith('j'):
            need(int(i.op_str, 16) in starts, 'native branch leaves instruction boundaries')
    return dict(instruction_count=len(ins), instruction_nop_offsets=[i.address for i in ins if i.mnemonic == 'nop'],
                return_kind='retf', return_cleanup=10, return_offset=returns[0].address)


def build_metadata(*, root=ROOT):
    inherited = json.loads((root / BASE).read_text())
    # Recheck primary archive, all frozen sources, actual listing/OMF/link and
    # the independent large-model macro context. The old decision is unchanged.
    base.review_inputs(inherited, root=root)
    raw = {key: base.pinned(root, value) for key, value in inherited['inputs'].items()}
    upstream = base.stored_lzh(raw['inner_archive'])
    active = base.listing_procedures(raw['listing'])
    original, linked = parse_mz(raw['target']), parse_mz(raw['calibration_exe'])
    obj = base.object_text(raw['saved_object'])
    public_records = [r.data for r in parse_omf(raw['saved_object']) if r.name == 'PUBDEF']
    rows = []
    for direction, letter, start, end, patches in SCOPES:
        name = 'EGC_SHIFT_'+direction
        proc = next(p for p in active if p['name'] == name and p['local_start']+0x272 == start)
        need(proc['local_end']+0x272 == end and not proc['inline_data'], 'complete listing boundary differs')
        source = 'libs/master.lib/egc_shift_'+direction.lower()+'.asm'
        need(proc['source'] == source, 'listing owner differs')
        candidate = (root / inherited['candidate_source_root'] / source).read_bytes()
        originals = [b for b in base.source_blocks(upstream['EGCSFT'+letter+'.ASM'], 'cp932') if b['name'] == name]
        candidates = [b for b in base.source_blocks(candidate, 'utf8') if b['name'] == name]
        need(len(originals) == len(candidates) == 1, 'unique complete source blocks required')
        before, after = originals[0], candidates[0]
        edits = rename_map(patches)
        counts = verify_private_symbol_equivalence(before['text'], after['text'], edits)
        need(all(new.encode() not in record for new in edits.values() for record in public_records), 'edited private symbol exported')
        _, actions = base.linked_object_procedure(obj, start, end-start)
        pads = [dict(start=p['local_start']+0x272, size=1, value=0x90, listing_line=p['listing_line']) for p in proc['padding']]
        row = dict(name=name, start=start, end=end, size=end-start, candidate_file=source,
                   candidate_lines=[after['start_line'], after['end_line']], upstream_file='EGCSFT'+letter+'.ASM',
                   upstream_lines=[before['start_line'], before['end_line']],
                   upstream_block_sha256=sha(before['text'].encode()), candidate_block_sha256=sha(after['text'].encode()),
                   renames=edits, rename_occurrences=counts, distance=proc['distance'], inline_data=False,
                   start_listing_line=proc['start_listing_line'], end_listing_line=proc['end_listing_line'],
                   padding=pads, linked_sha256=sha(linked.program_image[start:end]),
                   ordered_mz_fixups=[], object_link_actions=actions,
                   **native_observations(original.program_image[start:end]))
        base.verify_raw_procedure(row, original, linked, obj)
        rows.append(row)
    return dict(schema_version=1, kind='source-backed-master-egc-shift-proposal', decision='PROPOSAL',
                authored_credit=0, authored_denominator=None, compiler_invocations=0,
                base_proof_sha256=sha((root / BASE).read_bytes()), full_bytes=1048,
                padding_bytes=11, nonpadding_bytes=1037, procedures=rows,
                reviewer_sources=[dict(file=name, sha256=sha((root/name).read_bytes())) for name in SOURCES],
                limitations='Four primary-source-derived large-model procedures only. Secondary near-model binary members do not match and supply no proof. No authored credit, new builds, byte edits or global denominator.')


def review_inputs(meta, *, root=ROOT):
    validate_metadata(meta, root=root)
    need(build_metadata(root=root) == meta, 'current primary/native observations differ from proposal')
    return dict(procedures=4, full_bytes=1048, byte_proof_replayed=True, authored_credit=0, compiler_invocations=0)


def reviewed_claims(root, views, *, verify_targets=False):
    path = root / DECISION
    if not path.exists():
        return [], None
    decision = json.loads(path.read_text())
    raw = (root / PROOF).read_bytes()
    meta = json.loads(raw)
    validate_metadata(meta, root=root)
    expected = dict(schema_version=1, decision='ADOPT', classification='verified-vendor-code',
                    proof_sha256=sha(raw), base_proof_sha256=BASE_SHA,
                    target_sha256=json.loads((root / BASE).read_text())['inputs']['target']['sha256'],
                    full_bytes=1048, authored_credit=0, authored_denominator=None,
                    procedures=[r['name'] for r in meta['procedures']])
    need(decision == expected, 'explicit EGC vendor adoption differs')
    need(views['main']['sha256'] == json.loads((root / BASE).read_text())['target_payload_sha256'],
         'adoption target payload differs')
    if verify_targets:
        review_inputs(meta, root=root)
    claims = [dict(start=r['start'], end=r['end'], kind='verified-vendor-code',
                   library='master.lib 0.23 source', member=r['name']) for r in meta['procedures']]
    return claims, sha(path.read_bytes())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    for name in ('write', 'check', 'structural-check'):
        modes.add_argument('--'+name, action='store_true')
    args = parser.parse_args()
    if args.write:
        meta = build_metadata()
        (ROOT / PROOF).write_text(json.dumps(meta, indent=2)+'\n')
    else:
        meta = json.loads((ROOT / PROOF).read_text())
    validate_metadata(meta)
    result = review_inputs(meta) if args.check else dict(procedures=4, full_bytes=1048,
             byte_proof_replayed=args.write, authored_credit=0, compiler_invocations=0)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
