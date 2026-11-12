#!/usr/bin/env python3
"""Prove the source-backed JS, palette and MEM `_BSS` variables in three MZs.

Distinct from existing initialized Master DATA and the much larger SUPERPA
arrays. Every byte here has '?' source provenance, zero authored credit.
"""
from __future__ import annotations
import argparse,json,re
from pathlib import Path
from lib.omf import parse_omf
from lib.unit_extents import _index
from lib.unit_context import UnitContext,load_unit_target
from lib.unit_oracle import relative_fixups
from lib.pc98 import parse_mz
from review_master import pinned,stored_lzh,sha,need

ROOT=Path(__file__).resolve().parents[1]
PROOF=ROOT/'config/reviewed_master_compact_bss.json'
PARENT=ROOT/'config/master_vendor_ownership.json'
OTHER=ROOT/'config/master_vendor_additions.json'
SPECS={
 'main':('main-calibration-b','main',0x23016,'209E:2658',0x2C,0xA080),
 'op':('op-calibration-a','op',0x11DFA,'0EFE:2E1A',0x24,0x1128),
 'maine':('maine-calibration-a','mainem',0x11EA6,'1010:1D96',0x24,0x1114),
}
PARTS=(('JS_STAT',0,4,'JS.ASM','js[bss].asm','js_stat'),
       ('PALETTES',4,48,'PAL.ASM','pal[bss].asm','_Palettes'),
       ('VSYNC_CORE',52,8,'VS.ASM','vs[bss].asm','_vsync_Count1'),
       ('VSYNC_DELAY',60,2,'VSYNC.ASM','vsync[bss].asm','vsync_delay_count'),
       ('MEM_WORK',62,8,'MEM.ASM','mem[bss].asm','mem_OutSeg'))


def source_shape(raw:bytes,encoding:str,member:str,archived:bool=False):
    s=raw.decode(encoding)
    if archived:need(re.search(r'(?im)^\s*\.DATA\?\s*$',s),
                     'original Master source no longer reserves BSS')
    if member=='JS_STAT':
        need(len(re.findall(r'(?im)^\s*js_stat\s+dw\s*\?\s*,\s*\?\s*$',s))==1,
             'Master joystick two-player BSS declaration changed')
    elif member=='PALETTES':
        need(len(re.findall(r'(?im)^\s*_Palettes\s+db\s+48\s+dup\s*\(\s*\?\s*\)\s*$',s))==1,
             'Master 16-color writable RGB palette source changed')
    elif member=='VSYNC_CORE':
        for key,kind in (('_vsync_Count1','dw'),('_vsync_Count2','dw'),('vsync_OldVect','dd')):
            need(len(re.findall(r'(?im)^\s*'+key+r'\s+'+kind+r'\s+\?\s*(?:;.*)?$',s))==1,
                 'original VSYNC counter/vector BSS differs: '+key)
    elif member=='VSYNC_DELAY':
        need(len(re.findall(r'(?im)^\s*vsync_delay_count\s+dw\s+\?\s*(?:;.*)?$',s))==1,
             'original VSYNC divider counter BSS differs')
    elif member=='MEM_WORK':
        for key in ('mem_OutSeg','mem_TopHeap','mem_FirstHole','mem_EndMark'):
            need(len(re.findall(r'(?im)^\s*'+key+r'\s+dw\s+\?\s*$',s))==1,
                 'original four-word memory heap BSS differs: '+key)
    else:raise ValueError('unreviewed compact BSS type')


def bss_publics(obj:bytes,expected:list[tuple[str,int]],bss_size:int)->dict:
    names=[''];segments=[None];publics={};writes=[]
    for rec in parse_omf(obj):
        raw=rec.data
        if rec.name=='LNAMES':
            i=0
            while i<len(raw):
                size=raw[i];i+=1
                need(i+size<=len(raw),'truncated native TASM string')
                names.append(raw[i:i+size].decode('cp437'));i+=size
        elif rec.name=='SEGDEF':
            ni,i=_index(raw,3);ci,i=_index(raw,i);oi,i=_index(raw,i)
            segments.append((names[ni],names[ci],int.from_bytes(raw[1:3],'little')))
        elif rec.name=='PUBDEF':
            if len(raw)<4:continue
            group,seg=raw[0],raw[1];p=2
            if seg==0:p+=2
            if p>=len(raw):continue
            length=raw[p];p+=1
            if p+length+2>len(raw):continue
            public=raw[p:p+length].decode('cp437');p+=length
            if public in (k for k,o in expected):
                publics[public]=(group,seg,int.from_bytes(raw[p:p+2],'little'))
        elif rec.name in ('LEDATA','LIDATA'):
            seg,pos=_index(raw,0)
            writes.append((rec.name,seg,int.from_bytes(raw[pos:pos+2],'little')))
    bss=[(i,s) for i,s in enumerate(segments) if s and s[:2]==('_BSS','BSS')]
    need(len(bss)==1 and bss[0][1][2]==bss_size,
         'native _BSS OMF segment size/class changed')
    idx=bss[0][0]
    need(not [w for w in writes if w[1]==idx],
         'unexpected initialized TASM LEDATA/LIDATA in actual _BSS')
    for symbol,off in expected:
        need(publics.get(symbol)==(1,idx,off),
             'native _BSS PUBDEF address differs: '+symbol)
    return dict(bss_segment_index=idx,bss_segment_size=bss_size,
                source_public_offsets={key:publics[key][2] for key,_ in expected},
                source_initialized_records=0)


def review():
    parent=json.loads(PARENT.read_text());other=json.loads(OTHER.read_text())
    author=stored_lzh(pinned(ROOT,parent['inputs']['inner_archive']))
    rows=[]
    for name,(build,objname,first_original,first_map,first_local,bss_size) in SPECS.items():
        base=ROOT/'.analysis/builds'/build/'source'
        pins=parent['inputs'] if name=='main' else other['table_contexts'][name]['inputs']
        obj=pinned(ROOT,pins['calibration_object']);mp=pinned(ROOT,pins['calibration_map']);exe=pinned(ROOT,pins['calibration_exe'])
        mapframe,offset=first_map.split(':');pub=[]
        for member,diff,sz,archivefile,nativefile,firstsym in PARTS:
            if member=='MEM_WORK':
                localsymbols=[(k,first_local+diff+2*i) for i,k in enumerate(('mem_OutSeg','mem_TopHeap','mem_FirstHole','mem_EndMark'))]
            elif member=='VSYNC_CORE':
                localsymbols=[('_vsync_Count1',first_local+diff),
                              ('_vsync_Count2',first_local+diff+2),
                              ('_vsync_OldVect',first_local+diff+4)]
            else:localsymbols=[(firstsym,first_local+diff)]
            pub.extend(localsymbols)
            source=(base/'libs/master.lib'/nativefile).read_bytes()
            source_shape(author[archivefile],'cp932',member,archived=True)
            source_shape(source,'utf8',member)
            for symbol,_ in localsymbols:
                dslabel=f'{mapframe}:{int(offset,16)+diff+(_-first_local-diff):04X}'
                need(len(re.findall(r'(?im)^\s*'+dslabel+r'\s+(?:idle\s+)?'+symbol+r'\s*$',mp.decode('cp437')))>=2,
                     'native MAP lacks exact BSS word '+symbol)
            ctx=UnitContext(ROOT,name);artifact,target,_=load_unit_target(ctx,ctx.config())
            at=first_original+diff
            need(target.program_image[at:at+sz]==b'\0'*sz,
                 'original MZ BSS scope not materialized as complete zero array')
            need(relative_fixups(target,at,sz)==[],
                 'uninitialized BSS acquired original MZ relocation')
            cal=parse_mz(exe)
            calibration_at=(int(mapframe,16)<<4)+int(offset,16)+diff
            need(cal.valid and len(cal.program_image)<=calibration_at,
                 'retained MZ unexpectedly has source-written BSS payload')
            rows.append(dict(artifact=artifact['id'],member=member,start=at,end=at+sz,
                 original_sha256=artifact['sha256'],original_payload_sha256=sha(target.program_image),
                 source_sha256=sha(source),author_sha256=sha(author[archivefile]),
                 omf_sha256=sha(obj),map_sha256=sha(mp),exe_sha256=sha(exe),
                 local_segment_start=first_local+diff,ordered_fixups=[],
                 initialized_source_bytes=0))
        parsed=bss_publics(obj,pub,bss_size)
        for row in rows[-len(PARTS):]:row['complete_actual_BSS']=parsed
    return dict(version=1,kind='original-Master-JS-PAL-VSYNC-MEM-unwritten-BSS',
         classification='reviewed-uninitialized-vendor-storage',
         source_archive_sha256=parent['inputs']['inner_archive']['sha256'],
         total_bytes=210,authored_credit=0,source_unclaimed_interstitial_bytes=0,
         scopes=rows)


def validate(proof):
    parent=json.loads(PARENT.read_text());other=json.loads(OTHER.read_text())
    author=stored_lzh(pinned(ROOT,parent['inputs']['inner_archive']))
    need(proof.get('version')==1 and
         proof.get('kind')=='original-Master-JS-PAL-VSYNC-MEM-unwritten-BSS' and
         proof.get('classification')=='reviewed-uninitialized-vendor-storage' and
         proof.get('source_archive_sha256')==parent['inputs']['inner_archive']['sha256'] and
         proof.get('total_bytes')==210 and proof.get('authored_credit')==0 and
         proof.get('source_unclaimed_interstitial_bytes')==0 and
         len(proof.get('scopes',[]))==len(SPECS)*len(PARTS),'stale/partial source-backed Master compact BSS scope')
    for i,(name,(build,objname,first_original,first_map,first_local,bss_size)) in enumerate(SPECS.items()):
        pins=parent['inputs'] if name=='main' else other['table_contexts'][name]['inputs']
        info=other['table_contexts'][name] if name!='main' else None
        targetsha=parent['inputs']['target']['sha256'] if name=='main' else info['target_sha256']
        payloadsha=parent['target_payload_sha256'] if name=='main' else info['target_payload_sha256']
        root=ROOT/'.analysis/builds'/build/'source/libs/master.lib'
        pubs=[]
        for member,diff,sz,sourcefile,nativefile,firstsym in PARTS:
            if member=='MEM_WORK':pubs.extend((k,first_local+diff+2*k_i) for k_i,k in enumerate(('mem_OutSeg','mem_TopHeap','mem_FirstHole','mem_EndMark')))
            elif member=='VSYNC_CORE':
                pubs.extend((k,first_local+diff+offset) for k,offset in
                            (('_vsync_Count1',0),('_vsync_Count2',2),('_vsync_OldVect',4)))
            else:pubs.append((firstsym,first_local+diff))
        actual_bss=bss_publics(pinned(ROOT,pins['calibration_object']),pubs,bss_size)
        for j,(member,diff,sz,authorfile,nativefile,_) in enumerate(PARTS):
            row=proof['scopes'][i*len(PARTS)+j]
            source_shape(author[authorfile],'cp932',member,archived=True)
            source=(root/nativefile).read_bytes()
            source_shape(source,'utf8',member)
            need(row.get('artifact')=='th05-'+name and row.get('member')==member and
                 row.get('start')==first_original+diff and row.get('end')==first_original+diff+sz and
                 row.get('original_sha256')==targetsha and row.get('original_payload_sha256')==payloadsha and
                 row.get('source_sha256')==sha(source) and row.get('author_sha256')==sha(author[authorfile]) and
                 row.get('omf_sha256')==pins['calibration_object']['sha256'] and
                 row.get('map_sha256')==pins['calibration_map']['sha256'] and
                 row.get('exe_sha256')==pins['calibration_exe']['sha256'] and
                 row.get('local_segment_start')==first_local+diff and
                 row.get('complete_actual_BSS')==actual_bss and
                 row.get('ordered_fixups')==[] and row.get('initialized_source_bytes')==0,
                 'original compact Master _BSS source, MZ or actual TASM structure changed')


def reviewed_claims(root,views,*,verify_targets=False):
    if not PROOF.exists():return {},None
    raw=PROOF.read_bytes();proof=json.loads(raw);validate(proof)
    if verify_targets:need(proof==review(),'native source-backed JS/PAL/MEM _BSS proof changed')
    claims={}
    for row in proof['scopes']:
        name=row['artifact'].removeprefix('th05-')
        need(views[name]['sha256']==row['original_payload_sha256'],
             'compact Master BSS belongs to another decoded target')
        source={'JS_STAT':'JS.ASM/JS_STAT',
                'PALETTES':'PAL.ASM/PALETTES',
                'VSYNC_CORE':'VS.ASM/VSYNC_CORE',
                'VSYNC_DELAY':'VSYNC.ASM/VSYNC_DELAY',
                'MEM_WORK':'MEM.ASM/MEM_WORK'}[row['member']]
        claims.setdefault(name,[]).append(dict(start=row['start'],end=row['end'],
              kind='reviewed-uninitialized-vendor-storage',
              content_kind='source-question-mark-struct',library='Master 0.23',
              member=row['member'],source=source,authored_credit=0,instruction_bytes=0))
    return claims,sha(raw)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    g=p.add_mutually_exclusive_group(required=True)
    for opt in ('write','check','structural-check'):g.add_argument('--'+opt,action='store_true')
    a=p.parse_args()
    if a.write:
        proof=review();PROOF.write_text(json.dumps(proof,indent=2)+'\n')
    else:proof=json.loads(PROOF.read_text())
    validate(proof)
    if a.check:need(proof==review(),'compact original Master BSS evidence changed')
    print('PASS: fifteen original Master JS/PAL/VSYNC/MEM BSS spans, 210 bytes, zero authored credit')

if __name__=='__main__':main()
