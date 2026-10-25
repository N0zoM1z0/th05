"""Unchanged original-source vendor proof cannot grant authored credit."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import review_master_primary_circlefill as review


def synthetic_object(changes=None, extra=None):
    """CRC-valid OMF container with synthetic INT3 bytes, never target code."""
    fields = [('header', 0x80, b'\x0cGC_CIRCF.ASM'), ('comment1', 0x88, b'\x40\xa1'),
              ('names1', 0x96, b'\0'), ('names2', 0x96, b'\x05_TEXT\x04CODE'),
              ('names3', 0x96, b'\x05_DATA\x04DATA'), ('names4', 0x96, b'\x06DGROUP'),
              ('code', 0x98, b'\x48\x96\0\x02\x03\x01'),
              ('data', 0x98, b'\x48\0\0\x04\x05\x01'), ('group', 0x9a, b'\x06\xff\x02'),
              ('external', 0x8c, b'\x0aGRCG_HLINE\0\x09GRCG_PSET\0'),
              ('public', 0x90, b'\0\x01\x0fGRCG_CIRCLEFILL\0\0\0'),
              ('bytes', 0xa0, b'\x01\0\0'+b'\xcc'*150),
              ('fixups', 0x9c, b''.join(bytes([0x84, at, 6, 1, target]) for at, target in
                                      [(40, 1), (61, 1), (92, 1), (113, 1), (142, 2)])),
              ('comment2', 0x88, b'\x40\xa2\x01'), ('end', 0x8a, b'\0')]
    if extra:
        fields.insert(-1, extra)
    out = bytearray()
    for name, kind, data in fields:
        data = (changes or {}).get(name, data)
        head = bytes([kind])+(len(data)+1).to_bytes(2, 'little')
        out.extend(head+data+bytes([(-sum(head+data)) & 255]))
    return bytes(out)


class OriginalInputTests(unittest.TestCase):
    def test_positive_bytes_are_returned_without_text_or_encoding_changes(self):
        raw = b'\x82\xa0; synthetic comment\r\n\tmov\tDI,0\r\n'
        self.assertIs(review.source_input(raw, False), raw)
        self.assertEqual(review.source_input(raw, True),
                         b'\x82\xa0; synthetic comment\r\n\tmov\tDI,1\r\n')

    def test_negative_marker_must_be_unique(self):
        for raw in (b'nothing to mutate', b'mov\tDI,0\nmov\tDI,0'):
            with self.assertRaisesRegex(ValueError, 'unique'):
                review.source_input(raw, True)

    def test_original_quiet_object_container_requires_complete_code(self):
        scope = review.object_shape(synthetic_object())
        self.assertEqual((scope['segment'], scope['size'], scope['ledata'][0]['size']),
                         ('_TEXT', 150, 150))

    def test_crc_valid_segment_relocation_and_coverage_tampering_fail(self):
        fixups = b''.join(bytes([0x84, at, 6, 1, target]) for at, target in
                         [(41, 1), (61, 1), (92, 1), (113, 1), (142, 2)])
        for obj in (synthetic_object({'code': b'\x48\x95\0\x02\x03\x01'}),
                    synthetic_object({'data': b'\x48\x01\0\x04\x05\x01'}),
                    synthetic_object({'fixups': fixups}),
                    synthetic_object({'bytes': b'\x01\0\0'+b'\xcc'*149}),
                    synthetic_object({'comment1': b'\x40\xa0'}),
                    synthetic_object(extra=('extra', 0xa0, b'\x01\0\0\xcc'))):
            review.parse_omf(obj)  # Reject the profile, not a broken checksum.
            with self.subTest(obj=obj), self.assertRaises(ValueError):
                review.object_shape(obj)


class FrozenPrimaryTests(unittest.TestCase):
    def setUp(self):
        self.meta = json.loads((ROOT/review.PROOF).read_text())

    def test_public_structural_check_does_not_read_private_sources(self):
        pinned = review.base.pinned
        def public_only(root, row):
            self.assertTrue(row['file'].startswith('scripts/'))
            return pinned(root, row)
        with patch.object(review.base, 'pinned', side_effect=public_only), \
                patch.object(review, 'primary_inputs', side_effect=AssertionError('private archive read')):
            review.validate_metadata(self.meta)
        self.assertEqual(self.meta['source_transformations'], [])
        self.assertEqual(self.meta['negative_changed_offsets'], [19])
        self.assertEqual(self.meta['size'], 150)

    def test_source_flags_scope_results_or_credit_cannot_be_changed(self):
        for mutate in (lambda m: m.update(authored_credit=150),
                       lambda m: m.update(authored_denominator=150),
                       lambda m: m.update(size=149),
                       lambda m: m.update(start=0x100f),
                       lambda m: m['source_flags'].append('/DNEARMODEL'),
                       lambda m: m['source_transformations'].append('word ptr insertion'),
                       lambda m: m['primary_inputs'].update({'GC_CIRCF.ASM': '0'*64}),
                       lambda m: m['rounds'][0]['observation']['comparison'].update(raw_exact=False),
                       lambda m: m['rounds'][0]['observation']['comparison'].update(target_fixups=[2]),
                       lambda m: m['rounds'][2]['observation']['comparison'].update(exact=True)):
            changed = copy.deepcopy(self.meta); mutate(changed)
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                review.validate_metadata(changed)

    def test_raw_original_object_and_raw_linked_outputs_are_pinned(self):
        for key in ('original_object_raw', 'map_raw', 'mz_raw'):
            changed = copy.deepcopy(self.meta)
            changed['rounds'][1]['observation']['deterministic_identity'][key] = '0'*64
            with self.subTest(key=key), self.assertRaises(ValueError):
                review.validate_metadata(changed)
        changed = copy.deepcopy(self.meta)
        changed['rounds'][0]['observation']['artifacts']['before.obj'] = '0'*64
        with self.assertRaises(ValueError):
            review.validate_metadata(changed)

    def test_reviewer_source_edits_stale_the_proof(self):
        changed = copy.deepcopy(self.meta)
        changed['reviewer_sources'][0]['sha256'] = '0'*64
        with self.assertRaisesRegex(ValueError, 'reviewer source'):
            review.validate_metadata(changed)

    def test_only_an_explicit_whole_vendor_decision_produces_claims(self):
        raw = (ROOT/review.PROOF).read_bytes()
        inherited = json.loads((ROOT/review.BASE).read_text())
        views = {'main': {'sha256': inherited['target_payload_sha256']}}
        decision = dict(schema_version=1, decision='ADOPT', classification='verified-vendor-code',
                        proof_sha256=review.sha(raw), base_proof_sha256=review.BASE_SHA,
                        target_sha256=self.meta['target_sha256'], start=0x100e, size=150,
                        procedure='GRCG_CIRCLEFILL', authored_credit=0, authored_denominator=None)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'decision.json'
            with patch.object(review, 'DECISION', str(path)):
                self.assertEqual(review.reviewed_claims(ROOT, {}), ([], None))
                path.write_text(json.dumps(decision))
                claims, _ = review.reviewed_claims(ROOT, views)
                self.assertEqual([(r['start'], r['end'], r['kind']) for r in claims],
                                 [(0x100e, 0x10a4, 'verified-vendor-code')])
                for key, value in [('proof_sha256', '0'*64), ('size', 149), ('authored_credit', 150),
                                   ('authored_denominator', 150), ('procedure', 'GRCG_CIRCLE')]:
                    path.write_text(json.dumps({**decision, key: value}))
                    with self.subTest(key=key), self.assertRaises(ValueError):
                        review.reviewed_claims(ROOT, views)
                path.write_text(json.dumps(decision))
                with self.assertRaisesRegex(ValueError, 'target payload'):
                    review.reviewed_claims(ROOT, {'main': {'sha256': '0'*64}})


if __name__ == '__main__':
    unittest.main()
