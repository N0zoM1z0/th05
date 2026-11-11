#!/usr/bin/env python3
"""Two complete TH05 Master/ZUN no-Y-clip packed-pixel blitters.

The actual GAME=5 TASM source is exactly the author's Master 0.23
GRAPH_PACK_PUT_8 minus the three Y-clip instructions, with local-name changes.
Both original decoded scopes must relink from real OMF LEDATA and FIXUPP.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re

from lib.pc98 import digest_file, parse_mz
from lib.unit_context import UnitContext, load_unit_target
from lib.unit_oracle import relative_fixups
from review_master import pinned, need, sha, stored_lzh, source_blocks
from review_master_grcg import symbolic_source
from review_context_master_large import ROOT, MASTER, real_omf, native_map, whole_source, rebind

PROOF = ROOT / 'config/context_graph_pack_noclip.json'
DECISION = ROOT / 'config/reviewed_context_graph_pack_noclip.json'
ORIG_ARCHIVE = 'GRPPPUT8.ASM'
ORIG_PROC = 'GRAPH_PACK_PUT_8'
NATIVE_PROC = 'GRAPH_PACK_PUT_8_NOCLIP'
NATIVE_SOURCE = 'libs/master.lib/graph_pack_put_8_noclip.asm'
SCOPE = {'op': (0x35b0, 196), 'maine': (0x3778, 196)}
ORIGINAL_REMOVED = ('subax,clipyt', 'cmpax,clipyh', 'jashortclipout')


def original_derivative(archive, native_source):
    originals = [b for b in source_blocks(archive[ORIG_ARCHIVE], 'cp932')
                 if b['name'] == ORIG_PROC]
    products = [b for b in source_blocks(native_source, 'utf8')
                if b['name'] == NATIVE_PROC]
    need(len(originals) == len(products) == 1,
         'complete original/derived Master blitter procedure absent')
    old = symbolic_source(originals[0]['text'])
    need(all(old.count(line) == 1 for line in ORIGINAL_REMOVED),
         'original unique Y clipping instruction sequence changed')
    need(old.index(ORIGINAL_REMOVED[1]) == old.index(ORIGINAL_REMOVED[0])+1 and
         old.index(ORIGINAL_REMOVED[2]) == old.index(ORIGINAL_REMOVED[1])+1,
         'removed Y clipping guards are not one original contiguous block')
    product = [line.replace('graph_pack_put_8', 'graph_pack_put_8_noclip')
                   .replace('clipout', 'grppp8nc_clipout')
               for line in old if line not in ORIGINAL_REMOVED]
    actual = symbolic_source(products[0]['text'])
    need(product == actual and len(actual) >= 100,
         'modified procedure contains changes beyond original three Y-clip instructions and names')
    return {'author_block_sha256':sha(originals[0]['text'].encode('utf8')),
            'native_block_sha256':sha(products[0]['text'].encode('utf8')),
            'derived_canonical_sha256':sha('\n'.join(product).encode('utf8')),
            'canonical_lines':len(actual),
            'actual_modification':'remove three contiguous Y-clip instructions; rename procedure and exit label'}


def replay():
    parent=json.loads(MASTER.read_text())
    archive=stored_lzh(pinned(ROOT,parent['inputs']['inner_archive']))
    rows=[];original_views={}
    for art, (start,size) in SCOPE.items():
        base=ROOT/f'.analysis/builds/{art}-calibration-a/source'
        module='op' if art=='op' else 'mainem'
        obj=(base/f'obj/th05/{module}.obj').read_bytes()
        segments,blocks,fixups,groups=real_omf(obj)
        map_data,offsets,public=native_map(art,'th05_op.asm' if art=='op' else 'th05_maine_master.asm',segments)
        need(public.get(NATIVE_PROC)=={start},'actual complete blitter MAP public changed')
        native_source=(base/NATIVE_SOURCE).read_bytes()
        source_proof=original_derivative(archive,native_source)
        context=UnitContext(ROOT,art)
        native=load_unit_target(context,context.config())[1]
        original_views[art]=sha(native.program_image)
        cal=parse_mz((base/f'bin/th05/{art}.exe').read_bytes())
        cg=int.from_bytes(cal.program_image[1:3],'little')
        og=int.from_bytes(native.program_image[1:3],'little')
        need(og-cg==(1 if art=='maine' else 0),'original CTR group mismatch')
        code=whole_source(blocks,start,size)
        actions=[f for f in fixups if start<=f['site']<start+size]
        calcode,nativecode,rebased,mz=rebind(code,actions,start,offsets,segments,groups,cg,og)
        observed=native.program_image[start:start+size]
        need(calcode==cal.program_image[start:start+size] and nativecode==observed,
             'whole native blitter CODE differs from original two image producers')
        need(mz==relative_fixups(cal,start,size)==relative_fixups(native,start,size),
             'original ordered MZ relocation sequence differs')
        need(native.program_image.find(observed)==start and
             native.program_image.find(observed,start+1)==-1,
             'full original blitter CODE does not occur uniquely')
        rows.append({'artifact':'th05-'+art,'member':NATIVE_PROC,
                     'start':start,'end':start+size,'size':size,
                     'source':NATIVE_SOURCE,'archive_source':ORIG_ARCHIVE,
                     'native_source_sha256':sha(native_source),
                     'native_OMF_sha256':sha(obj),'native_MAP_sha256':sha(map_data),
                     **source_proof,
                     'unlinked_CODE_sha256':sha(code),'calibrated_CODE_sha256':sha(calcode),
                     'native_CODE_sha256':sha(nativecode),'ordered_OMF_actions':rebased,
                     'original_ordered_MZ':mz,'authored_credit':0})
    return {'schema_version':1,'kind':'master-derived-no-Y-clip-packed-blitter-original-source-linked',
            'scopes':rows,'CODE_bytes':sum(r['size'] for r in rows),
            'original_view_sha256':original_views,
            'author_archive_sha256':parent['inputs']['inner_archive']['sha256'],
            'master_parent_sha256':digest_file(MASTER),
            'verifier_sha256':digest_file(ROOT/'scripts/review_context_graph_pack_noclip.py'),
            'authored_credit':0,'non_CODE_claimed':0}


def validate(proof):
    parent=json.loads(MASTER.read_text())
    need(proof.get('schema_version')==1 and
         proof.get('kind')=='master-derived-no-Y-clip-packed-blitter-original-source-linked' and
         proof.get('CODE_bytes')==392 and
         proof.get('author_archive_sha256')==parent['inputs']['inner_archive']['sha256'] and
         proof.get('master_parent_sha256')==digest_file(MASTER) and
         proof.get('verifier_sha256')==digest_file(ROOT/'scripts/review_context_graph_pack_noclip.py') and
         proof.get('authored_credit')==proof.get('non_CODE_claimed')==0,
         'original Master derivative source/verifier identity changed')
    rows=proof.get('scopes',[])
    need([(x.get('artifact'),x.get('member'),x.get('start'),x.get('size')) for x in rows]==
         [('th05-'+a,NATIVE_PROC,*v) for a,v in SCOPE.items()],
         'whole original no-clip blitter scope list changed')
    views=proof.get('original_view_sha256')
    need(isinstance(views,dict) and set(views)==set(SCOPE) and
         all(isinstance(x,str) and re.fullmatch('[0-9a-f]{64}',x) for x in views.values()),
         'original decoded view identities missing')
    for x in rows:
        need(x.get('end')==x['start']+x['size'] and x.get('authored_credit')==0 and
             x.get('source')==NATIVE_SOURCE and x.get('archive_source')==ORIG_ARCHIVE and
             x.get('canonical_lines')>=100 and
             x.get('actual_modification')==
             'remove three contiguous Y-clip instructions; rename procedure and exit label' and
             x.get('original_ordered_MZ')==
             [f['site'] for f in x['ordered_OMF_actions'] if f['kind']==2],
             'complete procedure source transform or original ordered fixups changed')
        for field in ('native_source_sha256','native_OMF_sha256','native_MAP_sha256',
                      'author_block_sha256','native_block_sha256','derived_canonical_sha256',
                      'unlinked_CODE_sha256','calibrated_CODE_sha256','native_CODE_sha256'):
            need(isinstance(x.get(field),str) and re.fullmatch('[0-9a-f]{64}',x[field]),
                 'missing original source/OMF/code evidence SHA-256')
    if DECISION.exists():
        d=json.loads(DECISION.read_text())
        need(d.get('schema_version')==1 and d.get('decision')=='ADOPT_TWO_MASTER_DERIVED_NOCLIP_CODE' and
             d.get('evidence_sha256')==digest_file(PROOF) and
             d.get('scopes')==[[x['artifact'],x['member']] for x in rows] and
             d.get('CODE_bytes')==392 and d.get('authored_credit')==d.get('other_claims')==0,
             'explicit original Master derivative adoption stale')


def reviewed_claims(root,artifact,view,*,verify_targets=False):
    if not DECISION.exists():return [],None
    need(root.resolve()==ROOT.resolve(),'wrong checked-out source tree')
    p=json.loads(PROOF.read_text());validate(p)
    need(p['original_view_sha256'][artifact]==view['sha256'],'original decoded target view changed')
    if verify_targets:need(replay()==p,'real native TASM original blitter changed')
    rows=[r for r in p['scopes'] if r['artifact']=='th05-'+artifact]
    return ([{'start':r['start'],'end':r['end'],'kind':'verified-vendor-code',
              'library':'Master 0.23/ZUN-derived packed graphics',
              'member':r['member'],'authored_credit':0} for r in rows],digest_file(DECISION))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write',action='store_true')
    mode.add_argument('--check',action='store_true')
    mode.add_argument('--structural-check',action='store_true')
    args=parser.parse_args()
    if args.write:
        need(not PROOF.exists() and not DECISION.exists(),'do not overwrite native original proof')
        proof=replay();PROOF.write_text(json.dumps(proof,indent=2)+'\n')
        print('PASS original Master/ZUN derivative CODE',proof['CODE_bytes'])
    else:
        proof=json.loads(PROOF.read_text());validate(proof)
        if args.check:
            need(replay()==proof,'full source-linked native original blitter differs')
            print('PASS exact native original GRAPH_PACK_PUT_8_NOCLIP in OP and MAINE')
        else:print('PASS original source-derivative structural proof')

if __name__=='__main__':main()
