"""Complete class-library CODE provenance never grants authored-source credit."""
import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import review_string_runtime as review


class StringRuntimeOwnershipTests(unittest.TestCase):
    def proof(self):
        return json.loads((ROOT / review.PROOF).read_text())

    def test_complete_six_contributions_and_no_authored_denominator(self):
        result = review.validate_metadata(self.proof())
        self.assertEqual(result, dict(contributions=6, bytes=4034,
                                     authored_credit=0, byte_proof_replayed=False))
        rows = self.proof()['contributions']
        self.assertEqual({r['segment'] for r in rows}, {'_TEXT', '_TEXTC'})
        self.assertEqual(sum(len(r['native']['fixup_actions']) for r in rows), 209)
        self.assertEqual(sum(len(r['native']['ordered_MZ_fixups']) for r in rows), 131)

    def test_all_relaxation_nops_are_uncredited_and_metadata_is_not_an_instruction(self):
        rows = self.proof()['contributions']
        self.assertEqual(sum(len(r['native_nops']['instruction_nop_offsets']) for r in rows), 28)
        self.assertTrue(all(r['native_nops']['uncredited'] for r in rows))
        self.assertEqual([(r['member'], r['segment'], n['offset']) for r in rows
                          for n in r['native_nops']['nonopcode_90']],
                         [('ctor3', '_TEXTC', 203), ('strings', '_TEXT', 526)])
        bad = self.proof()
        bad['contributions'][3]['native_nops']['instruction_nop_offsets'].append(203)
        with self.assertRaises(ValueError):
            review.validate_metadata(bad)

    def test_binding_model_credit_types_and_pins_are_fixed(self):
        for key, value in [('authored_credit', 1), ('authored_credit', False),
                           ('compiler_invocations', False), ('schema_version', True),
                           ('authored_denominator', 4034)]:
            bad = self.proof()
            bad[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                review.validate_metadata(bad)
        for section, key in [('binding_model', 'offset_change'), ('inputs', 'library_sha256')]:
            bad = self.proof()
            bad[section][key] = 0
            with self.assertRaises(ValueError):
                review.validate_metadata(bad)

    def test_no_selected_function_slice_or_data_can_replace_a_code_contribution(self):
        for key, value in [('start', 0), ('size', 232), ('class_name', 'DATA')]:
            bad = self.proof()
            bad['contributions'][1]['native'][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                review.validate_metadata(bad)
        bad = self.proof()
        bad['contributions'].pop()
        with self.assertRaises(ValueError):
            review.validate_metadata(bad)

    def test_reversing_both_mz_lists_still_disagrees_with_original_omf_order(self):
        bad = self.proof()
        for side in ('native', 'calibration'):
            bad['contributions'][1][side]['ordered_MZ_fixups'].reverse()
        with self.assertRaises(ValueError):
            review.validate_metadata(bad)

    def test_incomplete_ledata_and_overlapping_fixup_writes_fail(self):
        for operation in ('gap', 'overlap'):
            bad = self.proof()
            for side in ('native', 'calibration'):
                row = bad['contributions'][0][side]
                if operation == 'gap':
                    row['CODE_LEDATA'][0]['offset'] = 1
                else:
                    row['fixup_actions'][1]['write_start'] = row['fixup_actions'][0]['write_start']
            with self.subTest(operation=operation), self.assertRaises(ValueError):
                review.validate_metadata(bad)

    def test_every_scope_keeps_its_own_object_model_negative(self):
        bad = self.proof()
        bad['negatives'].pop()
        with self.assertRaises(ValueError):
            review.validate_metadata(bad)
        bad = self.proof()
        bad['contributions'][0]['native']['linked_CODE_sha256'] = 'malformed'
        with self.assertRaises(ValueError):
            review.validate_metadata(bad)

    def test_constructor_frame_anchors_cannot_be_rebased_or_duplicated(self):
        for operation in ('frame', 'duplicate'):
            bad = self.proof()
            if operation == 'frame':
                bad['native_far_call_anchors'][0]['frame'] += 16
            else:
                bad['native_far_call_anchors'].append(copy.deepcopy(bad['native_far_call_anchors'][0]))
            with self.subTest(operation=operation), self.assertRaises(ValueError):
                review.validate_metadata(bad)

    def test_explicit_adoption_cannot_broaden_or_claim_source_credit(self):
        views = tomllib.loads((ROOT / 'config/ownership.toml').read_text())['views']
        claims, _ = review.reviewed_claims(ROOT, views)
        self.assertEqual(sum(c['end']-c['start'] for c in claims), 4034)
        self.assertTrue(all(c['kind'] == 'verified-vendor-code' for c in claims))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in (*review.SOURCES, review.PROOF, review.DECISION, review.NOTES):
                dst = root / name
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / name, dst)
            original = json.loads((root / review.DECISION).read_text())
            for operation in ('credit', 'extent', 'evidence'):
                bad = copy.deepcopy(original)
                if operation == 'credit':
                    bad['authored_credit'] = 4034
                elif operation == 'extent':
                    bad['scopes'][0]['start'] -= 1
                else:
                    bad['evidence_sha256'] = '0'*64
                (root / review.DECISION).write_text(json.dumps(bad))
                with self.subTest(operation=operation), self.assertRaises(ValueError):
                    review.reviewed_claims(root, views)


if __name__ == '__main__':
    unittest.main()
