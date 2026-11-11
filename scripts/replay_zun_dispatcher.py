#!/usr/bin/env python3
"""Strict incremental native proof of the inner ZUN.COM dispatcher and table.

The five embedded programs occupy *proof-only zero ORG holes*. No original
child byte or child source file is consumed or emitted by this replay.
"""
from __future__ import annotations

import argparse
import fcntl
import json
from pathlib import Path
import re
import tomllib

from lib.launcher import parse_launcher
from lib.omf import describe_omf, parse_omf
from lib.pc98 import digest_bytes, digest_file
from lib.reference_build import Builder
from lib.replay_toolchain import freeze_toolchain
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / 'config/zun_dispatcher.toml'
PUBLIC = ROOT / 'config/zun_dispatcher_acceptance.json'
TASM = ['wine', r'C:\TASM50\bin\TASM32.EXE', '/m', '/mx', '/t']
MEMBER_ORDER = ('-O', '-I', '-S', '-G', '-M')
EXPECTED_SIZES = (926, 1009, 6564, 8377, 311)
# Ranges are **relative to the generated proof-local COM** with ORG 0100.
# Only these 558 bytes are reconstructed. The foreign 17187-byte gap is not.
CODE_SPANS = ((0, 2), (23, 223), (547, 550), (17737, 17745))
DATA_SPANS = ((2, 23), (223, 547))


def scope(config: dict) -> None:
    if (config.get('schema_version') != 1 or config.get('artifact') != 'th05-zun' or
            config.get('origin') != 'pipeline-reconstructed-assembly' or
            config.get('global_authored_credit') != 'unreviewed' or
            config.get('inner_start') != 0x12F or config.get('inner_prefix_size') != 550 or
            config.get('transfer_start') != 0x4678 or config.get('transfer_size') != 8 or
            config.get('child_hole_start') != 550 or
            config.get('child_hole_bytes') != sum(EXPECTED_SIZES) or
            config.get('full_proof_com_size') != 17745 or
            config.get('code_bytes') != sum(e-s for s,e in CODE_SPANS) or
            config.get('initialized_data_bytes') != sum(e-s for s,e in DATA_SPANS) or
            config.get('code_bytes') + config.get('initialized_data_bytes') != 558 or
            tuple(config['child_sizes'][n] for n in MEMBER_ORDER) != EXPECTED_SIZES or
            config.get('publics') != {
                'start': 0x100, 'entry': 0x117, 'print_procs': 0x133,
                'findentry': 0x166, 'fixup': 0x197,
                'proc_count': 0x1DF, 'proc_names': 0x1E1,
                'proc_entries': 0x2E1, 'moveup_indirect': 0x323,
                'member_O': 0x326, 'member_I': 0x6C4,
                'member_S': 0xAB5, 'member_G': 0x2459,
                'member_M': 0x4512, 'inner_moveup': 0x4649}):
        raise ValueError('invalid complete native dispatcher, table, or origin scope')
    # Assert physical ranges are a closed prefix and isolated eight-byte tail.
    sections = [(s,e) for s,e in CODE_SPANS + DATA_SPANS if s<550]
    sections.sort()
    if sections != [(0,2),(2,23),(23,223),(223,547),(547,550)]:
        raise ValueError('incomplete inner-stub CODE/message/directory partition')
    if CODE_SPANS[-1] != (17737,17745) or 550 + sum(EXPECTED_SIZES) != 17737:
        raise ValueError('children do not meet the original transfer endpoint')


def original(config: dict) -> tuple[bytes, bytes]:
    a = find_artifact(load_target_manifest(ROOT / 'config/targets.toml'), config['artifact'])
    raw = read_verified_artifact(ROOT, a)
    z = parse_launcher(raw, expected_sha256=a['sha256'])
    children = {row['name']:row for row in z['payloads']}
    for name, size in zip(MEMBER_ORDER, EXPECTED_SIZES):
        if name not in children or children[name]['size'] != size:
            raise ValueError('a pinned original foreign child has changed size')
    prefix = raw[config['inner_start']:config['inner_start']+config['inner_prefix_size']]
    helper = raw[config['transfer_start']:config['transfer_start']+config['transfer_size']]
    if digest_bytes(prefix) != config['inner_prefix_sha256'] or digest_bytes(helper) != config['transfer_sha256']:
        raise ValueError('original independent dispatcher code/catalog no longer matches')
    if children['-O']['file_start'] != 0x355 or children['-M']['file_end'] != 0x4678:
        raise ValueError('original source-owned scope touches a foreign child')
    return prefix, helper


def observe(work: Path, prefix: bytes, helper: bytes, config: dict) -> dict:
    candidate = (work / 'dispatch.com').read_bytes()
    if len(candidate) != 17745:
        raise ValueError('not the complete original-offset tiny COM source context')
    if any(candidate[550:17737]):
        raise ValueError('proof-local foreign child holes contain code or asset bytes')
    original_view = prefix + b'\0' * sum(EXPECTED_SIZES) + helper
    if len(original_view) != len(candidate):
        raise ValueError('proof-only staged source bounds diverge')
    code_exact = all(candidate[s:e] == original_view[s:e] for s,e in CODE_SPANS)
    data_exact = all(candidate[s:e] == original_view[s:e] for s,e in DATA_SPANS)
    # Assert the member offset table is *derived* from the five independently
    # grounded lengths and that all 27 unused entries remain semantically zero.
    n = int.from_bytes(candidate[223:225], 'little')
    names = [candidate[225+i*8:233+i*8].decode('ascii') for i in range(32)]
    pointers = [int.from_bytes(candidate[481+i*2:483+i*2], 'little') for i in range(33)]
    destinations = [0x326]
    for nbytes in EXPECTED_SIZES:
        destinations.append(destinations[-1] + nbytes)
    if (n != 5 or names[:5] != [n+' '*(8-len(n)) for n in MEMBER_ORDER] or
            names[5:] != [' '*8]*27 or pointers[:6] != destinations or
            pointers[6:] != [0]*27 or candidate[547:550] != prefix[547:550]):
        raise ValueError('source-owned dispatcher catalog is not the real five-child layout')
    obj=(work/'dispatch.obj').read_bytes()
    metadata=describe_omf(obj)
    if not metadata['valid'] or metadata['translator_comments'] != ['Turbo Assembler  Version 5.0']:
        raise ValueError('invalid real TASM source object')
    # The source may use OMF iterated data only for 27 blank name slots or
    # unused pointer slots; no member contents may be supplied in LEDATA.
    omf_records=parse_omf(obj)
    if len([z for z in omf_records if z.name == 'SEGDEF'])!=2:
        raise ValueError('unexpected real tiny-model CODE/DATA contexts')
    if len([z for z in omf_records if z.name == 'LIDATA'])!=2:
        raise ValueError('unexpected proof-source directory repetition layout')
    map_text=(work/'dispatch.map').read_text(encoding='cp437')
    for name,address in config['publics'].items():
        vals=re.findall(r'^\s*0000:([0-9A-F]{4})\s+(?:idle\s+)?'+re.escape(name)+r'\s*$',
                        map_text, re.M|re.I)
        if not vals or any(int(value,16)!=address for value in vals):
            raise ValueError('actual original runtime/public address changed: '+name)
    return {'size':len(candidate), 'source_owned_size':558,
            'code_bytes':213, 'initialized_data_bytes':345,
            'foreign_bytes':17187, 'foreign_zeroed':True,
            'prefix_exact':candidate[:550]==prefix,
            'transfer_exact':candidate[17737:]==helper,
            'code_exact':code_exact,'data_exact':data_exact,
            'prefix_sha256':digest_bytes(candidate[:550]),
            'transfer_sha256':digest_bytes(candidate[17737:]),
            'omf_normalized_sha256':metadata['dependency_timestamp_normalized_sha256'],
            'omf_sha256':metadata['sha256'],
            'map_sha256':digest_file(work/'dispatch.map')}


def run_round(directory: Path, source: str, prefix: bytes, helper: bytes,
              config: dict, negative: bool=False) -> dict:
    work=directory/'source';work.mkdir(parents=True,exist_ok=False)
    if negative:
        old,new=config['negative']['find'],config['negative']['replace']
        if not old or source.count(old)!=1 or old==new:
            raise ValueError('invalid source-level FCB copy negative')
        source=source.replace(old,new)
    (work/'dispatch.asm').write_text(source)
    (work/'build_dumb.bat').touch()
    b=Builder(work,ROOT/'.analysis/toolchain/wineprefix',ROOT/'_reference/ReC98/bin/msdos.exe')
    b.execute('assemble',[*TASM,'dispatch.asm','dispatch.obj'])
    (work/'link.rsp').write_bytes(b'-c -s -t dispatch.obj, dispatch.com, dispatch.map,\r\n')
    b.execute('link',['wine',str(b.msdos),'-e','-x','tlink','@link.rsp'])
    return observe(work,prefix,helper,config)


def check_record(x: dict,c: dict) -> None:
    if (x.get('manifest_sha256')!=digest_file(CONFIG) or
            x.get('source_sha256')!=digest_file(ROOT/c['source']) or
            x.get('toolchain_manifest_sha256')!=digest_file(ROOT/'config/toolchain.toml') or
            x.get('origin')!=c['origin'] or x.get('global_authored_credit')!='unreviewed'):
        raise ValueError('stale native source, manifest, compiler, or false global credit')
    rounds=x.get('rounds',[]);negative=x.get('negative_control',{})
    if (len(rounds)!=2 or any(not all(r[k] for k in (
                'prefix_exact','transfer_exact','code_exact','data_exact','foreign_zeroed')) or
            r['source_owned_size']!=558 or r['foreign_bytes']!=17187 or
            r['prefix_sha256']!=c['inner_prefix_sha256'] or
            r['transfer_sha256']!=c['transfer_sha256'] for r in rounds) or
            rounds[0]['omf_normalized_sha256']!=rounds[1]['omf_normalized_sha256'] or
            negative.get('code_exact') is not False or
            negative.get('prefix_exact') is not False or
            negative.get('transfer_exact') is not True or
            negative.get('data_exact') is not True or
            negative.get('foreign_zeroed') is not True):
        raise ValueError('missing two exact producers or valid semantic source negative')


def accept(path: Path,c: dict) -> None:
    receipt=json.loads(path.read_text())
    if receipt['manifest_sha256']!=digest_file(CONFIG) or digest_file(path.parent/'input.asm')!=receipt['source_sha256']:
        raise ValueError('input or manifest differs from native source run')
    toolpath=path.parent/'toolchain-attestation.json'
    tool=json.loads(toolpath.read_text())
    if (digest_file(toolpath)!=receipt['toolchain_receipt_sha256'] or
            tool['manifest_sha256']!=digest_file(ROOT/'config/toolchain.toml') or
            not all(tool[key] for key in ('ready','identity_pass','execution_pass'))):
        raise ValueError('native toolchain attestation changed')
    if 'toolchain_reuse_proof_sha256' in receipt:
        if digest_file(path.parent/'toolchain-reuse-proof.json')!=receipt['toolchain_reuse_proof_sha256']:
            raise ValueError('toolchain reuse proof changed')
    prefix,helper=original(c)
    for index,key in enumerate(('a','b')):
        if observe(path.parent/key/'source',prefix,helper,c)!=receipt['rounds'][index]:
            raise ValueError('saved native positive mismatch')
    if observe(path.parent/'negative/source',prefix,helper,c)!=receipt['negative_control']:
        raise ValueError('saved source negative mismatch')
    finalized={**receipt, 'replay_receipt_sha256':digest_file(path)}
    check_record(finalized,c)
    PUBLIC.write_text(json.dumps(finalized,indent=2)+'\n')


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--output',type=Path)
    mode.add_argument('--accept',type=Path)
    mode.add_argument('--check',action='store_true')
    args=parser.parse_args()
    config=tomllib.loads(CONFIG.read_text())
    scope(config)
    if args.check:
        check_record(json.loads(PUBLIC.read_text()),config)
        print('PASS: source-current ZUN inner dispatcher: 213 CODE + 345 directory/message, five children untouched')
        return 0
    if args.accept:
        accept(args.accept,config)
        print('PASS: accepted exact 550-byte dispatcher/catalog and separate 8-byte transfer')
        return 0
    out=args.output.resolve()
    if out.exists():parser.error('focused dispatcher output directory must be new')
    out.mkdir(parents=True)
    source=(ROOT/config['source']).read_bytes();text=source.decode('utf-8')
    (out/'input.asm').write_bytes(source)
    (out/'unit.toml').write_bytes(CONFIG.read_bytes())
    prefix,helper=original(config)
    with (ROOT/'.analysis/borland.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        t=freeze_toolchain(ROOT,out/'toolchain-attestation.json')
        positives=[run_round(out/key,text,prefix,helper,config) for key in ('a','b')]
        negative=run_round(out/'negative',text,prefix,helper,config,True)
    receipt={'schema_version':1,'kind':'focused-inner-zun-source-only-dispatcher-replay',
             'manifest_sha256':digest_file(CONFIG),
             'source_sha256':digest_bytes(source),
             'toolchain_manifest_sha256':digest_file(ROOT/'config/toolchain.toml'),
             'toolchain_receipt_sha256':digest_file(out/'toolchain-attestation.json'),
             'toolchain_reused':t['reused'],
             'toolchain_reuse_proof_sha256':t['proof_sha256'],
             'origin':config['origin'],'global_authored_credit':'unreviewed',
             'rounds':positives,'negative_control':negative}
    check_record(receipt,config)
    (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('PASS: two exact native dispatcher/code+catalog scopes and semantic negative:',out/'receipt.json')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
