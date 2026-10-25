#!/usr/bin/env python3
"""Additive, source-backed Master ownership PROPOSAL; never adopts members.

Public --structural-check needs no game or toolchain cache. Native --check
rereads primary archives, actual retained objects/links and original targets.
This is vendor ownership evidence with zero authored credit and no new build.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct

import review_master as base
import review_vendor as vendor
import review_vendor_context as contexts
from lib.omf import describe_omf, parse_omf
from lib.pc98 import parse_mz
from lib.unit_context import UnitContext, load_unit_target

ROOT = Path(__file__).resolve().parents[1]
PROOF = 'config/master_vendor_additions.json'
BASE_PROOF = 'config/master_vendor_ownership.json'
BASE_SHA256 = '8b5e9b31ce345df277a31348d49aec9197e4c5c390eec0b9f812516c8287010a'
LIB_SHA256 = '6be41dbcfcf4504977165ccc44443525a29a01f85a1580e6ad0c620bf802faf6'
FROZEN_EVIDENCE_SHA256 = '41dfd7758455bd7708b3e82c332c6099880429fb88a85ec6be4ad81363bfa6ae'  # Filled after bounded scope review; excludes reviewer source hashes.
SOURCES = list(dict.fromkeys(['scripts/review_master_additions.py','scripts/review_master.py',
                            *contexts.REVIEWER_SOURCES]))
MAIN = [('main-pfgetc','PFGETC',0x227C,0x228C),
        ('main-assignall','ASSIGNALL',0x2442,0x2448),
        ('main-sound-joy','SOUND_JOY',0x3668,0x3679),
        ('main-sajout','SAJOUT',0x3686,0x368F),
        ('main-str-ieq','STR_IEQ',0x45B0,0x45E8)]
TABLES = {
 'op': dict(start=0x1C88,end=0x2088,module='th05_op.asm',object='op',module_size=0x38A6,
            object_sha256='b32328d03d8eb942bcdb55dcd0d816051db46b117de0a7817f4bd558f08acc92'),
 'maine': dict(start=0x1E22,end=0x2222,module='th05_maine_master.asm',object='mainem',module_size=0x3A6E,
               object_sha256='99de745399982cb12f50b11ba3f9570b6cbf96ca0f5805f1af71ab4932922f00'),
}


def need(condition,message):
    if not condition: raise ValueError(message)


def sha(raw): return hashlib.sha256(raw).hexdigest()


def identity(root,path):
    path=base.relative(str(path)); full=root/path
    need(full.is_file() and not full.is_symlink() and full.resolve().is_relative_to(root.resolve()),
         'missing/unsafe input: '+str(path))
    raw=full.read_bytes()
    return dict(file=str(path),size=len(raw),sha256=sha(raw))


def evidence_digest(meta):
    return sha(json.dumps({k:v for k,v in meta.items() if k not in ('evidence_digest','reviewer_sources')},
                          sort_keys=True,separators=(',',':')).encode())


def integer(value,low,high):
    need(type(value) is int and low<=value<=high,'invalid evidence integer')
    return value


def initializer(raw,encoding):
    """A complete original symbolic initializer, not a target-derived byte table."""
    lines=base.decoded(raw,encoding).split('\n')
    starts=[i for i,s in enumerate(lines)if re.fullmatch(r'\s*public\s+RotTbl\s*',s)]
    need(len(starts)==1,'unique RotTbl initializer declaration required')
    a=starts[0];last=None;values=[]
    for i in range(a+1,len(lines)):
        if not lines[i].strip():continue
        match=re.fullmatch(r'\s*(?:RotTbl\s+)?dd\s+([0-9A-Fa-fhH, \t]+)',lines[i])
        if not match:break
        tokens=[s.strip() for s in match[1].split(',')]
        need(all(re.fullmatch('[0-9A-Fa-f]+h',s) for s in tokens),'unsupported initializer expression')
        values.extend(int(s[:-1],16) for s in tokens);last=i
    need(len(values)==256 and all(0<=v<=0xFFFFFFFF for v in values),'whole256-dword initializer required')
    block='\n'.join(lines[a:last+1])
    return dict(lines=[a+1,last+1],block=block,source_block_sha256=sha(block.encode()),
                content=b''.join(struct.pack('<I',v)for v in values))


def literal_initializer(original,candidate):
    before,after=initializer(original,'cp932'),initializer(candidate,'utf8')
    need(before['block']==after['block'],'complete literal symbolic initializer source differs')
    need(before['content']==after['content'],'symbolic initializer values differ')
    return before,after


def unique_source_block(originals,candidate,name):
    local=[p for p in base.source_blocks(candidate,'utf8') if p['name'].casefold()==name.casefold()]
    matches=[]
    for filename,raw in originals.items():
        if not filename.endswith('.ASM'):continue
        for original in base.source_blocks(raw,'cp932'):
            if original['name'].casefold()!=name.casefold():continue
            for after in local:
                if original['text']==after['text']:matches.append((filename,original,after))
    need(len(matches)==1,'complete primary source procedure absent/ambiguous/different')
    return matches[0]


def map_context(raw,module,module_size,start,size):
    contributions=[];publics={'Name':[],'Value':[]};sections=[];section=None
    for line in raw.decode('cp437').splitlines():
        heading=re.fullmatch(r'\s*Address\s+Publics by (Name|Value)\s*',line)
        if heading:section=heading[1];sections.append(section)
        match=re.fullmatch(r'\s*([0-9A-F]{4}):([0-9A-F]{4})\s+([0-9A-F]{4})\s+C=CODE\s+S=_TEXT\s+G=\(none\)\s+M='+re.escape(module)+r'\s+ACBP=48\s*',line,re.I)
        if match:
            frame,off=int(match[1],16)*16,int(match[2],16)
            contributions.append(dict(frame=frame,offset=off,start=frame+off,size=int(match[3],16),
                                      module=module,segment='_TEXT',class_name='CODE',acbp=0x48))
        match=re.fullmatch(r'\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:idle\s+)?RotTbl\s*',line,re.I)
        if match:
            need(section in publics,'public outside actual MAP public section')
            publics[section].append(dict(frame=int(match[1],16)*16,offset=int(match[2],16)))
    expected=dict(frame=0,offset=0x272,start=0x272,size=module_size,module=module,
                  segment='_TEXT',class_name='CODE',acbp=0x48)
    need(contributions==[expected],'actual complete monolithic MAP contribution differs/duplicates')
    need(sections==['Name','Value'] and
         all(rows==[dict(frame=0,offset=start)]for rows in publics.values()) and
         0x272<=start<start+size<=0x272+module_size,
         'actual literal MAP RotTbl frame:offset differs/duplicates')
    return expected,publics['Name'][0]


def object_scope(raw,con,start,size):
    """Actual retained OMF; no synthetic member, MZ or inferred MAP contribution."""
    names=[''];segs=[None];pubs=[];blocks=[];fixups=[];last=None
    allowed={'THEADR','COMENT','LNAMES','SEGDEF','GRPDEF','PUBDEF','EXTDEF','LEDATA','FIXUPP','LIDATA','MODEND'}
    records=parse_omf(raw)
    need(not {r.name for r in records}-allowed,'unsupported actual OMF record')
    for rec in records:
        b=rec.data
        if rec.name=='LNAMES':
            c=0
            while c<len(b):
                n=b[c];need(c+1+n<=len(b),'LNAMES bounds')
                names.append(b[c+1:c+1+n].decode('ascii'));c+=1+n
        elif rec.name=='SEGDEF':
            need(len(b)>=6 and b[0]&0xE0 and not b[0]&2,'unsupported SEGDEF')
            ni,c=base.idx(b,3);ci,c=base.idx(b,c);oi,c=base.idx(b,c)
            need(c==len(b) and 0<ni<len(names) and 0<ci<len(names) and 0<=oi<len(names),'SEGDEF indices')
            segs.append(dict(name=names[ni],class_name=names[ci],size=int.from_bytes(b[1:3],'little'),acbp=b[0]))
        elif rec.name=='PUBDEF':
            gi,c=base.idx(b,0);si,c=base.idx(b,c)
            if si==0:c+=2
            while c<len(b):
                n=b[c];c+=1;need(c+n+2<=len(b),'PUBDEF bounds')
                name=b[c:c+n].decode('ascii');c+=n;off=int.from_bytes(b[c:c+2],'little');c+=2
                _,c=base.idx(b,c);pubs.append((name,si,off))
        elif rec.name=='LEDATA':
            si,c=base.idx(b,0);need(0<si<len(segs) and c+2<=len(b),'LEDATA segment/offset')
            off=int.from_bytes(b[c:c+2],'little');content=b[c+2:]
            need(off+len(content)<=segs[si]['size'],'LEDATA outside SEGDEF')
            last=(si,off,content);blocks.append((si,off,content,rec.offset))
        elif rec.name=='LIDATA':
            si,_=base.idx(b,0)
            need(0<si<len(segs) and segs[si]['name']!='_TEXT','iterated CODE data unsupported')
            last=None
        elif rec.name=='FIXUPP':
            need(last is not None,'FIXUPP without LEDATA');c=0
            while c<len(b):
                need(c+3<=len(b),'FIXUPP truncation');loc,dat=b[c],b[c+2]
                need(loc&128 and not dat&128 and not dat&8,'threaded FIXUPP unsupported')
                site=((loc&3)<<8)|b[c+1];kind=(loc>>2)&15;fm=(dat>>4)&7;c+=3
                if fm<=2:_,c=base.idx(b,c)
                else:need(fm in(4,5),'unsupported frame method')
                _,c=base.idx(b,c)
                if not dat&4:c+=2
                need(c<=len(b) and kind in(1,2,3) and site+{1:2,2:2,3:4}[kind]<=len(last[2]),'FIXUPP field bounds')
                fixups.append((last[0],last[1]+site,{1:2,2:2,3:4}[kind]))
    indices=[i for i,s in enumerate(segs)if s and s['name']=='_TEXT' and s['class_name']=='CODE']
    need(len(indices)==1,'unique actual _TEXT required');si=indices[0]
    need(segs[si]['size']==con['size'] and segs[si]['acbp']==con['acbp'],'actual SEGDEF/MAP differs')
    lo,hi=start-con['start'],start-con['start']+size
    need(0<=lo<hi<=segs[si]['size'],'object scope bounds')
    need([p for p in pubs if p[0]=='RotTbl']==[('RotTbl',si,lo)],'actual unique PUBDEF disagrees with MAP')
    need(not [(s,a,w)for s,a,w in fixups if s==si and a<hi and a+w>lo],
         'FIXUPP intersects complete initializer or crosses boundary')
    content,coverage=bytearray(size),bytearray(size);used=[]
    for s,a,body,record_offset in blocks:
        if s!=si:continue
        left,right=max(a,lo),min(a+len(body),hi)
        if left>=right:continue
        need(not any(coverage[left-lo:right-lo]),'overlapping complete initializer LEDATA')
        content[left-lo:right-lo]=body[left-a:right-a];coverage[left-lo:right-lo]=b'\1'*(right-left)
        used.append(dict(record_offset=record_offset,segment_offset=a,size=len(body),sha256=sha(body),
                         scope_offset=left-lo,scope_size=right-left))
    need(all(coverage),'unwritten complete initializer LEDATA gap')
    return bytes(content),dict(SEGDEF=segs[si],PUBDEF=dict(name='RotTbl',segment=si,offset=lo),
                              CODE_LEDATA=used,intersecting_FIXUPP_count=0)


def no_relocations(image,start,size):
    rows=[r.linear-start for r in image.relocations if start-1<=r.linear<start+size]
    need(rows==[],'ordered target relocations intersect or cross complete scope')
    return rows


def source_closure(root,source_root,objraw):
    description=describe_omf(objraw)
    names=list(dict.fromkeys(path.replace('\\','/')for path in description['dependency_paths']))
    need(names and all(not Path(name).is_absolute() and '..' not in Path(name).parts for name in names),
         'unsafe/empty actual OMF source closure')
    return [dict(name=name,**identity(root,Path(source_root)/name))for name in names]


def build_metadata(root=ROOT):
    baseline_raw=base.pinned(root,dict(file=BASE_PROOF,size=(root/BASE_PROOF).stat().st_size,sha256=BASE_SHA256))
    baseline=json.loads(baseline_raw)
    base_result=base.review_inputs(baseline,root=root)  # All653 archive files, actual395 source closure, listing, macros, old extents.
    upstream=base.stored_lzh(base.pinned(root,baseline['inputs']['inner_archive']))
    originals={name:raw for name,raw in upstream.items()if name.endswith('.ASM')}
    raw_object=base.pinned(root,baseline['inputs']['saved_object']);obj=base.object_text(raw_object)
    original=parse_mz(base.pinned(root,baseline['inputs']['target']))
    linked=parse_mz(base.pinned(root,baseline['inputs']['calibration_exe']))
    listing=base.listing_procedures(base.pinned(root,baseline['inputs']['listing']))
    scopes=[]
    for id,name,a,z in MAIN:
        actual=[p for p in listing if p['name'].casefold()==name.casefold() and p['local_start']+0x272==a]
        need(len(actual)==1 and actual[0]['local_end']+0x272==z and not actual[0]['inline_data'],'complete active procedure boundary differs')
        proc=actual[0];filename=proc['source']
        source_path=Path(baseline['candidate_source_root'])/filename
        source_raw=(root/source_path).read_bytes()
        need(source_raw==(root/Path(baseline['calibration_source_root'])/filename).read_bytes(),'candidate/cal source differs')
        upname,before,after=unique_source_block(originals,source_raw,name)
        rebuilt,actions=base.linked_object_procedure(obj,a,z-a)
        pads=[dict(start=p['local_start']+0x272,size=1,value=0x90,listing_line=p['listing_line'])for p in proc['padding']]
        row=dict(id=id,artifact='th05-main',content_kind='library-instructions',name=name,start=a,end=z,size=z-a,
                 instruction_bytes=z-a-len(pads),library_padding_bytes=len(pads),padding=pads,inline_data=False,
                 distance=proc['distance'],start_listing_line=proc['start_listing_line'],end_listing_line=proc['end_listing_line'],
                 candidate_file=filename,candidate_source=identity(root,source_path),candidate_lines=[after['start_line'],after['end_line']],
                 upstream_file=upname,upstream_source=identity(root,Path(baseline['upstream_source_root'])/upname),
                 upstream_lines=[before['start_line'],before['end_line']],source_block_sha256=sha(before['text'].encode()),
                 linked_sha256=sha(rebuilt),ordered_mz_fixups=[],object_link_actions=actions)
        base.verify_raw_procedure(row,original,linked,obj)
        scopes.append(row)
    lib_path=Path('_reference/ReC98/bin/masters.lib');libraw=(root/lib_path).read_bytes()
    need(sha(libraw)==LIB_SHA256,'binary library corroboration identity drift')
    primary_path=Path(baseline['upstream_source_root'])/'ROTTBL.ASM';primary=(root/primary_path).read_bytes()
    need(primary==upstream['ROTTBL.ASM'],'original table archive extraction differs')
    table_contexts={}
    for name,pin in TABLES.items():
        ctx=UnitContext(root,name);cfg=ctx.config();artifact,target,proof=load_unit_target(ctx,cfg)
        contexts.validate_target_context(ctx,cfg,artifact,target,proof)
        prefix=Path(f'.analysis/builds/{name}-calibration-a/source')
        exe=prefix/f'bin/th05/{name}.exe';mp=prefix/f'obj/th05/{name}.map';op=prefix/f'obj/th05/{pin["object"]}.obj'
        inputs={role:identity(root,path)for role,path in [('calibration_exe',exe),('calibration_map',mp),('calibration_object',op)]}
        for role,digest in [('calibration_exe',contexts.PINS[name]['calibration_exe']),('calibration_map',contexts.PINS[name]['calibration_map']),('calibration_object',pin['object_sha256'])]:
            need(inputs[role]['sha256']==digest,'retained context input differs: '+name+'/'+role)
        objraw=(root/op).read_bytes();closure=source_closure(root,prefix,objraw)
        need(closure[0]['name']==pin['module'],'actual retained object dependency/module differs')
        candidate=prefix/'libs/master.lib/rottbl.asm';before,after=literal_initializer(primary,(root/candidate).read_bytes())
        con,pub=map_context((root/mp).read_bytes(),pin['module'],pin['module_size'],pin['start'],1024)
        body,omf=object_scope(objraw,con,pin['start'],1024)
        cal=parse_mz((root/exe).read_bytes());need(cal.valid,'invalid actual calibration MZ')
        a,z=pin['start'],pin['end']
        need(body==before['content']==target.program_image[a:z]==cal.program_image[a:z],'complete original/source/OMF/link bytes differ')
        need(target.program_image.find(body)==a and target.program_image.find(body,a+1)<0,'nonunique complete original initializer')
        no_relocations(target,a,1024);no_relocations(cal,a,1024)
        library=vendor.VendorReview(libraw,(root/mp).read_bytes(),cal,target);member=library.mods['rottbl']
        need(member['pubs']==[('RotTbl',1,0)] and not member['fixups'] and
             member['segs'][1]==dict(name='_TEXT',cl='CODE',size=1024,acbp=0x48),'corroborating original member context differs')
        need(b''.join(b['data']for b in member['blocks']if b['segment']==1)==body,'binary member corroboration differs')
        scopes.append(dict(id=name+'-rottbl',artifact=ctx.artifact,content_kind='library-code-data',name='RotTbl',
            start=a,end=z,size=1024,instruction_bytes=0,library_padding_bytes=0,padding=[],ordered_mz_fixups=[],
            symbolic_initializer=dict(dwords=256,byte_order='little',primary_lines=before['lines'],candidate_lines=after['lines'],
              source_block_sha256=before['source_block_sha256'],primary_source=identity(root,primary_path),
              candidate_source=identity(root,candidate)),linked_sha256=sha(body),actual_MAP_public=pub,
            actual_monolithic_CODE_contribution=con,actual_OMF_scope=omf,
            binary_member_corroboration=dict(member='rottbl',program_sha256=member['program_sha256'],
              SEGDEF=member['segs'][1],record_counts=dict(member['records']),
              authority='corroboration only; UNKNOWN_0x8E not interpreted or discarded; primary source and actual linked OMF are authority')))
        table_contexts[name]=dict(artifact=ctx.artifact,target_sha256=artifact['sha256'],target_payload_sha256=sha(target.program_image),
            target_view=proof,inputs=inputs,source_root=str(prefix),frozen_source_closure=closure,
            actual_retained_link_producers=1,actual_OMF_module=describe_omf(objraw)['module_name'])
    decisions=[dict(artifact='th05-'+name,decision='PROPOSAL_ONLY_LISTED_SCOPES',classification='third-party-library-code',
                    scopes=[row['id']for row in scopes if row['artifact']=='th05-'+name],authored_credit=0,
                    authored_denominator=None,other_procedures_policy='unknown',uncovered_gaps_policy='unknown')
               for name in ('main','op','maine')]
    meta=dict(schema_version=1,kind='master-source-backed-additions-proposal',decision='PROPOSAL',ownership_decision=None,
        authored_credit=0,authored_denominator=None,denominator_changed=False,compiler_invocations=0,
        scope_count=7,full_bytes=2152,instruction_bytes=103,library_padding_bytes=1,library_code_data_bytes=2048,
        existing_MAIN_proof=identity(root,BASE_PROOF),existing_MAIN_native_context=base_result,
        primary_source=dict(outer_archive=baseline['inputs']['outer_archive'],inner_archive=baseline['inputs']['inner_archive'],
          extracted_source_root=baseline['upstream_source_root'],literal_archive_members=653,
          author='Akihiko Koizuka and master.lib coauthors',version='0.23',primary_url=baseline['upstream']['primary_source'],
          authority='Independently pinned author archive; all653 literal extracted members reread by baseline context replay'),
        binary_library_corroboration=identity(root,lib_path),table_contexts=table_contexts,scopes=scopes,proposed_decisions=decisions,
        normalization=['Strict CP932 versus UTF8 decoding','CRLF/CR toLF only'],
        provenance_limitations=['Original game candidate-local-attested, not independently pristine.',
         'One retained link per context; zero fresh compiler producers, no authored source acceptance.',
         'No per-member MAP contribution is claimed: actual linked objects are mixed monolithic game/library contributions.',
         'Binary library original-distribution provenance is secondary ReC98 commitcc219ff2; independent original source archive supplies ownership authority.',
         'Source-mismatch procedures, unreviewed members, DATA/BSS and uncovered gaps remain unknown; no adoption by this proof.'],
        reviewer_sources=[identity(root,p)for p in SOURCES])
    meta['evidence_digest']=evidence_digest(meta)
    return meta


def validate_metadata(meta,*,root=ROOT):
    need(type(meta.get('schema_version'))is int and meta['schema_version']==1 and
         meta.get('kind')=='master-source-backed-additions-proposal','additions metadata schema')
    need(meta.get('decision')=='PROPOSAL' and meta.get('ownership_decision')is None and
         type(meta.get('authored_credit'))is int and meta['authored_credit']==0 and
         meta.get('authored_denominator','missing')is None and meta.get('denominator_changed')is False and
         type(meta.get('compiler_invocations'))is int and meta['compiler_invocations']==0,'proposal cannot adopt/grant credit')
    need(meta.get('existing_MAIN_proof',{}).get('sha256')==BASE_SHA256,'baseline evidence identity differs')
    base.pinned(root,meta['existing_MAIN_proof'])  # Public existing proof, not private game.
    need(meta.get('scope_count')==7 and meta.get('full_bytes')==2152 and meta.get('instruction_bytes')==103 and
         meta.get('library_padding_bytes')==1 and meta.get('library_code_data_bytes')==2048,'reviewed totals differ')
    expected=[(id,'th05-main',a,z)for id,_,a,z in MAIN]+[(name+'-rottbl','th05-'+name,p['start'],p['end'])for name,p in TABLES.items()]
    rows=meta.get('scopes',[])
    need([(r.get('id'),r.get('artifact'),r.get('start'),r.get('end'))for r in rows]==expected,'reviewed complete scopes differ')
    for row in rows:
        need(type(row.get('size'))is int and row['size']==row['end']-row['start'] and row['ordered_mz_fixups']==[],
             'complete scope size/ordered fixups differs')
        need(row['instruction_bytes']+row['library_padding_bytes']+(row['size']if row['content_kind']=='library-code-data'else 0)==row['size'],
             'CODE instructions/data/library padding accounting differs')
    need([r.get('file')for r in meta.get('reviewer_sources',[])]==SOURCES,'reviewer/loader source closure differs')
    for row in meta['reviewer_sources']:base.pinned(root,row)
    need(evidence_digest(meta)==meta.get('evidence_digest') and
         (not FROZEN_EVIDENCE_SHA256 or meta['evidence_digest']==FROZEN_EVIDENCE_SHA256),'frozen additive evidence digest differs')
    def public(value):
        if isinstance(value,dict):
            need(not set(value)&{'raw','data','source_text','text','instructions','program_records','bytes_hex','content','block'},'private source/bytes in metadata')
            for x in value.values():public(x)
        elif isinstance(value,list):
            for x in value:public(x)
        elif isinstance(value,str):need(not value.startswith(('/home/','/mnt/','C:\\','D:\\')),'private absolute path')
    public(meta)
    return dict(kind='public-master-additions-structure-only',scopes=7,full_bytes=2152,instruction_bytes=103,
                library_padding_bytes=1,library_code_data_bytes=2048,byte_proof_replayed=False,
                decision='PROPOSAL',authored_credit=0,authored_denominator=None)


def review_inputs(meta,*,root=ROOT):
    validate_metadata(meta,root=root)
    actual=build_metadata(root)
    need(actual==meta,'saved additions differ from actual primary-source/OMF/target replay')
    return dict(kind='native-source-backed-master-additions-review',scopes=7,full_bytes=2152,instruction_bytes=103,
                library_padding_bytes=1,library_code_data_bytes=2048,byte_proof_replayed=True,
                decision='PROPOSAL',authored_credit=0,compiler_invocations=0,authored_denominator=None)


def main():
    parser=argparse.ArgumentParser(description=__doc__);modes=parser.add_mutually_exclusive_group(required=True)
    for mode in ('check','write','structural-check'):modes.add_argument('--'+mode,action='store_true')
    args=parser.parse_args();path=ROOT/PROOF
    if args.write:
        meta=build_metadata();validate_metadata(meta);path.write_text(json.dumps(meta,indent=2)+'\n')
        result=dict(kind='master-additions-proposal-written',scopes=7,full_bytes=2152,decision='PROPOSAL',authored_credit=0)
    else:
        meta=json.loads(path.read_text());result=validate_metadata(meta)if args.structural_check else review_inputs(meta)
    print(json.dumps(result,indent=2));return 0


if __name__=='__main__':
    import os,resource
    resource.setrlimit(resource.RLIMIT_AS,(384*1024*1024,)*2)
    os.nice(15);os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    raise SystemExit(main())
