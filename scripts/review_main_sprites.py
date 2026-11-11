#!/usr/bin/env python3
"""Recover MAIN preshifted sprite assets from original BMPs and bmp2arr.

Only four exact whole raw 1bpp BMP-derived tables are adopted as resources,
not source-generated CPU instructions. --check builds the actual preserved
bmp2arr twice, re-generates the exact native-compiled ASM includes and checks
their entire byte contents against original MAIN and calibration.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import tempfile

from lib.pc98 import digest_file, parse_mz
from lib.unit_oracle import relative_fixups
from review_master import need, pinned, sha

ROOT = Path(__file__).resolve().parents[1]
PROOF = ROOT/'config/main_sprite_resources.json'
DECISION = ROOT/'config/reviewed_main_sprite_resources.json'
MASTER = ROOT/'config/master_vendor_ownership.json'
RECPROJECT = ROOT/'_reference/ReC98'
MODEL = 'th05-main-bmp2arr-8px-1bpp-preshifted'
# The native layout is independently observed, not inferred by applying a
# uniform original-vs-calibration DATA delta. Complete source table extents:
# (name, original start, calibration start, total size, BMP relative path,
#  exported symbol, sprite height, preshift order)
SCOPE = (
 ('pointnum',0x2121a,0x21764,1536,'th04/sprites/pointnum.bmp','_sPOINTNUMS',8,'inner'),
 ('pellet',0x2181a,0x212a2,128,'th02/sprites/pellet.bmp','_sPELLET',8,'outer'),
 ('pellet-bottom',0x2189a,0x21322,64,'th04/sprites/pelletbt.bmp','_sPELLET_BOTTOM',4,'outer'),
 ('sparks',0x21e7a,0x21362,1024,'th02/sprites/sparks.bmp','_sSPARKS',8,'outer'),
)
GENERATOR = ('Pipeline/bmp2arr.c','Pipeline/bmp2arrl.c','Pipeline/bmp2arrl.h')
CALIBRATION_ROOT = ROOT/'.analysis/vendor-review/master-listing-a/source'


def generator_sources():
    return [{'path':str(Path('_reference/ReC98')/item),
             'size':(RECPROJECT/item).stat().st_size,
             'sha256':digest_file(RECPROJECT/item)}
            for item in GENERATOR]


def bitmap_bytes(text, symbol):
    # Generated ASM is data, not 16-bit executable instructions. Parse only
    # literal binary DB declarations; reject unexpected numeric syntax.
    need(len(re.findall(r'(?im)^public\s+'+re.escape(symbol)+r'\s*$',text))==1 and
         len(re.findall(r'(?im)^label\s+'+re.escape(symbol)+r'\s+byte\s*$',text))==1,
         'generator does not name exactly one expected sprite table')
    values=[]
    for line in text.splitlines():
        body=line.split(';',1)[0].strip()
        if not body:continue
        match=re.fullmatch(r'db\s+([01]{8}b(?:\s*,\s*[01]{8}b)*)',body,re.I)
        if match:
            values.extend(int(tok.strip()[:-1],2) for tok in match[1].split(','))
        elif re.match(r'^db(?:\s|$)',body,re.I):
            raise ValueError('unexpected sprite source literal; no target bytes are allowed')
    need(bool(values),'generated source contained no pixel rows')
    return bytes(values)


def regenerate(tmp, optimization):
    # Use the actual historical ReC98 generator, not a new source-pixel model
    # or a table copied out of the target. GNU __cdecl is only calling-conv
    # spelling on the native host; no source files are patched.
    compiler=tmp/('bmp2arr-'+optimization)
    run=subprocess.run(
        ['gcc','-std=gnu99','-w','-D__cdecl=','-'+optimization,
         '-o',str(compiler),*(str(RECPROJECT/p) for p in GENERATOR[:2])],
        cwd=ROOT,capture_output=True,text=True,check=True)
    need(compiler.is_file(), 'native ReC98 BMP-to-ASM producer not built')
    result={}
    for name,start,cal_start,length,bmp,symbol,height,preshift in SCOPE:
        output=tmp/(name+'-'+optimization+'.asp')
        subprocess.run([str(compiler),'-q','-i',bmp,'-o',str(output),
                        '-sym',symbol,'-of','asm','-sw','8','-sh',str(height),
                        '-pshf',preshift],
                       cwd=RECPROJECT,capture_output=True,text=True,check=True)
        generated=output.read_bytes()
        result[name]=(generated,bitmap_bytes(generated.decode('ascii'),symbol))
    return result


def replay():
    parent=json.loads(MASTER.read_text())
    calibrated=parse_mz(pinned(ROOT,parent['inputs']['calibration_exe']))
    original=parse_mz(pinned(ROOT,parent['inputs']['target']))
    need(original.valid and calibrated.valid and
         sha(original.program_image)==parent['target_payload_sha256'],
         'source review target is not the attested original MAIN')
    native_files={row['name']:row for row in parent['frozen_source_closure']}
    with tempfile.TemporaryDirectory(prefix='th05-sprites-') as tmpdir:
        temporary=Path(tmpdir)
        first=regenerate(temporary,'O0')
        second=regenerate(temporary,'O2')
    rows=[]
    for name,start,cal_start,size,bmp,symbol,height,preshift in SCOPE:
        asp=bmp.replace('.bmp','.asp')
        need(asp in native_files,'sprite source absent from original native OMF closure')
        retained=(CALIBRATION_ROOT/asp).read_bytes()
        need(sha(retained)==native_files[asp]['sha256'] and
             retained==first[name][0]==second[name][0],
             'BMP generator does not reproduce genuine compiled ASM input')
        pixels=first[name][1]
        need(pixels==second[name][1] and len(pixels)==size,
             'independently built BMP sprite generators disagree on complete table')
        need(pixels==original.program_image[start:start+size] and
             pixels==calibrated.program_image[cal_start:cal_start+size],
             'complete original/calibration pixel tables disagree with BMP source')
        need(original.program_image.find(pixels)==start and
             original.program_image.find(pixels,start+1)==-1,
             'native original BMP asset is not a unique full-length match')
        need(calibrated.program_image.find(pixels)==cal_start and
             calibrated.program_image.find(pixels,cal_start+1)==-1,
             'calibration source-bound BMP asset not uniquely placed')
        need(relative_fixups(original,start,size)==
             relative_fixups(calibrated,cal_start,size)==[],
             'native original BMP DATA contains unexpected ordered MZ fixups')
        bmpbytes=(RECPROJECT/bmp).read_bytes()
        need(bmpbytes[:2]==b'BM','source sprite must be a BMP, not a target table')
        rows.append({
            'id':'main-sprite-'+name,'name':name,
            'start':start,'end':start+size,'size':size,
            'calibration_start':cal_start,
            'source_bmp':str(Path('_reference/ReC98')/bmp),
            'bmp_size':len(bmpbytes),'bmp_sha256':sha(bmpbytes),
            'native_compiled_ASM':asp,
            'native_compiled_ASM_sha256':sha(retained),
            'compiled_pixel_table_sha256':sha(pixels),
            'original_pixel_table_sha256':sha(original.program_image[start:start+size]),
            'source_symbol':symbol,'height':height,'preshift':preshift,
            'original_ordered_MZ_fixups':[],
            'instruction_bytes':0,'authored_code_credit':0,
        })
    return {'schema_version':1,'kind':'original-BMP-generated-native-sprite-assets',
            'artifact':'th05-main','model':MODEL,
            'resources':rows,'sprite_data_bytes':sum(row['size'] for row in rows),
            'first_producer':'ReC98 bmp2arr gcc -O0','second_producer':'ReC98 bmp2arr gcc -O2',
            'generator_source_inputs':generator_sources(),
            'original_target_sha256':parent['inputs']['target']['sha256'],
            'original_target_payload_sha256':parent['target_payload_sha256'],
            'native_calibration_sha256':parent['inputs']['calibration_exe']['sha256'],
            'native_parent_review_sha256':digest_file(MASTER),
            'verifier_sha256':digest_file(ROOT/'scripts/review_main_sprites.py'),
            'instruction_bytes':0,'authored_code_credit':0,
            'other_bytes_claimed':0}


def validate_public(record):
    parent=json.loads(MASTER.read_text())
    need(record.get('schema_version')==1 and
         record.get('kind')=='original-BMP-generated-native-sprite-assets' and
         record.get('artifact')=='th05-main' and record.get('model')==MODEL and
         record.get('sprite_data_bytes')==sum(s[3] for s in SCOPE) and
         record.get('first_producer')=='ReC98 bmp2arr gcc -O0' and
         record.get('second_producer')=='ReC98 bmp2arr gcc -O2' and
         record.get('original_target_sha256')==parent['inputs']['target']['sha256'] and
         record.get('original_target_payload_sha256')==parent['target_payload_sha256'] and
         record.get('native_calibration_sha256')==parent['inputs']['calibration_exe']['sha256'] and
         record.get('native_parent_review_sha256')==digest_file(MASTER) and
         record.get('verifier_sha256')==digest_file(ROOT/'scripts/review_main_sprites.py') and
         record.get('instruction_bytes')==record.get('authored_code_credit')==
         record.get('other_bytes_claimed')==0,
         'unreviewed native sprite source, target or verifier')
    sources=record.get('generator_source_inputs')
    need(isinstance(sources,list) and len(sources)==len(GENERATOR) and
         [r.get('path') for r in sources]==[str(Path('_reference/ReC98')/f) for f in GENERATOR],
         'generator source identity list modified')
    for r in sources:
        need(type(r.get('size')) is int and r['size']>0 and
             isinstance(r.get('sha256'),str) and re.fullmatch('[0-9a-f]{64}',r['sha256']),
             'invalid native original-generator file identity')
    resources=record.get('resources')
    need(isinstance(resources,list) and len(resources)==len(SCOPE),
         'BMP source asset list altered')
    for row,(name,start,cal,size,bmp,sym,height,preshift) in zip(resources,SCOPE):
        need((row.get('id'),row.get('name'),row.get('start'),row.get('end'),
              row.get('size'),row.get('calibration_start'),
              row.get('source_bmp'),row.get('native_compiled_ASM'),
              row.get('source_symbol'),row.get('height'),row.get('preshift')) ==
             ('main-sprite-'+name,name,start,start+size,size,cal,
              str(Path('_reference/ReC98')/bmp),bmp.replace('.bmp','.asp'),
              sym,height,preshift) and
             row.get('original_ordered_MZ_fixups')==[] and
             row.get('instruction_bytes')==row.get('authored_code_credit')==0 and
             type(row.get('bmp_size')) is int and row['bmp_size']>0,
             'original BMP DATA extent/format/scope changed')
        for field in ('bmp_sha256','native_compiled_ASM_sha256',
                      'compiled_pixel_table_sha256','original_pixel_table_sha256'):
            need(isinstance(row.get(field),str) and
                 re.fullmatch('[0-9a-f]{64}',row[field]),
                 'missing or malformed source-derived whole-table digest')
        need(row['compiled_pixel_table_sha256']==row['original_pixel_table_sha256'],
             'source bytes do not match original pixel table')
    if DECISION.exists():
        decision=json.loads(DECISION.read_text())
        need(decision.get('schema_version')==1 and
             decision.get('artifact')=='th05-main' and
             decision.get('decision')=='ADOPT_ONLY_COMPLETE_BMP_SPRITE_TABLES' and
             decision.get('evidence_sha256')==digest_file(PROOF) and
             decision.get('resources')==[r['id'] for r in resources] and
             decision.get('sprite_data_bytes')==record['sprite_data_bytes'] and
             decision.get('instruction_bytes')==decision.get('authored_code_credit')==0 and
             decision.get('other_scopes_policy')=='unknown',
             'native resource adoption is missing, stale, or widened')


def reviewed_claims(root,view,*,verify_targets=False):
    if not DECISION.exists():return [],None
    need(root.resolve()==ROOT.resolve(),'wrong original sprite source checkout')
    proof=json.loads(PROOF.read_text());validate_public(proof)
    need(view['sha256']==proof['original_target_payload_sha256'],
         'original sprite resource belongs to another MAIN')
    if verify_targets:need(replay()==proof,'native source BMP reproduction differs')
    return ([{'start':r['start'],'end':r['end'],
              'kind':'reviewed-embedded-sprite-bitmap','resource':r['id'],
              'model':MODEL,'instruction_bytes':0,'authored_credit':0}
             for r in proof['resources']],digest_file(DECISION))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write',action='store_true')
    mode.add_argument('--check',action='store_true')
    mode.add_argument('--structural-check',action='store_true')
    args=parser.parse_args()
    if args.write:
        need(not PROOF.exists() and not DECISION.exists(),
             'refusing to overwrite original BMP evidence')
        result=replay()
        PROOF.write_text(json.dumps(result,indent=2)+'\n')
        print('PASS: native generated BMP source',result['sprite_data_bytes'],'complete resource bytes')
    else:
        result=json.loads(PROOF.read_text());validate_public(result)
        if args.check:
            need(replay()==result,'original sprite source BMP/native CODE evidence changed')
            print('PASS: generated BMP/ASM, source calibration, original MAIN pixel tables')
        else:
            print('PASS: public source-current BMP sprite review')


if __name__=='__main__':main()
