#!/usr/bin/env python3
"""Source-linked original Master BGM timer/PSG procedures in OP and MAINE.

Seven complete original source procedures per decoded artifact, including the
280-byte timer interrupt hook. Only the original TASM OMF writes/fixups and
pinned author-archive source are accepted. No cold replay or inferred bytes.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

from lib.pc98 import digest_file, parse_mz
from lib.unit_context import UnitContext,load_unit_target
from lib.unit_oracle import relative_fixups
from review_master import pinned,need,sha,stored_lzh,source_blocks
from review_master_grcg import symbolic_source
from review_context_master_large import ROOT,MASTER,real_omf,native_map,whole_source,rebind

PROOF=ROOT/'config/context_bgm_timers.json'
DECISION=ROOT/'config/reviewed_context_bgm_timers.json'
# These are full native MAP public boundaries, not selected byte-match slices.
# Every source corresponds to a complete PROC/FUNC in the original archive.
SCOPES=(
    ('_BGM_BELL_ORG','bgm_bell_org.asm','B_B_ORG.ASM',0x2cd0,88,1),
    ('_BGM_TIMER_INIT','bgm_timer.asm','B_TIMER.ASM',0x2f92,68,9),
    ('_BGM_TIMER_FINISH','bgm_timer.asm','B_TIMER.ASM',0x2fd6,42,4),
    ('_BGM_PINIT','bgm_pinit.asm','B_PINIT.ASM',0x3000,62,2),
    ('_BGM_TIMERHOOK','bgm_timerhook.asm','B_TMHOOK.ASM',0x303e,280,21),
    ('BGM_STOP_PLAY','bgm_stop_play.asm','B_SP_PLY.ASM',0x3346,26,2),
    ('BGM_SET_TEMPO','bgm_set_tempo.asm','B_S_TEMP.ASM',0x3360,46,4),
)
OFFSETS={'op':0,'maine':0x1c8}
NOPCALLS={
    '_BGM_TIMER_INIT':('calldos_setvect',),
    '_BGM_TIMER_FINISH':('calldos_setvect',),
    '_BGM_TIMERHOOK':('call_bgm_play','call_bgm_bell_org','call_bgm_effect_sound','call_bgm_bell_org'),
    'BGM_STOP_PLAY':('call_bgm_bell_org',),
}


def derived_source(original,live,name):
    old=symbolic_source(original)
    actual=symbolic_source(live)
    if name=='_BGM_PINIT':
        mapped=('[bx].mbuf','[bx].pptr','[bx].oct','[bx].note',
                '[bx].dflen','[bx].len','[bx].lcnt','[bx].tnt')
        for i,source in enumerate(mapped):
            need(any(source in x for x in old),
                 'original Master PSG field missing: '+source)
        expected=[x.replace('[bx].','[bx].spart.') for x in old]
    elif name=='_BGM_BELL_ORG':
        need(old.count('pc98:')==1 and old.count('jnzshortpcat')==1 and
             old.count('jnzshortclock8mhz')==1,
             'original 98/AT PSG bell split changed')
        expected=[x.replace('jnzshortpcat','jnzshortb_b_org_pcat')
                  .replace('jnzshortclock8mhz','jnzshortb_b_org_clock8mhz')
                  .replace('clock8mhz:','b_b_org_clock8mhz:')
                  .replace('pcat:','b_b_org_pcat:')
                  for x in old if x!='pc98:']
    else:
        expected=list(old)
    # The real native TASM source explicitly marks near relaxation for
    # selected original far CALLs. Restrict each insertion by exact opcode
    # spelling and occurrence count; no semantic instruction is removed.
    counts={}
    for operation in NOPCALLS.get(name,()):
        counts[operation]=counts.get(operation,0)+1
    for operation,count in counts.items():
        need(expected.count(operation)==count,'original Master CALL location changed')
    expected=['nop'+x if x in counts else x for x in expected]
    need(expected==actual and len(expected)>=10,
         'Master BGM source body differs outside explicit call/field/label adaptations: '+name)
    return sha('\n'.join(actual).encode('utf8'))


def linked_unit(raw,fixups,start,size,offsets,segments,groups,cg,og,artifact,name):
    # The authentic TIMER_INIT OBJ contains one segment16 FIXUPP to its own
    # CODE SEGDEF (_TEXT), not to DGROUP. Original and calibration frame are
    # zero, but this *is* a genuine ordered MZ relocation at +19. The shared
    # generic Master binder accepts DGROUP segment16 only; validate this
    # second real kind directly rather than rewriting the OMF source.
    special=[f for f in fixups if f['kind']==2 and f['target_method']==0]
    if name=='_BGM_TIMER_INIT':
        need(len(special)==1 and special[0]['site']==start+19 and
             special[0]['frame_method']==5 and special[0]['target_index']==1 and
             special[0]['displacement']==0 and not special[0]['relative'] and
             segments[1][0]=='_TEXT' and offsets['_TEXT']['start']==0x272 and
             raw[19:21]==b'\0\0',
             'the actual original TASM CODE-segment relocation is not as reviewed')
    else:
        need(not special,'unexpected non-DGROUP original MZ segment relocation')
    ordinary=[f for f in fixups if f not in special]
    cal,native,actions,mz=rebind(raw,ordinary,start,offsets,segments,groups,cg,og)
    if special:
        need(cal[19:21]==native[19:21]==b'\0\0',
             'original relocatable CODE segment word is not zero')
        mz=[19]
        # Preserve actual OMF site/order; do not silently discard the action.
        actions.append({**special[0], 'site':19, 'binding':'original_TEXT_segment16_zero_frame',
                        'calibrated_word_sha256':sha(b'\0\0'),
                        'native_word_sha256':sha(b'\0\0')})
    return cal,native,actions,mz


def replay():
    parent=json.loads(MASTER.read_text())
    archive=stored_lzh(pinned(ROOT,parent['inputs']['inner_archive']))
    results=[];original_views={}
    for art,shift in OFFSETS.items():
        root=ROOT/f'.analysis/builds/{art}-calibration-a/source'
        module='op' if art=='op' else 'mainem'
        obj=(root/f'obj/th05/{module}.obj').read_bytes()
        segments,blocks,fixups,groups=real_omf(obj)
        map_data,offsets,public=native_map(art,'th05_op.asm' if art=='op' else 'th05_maine_master.asm',segments)
        context=UnitContext(ROOT,art)
        original=load_unit_target(context,context.config())[1]
        original_views[art]=sha(original.program_image)
        cal=parse_mz((root/f'bin/th05/{art}.exe').read_bytes())
        cg=int.from_bytes(cal.program_image[1:3],'little')
        og=int.from_bytes(original.program_image[1:3],'little')
        need(og-cg==(0 if art=='op' else 1),'native original BGM CRT/DGROUP frame differs')
        for name,filename,origfile,op_start,size,count in SCOPES:
            start=op_start+shift
            need(public.get(name)=={start},'original BGM complete public entry changed: '+name)
            sourcepath=root/'libs/master.lib'/filename
            rawsource=sourcepath.read_bytes()
            live=[b for b in source_blocks(rawsource,'utf8') if b['name']==name]
            author=[b for b in source_blocks(archive[origfile],'cp932') if b['name']==name]
            need(len(live)==len(author)==1,'complete original BGM authored PROC missing: '+name)
            canonical=derived_source(author[0]['text'],live[0]['text'],name)
            raw=whole_source(blocks,start,size)
            ordered=[f for f in fixups if start<=f['site']<start+size]
            need(len(ordered)==count,'real original BGM CODE FIXUPP count differs: '+name)
            ca,native,rebased,mz=linked_unit(raw,ordered,start,size,offsets,segments,groups,cg,og,art,name)
            observed=original.program_image[start:start+size]
            need(ca==cal.program_image[start:start+size] and native==observed,
                 'complete original Master BGM function CODE differs: '+art+':'+name)
            need(mz==relative_fixups(cal,start,size)==relative_fixups(original,start,size),
                 'original MZ relocation sites/order differ: '+art+':'+name)
            need(original.program_image.find(observed)==start and
                 original.program_image.find(observed,start+1)==-1,
                 'complete original BGM procedure not uniquely located: '+name)
            results.append({'artifact':'th05-'+art,'member':name,'start':start,
                            'end':start+size,'size':size,'source':'libs/master.lib/'+filename,
                            'original_archive_member':origfile,
                            'source_adaptation':'NOPCALL/typed-PSG-field/private-label only',
                            'original_block_sha256':sha(author[0]['text'].encode('utf8')),
                            'native_block_sha256':sha(live[0]['text'].encode('utf8')),
                            'canonical_source_sha256':canonical,
                            'actual_source_sha256':sha(rawsource),
                            'native_OMF_sha256':sha(obj),'native_MAP_sha256':sha(map_data),
                            'unlinked_CODE_sha256':sha(raw),
                            'calibrated_CODE_sha256':sha(ca),
                            'native_CODE_sha256':sha(native),
                            'ordered_OMF_actions':rebased,'ordered_MZ':mz,
                            'authored_credit':0})
    return {'schema_version':1,'kind':'original-OP-MAINE-BGM-source-linked-timer-and-PSG',
            'scopes':results,'source_written_CODE_bytes':sum(r['size'] for r in results),
            'original_view_sha256':original_views,
            'original_archive_sha256':parent['inputs']['inner_archive']['sha256'],
            'master_parent_sha256':digest_file(MASTER),
            'verifier_sha256':digest_file(ROOT/'scripts/review_context_bgm_timers.py'),
            'authored_credit':0,'non_CODE_claimed':0}


def validate(record):
    master=json.loads(MASTER.read_text())
    expect=[('th05-'+art,n,st+shift,sz) for art,shift in OFFSETS.items()
            for n,_,_,st,sz,_ in SCOPES]
    need(record.get('schema_version')==1 and
         record.get('kind')=='original-OP-MAINE-BGM-source-linked-timer-and-PSG' and
         record.get('source_written_CODE_bytes')==sum(r[3] for r in expect) and
         record.get('original_archive_sha256')==master['inputs']['inner_archive']['sha256'] and
         record.get('master_parent_sha256')==digest_file(MASTER) and
         record.get('verifier_sha256')==digest_file(ROOT/'scripts/review_context_bgm_timers.py') and
         record.get('authored_credit')==record.get('non_CODE_claimed')==0,
         'native original Master BGM proof/verifier identity changed')
    rows=record.get('scopes',[])
    need([(r.get('artifact'),r.get('member'),r.get('start'),r.get('size')) for r in rows]==expect,
         'original BGM source procedure bounds or list changed')
    v=record.get('original_view_sha256',{})
    need(set(v)==set(OFFSETS) and all(re.fullmatch('[0-9a-f]{64}',x) for x in v.values()),
         'original OP/MAINE target view identities missing')
    for r in rows:
        meta=next((entry for entry in SCOPES if entry[0]==r['member']),None)
        need(meta is not None and r.get('source')=='libs/master.lib/'+meta[1] and
             r.get('original_archive_member')==meta[2] and
             r.get('source_adaptation')=='NOPCALL/typed-PSG-field/private-label only' and
             r.get('end')==r['start']+r['size'] and r.get('authored_credit')==0 and
             len(r.get('ordered_OMF_actions',[]))==meta[5] and
             r.get('ordered_MZ')==[f['site'] for f in r['ordered_OMF_actions'] if f['kind']==2],
             'incomplete source code/unique Master BGM fixup record')
        for field in ('original_block_sha256','native_block_sha256','canonical_source_sha256',
                      'actual_source_sha256','native_OMF_sha256','native_MAP_sha256',
                      'unlinked_CODE_sha256','calibrated_CODE_sha256','native_CODE_sha256'):
            need(isinstance(r.get(field),str) and re.fullmatch('[0-9a-f]{64}',r[field]),
                 'original Master source or actual linked CODE SHA is missing')
    if DECISION.exists():
        decision=json.loads(DECISION.read_text())
        need(decision.get('schema_version')==1 and
             decision.get('decision')=='ADOPT_ONLY_COMPLETE_ORIGINAL_BGM_TIMER_CODE' and
             decision.get('evidence_sha256')==digest_file(PROOF) and
             decision.get('scopes')==[[r['artifact'],r['member']] for r in rows] and
             decision.get('CODE_bytes')==record['source_written_CODE_bytes'] and
             decision.get('authored_credit')==decision.get('other_claims')==0,
             'explicit original BGM timer source adoption is stale')


def reviewed_claims(root,artifact,view,*,verify_targets=False):
    if not DECISION.exists():return [],None
    need(root.resolve()==ROOT.resolve(),'wrong checked out reconstructed source tree')
    proof=json.loads(PROOF.read_text());validate(proof)
    need(proof['original_view_sha256'][artifact]==view['sha256'],
         'wrong original OP/MAINE decoded source image')
    if verify_targets:need(replay()==proof,'source-linked original BGM code no longer matches')
    return ([{'start':r['start'],'end':r['end'],'kind':'verified-vendor-code',
              'library':'original Master 0.23 BGM','member':r['member'],'authored_credit':0}
             for r in proof['scopes'] if r['artifact']=='th05-'+artifact],digest_file(DECISION))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write',action='store_true')
    mode.add_argument('--check',action='store_true')
    mode.add_argument('--structural-check',action='store_true')
    args=parser.parse_args()
    if args.write:
        need(not PROOF.exists() and not DECISION.exists(),'cannot overwrite accepted BGM proof')
        proof=replay();PROOF.write_text(json.dumps(proof,indent=2)+'\n')
        print('PASS original complete Master BGM CODE',proof['source_written_CODE_bytes'])
    else:
        proof=json.loads(PROOF.read_text());validate(proof)
        if args.check:
            need(replay()==proof,'complete native original BGM CODE differs')
            print('PASS exact original BGM timers and PSG producers/fixups')
        else:print('PASS BGM timer original source structural proof')

if __name__=='__main__':main()
