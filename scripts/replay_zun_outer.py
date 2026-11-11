#!/usr/bin/env python3
"""Strict ZUN.COM outer COMCSTM header/usage/stub source-only reconstruction.

The 17745-byte *inner program* is always a private zero ORG reservation.
Only the 303-byte source header/usage and complete 68-byte stub are compared.
"""
from __future__ import annotations

import argparse
import fcntl
import json
from pathlib import Path
import re
import struct
import tomllib

from lib.omf import describe_omf, parse_omf
from lib.pc98 import digest_bytes, digest_file
from lib.reference_build import Builder
from lib.replay_toolchain import freeze_toolchain
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from lib.unit_extents import _index as omf_index

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / 'config/zun_outer.toml'
PUBLIC = ROOT / 'config/zun_outer_acceptance.json'
TASM = ['wine', r'C:\TASM50\bin\TASM32.EXE', '/m', '/mx', '/t']
PUBLICS = {'outer_header':0x100, 'outer_usage':0x127,
           'inner_program_start':0x22F, 'outer_entry':0x4780,
           'outer_copy_up':0x47A8, 'outer_end':0x47C4}


def scope(config: dict) -> None:
    if (config.get('schema_version') != 1 or config.get('artifact') != 'th05-zun' or
            config.get('assembler_source') != 'src/zun/launcher/outer.asm' or
            config.get('usage_source') != 'src/zun/launcher/usage_ja.txt' or
            config.get('usage_encoding') != 'utf-8' or
            config.get('proof_only_assembler_include') != 'usage_private.inc' or
            config.get('origin') != 'third-party-comcstm-stub-reference' or
            config.get('global_authored_credit') != 'unreviewed' or
            config.get('header_size') != 39 or config.get('usage_size') != 264 or
            config.get('inner_start') != 0x12F or
            config.get('foreign_inner_size') != 17745 or
            config.get('wrapper_start') != 0x4680 or config.get('wrapper_size') != 68 or
            config.get('container_size') != 18116 or
            config.get('inner_start') + config.get('foreign_inner_size') != config.get('wrapper_start') or
            config.get('wrapper_start') + config.get('wrapper_size') != config.get('container_size') or
            config.get('code_bytes') != 71 or
            config.get('semantic_header_and_usage_bytes') != 300 or
            config.get('code_bytes') + config.get('semantic_header_and_usage_bytes') != 371 or
            config.get('publics') != PUBLICS):
        raise ValueError('outer header, usage, code, or zero-credit foreign extent changed')


def real_target(config: dict) -> tuple[bytes,bytes,bytes]:
    art = find_artifact(load_target_manifest(ROOT/'config/targets.toml'),config['artifact'])
    raw = read_verified_artifact(ROOT,art)
    if len(raw) != config['container_size']:
        raise ValueError('complete original outer file size changed')
    header,usage,wrapper = raw[:39],raw[39:303],raw[0x4680:0x46c4]
    for name,data in [('header',header),('usage',usage),('wrapper',wrapper)]:
        if digest_bytes(data) != config[name+'_sha256']:
            raise ValueError('attested original ' + name + ' bytes changed')
    if raw[:1] != b'\xE9' or int.from_bytes(raw[3:5],'little') != 0x127 or int.from_bytes(raw[5:7],'little') != 264 or int.from_bytes(raw[7:9],'little') != 17745:
        raise ValueError('incorrect authentic COMCSTM header semantics')
    return header,usage,wrapper


def usage_bytes(config: dict) -> bytes:
    source = (ROOT/config['usage_source']).read_text(encoding=config['usage_encoding'])
    if (not source.endswith('\n') or '\r' in source or source.count('\n') != 10 or
            source.count('␠') != 1 or '割り込みマスク␠\n' not in source or
            not source.startswith('\n')):
        raise ValueError('usage source must be a normalized Japanese UTF-8 text file')
    # The original reference has CRLF between lines and an isolated CR at EOF.
    # Derive that DOS input-file encoding from readable source, never from the
    # original packed program or copied target byte arrays.
    data = source.replace('␠', ' ').replace('\n','\r\n').encode('cp932')[:-1]
    if len(data) != config['usage_size'] or digest_bytes(data) != config['usage_sha256']:
        raise ValueError('original pinned Japanese help text encoding changed')
    return data


def private_include(usage: bytes) -> str:
    lines = ['; Generated privately from maintained readable Japanese help text.']
    for off in range(0,len(usage),16):
        lines.append('db ' + ','.join(f'0{b:02X}h' for b in usage[off:off+16]))
    return '\n'.join(lines) + '\n'


def observe(work: Path, target: tuple[bytes,bytes,bytes], config: dict) -> dict:
    actual = (work/'outer.com').read_bytes()
    if len(actual) != config['container_size'] or any(actual[303:0x4680]):
        raise ValueError('not an authentic-offset CODE producer with zeroed foreign inner')
    header,usage,wrapper=target
    if actual[39:303] != usage:
        raise ValueError('native usage differs from pinned source')
    obj = (work/'outer.obj').read_bytes()
    omf=describe_omf(obj)
    if not omf['valid'] or omf['translator_comments'] != ['Turbo Assembler  Version 5.0']:
        raise ValueError('not a verified native TASM object')
    records=parse_omf(obj)
    segs=[z for z in records if z.name=='SEGDEF']
    if len(segs)!=2 or [struct.unpack_from('<H',z.data,1)[0] for z in segs] != [0x47C4,0]:
        raise ValueError('the native tiny COM CODE/DATA segment extents differ')
    ledatas=[z for z in records if z.name=='LEDATA']
    if len(ledatas)!=2 or any(z.name in ('LIDATA','COMDAT','COMDAT32','LIDATA32') for z in records):
        raise ValueError('unexpected original CODE/usage payload or source compression')
    for z,offset,size in zip(ledatas,(0x100,0x4780),(303,68)):
        seg,at=omf_index(z.data,0)
        if (seg,struct.unpack_from('<H',z.data,at)[0],len(z.data)-at-2)!=(1,offset,size):
            raise ValueError('noncanonical complete original code-and-usage LEDATA')
    m=(work/'outer.map').read_text(encoding='cp437')
    for name,native in config['publics'].items():
        vals=re.findall(r'^\s*0000:([0-9A-F]{4})\s+(?:idle\s+)?'+re.escape(name)+r'\s*$',m,re.M|re.I)
        if not vals or any(int(n,16)!=native for n in vals):
            raise ValueError('original source-owned public address differs: '+name)
    return {'size':len(actual),'source_owned_size':371,'instruction_bytes':71,
            'header_and_help_data_bytes':300,'foreign_bytes':17745,'foreign_zeroed':True,
            'header_exact':actual[:39]==header,
            'usage_exact':actual[39:303]==usage,
            'wrapper_exact':actual[0x4680:]==wrapper,
            'code_exact':actual[:3]==header[:3] and actual[0x4680:]==wrapper,
            'data_exact':actual[3:303]==header[3:]+usage,
            'header_sha256':digest_bytes(actual[:39]),
            'usage_sha256':digest_bytes(actual[39:303]),
            'wrapper_sha256':digest_bytes(actual[0x4680:]),
            'omf_normalized_sha256':omf['dependency_timestamp_normalized_sha256'],
            'map_sha256':digest_file(work/'outer.map')}


def run_round(where: Path, source: str, usage: bytes,
              target: tuple[bytes,bytes,bytes],config: dict,
              *, negative: bool=False) -> dict:
    work=where/'source';work.mkdir(parents=True,exist_ok=False)
    if negative:
        old,new=config['negative']['find'],config['negative']['replace']
        if not old or source.count(old)!=1 or old==new:
            raise ValueError('invalid compiled outer-wrapper DOS-handle variation')
        source=source.replace(old,new)
    (work/'outer.asm').write_text(source)
    (work/config['proof_only_assembler_include']).write_text(private_include(usage))
    (work/'build_dumb.bat').touch()
    b=Builder(work,ROOT/'.analysis/toolchain/wineprefix',ROOT/'_reference/ReC98/bin/msdos.exe')
    b.execute('assembler',[*TASM,'outer.asm','outer.obj'])
    (work/'link.rsp').write_bytes(b'-c -s -t outer.obj, outer.com, outer.map,\r\n')
    b.execute('link',['wine',str(b.msdos),'-e','-x','tlink','@link.rsp'])
    return observe(work,target,config)


def check_record(x: dict,c: dict) -> None:
    if (x.get('manifest_sha256')!=digest_file(CONFIG) or
            x.get('source_sha256')!=digest_file(ROOT/c['assembler_source']) or
            x.get('usage_source_sha256')!=digest_file(ROOT/c['usage_source']) or
            x.get('toolchain_manifest_sha256')!=digest_file(ROOT/'config/toolchain.toml') or
            x.get('origin')!=c['origin'] or x.get('global_authored_credit')!='unreviewed'):
        raise ValueError('stale source/usage/toolchain or false global credit')
    pos=x.get('rounds',[]);n=x.get('negative_control',{})
    if (len(pos)!=2 or any(not all(z[k] for k in (
            'header_exact','usage_exact','wrapper_exact','code_exact','data_exact','foreign_zeroed')) or
            z['source_owned_size']!=371 or z['foreign_bytes']!=17745 or
            z['header_sha256']!=c['header_sha256'] or z['usage_sha256']!=c['usage_sha256'] or
            z['wrapper_sha256']!=c['wrapper_sha256'] for z in pos) or
            pos[0]['omf_normalized_sha256']!=pos[1]['omf_normalized_sha256'] or
            n.get('code_exact') is not False or n.get('wrapper_exact') is not False or
            n.get('header_exact') is not True or n.get('usage_exact') is not True or
            n.get('data_exact') is not True or n.get('foreign_zeroed') is not True):
        raise ValueError('missing two native exact positives or compiled semantic negative')


def accept(path: Path,c: dict) -> None:
    receipt=json.loads(path.read_text())
    if (receipt['manifest_sha256']!=digest_file(CONFIG) or
            digest_file(path.parent/'input.asm')!=receipt['source_sha256'] or
            digest_file(path.parent/'usage_ja.txt')!=receipt['usage_source_sha256']):
        raise ValueError('source or usage changed after native round')
    toolpath=path.parent/'toolchain-attestation.json'
    tool=json.loads(toolpath.read_text())
    if (digest_file(toolpath)!=receipt['toolchain_receipt_sha256'] or
            tool['manifest_sha256']!=digest_file(ROOT/'config/toolchain.toml') or
            not all(tool[z] for z in ('ready','identity_pass','execution_pass'))):
        raise ValueError('native toolchain attestation changed')
    if 'toolchain_reuse_proof_sha256' in receipt:
        if digest_file(path.parent/'toolchain-reuse-proof.json')!=receipt['toolchain_reuse_proof_sha256']:
            raise ValueError('native reuse proof changed')
    target,usage=real_target(c),usage_bytes(c)
    for i,k in enumerate(('a','b')):
        if observe(path.parent/k/'source',target,c)!=receipt['rounds'][i]:
            raise ValueError('stored positive producer differs')
    if observe(path.parent/'negative/source',target,c)!=receipt['negative_control']:
        raise ValueError('stored semantic negative differs')
    final={**receipt,'replay_receipt_sha256':digest_file(path)}
    check_record(final,c)
    PUBLIC.write_text(json.dumps(final,indent=2)+'\n')


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--output',type=Path)
    mode.add_argument('--accept',type=Path)
    mode.add_argument('--check',action='store_true')
    args=parser.parse_args()
    cfg=tomllib.loads(CONFIG.read_text());scope(cfg)
    if args.check:
        check_record(json.loads(PUBLIC.read_text()),cfg)
        print('PASS: source-current ZUN COMCSTM 68-byte wrapper + 303-byte header/usage; 17745 inner bytes foreign')
        return 0
    if args.accept:
        accept(args.accept,cfg)
        print('PASS: exact original outer header/usage/wrapper, two real producers and source negative')
        return 0
    out=args.output.resolve()
    if out.exists():parser.error('outer COMCSTM proof requires fresh output directory')
    out.mkdir(parents=True)
    source=(ROOT/cfg['assembler_source']).read_bytes()
    usage_source=(ROOT/cfg['usage_source']).read_bytes()
    (out/'input.asm').write_bytes(source)
    (out/'usage_ja.txt').write_bytes(usage_source)
    (out/'unit.toml').write_bytes(CONFIG.read_bytes())
    target=real_target(cfg)
    usage=usage_bytes(cfg)
    with (ROOT/'.analysis/borland.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        tool=freeze_toolchain(ROOT,out/'toolchain-attestation.json')
        pos=[run_round(out/key,source.decode('utf-8'),usage,target,cfg) for key in ('a','b')]
        neg=run_round(out/'negative',source.decode('utf-8'),usage,target,cfg,negative=True)
    receipt={'schema_version':1,'kind':'focused-zun-outer-comcstm-header-wrapper',
             'manifest_sha256':digest_file(CONFIG),'source_sha256':digest_bytes(source),
             'usage_source_sha256':digest_bytes(usage_source),
             'toolchain_manifest_sha256':digest_file(ROOT/'config/toolchain.toml'),
             'toolchain_receipt_sha256':digest_file(out/'toolchain-attestation.json'),
             'toolchain_reused':tool['reused'],
             'toolchain_reuse_proof_sha256':tool['proof_sha256'],
             'origin':cfg['origin'],'global_authored_credit':'unreviewed',
             'rounds':pos,'negative_control':neg}
    check_record(receipt,cfg)
    (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('PASS: two exact outer COMCSTM native producer scopes and source negative:',out/'receipt.json')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
