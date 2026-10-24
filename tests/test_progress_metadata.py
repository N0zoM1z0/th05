"""Synthetic classification controls never waive complete raw-byte exactness."""
import copy
import json
from pathlib import Path
import sys
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from progress import classify_extent, render, summarize, validate_result


def sample_entry():
    return {'size': 64, 'alignment_offsets': [63],
            'padding_bytes': [{'offset': 2, 'value': 0}, {'offset': 13, 'value': 0}],
            'code_data_ranges': [
                {'offset': 8, 'size': 4, 'kind': 'compiler-switch-table'},
                {'offset': 32, 'size': 4, 'kind': 'compiler-switch-table'}]}


class ExtentMetadataTests(unittest.TestCase):
    def test_legacy_nop_metadata_preserves_previous_instruction_credit(self):
        entry = {'size': 30, 'alignment_offsets': [29]}
        self.assertEqual(classify_extent(entry), {'authored_code_bytes': 29,
            'instruction_bytes': 29, 'code_data_bytes': 0, 'padding_bytes': 1})
        raw = bytes(29) + b'\x90'
        classify_extent(entry, target_bytes=raw)
        with self.assertRaisesRegex(ValueError, 'original target'):
            classify_extent(entry, target_bytes=bytes(30))
        self.assertEqual(entry, {'size': 30, 'alignment_offsets': [29]})

    def test_tables_are_authored_code_but_not_instruction_bytes(self):
        result = classify_extent(sample_entry())
        self.assertEqual(result, {'authored_code_bytes': 61, 'instruction_bytes': 53,
                                  'code_data_bytes': 8, 'padding_bytes': 3})
        self.assertEqual(result['authored_code_bytes'] + result['padding_bytes'], 64)
        self.assertEqual(result['instruction_bytes'] + result['code_data_bytes'],
                         result['authored_code_bytes'])

    def test_non_nop_padding_must_match_declared_real_target_value(self):
        entry = sample_entry()
        raw = bytearray(64)
        raw[63] = 0x90
        classify_extent(entry, target_bytes=bytes(raw))
        raw[2] = 0x90
        with self.assertRaisesRegex(ValueError, 'original target'):
            classify_extent(entry, target_bytes=bytes(raw))
        with self.assertRaisesRegex(ValueError, 'complete original extent'):
            classify_extent(entry, target_bytes=bytes(raw[:-1]))

    def test_overlapping_or_duplicate_table_ranges_are_rejected(self):
        for start in (8, 9, 11):
            with self.subTest(start=start):
                entry = sample_entry()
                entry['code_data_ranges'].append(
                    {'offset': start, 'size': 2, 'kind': 'compiler-switch-table'})
                with self.assertRaisesRegex(ValueError, 'overlap'):
                    classify_extent(entry)

    def test_out_of_bounds_and_empty_tables_are_rejected(self):
        for start, size in [(-1, 2), (64, 2), (63, 2), (1, 0), (1, -1), (1.0, 2), (1, True)]:
            with self.subTest(start=start, size=size):
                entry = {'size': 64, 'code_data_ranges': [
                    {'offset': start, 'size': size, 'kind': 'compiler-switch-table'}]}
                with self.assertRaises(ValueError):
                    classify_extent(entry)

    def test_duplicate_padding_including_legacy_aliases_is_rejected(self):
        cases = [
            {'size': 64, 'alignment_offsets': [4, 4]},
            {'size': 64, 'padding_bytes': [{'offset': 4, 'value': 0}, {'offset': 4, 'value': 0}]},
            {'size': 64, 'alignment_offsets': [4], 'padding_bytes': [{'offset': 4, 'value': 0x90}]},
            {'size': 64, 'alignment_offsets': [4], 'padding_bytes': [{'offset': 4, 'value': 0}]},
        ]
        for entry in cases:
            with self.subTest(entry=entry):
                with self.assertRaisesRegex(ValueError, 'duplicate'):
                    classify_extent(entry)

    def test_padding_and_tables_are_mutually_exclusive_with_half_open_edges(self):
        for offset in range(8, 12):
            with self.subTest(offset=offset):
                entry = sample_entry()
                entry['padding_bytes'].append({'offset': offset, 'value': 0})
                with self.assertRaisesRegex(ValueError, 'overlap'):
                    classify_extent(entry)
        entry = sample_entry()
        entry['padding_bytes'].extend([{'offset': 7, 'value': 0}, {'offset': 12, 'value': 0}])
        classify_extent(entry)

    def test_padding_values_and_offsets_are_strict_bytes(self):
        for offset, value in [(-1, 0), (64, 0), (True, 0), (1, -1), (1, 256), (1, False), (1, '00')]:
            with self.subTest(offset=offset, value=value):
                with self.assertRaises(ValueError):
                    classify_extent({'size': 64, 'padding_bytes': [{'offset': offset, 'value': value}]})

    def test_assets_and_raw_exemption_directives_are_not_table_metadata(self):
        for kind in ['asset-array', 'game-data', 'unknown', 'padding', None]:
            with self.subTest(kind=kind):
                with self.assertRaisesRegex(ValueError, 'only compiler-switch-table'):
                    classify_extent({'size': 64, 'code_data_ranges': [
                        {'offset': 8, 'size': 4, 'kind': kind}]})
        for key in ['raw_exempt', 'skip_bytes', 'ignore_fixups']:
            with self.subTest(key=key):
                table = {'offset': 8, 'size': 4, 'kind': 'compiler-switch-table', key: True}
                with self.assertRaises(ValueError):
                    classify_extent({'size': 64, 'code_data_ranges': [table]})
        with self.assertRaisesRegex(ValueError, 'instruction bytes'):
            classify_extent({'size': 64, 'code_data_ranges': [
                {'offset': 0, 'size': 64, 'kind': 'compiler-switch-table'}]})

    def test_classification_metadata_cannot_waive_failed_complete_raw_digest(self):
        config = tomllib.loads((ROOT / 'config/exact_units.toml').read_text())
        accepted = json.loads((ROOT / 'config/accepted_units.json').read_text())['units'][0]
        entry = copy.deepcopy(next(row for row in config['units'] if row['id'] == accepted['id']))
        entry['code_data_ranges'] = [{'offset': 0, 'size': 2, 'kind': 'compiler-switch-table'}]
        result = copy.deepcopy(accepted['result'])
        validate_result(entry, result)
        result['rounds'][0]['candidate_sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'raw bytes'):
            validate_result(entry, result)

    def test_summary_exposes_all_counts_without_establishing_global_denominator(self):
        summary = summarize(ROOT)
        self.assertEqual(summary['authored_code_bytes'] + summary['padding_bytes'],
                         summary['complete_extent_bytes'])
        self.assertEqual(summary['instruction_bytes'] + summary['code_data_bytes'],
                         summary['authored_code_bytes'])
        self.assertEqual(summary['code_data_bytes'], sum(row['code_data_bytes'] for row in summary['units']))
        self.assertIsNone(summary['percentage'])
        self.assertIsNone(summary['authored_denominator'])

    def test_render_prioritizes_authored_code_and_keeps_instruction_table_counts_separate(self):
        summary = {'unit_count': 8, 'functions': 36, 'complete_extent_bytes': 6099,
                   'authored_code_bytes': 6088, 'instruction_bytes': 5972,
                   'code_data_bytes': 116, 'padding_bytes': 11}
        markdown, svg = render(summary)
        self.assertIn('| MAIN bounded C++ units | 36 | 6088 | 5972 | 116 | 6099 |', markdown)
        self.assertIn('6088 authored code bytes', svg)
        self.assertIn('5972 instruction', svg)
        self.assertIn('116 compiler switch-table', svg)
        self.assertIn('11 padding bytes', svg)
        self.assertIn('no byte-comparison exemption', markdown)
        self.assertIn('Global percentage: **unmeasured**', markdown)


if __name__ == '__main__':
    unittest.main()
