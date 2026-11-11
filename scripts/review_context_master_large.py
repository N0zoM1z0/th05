#!/usr/bin/env python3
"""Source-linked complete Master 0.23 procedures in original OP and MAINE.

The authentic TASM OMF _TEXT LEDATA and FIXUPP records are rebased through
the real native MAP contribution offsets. Each complete function is checked
against both original and retained calibration, with original ordered MZ
relocations; the original author archive independently proves ASM provenance.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import tomllib

from lib.omf import describe_omf, parse_omf
from lib.pc98 import digest_file, parse_mz
from lib.unit_context import UnitContext, load_unit_target
from lib.unit_oracle import relative_fixups
from review_master import idx, need, pinned, sha, source_blocks, stored_lzh
from review_master_super import source_lines as super_lines
from review_master_bgm import source_lines as bgm_lines
from review_master_grcg import symbolic_source
from review_master_io import semantic_lines
from review_master_super_helpers import near_proc_blocks, canonical as canonical_helper

ROOT=Path(__file__).resolve().parents[1]
MASTER=ROOT/'config/master_vendor_ownership.json'
PROOF=ROOT/'config/context_master_large.json'
DECISION=ROOT/'config/reviewed_context_master_large.json'
# All scopes are complete natural Master PROC/FUNC extents from the actual
# TLINK Publics-by-Value MAP, never anonymous or compiler branch fragments.
FUNCTIONS={
    'SUPER_PUT':{'op':(0x292a,240),'maine':(0x2b68,240)},
    # Native Master SUPERPUT.ASM defines five separate, private PROC/ENDP
    # drawing dispatchers; three EVEN bytes between them are NOT owned.
    'SUPERPUT_DISP1':{'op':(0x2a1a,35),'maine':(0x2c58,35)},
    'SUPERPUT_DISP2':{'op':(0x2a3e,45),'maine':(0x2c7c,45)},
    'SUPERPUT_DISP3':{'op':(0x2a6c,54),'maine':(0x2caa,54)},
    'SUPERPUT_DISP4':{'op':(0x2aa2,49),'maine':(0x2ce0,49)},
    'SUPERPUT_DISP':{'op':(0x2ad4,8),'maine':(0x2d12,8)},
    'BGM_INIT':{'op':(0x338e,420),'maine':(0x3556,420)},
    'PALETTE_SHOW':{'op':(0x19f0,266),'maine':(0x1b8a,266)},
    'HMEM_ALLOC':{'op':(0x2336,240),'maine':(0x2574,240)},
    'BGM_READ_SDATA':{'op':(0x2e52,320),'maine':(0x301a,320)},
    'GRCG_POLYGON_C':{'op':(0x0cca,536)},
    'GRCG_BOXFILL':{'maine':(0x0bce,208)},
}
ARTIFACTS=('op','maine')


def normalized_source(text,name):
    if name.startswith('SUPERPUT_DISP'):return canonical_helper(text,name)
    if name=='SUPER_PUT':return super_lines(text)
    if name in ('BGM_INIT','BGM_READ_SDATA'):return bgm_lines(text,name)
    if name in ('PALETTE_SHOW','GRCG_BOXFILL'):return symbolic_source(text)
    if name=='HMEM_ALLOC':return semantic_lines(text,name)
    if name=='GRCG_POLYGON_C':
        return [re.sub(r'\s+','',row.split(';',1)[0].lower().replace('@@',''))
                for row in text.splitlines() if row.split(';',1)[0].strip()]
    raise ValueError('unreviewed original source normalization')


def real_omf(module):
    names=[''];segs=[None];groups=[None];blocks=[];fixups=[];current=None
    for rec in parse_omf(module):
        b=rec.data
        if rec.name=='LNAMES':
            i=0
            while i<len(b):
                n=b[i];i+=1
                need(i+n<=len(b),'original Master source LNAMES truncated')
                names.append(b[i:i+n].decode('ascii'));i+=n
        elif rec.name=='SEGDEF':
            ni,i=idx(b,3);ci,i=idx(b,i);oi,i=idx(b,i)
            need(ni<len(names) and ci<len(names),'unreviewed SEGDEF name')
            segs.append((names[ni],names[ci],int.from_bytes(b[1:3],'little')))
        elif rec.name=='GRPDEF':
            gi,i=idx(b,0)
            need(gi<len(names),'unreviewed OMF group name')
            groups.append(names[gi])
        elif rec.name=='LEDATA':
            si,i=idx(b,0);pos=int.from_bytes(b[i:i+2],'little')
            need(si<len(segs) and pos+len(b[i+2:])<=segs[si][2],
                 'native Master original source LEDATA outside member')
            current=(si,pos)
            if si==1:blocks.append((pos,b[i+2:]))
        elif rec.name=='FIXUPP':
            need(current is not None,'FIXUPP without preceding original source LEDATA')
            i=0
            while i<len(b):
                need(i+3<=len(b),'original FIXUPP truncated')
                loc,info=b[i],b[i+2]
                need(loc&0x80 and not info&0x88,'threaded or unsupported OMF source FIXUPP')
                site=((loc&3)<<8)|b[i+1]
                kind=(loc>>2)&15;fm=(info>>4)&7;tm=info&3
                relative=not bool(loc&0x40);i+=3
                if fm<=2:frame,i=idx(b,i)
                else:
                    need(fm in (4,5),'unsupported native OMF source frame method')
                    frame=None
                target,i=idx(b,i)
                disp=0
                if not info&4:disp=int.from_bytes(b[i:i+2],'little');i+=2
                if current[0]==1:
                    fixups.append({'site':current[1]+site+0x272,
                                   'kind':kind,'frame_method':fm,'frame_index':frame,
                                   'target_method':tm,'target_index':target,
                                   'relative':relative,'displacement':disp})
    need(len(segs)>=9 and segs[1][0]=='_TEXT' and segs[1][1]=='CODE' and
         segs[2][0]=='_DATA' and segs[2][1]=='DATA' and
         groups[1]=='DGROUP',
         'native original Master object lacks expected _TEXT/DGROUP segments')
    return segs,blocks,fixups,groups


def native_map(artifact, native_module, segs):
    file=ROOT/f'.analysis/builds/{artifact}-calibration-a/source/obj/th05/{artifact}.map'
    raw=file.read_bytes();text=raw.decode('cp437')
    offsets={}
    for line in text.splitlines():
        m=re.match(r'\s*([0-9A-F]{4}):([0-9A-F]{4})\s+([0-9A-F]{4})\s+'
                   r'C=(\S+)\s+S=(\S+)\s+G=(\S+)\s+M=(\S+)',line,re.I)
        if not m or m[7].casefold()!=native_module.casefold():continue
        if m[5] in ('_TEXT','_DATA','_BSS'):
            need(m[5] not in offsets,'ambiguous original Master segment MAP contribution')
            offsets[m[5]]={'start':int(m[1],16)*16+int(m[2],16),
                           'size':int(m[3],16),
                           'group':m[6],'cl':m[4]}
    need(set(offsets)=={'_TEXT','_DATA','_BSS'} and
         offsets['_TEXT']['start']==0x272 and
         all(offsets[name]['size']==seg[2] for name,seg in
             ((s[0],s) for s in segs if s and s[0] in offsets)),
         'actual native MAP and original OMF segment ownership disagree')
    public={}
    for line in text.splitlines():
        m=re.match(r'\s*([0-9A-F]{4}):([0-9A-F]{4})\s+'
                   r'(?:idle\s+)?(\S+)\s*$',line)
        if m:
            point=int(m[1],16)*16+int(m[2],16)
            public.setdefault(m[3],set()).add(point)
    return raw,offsets,public


def whole_source(blocks,start,size):
    lo=start-0x272;code=bytearray(size);coverage=bytearray(size)
    for pos,data in blocks:
        a=max(lo,pos);z=min(lo+size,pos+len(data))
        if a>=z:continue
        need(not any(coverage[a-lo:z-lo]),'original Master source LEDATA overlap')
        code[a-lo:z-lo]=data[a-pos:z-pos]
        coverage[a-lo:z-lo]=b'\1'*(z-a)
    need(all(coverage),'original complete Master procedure source CODE has a hole')
    return bytes(code)


def rebind(source,fixups,start,offsets,segs,groups,cal_group,original_group):
    cal=bytearray(source);original=bytearray(source);relocations=[];actions=[];written=set()
    for f in fixups:
        site=f['site']-start
        need(0<=site<len(source)-1 and
             not any(byte in written for byte in (site,site+1)),
             'source OMF FIXUPP outside complete Master function or duplicated')
        written.update((site,site+1))
        need(not f['relative'] and f['displacement']==0,
             'unmodeled original relative source FIXUPP')
        old=int.from_bytes(source[site:site+2],'little')
        ti=f['target_index'];fm=f['frame_method'];fi=f['frame_index']
        if f['kind']==1:
            need(f['target_method']==0 and ti<len(segs) and
                 segs[ti][0] in offsets,'unsupported original OMF target segment')
            name=segs[ti][0]
            need((fm==5 or (fm==1 and fi==1) or
                  (fm==0 and fi==2 and name=='_BSS')),
                 'unreviewed original source CODE offset frame')
            value=offsets[name]['start']-(0 if name=='_TEXT' else cal_group*16)
            a=b=(old+value)&0xffff
            binding='original_SEGDEF:'+name
        elif f['kind']==2:
            need(f['target_method']==1 and ti<len(groups) and
                 groups[ti]=='DGROUP' and fm==5,
                 'unsupported original MZ segment fixup')
            a=(old+cal_group)&0xffff
            b=(old+original_group)&0xffff
            relocations.append(site)
            binding='DGROUP_segment'
        else:
            raise ValueError('unreviewed source CODE fixup width/target')
        cal[site:site+2]=a.to_bytes(2,'little')
        original[site:site+2]=b.to_bytes(2,'little')
        actions.append({**f,'site':site,'binding':binding,
                        'calibrated_word_sha256':sha(a.to_bytes(2,'little')),
                        'native_word_sha256':sha(b.to_bytes(2,'little'))})
    return bytes(cal),bytes(original),actions,relocations


def replay():
    parent=json.loads(MASTER.read_text())
    archive=stored_lzh(pinned(ROOT,parent['inputs']['inner_archive']))
    from collections import defaultdict
    upstream=defaultdict(list)
    for file,raw in archive.items():
        if not file.upper().endswith('.ASM'):continue
        try:sections=source_blocks(raw,'cp932')
        except UnicodeDecodeError:continue
        for section in sections:upstream[section['name'].casefold()].append((file,section['text']))
    outputs=[]
    for art in ARTIFACTS:
        module='op' if art=='op' else 'mainem'
        source='th05_op.asm' if art=='op' else 'th05_maine_master.asm'
        p=ROOT/f'.analysis/builds/{art}-calibration-a/source'
        path=p/f'obj/th05/{module}.obj'
        obj=path.read_bytes()
        desc=describe_omf(obj)
        need(desc['valid'] and desc['module_name']==source,
             'native original Master TASM source module identity differs')
        segs,blocks,fixups,groups=real_omf(obj)
        map_raw,offsets,public=native_map(art,source,segs)
        target=load_unit_target(UnitContext(ROOT,art),UnitContext(ROOT,art).config())[1]
        cal=parse_mz((p/f'bin/th05/{art}.exe').read_bytes())
        need(cal.valid and target.valid and
             cal.program_image[0]==target.program_image[0]==0xba,
             'native original and calibration CRT segment model differs')
        cg=int.from_bytes(cal.program_image[1:3],'little')
        og=int.from_bytes(target.program_image[1:3],'little')
        need(og-cg==(1 if art=='maine' else 0),
             'original OP/MAINE DGROUP frame differs from pinned CRT')
        source_evidence={}
        for name,scope in FUNCTIONS.items():
            if art not in scope:continue
            start,size=scope[art]
            if name.startswith('SUPERPUT_DISP'):
                # Real TASM local PROC symbols are intentionally absent
                # from the exported MAP publics. Validate their positions
                # relative to the independently verified SUPER_PUT entry.
                delta={'SUPERPUT_DISP1':240,'SUPERPUT_DISP2':276,
                       'SUPERPUT_DISP3':322,'SUPERPUT_DISP4':376,
                       'SUPERPUT_DISP':426}[name]
                need(start==FUNCTIONS['SUPER_PUT'][art][0]+delta,
                     'native private SUPERPUT PROC position drift')
                source_path=p/'libs/master.lib/super_put.asm'
                native=near_proc_blocks(source_path.read_bytes(),'utf8',name)
                author_name=name.replace('SUPERPUT_','')
                archived=near_proc_blocks(archive['SUPERPUT.ASM'],'cp932',author_name)
                need(len(native)==len(archived)==1,
                     'complete private Master SUPERPUT PROC missing')
                block=native[0]
                ref_file='SUPERPUT.ASM'
                ref=archived[0]['text']
            else:
                need(start in public.get(name,set()),
                     'genuine TASM/MAP complete Master function entry differs')
                source_paths=[(f,b) for f in (p/'libs/master.lib').glob('*.asm')
                              for b in source_blocks(f.read_bytes(),'utf8')
                              if b['name']==name]
                refs=upstream[name.casefold()]
                need(len(source_paths)==len(refs)==1,
                     'original or compiled Master function source missing/ambiguous: '+name)
                source_path,block=source_paths[0]
                ref_file,ref=refs[0]
            norm=normalized_source(ref,name)
            need(norm==normalized_source(block['text'],name),
                 'original author Master function operands/source differ: '+name)
            blob=whole_source(blocks,start,size)
            actions=[f for f in fixups if start<=f['site']<start+size]
            ca,ori,source_actions,mz=rebind(blob,actions,start,offsets,segs,groups,cg,og)
            need(ca==cal.program_image[start:start+size] and
                 ori==target.program_image[start:start+size],
                 'complete original source-linked Master function bytes differ: '+name)
            need(mz==relative_fixups(cal,start,size)==relative_fixups(target,start,size),
                 'original ordered MZ relocations differ from native OMF')
            need(target.program_image.find(ori)==start and
                 target.program_image.find(ori,start+1)<0,
                 'complete native original Master CODE extent ambiguous')
            outputs.append({'artifact':'th05-'+art,'member':name,'start':start,
                            'end':start+size,'size':size,'native_OMF_sha256':sha(obj),
                            'native_MAP_sha256':sha(map_raw),
                            'original_author_archive_member':ref_file,
                            'original_author_source_sha256':sha(ref.encode('utf8')),
                            'native_TASM_source':str(source_path.relative_to(p)),
                            'native_TASM_source_sha256':digest_file(source_path),
                            'canonical_source_sha256':sha('\n'.join(norm).encode('utf8')),
                            'canonical_source_lines':len(norm),
                            'source_unlinked_CODE_sha256':sha(blob),
                            'original_linked_CODE_sha256':sha(ori),
                            'calibrated_linked_CODE_sha256':sha(ca),
                            'OMF_actions':source_actions,
                            'original_ordered_MZ':mz,
                            'authored_credit':0})
    return {'schema_version':1,'kind':'native-original-OP-MAINE-Master-large-procedures',
            'scopes':outputs,'source_verified_CODE_bytes':sum(x['size'] for x in outputs),
            'original_master_archive_sha256':parent['inputs']['inner_archive']['sha256'],
            'parent_master_proof_sha256':digest_file(MASTER),
            'verifier_sha256':digest_file(ROOT/'scripts/review_context_master_large.py'),
            'authored_credit':0,'non_CODE_bytes_claimed':0}


def validate_public(record):
    parent=json.loads(MASTER.read_text())
    expected=[('th05-'+art,name,values[art][0],values[art][1]) for art in ARTIFACTS
              for name,values in FUNCTIONS.items() if art in values]
    need(record.get('schema_version')==1 and
         record.get('kind')=='native-original-OP-MAINE-Master-large-procedures' and
         record.get('source_verified_CODE_bytes')==sum(x[3] for x in expected) and
         record.get('original_master_archive_sha256')==parent['inputs']['inner_archive']['sha256'] and
         record.get('parent_master_proof_sha256')==digest_file(MASTER) and
         record.get('verifier_sha256')==digest_file(ROOT/'scripts/review_context_master_large.py') and
         record.get('authored_credit')==record.get('non_CODE_bytes_claimed')==0,
         'original Master source/scope or verifier identity changed')
    scopes=record.get('scopes')
    need(isinstance(scopes,list) and
         [(r.get('artifact'),r.get('member'),r.get('start'),r.get('size'))
          for r in scopes]==expected,'unreviewed Master full-function extent or source order')
    for row in scopes:
        need(row.get('end')==row['start']+row['size'] and row.get('authored_credit')==0 and
             isinstance(row.get('canonical_source_lines'),int) and row['canonical_source_lines']>5 and
             row.get('original_ordered_MZ')==
             [f['site'] for f in row['OMF_actions'] if f['kind']==2],
             'source binding or original MZ order incomplete')
        for field in ('native_OMF_sha256','native_MAP_sha256','original_author_source_sha256',
                      'native_TASM_source_sha256','canonical_source_sha256',
                      'source_unlinked_CODE_sha256','original_linked_CODE_sha256',
                      'calibrated_linked_CODE_sha256'):
            need(isinstance(row.get(field),str) and re.fullmatch('[0-9a-f]{64}',row[field]),
                 'whole native source or linked digest missing')
    if DECISION.exists():
        d=json.loads(DECISION.read_text())
        need(d.get('schema_version')==1 and
             d.get('decision')=='ADOPT_ONLY_COMPLETE_ORIGINAL_MASTER_PROCEDURES' and
             d.get('evidence_sha256')==digest_file(PROOF) and
             d.get('scopes')==[[r['artifact'],r['member']] for r in scopes] and
             d.get('CODE_bytes')==record['source_verified_CODE_bytes'] and
             d.get('authored_credit')==d.get('other_bytes_claimed')==0,
             'explicit original Master function adoption differs')


def reviewed_claims(root,artifact,view,*,verify_targets=False):
    if artifact not in ARTIFACTS or not DECISION.exists():return [],None
    need(root.resolve()==ROOT.resolve(),'wrong source checkout for native original Master')
    record=json.loads(PROOF.read_text());validate_public(record)
    allowed=tomllib.loads((ROOT/'config/ownership.toml').read_text())['views']
    need(view['sha256']==allowed[artifact]['sha256'],
         'large native Master source belongs to another original decoded target')
    if verify_targets:need(replay()==record,'native original Master OMF/source reconstruction changed')
    return ([{'start':r['start'],'end':r['end'],
              'kind':'verified-vendor-code','library':'master.lib 0.23',
              'member':r['member'],'authored_credit':0}
             for r in record['scopes'] if r['artifact']=='th05-'+artifact],
            digest_file(DECISION))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    mode=p.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write',action='store_true')
    mode.add_argument('--check',action='store_true')
    mode.add_argument('--structural-check',action='store_true')
    args=p.parse_args()
    if args.write:
        need(not PROOF.exists() and not DECISION.exists(),
             'do not overwrite original Master review input')
        result=replay()
        PROOF.write_text(json.dumps(result,indent=2)+'\n')
        print('PASS: source exact OP/MAINE original Master CODE',result['source_verified_CODE_bytes'])
    else:
        result=json.loads(PROOF.read_text());validate_public(result)
        if args.check:
            need(replay()==result,'native original Master whole source/relocation mismatch')
            print('PASS: original OP/MAINE Master source, complete CODE and ordered MZ')
        else:print('PASS: original Master complete source proof is current')


if __name__=='__main__':main()
