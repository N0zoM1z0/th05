"""Synthetic and public-only tests; no vendor/game bytes or DOS tools needed."""
import copy
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.pc98 import parse_mz
from review_master import (
    crc16, decoded, linked_object_procedure, listing_procedures, macro_blocks,
    object_text, pinned, relative, sha, source_blocks, stored_lzh,
    validate_metadata, verify_macro_context, verify_raw_procedure,
)


def record(kind, payload):
    frame = bytes([kind])+struct.pack("<H", len(payload)+1)+payload
    return frame+bytes([-sum(frame)&255])


def obj(code=b"abcd", fixups=b"", blocks=None):
    raw = record(0x80, b"\x06sample")
    raw += record(0x96, b"\x05_TEXT\x04CODE\x00")
    raw += record(0x98, b"\x48\x76\x43\x01\x02\x03")
    for offset, content in blocks if blocks is not None else [(0, code)]:
        raw += record(0xA0, b"\1"+struct.pack("<H",offset)+content)
    if fixups:
        raw += record(0x9C,fixups)
    return raw+record(0x8A,b"\0")


def lzh(name=b"SAMPLE.ASM", content=b"sample\r\n"):
    h = bytearray(len(name)+27)
    h[0] = len(h)-2
    h[2:7] = b"-lh0-"
    struct.pack_into("<II",h,7,len(content),len(content))
    h[20],h[21] = 1,len(name)
    h[22:22+len(name)] = name
    struct.pack_into("<H",h,22+len(name),crc16(content))
    h[1] = sum(h[2:])&255
    return bytes(h)+content+b"\0"


def mz(body, sites=()):
    h = bytearray(64)
    size = len(h)+len(body)
    struct.pack_into("<14H", h, 0, 0x5A4D,size%512,(size+511)//512,
                     len(sites),4,1,0xFFFF,0,16,0,0,0,28,0)
    for i,site in enumerate(sites):
        struct.pack_into("<HH",h,28+i*4,site&15,site>>4)
    image = parse_mz(bytes(h)+body)
    assert image.valid
    return image


class MasterSourceTests(unittest.TestCase):
    def test_literal_complete_blocks_only_allow_decoding_and_line_endings(self):
        left = b"func SAMPLE\r\n\tnop ; comment\r\nendfunc\r\n"
        right = left.replace(b"\r\n",b"\n")
        a,b = source_blocks(left,"cp932"),source_blocks(right,"utf8")
        self.assertEqual(a,b)
        for changed in (right.replace(b"comment",b"Comment"),
                        right.replace(b"\tnop",b" nop"),
                        right.replace(b"SAMPLE",b"sample")):
            self.assertNotEqual(a[0]["text"],source_blocks(changed,"utf8")[0]["text"])
        self.assertEqual(source_blocks(b"func SAMPLE\n nop\n","ascii"),[])
        with self.assertRaises(UnicodeDecodeError):
            decoded(b"\xff","utf8")

    def test_nested_function_wrapper_macro_is_complete(self):
        raw = b"func macro name\n name proc\n endfunc macro\n name endp\n endm\n endm\n"
        block = macro_blocks(raw,"ascii","func")
        self.assertEqual(len(block),1)
        self.assertTrue(block[0].endswith(" endm\n endm"))

    def test_listing_ignores_inactive_declarations_and_macro_definitions(self):
        raw = (" 1\t 0000\t _TEXT segment\n"
               " 2\t\t include libs/master.lib/sample.asm\n"
               "1 3\t\t hidden proc far\n"
               "1 4\t 0000\t SAMPLE proc far\n"
               "2 5\t\t macro_only endp\n"
               " 6\t\t wrapped comment without a depth marker\n"
               "1 7\t 0001 90\t EVEN\n"
               "1 8\t 0002\t SAMPLE endp\n"
               " 9\t 0002\t _TEXT ends\n").encode()
        rows = listing_procedures(raw,size=2)
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]["source"],"libs/master.lib/sample.asm")
        self.assertEqual(rows[0]["local_end"],2)
        self.assertEqual(rows[0]["padding"],[dict(local_start=1,size=1,listing_line=7)])
        with self.assertRaisesRegex(ValueError,"unpaired"):
            listing_procedures(raw.replace(b"SAMPLE endp",b"WRONG endp"),size=2)
        with self.assertRaisesRegex(ValueError,"complete"):
            listing_procedures(raw.replace(b" 0002\t _TEXT ends",b" 0003\t _TEXT ends"),size=2)

    def test_listing_does_not_classify_inline_data_as_instructions(self):
        raw = b"1\t0000\t_TEXT segment\n2\t0000\tSAMPLE proc far\n3\t0000\tdb 0\n4\t0001\tSAMPLE endp\n5\t0001\t_TEXT ends\n"
        self.assertTrue(listing_procedures(raw,size=1)[0]["inline_data"])


class MasterMacroTests(unittest.TestCase):
    def fixture(self):
        wrapper = "func macro name\n name proc CALLMODEL\n endm\nretfunc macro name\n name proc CALLMODEL\n endm\n"
        call = "IF RETSIZE EQ 2\n_call macro sample\n nop\n endm\nELSE\n_call macro sample\n ret\n endm\nENDIF\n"
        a = ("IFDEF FARMODEL\n CALLMODEL equ FAR\n RETSIZE EQU 2\n DATASIZE EQU 2\nENDIF\n"+wrapper+call).encode()
        b = ("ELSEIF @MODEL EQ 5\n RETSIZE EQU 2\n DATASIZE EQU 2\n"+wrapper.replace(" CALLMODEL","")+call).encode()
        upstream = {"FUNC.INC":a,"MAKEFILE":b".asm{$(LARGEDIR)}.obj :\n $(AS) /DFARMODEL sample\n",
                    "PF.INC":b"; synthetic shared declarations\n", "PORT.ASM":b"PORT equ 12h\n"}
        candidate = {"libs/master.lib/func.inc":b,"libs/master.lib/pf.inc":upstream["PF.INC"],
                     "libs/master.lib/port.asm":upstream["PORT.ASM"]}
        blocks=macro_blocks(a,"ascii","_call")
        ctx={"active_listing_lines":{"RETSIZE":2,"DATASIZE":3},
             "literal_macros":[dict(name="_call",upstream_file="FUNC.INC",candidate_file="libs/master.lib/func.inc",
                                     sha256=sha(blocks[0].encode()),variant_sha256=[sha(x.encode())for x in blocks])],
             "constants":[dict(name="PORT",expression="12h",upstream_file="PORT.ASM",candidate_file="libs/master.lib/port.asm")]}
        listing=b".model use16 large _TEXT\n=0002 RETSIZE EQU 2\n=0002 DATASIZE EQU 2\n"
        return {"macro_context":ctx},listing,upstream,candidate

    def test_large_model_source_and_actual_listing_are_both_required(self):
        args=self.fixture();verify_macro_context(*args)
        meta,listing,upstream,candidate=args
        with self.assertRaisesRegex(ValueError,"active FAR/data2"):
            verify_macro_context(meta,listing.replace(b"=0002 RETSIZE",b"=0001 RETSIZE"),upstream,candidate)
        bad=copy.deepcopy(upstream);bad["MAKEFILE"]=bad["MAKEFILE"].replace(b"/DFARMODEL",b"/DNEARMODEL")
        with self.assertRaisesRegex(ValueError,"large-model build flag"):
            verify_macro_context(meta,listing,bad,candidate)
        bad=copy.deepcopy(candidate);bad["libs/master.lib/func.inc"]=bad["libs/master.lib/func.inc"].replace(b"IF RETSIZE EQ 2",b"IF RETSIZE EQ 1")
        with self.assertRaisesRegex(ValueError,"proven FAR/data2 arm"):
            verify_macro_context(meta,listing,upstream,bad)

    def test_macro_wrappers_data_layout_and_port_constants_cannot_drift(self):
        meta,listing,upstream,candidate=self.fixture()
        for filename,before,after,message in (
            ("libs/master.lib/func.inc",b" nop",b" push ax","complete macro"),
            ("libs/master.lib/func.inc",b"name proc",b"name proc\n nop","function wrapper"),
            ("libs/master.lib/pf.inc",b"shared",b"changed","PF.INC"),
            ("libs/master.lib/port.asm",b"12h",b"13h","constant context"),
        ):
            bad=copy.deepcopy(candidate);bad[filename]=bad[filename].replace(before,after)
            with self.subTest(filename=filename,message=message):
                with self.assertRaisesRegex(ValueError,message):
                    verify_macro_context(meta,listing,upstream,bad)


class MasterArchiveTests(unittest.TestCase):
    def test_crc_reference_and_literal_stored_member(self):
        self.assertEqual(crc16(b"123456789"),0xBB3D)
        self.assertEqual(stored_lzh(lzh()),{"SAMPLE.ASM":b"sample\r\n"})

    def test_header_content_crc_and_trailing_bytes_are_independent(self):
        raw=bytearray(lzh())
        raw[7] ^= 1
        with self.assertRaisesRegex(ValueError,"header checksum"):
            stored_lzh(bytes(raw))
        raw=bytearray(lzh());raw[-3]^=1
        with self.assertRaisesRegex(ValueError,"member CRC"):
            stored_lzh(bytes(raw))
        for broken in (lzh()+b"\0",lzh()[:-2],lzh()[:-1]):
            with self.assertRaises(ValueError):
                stored_lzh(broken)

    def test_duplicate_traversal_and_unsupported_compression_fail_closed(self):
        for name in (b"../BAD",b"C:BAD",b"..",b"A\\B"):
            with self.assertRaisesRegex(ValueError,"unsafe"):
                stored_lzh(lzh(name))
        with self.assertRaisesRegex(ValueError,"duplicate"):
            stored_lzh(lzh()[:-1]+lzh(b"sample.asm"))
        raw=bytearray(lzh());raw[2:7]=b"-lh5-";raw[1]=sum(raw[2:raw[0]+2])&255
        with self.assertRaisesRegex(ValueError,"method"):
            stored_lzh(bytes(raw))


class MasterObjectTests(unittest.TestCase):
    def test_real_segment_offset_fixup_uses_actual_map_bias(self):
        parsed=object_text(obj(b"A\x10\0B",b"\xc4\x01\x54\x01"))
        data,actions=linked_object_procedure(parsed,0x272,4)
        self.assertEqual(data,b"A\x82\x02B")
        self.assertEqual(actions,[dict(offset=1,operation="actual MAP _TEXT offset addition",addend=0x272)])
        self.assertNotEqual(linked_object_procedure(parsed,0x271,4,bias=0x271)[0],data)

    def test_omf_checksum_bounds_threads_and_unsupported_fixups_reject(self):
        raw=bytearray(obj());raw[5]^=1
        with self.assertRaisesRegex(ValueError,"checksum"):
            object_text(bytes(raw))
        for f in (b"\0\0\0",b"\xc4\x03\x54\x01"):
            with self.assertRaises(ValueError):
                object_text(obj(fixups=f))
        for f in (b"\xc4\x01\x56\x01",b"\xc4\x01\x04\x01\x01"):
            parsed=object_text(obj(fixups=f))
            with self.assertRaisesRegex(ValueError,"unreviewed"):
                linked_object_procedure(parsed,0x272,4)

    def test_procedure_ledatas_cannot_hide_gap_overlap_or_boundary_fixup(self):
        for blocks in ([(0,b"abc")],[(0,b"abcd"),(1,b"b")]):
            with self.assertRaisesRegex(ValueError,"LEDATA"):
                linked_object_procedure(object_text(obj(blocks=blocks)),0x272,4)
        parsed=object_text(obj(b"abcd",b"\xc4\x01\x54\x01"))
        with self.assertRaisesRegex(ValueError,"crosses"):
            linked_object_procedure(parsed,0x272,2)
        parsed=object_text(obj(b"abcd",b"\xc4\x01\x54\x01\xc4\x01\x54\x01"))
        with self.assertRaisesRegex(ValueError,"overlapping"):
            linked_object_procedure(parsed,0x272,4)

    def test_original_raw_relocations_and_padding_are_rechecked(self):
        body=bytes(0x272)+b"abc\x90"
        row=dict(start=0x272,end=0x276,linked_sha256=sha(b"abc\x90"),
                 ordered_mz_fixups=[],object_link_actions=[],padding=[dict(start=0x275,value=0x90)])
        parsed=object_text(obj(b"abc\x90")); image=mz(body)
        verify_raw_procedure(row,image,image,parsed)
        with self.assertRaisesRegex(ValueError,"raw"):
            verify_raw_procedure(row,mz(body[:-1]+b"\0"),image,parsed)
        with self.assertRaisesRegex(ValueError,"ordered MZ"):
            verify_raw_procedure(row,mz(body,(0x272,)),image,parsed)
        with self.assertRaisesRegex(ValueError,"ordered MZ"):
            verify_raw_procedure(row,mz(body,(0x271,)),image,parsed)
        bad=copy.deepcopy(row);bad["padding"][0]["value"]=0
        with self.assertRaisesRegex(ValueError,"padding"):
            verify_raw_procedure(bad,image,image,parsed)


class MasterPublicTests(unittest.TestCase):
    def metadata(self):
        return json.loads((ROOT/"config/master_vendor_ownership.json").read_text())

    def test_public_structure_needs_no_private_inputs(self):
        meta=self.metadata()
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            for row in meta["reviewer_sources"]:
                p=root/row["file"];p.parent.mkdir(parents=True,exist_ok=True)
                p.write_bytes((ROOT/row["file"]).read_bytes())
            self.assertFalse(validate_metadata(meta,root=root)["byte_proof_replayed"])
            (root/"scripts/review_master.py").write_text("# drift")
            with self.assertRaisesRegex(ValueError,"identity drift"):
                validate_metadata(meta,root=root)

    def test_scope_credit_context_and_deferred_changes_cannot_be_smuggled(self):
        base=self.metadata()
        for mutate in (
            lambda m:m.update(authored_credit=367),
            lambda m:m.update(decision="ADOPTED"),
            lambda m:m["procedures"][0].update(end=2000),
            lambda m:m["procedures"][0].update(ordered_mz_fixups=[1]),
            lambda m:m["deferred_source_mismatches"][0].update(decision="ACCEPTED"),
            lambda m:m["macro_context"]["active_model"].update(DATASIZE=1),
            lambda m:m["uncovered_gaps"][0].update(decision="VENDOR"),
            lambda m:m.update(reviewer_sources=[]),
            lambda m:m["procedures"][0].update(linked_sha256="0"*64),
        ):
            with self.subTest(mutate=mutate):
                bad=copy.deepcopy(base);mutate(bad)
                with self.assertRaises(ValueError):validate_metadata(bad)

    def test_actual_input_hash_is_checked_instead_of_saved_pass_status(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);p=root/"input";p.write_bytes(b"original")
            row=dict(file="input",size=8,sha256=sha(b"original"),status="PASS")
            self.assertEqual(pinned(root,row),b"original")
            p.write_bytes(b"modified")
            with self.assertRaisesRegex(ValueError,"identity drift"):pinned(root,row)
            for name in ("../input","/tmp/input","C:/input","a\\b"):
                with self.assertRaises(ValueError):relative(name)


if __name__ == "__main__":
    unittest.main()
