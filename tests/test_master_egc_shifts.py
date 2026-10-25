"""Source identity remains strict except for seven explicitly reviewed names."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import review_master_egc_shifts as review

SOURCE = 'func TEST\npatch EQU $-1\nnext_line:\tmov AX, CS:[patch] ; patch stays in comment\n\tjne next_line\nendfunc\n'
RENAMES = {'patch': 'test_patch', 'next_line': '@@next_line'}


class PrivateSymbolTests(unittest.TestCase):
    def test_only_named_defined_identifiers_change(self):
        result, counts = review.rename_private_symbols(SOURCE, RENAMES)
        self.assertEqual(result, 'func TEST\ntest_patch EQU $-1\n@@next_line:\tmov AX, CS:[test_patch] ; patch stays in comment\n\tjne @@next_line\nendfunc\n')
        self.assertEqual(counts, {'patch': 2, 'next_line': 2})

    def test_code_tokens_and_public_or_unknown_names_cannot_be_renamed(self):
        for names in ({'AX': 'BX'}, {'TEST': 'OTHER'}, {'unknown': 'alias'}):
            with self.subTest(names=names), self.assertRaises(ValueError):
                review.rename_private_symbols(SOURCE, names)

    def test_collisions_nonbijective_and_unused_definitions_fail(self):
        for text, names in ((SOURCE, {'patch': 'TEST'}),
                            (SOURCE, {'patch': 'alias', 'next_line': 'alias'}),
                            (SOURCE+'unused:\n', {'unused': '@@unused'}),
                            (SOURCE.replace('$-1', '16'), {'patch': 'test_patch'})):
            with self.subTest(names=names), self.assertRaises(ValueError):
                review.rename_private_symbols(text, names)

    def test_strings_are_not_a_general_source_normalization_surface(self):
        with self.assertRaisesRegex(ValueError, 'quoted'):
            review.rename_private_symbols(SOURCE+'db "patch"\n', RENAMES)
        transformed, _ = review.rename_private_symbols(SOURCE, RENAMES)
        review.verify_private_symbol_equivalence(SOURCE, transformed, RENAMES)
        for changed in (transformed.replace('mov AX', 'mov BX'),
                        transformed.replace('; patch stays', '; edited'),
                        transformed.replace('\tmov', ' mov')):
            with self.assertRaisesRegex(ValueError, 'complete source'):
                review.verify_private_symbol_equivalence(SOURCE, changed, RENAMES)


class FrozenEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.meta = json.loads((ROOT / review.PROOF).read_text())

    def test_public_metadata_uses_no_private_inputs(self):
        review.validate_metadata(self.meta)
        self.assertEqual(sum(x['size'] for x in self.meta['procedures']), 1048)
        self.assertEqual(self.meta['authored_credit'], 0)

    def test_altered_scope_byte_proof_padding_or_policy_is_not_relabelled(self):
        for mutate in (lambda r: r.update(authored_credit=1048),
                       lambda r: r.update(authored_denominator=1048),
                       lambda r: r.update(compiler_invocations=1),
                       lambda r: r['procedures'][0].update(start=0x8ab),
                       lambda r: r['procedures'][0]['renames'].update(AX='BX'),
                       lambda r: r['procedures'][0].update(ordered_mz_fixups=[1]),
                       lambda r: r['procedures'][0]['padding'][0].update(value=0),
                       lambda r: r['procedures'][0].update(linked_sha256='0'*64)):
            row = copy.deepcopy(self.meta); mutate(row)
            with self.assertRaises(ValueError):
                review.validate_metadata(row)

    def test_source_edits_stale_the_public_review(self):
        row = copy.deepcopy(self.meta)
        row['reviewer_sources'][0]['sha256'] = '0'*64
        with self.assertRaisesRegex(ValueError, 'reviewer source'):
            review.validate_metadata(row)

    def test_adoption_binds_complete_proof_and_never_grants_authored_credit(self):
        raw = (ROOT / review.PROOF).read_bytes()
        base = json.loads((ROOT / review.BASE).read_text())
        target = base['inputs']['target']['sha256']
        views = {'main': {'sha256': base['target_payload_sha256']}}
        decision = dict(schema_version=1, decision='ADOPT', classification='verified-vendor-code',
                        proof_sha256=review.sha(raw), base_proof_sha256=review.BASE_SHA,
                        target_sha256=target, full_bytes=1048, authored_credit=0,
                        authored_denominator=None, procedures=[r['name'] for r in self.meta['procedures']])
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'decision.json'
            with patch.object(review, 'DECISION', str(path)):
                self.assertEqual(review.reviewed_claims(ROOT, {}), ([], None))
                path.write_text(json.dumps(decision))
                claims, _ = review.reviewed_claims(ROOT, views)
                self.assertEqual(sum(c['end']-c['start'] for c in claims), 1048)
                self.assertEqual({c['kind'] for c in claims}, {'verified-vendor-code'})
                for key, value in (('proof_sha256', '0'*64), ('authored_credit', 1048), ('authored_denominator', 1048)):
                    changed = {**decision, key: value}; path.write_text(json.dumps(changed))
                    with self.assertRaises(ValueError):
                        review.reviewed_claims(ROOT, views)


if __name__ == '__main__':
    unittest.main()
