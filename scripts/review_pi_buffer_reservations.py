#!/usr/bin/env python3
"""Review OP/MAINE original 8 x far-pointer PI reserves without DATA credit.

ReC98's candidate-native ASM explicitly says `dd 8 dup(?)`, not an initial
value. The 32 bytes are a source-backed unwritten _DATA reservation, never
an original initialized-data producer or C++ authored byte claim.
"""
from __future__ import annotations
import argparse,json,re
from pathlib import Path
from lib.omf import parse_omf
from lib.unit_extents import _index
from lib.pc98 import parse_mz
from lib.unit_context import UnitContext,load_unit_target
from lib.unit_oracle import relative_fixups
from review_master import need,sha

ROOT=Path(__file__).resolve().parents[1]
PROOF=ROOT/'config/reviewed_pi_buffer_reservations.json'
PARENT=ROOT/'config/master_vendor_additions.json'
ORIGINAL_SOURCE=ROOT/'_reference/ReC98/th05/formats/pi_buffers[bss].asm'
# Exact original coordinates; real calibration _DATA starts and local offsets.
SPECS={
 'op':('op-calibration-a','op2.obj',0xfa64,0xfa64,0x09e2,0xa2,'0EFE:0A84'),
 'maine':('maine-calibration-a','maine.obj',0x1080e,0x107fe,0x06c0,0x3e,'1010:06FE'),
}


def source_shape(raw:bytes)->None:
    text=raw.decode('utf8')
    need(len(re.findall(r'(?im)^\s*public\s+_pi_buffers\s*$',text))==1 and
         len(re.findall(r'(?im)^\s*_pi_buffers\s+dd\s+8\s+dup\s*\(\s*\?\s*\)\s*$',text))==1,
         'original PI storage is no longer exactly eight unwritten far pointers')


def prove_omf(raw:bytes,local:int)->dict:
    records=parse_omf(raw)
    pubs=[r for r in records if r.name=='PUBDEF' and b'_pi_buffers' in r.data]
    need(len(pubs)==1 and pubs[0].data[:2]==b'\x01\x02' and
         pubs[0].data.endswith(local.to_bytes(2,'little')+b'\x00'),
         'PI buffer source does not declare a complete _DATA pointer public')
    initialized=[]
    for r in records:
        if r.name not in ('LEDATA','LIDATA'):continue
        seg,p=_index(r.data,0)
        off=int.from_bytes(r.data[p:p+2],'little')
        if seg!=2:continue
        if r.name=='LIDATA':
            # There should be none for this source: never credit a source
            # byte just because the linker later materializes zero memory.
            raise ValueError('unreviewed iterated _DATA in PI buffer source object')
        extent=len(r.data)-p-2
        need(off+extent<=local or off>=local+32,
             'an actual initialized TASM LEDATA overlaps the 32-byte reserve')
        initialized.append((off,off+extent))
    need(any(hi==local for lo,hi in initialized) and
         any(lo==local+32 for lo,hi in initialized),
         'PI reserve is not precisely between independently source-written DATA')
    return dict(public_record_offset=pubs[0].offset,
                earlier_final_omf_byte=local,later_first_omf_byte=local+32,
                no_omf_initialized_bytes=True)


def review():
    source=ORIGINAL_SOURCE.read_bytes();source_shape(source)
    other=json.loads(PARENT.read_text());scopes=[]
    for name,(build,objname,orig,calstart,data_base,local,public) in SPECS.items():
        base=ROOT/'.analysis/builds'/build/'source'
        asm=(base/'th05/formats/pi_buffers[bss].asm').read_bytes()
        source_shape(asm)
        need(asm==source,'retained source differs from original candidate PI reserve')
        obj=(base/'obj/th05'/objname).read_bytes()
        omf=prove_omf(obj,local)
        pins=other['table_contexts'][name]['inputs']
        mapbytes=(base/f'obj/th05/{name}.map').read_bytes()
        need(len(re.findall(r'(?im)^\s*'+public+r'\s+(?:idle\s+)?_pi_buffers\s*$',
                            mapbytes.decode('cp437')))==2,
             'native PI buffer pointer public not anchored at proper DS offset')
        maptext=mapbytes.decode('cp437')
        mapbase=f'{public[:5]}{data_base:04X}'
        need(len(re.findall(r'(?im)^\s*'+mapbase+r'\s+00[0-9A-F]{2}\s+C=DATA.*M=',maptext))>=1,
             'PI reserve has no actual containing _DATA linker contribution')
        c=UnitContext(ROOT,name);art,target,_=load_unit_target(c,c.config())
        cal=parse_mz((base/f'bin/th05/{name}.exe').read_bytes())
        need(cal.valid and target.program_image[orig:orig+32]==b'\0'*32 and
             cal.program_image[calstart:calstart+32]==b'\0'*32,
             'original/calibrated PI reserve no longer has 32 zero materialized bytes')
        need(relative_fixups(target,orig,32)==relative_fixups(cal,calstart,32)==[],
             'uninitialized PI pointer reserve must have no original MZ fixup')
        scopes.append(dict(artifact=art['id'],start=orig,end=orig+32,
                           source_sha256=sha(asm),omf_sha256=sha(obj),
                           map_sha256=sha(mapbytes),
                           calibration_exe_sha256=sha((base/f'bin/th05/{name}.exe').read_bytes()),
                           target_sha256=art['sha256'],
                           target_payload_sha256=sha(target.program_image),
                           data_segment_calibration_offset=data_base,
                           data_local_offset=local,
                           zero_initialized_source_bytes=0,
                           reserved_original_bytes=32,
                           omf_reservation=omf,ordered_fixups=[]))
    return dict(version=1,kind='original-candidate-game-PI-eight-far-pointer-reservation',
                classification='reviewed-uninitialized-game-storage',
                total_reserve_bytes=64,authored_credit=0,
                original_candidate_source_sha256=sha(source),
                context_proof_sha256=sha(PARENT.read_bytes()),scopes=scopes)


def validate(proof):
    source=ORIGINAL_SOURCE.read_bytes();source_shape(source)
    other=json.loads(PARENT.read_text())
    need(proof.get('version')==1 and proof.get('kind')=='original-candidate-game-PI-eight-far-pointer-reservation' and
         proof.get('classification')=='reviewed-uninitialized-game-storage' and
         proof.get('total_reserve_bytes')==64 and proof.get('authored_credit')==0 and
         proof.get('original_candidate_source_sha256')==sha(source) and
         proof.get('context_proof_sha256')==sha(PARENT.read_bytes()) and
         len(proof.get('scopes',[]))==2,
         'stale/incomplete original PI eight-far-pointer storage review')
    for row,(name,(build,objname,st,cal,base,local,public)) in zip(proof['scopes'],SPECS.items()):
        folder=ROOT/'.analysis/builds'/build/'source'
        ctx=other['table_contexts'][name]
        blob=(folder/'obj/th05'/objname).read_bytes()
        need(row.get('artifact')=='th05-'+name and row.get('start')==st and row.get('end')==st+32 and
             row.get('source_sha256')==sha((folder/'th05/formats/pi_buffers[bss].asm').read_bytes()) and
             row.get('omf_sha256')==sha(blob) and
             row.get('map_sha256')==ctx['inputs']['calibration_map']['sha256'] and
             row.get('calibration_exe_sha256')==ctx['inputs']['calibration_exe']['sha256'] and
             row.get('target_sha256')==ctx['target_sha256'] and
             row.get('target_payload_sha256')==ctx['target_payload_sha256'] and
             row.get('data_segment_calibration_offset')==base and
             row.get('data_local_offset')==local and
             row.get('zero_initialized_source_bytes')==0 and
             row.get('reserved_original_bytes')==32 and
             row.get('ordered_fixups')==[] and
             row.get('omf_reservation')==prove_omf(blob,local),
             'invalid game PI uninitialized source/OMF scope or original identity')


def reviewed_claims(root,views,*,verify_targets=False):
    if not PROOF.exists():return {},None
    raw=PROOF.read_bytes();proof=json.loads(raw);validate(proof)
    if verify_targets:need(proof==review(),'actual PI uninitialized source review changed')
    claims={}
    for row in proof['scopes']:
        name=row['artifact'].removeprefix('th05-')
        need(views[name]['sha256']==row['target_payload_sha256'],
             'PI uninitialized reserve belongs to a different target')
        claims[name]=[dict(start=row['start'],end=row['end'],
                           kind='reviewed-uninitialized-game-storage',
                           content_kind='source-question-mark-reserve',
                           instruction_bytes=0,authored_credit=0,
                           source='th05/formats/pi_buffers[bss].asm',
                           member='_pi_buffers')]
    return claims,sha(raw)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    g=p.add_mutually_exclusive_group(required=True)
    for name in ('write','check','structural-check'):g.add_argument('--'+name,action='store_true')
    a=p.parse_args()
    if a.write:
        proof=review();PROOF.write_text(json.dumps(proof,indent=2)+'\n')
    else:proof=json.loads(PROOF.read_text())
    validate(proof)
    if a.check:need(proof==review(),'original game PI source/OMF proof changed')
    print('PASS: two complete 32-byte PI far-pointer unwritten source reserves; zero authored credit')

if __name__=='__main__':main()
