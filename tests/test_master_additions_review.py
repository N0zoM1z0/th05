"""Bounded vendor additions: real-source semantics, complete OMF and no adoption."""
import copy
import json
from pathlib import Path
import shutil
import struct
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import review_master_additions as review
from lib.pc98 import parse_mz


def record(kind,data):
    raw=bytes([kind])+struct.pack('<H',len(data)+1)+data
    return raw+bytes([-sum(raw)&255])


def object_image(*,chunks=None,pub_offset=0,duplicate_public=False,fixup=None,extra=b''):
    raw=record(0x80,b'\x01x')+record(0x96,b'\x05_TEXT\x04CODE\x00')
    raw+=record(0x98,b'\x48\x04\x00\x01\x02\x03')
    pub=b'\x00\x01\x06RotTbl'+struct.pack('<H',pub_offset)+b'\x00'
    raw+=record(0x90,pub)
    if duplicate_public:raw+=record(0x90,pub)
    for at,data in chunks if chunks is not None else [(0,b'abcd')]:
        raw+=record(0xA0,b'\x01'+struct.pack('<H',at)+data)
        if fixup is not None:raw+=record(0x9C,fixup)
    return raw+extra+record(0x8A,b'\x00')


def con(size=4):return dict(start=0x272,size=size,acbp=0x48)


def table_source(*,comment='historical comment',value='00000000h',lines=64):
    return ('; '+comment+'\n\tpublic RotTbl\n'+''.join(
        ('RotTbl' if i==0 else '')+'\tdd\t'+','.join([value]*4)+'\n'for i in range(lines))).encode()


def map_source(*,public='0000:1C88',duplicate=False,contribution_duplicate=False):
    contribution=' 0000:0272 38A6 C=CODE S=_TEXT G=(none) M=th05_op.asm ACBP=48\n'
    return (contribution*(2 if contribution_duplicate else 1)+' Address Publics by Name\n'+
        (' '+public+' idle RotTbl\n')*(2 if duplicate else 1)+' Address Publics by Value\n '+public+' idle RotTbl\n').encode()


class MasterSourceTests(unittest.TestCase):
    def test_full_symbolic_initializer_is_compared_literally(self):
        before,after=review.literal_initializer(table_source(),table_source())
        self.assertEqual(len(before['content']),1024)
        self.assertEqual(before['block'],after['block'])
        # Comments outside the initializer do not claim source identity.
        review.literal_initializer(table_source(comment='outside changed'),table_source())
        changed=table_source().replace(b'\tdd\t',b' dd ',1)
        self.assertEqual(review.initializer(changed,'utf8')['content'],before['content'])
        with self.assertRaisesRegex(ValueError,'literal'):
            review.literal_initializer(table_source(),changed)
        for bad in (table_source(value='00000001h'),table_source(lines=63),
                    table_source().replace(b'00000000h',b'4294967296',1)):
            with self.subTest(bad=bad[:40]),self.assertRaises(ValueError):
                review.literal_initializer(table_source(),bad)

    def test_complete_procedure_comments_case_and_ambiguity_are_not_normalized(self):
        raw=b'func ORIGINAL\n mov ax,1 ; historical\nendfunc\n'
        source={'ORIGINAL.ASM':raw}
        self.assertEqual(review.unique_source_block(source,raw,'ORIGINAL')[0],'ORIGINAL.ASM')
        for candidate in (raw.replace(b'historical',b'changed'),raw.replace(b'mov',b'MOV'),raw+raw):
            with self.subTest(candidate=candidate),self.assertRaisesRegex(ValueError,'source procedure'):
                review.unique_source_block(source,candidate,'ORIGINAL')

    def test_archive_crc_and_extracted_member_authentication_delegate_real_parser(self):
        # The additive native path invokes the frozen baseline full archive replay,
        # and the exact pinned inner parser; malformed archive headers fail natively.
        with self.assertRaises((ValueError,IndexError)):
            review.base.stored_lzh(b'\x02\x00\x01\x02\x00')
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);p=root/'archive';p.write_bytes(b'actual bytes')
            row=review.identity(root,'archive')
            p.write_bytes(b'changed bytes')
            with self.assertRaisesRegex(ValueError,'identity drift'):
                review.base.pinned(root,row)


class ActualObjectTests(unittest.TestCase):
    def test_actual_complete_object_scope_and_pubdef(self):
        body,evidence=review.object_scope(object_image(),con(),0x272,4)
        self.assertEqual(body,b'abcd')
        self.assertEqual(evidence['intersecting_FIXUPP_count'],0)
        self.assertEqual(evidence['PUBDEF']['offset'],0)

    def test_gaps_zero_holes_overlaps_and_duplicate_pubdefs_reject(self):
        cases=[object_image(chunks=[(0,b'a'),(2,b'cd')]),
               object_image(chunks=[(0,b'ab'),(1,b'bcd')]),
               object_image(duplicate_public=True),object_image(pub_offset=1),
               object_image(extra=record(0x8E,b'\0'))]
        for raw in cases:
            with self.subTest(raw_size=len(raw)),self.assertRaises(ValueError):
                review.object_scope(raw,con(),0x272,4)

    def test_inside_and_boundary_crossing_fixupp_cannot_hide_in_initializer(self):
        # A real explicit OMF16 offset fixup at zero, field width2.
        # Scope1..3 means it crosses the lower boundary instead of starting inside.
        raw=object_image(pub_offset=1,fixup=b'\xC4\x00\x54\x01')
        with self.assertRaisesRegex(ValueError,'crosses boundary'):
            review.object_scope(raw,con(),0x273,2)
        with self.assertRaisesRegex(ValueError,'intersects'):
            review.object_scope(object_image(fixup=b'\xC4\x00\x54\x01'),con(),0x272,4)

    def test_actual_map_public_sections_preserve_frame_identity(self):
        contribution,public=review.map_context(map_source(),'th05_op.asm',0x38A6,0x1C88,1024)
        self.assertEqual(public,dict(frame=0,offset=0x1C88))
        self.assertEqual(contribution['start'],0x272)
        for raw in (map_source(public='0001:1C78'),map_source(duplicate=True),
                    map_source(contribution_duplicate=True),map_source().replace(b'RotTbl',b'not_table')):
            with self.subTest(raw=raw[:50]),self.assertRaisesRegex(ValueError,'MAP'):
                review.map_context(raw,'th05_op.asm',0x38A6,0x1C88,1024)

    def test_original_mz_relocation_before_scope_is_not_silently_clipped(self):
        header=struct.pack('<14H',0x5A4D,52,1,1,2,1,0xFFFF,0,16,0,0,0,28,0)
        image=parse_mz(header+struct.pack('<HH',1,0)+b'abcdefghijklmnopqrst')
        self.assertTrue(image.valid)
        with self.assertRaisesRegex(ValueError,'cross'):
            review.no_relocations(image,2,4)
        self.assertEqual(review.no_relocations(image,4,4),[])


class PublicProposalTests(unittest.TestCase):
    def metadata(self):return json.loads((ROOT/review.PROOF).read_text())

    def test_public_structure_needs_no_private_inputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            for path in [*review.SOURCES,review.BASE_PROOF]:
                dest=root/path;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/path,dest)
            self.assertFalse((root/'.analysis').exists())
            result=review.validate_metadata(self.metadata(),root=root)
            self.assertEqual((result['scopes'],result['full_bytes']),(7,2152))
            self.assertFalse(result['byte_proof_replayed'])
            (root/'scripts/lib/unit_context.py').write_text('changed actual decoded loader')
            with self.assertRaisesRegex(ValueError,'identity drift'):
                review.validate_metadata(self.metadata(),root=root)

    def test_redigested_scope_drift_and_adoption_policies_reject(self):
        for change in ('extent','data','source','closure','adopt','authored','gap-policy'):
            meta=self.metadata()
            if change=='extent':meta['scopes'][0]['end']+=1
            elif change=='data':meta['scopes'][-1]['linked_sha256']='0'*64
            elif change=='source':meta['scopes'][0]['source_block_sha256']='0'*64
            elif change=='closure':meta['table_contexts']['op']['frozen_source_closure'].pop()
            elif change=='adopt':meta['decision']='ADOPT'
            elif change=='authored':meta['authored_credit']=False
            else:meta['proposed_decisions'][0]['uncovered_gaps_policy']='vendor'
            meta['evidence_digest']=review.evidence_digest(meta)
            with self.subTest(change=change),self.assertRaises(ValueError):
                review.validate_metadata(meta)

    def test_private_review_rebuilds_not_saved_status(self):
        meta=self.metadata()
        with patch.object(review,'build_metadata',return_value={'saved_status':'PASS'}) as replay:
            with self.assertRaisesRegex(ValueError,'actual primary-source'):
                review.review_inputs(meta)
            replay.assert_called_once_with(ROOT)

    def test_wrong_context_and_archive_identity_reject(self):
        for field in ('calibration_object','calibration_map'):
            meta=self.metadata()
            meta['table_contexts']['op']['inputs'][field]=copy.deepcopy(meta['table_contexts']['maine']['inputs'][field])
            meta['evidence_digest']=review.evidence_digest(meta)
            with self.subTest(field=field),self.assertRaises(ValueError):review.validate_metadata(meta)
        meta=self.metadata();meta['primary_source']['inner_archive']['sha256']='0'*64
        meta['evidence_digest']=review.evidence_digest(meta)
        with self.assertRaises(ValueError):review.validate_metadata(meta)


if __name__=='__main__':unittest.main()
