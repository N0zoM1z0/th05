#!/usr/bin/env python3
"""Strict focused TASM32/TLINK proof of nine ZUN -S Master file functions.

Only nine full functions at COM 0698..0970 are native source-owned.
All source-free code, DOS helper providers, and DATA/BSS are external.
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
from lib.omf import describe_omf,parse_omf
from lib.pc98 import digest_bytes,digest_file
from lib.reference_build import Builder
from lib.replay_toolchain import freeze_toolchain
from lib.targets import find_artifact,load_target_manifest,read_verified_artifact
from lib.unit_extents import _index as omf_index

ROOT=Path(__file__).resolve().parents[1]
CONFIG=ROOT/'config/zun_file_native.toml'
PUBLIC=ROOT/'config/zun_file_native_acceptance.json'
TASM=['wine',r'C:\TASM50\bin\TASM32.EXE','/m','/mx','/t']
FILENAMES={'file_family_native.asm':'filefamily.asm','master_file_tiny.inc':'master_file_tiny.inc',
           'master_read.inc':'master_read.inc','master_close.inc':'master_close.inc',
           'master_ropen.inc':'master_ropen.inc',
           'master_write.inc':'master_write.inc','master_create.inc':'master_create.inc',
           'master_seek.inc':'master_seek.inc','master_append.inc':'master_append.inc'}
PUBS={'FILE_READ':0x698,'FILE_FLUSH':0x74c,'FILE_CLOSE':0x7b8,'FILE_ROPEN':0x7c6,
      'FILE_WRITE':0x7fc,'FILE_CREATE':0x8a2,'FILE_SEEK':0x8de,
      'FILE_TELL':0x912,'FILE_APPEND':0x920}


def scope(c:dict)->None:
    if (c.get('schema_version')!=1 or c.get('artifact')!='th05-zun' or
            c.get('member')!='-S' or c.get('member_start')!=0x0ae4 or
            c.get('member_size')!=6564 or (c.get('start_com'),c.get('end_com'))!=(0x698,0x970) or
            c.get('scope_size')!=728 or c.get('instruction_bytes')!=723 or
            c.get('uncredited_alignment_offsets')!=[131,287,473,581,633] or
            c.get('origin')!='pinned-master-library-original-assembly' or
            c.get('global_authored_credit')!='vendor-zero' or
            c.get('source')!='src/zun/resident/file_family_native.asm' or
            c.get('includes')!=['src/zun/resident/'+x for x in (
                'master_file_tiny.inc','master_read.inc','master_close.inc','master_ropen.inc',
                'master_write.inc','master_create.inc','master_seek.inc','master_append.inc')] or
            c.get('publics')!=PUBS or c.get('negative',{}).get('file')!=c['includes'][1]):
        raise ValueError('unreviewed source, vendor or actual native file-function scope')


def input_hashes(c:dict)->dict:
    return {name:digest_file(ROOT/name) for name in [c['source'],*c['includes']]}


def original(c:dict)->bytes:
    a=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),c['artifact'])
    raw=read_verified_artifact(ROOT,a)
    child=next(z for z in parse_launcher(raw,expected_sha256=a['sha256'])['payloads'] if z['name']=='-S')
    if (child['file_start'],child['size'])!=(c['member_start'],c['member_size']):
        raise ValueError('original ZUN -S complete member identity changed')
    return raw[child['file_start']+(0x698-0x100):child['file_start']+(0x970-0x100)]


def observe(where:Path,target:bytes,c:dict)->dict:
    data=(where/'filefamily.com').read_bytes()
    st,en=0x698-0x100,0x970-0x100
    if len(data)<en or any(data[:st]) or any(data[en:]):
        raise ValueError('original foreign code/DGROUP values were supplied by this unit')
    body=data[st:en]
    if len(body)!=728 or any(body[i]!=0x90 for i in (131,287,473,581,633)):
        raise ValueError('missing whole functions or original linker EVEN padding')
    obj=(where/'filefamily.obj').read_bytes();omf=describe_omf(obj)
    if not omf['valid'] or omf['translator_comments']!=['Turbo Assembler  Version 5.0']:
        raise ValueError('incorrect native assembler or invalid object')
    records=parse_omf(obj);segs=[z for z in records if z.name=='SEGDEF']
    if len(segs)!=2 or [struct.unpack_from('<H',z.data,1)[0] for z in segs]!=[0x16be,0x3fa]:
        raise ValueError('fake original CODE/DGROUP frame for real DOS pointers')
    ledatas=[z for z in records if z.name=='LEDATA']
    if len(ledatas)!=1:
        raise ValueError('source emits invented initialized data or extra owned code')
    seg,at=omf_index(ledatas[0].data,0)
    if (seg,struct.unpack_from('<H',ledatas[0].data,at)[0],len(ledatas[0].data)-at-2)!=(1,0x698,728):
        raise ValueError('wrong original complete family LEDATA')
    mapping=(where/'filefamily.map').read_text(encoding='cp437')
    for name,off in c['publics'].items():
        matched=re.findall(r'^\s*0000:([0-9A-F]{4})\s+(?:idle\s+)?'+re.escape(name)+r'\s*$',
                           mapping,re.M|re.I)
        if not matched or any(int(v,16)!=off for v in matched):
            raise ValueError('real original Master function boundary differs '+name)
    def instructions(x:bytes)->bytes:
        return bytes(value for index,value in enumerate(x) if index not in (131,287,473,581,633))
    return {'size':len(body),'scope_exact':body==target,
            'scope_sha256':digest_bytes(body),
            'instruction_exact':instructions(body)==instructions(target),
            'alignment_exact':all(body[i]==target[i] for i in (131,287,473,581,633)),
            'source_code_extent':728,'source_instruction_bytes':723,
            'foreign_zeroed':True,
            'omf_normalized_sha256':omf['dependency_timestamp_normalized_sha256'],
            'map_sha256':digest_file(where/'filefamily.map')}


def roundtrip(dest:Path,c:dict,target:bytes,negative:bool)->dict:
    dest.mkdir(parents=True,exist_ok=False)
    for original,compiled in FILENAMES.items():
        path=ROOT/'src/zun/resident'/original
        text=path.read_text(encoding='utf8')
        if negative and c['negative']['file']==f'src/zun/resident/{original}':
            old,new=c['negative']['find'],c['negative']['replace']
            if text.count(old)!=1 or old==new:
                raise ValueError('semantic native source negative is not unique')
            text=text.replace(old,new)
        (dest/compiled).write_text(text)
    (dest/'build_dumb.bat').touch()
    b=Builder(dest,ROOT/'.analysis/toolchain/wineprefix',ROOT/'_reference/ReC98/bin/msdos.exe')
    b.execute('assemble',[*TASM,'filefamily.asm','filefamily.obj'])
    (dest/'link.rsp').write_bytes(b'-c -s -t filefamily.obj, filefamily.com, filefamily.map,\r\n')
    b.execute('link',['wine',str(b.msdos),'-e','-x','tlink','@link.rsp'])
    return observe(dest,target,c)


def check(x:dict,c:dict)->None:
    if (x.get('manifest_sha256')!=digest_file(CONFIG) or
            x.get('source_hashes')!=input_hashes(c) or
            x.get('toolchain_manifest_sha256')!=digest_file(ROOT/'config/toolchain.toml') or
            x.get('origin')!=c['origin'] or x.get('global_authored_credit')!='vendor-zero'):
        raise ValueError('stale file-function source/manifest or false authored credit')
    pos=x.get('rounds',[]);neg=x.get('negative_control',{})
    if (len(pos)!=2 or any(not all(z[q] for q in ('scope_exact','instruction_exact','alignment_exact','foreign_zeroed'))
            or z['size']!=728 for z in pos) or
            pos[0]['omf_normalized_sha256']!=pos[1]['omf_normalized_sha256'] or
            neg.get('scope_exact') is not False or neg.get('instruction_exact') is not False or
            neg.get('alignment_exact') is not True or neg.get('foreign_zeroed') is not True):
        raise ValueError('missing complete native double-positive and compiled semantic negative')


def main()->int:
    parser=argparse.ArgumentParser(description=__doc__)
    flags=parser.add_mutually_exclusive_group(required=True)
    flags.add_argument('--output',type=Path)
    flags.add_argument('--accept',type=Path)
    flags.add_argument('--check',action='store_true')
    args=parser.parse_args();c=tomllib.loads(CONFIG.read_text());scope(c)
    if args.check:
        check(json.loads(PUBLIC.read_text()),c)
        print('PASS: exact 728-byte ZUN -S Master file I/O family, vendor zero credit')
        return 0
    if args.accept:
        p=args.accept.resolve();x=json.loads(p.read_text())
        if (x.get('manifest_sha256')!=digest_file(CONFIG) or
                x.get('source_hashes')!=input_hashes(c)):
            raise ValueError('stale source unit manifest')
        att=p.parent/'toolchain-attestation.json';t=json.loads(att.read_text())
        if (digest_file(att)!=x['toolchain_receipt_sha256'] or
                t['manifest_sha256']!=digest_file(ROOT/'config/toolchain.toml') or
                not all(t[k] for k in ('ready','identity_pass','execution_pass'))):
            raise ValueError('native toolchain attestation changed')
        if 'toolchain_reuse_proof_sha256' in x and digest_file(p.parent/'toolchain-reuse-proof.json')!=x['toolchain_reuse_proof_sha256']:
            raise ValueError('native toolchain reuse proof differs')
        target=original(c)
        if [observe(p.parent/k/'source',target,c) for k in ('a','b')]!=x['rounds']:
            raise ValueError('saved positive native producers differ')
        if observe(p.parent/'negative/source',target,c)!=x['negative_control']:
            raise ValueError('saved negative source assembly differs')
        finalized={**x,'replay_receipt_sha256':digest_file(p)}
        check(finalized,c)
        PUBLIC.write_text(json.dumps(finalized,indent=2)+'\n')
        print('PASS: exact nine-function vendor file I/O family accepted')
        return 0
    out=args.output.resolve()
    if out.exists():parser.error('only a new focused replay directory is valid')
    out.mkdir(parents=True)
    (out/'unit.toml').write_bytes(CONFIG.read_bytes())
    target=original(c)
    with (ROOT/'.analysis/borland.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        att=freeze_toolchain(ROOT,out/'toolchain-attestation.json')
        pos=[roundtrip(out/k/'source',c,target,False) for k in ('a','b')]
        neg=roundtrip(out/'negative/source',c,target,True)
    receipt={'schema_version':1,'kind':'focused-zun-s-master-file-io-family',
             'manifest_sha256':digest_file(CONFIG),'source_hashes':input_hashes(c),
             'toolchain_manifest_sha256':digest_file(ROOT/'config/toolchain.toml'),
             'toolchain_receipt_sha256':digest_file(out/'toolchain-attestation.json'),
             'toolchain_reused':att['reused'],'toolchain_reuse_proof_sha256':att['proof_sha256'],
             'origin':c['origin'],'global_authored_credit':'vendor-zero',
             'rounds':pos,'negative_control':neg}
    check(receipt,c)
    (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('PASS: two exact 728-byte nine-function Master file native producers + negative:',out/'receipt.json')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
