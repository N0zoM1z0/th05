#!/usr/bin/env python3
"""Incremental exact native reconstruction of only ZUN.COM's -I COM child.

This is an independently reviewed mixed register-CODE/initialized-message scope,
not a claim of historical source spelling or global authored-byte credit.
"""
from __future__ import annotations

import argparse
import fcntl
import json
from pathlib import Path
import re
import struct
import tomllib

from lib.launcher import parse_launcher
from lib.omf import describe_omf, parse_omf
from lib.pc98 import digest_bytes, digest_file
from lib.reference_build import Builder
from lib.replay_toolchain import freeze_toolchain
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from lib.unit_extents import _index as omf_index

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / 'config/zun_interrupt.toml'
PUBLIC = ROOT / 'config/zun_interrupt_acceptance.json'
EXECUTABLES = ['wine', r'C:\TASM50\bin\TASM32.EXE', '/m', '/mx', '/t']


def scope(config: dict) -> list[dict]:
    """Code/data are non-overlapping complete physical COM extents."""
    special = [dict(row, kind=key) for key in ('code_spans', 'data_spans')
               for row in config[key]]
    special.sort(key=lambda row: row['start'])
    cursor = 0
    totals = {'code_spans': 0, 'data_spans': 0}
    for row in special:
        if (type(row['start']) is not int or type(row['size']) is not int
                or row['start'] != cursor or row['size'] <= 0):
            raise ValueError('incomplete or overlapping -I child ranges')
        totals[row['kind']] += row['size']
        cursor += row['size']
    # These are actual procedure and initialized-string boundaries, not an
    # arbitrary choice of how many bytes to credit as executable instructions.
    if [(row['kind'], row['start'], row['size']) for row in special] != [
            ('code_spans', 0x000, 0x0EA), ('data_spans', 0x0EA, 0x102),
            ('code_spans', 0x1EC, 0x0DA), ('data_spans', 0x2C6, 0x12B)]:
        raise ValueError('the four independently reviewed -I boundaries changed')
    if (cursor != config['size'] or totals != {
            'code_spans': config['code_bytes'],
            'data_spans': config['initialized_data_bytes']}):
        raise ValueError('incomplete -I CODE/message byte classification')
    padding = config['uncredited_alignment_offsets']
    if padding != [3, 0x9B] or not all(
            any(row['kind'] == 'code_spans' and row['start'] <= n < row['start'] + row['size']
                for row in special) for n in padding):
        raise ValueError('incorrect explicit -I alignment padding')
    if config['origin'] != 'inferred-original-register-assembly' or config['global_authored_credit'] != 'unreviewed':
        raise ValueError('unreviewed historical source must not gain global credit')
    return special


def target_child(config: dict) -> bytes:
    a = find_artifact(load_target_manifest(ROOT / 'config/targets.toml'), config['artifact'])
    raw = read_verified_artifact(ROOT, a)
    z = parse_launcher(raw, expected_sha256=a['sha256'])
    members = [p for p in z['payloads'] if p['name'] == config['member']]
    if (len(members) != 1 or members[0]['file_start'] != config['container_start']
            or members[0]['size'] != config['size'] or members[0]['sha256'] != config['sha256']):
        raise ValueError('pinned launcher child identity changed')
    child = raw[members[0]['file_start']:members[0]['file_end']]
    if digest_bytes(child) != config['sha256']:
        raise ValueError('launcher child content changed')
    return child


def observe(source: Path, target: bytes, config: dict) -> dict:
    binary = (source / 'install.com').read_bytes()
    desc = describe_omf((source / 'install.obj').read_bytes())
    if not desc['valid'] or desc['translator_comments'] != ['Turbo Assembler  Version 5.0']:
        raise ValueError('not a valid TASM OMF producer')
    # Source DATA resides inside the original tiny-model CODE SEGDEF, not in a
    # made-up DATA SEGDEF, and the COM remains exactly 1009 bytes.
    ledger = (source / 'install.map').read_text(encoding='cp437')
    for name, address in config['publics'].items():
        matches = re.findall(r'^\s*0000:([0-9A-F]{4})\s+(?:idle\s+)?' + re.escape(name) + r'\s*$', ledger, re.M | re.I)
        if not matches or any(int(value, 16) != address for value in matches):
            raise ValueError('incorrect real COM public: ' + name)
    spans = scope(config)
    parts = [(r, binary[r['start']:r['start']+r['size']], target[r['start']:r['start']+r['size']]) for r in spans]
    if len(binary) != config['size']:
        raise ValueError('complete -I COM size differs')
    if any(binary[x] != 0x90 for x in config['uncredited_alignment_offsets']):
        raise ValueError('real even-alignment bytes missing')
    # Prove one ordinary complete segment with ORG 0100 and no image DATA
    # reclassification. This is a single emitted COM image; no relocs exist.
    recs = parse_omf((source / 'install.obj').read_bytes())
    if any(r.name in ('LIDATA', 'COMDAT', 'LIDATA32', 'COMDAT32') for r in recs):
        raise ValueError('iterated COM payload not accepted')
    ledatas = [r for r in recs if r.name == 'LEDATA']
    if len(ledatas) != 1:
        raise ValueError('expected a single complete ordinary -I CODE LEDATA')
    segment, at = omf_index(ledatas[0].data, 0)
    offset = struct.unpack_from('<H', ledatas[0].data, at)[0]
    if (segment != 1 or offset != 0x100
            or len(ledatas[0].data) - at - 2 != config['size']):
        raise ValueError('OMF CODE extent is not the complete COM after ORG 100h')
    segdefs = [r for r in recs if r.name == 'SEGDEF']
    if (len(segdefs) != 2 or int.from_bytes(segdefs[0].data[1:3], 'little') != 0x4F1
            or int.from_bytes(segdefs[1].data[1:3], 'little') != 0):
        raise ValueError('unexpected CODE/DATA SEGDEFs: inserted data or compiled code')
    return {'size': len(binary), 'sha256': digest_bytes(binary),
            'raw_exact': binary == target,
            'code_exact': all(a == b for r, a, b in parts if r['kind'] == 'code_spans'),
            'data_exact': all(a == b for r, a, b in parts if r['kind'] == 'data_spans'),
            'code_sha256': digest_bytes(b''.join(a for r, a, b in parts if r['kind'] == 'code_spans')),
            'data_sha256': digest_bytes(b''.join(a for r, a, b in parts if r['kind'] == 'data_spans')),
            'object_sha256': desc['sha256'],
            'object_normalized_sha256': desc['dependency_timestamp_normalized_sha256'],
            'publics': config['publics'], 'map_sha256': digest_file(source / 'install.map')}


def run_round(base: Path, text: str, target: bytes, config: dict, negative: bool = False) -> dict:
    source = base / 'source'
    source.mkdir(parents=True, exist_ok=False)
    if negative:
        original, modified = config['negative']['find'], config['negative']['replace']
        if not original or text.count(original) != 1 or original == modified:
            raise ValueError('invalid full-source negative mutation')
        text = text.replace(original, modified)
    (source / 'install.asm').write_bytes(text.encode(config['assembler_encoding']))
    (source / 'build_dumb.bat').touch()
    b = Builder(source, ROOT / '.analysis/toolchain/wineprefix', ROOT / '_reference/ReC98/bin/msdos.exe')
    b.execute('assembler', [*EXECUTABLES, 'install.asm', 'install.obj'])
    (source / 'link.rsp').write_bytes(b'-c -s -t install.obj, install.com, install.map,\r\n')
    b.execute('link', ['wine', str(b.msdos), '-e', '-x', 'tlink', '@link.rsp'])
    return observe(source, target, config)


def check_record(record: dict, config: dict) -> None:
    if (record['manifest_sha256'] != digest_file(CONFIG)
            or record['source_sha256'] != digest_file(ROOT / config['source'])
            or record['toolchain_manifest_sha256'] != digest_file(ROOT / 'config/toolchain.toml')
            or record['origin'] != config['origin'] or record['global_authored_credit'] != 'unreviewed'
            or record['size'] != config['size']):
        raise ValueError('source, toolchain, scope or unreviewed credit changed')
    p, n = record['rounds'], record['negative_control']
    if (len(p) != 2 or any(not all(a[k] for k in ('raw_exact', 'code_exact', 'data_exact'))
            or a['size'] != config['size'] or a['sha256'] != config['sha256'] for a in p)
            or p[0]['object_normalized_sha256'] != p[1]['object_normalized_sha256']
            or n['raw_exact'] or n['code_exact'] or not n['data_exact']):
        raise ValueError('incomplete native double-positive or source negative')


def accept(path: Path, config: dict) -> None:
    receipt = json.loads(path.read_text())
    if receipt['manifest_sha256'] != digest_file(CONFIG):
        raise ValueError('stale original -I manifest')
    frozen = path.parent / 'input.asm'
    if (digest_file(frozen) != receipt['source_sha256']
            or digest_file(ROOT / config['source']) != receipt['source_sha256']):
        raise ValueError('stale source or frozen input')
    tool_path = path.parent / 'toolchain-attestation.json'
    tool = json.loads(tool_path.read_text())
    if (digest_file(tool_path) != receipt['toolchain_receipt_sha256']
            or tool['manifest_sha256'] != digest_file(ROOT / 'config/toolchain.toml')
            or not tool['ready'] or not tool['identity_pass'] or not tool['execution_pass']):
        raise ValueError('native toolchain attestation changed')
    if 'toolchain_reuse_proof_sha256' in receipt:
        proof_path = path.parent / 'toolchain-reuse-proof.json'
        if digest_file(proof_path) != receipt['toolchain_reuse_proof_sha256']:
            raise ValueError('invalid toolchain reuse proof')
    t = target_child(config)
    for i, label in enumerate(('a','b')):
        if observe(path.parent / label / 'source', t, config) != receipt['rounds'][i]:
            raise ValueError('saved COM producer differs')
    if observe(path.parent / 'negative/source', t, config) != receipt['negative_control']:
        raise ValueError('saved source negative differs')
    saved = {**receipt, 'replay_receipt_sha256': digest_file(path)}
    check_record(saved, config)
    PUBLIC.write_text(json.dumps(saved, indent=2) + '\n')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--output', type=Path)
    modes.add_argument('--accept', type=Path)
    modes.add_argument('--check', action='store_true')
    args = parser.parse_args()
    config = tomllib.loads(CONFIG.read_text())
    if config['schema_version'] != 1:
        raise ValueError('unsupported -I manifest version')
    scope(config)
    if args.check:
        check_record(json.loads(PUBLIC.read_text()), config)
        print('PASS: source-current 1009-byte ZUN -I child; global authored credit remains unreviewed')
        return 0
    if args.accept:
        accept(args.accept, config)
        print('PASS: complete 1009-byte ZUN -I native child accepted')
        return 0
    out = args.output.resolve()
    if out.exists():
        parser.error('focused -I output directory must be new')
    out.mkdir(parents=True)
    original = (ROOT / config['source']).read_bytes()
    text = original.decode(config['source_encoding'])
    (out / 'input.asm').write_bytes(original)
    (out / 'unit.toml').write_bytes(CONFIG.read_bytes())
    target = target_child(config)
    with (ROOT / '.analysis/borland.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        tool = freeze_toolchain(ROOT, out / 'toolchain-attestation.json')
        positives = [run_round(out / label, text, target, config) for label in ('a', 'b')]
        negative = run_round(out / 'negative', text, target, config, negative=True)
    receipt = {'schema_version': 1, 'kind': 'bounded-zun-interrupt-com-replay',
               'manifest_sha256': digest_file(CONFIG), 'source_sha256': digest_bytes(original),
               'toolchain_manifest_sha256': digest_file(ROOT / 'config/toolchain.toml'),
               'toolchain_receipt_sha256': digest_file(out / 'toolchain-attestation.json'),
               'toolchain_reused': tool['reused'],
               'toolchain_reuse_proof_sha256': tool['proof_sha256'],
               'origin': config['origin'], 'global_authored_credit': 'unreviewed',
               'size': config['size'], 'rounds': positives, 'negative_control': negative}
    check_record(receipt, config)
    (out / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print('PASS: two 1009-byte native TASM/TLINK -I producers and compiled source negative:', out / 'receipt.json')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
