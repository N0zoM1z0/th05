"""Retained positives remain immutable; only a real DATA-specific negative builds."""
import copy
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import progress
import replay_units
import review_saved_data as review
from lib.pc98 import parse_mz
from lib.replay_toolchain import digest, entry_digest, snapshot_paths
from lib.unit_context import compiler_arguments
from lib.unit_oracle import compare_mapped_unit
from lib.unit_sources import producer_snapshot
from test_initialized_data_replay import object_bytes, executable, record
from lib.omf import parse_omf


def manifest(config):
    lines = ['artifact = "th05-main"']
    for table in ('units', 'controls'):
        for row in config.get(table, []):
            lines += ['[[' + table + ']]']
            lines += [key + ' = ' + json.dumps(value) for key, value in row.items()]
    return '\n'.join(lines) + '\n'


def object_code(data, code):
    out = b''
    for row in parse_omf(object_bytes(data)):
        payload = row.data
        if row.record_type == 0xA0 and payload[:1] == b'\1':
            payload = payload[:-1] + bytes([code])
        out += record(row.record_type, payload)
    return out


class SavedDataTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.parent = self.root / '.analysis/parent'
        self.output = self.root / '.analysis/data-review'
        for name in ('src', 'probes', 'config', '.analysis/toolchain'):
            (self.root / name).mkdir(parents=True)
        self.canonical = 'const char caption[] = "開始";\nint marker = 8;\nvoid far owner(void) {}\n'
        (self.root / 'src/owner.cpp').write_text(self.canonical)
        (self.root / 'probes/bindings.asm').write_text('.386\nend\n')
        common = {'source': 'src/owner.cpp', 'module': 'th05/owner.cpp',
                  'source_encoding': 'cp932', 'bindings_source': 'probes/bindings.asm',
                  'origin': 'compiler-generated-cxx'}
        self.code = {**common, 'id': 'code', 'segment': 'OWNER_TEXT', 'target_start': 0,
                     'size': 1, 'functions': 1}
        self.data = {**common, 'id': 'data', 'segment': '_DATA', 'target_start': 16,
                     'size': 10, 'functions': 0, 'extent_kind': 'initialized-data',
                     'data_semantics': ['ui-text', 'function-pointers', 'state']}
        self.code_mutation = {'unit': 'code', 'source': 'src/owner.cpp',
                              'find': 'marker = 8', 'replace': 'marker = 7'}
        self.data_mutation = {'unit': 'data', 'source': 'src/owner.cpp',
                              'find': '開始', 'replace': '終了'}
        self.config = {'artifact': 'th05-main', 'units': [self.code, self.data],
                       'controls': [self.code_mutation, self.data_mutation]}
        (self.root / 'config/exact_units.toml').write_text(manifest(self.config))
        (self.root / 'config/toolchain.toml').write_text('# immutable synthetic tool pin\n')
        self.tool_sha = digest(self.root / 'config/toolchain.toml')
        tool = {'ready': True, 'identity_pass': True, 'execution_pass': True,
                'execution': {'pass': True}, 'surfaces': [], 'selected_surface_ids': [],
                'manifest_sha256': self.tool_sha}
        (self.root / '.analysis/toolchain/attestation.json').write_text(json.dumps(tool))
        self.calls = []
        self.code_only_negative = False
        case = self

        class FakeBuilder:
            def __init__(self, source, prefix, msdos):
                self.source, self.msdos, self.records = source, msdos, []

            def execute(self, label, command):
                self.records.append({'output': label, 'command': command, 'returncode': 0})
                if 'tcc' in command:
                    case.calls.append(command)
                    raw = (self.source / 'src/owner.cpp').read_bytes()
                    caption = raw.split(b'"')[1]
                    self.code = 0xCB if b'marker = 8' in raw else 0xCA
                    if case.code_only_negative and caption != '開始'.encode('cp932'):
                        caption, self.code = '開始'.encode('cp932'), 0xCA
                    self.data = bytes(4) + caption + b'\0\1'
                    (self.source / label).write_bytes(object_code(self.data, self.code))
                elif label == 'bindings':
                    (self.source / 'bindings.obj').write_bytes(b'synthetic symbol-only binder')
                elif label == 'link':
                    mz = bytearray(executable(self.data));mz[48] = self.code
                    (self.source / 'units.exe').write_bytes(mz)
                    (self.source / 'units.map').write_text(
                        ' 0000:0000 0001 C=CODE S=OWNER_TEXT G=OWN M=th05/owner.cpp ACBP=28\n'
                        ' 0000:0010 000A C=DATA S=_DATA G=DGROUP M=th05/owner.cpp ACBP=48\n')

        self.addCleanup(patch.stopall)
        patch.object(replay_units, 'ROOT', self.root).start()
        patch.object(replay_units, 'Builder', FakeBuilder).start()
        patch('lib.replay_toolchain.static_toolchain', return_value=(self.tool_sha, [])).start()
        patch.object(review, 'static_toolchain', return_value=(self.tool_sha, [])).start()
        paths = {'src/owner.cpp', 'probes/bindings.asm'}
        self.parent.mkdir(parents=True)
        from lib.replay_toolchain import freeze_toolchain
        tool_identity = freeze_toolchain(self.root, self.parent / 'toolchain-attestation.json', allow_probes=False)
        (self.parent / 'toolchain.toml').write_bytes((self.root / 'config/toolchain.toml').read_bytes())
        (self.parent / 'exact-units.toml').write_text(manifest({'units': [self.code], 'controls': [self.code_mutation]}))
        for name in paths:
            dst = self.parent / 'inputs' / name;dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes((self.root / name).read_bytes())
        self.rounds = [replay_units.cold_round(self.parent / label, self.parent / 'inputs', [self.code], paths=paths)
                       for label in ('a', 'b')]
        negative = replay_units.cold_round(self.parent / 'negative', self.parent / 'inputs', [self.code],
                                           paths=paths, mutation=self.code_mutation)
        self.target = self.rounds[0]['candidate']
        self.artifact = {'sha256': digest(self.rounds[0]['source'] / 'units.exe')}
        (self.root / 'config/targets.toml').write_text('[[artifacts]]\nid="th05-main"\nsha256="' + self.artifact['sha256'] + '"\n')
        patch.object(progress, 'load_unit_target', return_value=(self.artifact, self.target, None)).start()
        patch.object(review, 'load_unit_target', return_value=(self.artifact, self.target, None)).start()
        snapshots = snapshot_paths(self.root, paths)
        comparisons = [compare_mapped_unit(self.target, r['candidate'], r['source'] / 'units.map', self.code)
                       for r in self.rounds]
        control = replay_units.mapped_control_comparison(self.target, negative['candidate'], self.code,
                                                         negative['source'] / 'units.map')
        result = {'id': 'code', 'entry_sha256': entry_digest(self.code), 'rounds': comparisons,
                  'omfs': [r['omfs']['code'] for r in self.rounds], 'producer_paths': ['a/source', 'b/source'],
                  'compiler_arguments': [r['compiler_arguments']['code'] for r in self.rounds],
                  'source_inputs': snapshots, 'producer_source_inputs': [producer_snapshot(r['source'], self.code, snapshots) for r in self.rounds],
                  'object_normalized_equal': True, 'exact': True}
        neg = {'unit_id': 'code', 'entry_sha256': entry_digest(self.code), 'mutation': self.code_mutation,
               'control_sha256': entry_digest(self.code_mutation), 'producer_path': 'negative/source',
               'omf': negative['omfs']['code'], 'comparison': control,
               'compiler_arguments': negative['compiler_arguments']['code'],
               'producer_source_inputs': producer_snapshot(negative['source'], self.code, snapshots)}
        self.parent_receipt = {'schema_version': 2, 'kind': review.PARENT_KIND, 'pass': True,
            'selected_units': ['code'], 'manifest_sha256': digest(self.parent / 'exact-units.toml'),
            'target_sha256': self.artifact['sha256'], 'toolchain_manifest_sha256': self.tool_sha,
            'toolchain_receipt_sha256': tool_identity['receipt_sha256'], 'toolchain_reused': True,
            'toolchain_reuse_proof_sha256': tool_identity['proof_sha256'], 'source_inputs': snapshots,
            'results': [result], 'negative_control': neg, 'compiled_negative_control': control,
            'complete_executable_exact': False}
        (self.parent / 'receipt.json').write_text(json.dumps(self.parent_receipt))
        self.calls.clear()

    def make_review(self):
        return review.review(self.root, 'main', self.parent / 'receipt.json', 'data', self.output)

    def validate(self, path):
        return progress.accept(path, root=self.root, validate_only=True)

    def test_two_old_positives_and_one_fresh_cp932_data_negative_import_without_relabel(self):
        before = review.archive_hashes(self.parent)
        path = self.make_review()
        receipt = self.validate(path)
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(receipt['compiler_invocations'], 1)
        self.assertEqual(receipt['retained_cold_producer_count'], 2)
        self.assertEqual(receipt['results'][0]['producer_paths'], ['parent/a/source', 'parent/b/source'])
        self.assertEqual(receipt['parent_receipt_sha256'], digest(self.parent / 'receipt.json'))
        self.assertEqual(receipt['toolchain_receipt_sha256'], self.parent_receipt['toolchain_receipt_sha256'])
        self.assertEqual(review.archive_hashes(self.parent), before)
        raw = (self.output / 'negative/source/src/owner.cpp').read_bytes()
        self.assertIn('終了'.encode('cp932'), raw)
        self.assertNotIn('終了'.encode(), raw)
        self.assertTrue(receipt['pass'])
        progress.accept(path, root=self.root)
        summary = progress.summarize(self.root)
        self.assertEqual((summary['functions'], summary['authored_data_bytes']), (0, 10))

    def test_stale_source_or_changed_flags_fail_before_any_new_compiler(self):
        (self.root / 'src/owner.cpp').write_text(self.canonical + '// changed\n')
        with self.assertRaises(ValueError):self.make_review()
        self.assertEqual(self.calls, [])
        (self.root / 'src/owner.cpp').write_text(self.canonical)
        self.data['wrapper_options'] = '-zPother'
        (self.root / 'config/exact_units.toml').write_text(manifest(self.config))
        with self.assertRaisesRegex(ValueError, 'flags|whole CODE owner'):self.make_review()
        self.assertEqual(self.calls, [])

    def test_every_producer_context_dimension_must_match_the_original(self):
        from lib.unit_context import UnitContext
        parent_config = {'units': [self.code]}
        for changed in ({'source': 'src/other.cpp'}, {'module': 'th05/other.cpp'},
                        {'wrapper_options': '-zPother'}, {'bindings_source': 'probes/other.asm'},
                        {'binary': 'O'}, {'source_encoding': 'raw'}):
            with self.subTest(changed=changed), self.assertRaisesRegex(ValueError, 'flags|whole CODE owner'):
                review.parent_owner(self.parent_receipt, parent_config, {**self.data, **changed},
                                    UnitContext(self.root))

    def test_parent_obj_or_mz_tampering_cannot_be_hidden_by_rehashing_archive(self):
        path = self.make_review();original = path.read_bytes()
        for name in ('owner.obj', 'units.exe'):
            with self.subTest(name=name):
                p = self.output / 'parent/a/source' / name
                previous = p.read_bytes();changed = bytearray(previous);changed[68 if name == 'units.exe' else -1] ^= 1;p.write_bytes(changed)
                receipt = json.loads(original);receipt['parent_artifacts'] = review.archive_hashes(self.output / 'parent')
                path.write_text(json.dumps(receipt))
                with self.assertRaises(ValueError):self.validate(path)
                p.write_bytes(previous)
        path.write_bytes(original)
        self.validate(path)

    def test_changed_parent_receipt_and_review_of_review_are_rejected(self):
        path = self.make_review();receipt = json.loads(path.read_text())
        parent_path = self.output / 'parent/receipt.json';parent = json.loads(parent_path.read_text())
        parent['kind'] = review.KIND;parent_path.write_text(json.dumps(parent))
        receipt['parent_receipt_sha256'] = digest(parent_path)
        receipt['parent_artifacts'] = review.archive_hashes(self.output / 'parent');path.write_text(json.dumps(receipt))
        with self.assertRaisesRegex(ValueError, 'parent receipt|artifacts'):self.validate(path)
        with self.assertRaisesRegex(ValueError, 'original bounded'):review.review(self.root, 'main', path, 'data', self.root / '.analysis/again')

    def test_code_only_negative_cannot_validate_initialized_data(self):
        self.code_only_negative = True
        with self.assertRaises(ValueError):self.make_review()
        self.assertEqual(len(self.calls), 1)
        self.assertTrue(compare_mapped_unit(self.target, parse_mz((self.output / 'negative/source/units.exe').read_bytes()),
                                          self.output / 'negative/source/units.map', self.data)['raw_exact'])

    def test_forged_count_negative_argv_or_binding_alias_is_rejected(self):
        path = self.make_review();original = path.read_bytes()
        receipt = json.loads(original);receipt['compiler_invocations'] = 0;path.write_text(json.dumps(receipt))
        with self.assertRaisesRegex(ValueError, 'relabel'):self.validate(path)
        path.write_bytes(original)
        source = self.output / 'negative/source'
        for name, raw in [('compiler-arguments.json', b'{}'), ('bindings.asm', b'forged alias')]:
            p = source / name;previous = p.read_bytes();p.write_bytes(raw)
            receipt = json.loads(original);receipt['negative_artifacts'] = review.archive_hashes(self.output / 'negative')
            path.write_text(json.dumps(receipt))
            with self.assertRaises(ValueError):self.validate(path)
            p.write_bytes(previous)
        path.write_bytes(original)
        self.validate(path)

    def test_new_main_actual_argv_tampering_rejected_but_legacy_absence_stays_valid(self):
        self.validate(self.parent / 'receipt.json')
        argv = self.parent / 'a/source/compiler-arguments.json'
        original = argv.read_bytes();argv.write_text('{}')
        with self.assertRaisesRegex(ValueError, 'compiler binary arguments'):self.validate(self.parent / 'receipt.json')
        argv.write_bytes(original)
        legacy = copy.deepcopy(self.parent_receipt)
        legacy['results'][0].pop('compiler_arguments');legacy['negative_control'].pop('compiler_arguments')
        for relative in ['a', 'b', 'negative']:
            (self.parent / relative / 'source/compiler-arguments.json').unlink()
        (self.parent / 'receipt.json').write_text(json.dumps(legacy))
        self.validate(self.parent / 'receipt.json')
        with self.assertRaisesRegex(ValueError, 'saved actual compiler argv'):self.make_review()
        self.assertEqual(self.calls, [])


if __name__ == '__main__':
    unittest.main()
