#!/usr/bin/env python3
"""Review two CL.LIB CODE members with explicit uninitialized runtime slots.

Native CL.LIB OMF is the source; no compiler or cold executable replay runs.
Only bytes actually contributed by LEDATA/LIDATA can receive vendor CODE
ownership. The original unwritten in-CODE runtime state stays unknown.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

from lib.borland_library import library_members
from lib.omf import parse_omf
from lib.pc98 import parse_mz
from lib.unit_context import UnitContext,load_unit_target
from lib.unit_oracle import relative_fixups
from review_vendor import VendorReview, deferred_reservations, PINS, idx, need, sha

ROOT=Path(__file__).resolve().parents[1]
PROOF=ROOT/'config/vendor_reserved_ownership.json'
DECISION=ROOT/'config/reviewed_vendor_reserved.json'
SCOPE={'farheap':(0x527f,0x56da,6,6), 'exec':(0xa2fc,0xa6a1,356,2)}
ORIGINAL_TARGET_SHA=PINS['target_sha256']


def load_native():
    root=ROOT
    lib=(root/'.analysis/toolchain/installed/tc40j/LIB/CL.LIB').read_bytes()
    mapraw=(root/'.analysis/builds/main-calibration-b/source/obj/th05/main.map').read_bytes()
    exe=(root/'.analysis/builds/main-calibration-b/source/bin/th05/main.exe').read_bytes()
    for key,bytes_ in (('library_sha256',lib),('calibration_map_sha256',mapraw),('calibration_exe_sha256',exe)):
        need(sha(bytes_)==PINS[key],'private vendor producer pin changed: '+key)
    art,target,_=load_unit_target(UnitContext(root,'main'),UnitContext(root,'main').config())
    need(art['sha256']==ORIGINAL_TARGET_SHA and sha(target.program_image)==PINS['target_payload_sha256'],
         'pinned TH05 MAIN original differs')
    cal=parse_mz(exe)
    need(cal.valid,'invalid pinned Borland calibration image')
    return VendorReview(lib,mapraw,cal,target)


def expand_lidata(data:bytes,cursor:int,maxlen:int,depth:int=0)->tuple[bytes,int]:
    need(depth<16 and cursor+4<=len(data),'nested OMF LIDATA exceeds structural bounds')
    repeat=int.from_bytes(data[cursor:cursor+2],'little')
    count=int.from_bytes(data[cursor+2:cursor+4],'little')
    cursor+=4
    if count:
        pieces=[]
        for _ in range(count):
            piece,cursor=expand_lidata(data,cursor,maxlen,depth+1)
            pieces.append(piece)
            need(sum(len(z) for z in pieces)<=maxlen,'nested LIDATA oversized')
        block=b''.join(pieces)
    else:
        need(cursor<len(data),'missing LIDATA atom size')
        n=data[cursor];cursor+=1
        need(cursor+n<=len(data),'LIDATA atom truncation')
        block=data[cursor:cursor+n];cursor+=n
    need(repeat*len(block)<=maxlen,'LIDATA expansion exceeds CODE')
    return block*repeat,cursor


def reconstruct(review:VendorReview,name:str)->dict:
    expected=SCOPE[name]
    conlist=[c for c in review.contribs if c['module'].casefold()==name and
             c['cl']=='CODE' and c['start']==expected[0] and c['size']==expected[1]-expected[0]]
    need(len(conlist)==1,'missing original complete vendor member CODE MAP')
    con=conlist[0];mod=review.mods[name]
    si=next(i for i,seg in enumerate(mod['segs']) if seg and seg['name']==con['segment'] and seg['cl']=='CODE')
    size=con['size']
    need(mod['segs'][si]['size']==size and con['segment']=='_TEXT','native CODE SEGDEF/MAP mismatch')
    allowed={'THEADR','COMENT','LNAMES','SEGDEF','GRPDEF','EXTDEF','PUBDEF','LEDATA','FIXUPP','LIDATA','ALIAS','MODEND'}
    need(not set(mod['records'])-allowed,'unsupported real vendor object records')
    buf=bytearray(size)
    cover=bytearray(size)
    sources=[]

    def source_write(off:int,bytes_:bytes,kind:str,record_offset:int):
        end=off+len(bytes_)
        need(0<=off<end<=size and not any(cover[off:end]),'source CODE write overlap or escapes SEGDEF')
        buf[off:end]=bytes_
        cover[off:end]=b'\1'*len(bytes_)
        sources.append({'kind':kind,'offset':off,'size':len(bytes_),'sha256':sha(bytes_),
                        'record_offset':record_offset})

    for b in mod['blocks']:
        if b['segment']==si:
            source_write(b['offset'],b['data'],'LEDATA',b['record_offset'])

    recs=parse_omf(bytes.fromhex('800200007e')+mod['program_records'])
    for rec in recs:
        if rec.name!='LIDATA':continue
        seg,at=idx(rec.data,0)
        need(at+2<=len(rec.data),'LIDATA source offset unavailable')
        off=int.from_bytes(rec.data[at:at+2],'little');at+=2
        need(seg==si,'unreviewed other-segment LIDATA')
        chunks=[]
        while at<len(rec.data):
            expanded,at=expand_lidata(rec.data,at,size)
            chunks.append(expanded)
            need(sum(map(len,chunks))<=size,'LIDATA total oversized')
        source_write(off,b''.join(chunks),'LIDATA',rec.offset-5)

    gaps=[]
    at=0
    while at<size:
        if cover[at]:at+=1;continue
        end=at+1
        while end<size and not cover[end]:end+=1
        gaps.append((at,end-at))
        at=end
    need(gaps==[(expected[2],expected[3])],'unexpected CODE reservation/source gap')
    gapoffset,gapsize=gaps[0]
    a=con['start']+gapoffset
    for img in (review.cal.program_image,review.target.program_image):
        need(img[a:a+gapsize]==bytes(gapsize),'native runtime reservation is not zero')
    need(not relative_fixups(review.target,a,gapsize),'runtime reservation contains original relocation')

    # Validate one actual runtime read and one actual write of the unwritten
    # CS: variable by reading the target instruction sequences, not by
    # guessing that all uninitialized CODE is harmless padding.
    text=review.target.program_image[con['start']:con['start']+size]
    if name=='exec':
        for byte_string in (bytes.fromhex('2e a3 60 a4'),bytes.fromhex('2e 8e 06 60 a4'),
                            bytes.fromhex('2e fe 0e 62 a4')):
            need(byte_string in text,'native exec runtime CS: slot access missing')
    else:
        for byte_string in (bytes.fromhex('2e 8c 1e 85 52'),bytes.fromhex('2e 89 16 87 52'),
                            bytes.fromhex('2e a3 89 52'),bytes.fromhex('2e 8b 36 89 52')):
            need(byte_string in text,'native farheap runtime CS: slot access missing')

    # Every CODE FIXUPP must belong to actually emitted source bytes, with
    # true original byte location/width/target/frame. Compute linked words
    # and real MZ fixup order, preserving the OMF fixup stream exactly.
    actions=[]
    mz=[]
    visited=set()
    for f in mod['fixups']:
        if f['segment']!=si:continue
        site,kind=f['site'],f['kind'];width={1:2,2:2,3:4}[kind]
        need(all(cover[site:site+width]),'fixup addresses unwritten CODE reservation')
        tm=f['target_method'];ti=f['target_index']
        if tm==0:
            need(0<ti<len(mod['segs']),'unresolved target segment')
            dstcon=review.contribution(mod,ti)
            dstseg=mod['segs'][ti]
            frame=(review.groups[dstcon['group'].casefold()] if dstcon['group']!='(none)'
                   else review.segbases[dstseg['name'].casefold()]//16*16)
            tf,to,binding=frame,dstcon['start']-frame,'segment:'+dstseg['name']
        elif tm==2:
            need(0<ti<len(mod['exts']),'bad target EXTDEF index')
            symbol=mod['exts'][ti]
            tf,to=review.external(symbol)
            binding='external:'+symbol
        else:raise ValueError('unsupported OMF target method for deferred member')
        fm=f['frame_method']
        if fm==5:frame=tf
        elif fm==1:frame=review.groups[mod['groups'][f['frame_index']]['name'].casefold()]
        elif fm==0:frame=review.segbases[mod['segs'][f['frame_index']]['name'].casefold()]//16*16
        else:raise ValueError('unreviewed OMF FIXUPP frame method')
        old=int.from_bytes(buf[site:site+2],'little')
        targetlinear=tf+to+f['displacement']
        start=site;length=width
        if kind==1:
            value=(old+targetlinear-(con['start']+site+2 if f['relative'] else frame)) & 0xffff
            data=value.to_bytes(2,'little');op='relative16' if f['relative'] else 'offset16'
        elif kind==2:
            need(not f['relative'],'relative segment unsupported')
            data=((old+frame//16)&0xffff).to_bytes(2,'little')
            mz.append(site);op='segment16'
        else:
            need(not f['relative'],'relative far pointer unsupported')
            oldseg=int.from_bytes(buf[site+2:site+4],'little')
            off=(old+targetlinear-frame)&0xffff
            seg=(oldseg+frame//16)&0xffff
            data=off.to_bytes(2,'little')+seg.to_bytes(2,'little')
            source_frame=review.segbases[con['segment'].casefold()]//16*16
            if site>0 and buf[site-1]==0x9a and seg==source_frame//16:
                rel=(old+targetlinear-(con['start']+site+4))&0xffff
                smart=b'\x90\x0e\xe8'+rel.to_bytes(2,'little')
                if review.cal.program_image[con['start']+site-1:con['start']+site+4]==smart:
                    start=site-1;length=5;data=smart
                    op='linked-same-segment-far-call'
                else:
                    mz.append(site+2);op='far-pointer16:16'
            else:
                mz.append(site+2);op='far-pointer16:16'
        need(not visited.intersection(range(start,start+length)), 'overlapping actual LINK FIXUPP writes')
        need(all(cover[start:start+length]),'linked FIXUPP touches unsupplied CODE')
        visited.update(range(start,start+length))
        buf[start:start+length]=data
        actions.append({'site':site,'kind':kind,'write_start':start,'write_size':length,
                        'operation':op,'binding':binding,'frame':frame,'target_frame':tf,
                        'target_offset':to,'byte_sha256':sha(data)})
    need(bytes(buf)==review.cal.program_image[con['start']:con['start']+size],
         'native CL.LIB OMF linked bytes differ from original calibration')
    need(bytes(buf)==review.target.program_image[con['start']:con['start']+size],
         'native CL.LIB linked bytes differ from original game')
    need(relative_fixups(review.cal,con['start'],size)==mz==relative_fixups(review.target,con['start'],size),
         'original ordered MZ relocations differ from native CL FIXUPP stream')
    need(review.target.program_image.find(bytes(buf))==con['start'] and
         review.target.program_image.find(bytes(buf),con['start']+1)<0,
         'unreviewed occurrence collision in main load image')
    # Fail closed on the exact OMF byte coverage independently corroborated
    # by the previously deferred native-ledger partition.
    old=deferred_reservations(review,mod,con)
    need(old['unwritten_SEGDEF_ranges'][0]['offset']==gapoffset and
         old['unwritten_SEGDEF_ranges'][0]['size']==gapsize,
         'prior deferred native OMF model disagrees')
    source_spans=[]
    i=0
    while i<size:
        if not cover[i]:i+=1;continue
        j=i+1
        while j<size and cover[j]:j+=1
        source_spans.append({'start':con['start']+i,'end':con['start']+j,'size':j-i})
        i=j
    need(sum(x['size'] for x in source_spans)==size-gapsize,'vendor source bytes not accounted')
    return {'member':name,'start':con['start'],'end':con['start']+size,'size':size,
            'member_program_sha256':mod['program_sha256'],
            'linked_extent_sha256':sha(bytes(buf)),
            'source_written_bytes':size-gapsize,'source_spans':source_spans,
            'CODE_SEGDEF':mod['segs'][si],
            'CODE_records':sorted(sources,key=lambda x:(x['offset'],x['kind'])),
            'runtime_unwritten_range':{'start':a,'end':a+gapsize,'bytes':gapsize,
                                         'original_and_calibration_zero':True,
                                         'authored_credit':0,'vendor_claim':False},
            'ordered_MZ_fixups':mz,'fixup_actions':actions,
            'unique_complete_original_extent':True}


def generate()->dict:
    review=load_native()
    rows=[reconstruct(review,name) for name in SCOPE]
    return {'schema_version':1,'kind':'pinned-CL-exec-farheap-actual-record-only',
            'artifact':'th05-main','classification':'third-party-OMF-CODE-not-all-instructions',
            'authored_credit':0,'unwritten_bytes_claimed':0,
            'native_inputs':PINS,'library_parser_sha256':sha((ROOT/'scripts/lib/borland_library.py').read_bytes()),
            'prior_vendor_verifier_sha256':sha((ROOT/'scripts/review_vendor.py').read_bytes()),
            'prior_vendor_evidence_sha256':sha((ROOT/'config/vendor_ownership.json').read_bytes()),
            'verifier_sha256':sha((ROOT/'scripts/review_vendor_reserved.py').read_bytes()),
            'members':rows,'source_written_total':sum(z['source_written_bytes'] for z in rows),
            'unwritten_total':sum(z['runtime_unwritten_range']['bytes'] for z in rows)}


def validate_public(proof:dict)->None:
    need(proof.get('schema_version')==1 and proof.get('kind')=='pinned-CL-exec-farheap-actual-record-only' and
         proof.get('artifact')=='th05-main' and proof.get('classification')=='third-party-OMF-CODE-not-all-instructions' and
         proof.get('authored_credit')==0 and proof.get('unwritten_bytes_claimed')==0 and
         proof.get('native_inputs')==PINS and proof.get('source_written_total')==2040 and
         proof.get('unwritten_total')==8,'invalid original two-member CODE source totals')
    for field,path in (('library_parser_sha256','scripts/lib/borland_library.py'),
                       ('prior_vendor_verifier_sha256','scripts/review_vendor.py'),
                       ('prior_vendor_evidence_sha256','config/vendor_ownership.json'),
                       ('verifier_sha256','scripts/review_vendor_reserved.py')):
        need(proof.get(field)==sha((ROOT/path).read_bytes()),'vendor verifier source changed: '+path)
    members=proof.get('members',[])
    need([x.get('member') for x in members]==list(SCOPE),'unreviewed vendor member selection')
    prior_deferred={x['member']:x for x in json.loads((ROOT/'config/vendor_ownership.json').read_text())['deferred']}
    need(set(prior_deferred)==set(SCOPE),'the pinned prior code-reservation inventory changed')
    for m in members:
        a,b,gap,n=SCOPE[m['member']]
        need(m.get('start')==a and m.get('end')==b and m.get('size')==b-a and
             m.get('source_written_bytes')==b-a-n and
             m.get('runtime_unwritten_range')=={'start':a+gap,'end':a+gap+n,'bytes':n,
                                                  'original_and_calibration_zero':True,
                                                  'authored_credit':0,'vendor_claim':False},
             'non-source CODE reservation was falsely claimed')
        spans=m.get('source_spans',[])
        need([(z['start'],z['end'],z['size']) for z in spans]==
             [(a,a+gap,gap),(a+gap+n,b,b-a-gap-n)],
             'verified vendor source spans contain unowned runtime variables')
        need(m.get('unique_complete_original_extent') is True and
             isinstance(m.get('CODE_records'),list) and m['CODE_records'] and
             isinstance(m.get('fixup_actions'),list) and
             isinstance(m.get('ordered_MZ_fixups'),list),
             'missing real OMF source/FIXUPP evidence')
        hashes = ([m['member_program_sha256'],m['linked_extent_sha256']]
                  + [z['sha256'] for z in m['CODE_records']]
                  + [z['byte_sha256'] for z in m['fixup_actions']])
        for v in hashes:
            need(isinstance(v,str) and re.fullmatch('[0-9a-f]{64}',v) is not None,
                 'unverified original source record hash')
        prior=prior_deferred[m['member']]
        need(m['member_program_sha256']==prior['member_program_sha256'] and
             m['linked_extent_sha256']==prior['linked_CODE_sha256'],
             'private original member/source identity differs from pinned evidence')
        actual_records=sorted([(z['kind'],z['offset'],z['size'],z['sha256']) for z in m['CODE_records']])
        prior_records=sorted([('LEDATA',z['offset'],z['size'],z['sha256']) for z in prior['CODE_LEDATA']]
                             + [('LIDATA',z['offset'],z['size'],z['sha256']) for z in prior['LIDATA']])
        need(actual_records==prior_records,'native actual OMF source writes differ from pinned source')
        actions=m['fixup_actions']
        need(len(actions)==(49 if m['member']=='farheap' else 21) and
             [z['site'] for z in actions]==sorted(set(z['site'] for z in actions)) and
             m['ordered_MZ_fixups']==[],
             'original linked FIXUPP location/order changed')
        gap_a,gap_b=a+gap,a+gap+n
        writes=set()
        for action in actions:
            at,size=action.get('write_start'),action.get('write_size')
            need(type(at) is int and type(size) is int and
                 0<=at<at+size<=b-a and not (at<gap+n and at+size>gap) and
                 not writes.intersection(range(at,at+size)),
                 'original FIXUPP claims the unwritten runtime state slot')
            writes.update(range(at,at+size))
    # Independent explicit public adoption; no whole-member CODE claim is
    # permitted from the checked but unwritten runtime data slots.
    if DECISION.exists():
        d=json.loads(DECISION.read_text())
        need(d.get('schema_version')==1 and d.get('artifact')=='th05-main' and
             d.get('evidence_sha256')==sha(PROOF.read_bytes()) and
             d.get('decision')=='ADOPT_ONLY_OMF_SOURCE_WRITTEN_CODE_SPANS' and
             d.get('members')==list(SCOPE) and d.get('authored_credit')==0 and
             d.get('unwritten_bytes_claimed')==0,'vendor reserved review decision missing or stale')


def reviewed_claims(root:Path,view:dict,*,verify_targets:bool=False):
    global ROOT,PROOF,DECISION
    # The normal checkout has no per-user active root switch; keep a fail-
    # closed pointer check so the ownership caller cannot silently redirect.
    need(root.resolve()==ROOT.resolve(),'vendor owner root changed')
    if not DECISION.exists():return [],None
    proof=json.loads(PROOF.read_text())
    validate_public(proof)
    need(proof['native_inputs']['target_payload_sha256']==view['sha256'],
         'original vendor CODE target load image changed')
    if verify_targets:
        need(generate()==proof,'private exact vendor record replay differs')
    claims=[]
    for m in proof['members']:
        for part in m['source_spans']:
            claims.append({'start':part['start'],'end':part['end'],'kind':'verified-vendor-code',
                           'content_kind':'library-OMF-CODE', 'library':'CL.LIB',
                           'member':m['member'], 'authored_credit':0})
    return claims,sha(DECISION.read_bytes())


def main()->int:
    parser=argparse.ArgumentParser(description=__doc__)
    flags=parser.add_mutually_exclusive_group(required=True)
    flags.add_argument('--write',action='store_true')
    flags.add_argument('--check',action='store_true')
    flags.add_argument('--structural-check',action='store_true')
    args=parser.parse_args()
    if args.write:
        if DECISION.exists():raise ValueError('reviewer cannot rewrite an adopted record without a new explicit decision')
        p=generate();PROOF.write_text(json.dumps(p,indent=2)+'\n');
        print('PASS: reviewed native CL.LIB exec/farheap source-write record',p['source_written_total'],'bytes, gaps',p['unwritten_total'])
    elif args.check:
        p=json.loads(PROOF.read_text());validate_public(p)
        need(generate()==p,'private OMF library/MAP/target replay disagrees with public evidence')
        print('PASS: rechecked private original vendor exec/farheap actual CODE records')
    else:
        validate_public(json.loads(PROOF.read_text()))
        print('PASS: public source-backed CL.LIB vendor reservations review; private binary not read')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
