#!/usr/bin/env python3
"""Source-backed SIN8 initialized vendor DATA PROPOSAL; never adopts bytes."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import struct
import review_master as master
import review_master_additions as context
import review_vendor_context as decoded
from lib.omf import describe_omf,parse_omf
from lib.pc98 import parse_mz
from lib.unit_context import UnitContext,load_unit_target

ROOT=Path(__file__).resolve().parents[1]
PROOF='config/master_sin8_ownership.json'
CONTEXT_PROOF='config/master_vendor_additions.json'
CONTEXT_SHA256='67aef0634d32c582994685f66633c4529ddf2db12ccfce8afff562dac48f5ee9'
FROZEN_EVIDENCE_SHA256='4ba80fb80108989a1f985495eb0ba3dca51ee5133976194b905f95a5cadee4aa'
SOURCES=list(dict.fromkeys(['scripts/review_master_sin8.py',*context.SOURCES]))
PINS={
 'main':dict(original_ds=0x209D,original_offset=0x41C,cal_ds=0x209E,cal_offset=0x42E,con_offset=0x90,con_size=0x1F40,module='th05_main.asm'),
 'op':dict(original_ds=0xEFE,original_offset=0x590,cal_ds=0xEFE,cal_offset=0x590,con_offset=0x4D2,con_size=0x4D0,module='th05_op.asm'),
 'maine':dict(original_ds=0x1011,original_offset=0x27A,cal_ds=0x1010,cal_offset=0x27A,con_offset=0xBC,con_size=0x5C4,module='th05_maine_master.asm'),
}
need,sha=master.need,master.sha


def initializer(raw,encoding):
    lines=master.decoded(raw,encoding).split('\n')
    starts=[i for i,s in enumerate(lines)if re.fullmatch(r'\s*public\s+_SinTable8,\s*_CosTable8\s*',s)]
    need(len(starts)==1,'unique whole SIN8 declaration required')
    a=starts[0];words=[];aliases={};last=None
    for i in range(a+1,len(lines)):
        if not lines[i].strip():continue
        match=re.fullmatch(r'\s*(?:(\w+)\s+)?dw\s+([-0-9, \t]+)',lines[i])
        if not match:break
        if match[1]:
            need(match[1]not in aliases,'duplicate SIN8 alias');aliases[match[1]]=len(words)*2
        values=[s.strip()for s in match[2].split(',')]
        need(all(re.fullmatch('-?[0-9]+',s)for s in values),'nonliteral signed word')
        words.extend(map(int,values));last=i
    need(len(words)==320 and aliases=={'_SinTable8':0,'_CosTable8':128} and
         all(-32768<=v<=32767 for v in words),'complete320signedwords/aliases required')
    block='\n'.join(lines[a:last+1])
    return dict(lines=[a+1,last+1],block=block,content=struct.pack('<320h',*words))


def map_data(raw,pin):
    contributions=[];publics={'Name':[],'Value':[]};sections=[];active=None
    for line in raw.decode('cp437').splitlines():
        heading=re.fullmatch(r'\s*Address\s+Publics by (Name|Value)\s*',line)
        if heading:active=heading[1];sections.append(active)
        match=re.fullmatch(r'\s*([0-9A-F]{4}):([0-9A-F]{4})\s+([0-9A-F]{4})\s+C=DATA\s+S=_DATA\s+G=DGROUP\s+M='+re.escape(pin['module'])+r'\s+ACBP=48\s*',line,re.I)
        if match:contributions.append(dict(frame=int(match[1],16)*16,offset=int(match[2],16),size=int(match[3],16)))
        match=re.fullmatch(r'\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:idle\s+)?(_SinTable8|_CosTable8)\s*',line)
        if match:
            need(active in publics,'alias outside MAP public section')
            publics[active].append(dict(name=match[3],frame=int(match[1],16)*16,offset=int(match[2],16)))
    con=dict(frame=pin['cal_ds']*16,offset=pin['con_offset'],size=pin['con_size'])
    expected=[dict(name=name,frame=pin['cal_ds']*16,offset=pin['cal_offset']+delta)
              for name,delta in [('_SinTable8',0),('_CosTable8',128)]]
    need(contributions==[con] and sections==['Name','Value'],'actual DATA contribution/sections differ')
    need(all(sorted(rows,key=lambda r:r['name'])==sorted(expected,key=lambda r:r['name'])for rows in publics.values()),
         'literal MAP aliases/frame/duplicates differ')
    return con,expected


def iterated_length(raw,cursor,limit,depth=0):
    need(depth<32 and cursor+4<=len(raw),'iterated DATA bounds/depth')
    repeat,children=struct.unpack_from('<HH',raw,cursor);cursor+=4;size=0
    if children:
        for _ in range(children):
            n,cursor=iterated_length(raw,cursor,limit,depth+1);size+=n
            need(size<=limit,'iterated DATA expansion bound')
    else:
        need(cursor<len(raw),'iterated DATA leaf missing');size=raw[cursor];cursor+=1
        need(cursor+size<=len(raw),'iterated DATA leaf bounds');cursor+=size
    need(size*repeat<=limit,'iterated DATA expansion bound')
    return size*repeat,cursor


def object_data(raw,con,start,size=640):
    names=[''];segs=[None];pubs=[];blocks=[];fixups=[];iterated=[];last=None
    allowed={'THEADR','COMENT','LNAMES','SEGDEF','GRPDEF','PUBDEF','EXTDEF','LEDATA','FIXUPP','LIDATA','MODEND'}
    records=parse_omf(raw);need(not {r.name for r in records}-allowed,'unsupported actual OMF transformation')
    for rec in records:
        b=rec.data
        if rec.name=='LNAMES':
            c=0
            while c<len(b):
                n=b[c];need(c+1+n<=len(b),'LNAMES bounds');names.append(b[c+1:c+1+n].decode('ascii'));c+=1+n
        elif rec.name=='SEGDEF':
            need(len(b)>=6 and b[0]&0xE0 and not b[0]&2,'SEGDEF attributes')
            ni,c=master.idx(b,3);ci,c=master.idx(b,c);oi,c=master.idx(b,c)
            need(c==len(b) and 0<ni<len(names) and 0<ci<len(names) and 0<=oi<len(names),'SEGDEF indices')
            segs.append(dict(name=names[ni],class_name=names[ci],size=int.from_bytes(b[1:3],'little'),acbp=b[0]))
        elif rec.name=='PUBDEF':
            gi,c=master.idx(b,0);si,c=master.idx(b,c)
            if si==0:c+=2
            while c<len(b):
                n=b[c];c+=1;need(c+n+2<=len(b),'PUBDEF bounds');name=b[c:c+n].decode('ascii');c+=n
                off=int.from_bytes(b[c:c+2],'little');c+=2;_,c=master.idx(b,c);pubs.append((name,si,off))
        elif rec.name in('LEDATA','LIDATA'):
            si,c=master.idx(b,0);need(0<si<len(segs) and c+2<=len(b),'DATA record bounds')
            off=int.from_bytes(b[c:c+2],'little');c+=2
            if rec.name=='LEDATA':
                need(off+len(b[c:])<=segs[si]['size'],'LEDATA outside SEGDEF')
                last=(si,off,b[c:]);blocks.append((*last,rec.offset))
            else:
                expanded=0
                while c<len(b):n,c=iterated_length(b,c,segs[si]['size']);expanded+=n
                need(off+expanded<=segs[si]['size'],'iterated DATA outside SEGDEF')
                iterated.append((si,off,off+expanded));last=None
        elif rec.name=='FIXUPP':
            need(last is not None,'FIXUPP without ordinary LEDATA');c=0
            while c<len(b):
                need(c+3<=len(b),'FIXUPP truncated');loc,dat=b[c],b[c+2]
                need(loc&128 and not dat&128 and not dat&8,'threaded FIXUPP unsupported')
                site=((loc&3)<<8)|b[c+1];kind=(loc>>2)&15;fm=(dat>>4)&7;c+=3
                if fm<=2:_,c=master.idx(b,c)
                else:need(fm in(4,5),'unsupported FIXUPP frame')
                _,c=master.idx(b,c)
                if not dat&4:c+=2
                need(c<=len(b) and kind in(1,2,3) and site+{1:2,2:2,3:4}[kind]<=len(last[2]),'FIXUPP field bounds')
                fixups.append((last[0],last[1]+site,{1:2,2:2,3:4}[kind]))
    matches=[i for i,s in enumerate(segs)if s and s['name']=='_DATA' and s['class_name']=='DATA']
    need(len(matches)==1,'unique real DATA SEGDEF required');si=matches[0]
    need(segs[si]['size']==con['size'] and segs[si]['acbp']==0x48,'actual DATA SEGDEF/MAP differs')
    lo=start-con['frame']-con['offset'];hi=lo+size
    need(0<=lo<hi<=segs[si]['size'],'complete initializer outside DATA')
    aliases=[p for p in pubs if p[0]in('_SinTable8','_CosTable8')]
    need(aliases==[('_SinTable8',si,lo),('_CosTable8',si,lo+128)],'actual PUBDEF aliases differ')
    need(not [(s,a,w)for s,a,w in fixups if s==si and a<hi and a+w>lo],'intersecting/cross-boundary FIXUPP')
    need(not [(s,a,z)for s,a,z in iterated if s==si and a<hi and z>lo],'intersecting iterated DATA')
    content,cover=bytearray(size),bytearray(size);used=[]
    for s,a,body,record in blocks:
        left,right=max(a,lo),min(a+len(body),hi)
        if s!=si or left>=right:continue
        need(not any(cover[left-lo:right-lo]),'overlapping SIN8 LEDATA')
        content[left-lo:right-lo]=body[left-a:right-a];cover[left-lo:right-lo]=b'\1'*(right-left)
        used.append(dict(record_offset=record,segment_offset=a,size=len(body),sha256=sha(body),scope_offset=left-lo,scope_size=right-left))
    need(all(cover),'unwritten SIN8 LEDATA gap')
    return bytes(content),dict(SEGDEF=segs[si],PUBDEF=[dict(name=n,segment=s,offset=o)for n,s,o in aliases],
                              LEDATA=used,intersecting_FIXUPP_count=0,intersecting_LIDATA_count=0)


def startup_dgroup(image,segment):
    p=image.program_image
    need(p[:1]==b'\xBA' and p[0x14:0x16]==b'\x8E\xDA' and int.from_bytes(p[1:3],'little')==segment and
         any(r.linear==1 for r in image.relocations),'actual startup DS protocol/frame differs')
    return dict(segment=segment,immediate_offset=1,load_DS_offset=0x14,startup_prefix_sha256=sha(p[:0x16]))


def build_metadata(root=ROOT):
    parent_raw=(root/CONTEXT_PROOF).read_bytes();need(sha(parent_raw)==CONTEXT_SHA256,'frozen retained context proof differs')
    parent=json.loads(parent_raw);context.review_inputs(parent,root=root)
    baseline=json.loads((root/context.BASE_PROOF).read_text())
    archive=master.stored_lzh(master.pinned(root,baseline['inputs']['inner_archive']))
    primary_path=Path(baseline['upstream_source_root'])/'SIN8.ASM';primary=(root/primary_path).read_bytes()
    need(primary==archive['SIN8.ASM'],'primary archive extraction differs');before=initializer(primary,'cp932');scopes=[]
    for name,pin in PINS.items():
        main=name=='main';inputs=baseline['inputs']if main else parent['table_contexts'][name]['inputs']
        prefix=baseline['calibration_source_root']if main else parent['table_contexts'][name]['source_root']
        exe=master.pinned(root,inputs['calibration_exe']);mp=master.pinned(root,inputs['calibration_map']);obj=master.pinned(root,inputs['calibration_object'])
        ctx=UnitContext(root,name);cfg=ctx.config();artifact,target,view=load_unit_target(ctx,cfg)
        if main:need(artifact['sha256']==baseline['inputs']['target']['sha256'] and sha(target.program_image)==baseline['target_payload_sha256'],'MAIN original identity differs')
        else:decoded.validate_target_context(ctx,cfg,artifact,target,view)
        cal=parse_mz(exe);need(cal.valid,'invalid real retained MZ')
        candidate=Path(prefix)/'libs/master.lib/sin8[data].asm';after=initializer((root/candidate).read_bytes(),'utf8')
        need(before['block']==after['block'],'literal complete signed-word initializer differs')
        con,aliases=map_data(mp,pin);original=pin['original_ds']*16+pin['original_offset'];linked=pin['cal_ds']*16+pin['cal_offset']
        body,omf=object_data(obj,con,linked);need(body==before['content']==target.program_image[original:original+640]==cal.program_image[linked:linked+640],'complete primary/OMF/original/calibration raw differs')
        for image,a in((target,original),(cal,linked)):
            context.no_relocations(image,a,640);need(image.program_image.find(body)==a and image.program_image.find(body,a+1)<0,'nonunique complete table')
        paths=describe_omf(obj)['dependency_paths'];need('libs/master.lib/sin8[data].asm'in [p.replace('\\','/')for p in paths],'SIN8 source absent from actual dependency closure')
        scopes.append(dict(id=name+'-sin8',artifact=artifact['id'],claim_kind='verified-vendor-initialized-data',content_kind='library-initialized-data',
            size=640,word_count=320,original_start=original,original_end=original+640,calibration_start=linked,calibration_end=linked+640,
            original_aliases=[dict(name=n,frame=pin['original_ds']*16,offset=pin['original_offset']+d)for n,d in[('_SinTable8',0),('_CosTable8',128)]],
            original_alias_basis='Complete primary table and unique original occurrence relative to actual startup DS; no original MAP claimed.',
            actual_MAP_aliases=aliases,original_startup_DS=startup_dgroup(target,pin['original_ds']),calibration_startup_DS=startup_dgroup(cal,pin['cal_ds']),
            actual_DATA_contribution=con,actual_OMF_scope=omf,source=context.identity(root,candidate),source_lines=after['lines'],
            original_packed_sha256=artifact['sha256'],target_payload_sha256=sha(target.program_image),target_view=view,
            actual_inputs={r:inputs[r]for r in('calibration_exe','calibration_map','calibration_object')},
            complete_initializer_sha256=sha(body),original_ordered_fixups=[],calibration_ordered_fixups=[],actual_retained_links=1))
    meta=dict(schema_version=1,kind='source-backed-master-initialized-data-proposal',decision='PROPOSAL',authored_credit=0,authored_denominator=None,
        ownership_decision=None,compiler_invocations=0,denominator_changed=False,full_bytes=1920,instruction_bytes=0,
        inherited_context_proofs=[context.identity(root,CONTEXT_PROOF),context.identity(root,context.BASE_PROOF)],
        primary_source=context.identity(root,primary_path),primary_lines=before['lines'],primary_source_block_sha256=sha(before['block'].encode()),
        primary_archives={r:baseline['inputs'][r]for r in('outer_archive','inner_archive')},literal_extracted_members=653,
        normalization=['Strict CP932 versus UTF8 decoding','CRLF/CR toLF only'],scopes=scopes,
        proposed_claim_kind='verified-vendor-initialized-data',other_scopes_policy='unknown',uncovered_gaps_policy='unknown',
        limits=['One retained link per context, no new compiler or authored recovery claim.','All653 primary archive members and complete per-context source closures are reread through immutable parent context review.',
                'Original and actual calibration positions/frames differ; no byte, relocation or frame normalization.','Sin/Cos share320words physically; not two256word allocations.',
                'No binary archive/member ownership assertion or broad mixed-object claim. No ownership hook or active decision.'],
        reviewer_sources=[context.identity(root,p)for p in SOURCES])
    meta['evidence_digest']=context.evidence_digest(meta);return meta


def validate_metadata(meta,*,root=ROOT):
    need(type(meta.get('schema_version'))is int and meta['schema_version']==1 and meta.get('kind')=='source-backed-master-initialized-data-proposal','SIN8 schema')
    need(meta.get('decision')=='PROPOSAL' and meta.get('ownership_decision')is None and type(meta.get('authored_credit'))is int and meta['authored_credit']==0 and
         meta.get('authored_denominator','missing')is None and type(meta.get('compiler_invocations'))is int and meta['compiler_invocations']==0 and meta.get('denominator_changed')is False,'proposal cannot adopt/grant credit')
    need(meta.get('proposed_claim_kind')=='verified-vendor-initialized-data' and meta.get('full_bytes')==1920 and meta.get('instruction_bytes')==0,'DATA only accounting')
    parents=meta.get('inherited_context_proofs',[]);need(len(parents)==2 and parents[0]['sha256']==CONTEXT_SHA256 and parents[1]['sha256']==context.BASE_SHA256,'retained context identity differs')
    for p in parents:master.pinned(root,p)
    expected=[(n+'-sin8','th05-'+n,p['original_ds']*16+p['original_offset'],p['cal_ds']*16+p['cal_offset'])for n,p in PINS.items()]
    need([(s['id'],s['artifact'],s['original_start'],s['calibration_start'])for s in meta.get('scopes',[])]==expected,'three literal original/calibration positions required')
    need([r['file']for r in meta.get('reviewer_sources',[])]==SOURCES,'complete reviewer closure required')
    for row in meta['reviewer_sources']:master.pinned(root,row)
    need(context.evidence_digest(meta)==meta.get('evidence_digest') and (not FROZEN_EVIDENCE_SHA256 or meta['evidence_digest']==FROZEN_EVIDENCE_SHA256),'frozen SIN8 evidence differs')
    def public(v):
        if isinstance(v,dict):
            need(not set(v)&{'raw','data','source_text','text','instructions','content','block','program_records','bytes_hex'},'private source/bytes in public metadata')
            for x in v.values():public(x)
        elif isinstance(v,list):
            for x in v:public(x)
        elif isinstance(v,str):need(not v.startswith(('/home/','/mnt/','C:\\','D:\\')),'private absolute path')
    public(meta)
    return dict(kind='public-SIN8-structure-only',scopes=3,full_bytes=1920,instruction_bytes=0,byte_proof_replayed=False,decision='PROPOSAL',authored_credit=0,authored_denominator=None)


def review_inputs(meta,*,root=ROOT):
    validate_metadata(meta,root=root);need(build_metadata(root)==meta,'actual SIN8 source/OMF/original inputs differ')
    return dict(kind='native-SIN8-initialized-data-review',scopes=3,full_bytes=1920,instruction_bytes=0,byte_proof_replayed=True,decision='PROPOSAL',authored_credit=0,compiler_invocations=0,authored_denominator=None)


def main():
    parser=argparse.ArgumentParser(description=__doc__);modes=parser.add_mutually_exclusive_group(required=True)
    for mode in('check','write','structural-check'):modes.add_argument('--'+mode,action='store_true')
    args=parser.parse_args();path=ROOT/PROOF
    if args.write:meta=build_metadata();validate_metadata(meta);path.write_text(json.dumps(meta,indent=2)+'\n');result=dict(kind='SIN8-PROPOSAL-written',scopes=3,full_bytes=1920,authored_credit=0)
    else:meta=json.loads(path.read_text());result=validate_metadata(meta)if args.structural_check else review_inputs(meta)
    print(json.dumps(result,indent=2));return 0


if __name__=='__main__':
    import os,resource
    resource.setrlimit(resource.RLIMIT_AS,(384*1024*1024,)*2);os.nice(15);os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    raise SystemExit(main())
