#!/usr/bin/env python3
"""Complete original Master RTC/SMEM/VSYNC/memory CODE in OP/MAINE.

Fourteen complete functions per artifact, including the private original RTC
interrupt service routine and the unexported CRTBIOS/VSYNC helpers. Preserve
the original complete PROC boundaries, real CODE LEDATA and ordered FIXUPP/MZ.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

from lib.pc98 import digest_file,parse_mz
from lib.unit_context import UnitContext,load_unit_target
from lib.unit_oracle import relative_fixups
from review_master import pinned,need,sha,stored_lzh,source_blocks
from review_master_grcg import symbolic_source
from review_context_master_large import ROOT,MASTER,real_omf,native_map,whole_source,rebind

PROOF=ROOT/'config/context_memory_vsync.json'
DECISION=ROOT/'config/reviewed_context_memory_vsync.json'
# Original absolute decoded CODE coordinates. Entries correspond to complete
# author FUNC or near PROC spans in the real retained TASM source; do not merge
# VSYNC_START with the adjacent CRTBIOS_COOK and VSYNC_COUNT helper routines.
SCOPE=(
 ('rtc_int_set','atrtcmod.asm','ATRTCMOD.ASM',0x0454,0x0454,145,14),
 ('RTC_INT','atrtcmod.asm','ATRTCMOD.ASM',0x04f8,0x04f8,68,8),
 ('SMEM_RELEASE','smem_release.asm','SMEMREL.ASM',0x2088,0x2222,22,1),
 ('SMEM_WGET','smem_wget.asm','SMEMWGET.ASM',0x209e,0x2238,96,4),
 ('VSYNC_START','vsync.asm','VSYNC.ASM',0x2162,0x2320,106,12),
 ('CRTBIOS_COOK','vsync.asm','VSYNC.ASM',0x21cc,0x238a,10,1),
 ('VSYNC_COUNT','vsync.asm','VSYNC.ASM',0x21d6,0x2394,58,7),
 ('VSYNC_END','vsync.asm','VSYNC.ASM',0x2210,0x23ce,72,7),
 ('VSYNC_WAIT','vsync_wait.asm','VSYNCWAI.ASM',0x2258,0x2416,38,3),
 ('HMEM_LALLOCATE','hmem_lallocate.asm','HMEMLALC.ASM',0x227e,0x24bc,52,0),
 ('MEM_ASSIGN_DOS','mem_assign_dos.asm','MEMASDOS.ASM',0x22b2,0x24f0,34,1),
 ('MEM_ASSIGN','mem_assign.asm','MEMASSIG.ASM',0x22d4,0x2512,38,6),
 ('MEM_ASSIGN_ALL','mem_assign.asm','MEMASSIG.ASM',0x22fa,0x2538,40,2),
 ('HMEM_ALLOCBYTE','memheap.asm','MEMHEAP.ASM',0x2322,0x2560,20,0),
)
ARTIFACTS=('op','maine')


def normalized_author(author,name):
    original=symbolic_source(author)
    if name in ('rtc_int_set','RTC_INT'):
        # The original RTC code is unchanged apart from private CS: scratch
        # names and the actual native `NOPCALL` far-to-near relocation.
        if name=='rtc_int_set':
            need(original.count('calldos_setvect')==2 and
                 original.count('inal,imr')==2 and
                 original.count('outimr,al')==2 and
                 sum(line.count('timerorg') for line in original)==4,
                 'original RTC timer, port, or vector source operands changed')
        else:
            need(sum(line.count('skipslot1') for line in original)==2 and
                 original.count('jmpdwordptrcs:timerorg')==1,
                 'original RTC private label or far dispatch changed')
        return [line.replace('timerorg','rtc_timerorg')
                    .replace('calldos_setvect','nopcalldos_setvect')
                    .replace('inal,imr','inal,rtc_imr')
                    .replace('outimr,al','outrtc_imr,al')
                    .replace('skipslot1','skipslot11')
                for line in original]
    if name not in ('VSYNC_START','CRTBIOS_COOK','VSYNC_COUNT','VSYNC_END'):
        return original
    if name=='VSYNC_START':
        need(original.count('calldos_setvect')==2 and
             original.count('inal,imr')==1 and original.count('outimr,al')==1,
             'original VSYNC_START call/port operands changed')
    if name=='VSYNC_END':
        need(original.count('calldos_setvect')==2 and
             original.count('inal,imr')==2 and original.count('outimr,al')==2 and
             original.count('vsync_leavelabelcallmodel')==1,
             'original VSYNC_END calls/ports/label changed')
    return [line.replace('calldos_setvect','nopcalldos_setvect')
                 .replace('inal,imr','inal,vsync_imr')
                 .replace('outimr,al','outvsync_imr,al')
                 .replace('vsync_leavelabelcallmodel','vsync_leavelabelproc')
            for line in original]


def replay():
    parent=json.loads(MASTER.read_text());archive=stored_lzh(pinned(ROOT,parent['inputs']['inner_archive']))
    rows=[];target_views={}
    for art in ARTIFACTS:
        base=ROOT/f'.analysis/builds/{art}-calibration-a/source'
        module='op' if art=='op' else 'mainem'
        obj=(base/f'obj/th05/{module}.obj').read_bytes()
        segs,blocks,fixups,groups=real_omf(obj)
        map_raw,offsets,public=native_map(art,
            'th05_op.asm' if art=='op' else 'th05_maine_master.asm',segs)
        c=UnitContext(ROOT,art);original=load_unit_target(c,c.config())[1]
        target_views[art]=sha(original.program_image)
        calibration=parse_mz((base/f'bin/th05/{art}.exe').read_bytes())
        cg=int.from_bytes(calibration.program_image[1:3],'little')
        og=int.from_bytes(original.program_image[1:3],'little')
        need(og-cg==(1 if art=='maine' else 0),'original memory/VSYNC CRT frame changed')
        for name,file,author,op_start,maine_start,size,expected_fixups in SCOPE:
            start=op_start if art=='op' else maine_start
            if name=='RTC_INT':
                # A private, complete near RTC ISR at 04F8..053C. `rtc_int_set`
                # is the exported predecessor at 0454 and BCLOSER starts
                # exactly at the original ISR end. The intervening 19 source-
                # unreviewed bytes at 04E5..04F8 remain deliberately unowned.
                need(start==0x04f8 and size==68 and
                     public.get('rtc_int_set')=={0x0454} and
                     public.get('BCLOSER')=={0x053c},
                     'original private RTC interrupt/source boundaries differ')
            elif name in ('CRTBIOS_COOK','VSYNC_COUNT'):
                # Both near procedures are private to VSYNC.ASM and absent
                # from TLINK's exported-public list. The two genuine outer
                # public entries anchor their exact 106/10/58-byte layout.
                a=0x2162 if art=='op' else 0x2320
                z=0x2210 if art=='op' else 0x23ce
                expected=a+106 if name=='CRTBIOS_COOK' else a+116
                need(start==expected and z==a+106+10+58 and
                     public.get('VSYNC_START')=={a} and
                     public.get('VSYNC_END')=={z},
                     'original private CRTBIOS/VSYNC_COUNT source boundary drifted')
            else:
                need(public.get(name)=={start},
                     'native original Master exported public boundary changed: '+name)
            source_path=base/'libs/master.lib'/file
            data=source_path.read_bytes()
            live=[v for v in source_blocks(data,'utf8') if v['name']==name]
            upstream=[v for v in source_blocks(archive[author],'cp932') if v['name']==name]
            need(len(live)==len(upstream)==1,
                 'original author or native Master procedure source missing: '+name)
            canonical=normalized_author(upstream[0]['text'],name)
            need(canonical==symbolic_source(live[0]['text']) and len(canonical)>=7,
                 'original Master function source changed beyond reviewed VSYNC port/call aliases: '+name)
            blob=whole_source(blocks,start,size)
            actions=[v for v in fixups if start<=v['site']<start+size]
            need(len(actions)==expected_fixups,
                 'missing/reordered original Master OMF fixup action: '+name)
            cal,native,linked,mz=rebind(blob,actions,start,offsets,segs,groups,cg,og)
            target=original.program_image[start:start+size]
            need(cal==calibration.program_image[start:start+size] and native==target,
                 'source-written complete Master memory/VSYNC procedure differs: '+name)
            need(mz==relative_fixups(calibration,start,size)==relative_fixups(original,start,size),
                 'ordered native Master MZ relocations differ: '+name)
            need(original.program_image.find(target)==start and
                 original.program_image.find(target,start+1)==-1,
                 'complete Master procedure CODE occurrence is not unique: '+name)
            rows.append({'artifact':'th05-'+art,'member':name,
                         'start':start,'end':start+size,'size':size,
                         'native_source':'libs/master.lib/'+file,
                         'original_archive_member':author,
                         'author_procedure_sha256':sha(upstream[0]['text'].encode('utf8')),
                         'native_procedure_sha256':sha(live[0]['text'].encode('utf8')),
                         'canonical_source_sha256':sha('\n'.join(canonical).encode('utf8')),
                         'native_TASM_source_sha256':sha(data),
                         'actual_OMF_sha256':sha(obj),'actual_MAP_sha256':sha(map_raw),
                         'unlinked_CODE_sha256':sha(blob),
                         'calibrated_CODE_sha256':sha(cal),
                         'original_CODE_sha256':sha(native),
                         'ordered_OMF_actions':linked,'ordered_original_MZ':mz,
                         'authored_credit':0})
    # Do not pretend the 19 bytes after rtc_int_set are part of either
    # reviewed procedure, even when the native source has adjacent labels.
    for art in ARTIFACTS:
        rtc=[r for r in rows if r['artifact']=='th05-'+art and
             r['member'] in ('rtc_int_set','RTC_INT')]
        need(len(rtc)==2 and rtc[0]['end']==0x04e5 and
             rtc[1]['start']==0x04f8,
             'original RTC unknown gap ownership boundary changed')
    return {'schema_version':1,'kind':'original-master-context-complete-SMEM-VSYNC-MEM-CODE',
            'scopes':rows,'source_written_CODE_bytes':sum(r['size'] for r in rows),
            'rtc_unknown_gap':[0x04e5,0x04f8],
            'original_view_sha256':target_views,
            'author_archive_sha256':parent['inputs']['inner_archive']['sha256'],
            'parent_Master_sha256':digest_file(MASTER),
            'verifier_sha256':digest_file(ROOT/'scripts/review_context_memory_vsync.py'),
            'authored_credit':0,'non_CODE_claimed':0}


def validate(data):
    parent=json.loads(MASTER.read_text())
    expected=[('th05-'+art,name,op if art=='op' else maine,size)
              for art in ARTIFACTS for name,_,_,op,maine,size,_ in SCOPE]
    need(data.get('schema_version')==1 and
         data.get('kind')=='original-master-context-complete-SMEM-VSYNC-MEM-CODE' and
         data.get('source_written_CODE_bytes')==sum(x[3] for x in expected) and
         data.get('rtc_unknown_gap')==[0x04e5,0x04f8] and
         data.get('author_archive_sha256')==parent['inputs']['inner_archive']['sha256'] and
         data.get('parent_Master_sha256')==digest_file(MASTER) and
         data.get('verifier_sha256')==digest_file(ROOT/'scripts/review_context_memory_vsync.py') and
         data.get('authored_credit')==data.get('non_CODE_claimed')==0,
         'source-written memory and VSYNC metadata or original identity changed')
    rows=data.get('scopes',[])
    need([(r.get('artifact'),r.get('member'),r.get('start'),r.get('size')) for r in rows]==expected,
         'complete original SMEM/VSYNC/MEM function boundaries changed')
    v=data.get('original_view_sha256',{})
    need(set(v)==set(ARTIFACTS) and all(re.fullmatch('[0-9a-f]{64}',sha) for sha in v.values()),
         'original target view identities missing')
    for r in rows:
        spec=next((q for q in SCOPE if q[0]==r['member']),None)
        need(spec is not None and r['end']==r['start']+r['size'] and
             r['native_source']=='libs/master.lib/'+spec[1] and
             r['original_archive_member']==spec[2] and
             len(r['ordered_OMF_actions'])==spec[6] and
             r['ordered_original_MZ']==[x['site'] for x in r['ordered_OMF_actions'] if x['kind']==2] and
             r['authored_credit']==0,
             'invalid complete original source CODE or ordered FIXUPP record')
        for field in ('author_procedure_sha256','native_procedure_sha256',
                      'canonical_source_sha256','native_TASM_source_sha256',
                      'actual_OMF_sha256','actual_MAP_sha256','unlinked_CODE_sha256',
                      'calibrated_CODE_sha256','original_CODE_sha256'):
            need(isinstance(r.get(field),str) and re.fullmatch('[0-9a-f]{64}',r[field]),
                 'missing Master source/OMF/native SHA-256')
    if DECISION.exists():
        d=json.loads(DECISION.read_text())
        need(d.get('schema_version')==1 and d.get('decision')=='ADOPT_ONLY_ORIGINAL_SMEM_VSYNC_MEMORY_CODE' and
             d.get('evidence_sha256')==digest_file(PROOF) and
             d.get('scopes')==[[r['artifact'],r['member']] for r in rows] and
             d.get('CODE_bytes')==data['source_written_CODE_bytes'] and
             d.get('authored_credit')==d.get('other_claims')==0,
             'original memory/VSYNC explicit adoption stale')


def reviewed_claims(root,artifact,view,*,verify_targets=False):
    if not DECISION.exists():return [],None
    need(root.resolve()==ROOT.resolve(),'wrong original reconstruction checkout')
    record=json.loads(PROOF.read_text());validate(record)
    need(record['original_view_sha256'][artifact]==view['sha256'],
         'original OP/MAINE decoded image changed')
    if verify_targets:need(replay()==record,'actual source-linked original memory/VSYNC CODE differs')
    return ([{'start':r['start'],'end':r['end'],'kind':'verified-vendor-code',
              'library':'original Master 0.23 SMEM/VSYNC/MEM','member':r['member'],
              'authored_credit':0}
             for r in record['scopes'] if r['artifact']=='th05-'+artifact],digest_file(DECISION))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    modes=parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--write',action='store_true')
    modes.add_argument('--check',action='store_true')
    modes.add_argument('--structural-check',action='store_true')
    args=parser.parse_args()
    if args.write:
        need(not PROOF.exists() and not DECISION.exists(),'cannot overwrite accepted original source evidence')
        proof=replay();PROOF.write_text(json.dumps(proof,indent=2)+'\n')
        print('PASS native Master SMEM/VSYNC/MEM original CODE',proof['source_written_CODE_bytes'])
    else:
        proof=json.loads(PROOF.read_text());validate(proof)
        if args.check:
            need(replay()==proof,'original native memory/VSYNC complete CODE differs')
            print('PASS original Master memory/VSYNC source-linked CODE and fixups')
        else:print('PASS Master memory/VSYNC source/decision structural proof')

if __name__=='__main__':main()
