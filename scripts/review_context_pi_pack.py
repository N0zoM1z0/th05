#!/usr/bin/env python3
"""Complete OP/MAINE GRAPH_PI_LOAD_PACK OMF reconstruction from Master 0.23.

The original author function and maintained ReC98 adaptation have identical
438 source operations after explicitly reviewed assembler notation changes.
Each real native TASM OMF is relinked through its actual _DATA/DGROUP
contribution and original CRT segment word, not target-derived code.
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

ROOT = Path(__file__).resolve().parents[1]
PROOF = ROOT/'config/context_pi_pack.json'
DECISION = ROOT/'config/reviewed_context_pi_pack.json'
PARENT = ROOT/'config/master_vendor_ownership.json'
SOURCE = 'libs/master.lib/graph_pi_load_pack.asm'
UPSTREAM = 'GRPPILOD.ASM'
PROC = 'GRAPH_PI_LOAD_PACK'
LENGTH = 1512
# Both functions are complete original assembler procedures. The native
# original DATA order differs, so read the real MAP rather than assuming
# OP/MAINE share offsets or that calibration and original segment frames match.
TARGETS = {
    'op': {'module':'op','source':'th05_op.asm','start':0x1354,
           'code_segdef':0x38a6,'data_segdef_offset':0x4d2},
    'maine': {'module':'mainem','source':'th05_maine_master.asm','start':0x1446,
              'code_segdef':0x3a6e,'data_segdef_offset':0x00bc},
}
TRAMPOLINES = {
    ('jzshortgrppilod_color','jmp_errora','grppilod_color:'): 'jnz_errora',
    ('jzshortgrppilod_machine_information','jmp_errora','grppilod_machine_information:'): 'jnz_errora',
    ('jnbshortgrppilod_set_ptrs','jmp_errora','grppilod_set_ptrs:'): 'jc_errora',
    ('jnzshortgrppilod_length_context','jmpend_rla','grppilod_length_context:'): 'jzend_rla',
    ('jnzshortgrppilod_position','jmp_position_zero','grppilod_position:'): 'jz_position_zero',
    ('jbeshort_end_checkc','jmp_main_decode_loopa','_end_checkc:'): 'jnbe_main_decode_loopa',
    ('jbeshortfile_close','jmp_main_decode_loopa','file_close:'): 'jnbe_main_decode_loopa',
}


def lines(raw):
    return [re.sub(r'\s+','',line.split(';',1)[0].lower().replace('@@',''))
            for line in raw.splitlines() if line.split(';',1)[0].strip()]


def source_operations(original,adapted):
    author = [token.replace('_push[','push[') for token in lines(original)]
    tokens = lines(adapted)
    candidate=[]
    position=0
    expanded_far=trampoline_count=0
    while position<len(tokens):
        prefix=tuple(tokens[position:position+3])
        if prefix==('ifldata','pushwordptr[bp+filename+2]','endif'):
            candidate.append('push[bp+filename+2]')
            expanded_far+=1
            position+=3
            continue
        if prefix in TRAMPOLINES:
            candidate.append(TRAMPOLINES[prefix])
            trampoline_count+=1
            position+=3
            continue
        token=tokens[position]
        token=(token.replace('ds:','').replace('nopcall','call')
               .replace('pi_eof','eof').replace('pushwordptr','push'))
        candidate.append(token)
        position+=1
    need(len(author)==len(candidate)==438 and author==candidate and
         expanded_far==1 and trampoline_count==7,
         'full original Master PI loader source differs in an unreviewed operation')
    return {'effective_source_lines':438,
            'normalized_full_source_sha256':sha('\n'.join(author).encode('utf8')),
            'far_parameter_macro_expansions':expanded_far,
            'equivalent_long_branch_trampolines':trampoline_count}


def actual_source(root, artifact, description):
    build=root/f'.analysis/builds/{artifact}-calibration-a/source'
    fname=build/SOURCE
    need(SOURCE in description['dependency_paths'], 'real TASM object did not depend on loader ASM')
    contents=fname.read_bytes()
    matches=[s for s in source_blocks(contents,'utf8') if s['name']==PROC]
    need(len(matches)==1,'real TASM input contains no unique full loader')
    return contents,matches[0]['text']


def compiled_map(root,artifact,spec):
    p=root/f'.analysis/builds/{artifact}-calibration-a/source/obj/th05/{artifact}.map'
    payload=p.read_bytes()
    text=payload.decode('cp437')
    contrib=[]
    # Actual TLINK module _TEXT/_DATA sections, not inferred from target.
    for line in text.splitlines():
        m=re.match(r'\s*([0-9A-F]{4}):([0-9A-F]{4})\s+([0-9A-F]{4})\s+'
                   r'C=(\S+)\s+S=(\S+)\s+G=(\S+)\s+M=(\S+)',line,re.I)
        if m and m[7].casefold()==spec['source'].casefold():
            contrib.append({'start':int(m[1],16)*16+int(m[2],16),
                            'size':int(m[3],16),'class':m[4],
                            'segment':m[5],'group':m[6]})
    text_seg=[r for r in contrib if r['segment']=='_TEXT' and r['class']=='CODE']
    data_seg=[r for r in contrib if r['segment']=='_DATA' and r['class']=='DATA']
    need(len(text_seg)==len(data_seg)==1 and
         text_seg[0]['start']==0x272 and
         text_seg[0]['size']==spec['code_segdef'] and
         data_seg[0]['size']>0 and
         data_seg[0]['group']=='DGROUP',
         'original TASM object and MAP segment contributions differ')
    # Validate actual native public name/frame from the value section.
    starts=[int(a,16)*16+int(b,16) for a,b in
        re.findall(r'(?m)^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+'
                   +re.escape(PROC)+r'\s*$',text)]
    need(starts and set(starts)=={spec['start']},'native PI loader public MAP extent missing')
    return payload,data_seg[0]['start']


def source_object_scope(omf,start,size):
    names=[''];segments=[None];groups=[None];blocks=[];fixups=[];last=None
    for r in parse_omf(omf):
        b=r.data
        if r.name=='LNAMES':
            pos=0
            while pos<len(b):
                n=b[pos];pos+=1
                need(pos+n<=len(b),'original OMF LNAMES truncated')
                names.append(b[pos:pos+n].decode('ascii'));pos+=n
        elif r.name=='SEGDEF':
            ni,pos=idx(b,3);ci,pos=idx(b,pos);oi,pos=idx(b,pos)
            need(0<ni<len(names) and 0<ci<len(names),
                 'invalid original OMF SEGDEF name/class')
            segments.append({'name':names[ni],'cl':names[ci],
                             'size':int.from_bytes(b[1:3],'little')})
        elif r.name=='GRPDEF':
            ni,pos=idx(b,0)
            need(0<ni<len(names),'unknown original OMF GRPDEF')
            groups.append(names[ni])
        elif r.name=='LEDATA':
            si,pos=idx(b,0)
            offset=int.from_bytes(b[pos:pos+2],'little')
            data=b[pos+2:]
            need(si<len(segments) and offset+len(data)<=segments[si]['size'],
                 'original TASM CODE LEDATA outside SEGDEF')
            blocks.append((si,offset,data))
            last=(si,offset)
        elif r.name=='FIXUPP':
            need(last is not None,'FIXUPP without matching original source LEDATA')
            pos=0
            while pos<len(b):
                need(pos+3<=len(b),'OMF FIXUPP truncated')
                loc,flags=b[pos],b[pos+2]
                need(loc&128 and not flags&0x88,'unreviewed original OMF threaded relocation')
                relative=not bool(loc&64)
                local=((loc&3)<<8)|b[pos+1]
                kind=(loc>>2)&15
                frame_method=(flags>>4)&7
                tm=flags&3
                pos+=3
                if frame_method<=2:frame_index,pos=idx(b,pos)
                else:
                    need(frame_method in (4,5),'unreviewed OMF frame operation')
                    frame_index=None
                target_index,pos=idx(b,pos)
                displacement=0
                if not flags&4:
                    displacement=int.from_bytes(b[pos:pos+2],'little');pos+=2
                if last[0]!=1:continue
                linked_site=last[1]+local+0x272
                if start<=linked_site<start+size:
                    need(kind in (1,2) and start<=linked_site<start+size-1 and
                         not relative and displacement==0,
                         'original PI loader CODE fixup incomplete or unsupported')
                    fixups.append({'site':linked_site-start,'kind':kind,
                                   'frame_method':frame_method,
                                   'frame_index':frame_index,
                                   'target_method':tm,
                                   'target_index':target_index})
    need(len(segments)>2 and
         segments[1]['name']=='_TEXT' and segments[1]['cl']=='CODE' and
         segments[2]['name']=='_DATA' and segments[2]['cl']=='DATA' and
         len([r for r in segments if r and r['name']=='_TEXT'])==1 and
         len(groups)>1 and groups[1]=='DGROUP',
         'original source OMF did not retain unique _TEXT, _DATA, DGROUP')
    low=start-0x272
    source=bytearray(size);coverage=bytearray(size);used=[]
    for seg,offset,payload in blocks:
        if seg!=1:continue
        a=max(low,offset);z=min(low+size,offset+len(payload))
        if a>=z:continue
        need(not any(coverage[a-low:z-low]),'source CODE LEDATA overlapping writes')
        coverage[a-low:z-low]=b'\1'*(z-a)
        source[a-low:z-low]=payload[a-offset:z-offset]
        used.append({'source_SEGDEF':seg,'offset':offset,'size':len(payload),
                     'sha256':sha(payload)})
    need(all(coverage),'original complete native PI loader CODE has unwritten bytes')
    # Source contains 3 genuine SEG16 DGROUP pointers, 2 DGROUP data
    # offsets, and no local or unsupported relocation.
    need(len(fixups)==5 and
         sorted(f['site'] for f in fixups if f['kind']==2)==[220,309,1192] and
         sorted(f['site'] for f in fixups if f['kind']==1)==[225,314],
         'source CODE FIXUPP sites differ from complete real loader')
    return bytes(source), fixups, used,segments[1]['size']


def native_rebind(source,fixups,data_offset,group_paragraph):
    out=bytearray(source);written=set();actions=[];relocations=[]
    for f in fixups:
        index=f['site']
        need(not written.intersection((index,index+1)),
             'unreviewed original OMF overlapping source fixups')
        written.update((index,index+1))
        old=int.from_bytes(source[index:index+2],'little')
        if f['kind']==1:
            need(f['target_method']==0 and f['target_index']==2 and
                 ((f['frame_method']==1 and f['frame_index']==1) or
                  f['frame_method']==5),
                 'unreviewed native PI loader DATA-offset frame')
            value=(old+data_offset)&0xffff; operation='DGROUP_DATA_offset16'
        else:
            need(f['target_method']==1 and f['target_index']==1 and
                 f['frame_method']==5,'unreviewed native PI loader DGROUP paragraph')
            value=(old+group_paragraph)&0xffff
            operation='DGROUP_segment16'
            relocations.append(index)
        raw=value.to_bytes(2,'little')
        out[index:index+2]=raw
        actions.append({**f,'operation':operation,'written_word_sha256':sha(raw)})
    return bytes(out),relocations,actions


def replay():
    parent=json.loads(PARENT.read_text())
    original_archive=stored_lzh(pinned(ROOT,parent['inputs']['inner_archive']))
    original_src=original_archive[UPSTREAM]
    original_blocks=[z for z in source_blocks(original_src,'cp932') if z['name']==PROC]
    need(len(original_blocks)==1,'original Master 0.23 archive missing full PI loader')
    evidence=[]
    for art,spec in TARGETS.items():
        root=ROOT/f'.analysis/builds/{art}-calibration-a/source'
        obj_path=root/f'obj/th05/{spec["module"]}.obj'
        obj=obj_path.read_bytes()
        desc=describe_omf(obj)
        need(desc['valid'] and desc['module_name']==spec['source'],
             'actual native TASM PI loader OMF identity changed')
        compiled_source,compiled_block=actual_source(ROOT,art,desc)
        src_proof=source_operations(original_blocks[0]['text'],compiled_block)
        raw_map,data_linear=compiled_map(ROOT,art,spec)
        cal=parse_mz((root/f'bin/th05/{art}.exe').read_bytes())
        ctx=UnitContext(ROOT,art)
        _,target,_=load_unit_target(ctx,ctx.config())
        need(cal.valid and target.valid and
             cal.program_image[0]==target.program_image[0]==0xba,
             'original/calibrated CRT startup not recognized')
        group_cal=int.from_bytes(cal.program_image[1:3],'little')
        group_original=int.from_bytes(target.program_image[1:3],'little')
        # For MAINE the authentic group frame increases from 1010h to 1011h,
        # whereas OP's original and native calibration use the same frame.
        need((group_original-group_cal)==(1 if art=='maine' else 0),
             'original CRT group-base independently differs')
        data_offset=data_linear-group_cal*16
        need(data_offset==spec['data_segdef_offset'],'real source DATA MAP offset changed')
        source,fixups,ledatas,text_size=source_object_scope(obj,spec['start'],LENGTH)
        need(text_size==spec['code_segdef'],'native original OMF full _TEXT size changed')
        a,ma,cal_actions=native_rebind(source,fixups,data_offset,group_cal)
        b,mb,actions=native_rebind(source,fixups,data_offset,group_original)
        actual=target.program_image[spec['start']:spec['start']+LENGTH]
        need(a==cal.program_image[spec['start']:spec['start']+LENGTH] and
             b==actual,'real native TASM OMF source does not reconstruct whole original PI loader')
        need(ma==mb==relative_fixups(cal,spec['start'],LENGTH)==
             relative_fixups(target,spec['start'],LENGTH)==[220,309,1192],
             'original ordered MZ relocations differ from source FIXUPP')
        need(target.program_image.find(actual)==spec['start'] and
             target.program_image.find(actual,spec['start']+1)<0,
             'native original full PI loader is ambiguous')
        evidence.append({'artifact':'th05-'+art,'start':spec['start'],
                         'end':spec['start']+LENGTH,'size':LENGTH,
                         'source':SOURCE,'upstream_archive_member':UPSTREAM,
                         'native_code_MODULE':spec['source'],
                         'native_object_sha256':sha(obj),
                         'native_compiled_assembly_sha256':sha(compiled_source),
                         'original_source_block_sha256':sha(original_blocks[0]['text'].encode('utf8')),
                         'source_match':src_proof,
                         'native_map_sha256':sha(raw_map),
                         'calibration_MZ_sha256':digest_file(root/f'bin/th05/{art}.exe'),
                         'native_group_paragraph':group_original,
                         'calibration_group_paragraph':group_cal,
                         'actual_data_MAP_offset':data_offset,
                         'original_unlinked_CODE_sha256':sha(source),
                         'source_CODE_LEDATA':ledatas,
                         'real_OMF_actions':actions,
                         'original_full_CODE_sha256':sha(b),
                         'calibration_full_CODE_sha256':sha(a),
                         'ordered_native_MZ_fixups':mb,
                         'authored_credit':0})
    return {'schema_version':1,'kind':'two-original-Master-PI-loader-TASM-OMF-link',
            'source':'independently archived original Master 0.23 graphical PI/RLE decoder',
            'functions':evidence,
            'complete_source_CODE_bytes':sum(r['size'] for r in evidence),
            'original_author_archive_sha256':parent['inputs']['inner_archive']['sha256'],
            'original_source_proof_sha256':digest_file(PARENT),
            'verifier_sha256':digest_file(ROOT/'scripts/review_context_pi_pack.py'),
            'authored_credit':0,'non_CODE_claimed':0}


def validate_public(proof):
    parent=json.loads(PARENT.read_text())
    need(proof.get('schema_version')==1 and
         proof.get('kind')=='two-original-Master-PI-loader-TASM-OMF-link' and
         proof.get('complete_source_CODE_bytes')==2*LENGTH and
         proof.get('original_author_archive_sha256')==parent['inputs']['inner_archive']['sha256'] and
         proof.get('original_source_proof_sha256')==digest_file(PARENT) and
         proof.get('verifier_sha256')==digest_file(ROOT/'scripts/review_context_pi_pack.py') and
         proof.get('authored_credit')==proof.get('non_CODE_claimed')==0,
         'unreviewed original PI loader target, source or verifier')
    rows=proof.get('functions')
    need(isinstance(rows,list) and [r.get('artifact') for r in rows]==
         ['th05-'+art for art in TARGETS],'invalid native PI loader artifacts')
    for row,(art,spec) in zip(rows,TARGETS.items()):
        need((row.get('start'),row.get('end'),row.get('size'))==
             (spec['start'],spec['start']+LENGTH,LENGTH) and
             row.get('native_code_MODULE')==spec['source'] and
             row.get('source')==SOURCE and
             row.get('upstream_archive_member')==UPSTREAM and
             row.get('actual_data_MAP_offset')==spec['data_segdef_offset'] and
             row.get('native_group_paragraph')-row.get('calibration_group_paragraph')==
             (1 if art=='maine' else 0) and
             row.get('source_match',{}).get('effective_source_lines')==438 and
             row['source_match'].get('equivalent_long_branch_trampolines')==7 and
             row['source_match'].get('far_parameter_macro_expansions')==1 and
             row.get('ordered_native_MZ_fixups')==[220,309,1192] and
             [f.get('site') for f in row.get('real_OMF_actions',[])]==
             [220,309,225,314,1192] and
             row.get('authored_credit')==0,
             'unreviewed native PI loader source/OMF/code extent')
        for field in ('native_object_sha256','native_compiled_assembly_sha256',
                      'original_source_block_sha256','native_map_sha256',
                      'calibration_MZ_sha256','original_unlinked_CODE_sha256',
                      'original_full_CODE_sha256','calibration_full_CODE_sha256'):
            value=row.get(field)
            need(isinstance(value,str) and re.fullmatch('[0-9a-f]{64}',value),
                 'missing original native CODE SHA')
    if DECISION.exists():
        d=json.loads(DECISION.read_text())
        need(d.get('schema_version')==1 and
             d.get('decision')=='ADOPT_ONLY_BOTH_COMPLETE_NATIVE_PI_PACK_CODE' and
             d.get('evidence_sha256')==digest_file(PROOF) and
             d.get('artifacts')==[r['artifact'] for r in rows] and
             d.get('CODE_bytes')==2*LENGTH and
             d.get('authored_credit')==d.get('other_bytes_claimed')==0 and
             d.get('other_scopes_policy')=='unknown',
             'explicit two-target PI loader code ownership is stale')


def reviewed_claims(root,art,view,*,verify_targets=False):
    if art not in TARGETS or not DECISION.exists():return [],None
    need(root.resolve()==ROOT.resolve(),'incorrect original source checkout')
    proof=json.loads(PROOF.read_text())
    validate_public(proof)
    row=next(z for z in proof['functions'] if z['artifact']=='th05-'+art)
    allowed_views=tomllib.loads((ROOT/'config/ownership.toml').read_text())['views']
    need(view['sha256']==allowed_views[art]['sha256'],
         'source-linked PI loader belongs to another decoded original target')
    if verify_targets:need(replay()==proof,'original two-context OMF source reconstruction differs')
    return ([{'start':row['start'],'end':row['end'],
              'kind':'verified-vendor-code','library':'master.lib 0.23',
              'member':PROC,'authored_credit':0}],digest_file(DECISION))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write',action='store_true')
    mode.add_argument('--check',action='store_true')
    mode.add_argument('--structural-check',action='store_true')
    args=parser.parse_args()
    if args.write:
        need(not PROOF.exists() and not DECISION.exists(),
             'cannot overwrite the original PI loader evidence')
        result=replay()
        PROOF.write_text(json.dumps(result,indent=2)+'\n')
        print('PASS: original 2 x 1512-byte Master PI decode CODE:',result['complete_source_CODE_bytes'])
    else:
        proof=json.loads(PROOF.read_text());validate_public(proof)
        if args.check:
            need(replay()==proof,'raw original/OMF PI decode CODE evidence changed')
            print('PASS: original Master GRAPH_PI_LOAD_PACK in both native target contexts')
        else:
            print('PASS: source-current original PI loader review')


if __name__=='__main__':main()
