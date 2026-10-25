"""A common CODE segment may use two symbol-only views, never inserted code."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from lib import binding_layout as layout
import replay_units
from test_initialized_data_replay import record


def symbols(*, comment=b'first', initialized=False, entry=False, acbp=0x28):
    raw = record(0x80, b'\x08bindings') + record(0x88, b'\0\0' + bytes([len(comment)]) + comment)
    raw += record(0x96, b'\x04TEXT\x04CODE\x00')
    raw += record(0x98, bytes([acbp]) + b'\x10\0\x01\x02\x03')
    if initialized:
        raw += record(0xa0, b'\x01\0\0\x90')
    return raw + record(0x8a, b'\x40' if entry else b'\0')


class BindingLayoutTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.entry = dict(id='u', source='src/demo.cpp', module='th05/demo.cpp',
                          bindings_source='probes/bindings.asm', bindings_after_compiler=True)

    def source(self):
        self.root.joinpath('probes').mkdir(exist_ok=True)
        self.root.joinpath('probes/bindings.asm').write_bytes(b'; one immutable conditional assembly source\n')
        self.root.joinpath('bindings.asm').write_bytes(self.root.joinpath('probes/bindings.asm').read_bytes())
        self.root.joinpath('bindings.obj').write_bytes(symbols())
        self.root.joinpath('bindings_after.obj').write_bytes(symbols(comment=b'second'))
        self.root.joinpath('compiler-arguments.json').write_text(json.dumps({'th05/demo.cpp': ['-c']}))
        self.root.joinpath('link.rsp').write_bytes(layout.link_response('demo.obj'))
        return self.root

    def result(self):
        context = layout.observe(self.source(), self.entry)
        return dict(binding_context=[context, copy.deepcopy(context)],
                    source_inputs=[dict(path=self.entry['bindings_source'], sha256=context['source_sha256'])])

    def test_legacy_default_and_explicit_profile_are_not_interchangeable(self):
        self.assertFalse(layout.after_compiler({}))
        layout.validate_result({}, {})
        for value in (1, 'true', None):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, 'boolean'):
                layout.after_compiler({'bindings_after_compiler': value})
        with self.assertRaisesRegex(ValueError, 'legacy'):
            layout.validate_result({}, self.result())

    def test_crc_checked_bindings_have_no_initialized_bytes_entry_or_32bit_segments(self):
        self.assertIn('symbol_model_sha256', layout.symbol_only(symbols()))
        for raw in (symbols(initialized=True), symbols(entry=True), symbols(acbp=0x29),
                    symbols(acbp=0x2a), symbols(acbp=0x08), symbols()[:-1] + b'\xff'):
            with self.assertRaises(ValueError):
                layout.symbol_only(raw)

    def test_only_metadata_comments_are_ignored_for_semantic_determinism(self):
        first = layout.symbol_only(symbols(comment=b'first dependency timestamp'))
        second = layout.symbol_only(symbols(comment=b'second dependency timestamp'))
        self.assertNotEqual(first['sha256'], second['sha256'])
        self.assertEqual(first['symbol_model_sha256'], second['symbol_model_sha256'])
        changed = layout.symbol_only(symbols(acbp=0x48))
        self.assertNotEqual(first['symbol_model_sha256'], changed['symbol_model_sha256'])

    def test_linker_directive_and_unknown_comments_fail_closed(self):
        for payload in (b'\0\x9e', b'\x40\xa1dosseg', b'\x40\xa2\x02', b'\x40\xe9bad'):
            raw = symbols()[:-5] + record(0x88, payload) + record(0x8a, b'\0')
            with self.assertRaisesRegex(ValueError, 'COMENT'):
                layout.symbol_only(raw)

    def test_own_cpp_negative_retains_positive_binding_models(self):
        context = self.result()['binding_context'][0]
        negative = copy.deepcopy(context)
        negative['before']['sha256'] = '1'*64
        layout.validate_control(self.entry, context, negative)
        for mutate in (lambda r: r['after'].update(symbol_model_sha256='0'*64),
                       lambda r: r.update(source_sha256='0'*64),
                       lambda r: r.update(link_response_sha256='0'*64)):
            negative = copy.deepcopy(context); mutate(negative)
            with self.assertRaises(ValueError):
                layout.validate_control(self.entry, context, negative)

    def test_observe_requires_exact_real_link_order_and_one_source_translation_unit(self):
        source = self.source(); context = layout.observe(source, self.entry)
        self.assertEqual(context['compiler_object'], 'demo.obj')
        for response in (b'-c -s -E bindings.obj bindings_after.obj demo.obj, units.exe, units.map,\r\n',
                         layout.link_response('demo.obj').replace(b'-E', b'-f -E')):
            source.joinpath('link.rsp').write_bytes(response)
            with self.assertRaisesRegex(ValueError, 'linker order'):
                layout.observe(source, self.entry)
        self.source(); source.joinpath('compiler-arguments.json').write_text(json.dumps({'th05/demo.cpp': [], 'th05/other.cpp': []}))
        with self.assertRaisesRegex(ValueError, 'translation unit'):
            layout.observe(source, self.entry)

    def test_both_views_are_tied_to_the_canonical_unchanged_binding_source(self):
        source = self.source(); source.joinpath('bindings.asm').write_bytes(b'; edited alias\n')
        with self.assertRaisesRegex(ValueError, 'canonical frozen'):
            layout.observe(source, self.entry)
        result = self.result(); result['source_inputs'][0]['sha256'] = '0'*64
        with self.assertRaisesRegex(ValueError, 'source closure'):
            layout.validate_result(self.entry, result)

    def test_two_fresh_binding_models_and_bounded_file_identities_are_mandatory(self):
        layout.validate_result(self.entry, self.result())
        for mutate in (lambda r: r['binding_context'].pop(),
                       lambda r: r['binding_context'][1]['after'].update(symbol_model_sha256='0'*64),
                       lambda r: r['binding_context'][0].update(compiler_object='other.obj'),
                       lambda r: r['binding_context'][0].update(link_response_sha256='0'*64),
                       lambda r: r['binding_context'][0]['before'].update(sha256='bad')):
            result = self.result(); mutate(result)
            with self.assertRaises(ValueError):
                layout.validate_result(self.entry, result)

    def test_context_conflicts_and_tiny_profile_fail_before_any_tool_execution(self):
        with self.assertRaisesRegex(ValueError, 'conflicting'):
            replay_units.translation_units([self.entry, {**self.entry, 'id': 'other', 'bindings_after_compiler': False}])
        with self.assertRaisesRegex(ValueError, 'large-model'):
            replay_units.cold_round(self.root/'work', self.root, [self.entry], paths=set(), binary=None)
        self.assertFalse(self.root.joinpath('work').exists())


if __name__ == '__main__':
    unittest.main()
