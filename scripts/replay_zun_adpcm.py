#!/usr/bin/env python3
"""Focused, exact original-toolchain validation of ZUN.COM's -O ADPCM child.

Only the real 926-byte embedded COM is compiled. CODE, initialized state and
uninitialized BSS are kept distinct. Historical source origin is not assumed.
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
CONFIG = ROOT / 'config/zun_adpcm.toml'
PUBLIC = ROOT / 'config/zun_adpcm_acceptance.json'
ASSEMBLER = ['wine', r'C:\TASM50\bin\TASM32.EXE', '/m', '/mx', '/t']
EXPECTED_PUBLICS = {'ADPCM_DIAGNOSTIC_ENTRY': 0x100, 'CHECK_BOARD': 0x127,
                    'TRY_CLASSIC_BOARD': 0x1A0, 'TRY_EXTENDED_BOARD': 0x247,
                    'CHECK_RAM': 0x2E4, 'ADPCM_SETUP': 0x2FB,
                    'ADPCM_DRAIN': 0x3A8, 'ADPCM_RECEIVE_ONCE': 0x428,
                    'CHECK_RAM_SIGNATURE': 0x449,
                    'WRITE_ADPCM_REGISTER': 0x455}


def scope(config: dict) -> None:
    if (config['schema_version'] != 1 or config['artifact'] != 'th05-zun' or
            config['member'] != '-O' or config['container_start'] != 0x355 or
            config['size'] != 926 or config['code_bytes'] != 892 or
            config['initialized_data_bytes'] != 34 or config['bss_bytes'] != 42 or
            config['code_bytes'] + config['initialized_data_bytes'] != config['size'] or
            config['instruction_nops'] != [] or config['publics'] != EXPECTED_PUBLICS or
            config['origin'] != 'inferred-original-register-assembly' or
            config['global_authored_credit'] != 'unreviewed'):
        raise ValueError('invalid physical, semantic, or source-origin -O scope')


def target_child(config: dict) -> bytes:
    a = find_artifact(load_target_manifest(ROOT / 'config/targets.toml'), config['artifact'])
    raw = read_verified_artifact(ROOT, a)
    members = [p for p in parse_launcher(raw, expected_sha256=a['sha256'])['payloads']
               if p['name'] == config['member']]
    if (len(members) != 1 or
            (members[0]['file_start'], members[0]['size'], members[0]['sha256']) !=
            (config['container_start'], config['size'], config['sha256'])):
        raise ValueError('the original complete embedded -O child changed')
    return raw[members[0]['file_start']:members[0]['file_end']]


def observe(work: Path, target: bytes, config: dict) -> dict:
    raw = (work / 'check.com').read_bytes()
    if len(raw) != config['size']:
        raise ValueError('the full COM output is not exactly 926 bytes')
    obj = (work / 'check.obj').read_bytes()
    omf = describe_omf(obj)
    if not omf['valid'] or omf['translator_comments'] != ['Turbo Assembler  Version 5.0']:
        raise ValueError('not a valid native TASM32 object')
    map_text = (work / 'check.map').read_text(encoding='cp437')
    for public, native in EXPECTED_PUBLICS.items():
        matches = re.findall(r'^\s*0000:([0-9A-F]{4})\s+(?:idle\s+)?' +
                             re.escape(public) + r'\s*$', map_text, re.M | re.I)
        if not matches or any(int(m, 16) != native for m in matches):
            raise ValueError('the native public function entry differs: ' + public)
    if ('0000:0000 047C C=CODE' not in map_text or
            '0000:047C 0022 C=DATA' not in map_text or
            '0000:049E 002A C=BSS' not in map_text):
        raise ValueError('the original CODE/DATA/BSS linker frames differ')
    records = parse_omf(obj)
    if any(r.name in ('LIDATA', 'LIDATA32', 'COMDAT', 'COMDAT32') for r in records):
        raise ValueError('unsupported repeated data or member substitution')
    segs = [r for r in records if r.name == 'SEGDEF']
    if (len(segs) != 3 or
            [int.from_bytes(r.data[1:3], 'little') for r in segs] != [0x47C, 0x22, 0x2A]):
        raise ValueError('nonoriginal code, initialized data or uninitialized BSS')
    ledatas = [r for r in records if r.name == 'LEDATA']
    if len(ledatas) != 2:
        raise ValueError('incomplete original two-segment OMF payload')
    for record, expected_segment, expected_offset, expected_size in (
            (ledatas[0], 1, 0x100, 892), (ledatas[1], 2, 0, 34)):
        seg, pos = omf_index(record.data, 0)
        off = struct.unpack_from('<H', record.data, pos)[0]
        if (seg, off, len(record.data) - pos - 2) != (
                expected_segment, expected_offset, expected_size):
            raise ValueError('CODE/DATA LEDATA does not span the entire native producer')
    # In the original COM, BSS is allocated only by DOS's memory environment.
    # It is not an initialized byte array that would inflate compared content.
    return {'size': len(raw), 'sha256': digest_bytes(raw),
            'raw_exact': raw == target,
            'code_exact': raw[:892] == target[:892],
            'initialized_data_exact': raw[892:] == target[892:],
            'code_sha256': digest_bytes(raw[:892]),
            'data_sha256': digest_bytes(raw[892:]),
            'bss_initialized_bytes': 0,
            'object_sha256': omf['sha256'],
            'object_normalized_sha256': omf['dependency_timestamp_normalized_sha256'],
            'map_sha256': digest_file(work / 'check.map')}


def replay_round(directory: Path, source: str, original: bytes, config: dict,
                 *, negative: bool = False) -> dict:
    work = directory / 'source'
    work.mkdir(parents=True, exist_ok=False)
    if negative:
        a, b = config['negative']['find'], config['negative']['replace']
        if not a or source.count(a) != 1 or a == b:
            raise ValueError('invalid source-level negative variation')
        source = source.replace(a, b)
    (work / 'check.asm').write_bytes(source.encode(config['assembler_encoding']))
    (work / 'build_dumb.bat').touch()
    tool = Builder(work, ROOT / '.analysis/toolchain/wineprefix',
                   ROOT / '_reference/ReC98/bin/msdos.exe')
    tool.execute('assemble', [*ASSEMBLER, 'check.asm', 'check.obj'])
    (work / 'link.rsp').write_bytes(b'-c -s -t check.obj, check.com, check.map,\r\n')
    tool.execute('link', ['wine', str(tool.msdos), '-e', '-x', 'tlink', '@link.rsp'])
    return observe(work, original, config)


def check_public(record: dict, config: dict) -> None:
    if (record.get('manifest_sha256') != digest_file(CONFIG) or
            record.get('source_sha256') != digest_file(ROOT / config['source']) or
            record.get('toolchain_manifest_sha256') != digest_file(ROOT / 'config/toolchain.toml') or
            record.get('origin') != config['origin'] or
            record.get('global_authored_credit') != 'unreviewed' or
            record.get('bss_bytes') != config['bss_bytes']):
        raise ValueError('stale source/manifest/toolchain or false authored-byte claim')
    pos = record.get('rounds', [])
    negative = record.get('negative_control', {})
    if (len(pos) != 2 or
            any(not (p['raw_exact'] and p['code_exact'] and p['initialized_data_exact'])
                or p['size'] != 926 or p['sha256'] != config['sha256'] or
                p['bss_initialized_bytes'] != 0 for p in pos) or
            pos[0]['object_normalized_sha256'] != pos[1]['object_normalized_sha256'] or
            negative.get('raw_exact') is not False or
            negative.get('code_exact') is not False or
            negative.get('initialized_data_exact') is not True or
            negative.get('bss_initialized_bytes') != 0):
        raise ValueError('missing deterministic double exact or compiled semantic negative')


def accept(path: Path, config: dict) -> None:
    receipt = json.loads(path.read_text())
    if (receipt['manifest_sha256'] != digest_file(CONFIG) or
            digest_file(path.parent / 'input.asm') != receipt['source_sha256']):
        raise ValueError('the recorded source/manifest changed after replay')
    tool_path = path.parent / 'toolchain-attestation.json'
    tool = json.loads(tool_path.read_text())
    if (digest_file(tool_path) != receipt['toolchain_receipt_sha256'] or
            tool['manifest_sha256'] != digest_file(ROOT / 'config/toolchain.toml') or
            not all(tool[k] for k in ('ready', 'identity_pass', 'execution_pass'))):
        raise ValueError('the actual original-toolchain attestation changed')
    if 'toolchain_reuse_proof_sha256' in receipt:
        proof = path.parent / 'toolchain-reuse-proof.json'
        if digest_file(proof) != receipt['toolchain_reuse_proof_sha256']:
            raise ValueError('toolchain reuse proof disagrees')
    target = target_child(config)
    for i, name in enumerate(('a','b')):
        if observe(path.parent / name / 'source', target, config) != receipt['rounds'][i]:
            raise ValueError('saved positive producer differs from the accepted record')
    if observe(path.parent / 'negative/source', target, config) != receipt['negative_control']:
        raise ValueError('saved negative producer differs from the accepted record')
    record = {**receipt, 'replay_receipt_sha256': digest_file(path)}
    check_public(record, config)
    PUBLIC.write_text(json.dumps(record, indent=2) + '\n')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    choices = parser.add_mutually_exclusive_group(required=True)
    choices.add_argument('--output', type=Path)
    choices.add_argument('--accept', type=Path)
    choices.add_argument('--check', action='store_true')
    args = parser.parse_args()
    config = tomllib.loads(CONFIG.read_text())
    scope(config)
    if args.check:
        check_public(json.loads(PUBLIC.read_text()), config)
        print('PASS: ZUN -O original 926-byte COM source-current, BSS uncredited')
        return 0
    if args.accept:
        accept(args.accept, config)
        print('PASS: two native exact ZUN -O COM builds and the source negative accepted')
        return 0
    out = args.output.resolve()
    if out.exists():
        parser.error('focused -O replay requires a new output directory')
    out.mkdir(parents=True)
    source = (ROOT / config['source']).read_bytes()
    text = source.decode(config['source_encoding'])
    (out / 'input.asm').write_bytes(source)
    (out / 'unit.toml').write_bytes(CONFIG.read_bytes())
    target = target_child(config)
    with (ROOT / '.analysis/borland.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        tool = freeze_toolchain(ROOT, out / 'toolchain-attestation.json')
        pos = [replay_round(out / label, text, target, config) for label in ('a','b')]
        neg = replay_round(out / 'negative', text, target, config, negative=True)
    receipt = {'schema_version': 1, 'kind': 'focused-zun-O-adpcm-original-com-replay',
               'manifest_sha256': digest_file(CONFIG),
               'source_sha256': digest_bytes(source),
               'toolchain_manifest_sha256': digest_file(ROOT / 'config/toolchain.toml'),
               'toolchain_receipt_sha256': digest_file(out / 'toolchain-attestation.json'),
               'toolchain_reused': tool['reused'],
               'toolchain_reuse_proof_sha256': tool['proof_sha256'],
               'origin': config['origin'], 'global_authored_credit': 'unreviewed',
               'bss_bytes': config['bss_bytes'],
               'rounds': pos, 'negative_control': neg}
    check_public(receipt, config)
    (out / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print('PASS: complete original 926-byte ZUN -O child built twice with source negative:', out / 'receipt.json')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
