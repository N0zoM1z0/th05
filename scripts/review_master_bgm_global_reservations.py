#!/usr/bin/env python3
"""Review complete noninitialized Master BGM SGLB structures in three original MZs.

Original archived B_DATA.ASM/BGM.INC explicitly declare SGLB members as ?;
no original TASM _DATA LEDATA writes any of these 108 bytes. This is not C++
initialized DATA, executable code, or an original authored zero-byte array.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re

from lib.omf import parse_omf
from lib.pc98 import parse_mz
from lib.unit_context import UnitContext, load_unit_target
from lib.unit_extents import _index
from lib.unit_oracle import relative_fixups
from review_master import need, pinned, sha, stored_lzh

ROOT = Path(__file__).resolve().parents[1]
PROOF = ROOT / 'config/reviewed_master_bgm_global_reservations.json'
PARENT = ROOT / 'config/master_vendor_ownership.json'
OTHER = ROOT / 'config/master_vendor_additions.json'
SPECS = {
    'main': ('main-calibration-b', 'main.obj', 0x21164, 0x21186, 0x0716, '209E:07A6'),
    'op': ('op-calibration-a', 'op.obj', 0xF8F4, 0xF8F4, 0x0442, '0EFE:0914'),
    'maine': ('maine-calibration-a', 'mainem.obj', 0x10702, 0x106F2, 0x0536, '1010:05F2'),
}
SIZE = 108


def original_source_shape(body: bytes, include: bytes, encoding: str='cp932', archived: bool=True) -> dict:
    text = body.decode(encoding)
    layout = include.decode(encoding)
    if archived:
        need(re.search(r'(?im)^\s*\.DATA\?\s*$', text) and
         re.search(r'(?im)^\s*timerorg\s+dd\s+\?\s*$', text) and
         re.search(r'(?im)^\s*part\s+SPART\s+PMAX\s+dup\s*\(<>\)\s*$', text) and
         re.search(r'(?im)^\s*esound\s+SESOUND\s+SMAX\s+dup\s*\(<>\)\s*$', text),
             'original Master BGM other uninitialized types differ')
    need(re.search(r'(?im)^\s*_bgm_glb\s+label\s+word\s*$', text) and
         re.search(r'(?im)^\s*glb\s+SGLB\s*<>\s*$', text) and
         (not archived or re.search(r'(?im)^\s*\.DATA\s*$', text)),
         'original Master BGM SGLB no longer has a source-default structure')
    need(len(re.findall(r'(?im)^\s*MMAX\s+equ\s+16\s*(?:;.*)?$',layout)) == 1,
         'original music track count differs from 16')
    block = re.search(r'(?ims)^\s*SGLB\s+struc\s*(.*?)^\s*SGLB\s+ends\s*$',layout)
    need(block is not None,'missing one complete original Master SGLB structure')
    cols = []
    for line in block.group(1).splitlines():
        definition = line.split(';',1)[0].strip()
        if not definition:
            continue
        match = re.fullmatch(r'([A-Za-z][A-Za-z0-9_]*)\s+(dw|dd)\s+(?:(MMAX)\s+dup\s*\(\s*\?\s*\)|\?)',definition,re.I)
        need(match is not None,'non-? initialized value in archived BGM global: '+definition)
        cols.append(dict(name=match[1],type=match[2].lower(),count=16 if match[3] else 1))
    width = sum((2 if c['type']=='dw' else 4)*c['count'] for c in cols)
    need(width==SIZE and len(cols)==23 and cols[-1]==dict(name='clockbase',type='dd',count=1),
         'Master BGM SGLB not exactly 108 question-mark storage bytes')
    return dict(bytes=width,field_count=len(cols),fields=cols)


def genuine_unwritten_omf(obj: bytes, start: int) -> dict:
    # This is the actual _DATA segment of the retained monolithic game TASM
    # object (segment index 2 in all three independently reviewed producers).
    records = parse_omf(obj)
    led = []
    for rec in records:
        if rec.name not in ('LEDATA','LIDATA'):
            continue
        seg, i = _index(rec.data,0)
        offset = int.from_bytes(rec.data[i:i+2],'little')
        if seg != 2:
            continue
        need(rec.name != 'LIDATA' or not (start <= offset < start+SIZE),
             'source has iterated TASM bytes beginning inside reserved BGM global')
        if rec.name != 'LEDATA':
            continue
        end = offset + len(rec.data) - i - 2
        need(end<=start or offset>=start+SIZE,
             'native original OMF _DATA LEDATA writes reserved BGM state')
        led.append((offset,end,rec.offset))
    before = [x for x in led if x[1]==start]
    after = [x for x in led if x[0]==start+SIZE]
    need(len(before)==1 and len(after)==1,
         'BGM SGLB is not exactly between complete source-initialized contributions')
    return dict(prior_initialized_end=start, next_initialized_start=start+SIZE,
                preceding_record_offset=before[0][2],following_record_offset=after[0][2],
                source_initialized_bytes=0,original_reserve_bytes=SIZE)


def review() -> dict:
    parent = json.loads(PARENT.read_text())
    other = json.loads(OTHER.read_text())
    archive = stored_lzh(pinned(ROOT,parent['inputs']['inner_archive']))
    author = original_source_shape(archive['B_DATA.ASM'],archive['BGM.INC'])
    rows=[]
    for name,(build,objname,original_start,cal_start,local,public) in SPECS.items():
        root=ROOT/'.analysis/builds'/build/'source'
        source=(root/'libs/master.lib/bgm[data].asm').read_bytes()
        header=(root/'libs/master.lib/bgm.inc').read_bytes()
        need(original_source_shape(source,header,'utf8',archived=False)==author,
             'reconstructed original BGM globals differ from archived author')
        pins=parent['inputs'] if name=='main' else other['table_contexts'][name]['inputs']
        obj=pinned(ROOT,pins['calibration_object'])
        mapping=pinned(ROOT,pins['calibration_map'])
        exe=pinned(ROOT,pins['calibration_exe'])
        linked=parse_mz(exe)
        c=UnitContext(ROOT,name)
        artifact,target,_=load_unit_target(c,c.config())
        need(linked.valid,'invalid retained calibration MZ')
        omf=genuine_unwritten_omf(obj,local)
        need(all(byte==0 for byte in target.program_image[original_start:original_start+SIZE]) and
             all(byte==0 for byte in linked.program_image[cal_start:cal_start+SIZE]),
             'uninitialized original BGM state no longer has matching materialized bytes')
        need(relative_fixups(target,original_start,SIZE)==relative_fixups(linked,cal_start,SIZE)==[],
             'BGM SGLB has unexpected loader segment fixups')
        for label in ('glb','_bgm_glb'):
            need(len(re.findall(r'(?im)^\s*'+public+r'\s+(?:idle\s+)?'+label+r'\s*$',
                                mapping.decode('cp437')))==2,
                 'actual BGM structure MAP public moved: '+name+' '+label)
        rows.append(dict(artifact=artifact['id'],start=original_start,end=original_start+SIZE,
                         original_sha256=artifact['sha256'],payload_sha256=sha(target.program_image),
                         native_source_sha256=sha(source),native_header_sha256=sha(header),
                         omf_sha256=sha(obj),map_sha256=sha(mapping),exe_sha256=sha(exe),
                         local_source_offset=local,source_unwritten_extent=omf,
                         ordered_original_MZ_fixups=[]))
    return dict(version=1,kind='source-linked-uninitialized-Master-SGLB',
                classification='reviewed-uninitialized-vendor-storage',
                total_reserve_bytes=3*SIZE,authored_credit=0,
                author_B_DATA_sha256=sha(archive['B_DATA.ASM']),
                author_BGM_INC_sha256=sha(archive['BGM.INC']),
                source_archive_sha256=parent['inputs']['inner_archive']['sha256'],
                original_structure=author,scopes=rows)


def validate(proof: dict):
    parent=json.loads(PARENT.read_text())
    other=json.loads(OTHER.read_text())
    archive=stored_lzh(pinned(ROOT,parent['inputs']['inner_archive']))
    source=original_source_shape(archive['B_DATA.ASM'],archive['BGM.INC'])
    need(proof.get('version')==1 and proof.get('kind')=='source-linked-uninitialized-Master-SGLB' and
         proof.get('classification')=='reviewed-uninitialized-vendor-storage' and
         proof.get('total_reserve_bytes')==3*SIZE and proof.get('authored_credit')==0 and
         proof.get('author_B_DATA_sha256')==sha(archive['B_DATA.ASM']) and
         proof.get('author_BGM_INC_sha256')==sha(archive['BGM.INC']) and
         proof.get('source_archive_sha256')==parent['inputs']['inner_archive']['sha256'] and
         proof.get('original_structure')==source and len(proof.get('scopes',[]))==3,
         'stale/unreviewed Master BGM global reserve provenance')
    for row,(name,(build,objname,start,cal,local,public)) in zip(proof['scopes'],SPECS.items()):
        pins=parent['inputs'] if name=='main' else other['table_contexts'][name]['inputs']
        info=other['table_contexts'][name] if name!='main' else None
        targethash=parent['inputs']['target']['sha256'] if name=='main' else info['target_sha256']
        payloadhash=parent['target_payload_sha256'] if name=='main' else info['target_payload_sha256']
        base=ROOT/'.analysis/builds'/build/'source/libs/master.lib'
        obj=pinned(ROOT,pins['calibration_object'])
        need(row.get('artifact')=='th05-'+name and row.get('start')==start and row.get('end')==start+SIZE and
             row.get('original_sha256')==targethash and row.get('payload_sha256')==payloadhash and
             row.get('native_source_sha256')==sha((base/'bgm[data].asm').read_bytes()) and
             row.get('native_header_sha256')==sha((base/'bgm.inc').read_bytes()) and
             row.get('omf_sha256')==pins['calibration_object']['sha256'] and
             row.get('map_sha256')==pins['calibration_map']['sha256'] and
             row.get('exe_sha256')==pins['calibration_exe']['sha256'] and
             row.get('local_source_offset')==local and
             row.get('source_unwritten_extent')==genuine_unwritten_omf(obj,local) and
             row.get('ordered_original_MZ_fixups')==[],
             'Master BGM global source, TASM gap or target identity changed')


def reviewed_claims(root,views,*,verify_targets=False):
    if not PROOF.exists():return {},None
    raw=PROOF.read_bytes();proof=json.loads(raw);validate(proof)
    if verify_targets:need(proof==review(),'original Master BGM SGLB source/native scope changed')
    claims={}
    for row in proof['scopes']:
        name=row['artifact'].removeprefix('th05-')
        need(views[name]['sha256']==row['payload_sha256'],
             'BGM global reserve source belongs to another target')
        claims[name]=[dict(start=row['start'],end=row['end'],
                           kind='reviewed-uninitialized-vendor-storage',
                           content_kind='source-question-mark-struct',
                           library='Master 0.23',member='BGM_GLB',
                           source='B_DATA.ASM/SGLB',
                           authored_credit=0,instruction_bytes=0)]
    return claims,sha(raw)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    g=parser.add_mutually_exclusive_group(required=True)
    for name in ('write','check','structural-check'):g.add_argument('--'+name,action='store_true')
    a=parser.parse_args()
    if a.write:
        record=review();PROOF.write_text(json.dumps(record,indent=2)+'\n')
    else:record=json.loads(PROOF.read_text())
    validate(record)
    if a.check:need(record==review(),'original Master BGM global proof changed')
    print('PASS: three complete 108-byte unwritten BGM globals, zero initialized source bytes')

if __name__=='__main__':main()
