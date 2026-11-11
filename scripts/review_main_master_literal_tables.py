#!/usr/bin/env python3
"""Four complete original Master 0.23 literal DATA tables in TH05 MAIN.

The complete historic ASM source is independently decoded, numeric literal
initializers are evaluated (including UNDF=100 from BGM.INC), and genuine
TASM OMF LEDATA/MAP/linked original MZ bytes agree for each whole table.
Other mutable DATA or unwritten alignment is never adopted.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import struct

from lib.omf import parse_omf
from lib.pc98 import digest_file, parse_mz
from lib.unit_context import UnitContext, load_unit_target
from lib.unit_oracle import relative_fixups
from review_master import idx, need, pinned, sha, stored_lzh

ROOT=Path(__file__).resolve().parents[1]
PARENT=ROOT/'config/master_vendor_ownership.json'
PROOF=ROOT/'config/main_master_literal_tables_ownership.json'
DECISION=ROOT/'config/reviewed_main_master_literal_tables.json'
SOURCE=ROOT/'.analysis/builds/main-calibration-b/source/libs/master.lib'
# Original and retained TASM calibration starts: the native module's DATA
# contribution is based at calibration 20A70, 22h beyond original placement.
TABLES=(
    ('BFNT_ID','BFNTID.ASM','bfnt_id[data].asm',0x20D36,0x20D58,6,'BFNT_ID'),
    ('EDGES','EDGES.ASM','edges[data].asm',0x20D4C,0x20D6E,34,'EDGES'),
    ('BYTE_MASK','WORDMASK.ASM','wordmask[data].asm',0x2107C,0x2109E,8,'BYTE_MASK'),
    ('BGM_NOTE_AND_LENGTH','B_DATA.ASM','bgm[data].asm',0x210B4,0x210D6,176,'note_dat'),
)


def significant_lines(text: bytes,encoding: str):
    return [x.split(';',1)[0].strip().lower() for x in
            text.decode(encoding).replace('\r\n','\n').replace('\r','\n').splitlines()
            if x.split(';',1)[0].strip()]


def source_payload(raw: bytes, name: str, encoding: str, *, undf: int) -> bytes:
    lines=significant_lines(raw,encoding)
    if name=='BFNT_ID':
        need(sum('bfnt_id' in x and 'label' in x for x in lines)==1,
             'original independent BFNT identifier label changed')
        row=[i for i,x in enumerate(lines) if re.fullmatch("bfnt_id\\s+db\\s+'bfnt',01ah",x)]
        need(len(row)==1 and lines[row[0]+1]=='db 0',
             'original six-byte BFNT identifier source changed')
        return b'BFNT\x1a\0'
    if name=='EDGES':
        begin=[i for i,line in enumerate(lines) if re.fullmatch('edges\\s+dw\\s+[01]{16}b',line)]
        need(len(begin)==1,'original EDGES 16-bit word declaration missing')
        words=[]
        for line in lines[begin[0]:]:
            m=re.fullmatch(r'(?:edges\s+)?dw\s+([01]{16})b',line)
            if not m:break
            words.append(int(m[1],2))
        need(len(words)==17 and words[0]==0 and words[-1]==0xffff,
             'complete original seventeen-word EDGES mask table differs')
        return struct.pack('<17H',*words)
    if name=='BYTE_MASK':
        rows=[x for x in lines if re.fullmatch(r'byte_mask\s+db\s+(?:0?[0-9a-f]{1,2}h\s*,?\s*){8}',x)]
        need(len(rows)==1,'original complete eight-byte BYTE_MASK table changed')
        text=rows[0].split('db',1)[1]
        vals=[int(x.strip().removesuffix('h'),16) for x in text.split(',')]
        need(len(vals)==8 and vals==[0xff,0x7f,0x3f,0x1f,0x0f,0x07,0x03,0x01],
             'original byte width mask progression differs')
        return bytes(vals)
    if name=='BGM_NOTE_AND_LENGTH':
        label_lines=[]
        for label in ('note_dat','lcount'):
            starts=[i for i,line in enumerate(lines) if re.match('^'+label+r'\s+dw\s+',line)]
            need(len(starts)==1,'original complete BGM note/duration table declaration changed: '+label)
            offset=starts[0]
            out=[]
            for line in lines[offset:]:
                match=re.fullmatch(r'(?:'+label+r'\s+)?dw\s+([0-9a-z_,\s]+)',line)
                if not match:break
                tokens=[x.strip() for x in match[1].split(',')]
                need(all(re.fullmatch(r'[0-9]+|undf',t) for t in tokens),
                     'original BGM table contains nonliteral note/duration')
                out.extend(undf if tok=='undf' else int(tok) for tok in tokens)
                label_lines.append(line)
            want=24 if label=='note_dat' else 64
            need(len(out)==want and all(0<=v<=65535 for v in out),
                 'original complete BGM note or duration table length changed')
            if label=='note_dat':notes=out
            else:durations=out
        need(notes.count(undf)==7 and durations[0]==64 and durations[-1]==1,
             'original BGM UNDF note sentinel or note duration values differ')
        return struct.pack('<24H',*notes)+struct.pack('<64H',*durations)
    raise ValueError('unreviewed Master initializer')


def native_ledatas(raw: bytes) -> list[dict]:
    names=[''];segs=[None];results=[];last=None
    records=parse_omf(raw)
    for at,rec in enumerate(records):
        b=rec.data
        if rec.name=='LNAMES':
            i=0
            while i<len(b):
                n=b[i];i+=1
                need(i+n<=len(b),'native Master OMF name truncated')
                names.append(b[i:i+n].decode('ascii'));i+=n
        elif rec.name=='SEGDEF':
            ni,i=idx(b,3);ci,i=idx(b,i);oi,i=idx(b,i)
            need(ni<len(names) and ci<len(names),'native original OMF SEGDEF changed')
            segs.append((names[ni],names[ci],int.from_bytes(b[1:3],'little')))
        elif rec.name=='LEDATA':
            si,i=idx(b,0);need(0<si<len(segs),'native OMF LEDATA segment missing')
            offset=int.from_bytes(b[i:i+2],'little');i+=2
            if segs[si][0]=='_DATA':
                results.append({'offset':offset,'bytes':b[i:],'record_offset':rec.offset,
                                'next_record':records[at+1].name,'segment_index':si})
    data_segs=[(i,x) for i,x in enumerate(segs) if x and x[0]=='_DATA' and x[1]=='DATA']
    need(len(data_segs)==1 and data_segs[0][1][2]==8000,
         'real Master MAIN _DATA SEGDEF 8000 bytes changed')
    return results


def replay() -> dict:
    meta=json.loads(PARENT.read_text());root=ROOT
    archive=stored_lzh(pinned(root,meta['inputs']['inner_archive']))
    bgminc=archive['BGM.INC'].decode('cp932').lower()
    need(len(re.findall(r'(?m)^undf\s+equ\s+100\b',bgminc))==1,
         'original upstream BGM undefined note sentinel differs from 100')
    original_art,original,_=load_unit_target(UnitContext(root,'main'),UnitContext(root,'main').config())
    calibration=parse_mz(pinned(root,meta['inputs']['calibration_exe']))
    obj=pinned(root,meta['inputs']['calibration_object'])
    omf=native_ledatas(obj)
    map_bytes=pinned(root,meta['inputs']['calibration_map'])
    map_text=map_bytes.decode('cp437')
    rows=[]
    for name,archive_name,native_name,start,cal_start,size,public in TABLES:
        original_source=archive[archive_name];native_source=(SOURCE/native_name).read_bytes()
        body=source_payload(original_source,name,'cp932',undf=100)
        native_body=source_payload(native_source,name,'utf8',undf=100)
        need(len(body)==size and body==native_body,
             'original independent author and native TASM DATA initializer differ: '+name)
        need(original.program_image[start:start+size]==body and
             calibration.program_image[cal_start:cal_start+size]==body and
             original.program_image.find(body)==start and
             original.program_image.find(body,start+1)<0,
             'unmodified original/calibration source table bytes/unique original position differ: '+name)
        need(not relative_fixups(original,start,size) and
             not relative_fixups(calibration,cal_start,size),
             'original Master literal initialized table unexpectedly contains relocations')
        cal_label=(cal_start//16,cal_start%16)
        # MAP addresses are FRAME:OFFSET with the true original _DATA segment
        # at 209E and its historical linker offset (not linear grouping).
        pub_offset=cal_start-0x209e0
        need(len(re.findall(r'(?im)^\s*209E:'+f'{pub_offset:04X}'+r'\s+idle\s+'+re.escape(public)+r'\s*$',map_text))==2,
             'native original Master DATA MAP public missing at true anchored location: '+name)
        local=cal_start-0x20A70
        evidence=[]
        cover=bytearray(size)
        for rec in omf:
            left=max(rec['offset'],local);right=min(rec['offset']+len(rec['bytes']),local+size)
            if right<=left:continue
            need(rec['next_record']!='FIXUPP' and not any(cover[left-local:right-local]),
                 'original lookup contains overlapping or fixed-up native source record')
            need(rec['bytes'][left-rec['offset']:right-rec['offset']]==body[left-local:right-local],
                 'ordinary OMF LEDATA source bytes differ from complete Master initializer')
            cover[left-local:right-local]=b'\x01'*(right-left)
            evidence.append({'record_offset':rec['record_offset'],'segment_local_offset':rec['offset'],
                             'record_size':len(rec['bytes']),'scope_offset':left-local,
                             'scope_size':right-left,'record_sha256':sha(rec['bytes'])})
        need(all(cover) and evidence, 'original Master table has missing native OMF DATA source writes')
        rows.append({'member':name,'artifact':'th05-main','start':start,'end':start+size,'size':size,
                     'calibration_start':cal_start,'author_member':archive_name,
                     'author_source_sha256':sha(original_source),
                     'actual_source_sha256':sha(native_source),
                     'DATA_sha256':sha(body),'ordered_original_MZ':[],
                     'ordered_calibration_MZ':[],'real_OMF_DATA_source':evidence,
                     'authored_credit':0})
    return {'schema_version':1,'kind':'complete-original-Master-literal-DATA',
            'source_count':len(rows),'DATA_bytes':sum(x['size'] for x in rows),
            'scope_rows':rows,'original_author_archive_sha256':meta['inputs']['inner_archive']['sha256'],
            'original_target_sha256':original_art['sha256'],
            'original_payload_sha256':sha(original.program_image),
            'native_OMF_sha256':sha(obj),'native_MAP_sha256':sha(map_bytes),
            'BGM_include_sha256':sha(archive['BGM.INC']),
            'verifier_sha256':digest_file(ROOT/'scripts/review_main_master_literal_tables.py'),
            'authored_credit':0}


def validate(meta: dict, decision_required=True):
    parent=json.loads(PARENT.read_text())
    need(meta.get('schema_version')==1 and meta.get('kind')=='complete-original-Master-literal-DATA' and
         meta.get('source_count')==len(TABLES) and meta.get('DATA_bytes')==224 and
         meta.get('original_author_archive_sha256')==parent['inputs']['inner_archive']['sha256'] and
         meta.get('original_target_sha256')==parent['inputs']['target']['sha256'] and
         meta.get('native_OMF_sha256')==parent['inputs']['calibration_object']['sha256'] and
         meta.get('native_MAP_sha256')==parent['inputs']['calibration_map']['sha256'] and
         meta.get('verifier_sha256')==digest_file(ROOT/'scripts/review_main_master_literal_tables.py') and
         meta.get('authored_credit')==0,
         'original literal Master initialized-data proof identity differs')
    rows=meta.get('scope_rows',[])
    need([(x.get('member'),x.get('start'),x.get('size'),x.get('author_member')) for x in rows] ==
         [(n,s,z,ar) for n,ar,src,s,c,z,p in TABLES],
         'original complete Master literal table boundaries/author members differ')
    for (name,ar,src,st,ca,z,pub),r in zip(TABLES,rows):
        need(r['artifact']=='th05-main' and r['end']==st+z and
             r['calibration_start']==ca and r['authored_credit']==0 and
             r['ordered_original_MZ']==r['ordered_calibration_MZ']==[],
             'literal Master DATA source claim has relocation or widened boundary')
        for key in ('author_source_sha256','actual_source_sha256','DATA_sha256'):
            need(isinstance(r.get(key),str) and re.fullmatch('[0-9a-f]{64}',r[key]),
                 'original source or DATA hash missing')
        spans=r['real_OMF_DATA_source']
        need(isinstance(spans,list) and len(spans)==1 and spans[0].get('scope_offset')==0 and
             spans[0].get('scope_size')==z and spans[0].get('record_size',0)>=z and
             spans[0].get('segment_local_offset',-1)<=ca-0x20a70 and
             re.fullmatch('[0-9a-f]{64}',spans[0].get('record_sha256','')),
             'original DATA TASM OMF source write is partial or absent')
    for key in ('original_payload_sha256','BGM_include_sha256'):
        need(isinstance(meta.get(key),str) and re.fullmatch('[0-9a-f]{64}',meta[key]),
             'original source inclusion identity missing')
    if decision_required:
        d=json.loads(DECISION.read_text())
        need(d=={'schema_version':1,'decision':'ADOPT_ONLY_FOUR_MASTER_LITERAL_DATA_TABLES',
                 'evidence_sha256':digest_file(PROOF),
                 'scopes':[r['member'] for r in rows], 'DATA_bytes':224,
                 'CODE_bytes':0,'authored_credit':0},
             'independent Master literal DATA adoption decision missing/stale')


def reviewed_claims(root,*,view,verify_targets=False):
    if not DECISION.exists():return [],None
    need(root.resolve()==ROOT.resolve(),'wrong review checkout')
    j=json.loads(PROOF.read_text());validate(j)
    need(view['sha256']==j['original_payload_sha256'], 'native MAIN DATA identity changed')
    if verify_targets:need(replay()==j,'real original Master initialized DATA differs')
    claims=[{'start':r['start'],'end':r['end'],'kind':'verified-vendor-initialized-data',
             'content_kind':'library-initialized-data','instruction_bytes':0,
             'library':'Master 0.23','member':r['member']} for r in j['scope_rows']]
    return claims,digest_file(DECISION)


def main():
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True)
    for flag in ('write','check','structural-check'):g.add_argument('--'+flag,action='store_true')
    args=p.parse_args()
    if args.write:
        need(not PROOF.exists() and not DECISION.exists(), 'original Master proof already exists')
        j=replay();PROOF.write_text(json.dumps(j,indent=2)+'\n')
        decision={'schema_version':1,'decision':'ADOPT_ONLY_FOUR_MASTER_LITERAL_DATA_TABLES',
                  'evidence_sha256':digest_file(PROOF),
                  'scopes':[r['member'] for r in j['scope_rows']],
                  'DATA_bytes':224,'CODE_bytes':0,'authored_credit':0}
        DECISION.write_text(json.dumps(decision,indent=2)+'\n')
        validate(j);print('PASS four source-linked original Master literal tables',j['DATA_bytes'])
    else:
        j=json.loads(PROOF.read_text());validate(j)
        if args.check:need(replay()==j, 'original full Master literal DATA OMF/MZ changed')
        print('PASS four source-backed complete Master initialized DATA tables')

if __name__=='__main__':main()
