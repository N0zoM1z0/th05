#!/usr/bin/env python3
"""Strict focused TASM/TLINK proof for ZUN.COM's embedded -G installer.

The 8192-byte external image is assembled *only* in a private build directory
from a separately reviewed source BMP. No font bytes are committed or counted
as authored code. This accepts only the complete 8377-byte -G child.
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
from review_font_resource import bitmap_tiles, read_input

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / 'config/zun_gaiji.toml'
PUBLIC = ROOT / 'config/zun_gaiji_acceptance.json'
ASSEMBLER = ['wine', r'C:\TASM50\bin\TASM32.EXE', '/m', '/mx', '/t']
FONT_START = 185


def scope(config: dict) -> list[dict]:
    keys = ('code_bytes', 'alignment_bytes', 'initialized_message_bytes', 'external_resource_bytes')
    expected = (75, 1, 109, 8192)
    if (config['schema_version'] != 1 or
            tuple(config[k] for k in keys) != expected or
            config['size'] != sum(expected) or config['public_start'] != 0x100 or
            config['container_start'] != 0x2488 or config['member'] != '-G' or
            config['artifact'] != 'th05-zun' or
            config['private_asset_include'] != 'gaiji_private_asset.inc' or
            config['resource_proof'] != 'config/font_resource.json' or
            config['resource_decision'] != 'config/reviewed_font_resource.json' or
            config['origin'] != 'inferred-original-register-assembly' or
            config['global_authored_credit'] != 'unreviewed'):
        raise ValueError('invalid reviewed -G bytes, asset boundary or source ownership')
    cursor = 0
    spans = []
    for key in keys:
        spans.append({'kind': key, 'start': cursor, 'end': cursor + config[key]})
        cursor += config[key]
    if spans[-1]['start'] != FONT_START or spans[-1]['end'] != 8377:
        raise ValueError('incorrect native font offset or complete COM extent')
    return spans


def original(config: dict) -> bytes:
    artifact = find_artifact(load_target_manifest(ROOT / 'config/targets.toml'), config['artifact'])
    raw = read_verified_artifact(ROOT, artifact)
    view = parse_launcher(raw, expected_sha256=artifact['sha256'])
    matches = [row for row in view['payloads'] if row['name'] == config['member']]
    if (len(matches) != 1 or
            (matches[0]['file_start'], matches[0]['size'], matches[0]['sha256']) !=
            (config['container_start'], config['size'], config['sha256'])):
        raise ValueError('ZUN carrier -G member identity changed')
    child = raw[matches[0]['file_start']:matches[0]['file_end']]
    if digest_bytes(child) != config['sha256'] or digest_bytes(child[FONT_START:]) != config['bitmap_sha256']:
        raise ValueError('ZUN -G target child/font data differs from pinned source')
    return child


def asset_model(config: dict) -> bytes:
    proof = json.loads((ROOT / config['resource_proof']).read_text())
    decision = json.loads((ROOT / config['resource_decision']).read_text())
    # The font is independently reviewed as *zero-credit* embedded resource;
    # this verifier must never substitute an arbitrary local font.
    if (proof['id'] != 'zun-cg-font' or proof['member'] != '-G' or
            proof['bitmap_sha256'] != config['bitmap_sha256'] or
            (proof['bitmap_start'], proof['bitmap_end']) != (0x2541, 0x4541) or
            proof['reference_bitmap']['path'] != '_reference/ReC98/th05/sprites/gaiji.bmp' or
            proof['reference_bitmap']['sha256'] != '703f056ff649492bb61468ee74df9f5317f26000281f4d04f699e6d93d07efbe' or
            proof['authored_credit'] != 0 or decision.get('authored_credit') != 0):
        raise ValueError('unreviewed external font/model/zero-credit decision')
    bitmap = bitmap_tiles(read_input(ROOT, proof['reference_bitmap']))
    if len(bitmap) != config['external_resource_bytes'] or digest_bytes(bitmap) != config['bitmap_sha256']:
        raise ValueError('resource geometry fails independent source digest')
    return bitmap


def source_asset_include(asset: bytes) -> str:
    # Constructed only in .analysis/*/source, and not returned or published.
    lines = ['; Private proof-only expansion of the pinned independent BMP.']
    for i in range(0, len(asset), 16):
        lines.append('db ' + ','.join(f'0{value:02X}h' for value in asset[i:i+16]))
    return '\n'.join(lines) + '\n'


def observe(work: Path, target: bytes, asset: bytes, config: dict) -> dict:
    actual = (work / 'install.com').read_bytes()
    description = describe_omf((work / 'install.obj').read_bytes())
    if not description['valid'] or description['translator_comments'] != ['Turbo Assembler  Version 5.0']:
        raise ValueError('not the real Turbo Assembler OMF producer')
    if len(actual) != config['size']:
        raise ValueError('incomplete -G child size')
    if actual[75] != 0 or actual[FONT_START:] != asset:
        raise ValueError('noncanonical assembler alignment or unpinned private font')
    map_text = (work / 'install.map').read_text(encoding='cp437')
    matches = re.findall(r'^\s*0000:([0-9A-F]{4})\s+(?:idle\s+)?GAIJI_INSTALL_START\s*$',
                         map_text, re.M | re.I)
    if not matches or any(int(value, 16) != 0x100 for value in matches):
        raise ValueError('incorrect true COM entry public')
    if ('0000:0000 014B C=CODE' not in map_text or
            '0000:014C 206D C=DATA' not in map_text):
        raise ValueError('incorrect actual code/data OMF frames or allocation')
    records = parse_omf((work / 'install.obj').read_bytes())
    if any(record.name in ('LIDATA','LIDATA32','COMDAT','COMDAT32') for record in records):
        raise ValueError('unreviewed iterated DATA or COMDAT emitted')
    segdef = [z for z in records if z.name == 'SEGDEF']
    if (len(segdef) != 2 or
            struct.unpack_from('<H', segdef[0].data, 1)[0] != 0x14B or
            struct.unpack_from('<H', segdef[1].data, 1)[0] != 0x206D):
        raise ValueError('CODE/DATA SEGDEF boundaries differ from original')
    coverage = {1: bytearray(75), 2: bytearray(8301)}
    for row in records:
        if row.name != 'LEDATA':
            continue
        si, p = omf_index(row.data, 0)
        off = struct.unpack_from('<H', row.data, p)[0]
        body = row.data[p+2:]
        if (si not in coverage or (si == 1 and off != 0x100) or
                (si == 1 and len(body) != 75)):
            raise ValueError('unexpected original CODE SEGDEF LEDATA')
        pos = off - 0x100 if si == 1 else off
        if not 0 <= pos <= pos+len(body) <= len(coverage[si]) or any(coverage[si][pos:pos+len(body)]):
            raise ValueError('bad, overlapping or out-of-range original DATA LEDATA')
        coverage[si][pos:pos+len(body)] = b'\1' * len(body)
    if any(not all(data) for data in coverage.values()):
        raise ValueError('incomplete OMF CODE/DATA backing')
    spans = scope(config)
    compare = {p['kind']: actual[p['start']:p['end']] == target[p['start']:p['end']] for p in spans}
    return {'size': len(actual), 'sha256': digest_bytes(actual), 'raw_exact': actual == target,
            'content_exact': compare, 'font_sha256': digest_bytes(actual[FONT_START:]),
            'omf_sha256': description['sha256'],
            'omf_normalized_sha256': description['dependency_timestamp_normalized_sha256'],
            'map_sha256': digest_file(work / 'install.map')}


def run_round(where: Path, source: str, target: bytes, asset: bytes, config: dict, negative: bool) -> dict:
    where.mkdir(parents=True, exist_ok=False)
    if negative:
        old, new = config['negative']['find'], config['negative']['replace']
        if not old or source.count(old) != 1 or old == new:
            raise ValueError('invalid semantic source mutation')
        source = source.replace(old, new)
    (where / 'install.asm').write_bytes(source.encode(config['assembler_encoding']))
    (where / config['private_asset_include']).write_text(source_asset_include(asset))
    (where / 'build_dumb.bat').touch()
    builder = Builder(where, ROOT / '.analysis/toolchain/wineprefix', ROOT / '_reference/ReC98/bin/msdos.exe')
    builder.execute('assemble', [*ASSEMBLER, 'install.asm', 'install.obj'])
    (where / 'link.rsp').write_bytes(b'-c -s -t install.obj, install.com, install.map,\r\n')
    builder.execute('link', ['wine', str(builder.msdos), '-e', '-x', 'tlink', '@link.rsp'])
    return observe(where, target, asset, config)


def check_record(record: dict, config: dict) -> None:
    source = ROOT / config['source']
    if (record.get('manifest_sha256') != digest_file(CONFIG) or
            record.get('source_sha256') != digest_file(source) or
            record.get('toolchain_manifest_sha256') != digest_file(ROOT / 'config/toolchain.toml') or
            record.get('font_proof_sha256') != digest_file(ROOT / config['resource_proof']) or
            record.get('font_decision_sha256') != digest_file(ROOT / config['resource_decision']) or
            record.get('font_sha256') != config['bitmap_sha256'] or
            record.get('origin') != config['origin'] or
            record.get('global_authored_credit') != 'unreviewed'):
        raise ValueError('stale ZUN gaiji source/proof/decision or invented global authorship')
    positives, negative = record.get('rounds', []), record.get('negative_control', {})
    if (len(positives) != 2 or any(not x['raw_exact'] or x['sha256'] != config['sha256'] or
            x['size'] != config['size'] or not all(x['content_exact'].values()) or
            x['font_sha256'] != config['bitmap_sha256'] for x in positives) or
            positives[0]['omf_normalized_sha256'] != positives[1]['omf_normalized_sha256'] or
            negative.get('raw_exact') is not False or
            negative.get('content_exact', {}).get('code_bytes') is not False or
            any(negative.get('content_exact', {}).get(k) is not True for k in
                ('alignment_bytes','initialized_message_bytes','external_resource_bytes')) or
            negative.get('font_sha256') != config['bitmap_sha256']):
        raise ValueError('incomplete dual positive or source negative proof')


def accept(path: Path, config: dict) -> None:
    receipt = json.loads(path.read_text())
    if receipt['manifest_sha256'] != digest_file(CONFIG):
        raise ValueError('stale focused receipt manifest')
    if (digest_file(path.parent / 'input.asm') != receipt['source_sha256'] or
            digest_file(ROOT / config['source']) != receipt['source_sha256']):
        raise ValueError('frozen ZUN -G source differs')
    tool_path = path.parent / 'toolchain-attestation.json'
    tool = json.loads(tool_path.read_text())
    if (digest_file(tool_path) != receipt['toolchain_receipt_sha256'] or
            tool['manifest_sha256'] != digest_file(ROOT / 'config/toolchain.toml') or
            not all(tool[k] for k in ('ready','identity_pass','execution_pass'))):
        raise ValueError('invalid actual toolchain attestation')
    if 'toolchain_reuse_proof_sha256' in receipt:
        p = path.parent / 'toolchain-reuse-proof.json'
        if digest_file(p) != receipt['toolchain_reuse_proof_sha256']:
            raise ValueError('invalid reuse proof')
    target, font = original(config), asset_model(config)
    for index,label in enumerate(('a','b')):
        if observe(path.parent / label / 'source', target, font, config) != receipt['rounds'][index]:
            raise ValueError('saved complete positive does not reproduce its receipt')
    if observe(path.parent / 'negative/source', target, font, config) != receipt['negative_control']:
        raise ValueError('saved complete negative does not reproduce its receipt')
    saved = {**receipt, 'replay_receipt_sha256': digest_file(path)}
    check_record(saved, config)
    PUBLIC.write_text(json.dumps(saved, indent=2) + '\n')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--output', type=Path)
    mode.add_argument('--accept', type=Path)
    mode.add_argument('--check', action='store_true')
    args = parser.parse_args()
    config = tomllib.loads(CONFIG.read_text())
    scope(config)
    if args.check:
        check_record(json.loads(PUBLIC.read_text()), config)
        print('PASS: source-current standalone ZUN -G 8377-byte child; 8192 external font bytes zero credited')
        return 0
    if args.accept:
        accept(args.accept, config)
        print('PASS: complete ZUN -G native COM accepted, external resource separately attributed')
        return 0
    out = args.output.resolve()
    if out.exists():
        parser.error('focused -G output directory must be fresh')
    out.mkdir(parents=True)
    src = (ROOT / config['source']).read_bytes()
    text = src.decode(config['source_encoding'])
    (out / 'input.asm').write_bytes(src)
    (out / 'unit.toml').write_bytes(CONFIG.read_bytes())
    target, font = original(config), asset_model(config)
    with (ROOT / '.analysis/borland.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        tool = freeze_toolchain(ROOT, out / 'toolchain-attestation.json')
        rounds = [run_round(out / lab / 'source', text, target, font, config, False)
                  for lab in ('a','b')]
        negative = run_round(out / 'negative/source', text, target, font, config, True)
    receipt = {'schema_version': 1, 'kind': 'bounded-zun-gaiji-com-replay',
               'manifest_sha256': digest_file(CONFIG),
               'source_sha256': digest_bytes(src),
               'toolchain_manifest_sha256': digest_file(ROOT / 'config/toolchain.toml'),
               'toolchain_receipt_sha256': digest_file(out / 'toolchain-attestation.json'),
               'toolchain_reused': tool['reused'],
               'toolchain_reuse_proof_sha256': tool['proof_sha256'],
               'font_proof_sha256': digest_file(ROOT / config['resource_proof']),
               'font_decision_sha256': digest_file(ROOT / config['resource_decision']),
               'font_sha256': digest_bytes(font),
               'origin': config['origin'],
               'global_authored_credit': 'unreviewed',
               'rounds': rounds, 'negative_control': negative}
    check_record(receipt, config)
    (out / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print('PASS: two complete 8377-byte -G TASM/TLINK producers and a compiled source negative:', out / 'receipt.json')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
