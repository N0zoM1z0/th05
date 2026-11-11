#!/usr/bin/env python3
"""Targeted ZUN -S C0T.OBJ source-origin replay in true DOS tiny layout.

Re-links the original pinned startup OMF with the *already accepted* two
config C++ objects, no C++ recompilation. The foreign _INIT_/BSS/linker
reservations emit no bytes. A two-byte runtime CS: scratch remains unknown.
"""
from __future__ import annotations

import argparse
import fcntl
import json
from pathlib import Path
import re
import shutil
import struct
import tomllib

from lib.launcher import parse_launcher
from lib.omf import parse_omf,describe_omf
from lib.pc98 import digest_bytes,digest_file
from lib.reference_build import Builder
from lib.replay_toolchain import freeze_toolchain
from lib.targets import find_artifact,load_target_manifest,read_verified_artifact
from lib.tiny_com import TINY_CRT_SHA256
from lib.unit_extents import _index as omf_index

ROOT=Path(__file__).resolve().parents[1]
CONFIG=ROOT/'config/zun_crt.toml'
PUBLIC=ROOT/'config/zun_crt_acceptance.json'
TASM=['wine',r'C:\TASM50\bin\TASM32.EXE','/m','/mx','/t']
NATIVE_MEMBER='-S'
HEADER_BIAS=0x100
CODE_BOUNDS=(0x100,0x367)
DATA_BOUNDS=(0x1650,0x16be)
UNWRITTEN=(0x363,0x365)
CRT_PROGRAM_CODE_BYTES=613


def scope(c:dict)->None:
    expected={'schema_version':1,'artifact':'th05-zun','member':'-S','member_start':0xae4,
              'member_size':6564,'source':'probes/units/zun_crt_layout_bindings.asm',
              'original_crt_object_sha256':TINY_CRT_SHA256,
              'accepted_cfg_unit':'zun-resident-config',
              'accepted_cfg_receipt':'.analysis/unit-replays/zun-cfg-322-b/receipt.json',
              'original_crt_com_start':0x100,'original_crt_com_end':0x367,
              'source_written_code_bytes':613,
              'unwritten_code_runtime_slot_start':0x363,
              'unwritten_code_runtime_slot_size':2,
              'original_crt_data_start':0x1650,'original_crt_data_end':0x16be,
              'source_written_data_bytes':110,'original_INIT_start':0x1a94,
              'original_INIT_size':0x12,'original_BSS_start':0x1aa6,
              'original_BSS_size':0x54,
              'origin':'original-borland-C0T-CRT-object',
              'global_authored_credit':'vendor-zero'}
    if any(c.get(k)!=v for k,v in expected.items()):
        raise ValueError('native C0T source, COM target, initialization or BSS scope changed')
    if (CODE_BOUNDS[1]-CODE_BOUNDS[0]!=c['source_written_code_bytes']+c['unwritten_code_runtime_slot_size']
            or DATA_BOUNDS[1]-DATA_BOUNDS[0]!=c['source_written_data_bytes']):
        raise ValueError('incorrect complete CRT CODE and DATA accounting')


def target(c:dict)->bytes:
    a=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),c['artifact'])
    raw=read_verified_artifact(ROOT,a)
    member=[z for z in parse_launcher(raw,expected_sha256=a['sha256'])['payloads'] if z['name']==NATIVE_MEMBER]
    if len(member)!=1 or (member[0]['file_start'],member[0]['size'])!=(0xae4,6564):
        raise ValueError('ZUN COM source child identity changed')
    out=raw[member[0]['file_start']:member[0]['file_end']]
    if out[0x263:0x265]!=b'\0\0' or bytes.fromhex('2e8e066303') not in out[:0x267]:
        raise ValueError('original writable CS runtime variable not verified')
    return out


def inspect_original_crt(obj:bytes)->dict:
    if digest_bytes(obj)!=TINY_CRT_SHA256:
        raise ValueError('original Borland C0T.OBJ changed')
    info=describe_omf(obj)
    if not info['valid'] or info['record_counts'].get('FIXUPP')!=2:
        raise ValueError('original CRT object structure or fixups differ')
    segments=[]
    blocks=[]
    for rec in parse_omf(obj):
        if rec.name=='SEGDEF':segments.append(int.from_bytes(rec.data[1:3],'little'))
        if rec.name=='LEDATA':
            segment,at=omf_index(rec.data,0)
            offset=struct.unpack_from('<H',rec.data,at)[0]
            data=rec.data[at+2:]
            blocks.append((segment,offset,len(data)))
    if len(segments)!=14 or segments[0]!=0x367 or segments[3]!=0x6e or blocks!=[
            (1,0x100,611),(1,0x365,2),(4,0,110)]:
        raise ValueError('actual original CRT source LEDATA or full SEGDEF changed')
    return {'object_sha256':digest_bytes(obj),'OMF_translation':info['translator_comments'],
            'CODE_OMF_LEDATA':[[1,0x100,611],[1,0x365,2]],
            'DATA_OMF_LEDATA':[[4,0,110]], 'source_code_bytes':613,
            'source_data_bytes':110,'unwritten_CODE':2,
            'ordered_OMF_FIXUPP_records':2}


def accepted_cfg_objects()->list[tuple[Path,str]]:
    ledger=json.loads((ROOT/'config/accepted_units.zun.json').read_text())
    unit=[z for z in ledger['units'] if z['id']=='zun-resident-config']
    if len(unit)!=1 or not unit[0]['result']['exact']:
        raise ValueError('native configuration function has no accepted C++ identity')
    receipt=ROOT/'.analysis/unit-replays/zun-cfg-322-b/receipt.json'
    if digest_file(receipt)!=unit[0]['replay_receipt_sha256']:
        raise ValueError('original accepted 322-byte configuration receipt no longer matches')
    pairs=[]
    for i,label in enumerate(('a','b')):
        path=receipt.parent/'group-0'/label/'source/zcfg.obj'
        expected=unit[0]['result']['omfs'][i]['sha256']
        if digest_file(path)!=expected:
            raise ValueError('original accepted native configuration object differs')
        pairs.append((path,expected))
    return pairs


def crt_regions(image:bytes)->tuple[bytes,bytes]:
    s,e=CODE_BOUNDS
    ds,de=DATA_BOUNDS
    # A plain COM has no MZ header: physical file positions are runtime-0100h.
    return image[s-HEADER_BIAS:e-HEADER_BIAS],image[ds-HEADER_BIAS:de-HEADER_BIAS]


def observe(directory:Path,original:bytes,c:dict)->dict:
    data=(directory/'units.com').read_bytes()
    code,init=crt_regions(data)
    target_code,target_init=crt_regions(original)
    if len(code)!=615 or len(init)!=110 or code[0x263:0x265]!=b'\0\0':
        raise ValueError('incomplete original CRT CODE/DATA or writable CS: state gap')
    if (directory/'c0t.obj').read_bytes()!=(ROOT/'.analysis/toolchain/installed/tc40j/LIB/C0T.OBJ').read_bytes():
        raise ValueError('producer CRT object changed')
    info=inspect_original_crt((directory/'c0t.obj').read_bytes())
    binder_obj=describe_omf((directory/'bindings.obj').read_bytes())
    if not binder_obj['valid'] or any(binder_obj['record_counts'].get(k,0)
                                     for k in ('LEDATA','LIDATA','COMDAT','COMDAT32')):
        raise ValueError('foreign linker layout supplied executable/data payload')
    mapping=(directory/'units.map').read_text(encoding='cp437')
    # Verify true original, separate Borland CRT / config / foreign segment
    # frames. In negatives the table may move, but source-owned CODE must not.
    for text in ('0000:0000 0367 C=CODE   S=_TEXT          G=DGROUP  M=c0.ASM',
                 '0000:0367 0142 C=CODE   S=_TEXT          G=DGROUP  M=th05/zcfg.cpp',
                 '0000:1650 006E C=DATA   S=_DATA          G=DGROUP  M=c0.ASM'):
        if text not in mapping:
            raise ValueError('real CRT/config CODE and DATA source frames differ')
    # TLINK's summary whitespace varies with the length of the segment
    # name; check its true segment bounds, not literal column padding.
    layout_exact=all(re.search(pattern,mapping,re.M|re.I) for pattern in (
        r'^\s*01A94H\s+01AA5H\s+00012H\s+_INIT_\s+INITDATA\s*$',
        r'^\s*01AA6H\s+01AF9H\s+00054H\s+_BSS\s+BSS\s*$'))
    cxx_cfg=tuple(data[0x367-0x100:0x4a9-0x100])
    original_cfg=tuple(original[0x367-0x100:0x4a9-0x100])
    return {'code_raw_exact':code==target_code,
            'code_source_written_exact':code[:0x263]==target_code[:0x263] and code[0x265:]==target_code[0x265:],
            'code_runtime_slot_unwritten':code[0x263:0x265]==b'\0\0',
            'DATA_exact':init==target_init,'accepted_cfg_exact':cxx_cfg==original_cfg,
            'real_INIT_BSS_layout':layout_exact,
            'code_sha256':digest_bytes(code),'data_sha256':digest_bytes(init),
            'size_source_owned':723,'CODE_source_owned':613,'DATA_source_owned':110,
            'unwritten_CS_state':2,'crt_object':info,
            'map_sha256':digest_file(directory/'units.map'),
            'candidate_size':len(data)}


def native_round(destination:Path,binder_source:str,cfg_obj:Path,original:bytes,
                 c:dict,negative:bool=False)->dict:
    destination.mkdir(parents=True,exist_ok=False)
    text=binder_source
    if negative:
        needle,after=c['negative']['find'],c['negative']['replace']
        if text.count(needle)!=1 or needle==after:
            raise ValueError('compiler layout negative is not a genuine source change')
        text=text.replace(needle,after)
    (destination/'bindings.asm').write_text(text)
    (destination/'build_dumb.bat').touch()
    shutil.copyfile(ROOT/'.analysis/toolchain/installed/tc40j/LIB/C0T.OBJ',destination/'c0t.obj')
    shutil.copyfile(cfg_obj,destination/'zcfg.obj')
    b=Builder(destination,ROOT/'.analysis/toolchain/wineprefix',ROOT/'_reference/ReC98/bin/msdos.exe')
    b.execute('assemble',[*TASM,'bindings.asm','bindings.obj'])
    (destination/'link.rsp').write_bytes(b'-c -s -t c0t.obj zcfg.obj bindings.obj, units.com, units.map,\r\n')
    b.execute('link',['wine',str(b.msdos),'-e','-x','tlink','@link.rsp'])
    return observe(destination,original,c)


def check_record(receipt:dict,c:dict)->None:
    ledger=json.loads((ROOT/'config/accepted_units.zun.json').read_text())
    accepted=[z for z in ledger['units'] if z['id']==c['accepted_cfg_unit']]
    if len(accepted)!=1 or not accepted[0]['result']['exact']:
        raise ValueError('original 322-byte C++ configuration producer is no longer accepted')
    expected_cfg=[z['sha256'] for z in accepted[0]['result']['omfs']]
    model=receipt.get('CRT_record_model',{})
    if (receipt.get('accepted_cfg_objects_sha256')!=expected_cfg or
            model.get('object_sha256')!=TINY_CRT_SHA256 or
            model.get('CODE_OMF_LEDATA')!=[[1,0x100,611],[1,0x365,2]] or
            model.get('DATA_OMF_LEDATA')!=[[4,0,110]] or
            model.get('ordered_OMF_FIXUPP_records')!=2 or
            model.get('unwritten_CODE')!=2):
        raise ValueError('original Borland CRT OMF or previously accepted C++ source identity changed')
    if (receipt.get('source_sha256')!=digest_file(ROOT/c['source']) or
            receipt.get('manifest_sha256')!=digest_file(CONFIG) or
            receipt.get('toolchain_manifest_sha256')!=digest_file(ROOT/'config/toolchain.toml') or
            receipt.get('CRT_object_sha256')!=TINY_CRT_SHA256 or
            receipt.get('origin')!=c['origin'] or receipt.get('global_authored_credit')!='vendor-zero'):
        raise ValueError('stale original CRT source/manifest/toolchain or made-up credit')
    pos=receipt.get('rounds',[]);negative=receipt.get('negative_control',{})
    if (len(pos)!=2 or any(not all(p[k] for k in ('code_raw_exact','code_source_written_exact',
                'code_runtime_slot_unwritten','DATA_exact','accepted_cfg_exact','real_INIT_BSS_layout'))
            or p['size_source_owned']!=723 or p['unwritten_CS_state']!=2 or
            p['crt_object'].get('object_sha256')!=TINY_CRT_SHA256 for p in pos) or
            pos[0]['code_sha256']!=pos[1]['code_sha256'] or
            pos[0]['data_sha256']!=pos[1]['data_sha256'] or
            negative.get('code_raw_exact') is not False or
            negative.get('DATA_exact') is not False or
            negative.get('accepted_cfg_exact') is not True or
            negative.get('code_runtime_slot_unwritten') is not True or
            negative.get('real_INIT_BSS_layout') is not False):
        raise ValueError('original C0T double-positive or real context negative incomplete')


def accept(path:Path,c:dict)->None:
    receipt=json.loads(path.read_text())
    if (receipt['manifest_sha256']!=digest_file(CONFIG) or
            digest_file(path.parent/'input.asm')!=receipt['source_sha256']):
        raise ValueError('recorded CRT segment source is stale')
    attestation=path.parent/'toolchain-attestation.json'
    tool=json.loads(attestation.read_text())
    if (digest_file(attestation)!=receipt['toolchain_receipt_sha256'] or
            tool['manifest_sha256']!=digest_file(ROOT/'config/toolchain.toml') or
            not all(tool[k] for k in ('ready','identity_pass','execution_pass'))):
        raise ValueError('original toolchain identity/probe differs')
    if 'toolchain_reuse_proof_sha256' in receipt:
        if digest_file(path.parent/'toolchain-reuse-proof.json')!=receipt['toolchain_reuse_proof_sha256']:
            raise ValueError('native reuse evidence changed')
    original=target(c)
    cfg_objects=accepted_cfg_objects()
    for i,k in enumerate(('a','b')):
        if observe(path.parent/k/'source',original,c)!=receipt['rounds'][i]:
            raise ValueError('positive CRT native producer differs from saved original comparison')
        if digest_file(path.parent/k/'source/zcfg.obj')!=cfg_objects[i][1]:
            raise ValueError('accepted cfg producer identity changed')
    if observe(path.parent/'negative/source',original,c)!=receipt['negative_control']:
        raise ValueError('compiled negative CRT layout producer differs')
    record={**receipt,'replay_receipt_sha256':digest_file(path)}
    check_record(record,c)
    PUBLIC.write_text(json.dumps(record,indent=2)+'\n')


def reviewed_claims(root:Path,view:dict,*,verify_targets:bool=False):
    """Public explicit adoption of only original CRT OMF LEDATA bytes."""
    decision_path=root/'config/reviewed_zun_crt.json'
    if not decision_path.exists():
        return [],None
    if root.resolve()!=ROOT.resolve():
        raise ValueError('CRT verifier is bound to the live checked-out root')
    c=tomllib.loads(CONFIG.read_text())
    scope(c)
    original=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),c['artifact'])
    if view.get('sha256')!=original['sha256'] or view.get('size')!=original['size']:
        raise ValueError('zun CRT ownership view differs from original ZUN.COM file')
    source=json.loads(PUBLIC.read_text())
    check_record(source,c)
    decision=json.loads(decision_path.read_text())
    if (decision.get('schema_version')!=1 or decision.get('artifact')!='th05-zun' or
            decision.get('decision')!='ADOPT_ONLY_REAL_C0T_OMF_SOURCE_WRITES' or
            decision.get('evidence_sha256')!=digest_file(PUBLIC) or
            decision.get('source_written_code_bytes')!=613 or
            decision.get('source_written_data_bytes')!=110 or
            decision.get('unwritten_code_bytes_claimed')!=0 or
            decision.get('authored_credit')!=0):
        raise ValueError('ZUN CRT vendor adoption has no current explicit decision')
    if verify_targets:
        member=target(c)
        for key,index in (('a',0),('b',1)):
            proof_dir=ROOT/'.analysis/zun-crt/gpt-web-crt-b'/key/'source'
            if observe(proof_dir,member,c)!=source['rounds'][index]:
                raise ValueError('original CRT retained producer no longer validates')
    root_offset=c['member_start']
    claims=[
        {'start':root_offset,'end':root_offset+0x263,'kind':'verified-vendor-code',
         'library':'C0T.OBJ','member':'C0T_STARTUP','content_kind':'original-CRT-CODE-LEDATA','authored_credit':0},
        {'start':root_offset+0x265,'end':root_offset+0x267,'kind':'verified-vendor-code',
         'library':'C0T.OBJ','member':'C0T_MODEL_WORD','content_kind':'original-CRT-CODE-LEDATA','authored_credit':0},
        {'start':root_offset+(0x1650-0x100),'end':root_offset+(0x16be-0x100),
         'kind':'verified-vendor-initialized-data','library':'C0T.OBJ','member':'C0T_DATA',
         'content_kind':'library-initialized-data','instruction_bytes':0,'authored_credit':0},
    ]
    return claims,digest_file(decision_path)


def main()->int:
    p=argparse.ArgumentParser(description=__doc__)
    mode=p.add_mutually_exclusive_group(required=True)
    mode.add_argument('--output',type=Path)
    mode.add_argument('--accept',type=Path)
    mode.add_argument('--check',action='store_true')
    args=p.parse_args();cfg=tomllib.loads(CONFIG.read_text());scope(cfg)
    if args.check:
        check_record(json.loads(PUBLIC.read_text()),cfg)
        print('PASS: source-current original ZUN -S CRT 613 CODE + 110 DATA; 2 runtime CS bytes unowned')
        return 0
    if args.accept:
        accept(args.accept.resolve(),cfg)
        print('PASS: complete original C0T startup vendor CODE/DATA accepted, no authored credit')
        return 0
    out=args.output.resolve()
    if out.exists():p.error('focused CRT replay requires a new output directory')
    out.mkdir(parents=True)
    source=(ROOT/cfg['source']).read_bytes();text=source.decode('utf-8')
    (out/'input.asm').write_bytes(source)
    (out/'unit.toml').write_bytes(CONFIG.read_bytes())
    original=target(cfg)
    c0t=inspect_original_crt((ROOT/'.analysis/toolchain/installed/tc40j/LIB/C0T.OBJ').read_bytes())
    accepted=accepted_cfg_objects()
    with (ROOT/'.analysis/borland.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        tool=freeze_toolchain(ROOT,out/'toolchain-attestation.json')
        pos=[native_round(out/k/'source',text,accepted[i][0],original,cfg)
             for i,k in enumerate(('a','b'))]
        neg=native_round(out/'negative/source',text,accepted[0][0],original,cfg,negative=True)
    receipt={'schema_version':1,'kind':'focused-pinned-borland-C0T-native-source-origin',
             'source_sha256':digest_bytes(source),'manifest_sha256':digest_file(CONFIG),
             'toolchain_manifest_sha256':digest_file(ROOT/'config/toolchain.toml'),
             'toolchain_receipt_sha256':digest_file(out/'toolchain-attestation.json'),
             'toolchain_reused':tool['reused'], 'toolchain_reuse_proof_sha256':tool['proof_sha256'],
             'CRT_object_sha256':TINY_CRT_SHA256,
             'accepted_cfg_objects_sha256':[x[1] for x in accepted],
             'CRT_record_model':c0t,
             'origin':cfg['origin'],'global_authored_credit':'vendor-zero',
             'rounds':pos,'negative_control':neg}
    check_record(receipt,cfg)
    (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('PASS: original CRT C0T.OBJ double native link, real INIT/BSS negative:',out/'receipt.json')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
