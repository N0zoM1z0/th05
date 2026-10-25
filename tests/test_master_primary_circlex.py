"""Original source/vendor gates: record coverage, context and zero credit."""
import copy
import json
from pathlib import Path
from types import SimpleNamespace
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import review_master_primary_circlex as review


def synthetic_object(changes=None, *, extra=None, move_fixups=False):
    """CRC-valid container with synthetic INT3 bytes, never native CODE."""
    body = bytearray(b'\xcc'*240)
    for offset in (85, 93, 167):
        body[offset:offset+2] = (0x1234).to_bytes(2, 'little')
    for offset in (91, 165):
        body[offset] = 9
    fields = [('header', 0x80, b'\x0cGC_CIRCX.ASM'), ('names1', 0x96, b'\0'),
              ('comment1', 0x88, b'\x40\xa1'), ('names2', 0x96, b'\x05_TEXT\x04CODE'),
              ('code', 0x98, b'\x48\xf0\0\x02\x03\x01'),
              ('names3', 0x96, b'\x05_DATA\x04DATA'), ('data', 0x98, b'\x48\0\0\x04\x05\x01'),
              ('names4', 0x96, b'\x06DGROUP'), ('group', 0x9a, b'\x06\xff\x02'),
              ('external', 0x8c, b'\x06ClipYT\0\x0aClipYT_seg\0\x0egraph_VramZoom\0'),
              ('public', 0x90, b'\0\x01\x0dGRCG_CIRCLE_X\0\0\0'),
              ('comment2', 0x88, b'\x40\xa2\x01')]
    for i, (offset, size) in enumerate(review.CHUNKS):
        fields.append(('chunk'+str(i), 0xa0, b'\x01'+offset.to_bytes(2, 'little')+body[offset:offset+size]))
        if i == 0:
            fields.append(('fixups', 0x9c, bytes.fromhex(
                'c40e160103c41d160101c424160102c4125401c4165401c4295401c42d5401c4315401')))
    if move_fixups:
        fields[13], fields[14] = fields[14], fields[13]
    if extra:
        fields.append(extra)
    fields.append(('end', 0x8a, b'\0'))
    output = bytearray()
    for name, kind, raw in fields:
        raw = (changes or {}).get(name, raw)
        header = bytes([kind])+(len(raw)+1).to_bytes(2, 'little')
        output.extend(header+raw+bytes([(-sum(header+raw)) & 255]))
    return bytes(output)


def synthetic_context():
    clip = [('ClipXL', 'dw', '0'), ('ClipXW', 'dw', '639'), ('ClipXR', 'dw', '639'),
            ('ClipYT', 'dw', '0'), ('ClipYH', 'dw', '399'), ('ClipYB', 'dw', '399'),
            ('ClipYT_seg', 'dw', '0a800h'), ('ClipYB_adr', 'dw', '399*80')]
    graph = [('_graph_VramSeg', 'dw', '0a800h'), ('_graph_VramWords', 'dw', '16000'),
             ('_graph_VramLines', 'dw', '400'), ('_graph_VramWidth', 'dw', '80'),
             ('_graph_VramZoom', 'dw', '0'), ('_graph_MeshByte', 'db', '55h')]
    result = {}
    for name, rows in [('CLIP.ASM', clip), ('GRP.ASM', graph)]:
        result[name] = ('.DATA\r\n'+''.join(' '.join(row)+' ; synthetic\r\n' for row in rows)+
                        '.DATA?\r\nnot_initialized dw 4 dup(?)\r\nEND\r\n').encode()
    return result, clip, graph


class ContainerTests(unittest.TestCase):
    def test_original_input_and_own_unique_semantic_negative(self):
        raw = b'\x82\xa0; synthetic\r\n\tinc\tAX\r\n'
        self.assertIs(review.source_input(raw, False), raw)
        self.assertEqual(review.source_input(raw, True), raw.replace(b'inc\tAX', b'dec\tAX'))
        for bad in (b'no anchor', raw+raw):
            with self.assertRaisesRegex(ValueError, 'unique'):
                review.source_input(bad, True)

    def test_six_original_records_cover_every_byte_once(self):
        scope = review.object_shape(synthetic_object())
        self.assertEqual((scope['segment'], scope['size']), ('_TEXT', 240))
        self.assertEqual([(r['offset'], r['size']) for r in scope['ledata']], review.CHUNKS)
        self.assertEqual(sum(r['size'] for r in scope['ledata']), 240)

    def test_crc_valid_bad_frames_gaps_overlaps_and_record_association_fail(self):
        mutants = [synthetic_object({'code': b'\x48\xef\0\x02\x03\x01'}),
                   synthetic_object({'data': b'\x48\x01\0\x04\x05\x01'}),
                   synthetic_object({'chunk1': b'\x01\x56\0'+b'\xcc'*5}),
                   synthetic_object({'chunk1': b'\x01\x58\0'+b'\xcc'*5}),
                   synthetic_object({'chunk1': b'\x01\x57\0'+b'\xcc'*4}),
                   synthetic_object({'fixups': b'\xc4\x0e\x16\x01\x01'}),
                   synthetic_object({'comment1': b'\x40\xa0'}),
                   synthetic_object(extra=('extra', 0xa0, b'\x01\0\0\xcc')),
                   synthetic_object(move_fixups=True)]
        for raw in mutants:
            review.parse_omf(raw)
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                review.object_shape(raw)

    def test_initial_self_patched_operands_are_not_masked(self):
        for name, raw in [('chunk0', b'\x01\0\0'+b'\xcc'*87),
                          ('chunk1', b'\x01\x57\0'+b'\xcc'*5)]:
            with self.subTest(name=name), self.assertRaises(ValueError):
                review.object_shape(synthetic_object({name: raw}))


class ContextTests(unittest.TestCase):
    def setUp(self):
        self.source, clip, graph = synthetic_context()
        self.data = bytearray(0x23a26)
        for name, fields, offset in [('CLIP.ASM', clip, 0x36c), ('GRP.ASM', graph, 0x3c4)]:
            raw, _ = review.initializer(self.source[name], [(n, kind) for n, kind, _ in fields])
            self.data[0x209d0+offset:0x209d0+offset+len(raw)] = raw

    def test_whole_records_anchor_symbols_only_in_available_loaded_data(self):
        result = review.data_context(self.source, SimpleNamespace(program_image=self.data))
        self.assertEqual(result['foreign_WORD_symbols'], review.SYMBOLS)
        self.assertEqual(result['available_loaded_DATA_range'], [0x209d0, 0x23a26])
        self.assertFalse(result['DATA_ownership_adopted'])

    def test_missing_nonunique_or_changed_context_is_rejected(self):
        duplicate = bytearray(self.data)
        duplicate[0x20ed0:0x20ee0] = duplicate[0x20d3c:0x20d4c]
        for raw in (self.data[:0x20d40], duplicate, bytearray(0x23a26)):
            with self.subTest(size=len(raw)), self.assertRaises(ValueError):
                review.data_context(self.source, SimpleNamespace(program_image=raw))
        changed = {**self.source, 'CLIP.ASM': self.source['CLIP.ASM'].replace(b'399*80', b'399*81')}
        with self.assertRaises(ValueError):
            review.data_context(changed, SimpleNamespace(program_image=self.data))

    def test_initializer_parser_does_not_evaluate_code_or_count_bss(self):
        raw, offsets = review.initializer(b'.DATA\na dw 399*80\n.DATA?\nb dw 4 dup(?)\n', [('a', 'dw')])
        self.assertEqual(raw, (399*80).to_bytes(2, 'little'))
        self.assertEqual(offsets, {'a': 0})
        for expression in (b'foo', b'1+2', b'__import__("os")'):
            with self.subTest(expression=expression), self.assertRaises(ValueError):
                review.initializer(b'.DATA\na dw '+expression+b'\nEND\n', [('a', 'dw')])

    def test_anonymous_data_or_layout_directives_cannot_be_silently_skipped(self):
        for directive in (b'db 1', b'dw 1', b'ORG 2', b'ALIGN 2', b'EVEN', b'other EQU 2'):
            raw = b'.DATA\n'+directive+b'\na dw 399*80\nEND\n'
            with self.subTest(directive=directive), self.assertRaisesRegex(ValueError, 'layout directive'):
                review.initializer(raw, [('a', 'dw')])
        with self.assertRaisesRegex(ValueError, 'width'):
            review.initializer(b'.DATA\na db 256\nEND\n', [('a', 'db')])


class FrozenProofTests(unittest.TestCase):
    def setUp(self):
        self.meta = json.loads((ROOT/review.PROOF).read_text())

    def test_public_structural_validation_reads_no_private_inputs(self):
        pinned = review.base.pinned
        def public_only(root, row):
            self.assertTrue(row['file'].startswith('scripts/'))
            return pinned(root, row)
        with patch.object(review.base, 'pinned', side_effect=public_only), \
                patch.object(review, 'primary_inputs', side_effect=AssertionError('private archive')):
            review.validate_metadata(self.meta)
        self.assertEqual(self.meta['negative_changed_offsets'], [78])
        self.assertEqual(self.meta['instruction_nop_offsets'], [57, 65, 239])

    def test_credit_scope_source_context_nops_or_results_cannot_change(self):
        for mutate in (lambda m: m.update(authored_credit=240),
                       lambda m: m.update(authored_denominator=240),
                       lambda m: m.update(start=0x121b), lambda m: m.update(size=239),
                       lambda m: m['source_flags'].append('/DNEARMODEL'),
                       lambda m: m['source_transformations'].append('operand substitution'),
                       lambda m: m['context_inputs'].update({'CLIP.ASM': '0'*64}),
                       lambda m: m['data_context']['foreign_WORD_symbols'].update({'ClipYT': 0x384}),
                       lambda m: m['instruction_nop_offsets'].pop(),
                       lambda m: m['rounds'][0]['observation']['comparison'].update(raw_exact=False),
                       lambda m: m['rounds'][2]['observation']['comparison'].update(exact=True)):
            bad = copy.deepcopy(self.meta); mutate(bad)
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                review.validate_metadata(bad)

    def test_raw_original_object_map_and_mz_identity_remain_pinned(self):
        for key in ('original_object_raw', 'map_raw', 'mz_raw'):
            bad = copy.deepcopy(self.meta)
            bad['rounds'][1]['observation']['deterministic_identity'][key] = '0'*64
            with self.subTest(key=key), self.assertRaises(ValueError):
                review.validate_metadata(bad)
        bad = copy.deepcopy(self.meta); bad['reviewer_sources'][0]['sha256'] = '0'*64
        with self.assertRaisesRegex(ValueError, 'reviewer source'):
            review.validate_metadata(bad)

    def test_separate_adoption_is_only_whole_vendor_scope_with_zero_credit(self):
        raw = (ROOT/review.PROOF).read_bytes()
        inherited = json.loads((ROOT/review.BASE).read_text())
        views = {'main': {'sha256': inherited['target_payload_sha256']}}
        decision = dict(schema_version=1, decision='ADOPT', classification='verified-vendor-code',
                        proof_sha256=review.sha(raw), base_proof_sha256=review.BASE_SHA,
                        target_sha256=self.meta['target_sha256'], start=0x121c, size=240,
                        procedure='GRCG_CIRCLE_X', authored_credit=0, authored_denominator=None)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'decision.json'
            with patch.object(review, 'DECISION', str(path)):
                self.assertEqual(review.reviewed_claims(ROOT, {}), ([], None))
                path.write_text(json.dumps(decision))
                claims, _ = review.reviewed_claims(ROOT, views)
                self.assertEqual([(r['start'], r['end'], r['kind']) for r in claims],
                                 [(0x121c, 0x130c, 'verified-vendor-code')])
                for key, value in [('proof_sha256', '0'*64), ('start', 0x121b), ('size', 239),
                                   ('authored_credit', 240), ('authored_denominator', 240)]:
                    path.write_text(json.dumps({**decision, key: value}))
                    with self.subTest(key=key), self.assertRaises(ValueError):
                        review.reviewed_claims(ROOT, views)


if __name__ == '__main__':
    unittest.main()
