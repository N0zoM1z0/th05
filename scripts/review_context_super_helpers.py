#!/usr/bin/env python3
"""OP/MAINE original Master SUPER_RECT, exit and 3 near helper procedures.

These are real preserved author PROC/ENDP bodies, not arbitrary slices of the
public-map SUPER_PUT extent. All scope bytes come from the genuine TASM OMF
and must equal complete original and calibrated functions with ordered fixups.
The separate assembler EVEN alignment bytes remain unclaimed.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import tomllib

from lib.pc98 import digest_file,parse_mz
from lib.unit_context import UnitContext,load_unit_target
from lib.unit_oracle import relative_fixups
from review_master import need,pinned,sha,stored_lzh,source_blocks
from review_master_super import source_lines as super_lines
from review_master_super_helpers import near_proc_blocks,canonical
from review_context_master_large import ROOT,MASTER,real_omf,native_map,whole_source,rebind

PROOF=ROOT/'config/context_super_helpers.json'
DECISION=ROOT/'config/reviewed_context_super_helpers.json'
# Function-relative entry point to the two independent native parent sources.
RECT=(
 ('SUPERPTR_EXIT',-6,6,'SUPERPTR.ASM','EXIT','func'),
 ('SUPER_PUT_RECT',0,318,'SUPERPTR.ASM','SUPER_PUT_RECT','func'),
 ('superptr_draw_shift',318,70,'SUPERPTR.ASM','draw_shift','proc'),
 ('superptr_draw_noshift',388,48,'SUPERPTR.ASM','draw_noshift','proc'),
 ('superptr_draw',436,63,'SUPERPTR.ASM','draw','proc'),
)
ART={'op':(0x2736,0x292a),'maine':(0x2974,0x2b68)}
TOTAL=sum(s for _,_,s,*_ in RECT)*len(ART)


def scoped_source(raw,name,grammar):
    if grammar=='proc':
        return near_proc_blocks(raw,'utf8',name)
    return [r for r in source_blocks(raw,'utf8') if r['name']==name]


def source_identity(archive,artifact,func,orig_file,original_entry,grammar):
    root=ROOT/f'.analysis/builds/{artifact}-calibration-a/source/libs/master.lib'
    source_name='super_put_rect.asm' if orig_file=='SUPERPTR.ASM' else 'super_put.asm'
    content=(root/source_name).read_bytes()
    # The original Master author language is preserved in a separate
    # unmodified archive. No actual CODE instructions are replaced.
    original=archive[orig_file]
    if grammar=='proc':
        reference=near_proc_blocks(original,'cp932',original_entry)
        compiled=near_proc_blocks(content,'utf8',func)
    else:
        reference=[r for r in source_blocks(original,'cp932') if r['name']==original_entry]
        compiled=[r for r in source_blocks(content,'utf8') if r['name']==func]
    need(len(reference)==len(compiled)==1,'original Master helper source procedure absent')
    if func=='SUPER_PUT_RECT':
        a=super_lines(reference[0]['text'])
        b=super_lines(compiled[0]['text'])
    else:
        a=canonical(reference[0]['text'],func)
        b=canonical(compiled[0]['text'],func)
    need(a==b,'original Master helper opcode/operand differs: '+func)
    return {'original_archive_member':orig_file,
            'original_procedure_name':original_entry,
            'native_compiled_source':'libs/master.lib/'+source_name,
            'native_compiled_source_sha256':sha(content),
            'author_procedure_sha256':sha(reference[0]['text'].encode('utf8')),
            'native_procedure_sha256':sha(compiled[0]['text'].encode('utf8')),
            'canonical_full_source_sha256':sha('\n'.join(a).encode('utf8')),
            'original_language':'real TASM PROC/ENDP or FUNC'}


def replay():
    master=json.loads(MASTER.read_text())
    archive=stored_lzh(pinned(ROOT,master['inputs']['inner_archive']))
    result=[]
    for art,(rect,put) in ART.items():
        base=ROOT/f'.analysis/builds/{art}-calibration-a/source'
        module='op' if art=='op' else 'mainem'
        obj=(base/f'obj/th05/{module}.obj').read_bytes()
        segs,blocks,fixups,groups=real_omf(obj)
        map_raw,offsets,public=native_map(art,'th05_op.asm' if art=='op' else 'th05_maine_master.asm',segs)
        original=load_unit_target(UnitContext(ROOT,art),UnitContext(ROOT,art).config())[1]
        calibration=parse_mz((base/f'bin/th05/{art}.exe').read_bytes())
        cg=int.from_bytes(calibration.program_image[1:3],'little')
        og=int.from_bytes(original.program_image[1:3],'little')
        need(og-cg==(1 if art=='maine' else 0),
             'native CRT DGROUP location differs from actual original')
        need(public.get('SUPER_PUT_RECT')=={rect} and
             public.get('SUPER_PUT')=={put},
             'original full Master SUPER parent public entry drifted')
        for name,relative,size,file,old,grammar in [
            (n,rect+rel,sz,f,o,g) for n,rel,sz,f,o,g in RECT]:
            st=relative
            source=whole_source(blocks,st,size)
            actions=[f for f in fixups if st<=f['site']<st+size]
            native_cal,native_original,writes,mz=rebind(
                source,actions,st,offsets,segs,groups,cg,og)
            need(native_cal==calibration.program_image[st:st+size] and
                 native_original==original.program_image[st:st+size],
                 'source-linked entire original helper CODE differs: '+name)
            need(mz==relative_fixups(calibration,st,size)==
                 relative_fixups(original,st,size)==[],
                 'original SUPER helper ordered MZ fixups changed')
            identity=source_identity(archive,art,name,file,old,grammar)
            result.append({'artifact':'th05-'+art,'member':name,'start':st,
                           'end':st+size,'size':size,'source':identity,
                           'native_OMF_sha256':sha(obj),
                           'native_MAP_sha256':sha(map_raw),
                           'source_unlinked_CODE_sha256':sha(source),
                           'calibrated_CODE_sha256':sha(native_cal),
                           'original_CODE_sha256':sha(native_original),
                           'ordered_original_MZ':mz,'original_OMF_FIXUPP':writes,
                           'authored_credit':0})
        # The assembler's standalone EVEN bytes between procedure bodies do
        # not enter the proof, despite being located within the native _TEXT.
        for pad in (rect+499,):
            need(original.program_image[pad:pad+1] and
                 calibration.program_image[pad:pad+1] and
                 all(not(r['start']<=pad<r['end']) for r in result
                     if r['artifact']=='th05-'+art),
                 'review accidentally adopted an original EVEN alignment byte')
    return {'schema_version':1,'kind':'original-Master-OP-MAINE-SUPER-helper-PROC-CODE',
            'scopes':result,'source_written_CODE_bytes':sum(x['size'] for x in result),
            'upstream_Master_archive_sha256':master['inputs']['inner_archive']['sha256'],
            'parent_native_proof_sha256':digest_file(MASTER),
            'source_relink_verifier_sha256':digest_file(ROOT/'scripts/review_context_master_large.py'),
            'verifier_sha256':digest_file(ROOT/'scripts/review_context_super_helpers.py'),
            'authored_credit':0,'other_bytes_claimed':0}


def validate_public(j):
    parent=json.loads(MASTER.read_text())
    expected=[('th05-'+art,n,rect+off,sz) for art,(rect,put) in ART.items()
              for n,off,sz,*_ in RECT]
    need(j.get('schema_version')==1 and
         j.get('kind')=='original-Master-OP-MAINE-SUPER-helper-PROC-CODE' and
         j.get('source_written_CODE_bytes')==TOTAL and
         j.get('upstream_Master_archive_sha256')==parent['inputs']['inner_archive']['sha256'] and
         j.get('parent_native_proof_sha256')==digest_file(MASTER) and
         j.get('source_relink_verifier_sha256')==digest_file(ROOT/'scripts/review_context_master_large.py') and
         j.get('verifier_sha256')==digest_file(ROOT/'scripts/review_context_super_helpers.py') and
         j.get('authored_credit')==j.get('other_bytes_claimed')==0,
         'unreviewed actual original Master helper inputs or source identity')
    rows=j.get('scopes')
    need(isinstance(rows,list) and
         [(x.get('artifact'),x.get('member'),x.get('start'),x.get('size'))
          for x in rows]==expected,
         'unknown/partial original Master SUPER helper extent')
    for x in rows:
        need(x.get('end')==x['start']+x['size'] and x.get('authored_credit')==0 and
             x.get('ordered_original_MZ')==[] and
             isinstance(x.get('original_OMF_FIXUPP'),list),
             'invalid or partial original source helper record')
        for key in ('native_OMF_sha256','native_MAP_sha256',
                    'source_unlinked_CODE_sha256','calibrated_CODE_sha256','original_CODE_sha256'):
            need(isinstance(x.get(key),str) and re.fullmatch('[0-9a-f]{64}',x[key]),
                 'original source helper CODE digest missing')
    if DECISION.exists():
        d=json.loads(DECISION.read_text())
        need(d.get('schema_version')==1 and
             d.get('decision')=='ADOPT_ONLY_COMPLETE_ORIGINAL_SUPER_HELPERS' and
             d.get('evidence_sha256')==digest_file(PROOF) and
             d.get('members')==[[x['artifact'],x['member']] for x in rows] and
             d.get('CODE_bytes')==j['source_written_CODE_bytes'] and
             d.get('authored_credit')==d.get('other_bytes_claimed')==0,
             'stale explicit original source helper adoption')


def reviewed_claims(root,art,view,*,verify_targets=False):
    if art not in ART or not DECISION.exists():return [],None
    need(root.resolve()==ROOT.resolve(),'wrong native source checkout')
    record=json.loads(PROOF.read_text());validate_public(record)
    allowed=tomllib.loads((ROOT/'config/ownership.toml').read_text())['views']
    need(view['sha256']==allowed[art]['sha256'],
         'native original target identity mismatch')
    if verify_targets:need(replay()==record,'real original source helper OMF mismatch')
    return ([{'start':r['start'],'end':r['end'],
              'kind':'verified-vendor-code','library':'master.lib 0.23',
              'member':r['member'],'authored_credit':0}
             for r in record['scopes'] if r['artifact']=='th05-'+art],
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
             'refusing to overwrite original Master helper proof')
        result=replay()
        PROOF.write_text(json.dumps(result,indent=2)+'\n')
        print('PASS: full source-linked OP/MAINE SUPER helpers',result['source_written_CODE_bytes'])
    else:
        record=json.loads(PROOF.read_text());validate_public(record)
        if args.check:
            need(replay()==record,'actual original Master helper source/OMF differs')
            print('PASS: all complete source/OMF/MZ OP+MAINE SUPER helper functions')
        else:print('PASS: original Master SUPER helper evidence current')


if __name__=='__main__':main()
