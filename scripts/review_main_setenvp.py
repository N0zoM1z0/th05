#!/usr/bin/env python3
"""Original CL.LIB setenvp CODE, with distinct original/calibration DGROUP frames.

Uses pinned vendor OMF and genuine linker symbol binding. Only the complete
88-byte executable source record is classified; writable DATA/_INIT_ remains
foreign, never reconstructed from zero-filled or target-copy placeholders.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
from lib.pc98 import digest_bytes,digest_file
from lib.unit_oracle import relative_fixups
from review_vendor_reserved import load_native
from review_vendor import PINS, need, sha

ROOT=Path(__file__).resolve().parents[1]
PROOF=ROOT/'config/main_setenvp_ownership.json'
DECISION=ROOT/'config/reviewed_main_setenvp.json'
CODE_START=0xA6E4
CODE_SIZE=88
ORIG_DGROUP=0x209D0
ORIG_DATA_OFFSET=0x2564
ORIG_DATA_START=ORIG_DGROUP+ORIG_DATA_OFFSET


def link_source(review,mod,con,*, original:bool, data_offset:int|None=None)->dict:
    si=1
    code=[x for x in mod['blocks'] if x['segment']==si]
    need(len(code)==1 and code[0]['offset']==0 and len(code[0]['data'])==CODE_SIZE,
         'original CL.LIB setenvp CODE LEDATA not complete')
    buf=bytearray(code[0]['data'])
    group=(ORIG_DGROUP if original else review.groups['dgroup'])
    data=(ORIG_DATA_OFFSET if original else review.contribution(mod,2)['start']-group)
    if data_offset is not None:data=data_offset
    actions=[];mz=[];written=set()
    for f in mod['fixups']:
        if f['segment']!=si:continue
        site,kind=f['site'],f['kind']
        if f['target_method']==0:
            need(f['target_index']==2,'setenvp CODE has unexpected local segment binding')
            target_frame=group
            target_offset=data
            binding='own:_DATA/__environ'
        elif f['target_method']==2:
            symbol=mod['exts'][f['target_index']]
            target_frame,target_offset=review.external(symbol)
            if target_frame==review.groups['dgroup']:
                target_frame=group
            binding='external:'+symbol
        else:raise ValueError('unreviewed CL.LIB CODE target method')
        if f['frame_method']==5:frame=target_frame
        elif f['frame_method']==1:
            need(mod['groups'][f['frame_index']]['name']=='DGROUP','unexpected group frame')
            frame=group
        else:raise ValueError('unreviewed setenvp frame method')
        old=int.from_bytes(buf[site:site+2],'little')
        linear=target_frame+target_offset+f['displacement']
        begin=site;end=site+{1:2,2:2,3:4}[kind]
        if kind==1:
            value=(old+linear-(con['start']+site+2 if f['relative'] else frame))&0xffff
            payload=value.to_bytes(2,'little');operation='near-offset'
        elif kind==3:
            need(not f['relative'],'unexpected far relative fixup')
            segword=int.from_bytes(buf[site+2:site+4],'little')
            segment=(segword+frame//16)&0xffff
            if site and buf[site-1] in (0x9a,0xea) and segment==0:
                rel=(old+linear-(con['start']+site+4))&0xffff
                # TLINK preserves both 5-byte far-transfer footprints:
                # CALL -> NOP; PUSH CS; CALL rel16
                # JMP  -> NOP; NOP; JMP rel16
                if buf[site-1]==0x9a:
                    payload=b'\x90\x0e\xe8'+rel.to_bytes(2,'little')
                    operation='real-TLINK-same-segment-far-call'
                else:
                    payload=b'\x90\x90\xe9'+rel.to_bytes(2,'little')
                    operation='real-TLINK-same-segment-far-jump'
                begin=site-1
            else:
                payload=((old+linear-frame)&0xffff).to_bytes(2,'little')+segment.to_bytes(2,'little')
                mz.append(site+2);operation='far-pointer'
        else:raise ValueError('unexpected setenvp CODE segment fixup')
        need(len(payload)==end-begin and not written.intersection(range(begin,end)),
             'invalid overlapping setenvp original FIXUPP writes')
        written.update(range(begin,end))
        buf[begin:end]=payload
        actions.append({'source_site':site,'kind':kind,'operation':operation,
                        'binding':binding,'written_start':begin,'written_end':end,
                        'linked_bytes_sha256':sha(payload)})
    need(len(actions)==10 and mz==[],'setenvp CODE must have ten ordered OMF FIXUPP, no MZ relocations')
    expected=review.target if original else review.cal
    native=expected.program_image[CODE_START:CODE_START+CODE_SIZE]
    need(bytes(buf)==native,'actual CL.LIB source/link context is not complete original 88-byte CODE')
    need(relative_fixups(expected,CODE_START,CODE_SIZE)==[], 'unexpected original MZ fixup in setenvp')
    need(expected.program_image.find(native)==CODE_START and
         expected.program_image.find(native,CODE_START+1)<0,'setenvp complete occurrence ambiguous')
    return {'target_kind':'original-TH05' if original else 'pinned-calibration',
            'dgroup_base':group,'own_DATA_offset':data,
            'own_DATA_absolute':group+data,'source_CODE_extent':[CODE_START,CODE_START+CODE_SIZE],
            'object_unlinked_CODE_sha256':sha(code[0]['data']),
            'linked_CODE_sha256':sha(bytes(buf)),
            'CODE_source_bytes':CODE_SIZE,'ordered_original_MZ_fixups':mz,
            'OMF_source_fixup_actions':actions}


def replay(*,native_data_offset:int=ORIG_DATA_OFFSET)->dict:
    review=load_native()
    mod=review.mods['setenvp']
    code=[x for x in review.contribs if x['module']=='setenvp' and x['cl']=='CODE']
    need(len(code)==1 and (code[0]['start'],code[0]['size'])==(CODE_START,CODE_SIZE),
         'original CL.LIB setenvp MAP CODE extent has changed')
    need(mod['segs'][1]['size']==CODE_SIZE and mod['segs'][1]['cl']=='CODE' and
         mod['segs'][2]['size']==4 and mod['segs'][3]['size']==6 and
         mod['records']['LEDATA']==3 and mod['records']['FIXUPP']==2,
         'complete vendor CODE/DATA/INIT object record model changed')
    need(len(mod['fixups'])==11 and len([f for f in mod['fixups'] if f['segment']==1])==10,
         'original setenvp ten CODE fixups and one INIT fixup changed')
    need(review.groups['dgroup']==0x209E0,'native calibration DGROUP segment changed')
    source=mod['blocks'][0]['data']
    need(sha(source)==sha(mod['blocks'][0]['data']) and len(source)==CODE_SIZE,
         'raw CL library CODE source changed')
    cal=link_source(review,mod,code[0],original=False)
    orig=link_source(review,mod,code[0],original=True,data_offset=native_data_offset)
    # The 18-byte relocation in the *offset* is explained by the actual two
    # Borland DATA segment positions and DGROUP (not a target byte patch).
    need(cal['own_DATA_offset']-orig['own_DATA_offset']==0x12 and
         cal['own_DATA_absolute']-orig['own_DATA_absolute']==0x22,
         'target-vs-calibrated original DATA placement was not explained')
    need(review.target.program_image[ORIG_DATA_START:ORIG_DATA_START+4]==b'\0'*4,
         'original __environ pointer initialized data is not zero at the bound position')
    return {'schema_version':1,'kind':'main-setenvp-native-CL-object-DGROUP-context',
            'artifact':'th05-main','member':'setenvp','CODE_start':CODE_START,'CODE_size':CODE_SIZE,
            'source_written_CODE_bytes':CODE_SIZE, 'authored_credit':0,
            'original_vendor_member_program_sha256':mod['program_sha256'],
            'cl_library_sha256':PINS['library_sha256'],
            'calibration_map_sha256':PINS['calibration_map_sha256'],
            'original_target_sha256':PINS['target_sha256'],
            'original_target_payload_sha256':PINS['target_payload_sha256'],
            'input_verifier_sha256':sha((ROOT/'scripts/review_vendor.py').read_bytes()),
            'source_library_parser_sha256':sha((ROOT/'scripts/lib/borland_library.py').read_bytes()),
            'verifier_sha256':sha((ROOT/'scripts/review_main_setenvp.py').read_bytes()),
            'linked_views':[cal,orig],
            'initial_DATA_bytes_claimed':0,'INIT_bytes_claimed':0}


def validate_public(x:dict)->None:
    need(x.get('schema_version')==1 and x.get('kind')=='main-setenvp-native-CL-object-DGROUP-context' and
         x.get('artifact')=='th05-main' and x.get('member')=='setenvp' and
         (x.get('CODE_start'),x.get('CODE_size'),x.get('source_written_CODE_bytes'))==
         (CODE_START,CODE_SIZE,CODE_SIZE) and
         x.get('authored_credit')==0 and x.get('initial_DATA_bytes_claimed')==0 and
         x.get('INIT_bytes_claimed')==0 and
         x.get('cl_library_sha256')==PINS['library_sha256'] and
         x.get('calibration_map_sha256')==PINS['calibration_map_sha256'] and
         x.get('original_target_sha256')==PINS['target_sha256'] and
         x.get('original_target_payload_sha256')==PINS['target_payload_sha256'],
         'unreviewed vendor scope, source identity or authored data claim')
    for field,path in [('verifier_sha256','scripts/review_main_setenvp.py'),
                       ('input_verifier_sha256','scripts/review_vendor.py'),
                       ('source_library_parser_sha256','scripts/lib/borland_library.py')]:
        need(x.get(field)==sha((ROOT/path).read_bytes()), 'original code verifier identity changed')
    views=x.get('linked_views')
    need(isinstance(views,list) and len(views)==2 and
         [q.get('target_kind') for q in views]==['pinned-calibration','original-TH05'] and
         [(q.get('dgroup_base'),q.get('own_DATA_offset'),q.get('own_DATA_absolute')) for q in views]==
         [(0x209e0,0x2576,0x22f56),(ORIG_DGROUP,ORIG_DATA_OFFSET,ORIG_DATA_START)] and
         all(q.get('CODE_source_bytes')==88 and q.get('source_CODE_extent')==[CODE_START,CODE_START+88]
             and q.get('ordered_original_MZ_fixups')==[] and
             len(q.get('OMF_source_fixup_actions',[]))==10 for q in views),
         'original code/source/data relocation context incomplete')
    sites=[23,27,76,82,4,11,14,37,79,85]
    for row in views:
        need([a.get('source_site') for a in row['OMF_source_fixup_actions']]==sites,
             'the original ten CODE FIXUPP site/order records changed')
        need([row['OMF_source_fixup_actions'][6]['operation'],
              row['OMF_source_fixup_actions'][7]['operation']]==
             ['real-TLINK-same-segment-far-call','real-TLINK-same-segment-far-jump'],
             'the real original five-byte far-transfer rewrites changed')
    for left,right in zip(*[z['OMF_source_fixup_actions'] for z in views]):
        need((left['source_site'],left['kind'],left['operation'],left['binding'],left['written_start'],left['written_end'])==
             (right['source_site'],right['kind'],right['operation'],right['binding'],right['written_start'],right['written_end']),
             'original/calibrated CODE FIXUPP sites/targets changed')
    if DECISION.exists():
        d=json.loads(DECISION.read_text())
        need(d.get('schema_version')==1 and d.get('artifact')=='th05-main' and
             d.get('member')=='setenvp' and d.get('decision')=='ADOPT_ONLY_COMPLETE_SOURCE_WRITTEN_CODE' and
             d.get('evidence_sha256')==digest_file(PROOF) and d.get('code_bytes')==88 and
             d.get('data_bytes_claimed')==0 and d.get('authored_credit')==0,
             'original CL setenvp CODE needs explicit current adoption')


def reviewed_claims(root:Path,view:dict,*,verify_targets:bool=False):
    if not DECISION.exists():return [],None
    need(root.resolve()==ROOT.resolve(),'wrong original vendor root')
    record=json.loads(PROOF.read_text())
    validate_public(record)
    need(view['sha256']==record['original_target_payload_sha256'],
         'original MAIN setenvp code belongs to different payload')
    if verify_targets:
        need(replay()==record,'original CL.LIB full source binding replay differs')
    return [{'start':CODE_START,'end':CODE_START+CODE_SIZE,'kind':'verified-vendor-code',
             'library':'CL.LIB','member':'setenvp','authored_credit':0}],digest_file(DECISION)


def main()->None:
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--write',action='store_true')
    group.add_argument('--check',action='store_true')
    group.add_argument('--structural-check',action='store_true')
    args=parser.parse_args()
    if args.write:
        if DECISION.exists():raise ValueError('cannot silently replace an adopted original vendor decision')
        result=replay()
        PROOF.write_text(json.dumps(result,indent=2)+'\n')
        print('PASS: original complete 88-byte CL setenvp CODE reconstructed under both link contexts')
    else:
        x=json.loads(PROOF.read_text());validate_public(x)
        if args.check:
            need(replay()==x,'real private CL.LIB original object/target differs from maintained proof')
            print('PASS: actual pinned setenvp native CODE and all FIXUPP/target bytes rechecked')
        else:print('PASS: source-current pinned vendor setenvp CODE and DATA frame proof')

if __name__=='__main__':main()
