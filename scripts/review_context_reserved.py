#!/usr/bin/env python3
"""Original OP/MAINE CL.LIB exec/farheap CODE with uninitialized CS: slots.

Review only ordinary actual OMF CODE writes, their original FIXUPP records,
LIDATA expansion, linked target bytes and zero-credit unwritten state words.
Existing gapless CL.LIB review decisions and source are unchanged.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

from lib.omf import parse_omf
from lib.pc98 import parse_mz,digest_bytes,digest_file
from lib.unit_context import UnitContext,load_unit_target
from lib.unit_oracle import relative_fixups
from review_vendor import VendorReview, PINS as MAIN_PINS, need, sha, idx
from review_vendor_reserved import expand_lidata
from review_vendor_context import PINS as CONTEXT_PINS,validate_target_context

ROOT=Path(__file__).resolve().parents[1]
CONTEXTS=('op','maine')
SIZES={'farheap':(1115,6,6,49),'exec':(933,356,2,21)}


def proof_path(name:str)->Path:return ROOT/f'config/vendor_reserved_context.{name}.json'
def decision_path(name:str)->Path:return ROOT/f'config/reviewed_vendor_reserved_context.{name}.json'


def native_context(name:str):
    need(name in CONTEXTS,'reserved CODE needs OP or MAINE context')
    c=UnitContext(ROOT,name)
    config=c.config()
    art,target,proof=load_unit_target(c,config)
    validate_target_context(c,config,art,target,proof)
    pin=CONTEXT_PINS[name]
    base=ROOT/f'.analysis/builds/{name}-calibration-a/source'
    program=(base/f'bin/th05/{name}.exe').read_bytes()
    map_bytes=(base/f'obj/th05/{name}.map').read_bytes()
    library=(ROOT/'.analysis/toolchain/installed/tc40j/LIB/CL.LIB').read_bytes()
    need(sha(program)==pin['calibration_exe'] and sha(map_bytes)==pin['calibration_map'] and
         sha(library)==MAIN_PINS['library_sha256'],'pinned CL.LIB or native calibration changed')
    cal=parse_mz(program)
    need(cal.valid,'invalid native source linker output')
    return VendorReview(library,map_bytes,cal,target),pin


def reconstruct(view:VendorReview,name:str)->dict:
    size,gap,ngap,fixup_count=SIZES[name]
    matches=[row for row in view.contribs if row['module'].casefold()==name and
             row['cl']=='CODE' and row['size']==size]
    need(len(matches)==1,'missing complete native source member')
    con=matches[0];mod=view.mods[name]
    seg=next(i for i,z in enumerate(mod['segs']) if z and z['name']==con['segment'] and z['cl']=='CODE')
    need(mod['segs'][seg]['size']==size and con['segment']=='_TEXT',
         'actual native CODE SEGDEF/group/extent mismatch')
    body=bytearray(size);coverage=bytearray(size);source_records=[]

    def cover(off:int,bytes_:bytes,kind:str,source_position:int)->None:
        end=off+len(bytes_)
        need(len(bytes_)>0 and 0<=off<end<=size and not any(coverage[off:end]),
             'original vendor CODE has overlapping/out-of-range source records')
        body[off:end]=bytes_;coverage[off:end]=b'\x01'*len(bytes_)
        source_records.append({'kind':kind,'offset':off,'size':len(bytes_),
                               'sha256':sha(bytes_),'OMF_record_offset':source_position})

    for block in mod['blocks']:
        if block['segment']==seg:cover(block['offset'],block['data'],'LEDATA',block['record_offset'])
    for rec in parse_omf(bytes.fromhex('800200007e')+mod['program_records']):
        if rec.name!='LIDATA':continue
        si,pos=idx(rec.data,0)
        need(pos+2<=len(rec.data) and si==seg,'unreviewed non-CODE LIDATA')
        off=int.from_bytes(rec.data[pos:pos+2],'little');pos+=2
        chunks=[]
        while pos<len(rec.data):
            data,pos=expand_lidata(rec.data,pos,size)
            chunks.append(data)
        cover(off,b''.join(chunks),'LIDATA',rec.offset-5)

    need(sum(coverage)==size-ngap and coverage[gap:gap+ngap]==bytes(ngap) and
         all(coverage[:gap]) and all(coverage[gap+ngap:]),
         'original CODE source omission is not precisely the known runtime CS: state bank')
    source_spans=[[con['start'],con['start']+gap],
                  [con['start']+gap+ngap,con['start']+size]]
    original=view.target.program_image[con['start']:con['start']+size]
    calibrated=view.cal.program_image[con['start']:con['start']+size]
    need(original==calibrated and original[gap:gap+ngap]==bytes(ngap),
         'original/calibration whole CODE does not have identical original zero-state gap')
    state=(con['start']+gap).to_bytes(2,'little')
    if name=='exec':
        need(b'\x2e\xa3'+state in original and b'\x2e\xa1'+state in original,
             'native exec does not actually read and write its uninitialized CS: state')
    else:
        need(b'\x2e\x8e\x1e'+state in original and b'\x2e\x8c\x1e'+state in original,
             'native farheap does not actually read and write its uninitialized CS: state')
    actions=[];mz=[];writes=set()
    for f in mod['fixups']:
        if f['segment']!=seg:continue
        site,kind=f['site'],f['kind']
        need(kind in (1,2,3),'unreviewed source location type')
        tm,ti=f['target_method'],f['target_index']
        if tm==0:
            need(0<ti<len(mod['segs']),'invalid segment target')
            dstcon=view.contribution(mod,ti);dstseg=mod['segs'][ti]
            frame=(view.groups[dstcon['group'].casefold()] if dstcon['group']!='(none)'
                   else view.segbases[dstseg['name'].casefold()]//16*16)
            tf,to,binding=frame,dstcon['start']-frame,'segment:'+dstseg['name']
        elif tm==2:
            need(0<ti<len(mod['exts']),'invalid external target')
            binding='external:'+mod['exts'][ti]
            tf,to=view.external(mod['exts'][ti])
        else:raise ValueError('unsupported actual OMF target method')
        fm=f['frame_method']
        if fm==5:frame=tf
        elif fm==1:frame=view.groups[mod['groups'][f['frame_index']]['name'].casefold()]
        elif fm==0:frame=view.segbases[mod['segs'][f['frame_index']]['name'].casefold()]//16*16
        else:raise ValueError('unsupported real OMF frame method')
        old=int.from_bytes(body[site:site+2],'little')
        targetlinear=tf+to+f['displacement']
        first=site;size_written={1:2,2:2,3:4}[kind]
        if kind==1:
            val=(old+targetlinear-(con['start']+site+2 if f['relative'] else frame))&0xffff
            replacement=val.to_bytes(2,'little')
            mode='relative16' if f['relative'] else 'offset16'
        elif kind==2:
            need(not f['relative'],'relative source segment invalid')
            replacement=((old+frame//16)&0xffff).to_bytes(2,'little')
            mz.append(site);mode='segment16'
        else:
            need(not f['relative'],'relative 16:16 source invalid')
            old_segment=int.from_bytes(body[site+2:site+4],'little')
            offset=(old+targetlinear-frame)&0xffff
            segment=(old_segment+frame//16)&0xffff
            replacement=offset.to_bytes(2,'little')+segment.to_bytes(2,'little')
            code_frame=view.segbases[con['segment'].casefold()]//16*16
            if site>0 and body[site-1]==0x9a and segment==code_frame//16:
                rel=(old+targetlinear-(con['start']+site+4))&0xffff
                smart=b'\x90\x0e\xe8'+rel.to_bytes(2,'little')
                if view.cal.program_image[con['start']+site-1:con['start']+site+4]==smart:
                    first=site-1;size_written=5;replacement=smart
                    mode='real-TLINK-same-segment-far-call'
                else:
                    mz.append(site+2);mode='far16:16'
            else:
                mz.append(site+2);mode='far16:16'
        need(len(replacement)==size_written and not writes.intersection(range(first,first+size_written)) and
             all(coverage[first:first+size_written]),
             'original FIXUPP overwrites another source fixup or missing CODE bytes')
        writes.update(range(first,first+size_written))
        body[first:first+size_written]=replacement
        actions.append({'site':site,'kind':kind,'operation':mode,'binding':binding,
                        'frame':frame,'target_frame':tf,'target_offset':to,
                        'source_write_start':first,'source_write_size':size_written,
                        'linked_bytes_sha256':sha(replacement)})
    need(len(actions)==fixup_count and mz==[] and
         relative_fixups(view.cal,con['start'],size)==mz==relative_fixups(view.target,con['start'],size),
         'source FIXUPP count/order differs from original unsorted MZ relocations')
    need(bytes(body)==calibrated==original,'complete native OMF CODE did not reproduce both actual linked programs')
    need(view.target.program_image.find(original)==con['start'] and
         view.target.program_image.find(original,con['start']+1)<0,
         'original CODE occurrence ambiguous')
    return {'member':name,'start':con['start'],'size':size,'end':con['start']+size,
            'original_member_sha256':mod['program_sha256'],
            'source_written_bytes':size-ngap,'source_written_spans':source_spans,
            'source_records':source_records,'runtime_CS_slot':{'start':con['start']+gap,'end':con['start']+gap+ngap,
                  'bytes':ngap,'authored_credit':0,'source_written':False},
            'complete_original_linked_SHA256':sha(original),
            'ordered_native_MZ_relocations':mz,'OMF_fixup_actions':actions}


def generate(name:str)->dict:
    view,pin=native_context(name)
    rows=[reconstruct(view,k) for k in ('farheap','exec')]
    return {'schema_version':1,'kind':'pinned-context-CL-reserved-CODE-records',
            'context':name,'artifact':'th05-'+name,'origin':'original-Borland-CL-LIB-source-records',
            'authored_credit':0,'instruction_bytes_claimed':0,
            'library_sha256':MAIN_PINS['library_sha256'],
            'packed_target_sha256':pin['packed'],'original_payload_sha256':pin['payload'],
            'calibration_exe_sha256':pin['calibration_exe'],'calibration_map_sha256':pin['calibration_map'],
            'verifier_sha256':sha((ROOT/'scripts/review_context_reserved.py').read_bytes()),
            'source_parser_sha256':sha((ROOT/'scripts/review_vendor_reserved.py').read_bytes()),
            'members':rows,'source_written_total':sum(z['source_written_bytes'] for z in rows),
            'unwritten_total':sum(z['runtime_CS_slot']['bytes'] for z in rows)}


def validate_public(x:dict,name:str)->None:
    need(name in CONTEXTS and x.get('schema_version')==1 and
         x.get('kind')=='pinned-context-CL-reserved-CODE-records' and x.get('context')==name and
         x.get('artifact')=='th05-'+name and x.get('origin')=='original-Borland-CL-LIB-source-records' and
         x.get('authored_credit')==0 and x.get('instruction_bytes_claimed')==0 and
         x.get('library_sha256')==MAIN_PINS['library_sha256'] and
         x.get('packed_target_sha256')==CONTEXT_PINS[name]['packed'] and
         x.get('original_payload_sha256')==CONTEXT_PINS[name]['payload'] and
         x.get('calibration_exe_sha256')==CONTEXT_PINS[name]['calibration_exe'] and
         x.get('calibration_map_sha256')==CONTEXT_PINS[name]['calibration_map'] and
         x.get('source_written_total')==2040 and x.get('unwritten_total')==8 and
         x.get('verifier_sha256')==digest_file(ROOT/'scripts/review_context_reserved.py') and
         x.get('source_parser_sha256')==digest_file(ROOT/'scripts/review_vendor_reserved.py'),
         'unreviewed original CODE, toolchain/target identity or authored credit')
    rows=x.get('members',[])
    legacy=json.loads((ROOT/f'config/vendor_ownership.{name}.json').read_text())
    deferred={z['member']:z for z in legacy['deferred']}
    need([z.get('member') for z in rows]==['farheap','exec'] and
         set(['farheap','exec']).issubset(deferred),'unknown or changed original vendor CODE family')
    # The original CL.LIB member is byte-identical in MAIN, OP and MAINE.
    # Pin the complete OMF record source partition and literal unsorted
    # FIXUPP site sequence against MAIN's separately reviewed member records;
    # only linked external address *values* may vary by executable.
    prior=json.loads((ROOT/'config/vendor_reserved_ownership.json').read_text())
    source_family={row['member']:row for row in prior['members']}
    need(set(source_family)==set(SIZES),'independent MAIN original source family changed')
    for row in rows:
        member=row['member'];size,gap,n,fixups=SIZES[member]
        old=deferred[member];a=old['start']
        need(row['start']==a and row['size']==size and row['end']==a+size and
             row['original_member_sha256']==old['member_program_sha256'] and
             row['source_written_bytes']==size-n and
             row['source_written_spans']==[[a,a+gap],[a+gap+n,a+size]] and
             row['runtime_CS_slot']=={'start':a+gap,'end':a+gap+n,'bytes':n,
                                      'authored_credit':0,'source_written':False} and
             len(row['OMF_fixup_actions'])==fixups and
             row['ordered_native_MZ_relocations']==[] and
             isinstance(row['source_records'],list) and row['source_records'],
             'source-written CODE intervals, OMF FIXUPP or unowned CS: slot changed')
        coverage=sorted((z['kind'],z['offset'],z['offset']+z['size'])
                        for z in row['source_records'])
        expected_records=(
            [('LEDATA',0,6),('LEDATA',12,993),('LEDATA',993,1115)]
            if member=='farheap' else
            [('LEDATA',255,356),('LEDATA',358,933),('LIDATA',0,255)])
        need(coverage==sorted(expected_records),
             'original CODE source record partition or LIDATA unverified')
        donor=source_family[member]
        need(row['original_member_sha256']==donor['member_program_sha256'] and
             sorted((a['kind'],a['offset'],a['size'],a['sha256']) for a in row['source_records'])==
             sorted((a['kind'],a['offset'],a['size'],a['sha256']) for a in donor['CODE_records']),
             'actual original CL.LIB LEDATA/LIDATA source bytes changed from independent proof')
        need([(a['site'],a['kind'],a['source_write_start'],a['source_write_size'])
              for a in row['OMF_fixup_actions']]==
             [(a['site'],a['kind'],a['write_start'],a['write_size'])
              for a in donor['fixup_actions']],
             'actual original 49/21 OMF FIXUPP site/order/width differs from source')
        for field in [row['complete_original_linked_SHA256'],row['original_member_sha256']]+[
                z['sha256'] for z in row['source_records']]+[
                z['linked_bytes_sha256'] for z in row['OMF_fixup_actions']]:
            need(re.fullmatch('[0-9a-f]{64}',field) is not None,
                 'unreviewed vendor original CODE source hash')
    decision=decision_path(name)
    if decision.exists():
        d=json.loads(decision.read_text())
        need(d.get('schema_version')==1 and d.get('artifact')=='th05-'+name and
             d.get('decision')=='ADOPT_ONLY_REAL_OMF_SOURCE_CODE_WRITES' and
             d.get('evidence_sha256')==digest_file(proof_path(name)) and
             d.get('source_written_code_bytes')==2040 and d.get('unwritten_CS_bytes_claimed')==0 and
             d.get('authored_credit')==0 and d.get('members')==['farheap','exec'],
             'explicit two-member original CL.LIB source-review decision missing/stale')


def reviewed_claims(root:Path,name:str,view:dict,*,verify_targets:bool=False):
    if name not in CONTEXTS or not decision_path(name).exists():return [],None
    need(root.resolve()==ROOT.resolve(),'original review checkout differs')
    x=json.loads(proof_path(name).read_text());validate_public(x,name)
    need(view['sha256']==x['original_payload_sha256'],'wrong decoded binary owner')
    if verify_targets:need(generate(name)==x,'actual native linked CODE source differs')
    claims=[]
    for m in x['members']:
        for a,b in m['source_written_spans']:
            claims.append({'start':a,'end':b,'kind':'verified-vendor-code','library':'CL.LIB',
                           'member':m['member'],'authored_credit':0})
    return claims,digest_file(decision_path(name))


def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--context',choices=CONTEXTS,required=True)
    modes=p.add_mutually_exclusive_group(required=True)
    modes.add_argument('--write',action='store_true')
    modes.add_argument('--check',action='store_true')
    modes.add_argument('--structural-check',action='store_true')
    args=p.parse_args()
    if args.write:
        if decision_path(args.context).exists():raise ValueError('must not rewrite adopted vendor proof')
        x=generate(args.context)
        proof_path(args.context).write_text(json.dumps(x,indent=2)+'\n')
        print('PASS:',args.context,'two exact original vendor CODE members:',x['source_written_total'],'source bytes, 8 unknown')
    else:
        x=json.loads(proof_path(args.context).read_text());validate_public(x,args.context)
        if args.check:
            need(generate(args.context)==x,'linked native original CL.LIB CODE changed')
            print('PASS:',args.context,'native original two CODE objects and all 70 FIXUPP revalidated')
        else:print('PASS:',args.context,'public original CL.LIB CODE source only; 8 state bytes unknown')

if __name__=='__main__':main()
