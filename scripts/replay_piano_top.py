#!/usr/bin/env python3
"""Focused native proof for the OP piano's 12-byte note-top geometry table.

This source owns CODE-class semantic DATA, never CPU instructions or a sprite.
The neighboring accepted piano ASM/C++ functions are not rebuilt.
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
from lib.pc98 import digest_bytes, digest_file, parse_mz
from lib.reference_build import Builder
from lib.replay_toolchain import freeze_toolchain
from lib.unit_context import UnitContext, load_unit_target
from lib.unit_extents import _index as omf_index
from lib.unit_oracle import relative_fixups

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/'src/op/piano/pressed_top.asm'
BINDER = ROOT/'probes/units/piano_pressed_top_bindings.asm'
ACCEPT = ROOT/'config/piano_pressed_top_acceptance.json'
START, SIZE, CS_BASE = 0xDB01, 12, 0xD300
NATIVE = ['wine', r'C:\TASM50\bin\TASM32.EXE', '/m', '/mx', '/t']
MODEL = ('PIANO_SHARP_OR_OUTER', 'PIANO_SHARP_OR_OUTER', 'PIANO_CENTER_WHITE',
         'PIANO_SHARP_OR_OUTER', 'PIANO_RIGHT_WHITE_EDGE', 'PIANO_SHARP_OR_OUTER',
         'PIANO_SHARP_OR_OUTER', 'PIANO_CENTER_WHITE', 'PIANO_SHARP_OR_OUTER',
         'PIANO_CENTER_WHITE', 'PIANO_SHARP_OR_OUTER', 'PIANO_RIGHT_WHITE_EDGE')


def source_model(source: bytes) -> bytes:
    text = source.decode('utf8')
    defs = dict(re.findall(r'^(PIANO_[A-Z_]+) equ ([0-9]+b|[0-9]+)$', text, re.M))
    if defs != {'PIANO_TOP_PLANE_SHIFT':'5', 'PIANO_SHARP_OR_OUTER':'110b',
                'PIANO_CENTER_WHITE':'010b','PIANO_RIGHT_WHITE_EDGE':'011b'}:
        raise ValueError('unreviewed piano top-mask geometry or plane shift')
    tokens = re.findall(r'^\s*db \((PIANO_[A-Z_]+) shl PIANO_TOP_PLANE_SHIFT\)\s*;', text, re.M)
    if tuple(tokens) != MODEL or len(re.findall(r'^\s*db\b',text,re.M)) != SIZE:
        raise ValueError('the twelve source bytes are not complete natural piano note geometry')
    values = {'PIANO_SHARP_OR_OUTER':0b110, 'PIANO_CENTER_WHITE':0b010,
              'PIANO_RIGHT_WHITE_EDGE':0b011}
    return bytes(values[token] << 5 for token in MODEL)


def target() -> tuple[bytes, str]:
    context=UnitContext(ROOT,'op')
    art,image,_=load_unit_target(context,context.config())
    if relative_fixups(image,START,SIZE):
        raise ValueError('the original 12-byte CODE table unexpectedly has MZ fixups')
    return image.program_image[START:START+SIZE],art['sha256']


def inspect(work: Path, expected:bytes, *,negative:bool=False) -> dict:
    image=parse_mz((work/'units.exe').read_bytes())
    if not image.valid:
        raise ValueError('not a valid real MZ producer')
    emitted=image.program_image[START:START+SIZE]
    if (len(emitted)!=SIZE or relative_fixups(image,START,SIZE)):
        raise ValueError('piano table producer length/relocation differs')
    desc=describe_omf((work/'sprite.obj').read_bytes())
    if not desc['valid'] or desc['translator_comments']!=['Turbo Assembler  Version 5.0']:
        raise ValueError('not the original TASM32 object format')
    rows=parse_omf((work/'sprite.obj').read_bytes())
    code=[r for r in rows if r.name=='LEDATA']
    if len(code)!=1 or any(r.name in ('LIDATA','FIXUPP','COMDAT','LEDATA32') for r in rows):
        raise ValueError('piano top producer must own one literal 12-byte CODE-class data record')
    seg,at=omf_index(code[0].data,0)
    if (seg,struct.unpack_from('<H',code[0].data,at)[0],len(code[0].data)-at-2)!=(3,0,SIZE):
        raise ValueError('actual table CODE OMF segment/LEDATA is not the complete 12-byte table')
    if code[0].data[at+2:] != (source_model(SOURCE.read_bytes()) if not negative else emitted):
        raise ValueError('positive source model and TASM-produced code table differ')
    mapping=(work/'units.map').read_text(encoding='cp437')
    if (not re.search(r'^\s*0D30:0801\s+000C\s+C=CODE\s+S=SHARED\s+G=\(none\)\s+M=sprite\.asm\b',mapping,re.M|re.I)
            or not re.search(r'^\s*0D30:0801\s+idle\s+PIANO_KEY_PRESSED_TOP\s*$',mapping,re.M|re.I)
            or not re.search(r'^\s*0D30:080D\s+idle\s+piano_pressed_top_end\s*$',mapping,re.M|re.I)):
        raise ValueError('actual CODE source/public boundaries are not the original 0D30:0801..080D')
    return {'size':SIZE,'exact':emitted==expected,'sha256':digest_bytes(emitted),
            'omf_normalized_sha256':desc['dependency_timestamp_normalized_sha256'],
            'object_sha256':desc['sha256'],'map_sha256':digest_file(work/'units.map')}


def roundtrip(work:Path, source:bytes, binder:bytes, target_bytes:bytes, mutate:bool=False)->dict:
    work.mkdir(parents=True,exist_ok=False)
    if mutate:
        before=b'PIANO_TOP_PLANE_SHIFT equ 5'
        if source.count(before)!=1:
            raise ValueError('piano source negative must change exactly one pixel plane')
        source=source.replace(before,b'PIANO_TOP_PLANE_SHIFT equ 4')
    (work/'sprite.asm').write_bytes(source)
    (work/'bindings.asm').write_bytes(binder)
    (work/'build_dumb.bat').touch()
    (work/'link.rsp').write_bytes(b'-c -s -E bindings.obj sprite.obj, units.exe, units.map,\r\n')
    builder=Builder(work,ROOT/'.analysis/toolchain/wineprefix',ROOT/'_reference/ReC98/bin/msdos.exe')
    for stem in ('bindings','sprite'):
        builder.execute('tasm-'+stem,[*NATIVE,stem+'.asm',stem+'.obj'])
    builder.execute('tlink',['wine',str(builder.msdos),'-e','-x','tlink','@link.rsp'])
    return inspect(work,target_bytes,negative=mutate)


def check_record(data:dict)->None:
    model=source_model(SOURCE.read_bytes())
    target_sha=next(x['sha256'] for x in tomllib.loads((ROOT/'config/targets.toml').read_text())['artifacts'] if x['id']=='th05-op')
    if (data.get('kind')!='focused-piano-top-semantic-CODE-data' or data.get('start')!=START or
            data.get('size')!=SIZE or data.get('instruction_bytes')!=0 or
            data.get('source_sha256')!=digest_file(SOURCE) or
            data.get('binder_sha256')!=digest_file(BINDER) or
            data.get('semantic_sha256')!=digest_bytes(model) or
            data.get('target_sha256')!=target_sha or
            data.get('toolchain_sha256')!=digest_file(ROOT/'config/toolchain.toml') or
            data.get('authored_table_bytes')!=SIZE):
        raise ValueError('stale source, semantic pixels, scope or native toolchain')
    positives=data.get('rounds',[])
    neg=data.get('negative',{})
    if (len(positives)!=2 or any(not z['exact'] or z['size']!=SIZE or
             z['sha256']!=digest_bytes(model) for z in positives) or
            positives[0]['omf_normalized_sha256']!=positives[1]['omf_normalized_sha256'] or
            neg.get('exact') is not False or neg.get('size')!=SIZE or
            neg.get('sha256')==digest_bytes(model)):
        raise ValueError('missing independent exact builds or pixel-plane source negative')


def reviewed_claims(root:Path,view:dict)->list[dict]:
    if root.resolve()!=ROOT.resolve() or not ACCEPT.exists():return []
    data=json.loads(ACCEPT.read_text())
    check_record(data)
    if view['sha256']!=data['target_image_sha256'] or view['size']<=START+SIZE:
        raise ValueError('accepted piano table belongs to another OP image')
    return [{'start':START,'end':START+SIZE,
             'kind':'accepted-reviewed-asm-semantic-code-table',
             'unit':'op-piano-pressed-top',
             'origin':'reviewed-native-handwritten-assembly-reconstruction'}]


def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    modes=p.add_mutually_exclusive_group(required=True)
    modes.add_argument('--output',type=Path)
    modes.add_argument('--accept',type=Path)
    modes.add_argument('--check',action='store_true')
    args=p.parse_args()
    if args.check:
        check_record(json.loads(ACCEPT.read_text()))
        print('PASS: exact source-current 12-byte OP semantic piano key-top CODE table')
        return
    if args.accept:
        receipt=json.loads(args.accept.read_text())
        if (receipt['source_sha256']!=digest_file(SOURCE) or
                receipt['binder_sha256']!=digest_file(BINDER) or
                receipt['toolchain_sha256']!=digest_file(ROOT/'config/toolchain.toml')):
            raise ValueError('original saved source/toolchain changed')
        expected,_=target()
        original=SOURCE.read_bytes()
        changed=original.replace(b'PIANO_TOP_PLANE_SHIFT equ 5',b'PIANO_TOP_PLANE_SHIFT equ 4')
        if original.count(b'PIANO_TOP_PLANE_SHIFT equ 5')!=1:
            raise ValueError('the meaningful source mutation no longer exists')
        if (args.accept.parent/'negative/source/sprite.asm').read_bytes()!=changed:
            raise ValueError('saved negative source is not the real 5-to-4 plane mutation')
        for name in ('a','b'):
            directory=args.accept.parent/name/'source'
            if ((directory/'sprite.asm').read_bytes()!=original or
                    (directory/'bindings.asm').read_bytes()!=BINDER.read_bytes()):
                raise ValueError('saved positive source/binder differs from maintained source')
        for index,name in enumerate(('a','b')):
            if inspect(args.accept.parent/name/'source',expected)!=receipt['rounds'][index]:
                raise ValueError('saved original full positive producer differs')
        if inspect(args.accept.parent/'negative/source',expected,negative=True)!=receipt['negative']:
            raise ValueError('saved native source negative differs')
        check_record(receipt)
        ACCEPT.write_text(json.dumps({**receipt,'receipt_sha256':digest_file(args.accept)},indent=2)+'\n')
        print('PASS: source-backed original piano top semantic CODE table accepted')
        return
    work=args.output.resolve()
    if work.exists():p.error('use a fresh affected-unit replay directory')
    work.mkdir(parents=True)
    original,target_sha=target()
    source,binder=SOURCE.read_bytes(),BINDER.read_bytes()
    if source_model(source)!=original:raise ValueError('pinned semantic piano mask model does not match native bytes')
    with (ROOT/'.analysis/borland.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        rounds=[roundtrip(work/name/'source',source,binder,original) for name in ('a','b')]
        neg=roundtrip(work/'negative/source',source,binder,original,mutate=True)
    data={'kind':'focused-piano-top-semantic-CODE-data','start':START,'size':SIZE,
          'instruction_bytes':0,'authored_table_bytes':SIZE,
          'source_sha256':digest_bytes(source),'binder_sha256':digest_bytes(binder),
          'semantic_sha256':digest_bytes(original),'target_sha256':target_sha,
          'target_image_sha256':digest_bytes(load_unit_target(UnitContext(ROOT,'op'),UnitContext(ROOT,'op').config())[1].program_image),
          'toolchain_sha256':digest_file(ROOT/'config/toolchain.toml'),
          'rounds':rounds,'negative':neg}
    check_record(data)
    (work/'receipt.json').write_text(json.dumps(data,indent=2)+'\n')
    print('PASS: two full 12-byte TASM/TLINK positives + real plane-change negative:',work/'receipt.json')

if __name__=='__main__':main()
