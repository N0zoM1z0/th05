#!/usr/bin/env python3
"""Original MAIN 256-byte Master ATAN8 byte table (never alignment or game CODE).

Source-linked review of the complete original author initializer, retained
native TASM ordinary DATA LEDATA and linked calibration/original MZ views.
Only bounded checks; no compiler, emulator, or whole-program replay.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

from lib.omf import parse_omf
from lib.pc98 import digest_file, parse_mz
from lib.unit_context import UnitContext, load_unit_target
from lib.unit_oracle import relative_fixups
from review_master import idx, need, pinned, sha, stored_lzh

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / 'config/master_vendor_ownership.json'
PROOF = ROOT / 'config/main_atan8_data_ownership.json'
DECISION = ROOT / 'config/reviewed_main_atan8_data.json'
NATIVE_SOURCE = ROOT / '.analysis/builds/main-calibration-b/source/libs/master.lib/atan8[data].asm'
START, SIZE, CAL_START = 0x20C2E, 256, 0x20C50
OMF_OFFSET, OMF_LENGTH = 0x1E0, 258
# Two zeros in the following physical LEDATA are not part of the 256 values.
UNKNOWN_ALIGN = (START + SIZE, START + SIZE + 2)


def table(raw: bytes, *, encoding: str) -> tuple[bytes, int]:
    lines = raw.decode(encoding).replace('\r\n', '\n').replace('\r', '\n').splitlines()
    sources = []
    started = False
    for line in lines:
        statement = line.split(';', 1)[0].strip()
        if statement == 'AtanTable8' or statement == '_AtanTable8 label byte':
            continue
        match = re.fullmatch(r'(?:AtanTable8\s+)?db\s+([0-9,\s]+)', statement, flags=re.I)
        if match:
            values = [v.strip() for v in match[1].split(',')]
            need(len(values) == 16 and all(re.fullmatch(r'[0-9]+', v) for v in values),
                 'original ATAN8 DATA row must hold sixteen literal bytes')
            sources.append([int(v) for v in values]);started = True
        elif started and statement:
            break
    need(len(sources) == 16 and all(len(v) == 16 for v in sources),
         'original ATAN8 needs exactly sixteen complete 16-byte rows')
    payload = bytes(x for line in sources for x in line)
    need(len(payload) == SIZE and payload[:4] == b'\0'*4 and
         payload[-6:] == b'\x20'*6 and
         all(payload[i] <= payload[i+1] for i in range(SIZE-1)),
         'original bytewise ATAN8 monotonic lookup differs')
    return payload, len(sources)


def omf_data(raw: bytes, expected: bytes) -> dict:
    names = [''];segments = [None];source_ledatas = []
    last = None
    for rec in parse_omf(raw):
        b = rec.data
        if rec.name == 'LNAMES':
            i = 0
            while i < len(b):
                n = b[i];i += 1
                need(i+n <= len(b), 'original OMF name truncated')
                names.append(b[i:i+n].decode('ascii'));i += n
        elif rec.name == 'SEGDEF':
            ni,i=idx(b,3);ci,i=idx(b,i);oi,i=idx(b,i)
            need(ni < len(names) and ci < len(names), 'original OMF SEGDEF names changed')
            segments.append((names[ni],names[ci],int.from_bytes(b[1:3],'little')))
        elif rec.name in ('LEDATA','LIDATA'):
            si,i = idx(b,0)
            need(0 < si < len(segments), 'invalid original DATA segment')
            ofs=int.from_bytes(b[i:i+2],'little');i+=2
            body=b[i:] if rec.name=='LEDATA' else None
            if segments[si][0] == '_DATA':
                source_ledatas.append((rec.name,ofs,body,rec.offset))
            last = (si,ofs,body)
        elif rec.name == 'FIXUPP':
            # The OMF grammar binds each FIXUPP record to the preceding
            # LEDATA. The ATAN8 producer has none, so no fixup can be hidden
            # inside the reviewed 256-byte table.
            if last and segments[last[0]][0] == '_DATA' and last[2] is not None:
                left,right=last[1],last[1]+len(last[2])
                need(not (left < OMF_OFFSET+SIZE and right > OMF_OFFSET),
                     'unreviewed original ATAN8 DATA relocation')
    scoped=[(kind,ofs,body,where) for kind,ofs,body,where in source_ledatas
            if ofs <= OMF_OFFSET < ofs+(len(body) if body is not None else 0)]
    need(len(scoped)==1,'original ATAN8 requires one genuine ordinary DATA LEDATA')
    kind,offset,body,record_offset=scoped[0]
    need(kind=='LEDATA' and offset==OMF_OFFSET and len(body)==OMF_LENGTH and
         body[:SIZE] == expected and body[SIZE:] == b'\0\0',
         'native original Master ATAN8 256 literal bytes and two unwritten align bytes differ')
    need(all(offset >= OMF_OFFSET+SIZE or offset+(len(body) if body is not None else 0) <= OMF_OFFSET
             for kind,offset,body,where in source_ledatas if where!=record_offset and kind=='LEDATA'),
         'overlapping original DATA LEDATA near ATAN8')
    data_segs=[(i,s) for i,s in enumerate(segments) if s and s[0]=='_DATA' and s[1]=='DATA']
    need(len(data_segs)==1 and data_segs[0][1][2]==8000,
         'native whole MAIN DATA SEGDEF context differs')
    return {'segment_index':data_segs[0][0], 'segment_size':data_segs[0][1][2],
            'LEDATA_record_offset':record_offset, 'LEDATA_local_offset':offset,
            'LEDATA_written_size':len(body), 'LEDATA_sha256':sha(body),
            'lookup_written_bytes':SIZE, 'unclaimed_following_bytes':2,
            'intersecting_FIXUPP':0}


def replay() -> dict:
    root=ROOT
    parent=json.loads(PARENT.read_text())
    author=stored_lzh(pinned(root,parent['inputs']['inner_archive']))['ATAN8.ASM']
    native=NATIVE_SOURCE.read_bytes()
    before,nrows=table(author,encoding='cp932')
    after,native_rows=table(native,encoding='utf8')
    need(before==after and native_rows==nrows==16,
         'independent original Master source is not the native initializer')
    obj=pinned(root,parent['inputs']['calibration_object'])
    omf=omf_data(obj,before)
    map_raw=pinned(root,parent['inputs']['calibration_map'])
    map_text=map_raw.decode('cp437')
    for name in ('AtanTable8','_AtanTable8'):
        matches=re.findall(r'(?im)^\s*209E:0270\s+idle\s+'+re.escape(name)+r'\s*$',map_text)
        need(len(matches)==2,'both original MAP public lists must anchor ATAN8 at 209E:0270')
    ctx=UnitContext(root,'main');cfg=ctx.config()
    art,original,view=load_unit_target(ctx,cfg)
    calibration=parse_mz(pinned(root,parent['inputs']['calibration_exe']))
    need(art['sha256']==parent['inputs']['target']['sha256'] and
         original.program_image[START:START+SIZE] == before and
         calibration.program_image[CAL_START:CAL_START+SIZE] == before,
         'whole original/candidate Master atan byte table differs')
    need(original.program_image.find(before)==START and
         original.program_image.find(before,START+1)<0 and
         not relative_fixups(original,START,SIZE) and
         not relative_fixups(calibration,CAL_START,SIZE),
         'ATAN8 table occurrence or ordered original MZ relocations differ')
    need(original.program_image[UNKNOWN_ALIGN[0]:UNKNOWN_ALIGN[1]]==b'\0\0' and
         calibration.program_image[CAL_START+SIZE:CAL_START+SIZE+2]==b'\0\0',
         'unowned native after-table alignment bytes changed')
    return {'schema_version':1,'kind':'source-backed-original-Master-ATAN8-initialized-DATA',
            'artifact':'th05-main','start':START,'end':START+SIZE,'size':SIZE,
            'calibration_start':CAL_START,'source_written_bytes':SIZE,
            'unowned_following_interval':list(UNKNOWN_ALIGN),
            'DATA_roles':['monotonic-8-bit-atan-lookup'],
            'original_archive_member':'ATAN8.ASM',
            'original_source_sha256':sha(author),'native_source_sha256':sha(native),
            'native_object_sha256':sha(obj),'native_MAP_sha256':sha(map_raw),
            'author_archive_sha256':parent['inputs']['inner_archive']['sha256'],
            'target_sha256':art['sha256'],'target_payload_sha256':sha(original.program_image),
            'calibration_payload_sha256':sha(calibration.program_image),
            'whole_initializer_sha256':sha(before),'original_ordered_MZ':[],
            'calibration_ordered_MZ':[],'original_rows':nrows,
            'native_omf':omf,'verifier_sha256':digest_file(root/'scripts/review_main_atan8_data.py'),
            'authored_credit':0}


def validate(proof: dict, *, decision_required: bool = True) -> None:
    base=json.loads(PARENT.read_text())
    require={'schema_version':1,'kind':'source-backed-original-Master-ATAN8-initialized-DATA',
             'artifact':'th05-main','start':START,'end':START+SIZE,'size':SIZE,
             'calibration_start':CAL_START,'source_written_bytes':SIZE,
             'unowned_following_interval':list(UNKNOWN_ALIGN),
             'DATA_roles':['monotonic-8-bit-atan-lookup'],
             'original_archive_member':'ATAN8.ASM','original_rows':16,
             'author_archive_sha256':base['inputs']['inner_archive']['sha256'],
             'target_sha256':base['inputs']['target']['sha256'],
             'original_ordered_MZ':[],'calibration_ordered_MZ':[],
             'authored_credit':0,
             'verifier_sha256':digest_file(ROOT/'scripts/review_main_atan8_data.py')}
    need(all(proof.get(k)==v for k,v in require.items()),
         'fixed original whole ATAN8 source / relocation / boundary proof differs')
    for k in ('original_source_sha256','native_source_sha256','native_object_sha256',
              'native_MAP_sha256','target_payload_sha256','calibration_payload_sha256',
              'whole_initializer_sha256'):
        v=proof.get(k)
        need(isinstance(v,str) and re.fullmatch('[0-9a-f]{64}',v), 'missing ATAN8 SHA identity '+k)
    need(proof['native_object_sha256']==base['inputs']['calibration_object']['sha256'] and
         proof['native_MAP_sha256']==base['inputs']['calibration_map']['sha256'],
         'ATAN8 genuine retained TASM object / MAP identities differ')
    data=proof.get('native_omf',{})
    need(data.get('segment_size')==8000 and
         data.get('LEDATA_local_offset')==OMF_OFFSET and
         data.get('LEDATA_written_size')==OMF_LENGTH and
         data.get('lookup_written_bytes')==SIZE and
         data.get('unclaimed_following_bytes')==2 and
         data.get('intersecting_FIXUPP')==0 and
         isinstance(data.get('LEDATA_record_offset'),int) and
         re.fullmatch('[0-9a-f]{64}',data.get('LEDATA_sha256','')),
         'original source-written ATAN8 OMF record / alignment changed')
    if decision_required:
        d=json.loads(DECISION.read_text())
        need(d=={'schema_version':1,'decision':'ADOPT_ONLY_ORIGINAL_ATAN8_DATA',
                 'evidence_sha256':digest_file(PROOF),'scope':['th05-main',START,START+SIZE],
                 'CODE_bytes':0,'DATA_bytes':SIZE,'authored_credit':0},
             'reviewed original Master ATAN8 DATA adoption decision differs')


def reviewed_claims(root, *, view, verify_targets=False):
    if not DECISION.exists():return [],None
    need(root.resolve()==ROOT.resolve(), 'wrong ATAN8 source checkout')
    proof=json.loads(PROOF.read_text());validate(proof)
    need(view['sha256']==proof['target_payload_sha256'] and
         view['size'] >= START+SIZE,
         'different original MAIN decoded target')
    if verify_targets:need(replay()==proof,'original ATAN8 source or linked byte evidence differs')
    return ([{'start':START,'end':START+SIZE,'kind':'verified-vendor-initialized-data',
              'content_kind':'library-initialized-data','instruction_bytes':0,
              'library':'Master 0.23','member':'ATAN8'}], digest_file(DECISION))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    group=p.add_mutually_exclusive_group(required=True)
    for flag in ('write','check','structural-check'):group.add_argument('--'+flag,action='store_true')
    opts=p.parse_args()
    if opts.write:
        need(not PROOF.exists() and not DECISION.exists(),
             'cannot overwrite accepted original ATAN8 source proof')
        proof=replay();PROOF.write_text(json.dumps(proof,indent=2)+'\n')
        d={'schema_version':1,'decision':'ADOPT_ONLY_ORIGINAL_ATAN8_DATA',
           'evidence_sha256':digest_file(PROOF),'scope':['th05-main',START,START+SIZE],
           'CODE_bytes':0,'DATA_bytes':SIZE,'authored_credit':0}
        DECISION.write_text(json.dumps(d,indent=2)+'\n')
        validate(proof)
        print('PASS original ATAN8 source/OMF/MZ 256 bytes, two alignment bytes unclaimed')
    else:
        current=json.loads(PROOF.read_text());validate(current)
        if opts.check:need(replay()==current,'original ATAN8 native source bytes differ')
        print('PASS original complete 256-byte Master ATAN8 DATA proof')

if __name__=='__main__':main()
