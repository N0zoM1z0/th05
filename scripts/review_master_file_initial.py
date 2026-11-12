#!/usr/bin/env python3
"""Recover contiguous FIL handle words and native DOS_ROPEN sharing mode.

FIL.ASM has independent archived-author provenance; DOS_ROPEN's initializer is
proved by retained ReC98 source, original TASM OMF/MAP and original MZ bytes.
"""
from __future__ import annotations
import argparse,json,re
from pathlib import Path
from lib.unit_context import UnitContext,load_unit_target
from lib.unit_oracle import relative_fixups
from lib.pc98 import parse_mz
from review_master import pinned,stored_lzh,sha,need
from review_master_bgm_literal_data import actual_data

ROOT=Path(__file__).resolve().parents[1]
PROOF=ROOT/'config/reviewed_master_file_initial.json'
PARENT=ROOT/'config/master_vendor_ownership.json'
OTHER=ROOT/'config/master_vendor_additions.json'
SPECS={
 'main':('main-calibration-b',0x20d6e,0x20d90,0x320,'209E:03B0'),
 'op':('op-calibration-a',0xf4f2,0xf4f2,0x40,'0EFE:0512'),
 'maine':('maine-calibration-a',0x1030c,0x102fc,0x140,'1010:01FC'),
}


def author_file_bytes(raw:bytes)->bytes:
    txt=raw.decode('cp932')
    need(re.search(r'(?im)^\s*file_BufferSize\s+dw\s+0\s*$',txt) and
         re.search(r'(?im)^\s*file_Handle\s+dw\s+-1\s*$',txt),
         'archived author FIL file-handle initialized values changed')
    return b'\x00\x00\xff\xff'


def native_share_bytes(raw:bytes)->bytes:
    txt=raw.decode('utf8')
    need(re.search(r'(?im)^\s*file_sharingmode\s+dw\s+0\s*$',txt),
         'retained DOS_ROPEN source sharing-mode initializer changed')
    return b'\x00\x00'


def review():
    parent=json.loads(PARENT.read_text());other=json.loads(OTHER.read_text())
    archive=stored_lzh(pinned(ROOT,parent['inputs']['inner_archive']))
    authored=author_file_bytes(archive['FIL.ASM'])
    rows=[]
    for n,(b,orig,cal,local,anchor) in SPECS.items():
        base=ROOT/'.analysis/builds'/b/'source'
        f=(base/'libs/master.lib/fil[data].asm').read_bytes()
        sh=(base/'libs/master.lib/dos_ropen[data].asm').read_bytes()
        need(re.search(rb'(?im)^\s*file_BufferSize\s+dw\s+0\s*$',f) and
             re.search(rb'(?im)^\s*file_Handle\s+dw\s+-1\s*$',f),
             'retained TASM FIL source not equivalent to author FIL')
        pieces=(('FIL',0,authored,f),('DOS_ROPEN_SHARING',4,native_share_bytes(sh),sh))
        pins=parent['inputs'] if n=='main' else other['table_contexts'][n]['inputs']
        obj=pinned(ROOT,pins['calibration_object']);exe=pinned(ROOT,pins['calibration_exe']);mp=pinned(ROOT,pins['calibration_map'])
        ctx=UnitContext(ROOT,n);art,target,_=load_unit_target(ctx,ctx.config());calimg=parse_mz(exe)
        need(calimg.valid,'invalid calibration MZ')
        frame,off=anchor.split(':')
        for member,diff,source,source_data in pieces:
            physical=orig+diff;calphysical=cal+diff
            sym='file_BufferSize' if diff==0 else 'file_sharingmode'
            exported=f'{frame}:{int(off,16)+diff:04X}'
            need(len(re.findall(r'(?im)^\s*'+exported+r'\s+(?:idle\s+)?_?'+sym+r'\s*$',mp.decode('cp437')))==4,
                 'actual file DATA MAP public binding differs: '+n+' '+member)
            ld=actual_data(obj,local+diff,len(source))
            need(len(ld)==1 and ld[0]['scope_size']==len(source) and
                 ld[0]['scope_offset']==0 and ld[0]['scope_content_sha256']==sha(source),
                 'incomplete original file initializer TASM LEDATA')
            need(target.program_image[physical:physical+len(source)]==source and
                 calimg.program_image[calphysical:calphysical+len(source)]==source,
                 'actual/calibrated FILE initialized bytes mismatch')
            need(relative_fixups(target,physical,len(source))==relative_fixups(calimg,calphysical,len(source))==[],
                 'real FILE DATA contains MZ relocation')
            rows.append(dict(artifact=art['id'],member=member,start=physical,
                 end=physical+len(source),source_content_sha256=sha(source),
                 source_sha256=sha(source_data),actual_LEDATA=ld[0],
                 artifact_sha256=art['sha256'],payload_sha256=sha(target.program_image),
                 omf_sha256=sha(obj),map_sha256=sha(mp),exe_sha256=sha(exe),ordered_fixups=[]))
    return dict(version=1,kind='source-verified-Master-FIL-and-DOS_ROPEN-initialized-data',
         author_fil_sha256=sha(archive['FIL.ASM']),
         archive_sha256=parent['inputs']['inner_archive']['sha256'],
         authored_credit=0,total_bytes=18,rows=rows)


def validate(proof):
    parent=json.loads(PARENT.read_text());other=json.loads(OTHER.read_text())
    archive=stored_lzh(pinned(ROOT,parent['inputs']['inner_archive']))
    fil=author_file_bytes(archive['FIL.ASM'])
    need(proof.get('version')==1 and proof.get('kind')=='source-verified-Master-FIL-and-DOS_ROPEN-initialized-data' and
         proof.get('author_fil_sha256')==sha(archive['FIL.ASM']) and
         proof.get('archive_sha256')==parent['inputs']['inner_archive']['sha256'] and
         proof.get('authored_credit')==0 and proof.get('total_bytes')==18 and
         len(proof.get('rows',[]))==6,'partial or stale FILE source provenance')
    for i,(name,(b,orig,cal,local,anchor)) in enumerate(SPECS.items()):
        pins=parent['inputs'] if name=='main' else other['table_contexts'][name]['inputs']
        info=other['table_contexts'][name] if name!='main' else None
        artsha=parent['inputs']['target']['sha256'] if name=='main' else info['target_sha256']
        payloadsha=parent['target_payload_sha256'] if name=='main' else info['target_payload_sha256']
        base=ROOT/'.analysis/builds'/b/'source/libs/master.lib'
        for j,(member,off,source,srcpath) in enumerate((('FIL',0,fil,base/'fil[data].asm'),
                 ('DOS_ROPEN_SHARING',4,b'\0\0',base/'dos_ropen[data].asm'))):
            r=proof['rows'][i*2+j];led=r.get('actual_LEDATA',{})
            need(r.get('artifact')=='th05-'+name and r.get('member')==member and
                 r.get('start')==orig+off and r.get('end')==orig+off+len(source) and
                 r.get('source_content_sha256')==sha(source) and
                 r.get('source_sha256')==sha(srcpath.read_bytes()) and
                 r.get('artifact_sha256')==artsha and r.get('payload_sha256')==payloadsha and
                 r.get('omf_sha256')==pins['calibration_object']['sha256'] and
                 r.get('map_sha256')==pins['calibration_map']['sha256'] and
                 r.get('exe_sha256')==pins['calibration_exe']['sha256'] and
                 r.get('ordered_fixups')==[] and led.get('scope_offset')==0 and
                 led.get('scope_size')==len(source) and led.get('scope_content_sha256')==sha(source),
                 'FILE provenance/extent/byte identity changed')


def reviewed_claims(root,views,*,verify_targets=False):
    if not PROOF.exists():return {},None
    raw=PROOF.read_bytes();proof=json.loads(raw);validate(proof)
    if verify_targets:need(review()==proof,'native FILE source replay changed')
    claims={}
    for r in proof['rows']:
        name=r['artifact'].removeprefix('th05-')
        need(views[name]['sha256']==r['payload_sha256'],'original FILE target view changed')
        claims.setdefault(name,[]).append(dict(start=r['start'],end=r['end'],kind='verified-vendor-initialized-data',
                                                content_kind='library-initialized-data',instruction_bytes=0,
                                                library='Master 0.23',member=r['member']))
    return claims,sha(raw)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    group=p.add_mutually_exclusive_group(required=True)
    for mode in ('write','check','structural-check'):group.add_argument('--'+mode,action='store_true')
    a=p.parse_args()
    if a.write:record=review();PROOF.write_text(json.dumps(record,indent=2)+'\n')
    else:record=json.loads(PROOF.read_text())
    validate(record)
    if a.check:need(record==review(),'original source-linked FILE data proof changed')
    print('PASS: complete Master FIL 4 + DOS_ROPEN 2 bytes in each of three MZs')

if __name__=='__main__':main()
