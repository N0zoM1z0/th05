#!/usr/bin/env python3
"""Classify the two complete native OP piano bitmaps from source, not target literals."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import struct

from lib.omf import parse_omf
from lib.pc98 import parse_mz
from lib.unit_context import UnitContext, load_unit_target
from lib.unit_oracle import relative_fixups
from review_master import need, sha

ROOT=Path(__file__).resolve().parents[1]
PROOF=ROOT/'config/op_piano_resources.json'
DECISION=ROOT/'config/reviewed_op_piano_resources.json'
ASM=ROOT/'_reference/ReC98/th05/op/piano[data].asm'
BMP=ROOT/'_reference/ReC98/th05/sprites/piano_l.bmp'
BASE=ROOT/'.analysis/builds/op-calibration-a/source'
ASP=BASE/'th05/sprites/piano_l.asp'
OBJ=BASE/'obj/th05/op2.obj'
MAP=BASE/'obj/th05/op.map'
EXE=BASE/'bin/th05/op.exe'
MODEL='th05-op-piano-native-1bpp'
SCOPES=(('op-piano-black-keys',0xf9ce,28,'reviewed-embedded-sprite-bitmap','_PIANO_KEYS_BLACK',0x09ee,0x0c),
        ('op-piano-label-glyphs',0xf9ea,72,'reviewed-embedded-font-bitmap','_sPIANO_LABEL_FONT',0x0a0a,0x28))


def key_pixels(source: bytes) -> bytes:
    text=source.decode('cp437')
    need(len(re.findall(r'(?m)^public _PIANO_KEYS_BLACK\s*$',text))==1,
         'piano black-key source public changed')
    lines=[m.group(1) for line in text.splitlines() if
           (m:=re.fullmatch(r'\s*db\s+([01]{8}b(?:\s*,\s*[01]{8}b){6})\s*',line.split(';',1)[0],re.I))]
    need(len(lines)==4,'original piano has not exactly four rows of seven bytes')
    values=[bytes(int(t.strip()[:-1],2) for t in line.split(',')) for line in lines]
    need(len(set(values))==1,'all four two-octave black-key lines must match')
    return b''.join(values)


def font_pixels(bmp: bytes) -> bytes:
    need(len(bmp)==158 and bmp[:2]==b'BM' and
         struct.unpack_from('<I',bmp,2)[0]==len(bmp) and
         struct.unpack_from('<I',bmp,10)[0]==62 and
         struct.unpack_from('<IiiHHI',bmp,14)==(40,72,8,1,1,0),
         'not the original 9x1 row of 8x8 monochrome piano glyphs')
    # BMP scanlines are bottom-up. Each glyph owns one 8-bit column of the
    # 72-pixel row, and 12 bytes of source scanline stride (32-bit padding).
    return bytes(bmp[62+(7-y)*12+glyph] for glyph in range(9) for y in range(8))


def asp_pixels(text: bytes) -> bytes:
    lines=text.decode('ascii').splitlines()
    need(sum('public _sPIANO_LABEL_FONT' in x for x in lines)==1 and
         sum('label _sPIANO_LABEL_FONT byte' in x for x in lines)==1,
         'retained BMP-to-ASM public label differs')
    pixels=[]
    for line in lines:
        s=line.split(';',1)[0].strip()
        if s.lower().startswith('db '):
            match=re.fullmatch(r'db\s+([01]{8})b',s,re.I)
            need(match is not None,'nonbinary glyph pixel literal in native ASM')
            pixels.append(int(match[1],2))
    need(len(pixels)==72,'native BMP-generated ASM is not 9 complete 8x8 glyphs')
    return bytes(pixels)


def review():
    key_raw=ASM.read_bytes();bmp_raw=BMP.read_bytes();asp_raw=ASP.read_bytes()
    source_pixels={'op-piano-black-keys':key_pixels(key_raw),
                   'op-piano-label-glyphs':font_pixels(bmp_raw)}
    need(source_pixels['op-piano-label-glyphs']==asp_pixels(asp_raw),
         'actual retained BMP-to-ASM source differs from independent BMP tile model')
    obj_raw=OBJ.read_bytes();records=parse_omf(obj_raw)
    # Genuine TASM object has a complete first _DATA LEDATA covering both
    # resources; unrelated BGIMAGE/sound words around them remain unowned here.
    matching=[]
    for rec in records:
        if rec.name=='LEDATA':
            b=rec.data
            if b[0]==2 and int.from_bytes(b[1:3],'little')==0:
                matching.append((rec.offset,b[3:]))
    need(len(matching)==1 and len(matching[0][1])==162,
         'original OP second native TASM _DATA LEDATA changed')
    need(not any(rec.name=='FIXUPP' for rec in records),
         'original OP piano resource object acquired unexpected FIXUPP')
    obj_record,led=matching[0]
    map_raw=MAP.read_bytes();map_text=map_raw.decode('cp437')
    cal=parse_mz(EXE.read_bytes());ctx=UnitContext(ROOT,'op')
    artifact,target,view=load_unit_target(ctx,ctx.config())
    need(cal.valid and target.valid,'original or calibrated OP image invalid')
    rows=[]
    for name,start,size,kind,symbol,ds_offset,local in SCOPES:
        source=source_pixels[name]
        need(len(source)==size and led[local:local+size]==source,
             'native TASM ordinary LEDATA does not contain the entire image')
        need(target.program_image[start:start+size]==source and
             cal.program_image[start:start+size]==source,
             'original/calibration full piano bitmap differs from independent source')
        need(target.program_image.find(source)==start and
             target.program_image.find(source,start+1)==-1,
             'source pixels are not uniquely located in original OP')
        need(relative_fixups(target,start,size)==relative_fixups(cal,start,size)==[],
             'piano pixel resource has actual MZ relocations')
        address=f'0EFE:{ds_offset:04X}'
        need(len(re.findall(r'(?im)^\s*'+address+r'\s+'+re.escape(symbol)+r'\s*$',map_text))==2,
             'original TASM MAP does not export exact piano bitmap symbol')
        rows.append(dict(resource=name,kind=kind,start=start,end=start+size,
                         size=size,symbol=symbol,data_sha256=sha(source),
                         data_DS_offset=ds_offset,object_LEDATA_offset=local,
                         object_LEDATA_record_offset=obj_record,
                         original_ordered_relocations=[],calibration_ordered_relocations=[]))
    return dict(schema_version=1,kind='native-source-linked-OP-piano-bitmaps',
                artifact=artifact['id'],model=MODEL,authored_credit=0,
                instruction_bytes=0,resource_bytes=100,
                target_sha256=artifact['sha256'],target_payload_sha256=sha(target.program_image),
                target_size=len(target.program_image),
                source_black_keys_sha256=sha(key_raw),source_font_BMP_sha256=sha(bmp_raw),
                retained_compiled_font_ASM_sha256=sha(asp_raw),
                actual_TASM_object_sha256=sha(obj_raw),actual_MAP_sha256=sha(map_raw),
                actual_calibration_EXE_sha256=sha(EXE.read_bytes()),
                complete_TASM_LED_includes_both=True,resources=rows)


def validate(proof):
    need(proof.get('schema_version')==1 and proof.get('kind')=='native-source-linked-OP-piano-bitmaps' and
         proof.get('artifact')=='th05-op' and proof.get('model')==MODEL and
         proof.get('authored_credit')==proof.get('instruction_bytes')==0 and
         proof.get('resource_bytes')==100 and proof.get('complete_TASM_LED_includes_both') is True and
         proof.get('source_black_keys_sha256')==sha(ASM.read_bytes()) and
         proof.get('source_font_BMP_sha256')==sha(BMP.read_bytes()) and
         proof.get('retained_compiled_font_ASM_sha256')==sha(ASP.read_bytes()) and
         proof.get('actual_TASM_object_sha256')==sha(OBJ.read_bytes()) and
         proof.get('actual_MAP_sha256')==sha(MAP.read_bytes()) and
         proof.get('actual_calibration_EXE_sha256')==sha(EXE.read_bytes()),
         'wrong native OP piano resource provenance')
    # Target identity is bound to the current accepted decoded OP proof by
    # ownership's view equality; never infer coordinates from the BMP alone.
    rows=proof.get('resources',[])
    need(len(rows)==2,'piano source inventory must have both complete resources')
    for row, (name,start,size,kind,symbol,ds_offset,local) in zip(rows,SCOPES):
        need(row.get('resource')==name and row.get('kind')==kind and
             row.get('start')==start and row.get('end')==start+size and
             row.get('size')==size and row.get('symbol')==symbol and
             row.get('data_DS_offset')==ds_offset and
             row.get('object_LEDATA_offset')==local and
             row.get('original_ordered_relocations')==[] and
             row.get('calibration_ordered_relocations')==[] and
             row.get('data_sha256')==sha(key_pixels(ASM.read_bytes()) if name=='op-piano-black-keys' else font_pixels(BMP.read_bytes())) and
             type(row.get('object_LEDATA_record_offset')) is int,
             'changed piano resource boundary, identity or content')


def reviewed_claims(root,views,*,verify_targets=False):
    if not (root/DECISION).exists():return {},None
    raw=(root/PROOF).read_bytes();proof=json.loads(raw);validate(proof)
    decision_raw=(root/DECISION).read_bytes()
    need(json.loads(decision_raw)==dict(schema_version=1,decision='ADOPT_ONLY_TWO_OP_PIANO_RESOURCES',
         classification='original-embedded-bitmap-resources',authored_credit=0,
         evidence_sha256=sha(raw),resources=[r['resource'] for r in proof['resources']]),
         'missing explicit original piano sprite/font resource adoption')
    need(views['op']['size']==proof['target_size'] and
         views['op']['sha256']==proof['target_payload_sha256'],
         'OP piano bitmaps belong to a different original decoder image')
    if verify_targets:need(review()==proof,'source-derived OP piano image bytes no longer match')
    return {'op':[dict(start=r['start'],end=r['end'],kind=r['kind'],resource=r['resource'],
                       model=MODEL,authored_credit=0,instruction_bytes=0)
                  for r in proof['resources']]},sha(decision_raw)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    g=p.add_mutually_exclusive_group(required=True)
    for flag in ('write','check','structural-check'):g.add_argument('--'+flag,action='store_true')
    a=p.parse_args()
    if a.write:
        j=review();PROOF.write_text(json.dumps(j,indent=2)+'\n')
        DECISION.write_text(json.dumps(dict(schema_version=1,
           decision='ADOPT_ONLY_TWO_OP_PIANO_RESOURCES',
           classification='original-embedded-bitmap-resources',authored_credit=0,
           evidence_sha256=sha(PROOF.read_bytes()),
           resources=[r['resource'] for r in j['resources']]),indent=2)+'\n')
    else:j=json.loads(PROOF.read_text())
    validate(j)
    if a.check:need(review()==j,'piano resource native replay changed')
    print('PASS: 28-byte black-key sprites + 72-byte original 8x8 piano label glyphs')


if __name__=='__main__':main()
