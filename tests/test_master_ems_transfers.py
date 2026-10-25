"""Fixed frame names never authorize source edits or authored-byte credit."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import review_master_ems_transfers as review

# Synthetic symbol inventory, not a vendor procedure or target instruction body.
SOURCE = ('func FRAME_TEST\n'
          'handle = (RETSIZE+7)*2\noffs = (RETSIZE+5)*2\n'
          'mem = (RETSIZE+3)*2\nlen = (RETSIZE+1)*2\nblock = -18\n' +
          ''.join('\tmov AX,[BP+'+name+']\n' for name, count in
                  [('handle', 1), ('offs', 2), ('mem', 2), ('len', 2), ('block', 11)] for _ in range(count)) +
          '; handle and block stay literal in comments\nendfunc')


class FrameNamesTests(unittest.TestCase):
    def test_only_five_defined_frame_identifiers_change(self):
        result, counts = review.rename_frame_equates(SOURCE)
        self.assertEqual(counts, {'handle': 2, 'offs': 3, 'mem': 3, 'len': 3, 'block': 12})
        self.assertIn('@@handle = (RETSIZE+7)*2', result)
        self.assertIn('[BP+@@block]', result)
        self.assertIn('; handle and block stay literal in comments', result)
        self.assertEqual(review.verify_frame_equivalence(SOURCE, result), counts)

    def test_changed_expressions_missing_and_duplicate_definitions_fail(self):
        for text in (SOURCE.replace('(RETSIZE+7)*2', '(RETSIZE+6)*2'),
                     SOURCE.replace('block = -18', 'block = -20'),
                     SOURCE.replace('len = (RETSIZE+1)*2\n', ''),
                     SOURCE+'\nlen = (RETSIZE+1)*2',
                     SOURCE.replace('handle =', 'handle EQU'),
                     SOURCE.replace('block = -18', 'block:')):
            with self.subTest(text=text), self.assertRaisesRegex(ValueError, 'definition'):
                review.rename_frame_equates(text)

    def test_collisions_extra_references_or_exports_fail(self):
        for text in (SOURCE+'\n@@handle = 42', SOURCE+'\nmov AX,[BP+len]',
                     SOURCE+'\nPUBLIC block', SOURCE.replace('mov AX,[BP+handle]', 'mov AX,[BP+handle2]')):
            with self.subTest(text=text), self.assertRaises(ValueError):
                review.rename_frame_equates(text)

    def test_instructions_comments_case_and_whitespace_cannot_be_normalized(self):
        transformed, _ = review.rename_frame_equates(SOURCE)
        for changed in (transformed.replace('mov AX', 'mov BX', 1),
                        transformed.replace('; handle and', '; different'),
                        transformed.replace('\tmov', ' mov', 1),
                        transformed.replace('[BP+', '[bp+', 1),
                        transformed.replace('RETSIZE+7', 'RETSIZE+8', 1)):
            with self.subTest(changed=changed), self.assertRaisesRegex(ValueError, 'complete source'):
                review.verify_frame_equivalence(SOURCE, changed)

    def test_quoted_code_is_not_a_substitution_surface(self):
        with self.assertRaisesRegex(ValueError, 'quoted'):
            review.rename_frame_equates(SOURCE+'\ndb "handle;block"')
        with self.assertRaisesRegex(ValueError, 'quoted'):
            review.rename_frame_equates(SOURCE+"\ndb 'x'")
        review.rename_frame_equates(SOURCE+'\n; "handle" in a comment')


class FrozenEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.meta = json.loads((ROOT / review.PROOF).read_text())

    def test_public_metadata_checks_without_private_archive_or_game(self):
        review.validate_metadata(self.meta)
        self.assertEqual([(r['start'], r['end']) for r in self.meta['procedures']],
                         [(0x3f6a, 0x3fcc), (0x406c, 0x40ce)])
        self.assertEqual(self.meta['full_bytes'], 196)

    def test_changed_scope_source_proof_byte_order_or_credit_fail(self):
        for mutate in (lambda r: r.update(authored_credit=196),
                       lambda r: r.update(authored_denominator=196),
                       lambda r: r.update(compiler_invocations=1),
                       lambda r: r['procedures'][0].update(start=0x3f6b),
                       lambda r: r['procedures'][0].update(linked_sha256='0'*64),
                       lambda r: r['procedures'][0]['frame_equates'].update(block='-20'),
                       lambda r: r['procedures'][0]['renames'].update(AX='BX'),
                       lambda r: r['procedures'][0].update(ordered_mz_fixups=[1]),
                       lambda r: r['procedures'][0]['calls'].reverse(),
                       lambda r: r['procedures'][0].update(padding=[{'start': 0x3f6a}])):
            changed = copy.deepcopy(self.meta); mutate(changed)
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                review.validate_metadata(changed)

    def test_reviewer_source_edits_stale_the_proof(self):
        changed = copy.deepcopy(self.meta)
        changed['reviewer_sources'][0]['sha256'] = '0'*64
        with self.assertRaisesRegex(ValueError, 'reviewer source'):
            review.validate_metadata(changed)

    def test_explicit_adoption_binds_only_complete_vendor_scopes(self):
        raw = (ROOT / review.PROOF).read_bytes()
        inherited = json.loads((ROOT / review.BASE).read_text())
        views = {'main': {'sha256': inherited['target_payload_sha256']}}
        decision = dict(schema_version=1, decision='ADOPT', classification='verified-vendor-code',
                        proof_sha256=review.sha(raw), base_proof_sha256=review.BASE_SHA,
                        target_sha256=inherited['inputs']['target']['sha256'], full_bytes=196,
                        authored_credit=0, authored_denominator=None,
                        procedures=['EMS_READ', 'EMS_WRITE'])
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'decision.json'
            with patch.object(review, 'DECISION', str(path)):
                self.assertEqual(review.reviewed_claims(ROOT, {}), ([], None))
                path.write_text(json.dumps(decision))
                claims, _ = review.reviewed_claims(ROOT, views)
                self.assertEqual(sum(r['end']-r['start'] for r in claims), 196)
                self.assertEqual({r['kind'] for r in claims}, {'verified-vendor-code'})
                for field, value in [('proof_sha256', '0'*64), ('full_bytes', 195),
                                     ('authored_credit', 196), ('authored_denominator', 196),
                                     ('procedures', ['EMS_READ']), ('target_sha256', '0'*64)]:
                    path.write_text(json.dumps({**decision, field: value}))
                    with self.subTest(field=field), self.assertRaises(ValueError):
                        review.reviewed_claims(ROOT, views)
                path.write_text(json.dumps(decision))
                with self.assertRaisesRegex(ValueError, 'target payload'):
                    review.reviewed_claims(ROOT, {'main': {'sha256': '0'*64}})


if __name__ == '__main__':
    unittest.main()
