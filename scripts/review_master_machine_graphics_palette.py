#!/usr/bin/env python3
"""Reconstruct original Master 0.23 GETMAC/GRP/JS/MACHINE/PAL DATA.

Six genuine source contributions span 109 of 110 contiguous bytes in each
original MZ; the separate source-side graph even-byte stays unknown.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

from lib.pc98 import parse_mz
from lib.unit_context import UnitContext,load_unit_target
from lib.unit_oracle import relative_fixups
from review_master import need,pinned,sha,stored_lzh
from review_master_bgm_literal_data import actual_data

ROOT=Path(__file__).resolve().parents[1]
PROOF=ROOT/'config/reviewed_master_machine_graphics_palette.json'
PARENT=ROOT/'config/master_vendor_ownership.json'
OTHER=ROOT/'config/master_vendor_additions.json'
SPECS={
 'main':('main-calibration-b','main',0x20D74,0x20D96,0x326,'209E:03B6'),
 'op':('op-calibration-a','op',0xF4F8,0xF4F8,0x46,'0EFE:0518'),
 'maine':('maine-calibration-a','mainem',0x10312,0x10302,0x146,'1010:0202'),
}
# Relative to the beginning of the full source cluster; a one-byte alignment
# after the 11 original GRP literals (offset 43) is not author initialized.
MEMBERS=(('GETMAC98',0,10,'GETMAC98.ASM','get_machine_98[data].asm'),
         ('GETMACAT',10,22,'GETMACAT.ASM','get_machine_at[data].asm'),
         ('GRP',32,11,'GRP.ASM','grp[data].asm'),
         ('JS',44,8,'JS.ASM','js[data].asm'),
         ('MACHINE',52,2,'MACHINE.ASM','machine[data].asm'),
         ('PAL',54,56,'PAL.ASM','pal[data].asm'))
GRAPH_WORDS=(('graph_VramSeg',0xa800),('graph_VramWords',16000),
             ('graph_VramLines',400),('graph_VramWidth',80),('graph_VramZoom',0))
JS_WORDS=('js_bexist','js_saj_port','js_2player','js_shift')
PAL_LAST=('PaletteNote','ResPalSeg','SdiExists')
PUBLICS=((32,'graph_VramSeg'),(34,'graph_VramWords'),(42,'graph_MeshByte'),
         (44,'js_bexist'),(52,'Machine_State'),(54,'PaletteTone'),
         (56,'PalettesInit'),(104,'PaletteNote'),(106,'ResPalSeg'),(108,'SdiExists'))


def one_source(raw:bytes,encoding:str,member:str)->bytes:
    text=raw.decode(encoding)
    if member=='GETMAC98':
        after=text.split('EPSON_NOTES',1)
        need(len(after)==2,'missing original Epson machine-note table')
        vals=[]
        for line in after[1].splitlines():
            first=line.split(';',1)[0]
            m=re.search(r'(?i)\bdb\s+([0-9a-f]+)h\b',first)
            if m:vals.append(int(m[1],16))
            if len(vals)==9:break
        need(vals==[0x0d,0x16,0x20,0x22,0x27,0x2a,0x2e,0x36,0x3f],
             'Epson machine-note source byte sequence changed')
        need(re.search(r'(?im)^\s*db\s+00h\s*(?:;.*)?$',after[1]),
             'Epson note table source lacks explicit zero sentinel')
        return bytes(vals+[0])
    if member=='GETMACAT':
        for name in ('IBMADSP','IBMAFNT'):
            need(len(re.findall(r'(?im)^\s*'+name+r'\s+db\s+\'\$'+name+r"',\s*0\s*(?:;.*)?$",text))==1,
                 'original AT machine device ID initializer changed')
        need(len(re.findall(r'(?im)^\s*EXENTRY\s+dd\s+0\s*(?:;.*)?$',text))==1,
             'original DOS/V extension entry is not a zero far address')
        return b'$IBMADSP\0$IBMAFNT\0'+b'\0'*4
    if member=='GRP':
        values=[]
        for key,expect in GRAPH_WORDS:
            m=re.findall(r'(?im)^\s*_?'+key+r'\s+dw\s+([0-9a-f]+h|[0-9]+)\s*(?:;.*)?$',text)
            need(len(m)==1,'Master graphics parameter missing/duplicated: '+key)
            val=int(m[0][:-1],16) if m[0].lower().endswith('h') else int(m[0])
            need(val==expect,'Master graphics source value changed: '+key)
            values.append(val)
        need(len(re.findall(r'(?im)^\s*_?graph_MeshByte\s+db\s+55h\s*(?:;.*)?$',text))==1,
             'original mesh byte changed')
        return b''.join(v.to_bytes(2,'little') for v in values)+b'\x55'
    if member=='JS':
        for key in JS_WORDS:
            need(len(re.findall(r'(?im)^\s*_?'+key+r'\s+dw\s+0\s*(?:;.*)?$',text))==1,
                 'original joystick initialized state differs: '+key)
        return b'\0'*8
    if member=='MACHINE':
        need(len(re.findall(r'(?im)^\s*_?Machine_State\s+dw\s+0\s*(?:;.*)?$',text))==1,
             'original machine state initial word differs')
        return b'\0\0'
    if member=='PAL':
        need(len(re.findall(r'(?im)^\s*_?PaletteTone\s+dw\s+100\s*(?:;.*)?$',text))==1,
             'original palette tone is not 100')
        block=text.split('_PalettesInit',1)
        need(len(block)==2,'no original 16-color palette initializer')
        block=block[1].split('public _PaletteNote',1)
        need(len(block)==2,'palette has no independent following note word')
        triples=[]
        for line in block[0].splitlines():
            body=line.split(';',1)[0].strip()
            m=re.fullmatch(r'(?:_?PalettesInit\s+)?db\s+([0-9a-f]{3}h)\s*,\s*([0-9a-f]{3}h)\s*,\s*([0-9a-f]{3}h)',body,re.I)
            if m:triples.extend(int(v[:-1],16) for v in m.groups())
        expected=[0,0,0,0,0,255,255,0,0,255,0,255,0,255,0,0,255,255,
                  255,255,0,255,255,255,119,119,119,0,0,170,170,0,0,
                  170,0,170,0,170,0,0,170,170,170,170,0,170,170,170]
        need(triples==expected and len(triples)==48,
             'original 16-color RGB palette differs')
        for key in PAL_LAST:
            need(len(re.findall(r'(?im)^\s*_?'+key+r'\s+dw\s+0\s*(?:;.*)?$',text))==1,
                 'original palette trailing word differs: '+key)
        return (100).to_bytes(2,'little')+bytes(triples)+b'\0'*6
    raise ValueError('unreviewed member name: '+member)


def original_archive():
    parent=json.loads(PARENT.read_text())
    archive=stored_lzh(pinned(ROOT,parent['inputs']['inner_archive']))
    return parent,archive


def review():
    parent,archive=original_archive()
    other=json.loads(OTHER.read_text())
    sources={member:one_source(archive[name],'cp932',member) for member,_,_,name,_ in MEMBERS}
    need(sum(len(x) for x in sources.values())==109,'source should only own 109 of 110 bytes')
    scopes=[]
    for name,(build,objname,original_start,cal_start,local,public) in SPECS.items():
        base=ROOT/'.analysis/builds'/build/'source'
        pins=parent['inputs'] if name=='main' else other['table_contexts'][name]['inputs']
        obj=pinned(ROOT,pins['calibration_object'])
        mp=pinned(ROOT,pins['calibration_map'])
        exe=pinned(ROOT,pins['calibration_exe'])
        c=UnitContext(ROOT,name);art,target,_=load_unit_target(c,c.config())
        cal=parse_mz(exe)
        need(cal.valid,'bad original-compiler calibration MZ')
        frame,pubstart=public.split(':')
        for offset,symbol in PUBLICS:
            label=f'{frame}:{int(pubstart,16)+offset:04X}'
            need(len(re.findall(r'(?im)^\s*'+label+r'\s+(?:idle\s+)?_?'+symbol+r'\s*$',mp.decode('cp437')))>=2,
                 'real original-compiler MAP public moved: '+name+' '+symbol)
        for member,offset,length,author_name,filename in MEMBERS:
            source=(base/'libs/master.lib'/filename).read_bytes()
            expected=sources[member]
            need(len(expected)==length and one_source(source,'utf8',member)==expected,
                 'retained TASM source differs from archived author: '+member)
            actual=actual_data(obj,local+offset,length)
            need(len(actual)==1 and actual[0]['scope_offset']==0 and
                 actual[0]['scope_size']==length and actual[0]['scope_content_sha256']==sha(expected),
                 'incomplete source-written original OMF _DATA: '+member)
            native_at=original_start+offset;cal_at=cal_start+offset
            need(target.program_image[native_at:native_at+length]==expected and
                 cal.program_image[cal_at:cal_at+length]==expected,
                 'original/calibration/source bytes differ: '+member)
            need(relative_fixups(target,native_at,length)==relative_fixups(cal,cal_at,length)==[],
                 'unexpected MZ segment relocation inside Master initialized DATA')
            scopes.append(dict(artifact=art['id'],name=member,
                start=native_at,end=native_at+length,author_source_sha256=sha(archive[author_name]),
                native_source_sha256=sha(source),content_sha256=sha(expected),
                target_sha256=art['sha256'],target_payload_sha256=sha(target.program_image),
                actual_omf_sha256=sha(obj),actual_map_sha256=sha(mp),
                calibration_exe_sha256=sha(exe),original_ordered_fixups=[],
                actual_complete_omf_LEDATA=actual[0]))
        need(target.program_image[original_start+43]==0 and cal.program_image[cal_start+43]==0,
             'excluded graphics alignment is not the observed byte')
    return dict(version=1,kind='original-Master-machine-graphics-palette-initialized-DATA',
                classification='third-party-library-initialized-data',
                authored_credit=0,total_bytes=218,already_accepted_main_bytes=109,
                author_archive_sha256=parent['inputs']['inner_archive']['sha256'],
                excluded_one_alignment_per_MZ=True,scopes=scopes)


def validate(proof):
    parent,archive=original_archive();other=json.loads(OTHER.read_text())
    need(proof.get('version')==1 and
         proof.get('kind')=='original-Master-machine-graphics-palette-initialized-DATA' and
         proof.get('classification')=='third-party-library-initialized-data' and
         proof.get('total_bytes')==218 and proof.get('already_accepted_main_bytes')==109 and
         proof.get('authored_credit')==0 and
         proof.get('author_archive_sha256')==parent['inputs']['inner_archive']['sha256'] and
         proof.get('excluded_one_alignment_per_MZ') is True and
         len(proof.get('scopes',[]))==18,'stale/incomplete Master machine/graphics/palette proof')
    for i,(name,(build,objname,orig,cal,local,pub)) in enumerate(SPECS.items()):
        pins=parent['inputs'] if name=='main' else other['table_contexts'][name]['inputs']
        info=other['table_contexts'][name] if name!='main' else None
        artifact_sha=parent['inputs']['target']['sha256'] if name=='main' else info['target_sha256']
        payload_sha=parent['target_payload_sha256'] if name=='main' else info['target_payload_sha256']
        for j,(member,offset,sz,archive_name,filename) in enumerate(MEMBERS):
            row=proof['scopes'][i*6+j]
            exp=one_source(archive[archive_name],'cp932',member)
            source=ROOT/'.analysis/builds'/build/'source/libs/master.lib'/filename
            omf=row.get('actual_complete_omf_LEDATA',{})
            need(row.get('artifact')=='th05-'+name and row.get('name')==member and
                 row.get('start')==orig+offset and row.get('end')==orig+offset+sz and
                 row.get('author_source_sha256')==sha(archive[archive_name]) and
                 row.get('native_source_sha256')==sha(source.read_bytes()) and
                 row.get('content_sha256')==sha(exp) and
                 row.get('target_sha256')==artifact_sha and row.get('target_payload_sha256')==payload_sha and
                 row.get('actual_omf_sha256')==pins['calibration_object']['sha256'] and
                 row.get('actual_map_sha256')==pins['calibration_map']['sha256'] and
                 row.get('calibration_exe_sha256')==pins['calibration_exe']['sha256'] and
                 row.get('original_ordered_fixups')==[] and
                 omf.get('scope_offset')==0 and omf.get('scope_size')==sz and
                 omf.get('scope_content_sha256')==sha(exp),
                 'Master source, original target or native initialized LEDATA differs')


def reviewed_claims(root,views,*,verify_targets=False):
    if not PROOF.exists():return {},None
    raw=PROOF.read_bytes();proof=json.loads(raw);validate(proof)
    if verify_targets:need(review()==proof,'source-backed Master machine/graphics/palette replay changed')
    claims={}
    for row in proof['scopes']:
        name=row['artifact'].removeprefix('th05-')
        need(views[name]['sha256']==row['target_payload_sha256'],
             'Master machine/graphics/palette data belongs to different target')
        if name=='main':
            # The earlier independent native MAIN source review already owns
            # these 109 bytes in seven original parts. Re-prove identity,
            # never overlay or recredit the existing physical intervals.
            previous=json.loads((root/'config/main_master_literal_tables_ownership.json').read_text())
            prior=previous['scope_rows']
            first=next((r for r in prior if r['member'] == {
                'GETMAC98':'EPSON_NOTES','GETMACAT':'IBM_VIDEO_DEVICES',
                'GRP':'GRAPH_VRAM_DEFAULTS','JS':'JOYSTICK_DEFAULTS',
                'MACHINE':'MACHINE_STATE_DEFAULT','PAL':'PALETTE_DEFAULTS',
            }[row['name']]),None)
            need(first is not None and first['start']==row['start'] and
                 first['DATA_sha256']==(sha(one_source(
                   original_archive()[1]['PAL.ASM'],'cp932','PAL')[:50])
                   if row['name']=='PAL' else row['content_sha256']),
                 'previous MAIN Master literal source proof changed')
            if row['name']=='PAL':
                tail=next((r for r in prior if r['member']=='PALETTE_RUNTIME_DEFAULTS'),None)
                need(tail is not None and tail['start']==row['start']+50 and
                     tail['end']==row['end'] and
                     tail['DATA_sha256']==sha(one_source(original_archive()[1]['PAL.ASM'],'cp932','PAL')[50:]),
                     'previous MAIN palette runtime default owner differs')
            else:
                need(first['end']==row['end'],'prior MAIN Master extent differs')
            continue
        claims.setdefault(name,[]).append(dict(start=row['start'],end=row['end'],
              kind='verified-vendor-initialized-data',content_kind='library-initialized-data',
              instruction_bytes=0,library='Master 0.23',member=row['name']))
    return claims,sha(raw)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    g=parser.add_mutually_exclusive_group(required=True)
    for mode in ('write','check','structural-check'):g.add_argument('--'+mode,action='store_true')
    a=parser.parse_args()
    if a.write:
        proof=review();PROOF.write_text(json.dumps(proof,indent=2)+'\n')
    else:proof=json.loads(PROOF.read_text())
    validate(proof)
    if a.check:need(review()==proof,'original-Master source exact review changed')
    print('PASS: three complete source-compared MZs, 218 newly adopted OP/MAINE bytes, MAIN already accepted')

if __name__=='__main__':main()
