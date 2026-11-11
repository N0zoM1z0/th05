#!/usr/bin/env python3
"""Source-backed original Master SUPER helper procedures and CODE.

Only real source FUNC/retfunc or near PROC/ENDP extents are selected.
The original Master archive, pinned native TASM OMF and both linked
executables must agree on each entire selected extent and MZ relocations.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

from lib.pc98 import digest_file,parse_mz
from lib.unit_oracle import relative_fixups
from review_master import stored_lzh,source_blocks,need,sha,pinned,object_text,decoded
from review_master_super import code_scope
from review_main_runtime import startup

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'config/master_vendor_ownership.json'
PROOF=ROOT/'config/master_super_helpers.json'
DECISION=ROOT/'config/reviewed_master_super_helpers.json'

# (linked MAIN name, complete native start, size, author archive member,
#  original source entry name, original source grammar)
MEMBERS=(
 ('SUPERPAT_NO_MEMORY',0x2a24,10,'SUPERPAT.ASM','NO_MEMORY','func'),
 ('SUPER_ENTRY_BFNT',0x2d16,138,'SUPERBFT.ASM','SUPER_ENTRY_BFNT','func'),
 ('SUPERPTR_EXIT',0x31f6,6,'SUPERPTR.ASM','EXIT','func'),
 ('superptr_draw_shift',0x333a,70,'SUPERPTR.ASM','draw_shift','proc'),
 ('superptr_draw_noshift',0x3380,48,'SUPERPTR.ASM','draw_noshift','proc'),
 ('superptr_draw',0x33b0,63,'SUPERPTR.ASM','draw','proc'),
 ('SUPERPUT_DISP1',0x34e0,35,'SUPERPUT.ASM','DISP1','proc'),
 ('SUPERPUT_DISP2',0x3504,45,'SUPERPUT.ASM','DISP2','proc'),
 ('SUPERPUT_DISP3',0x3532,54,'SUPERPUT.ASM','DISP3','proc'),
 ('SUPERPUT_DISP4',0x3568,49,'SUPERPUT.ASM','DISP4','proc'),
 ('SUPERPUT_DISP',0x359a,8,'SUPERPUT.ASM','DISP','proc'),
 ('SUPER_PUT_8',0x40e6,124,'SUPERPT8.ASM','SUPER_PUT_8','func'),
)


def near_proc_blocks(raw,encoding,member):
    lines=decoded(raw,encoding).split('\n')
    begin=re.compile(r'^\s*'+re.escape(member)+r'\s+proc\s+near(?:\s|$)',re.I)
    end=re.compile(r'^\s*'+re.escape(member)+r'\s+endp\b',re.I)
    matches=[]
    for i,line in enumerate(lines):
        if not begin.match(line.split(';',1)[0]):continue
        for j in range(i+1,len(lines)):
            if end.match(lines[j].split(';',1)[0]):
                matches.append({'name':member,'start_line':i+1,'end_line':j+1,
                                'text':'\n'.join(lines[i:j+1])})
                break
    return matches


def canonical(text,member):
    text=text.lower().replace('@@','')
    # These are bounded namespaced equivalents of the upstream local
    # code/patch labels, not transformed instructions or altered immediates.
    for original,native in (
        ('superpat_no_memory','no_memory'),
        ('superptr_exit','exit'),
        ('superptr_s_drawlen_','_s_drawlen_'),
        ('superptr_s_add_si_','_s_add_si_'),
        ('superptr_s_add_di_','_s_add_di_'),
        ('superptr_ptnseg_','_ptnseg_'),
        ('superptr_planesize_','_planesize_'),
        ('superptr_ylen_','_ylen_'),
        ('superptr_draw_adr_','_draw_adr_'),
        ('superptr_drawlen_','_drawlen_'),
        ('superptr_shift_','_shift_'),
        ('superput_',''),
        ('superptr_',''),
        ('superpt8_',''),
    ):text=text.replace(original,native)
    if member=='SUPER_ENTRY_BFNT':
        # The original FAR-model _push expands to a segment push.
        # LDATA's typed conditional is the same active native large arm.
        text=text.replace('nopcall','call')
    rows=[re.sub(r'\s+','',line.split(';',1)[0])
          for line in text.splitlines() if line.split(';',1)[0].strip()]
    if member=='SUPER_ENTRY_BFNT':
        need(rows.count('ifldata')==rows.count('endif') or
             rows.count('ifldata')==rows.count('endif')+1,
             'original large-model BFNT conditional malformed')
        rows=[x.replace('_push[','push[').replace('pushwordptr[','push[')
              for x in rows if x not in ('ifldata','endif')]
    return rows


def source_evidence(base):
    archive=stored_lzh(pinned(ROOT,base['inputs']['inner_archive']))
    inventory={row['name']:row for row in base['active_procedure_inventory']}
    frozen={row['name']:row for row in base['frozen_source_closure']}
    results={}
    for member,start,size,upstream_file,old_name,grammar in MEMBERS:
        live=inventory[member]
        need((live['start'],live['end'])==(start,start+size),
             'actual TASM listing has different complete original helper extent')
        filename=live['source']
        need(filename in frozen and upstream_file in archive,
             'original helper source missing from pinned TASM/author archive')
        native=(ROOT/base['candidate_source_root']/filename).read_bytes()
        need(sha(native)==frozen[filename]['sha256'],
             'actual TASM-built native SUPER helper source changed')
        original=archive[upstream_file]
        if grammar=='proc':
            ref=near_proc_blocks(original,'cp932',old_name)
            candidate=near_proc_blocks(native,'utf8',member)
        else:
            ref=[x for x in source_blocks(original,'cp932') if x['name']==old_name]
            candidate=[x for x in source_blocks(native,'utf8') if x['name']==member]
        need(len(ref)==len(candidate)==1 and
             canonical(ref[0]['text'],member)==canonical(candidate[0]['text'],member),
             'complete original author SUPER helper instruction source differs: '+member)
        results[member]={
            'original_author_archive_member':upstream_file,
            'original_source_entry':old_name,
            'native_compiled_source':filename,
            'native_compiled_source_sha256':sha(native),
            'upstream_procedure_sha256':sha(ref[0]['text'].encode('utf8')),
            'native_source_procedure_sha256':sha(candidate[0]['text'].encode('utf8')),
            'canonical_full_source_sha256':sha(
                '\n'.join(canonical(ref[0]['text'],member)).encode('utf8')),
            'native_source_lines':[candidate[0]['start_line'],candidate[0]['end_line']],
            'source_grammar':grammar,
        }
    return results


def replay():
    parent=json.loads(BASE.read_text())
    obj=pinned(ROOT,parent['inputs']['saved_object'])
    need(obj==pinned(ROOT,parent['inputs']['calibration_object']),
         'original OMF not the preserved native TASM source')
    calibration=parse_mz(pinned(ROOT,parent['inputs']['calibration_exe']))
    target=parse_mz(pinned(ROOT,parent['inputs']['target']))
    before,after=startup(calibration),startup(target)
    need((before['dgroup'],after['dgroup'],after['init_start']-before['init_start'])==
         (0x209e0,0x209d0,-18),'original SUPER helper DATA/C0L link shift not anchored')
    sources=source_evidence(parent)
    omf=object_text(obj)
    rows=[]
    for member,start,size,*_ in MEMBERS:
        left,right,object_sha,fixups=code_scope(omf,start,size)
        need(left==calibration.program_image[start:start+size] and
             right==target.program_image[start:start+size],
             'original complete native SUPER helper CODE differs: '+member)
        need(relative_fixups(calibration,start,size)==
             relative_fixups(target,start,size)==[],
             'original Master SUPER helper MZ relocations differ')
        rows.append({
            'member':member,'start':start,'end':start+size,'size':size,
            'source':sources[member],
            'original_object_CODE_sha256':object_sha,
            'calibration_linked_CODE_sha256':sha(left),
            'original_linked_CODE_sha256':sha(right),
            'source_OMF_actions':fixups,'original_ordered_MZ_relocations':[],
            'authored_credit':0,
        })
    return {
        'schema_version':1,'kind':'original-master-super-native-proc-helpers',
        'artifact':'th05-main','members':rows,
        'source_written_CODE_bytes':sum(r['size'] for r in rows),
        'parent_Master_sha256':digest_file(BASE),
        'calibration_exe_sha256':parent['inputs']['calibration_exe']['sha256'],
        'original_target_sha256':parent['inputs']['target']['sha256'],
        'source_OMF_sha256':parent['inputs']['saved_object']['sha256'],
        'author_archive_sha256':parent['inputs']['inner_archive']['sha256'],
        'source_verifier_sha256':digest_file(ROOT/'scripts/review_master_super_helpers.py'),
        'linked_verifier_sha256':digest_file(ROOT/'scripts/review_master_super.py'),
        'authored_credit':0,'non_CODE_bytes_claimed':0,
    }


def validate_public(proof):
    parent=json.loads(BASE.read_text())
    need(proof.get('schema_version')==1 and
         proof.get('kind')=='original-master-super-native-proc-helpers' and
         proof.get('artifact')=='th05-main' and
         proof.get('source_written_CODE_bytes')==sum(z[2] for z in MEMBERS) and
         proof.get('parent_Master_sha256')==digest_file(BASE) and
         proof.get('calibration_exe_sha256')==parent['inputs']['calibration_exe']['sha256'] and
         proof.get('original_target_sha256')==parent['inputs']['target']['sha256'] and
         proof.get('source_OMF_sha256')==parent['inputs']['saved_object']['sha256'] and
         proof.get('author_archive_sha256')==parent['inputs']['inner_archive']['sha256'] and
         proof.get('source_verifier_sha256')==digest_file(ROOT/'scripts/review_master_super_helpers.py') and
         proof.get('linked_verifier_sha256')==digest_file(ROOT/'scripts/review_master_super.py') and
         proof.get('authored_credit')==proof.get('non_CODE_bytes_claimed')==0,
         'original SUPER helper source or verified inputs changed')
    rows=proof.get('members')
    need(isinstance(rows,list) and
         [(r.get('member'),r.get('start'),r.get('size')) for r in rows]==
         [(name,start,size) for name,start,size,*_ in MEMBERS],
         'SUPER native helper source extents incomplete or unexpected')
    for r in rows:
        need(r.get('end')==r['start']+r['size'] and
             r.get('authored_credit')==0 and
             r.get('original_ordered_MZ_relocations')==[] and
             isinstance(r.get('source_OMF_actions'),list),
             'unverified original helper extent or relocations')
        for key in ('original_object_CODE_sha256','calibration_linked_CODE_sha256',
                    'original_linked_CODE_sha256'):
            need(isinstance(r.get(key),str) and re.fullmatch('[0-9a-f]{64}',r[key]),
                 'source-linked helper CODE digest invalid')
    if DECISION.exists():
        d=json.loads(DECISION.read_text())
        need(d.get('schema_version')==1 and d.get('artifact')=='th05-main' and
             d.get('decision')=='ADOPT_ONLY_ORIGINAL_MASTER_SUPER_HELPERS' and
             d.get('evidence_sha256')==digest_file(PROOF) and
             d.get('members')==[x[0] for x in MEMBERS] and
             d.get('CODE_bytes')==proof['source_written_CODE_bytes'] and
             d.get('authored_credit')==d.get('other_bytes_claimed')==0,
             'explicit native SUPER helper source review selection changed')


def reviewed_claims(root,view,*,verify_targets=False):
    if not DECISION.exists():return [],None
    need(root.resolve()==ROOT.resolve(),'wrong source checkout for original SUPER')
    record=json.loads(PROOF.read_text());validate_public(record)
    need(view['sha256']==json.loads(BASE.read_text())['target_payload_sha256'],
         'source-linked SUPER belongs to another original target')
    if verify_targets:need(replay()==record,'actual source/OMF native SUPER helpers drifted')
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
             'refusing to overwrite original SUPER helper source review')
        record=replay()
        PROOF.write_text(json.dumps(record,indent=2)+'\n')
        print('PASS original complete Master SUPER helper CODE',record['source_written_CODE_bytes'])
    else:
        record=json.loads(PROOF.read_text());validate_public(record)
        if args.check:
            need(replay()==record,'original SUPER helper source/OMF/target mismatches')
            print('PASS original native SUPER source PROC and complete CODE')
        else:
            print('PASS public original SUPER helper proof')


if __name__=='__main__':main()
