#!/usr/bin/env python3
"""Verify full C0L.OBJ initialized _DATA via its real LIDATA and BSSEND fixup.

Borland CODE and DATA are distinct. This proof adds only 144 vendor DATA
bytes; all source writes, the real original/comparison BSSEND word and OMF
linker bindings must agree. There is no authored-game instruction credit.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import struct

from lib.omf import parse_omf
from lib.pc98 import digest_bytes,digest_file
from lib.unit_extents import _index as omf_index
from review_vendor_reserved import load_native,expand_lidata
from review_main_runtime import CRT_SHA256,expected_model,startup
from review_vendor import need,sha,PINS

ROOT=Path(__file__).resolve().parents[1]
PROOF=ROOT/'config/main_c0_data_ownership.json'
DECISION=ROOT/'config/reviewed_main_c0_data.json'
DATA_START=0x209D0
DATA_BYTES=0x90
FIXUP_AT=0x82


def replay(*,native_bss_end:int|None=None)->dict:
    vendor=load_native()
    source=(ROOT/'.analysis/toolchain/installed/tc40j/LIB/C0L.OBJ').read_bytes()
    need(sha(source)==CRT_SHA256,'original Borland C0L.OBJ identity changed')
    segments,groups,names=[None],[None],['']
    body=bytearray(DATA_BYTES);covered=bytearray(DATA_BYTES)
    parts=[];last=None;fixups=[]
    for rec in parse_omf(source):
        data=rec.data
        if rec.name=='LNAMES':
            cursor=0
            while cursor<len(data):
                length=data[cursor];cursor+=1
                names.append(data[cursor:cursor+length].decode('cp437'));cursor+=length
        elif rec.name=='SEGDEF':
            name,_=omf_index(data,3)
            segments.append(names[name])
        elif rec.name=='GRPDEF':
            name,_=omf_index(data,0)
            groups.append(names[name])
        elif rec.name in ('LEDATA','LIDATA'):
            segment,at=omf_index(data,0)
            off=struct.unpack_from('<H',data,at)[0];at+=2
            last=segment
            if segment!=6:continue
            if rec.name=='LEDATA':payload=data[at:]
            else:
                chunks=[]
                while at<len(data):
                    chunk,at=expand_lidata(data,at,DATA_BYTES)
                    chunks.append(chunk)
                payload=b''.join(chunks)
            stop=off+len(payload)
            need(payload and 0<=off<stop<=DATA_BYTES and not any(covered[off:stop]),
                 'unreviewed CRT DATA fragment overlap/gap')
            body[off:stop]=payload
            covered[off:stop]=b'\x01'*len(payload)
            parts.append({'kind':rec.name,'offset':off,'size':len(payload),'sha256':sha(payload)})
        elif rec.name=='FIXUPP' and last==6:
            fixups.append(data)
    need(segments[6]=='_DATA' and segments[16]=='_BSSEND' and groups[1]=='DGROUP',
         'OMF DATA or BSSEND segment name resolution changed')
    need(all(covered) and len(parts)==8 and
         [p['size'] for p in parts]==[4,10,2,4,2,4,6,112],
         'native C0L.OBJ full 144-byte DATA LEDATA/LIDATA coverage changed')
    # Original FIXUPP is C4 62 14 01 10: 16-bit offset, frame DGROUP(1),
    # target _BSSEND(16), located 0x62 past last LEDATA at offset 0x20.
    need(fixups==[bytes.fromhex('c4 62 14 01 10')] and
         parts[-1]['offset']==0x20 and FIXUP_AT==0x20+0x62,
         'real original C0L.OBJ BSSEND OMF binding missing or reordered')
    need(body[FIXUP_AT:FIXUP_AT+2]==b'\0\0',
         'original _BSSEND source word is not a true zero-initialized relocation')
    context=expected_model()
    linked=[]
    for key,owner,layout in [('calibration',vendor.cal,context['calibration']),
                             ('original',vendor.target,context['native'])]:
        observed=startup(owner)
        need(observed==layout,'native CRT linked segment/BSS topology disagrees')
        actual=layout['bss_end'] if key=='calibration' or native_bss_end is None else native_bss_end
        computed=bytearray(body)
        computed[FIXUP_AT:FIXUP_AT+2]=actual.to_bytes(2,'little')
        raw=owner.program_image[layout['dgroup']:layout['dgroup']+DATA_BYTES]
        need(bytes(computed)==raw,'native Borland original CRT initialized DATA bytes differ')
        linked.append({'kind':key,'dgroup':layout['dgroup'],'bss_end':actual,
                       'source_DATA_start':layout['dgroup'],
                       'source_DATA_end':layout['dgroup']+DATA_BYTES,
                       'linked_DATA_sha256':sha(computed)})
    return {'schema_version':1,'kind':'original-Borland-C0L-OMF-DATA-only',
            'artifact':'th05-main','crt_object_sha256':CRT_SHA256,
            'original_target_sha256':PINS['target_sha256'],
            'original_payload_sha256':PINS['target_payload_sha256'],
            'calibration_image_sha256':PINS['calibration_exe_sha256'],
            'native_record_model_sha256':sha(source),
            'source_written_DATA_bytes':DATA_BYTES,'CODE_bytes_claimed':0,
            'authored_credit':0,'CODE_instruction_bytes':0,
            'source_records':parts,'real_BSSEND_fixup_offset':FIXUP_AT,
            'real_BSSEND_FIXUPP_sha256':sha(fixups[0]),
            'verifier_sha256':sha((ROOT/'scripts/review_main_c0_data.py').read_bytes()),
            'original_vendor_model_sha256':sha((ROOT/'scripts/review_main_runtime.py').read_bytes()),
            'source_OMF_parser_sha256':sha((ROOT/'scripts/lib/omf.py').read_bytes()),
            'linked_views':linked}


def validate_public(x:dict)->None:
    need(x.get('schema_version')==1 and x.get('kind')=='original-Borland-C0L-OMF-DATA-only' and
         x.get('artifact')=='th05-main' and
         x.get('crt_object_sha256')==CRT_SHA256 and x.get('native_record_model_sha256')==CRT_SHA256 and
         x.get('original_target_sha256')==PINS['target_sha256'] and
         x.get('original_payload_sha256')==PINS['target_payload_sha256'] and
         x.get('calibration_image_sha256')==PINS['calibration_exe_sha256'] and
         x.get('source_written_DATA_bytes')==DATA_BYTES and
         x.get('CODE_bytes_claimed')==0 and x.get('authored_credit')==0 and
         x.get('CODE_instruction_bytes')==0 and x.get('real_BSSEND_fixup_offset')==FIXUP_AT and
         x.get('real_BSSEND_FIXUPP_sha256')==sha(bytes.fromhex('c4 62 14 01 10')),
         'invalid original CRT complete DATA or false CODE/authorship claim')
    for field,path in [('verifier_sha256','scripts/review_main_c0_data.py'),
                       ('original_vendor_model_sha256','scripts/review_main_runtime.py'),
                       ('source_OMF_parser_sha256','scripts/lib/omf.py')]:
        need(x.get(field)==sha((ROOT/path).read_bytes()),'original Borland verifier input identity changed')
    rows=x.get('source_records',[])
    need([(z.get('kind'),z.get('offset'),z.get('size')) for z in rows]==[
        ('LIDATA',0,4),('LEDATA',4,10),('LIDATA',14,2),('LIDATA',16,4),
        ('LIDATA',20,2),('LIDATA',22,4),('LIDATA',26,6),('LEDATA',32,112)],
        'original C0L source DATA records omit or overlap bytes')
    view=x.get('linked_views',[])
    model=expected_model()
    need([(z.get('kind'),z.get('dgroup'),z.get('bss_end'),z.get('source_DATA_start'),
           z.get('source_DATA_end')) for z in view]==[
        (name,ctx['dgroup'],ctx['bss_end'],ctx['dgroup'],ctx['dgroup']+DATA_BYTES)
        for name,ctx in [('calibration',model['calibration']),('original',model['native'])]],
        'original/calibration C0L DATA linkage must derive from genuine CRT BSSEND')
    for y in rows+view:
        need(isinstance(y.get('sha256',y.get('linked_DATA_sha256')),str) and
             re.fullmatch('[0-9a-f]{64}',y.get('sha256',y.get('linked_DATA_sha256'))) is not None,
             'unverified source/input record content hash')
    if DECISION.exists():
        d=json.loads(DECISION.read_text())
        need(d.get('schema_version')==1 and d.get('artifact')=='th05-main' and
             d.get('decision')=='ADOPT_ONLY_ORIGINAL_C0L_COMPLETE_DATA' and
             d.get('evidence_sha256')==digest_file(PROOF) and
             d.get('source_written_DATA_bytes')==144 and d.get('CODE_bytes_claimed')==0 and
             d.get('authored_credit')==0,'original CRT DATA needs current explicit source decision')


def reviewed_claims(root:Path,view:dict,*,verify_targets:bool=False):
    if not DECISION.exists():return [],None
    need(root.resolve()==ROOT.resolve(),'C0L verifier bound to another checkout')
    proof=json.loads(PROOF.read_text())
    validate_public(proof)
    need(view['sha256']==proof['original_payload_sha256'],
         'pinned C0L vendor DATA belongs to another original MAIN')
    if verify_targets:
        need(replay()==proof,'private original C0L source/CRT target proof differs')
    return [{'start':DATA_START,'end':DATA_START+DATA_BYTES,
             'kind':'verified-vendor-initialized-data','library':'C0L.OBJ','member':'C0L_DATA',
             'content_kind':'library-initialized-data','instruction_bytes':0,'authored_credit':0}],digest_file(DECISION)


def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    mode=p.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write',action='store_true')
    mode.add_argument('--check',action='store_true')
    mode.add_argument('--structural-check',action='store_true')
    args=p.parse_args()
    if args.write:
        if DECISION.exists():raise ValueError('cannot overwrite an accepted real Borland C0L DATA source')
        x=replay()
        PROOF.write_text(json.dumps(x,indent=2)+'\n')
        print('PASS: complete 144-byte original C0L initialized DATA from OMF LIDATA and BSSEND fixup')
    else:
        x=json.loads(PROOF.read_text())
        validate_public(x)
        if args.check:
            need(replay()==x,'private original CRT DATA source reconstruction no longer matches')
            print('PASS: actual native and calibration C0L DATA source 144/144 exact')
        else:print('PASS: source-current C0L OMF DATA source, no invented CODE or game authorship')

if __name__=='__main__':main()
