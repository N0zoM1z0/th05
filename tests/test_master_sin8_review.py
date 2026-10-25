"""SIN8 vendor DATA stays complete, literal, position-aware and proposal-only."""
import json
from pathlib import Path
import shutil
import struct
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import review_master_sin8 as review


def record(kind,data):
    raw=bytes([kind])+struct.pack('<H',len(data)+1)+data
    return raw+bytes([-sum(raw)&255])


def source(*,rows=40,cos_row=8,value='0'):
    lines=['\tpublic _SinTable8, _CosTable8','']
    for i in range(rows):
        label='_SinTable8'if i==0 else('_CosTable8'if i==cos_row else'')
        lines.append(label+'\tdw '+','.join([value]*8))
    return ('\n'.join(lines)+'\nEND\n').encode()


def data_object(*,total=640,pub=0,chunks=None,fixup=None,duplicate=False,extra=b''):
    raw=record(0x80,b'\x01x')+record(0x96,b'\x05_DATA\x04DATA\0')
    raw+=record(0x98,b'\x48'+struct.pack('<H',total)+b'\x01\x02\x03')
    pubs=b'\0\1'
    for name,offset in [('_SinTable8',pub),('_CosTable8',pub+128)]:
        pubs+=bytes([len(name)])+name.encode()+struct.pack('<H',offset)+b'\0'
    raw+=record(0x90,pubs)
    if duplicate:raw+=record(0x90,pubs)
    for start,data in chunks if chunks is not None else[(0,bytes(total))]:
        raw+=record(0xA0,b'\1'+struct.pack('<H',start)+data)
        if fixup:raw+=record(0x9C,fixup)
    return raw+extra+record(0x8A,b'\0')


def contribution(size=640):return dict(frame=0,offset=0,size=size)


def map_source(*,sin='0EFE:0590',cos='0EFE:0610',duplicate=False):
    return (' 0EFE:04D2 04D0 C=DATA S=_DATA G=DGROUP M=th05_op.asm ACBP=48\n'+
        ' Address Publics by Name\n '+cos+' _CosTable8\n '+sin+' _SinTable8\n'+
        (' '+sin+' _SinTable8\n'if duplicate else'')+
        ' Address Publics by Value\n '+sin+' _SinTable8\n '+cos+' _CosTable8\n').encode()


class Sin8ReviewTests(unittest.TestCase):
    def metadata(self):return json.loads((ROOT/review.PROOF).read_text())

    def test_whole320signedwords_and_shared_alias(self):
        parsed=review.initializer(source(value='-256'),'utf8')
        self.assertEqual(parsed['content'],struct.pack('<320h',*([-256]*320)))
        self.assertEqual(parsed['lines'],[1,42])
        self.assertEqual(len(parsed['content']),640)

    def test_cardinality_alias_shift_and_signed_word_overflow_reject(self):
        for raw in [source(rows=39),source(cos_row=9),source(value='-32769'),source(value='32768'),source(value='0x100')]:
            with self.subTest(raw=raw[:30]),self.assertRaises(ValueError):review.initializer(raw,'utf8')

    def test_symbolic_source_whitespace_and_comment_identity_is_not_normalized(self):
        before=review.initializer(source(),'utf8')
        changed=review.initializer(source().replace(b'\tdw ',b' dw ',1),'utf8')
        self.assertEqual(before['content'],changed['content'])
        self.assertNotEqual(before['block'],changed['block'])
        with self.assertRaises(ValueError):review.initializer(source().replace(b'\tdw ',b'\tdw ;changed\n',1),'utf8')

    def test_actual_DATA_OMF_scope_keeps_two_aliases_one_physical_table(self):
        content,scope=review.object_data(data_object(),contribution(),0)
        self.assertEqual(len(content),640)
        self.assertEqual([p['offset']for p in scope['PUBDEF']],[0,128])
        self.assertEqual(scope['SEGDEF']['class_name'],'DATA')

    def test_unwritten_zero_gap_overlapping_LEDADTA_and_pubdef_duplicates_reject(self):
        cases=[data_object(chunks=[(0,bytes(100)),(101,bytes(539))]),
               data_object(chunks=[(0,bytes(400)),(399,bytes(241))]),data_object(duplicate=True),
               data_object(pub=1),data_object(extra=record(0x8E,b'\0'))]
        for raw in cases:
            with self.subTest(length=len(raw)),self.assertRaises(ValueError):
                review.object_data(raw,contribution(),0)

    def test_fixupp_inside_or_crossing_lower_boundary_rejects(self):
        fixup=b'\xC4\x00\x54\x01'
        with self.assertRaisesRegex(ValueError,'cross-boundary'):
            review.object_data(data_object(total=642,pub=1,fixup=fixup),contribution(642),1)
        with self.assertRaisesRegex(ValueError,'FIXUPP'):
            review.object_data(data_object(fixup=fixup),contribution(),0)

    def test_iterated_DATA_outside_scope_is_bounded_inside_scope_rejects(self):
        def iterated(offset):return record(0xA2,b'\1'+struct.pack('<H',offset)+struct.pack('<HH',1,0)+b'\1x')
        raw=data_object(total=800,chunks=[(0,bytes(640))],extra=iterated(700))
        self.assertEqual(len(review.object_data(raw,contribution(800),0)[0]),640)
        with self.assertRaisesRegex(ValueError,'iterated'):
            review.object_data(data_object(extra=iterated(0)),contribution(),0)
        with self.assertRaisesRegex(ValueError,'expansion'):
            review.iterated_length(struct.pack('<HH',65535,0)+b'\1x',0,640)

    def test_MAP_literal_frames_aliases_and_section_duplicates_reject(self):
        con,pubs=review.map_data(map_source(),review.PINS['op'])
        self.assertEqual(con['frame'],0xEFE0)
        self.assertEqual([p['offset']for p in pubs],[0x590,0x610])
        for raw in [map_source(sin='0EFF:0580'),map_source(cos='0EFE:0612'),map_source(duplicate=True),
                    map_source().replace(b'04D0 C=DATA',b'04D0 C=CODE')]:
            with self.subTest(raw=raw[:30]),self.assertRaises(ValueError):review.map_data(raw,review.PINS['op'])

    def test_real_startup_DS_and_relocated_word_are_required(self):
        content=bytearray(32);content[0]=0xBA;struct.pack_into('<H',content,1,0x209D);content[20:22]=b'\x8E\xDA'
        image=SimpleNamespace(program_image=bytes(content),relocations=[SimpleNamespace(linear=1)])
        self.assertEqual(review.startup_dgroup(image,0x209D)['segment'],0x209D)
        for bad in [SimpleNamespace(program_image=bytes(content),relocations=[]),
                    SimpleNamespace(program_image=bytes(32),relocations=[SimpleNamespace(linear=1)])]:
            with self.assertRaisesRegex(ValueError,'startup DS'):review.startup_dgroup(bad,0x209D)
        with self.assertRaises(ValueError):review.startup_dgroup(image,0x209E)

    def test_public_structure_runs_without_private_cache_and_pins_helpers(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            for path in [*review.SOURCES,review.CONTEXT_PROOF,review.context.BASE_PROOF]:
                dest=root/path;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/path,dest)
            self.assertFalse((root/'.analysis').exists())
            result=review.validate_metadata(self.metadata(),root=root)
            self.assertEqual((result['full_bytes'],result['instruction_bytes']),(1920,0))
            self.assertFalse(result['byte_proof_replayed'])
            (root/'scripts/lib/unit_context.py').write_text('changed target loader')
            with self.assertRaisesRegex(ValueError,'identity drift'):review.validate_metadata(self.metadata(),root=root)

    def test_redigested_positions_kind_source_fixups_policy_or_context_tamper_rejects(self):
        for mode in ['original','calibration','frame','source','fixup','kind','credit','denominator','archive','context','gap']:
            meta=self.metadata()
            if mode=='original':meta['scopes'][0]['original_start']=meta['scopes'][0]['calibration_start']
            elif mode=='calibration':meta['scopes'][2]['calibration_start']=meta['scopes'][2]['original_start']
            elif mode=='frame':meta['scopes'][0]['original_aliases'][0]['frame']+=16
            elif mode=='source':meta['primary_source_block_sha256']='0'*64
            elif mode=='fixup':meta['scopes'][0]['original_ordered_fixups']=[0]
            elif mode=='kind':meta['proposed_claim_kind']='verified-vendor-code'
            elif mode=='credit':meta['authored_credit']=False
            elif mode=='denominator':meta['authored_denominator']=100
            elif mode=='archive':meta['primary_archives']['inner_archive']['sha256']='0'*64
            elif mode=='context':meta['scopes'][0]['actual_inputs']=meta['scopes'][1]['actual_inputs']
            else:meta['uncovered_gaps_policy']='vendor'
            meta['evidence_digest']=review.context.evidence_digest(meta)
            with self.subTest(mode=mode),self.assertRaises(ValueError):review.validate_metadata(meta)

    def test_native_replay_must_rebuild_actual_inputs_not_saved_status(self):
        meta=self.metadata()
        with patch.object(review,'build_metadata',return_value={'status':'PASS'})as replay:
            with self.assertRaisesRegex(ValueError,'actual SIN8'):review.review_inputs(meta)
            replay.assert_called_once_with(ROOT)


if __name__=='__main__':unittest.main()
