#!/usr/bin/env python3
"""Native source-linked Master 0.23 music driver CODE in original TH05 MAIN.

Recover complete instruction extents from the retained TASM original-language
OMF and original Master archive. Source-operand equivalence allows only named
local labels, an explicit old macro CALL -> NOP/CALL port, and type annotations.
No target/code bytes are patched, and vendor bytes earn zero game-authored credit.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

from lib.pc98 import parse_mz,digest_file
from lib.unit_oracle import relative_fixups
from review_master import object_text,source_blocks,stored_lzh,need,sha,pinned
from review_main_runtime import startup
from review_master_super import CALIBRATED_OFFSETS,DATA_DELTA,BIAS

ROOT=Path(__file__).resolve().parents[1]
PROOF=ROOT/'config/master_bgm_ownership.json'
DECISION=ROOT/'config/reviewed_master_bgm.json'
BASE=ROOT/'config/master_vendor_ownership.json'
MEMBERS=(
    ('_BGM_BELL_ORG',0x3690,48),
    ('_BGM_MGET',0x36e8,298),
    ('BGM_READ_SDATA',0x3812,320),
    ('_BGM_TIMER_INIT',0x3952,68),
    ('_BGM_TIMER_FINISH',0x3996,42),
    ('_BGM_PINIT',0x39c0,62),
    ('_BGM_TIMERHOOK',0x39fe,176),
    ('BGM_BELL',0x3aae,104),
    ('_BGM_PLAY',0x3b16,302),
    ('BGM_SOUND',0x3c44,74),
    ('_BGM_EFFECT_SOUND',0x3c8e,120),
    ('BGM_STOP_PLAY',0x3d06,26),
    ('BGM_SET_TEMPO',0x3d20,46),
    ('BGM_INIT',0x3d4e,420),
    ('BGM_FINISH',0x3ef2,94),
    ('BGM_STOP_SOUND',0x3f50,26),
)


def source_lines(raw,name):
    """Only documented type/macro spellings and function-local namespaces."""
    body=raw.lower().replace('@@','').replace('nopcall','call').replace('.spart.','.')
    for a,b in (('b_init_',''),('b_e_snd_',''),('b_b_org_','')):
        body=body.replace(a,b)
    rows=[re.sub(r'\s+','',line.split(';',1)[0]) for line in body.splitlines()
          if line.split(';',1)[0].strip()]
    if name=='BGM_READ_SDATA':
        # Original FAR stack _push macro vs one active LDATA assembly arm.
        # No instruction or source operand is omitted from the real OMF.
        if 'ifldata' in rows:
            need(rows.count('ifldata')==rows.count('endif')==1,
                 'unknown BGM file-loader conditional source macro')
        rows=[r.replace('_push[','push[').replace('pushwordptr[','push[')
              for r in rows if r not in ('ifldata','endif')]
    if name=='_BGM_BELL_ORG':
        # The unused original PC-98 fallthrough label is absent in the port.
        need(not any('pc98' in r and r!='pc98:' for r in rows),
             'unknown bell machine-branch source reference')
        rows=[r for r in rows if r!='pc98:']
    if name=='BGM_INIT':
        rows=[x.replace('pushwordptr[bp+bsize2]','push[bp+bsize2]') for x in rows]
    if name=='_BGM_EFFECT_SOUND':
        # Original unused label is absent in the port; no branch references it.
        need(not any('pcat' in x and x!='pcat:' for x in rows),
             'unknown original sound label reference')
        rows=[x for x in rows if x!='pcat:']
    return rows


def private_bgm_bell_source(author, native):
    """The original private BGM_BELL label before the exported _BGM_PLAY."""
    def body(raw):
        lines=raw.splitlines()
        starts=[i for i,line in enumerate(lines) if line.strip().lower()=='bgm_bell:']
        ends=[i for i,line in enumerate(lines) if line.strip().lower().startswith('func _bgm_play')]
        need(len(starts)==len(ends)==1 and starts[0]<ends[0],
             'original Master BGM bell source/private boundary changed')
        return '\n'.join(lines[starts[0]:ends[0]]),(starts[0]+1,ends[0])
    source,old_range=body(author)
    candidate,new_range=body(native)
    expected=source_lines(source,'BGM_BELL')
    actual=source_lines(candidate,'BGM_BELL')
    # Exact local-label namespace and original packed SPART/SGLB field
    # qualifiers are the only source adaptations. The old PCAT marker is
    # unreferenced; the native conditional branch still has the same body.
    changes={
        'cmp[si].pmask,on':'cmp[si].sglb.pmask,on',
        'jeshortexit':'jeshortb_play_exit',
        'jneshortnotoct1':'jneshortb_play_notoct1',
        'jmpshortoct1':'jmpshortb_play_oct1',
        'notoct1:':'b_play_notoct1:',
        'oct1:':'b_play_oct1:',
        'jzshortpc98':'jzshortb_play_pc98',
        'pcat:inal,61h':'inal,61h',
        'jmpshortdo_scale':'jmpshortb_play_do_scale',
        'pc98:':'b_play_pc98:',
        'jzshortclock10mhz':'jzshortb_play_clock10mhz',
        'do_scale:':'b_play_do_scale:',
        'clock10mhz:':'b_play_clock10mhz:',
        'exit:':'b_play_exit:',
    }
    for old in changes:
        need(expected.count(old)==1,
             'original BGM BELL private field or jump changed: '+old)
    adapted=[changes.get(line,line) for line in expected]
    need(adapted==actual,
         'BGM_BELL source differs beyond the original local labels and struct qualifiers')
    return source,candidate,old_range,new_range,sha('\n'.join(adapted).encode('utf8'))


def source_proof(base):
    archive=stored_lzh(pinned(ROOT,base['inputs']['inner_archive']))
    original={}
    for filename,raw in archive.items():
        if not filename.upper().endswith('.ASM'):continue
        try: blocks=source_blocks(raw,'cp932')
        except UnicodeDecodeError:continue
        for item in blocks:
            original.setdefault(item['name'].casefold(),[]).append((filename,item))
    live={row['name']:row for row in base['active_procedure_inventory']}
    frozen={x['name']:x for x in base['frozen_source_closure']}
    result={}
    for member,start,size in MEMBERS:
        if member=='BGM_BELL':
            # This is a full private near PROC in B_PLAY.ASM, physically
            # between the timer hook and the exported _BGM_PLAY, not a MAP
            # public of its own. Review the source outside PROC block parser.
            row=live['_BGM_PLAY']
            source_file=row['source']
            need(source_file in frozen and source_file.endswith('/bgm_play.asm'),
                 'original BGM_BELL source context differs')
            content=(ROOT/base['candidate_source_root']/source_file).read_bytes()
            need(sha(content)==frozen[source_file]['sha256'],
                 'private Master BGM source changed from native TASM input')
            old_bell=archive['B_PLAY.ASM'].decode('cp932')
            native_bell=content.decode('utf8')
            old,native,old_span,new_span,canonical=private_bgm_bell_source(old_bell,native_bell)
            need(start==0x3aae and size==104 and
                 live['_BGM_TIMERHOOK']['end']==start and
                 row['start']==start+size,
                 'private BGM_BELL complete source bounds shifted')
            result[member]={
                'candidate_source':source_file,
                'candidate_source_sha256':sha(content),
                'upstream_archive_member':'B_PLAY.ASM',
                'upstream_block_sha256':sha(old.encode('utf8')),
                'candidate_block_sha256':sha(native.encode('utf8')),
                'semantic_instruction_sha256':canonical,
                'candidate_line_span':list(new_span),
                'private_original_line_span':list(old_span),
            }
            continue
        row=live[member]
        need((row['start'],row['end'])==(start,start+size),
             'BGM original active source listing boundary changed')
        source_file=row['source'];need(source_file in frozen,
             'BGM source absent from genuine linked OMF closure')
        content=(ROOT/base['candidate_source_root']/source_file).read_bytes()
        need(sha(content)==frozen[source_file]['sha256'],
             'BGM source differs from original native assembler producer')
        candidate=[x for x in source_blocks(content,'utf8') if x['name']==member]
        need(len(candidate)==1,'native original-language BGM procedure incomplete')
        matches=[(filename,src) for filename,src in original.get(member.casefold(),[])
                 if source_lines(src['text'],member)==source_lines(candidate[0]['text'],member)]
        need(len(matches)==1,'unreviewed original Master BGM instruction/operand change: '+member)
        filename,up=matches[0]
        # Original call macro expansions and local labels are recorded as
        # source adaptations, never byte exemptions in the linked comparison.
        result[member]={'candidate_source':source_file,
                        'candidate_source_sha256':sha(content),
                        'upstream_archive_member':filename,
                        'upstream_block_sha256':sha(up['text'].encode('utf8')),
                        'candidate_block_sha256':sha(candidate[0]['text'].encode('utf8')),
                        'semantic_instruction_sha256':sha(
                            '\n'.join(source_lines(up['text'],member)).encode('utf8')),
                        'candidate_line_span':[candidate[0]['start_line'],candidate[0]['end_line']]}
    return result


def linked_scope(obj,start,size):
    low=start-BIAS;src=bytearray(size);coverage=bytearray(size)
    for b in obj['blocks']:
        a=max(low,b['offset']);z=min(low+size,b['offset']+len(b['content']))
        if a>=z:continue
        aa=a-low;zz=z-low
        need(not any(coverage[aa:zz]),'BGM original CODE source LEDATA overlap')
        src[aa:zz]=b['content'][a-b['offset']:z-b['offset']]
        coverage[aa:zz]=b'\1'*(z-a)
    need(all(coverage),'BGM whole original source CODE LEDATA incomplete')
    control=bytearray(src);native=bytearray(src);actions=[];mz=[];covered=set()
    for f in obj['fixups']:
        site=f['offset']+BIAS
        width={1:2,2:2,3:4}[f['kind']]
        if site+width<=start or site>=start+size:continue
        need(start<=site and site+width<=start+size and f['absolute'] and f['displacement']==0,
             'original BGM source FIXUPP crosses the full function extent')
        index=site-start
        need(not covered.intersection(range(index,index+width)),
             'native OMF BGM source has overlapping FIXUPP fields')
        covered.update(range(index,index+width))
        old=int.from_bytes(src[index:index+2],'little')
        if f['kind']==1:
            target=f['target_index'];fm=f['frame_method']
            need(f['target_method']==0 and target in CALIBRATED_OFFSETS and
                 ((target==1 and fm==5) or (target==2 and fm in (1,5)) or
                  (target==54 and fm in (0,1))) and
                 ((fm==0 and f['frame_index']==2) or
                  (fm==1 and f['frame_index']==1) or fm==5),
                 'unreviewed BGM original near offset fixup')
            base=CALIBRATED_OFFSETS[target]
            change=DATA_DELTA if target in (2,54) else 0
            cal=(old+base)&0xffff;orig=(old+base+change)&0xffff
            mode='native-offset16'
        elif f['kind']==2:
            need(f['frame_method']==5 and f['target_index']==1 and
                 ((f['target_method']==0) or (f['target_method']==1)),
                 'unreviewed BGM OMF segment binding')
            cal_frame=0 if f['target_method']==0 else 0x209e
            orig_frame=0 if f['target_method']==0 else 0x209d
            cal=(old+cal_frame)&0xffff;orig=(old+orig_frame)&0xffff
            mode='original-MZ-segment16'
            mz.append(index)
        else:raise ValueError('BGM original OMF far pointer not reviewed')
        control[index:index+2]=cal.to_bytes(2,'little')
        native[index:index+2]=orig.to_bytes(2,'little')
        actions.append({'source_site':index,'kind':f['kind'],
                        'target_method':f['target_method'],
                        'target_index':f['target_index'],
                        'frame_method':f['frame_method'],
                        'original_link_operation':mode,
                        'original_word_sha256':sha(orig.to_bytes(2,'little'))})
    return bytes(control),bytes(native),sha(src),mz,actions


def replay():
    base=json.loads(BASE.read_text())
    raw_obj=pinned(ROOT,base['inputs']['saved_object'])
    need(raw_obj==pinned(ROOT,base['inputs']['calibration_object']),
         'source-linked BGM original object/calibration differ')
    cal=parse_mz(pinned(ROOT,base['inputs']['calibration_exe']))
    orig=parse_mz(pinned(ROOT,base['inputs']['target']))
    before,after=startup(cal),startup(orig)
    need(before['dgroup']==0x209e0 and after['dgroup']==0x209d0 and
         after['bss_start']-before['bss_start']==DATA_DELTA and
         after['init_start']-before['init_start']==DATA_DELTA,
         'BGM source linkage has unreviewed original DATA/CRT frames')
    source=source_proof(base)
    obj=object_text(raw_obj)
    rows=[]
    for name,start,size in MEMBERS:
        a,b,unlinked,sites,actions=linked_scope(obj,start,size)
        expected=orig.program_image[start:start+size]
        if name=='BGM_BELL':
            # The whole near PROC is 103 instruction bytes followed by one
            # real EVEN NOP immediately before the exported _BGM_PLAY.
            need((start,size)==(0x3aae,104) and len(actions)==2 and
                 a[-1:]==b[-1:]==expected[-1:]==b'\x90' and
                 not sites,
                 'original private Master bell CODE/EVEN or fixups changed')
        need(a==cal.program_image[start:start+size] and b==expected,
             'original BGM OMF source does not reconstruct complete CODE: '+name)
        need(relative_fixups(cal,start,size)==relative_fixups(orig,start,size)==sites,
             'BGM original ordered MZ segment relocations differ')
        need(orig.program_image.find(expected)==start and
             orig.program_image.find(expected,start+1)<0,
             'original BGM full CODE occurrence not unique')
        rows.append({'member':name,'start':start,'end':start+size,'size':size,
                     'source':source[name],
                     'source_unlinked_CODE_sha256':unlinked,
                     'native_CODE_sha256':sha(b),
                     'calibration_CODE_sha256':sha(a),
                     'original_ordered_MZ_relocations':sites,
                     'OMF_source_actions':actions,'authored_credit':0})
    return {'schema_version':1,'kind':'original-master-BGM-source-and-MZ-link-review',
            'artifact':'th05-main','members':rows,
            'source_written_CODE_bytes':sum(x['size'] for x in rows),
            'original_DGROUP':after['dgroup'],'calibration_DGROUP':before['dgroup'],
            'source_data_offset_delta':DATA_DELTA,
            'original_target_sha256':base['inputs']['target']['sha256'],
            'calibration_exe_sha256':base['inputs']['calibration_exe']['sha256'],
            'source_object_sha256':base['inputs']['saved_object']['sha256'],
            'author_archive_sha256':base['inputs']['inner_archive']['sha256'],
            'parent_Master_proof_sha256':digest_file(BASE),
            'source_verifier_sha256':digest_file(ROOT/'scripts/review_master_bgm.py'),
            'assembly_model_sha256':digest_file(ROOT/'scripts/review_master_super.py'),
            'author_credit':0,'other_code_or_data_claimed':0}


def validate_public(j):
    base=json.loads(BASE.read_text())
    need(j.get('schema_version')==1 and
         j.get('kind')=='original-master-BGM-source-and-MZ-link-review' and
         j.get('artifact')=='th05-main' and
         j.get('source_written_CODE_bytes')==sum(n for _,_,n in MEMBERS) and
         j.get('original_DGROUP')==0x209d0 and j.get('calibration_DGROUP')==0x209e0 and
         j.get('source_data_offset_delta')==DATA_DELTA and
         j.get('original_target_sha256')==base['inputs']['target']['sha256'] and
         j.get('calibration_exe_sha256')==base['inputs']['calibration_exe']['sha256'] and
         j.get('source_object_sha256')==base['inputs']['saved_object']['sha256'] and
         j.get('author_archive_sha256')==base['inputs']['inner_archive']['sha256'] and
         j.get('parent_Master_proof_sha256')==digest_file(BASE) and
         j.get('source_verifier_sha256')==digest_file(ROOT/'scripts/review_master_bgm.py') and
         j.get('assembly_model_sha256')==digest_file(ROOT/'scripts/review_master_super.py') and
         j.get('author_credit')==j.get('other_code_or_data_claimed')==0,
         'original native Master BGM source verifier/target identity changed')
    rows=j.get('members',[])
    need([(z.get('member'),z.get('start'),z.get('size')) for z in rows]==list(MEMBERS),
         'original BGM source scope not the complete accepted functions')
    for row in rows:
        if row.get('member')=='BGM_BELL':
            need(len(row.get('OMF_source_actions',[]))==2 and
                 row.get('original_ordered_MZ_relocations')==[],
                 'original private bell source FIXUPP actions changed')
        need(row.get('end')==row['start']+row['size'] and
             row.get('authored_credit')==0 and
             isinstance(row.get('original_ordered_MZ_relocations'),list) and
             row.get('original_ordered_MZ_relocations')==
             [x['source_site'] for x in row.get('OMF_source_actions',[])
              if x.get('original_link_operation')=='original-MZ-segment16'],
             'missing original CODE extent/source or unsorted MZ fixups')
        for field in ('source_unlinked_CODE_sha256','native_CODE_sha256',
                      'calibration_CODE_sha256'):
            need(isinstance(row.get(field),str) and
                 re.fullmatch('[0-9a-f]{64}',row[field]),
                 'BGM source raw CODE SHA missing')
    if DECISION.exists():
        d=json.loads(DECISION.read_text())
        need(d.get('schema_version')==1 and d.get('artifact')=='th05-main' and
             d.get('decision')=='ADOPT_ONLY_NATIVE_BGM_COMPLETE_CODE' and
             d.get('evidence_sha256')==digest_file(PROOF) and
             d.get('members')==[x[0] for x in MEMBERS] and
             d.get('CODE_bytes')==j['source_written_CODE_bytes'] and
             d.get('authored_credit')==d.get('other_bytes_claimed')==0,
             'explicit BGM original native source CODE adoption changed')


def reviewed_claims(root,view,*,verify_targets=False):
    if not DECISION.exists():return [],None
    need(root.resolve()==ROOT.resolve(),'wrong source checkout')
    record=json.loads(PROOF.read_text());validate_public(record)
    need(view['sha256']==json.loads(BASE.read_text())['target_payload_sha256'],
         'original BGM CODE belongs to another target')
    if verify_targets:need(replay()==record,'actual source-linked BGM original differs')
    return ([{'start':r['start'],'end':r['end'],'kind':'verified-vendor-code',
              'library':'master.lib 0.23','member':r['member'],'authored_credit':0}
             for r in record['members']],digest_file(DECISION))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    mode=p.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write',action='store_true')
    mode.add_argument('--check',action='store_true')
    mode.add_argument('--structural-check',action='store_true')
    args=p.parse_args()
    if args.write:
        need(not PROOF.exists() and not DECISION.exists(),
             'cannot silently replace original BGM source proof')
        r=replay()
        PROOF.write_text(json.dumps(r,indent=2)+'\n')
        print('PASS: source exact original Master BGM CODE',r['source_written_CODE_bytes'])
    else:
        r=json.loads(PROOF.read_text());validate_public(r)
        if args.check:
            need(replay()==r,'original BGM CODE OMF/source source evidence differs')
            print('PASS: original complete Master BGM source CODE and MZ fixups')
        else:
            print('PASS: source-current original BGM code proof')


if __name__=='__main__':
    main()
