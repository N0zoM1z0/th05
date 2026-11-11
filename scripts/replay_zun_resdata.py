#!/usr/bin/env python3
"""Focused exact local TASM/TLINK proof of ZUN -S Master graphics and resdata functions.

No other resident functions, CRT, original bytes, or full -S replay are used.
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
from lib.pc98 import digest_bytes,digest_file
from lib.reference_build import Builder
from lib.replay_toolchain import freeze_toolchain
from lib.targets import find_artifact,load_target_manifest,read_verified_artifact
from lib.unit_extents import _index as omf_index

ROOT=Path(__file__).resolve().parents[1]
CONFIG=ROOT/'config/zun_resdata.toml'
PUBLIC=ROOT/'config/zun_resdata_acceptance.json'
TASM=['wine',r'C:\TASM50\bin\TASM32.EXE','/m','/mx','/t']


def check_scope(c:dict)->None:
    if (c.get('schema_version')!=1 or c.get('artifact')!='th05-zun' or
            c.get('member')!='-S' or c.get('member_start')!=0x0ae4 or
            c.get('member_size')!=6564 or c.get('scope_start_com')!=0x5b6 or
            c.get('scope_end_com')!=0x698 or c.get('scope_bytes')!=226 or
            c.get('instruction_bytes')!=224 or c.get('uncredited_alignment_offsets')!=[35,225] or
            c.get('global_authored_credit')!='vendor-zero' or
            c.get('origin')!='pinned-master-library-original-assembly' or
            c.get('source')!='src/zun/resident/resdata_native.asm' or
            c.get('includes')!=['src/zun/resident/graph_clear_native.inc'] or
            c.get('publics')!={'GRAPH_CLEAR':0x5b6,'RESDATA_EXIST':0x5da,'RESDATA_CREATE':0x622,'resdata_end':0x698}):
        raise ValueError('unreviewed Master memory ABI/scope/ownership')


def native(c:dict)->bytes:
    art=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),c['artifact'])
    raw=read_verified_artifact(ROOT,art)
    p=next(z for z in parse_launcher(raw,expected_sha256=art['sha256'])['payloads'] if z['name']==c['member'])
    if (p['file_start'],p['size'])!=(c['member_start'],c['member_size']):
        raise ValueError('original embedded resident program boundary changed')
    return raw[p['file_start']+(0x5b6-0x100):p['file_start']+(0x698-0x100)]


def observe(work:Path,target:bytes,c:dict)->dict:
    data=(work/'resdata.com').read_bytes()
    if len(data)!=(0x698-0x100) or any(data[:0x5b6-0x100]):
        raise ValueError('foreign code offset contains initialized bytes')
    scope=data[0x5b6-0x100:0x698-0x100]
    if len(scope)!=226 or scope[35]!=0x90 or scope[-1]!=0x90:
        raise ValueError('incomplete function boundary or original EVEN padding')
    obj=describe_omf((work/'resdata.obj').read_bytes())
    if not obj['valid'] or obj['translator_comments']!=['Turbo Assembler  Version 5.0']:
        raise ValueError('invalid real TASM native object')
    records=parse_omf((work/'resdata.obj').read_bytes())
    segs=[r for r in records if r.name=='SEGDEF']
    if len(segs)!=2 or [struct.unpack_from('<H',r.data,1)[0] for r in segs]!=[0x698,0]:
        raise ValueError('incorrect CODE/DATA contribution')
    ledatas=[r for r in records if r.name=='LEDATA']
    if len(ledatas)!=2:
        raise ValueError('expected exactly two natural contiguous Master CODE LEDATA records')
    for record,offset,size in zip(ledatas,(0x5b6,0x5da),(36,190)):
        si,pos=omf_index(record.data,0)
        if (si,struct.unpack_from('<H',record.data,pos)[0],len(record.data)-pos-2)!=(1,offset,size):
            raise ValueError('one original Master CODE extent is incomplete or misplaced')
    text=(work/'resdata.map').read_text(encoding='cp437')
    for name,off in c['publics'].items():
        found=re.findall(r'^\s*0000:([0-9A-F]{4})\s+(?:idle\s+)?'+re.escape(name)+r'\s*$',text,re.M|re.I)
        if not found or any(int(v,16)!=off for v in found):
            raise ValueError('wrong original Master public '+name)
    return {'scope_exact':scope==target,'size':len(scope),'scope_sha256':digest_bytes(scope),
            'instruction_exact':scope[:35]+scope[36:225]==target[:35]+target[36:225],
            'alignment_exact':scope[35:36]==target[35:36] and scope[-1:]==target[-1:],
            'omf_normalized_sha256':obj['dependency_timestamp_normalized_sha256'],
            'map_sha256':digest_file(work/'resdata.map')}


def run_round(where:Path,source:str,target:bytes,c:dict,negative:bool)->dict:
    work=where/'source';work.mkdir(parents=True,exist_ok=False)
    if negative:
        old,new=c['negative']['find'],c['negative']['replace']
        if source.count(old)!=1:raise ValueError('negative source anchor missing')
        source=source.replace(old,new)
    (work/'resdata.asm').write_text(source)
    (work/'graph_clear_native.inc').write_bytes((ROOT/c['includes'][0]).read_bytes())
    (work/'build_dumb.bat').touch()
    b=Builder(work,ROOT/'.analysis/toolchain/wineprefix',ROOT/'_reference/ReC98/bin/msdos.exe')
    b.execute('assembler',[*TASM,'resdata.asm','resdata.obj'])
    (work/'link.rsp').write_bytes(b'-c -s -t resdata.obj, resdata.com, resdata.map,\r\n')
    b.execute('link',['wine',str(b.msdos),'-e','-x','tlink','@link.rsp'])
    return observe(work,target,c)


def check_record(x:dict,c:dict)->None:
    if (x.get('manifest_sha256')!=digest_file(CONFIG) or
            x.get('source_sha256')!=digest_file(ROOT/c['source']) or
            x.get('included_sha256')!=digest_file(ROOT/c['includes'][0]) or
            x.get('toolchain_manifest_sha256')!=digest_file(ROOT/'config/toolchain.toml') or
            x.get('origin')!=c['origin'] or x.get('global_authored_credit')!='vendor-zero'):
        raise ValueError('stale input or unreviewed vendor claim')
    pos=x.get('rounds',[]);neg=x.get('negative_control',{})
    if (len(pos)!=2 or any(not z['scope_exact'] or not z['instruction_exact'] or
            not z['alignment_exact'] or z['size']!=226 for z in pos) or
            pos[0]['omf_normalized_sha256']!=pos[1]['omf_normalized_sha256'] or
            neg.get('scope_exact') is not False or neg.get('instruction_exact') is not False or
            neg.get('alignment_exact') is not True):
        raise ValueError('exact native double-positive/negative is incomplete')


def main()->int:
    ap=argparse.ArgumentParser(description=__doc__)
    flags=ap.add_mutually_exclusive_group(required=True)
    flags.add_argument('--output',type=Path)
    flags.add_argument('--accept',type=Path)
    flags.add_argument('--check',action='store_true')
    args=ap.parse_args()
    config=tomllib.loads(CONFIG.read_text());check_scope(config)
    if args.check:
        check_record(json.loads(PUBLIC.read_text()),config)
        print('PASS: exact 226-byte ZUN -S Master graph clear and resident memory family')
        return 0
    if args.accept:
        path=args.accept.resolve();x=json.loads(path.read_text())
        if (x['manifest_sha256']!=digest_file(CONFIG) or digest_file(path.parent/'input.asm')!=x['source_sha256'] or
                digest_file(path.parent/'graph_clear_native.inc')!=x['included_sha256']):
            raise ValueError('stale source/manifest receipt')
        p=path.parent/'toolchain-attestation.json';tool=json.loads(p.read_text())
        if (digest_file(p)!=x['toolchain_receipt_sha256'] or
                tool['manifest_sha256']!=digest_file(ROOT/'config/toolchain.toml') or
                not all(tool[k] for k in ('ready','identity_pass','execution_pass'))):
            raise ValueError('native toolchain changed')
        if 'toolchain_reuse_proof_sha256' in x and digest_file(path.parent/'toolchain-reuse-proof.json')!=x['toolchain_reuse_proof_sha256']:
            raise ValueError('toolchain reuse proof changed')
        target=native(config)
        for k,i in (('a',0),('b',1)):
            if observe(path.parent/k/'source',target,config)!=x['rounds'][i]:
                raise ValueError('saved original producer differs')
        if observe(path.parent/'negative/source',target,config)!=x['negative_control']:
            raise ValueError('saved source negative differs')
        proof={**x,'replay_receipt_sha256':digest_file(path)}
        check_record(proof,config)
        PUBLIC.write_text(json.dumps(proof,indent=2)+'\n')
        print('PASS: source-built complete 226-byte Master graphics/resdata family accepted independently')
        return 0
    where=args.output.resolve()
    if where.exists():ap.error('focused output directory must be new')
    where.mkdir(parents=True)
    original=(ROOT/config['source']).read_bytes();text=original.decode('utf-8')
    (where/'input.asm').write_bytes(original)
    (where/'graph_clear_native.inc').write_bytes((ROOT/config['includes'][0]).read_bytes())
    (where/'unit.toml').write_bytes(CONFIG.read_bytes())
    target=native(config)
    with (ROOT/'.analysis/borland.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        tool=freeze_toolchain(ROOT,where/'toolchain-attestation.json')
        a,b=(run_round(where/k,text,target,config,False) for k in ('a','b'))
        negative=run_round(where/'negative',text,target,config,True)
    receipt={'schema_version':1,'kind':'bounded-standalone-master-vendor-asm',
             'manifest_sha256':digest_file(CONFIG),'source_sha256':digest_bytes(original),
             'included_sha256':digest_file(ROOT/config['includes'][0]),
             'toolchain_manifest_sha256':digest_file(ROOT/'config/toolchain.toml'),
             'toolchain_receipt_sha256':digest_file(where/'toolchain-attestation.json'),
             'toolchain_reused':tool['reused'],'toolchain_reuse_proof_sha256':tool['proof_sha256'],
             'origin':config['origin'],'global_authored_credit':'vendor-zero',
             'rounds':[a,b],'negative_control':negative}
    check_record(receipt,config)
    (where/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('PASS: exact 226-byte ZUN -S Master graphics/memory family + source negative:',where/'receipt.json')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
