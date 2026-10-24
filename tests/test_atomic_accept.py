"""Two changed dependency owners must publish together or leave the ledger intact."""
import json
import contextlib
import io
from pathlib import Path
import shutil
import struct
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import progress
from lib.omf import describe_omf
from lib.pc98 import parse_mz
from lib.replay_toolchain import digest, entry_digest, snapshot_paths
from lib.unit_oracle import compare_mapped_unit
from replay_units import mapped_control_comparison
from test_initialized_data_replay import record, executable


def manifest(entries, controls):
    rows = ['artifact = "th05-main"']
    for table, values in (('units', entries), ('controls', controls)):
        for value in values:
            rows.append('[[' + table + ']]')
            rows.extend(key + '=' + json.dumps(item) for key, item in value.items())
    return '\n'.join(rows) + '\n'


def synthetic_object(entry, code):
    module = entry['module'].encode()
    out = record(0x80, bytes([len(module)]) + module)
    translator = b'TC86 Borland C++ 4.02'
    out += record(0x88, b'\0\0' + bytes([len(translator)]) + translator)
    for path in (entry['module'], entry['source'], 'src/shared.hpp'):
        name = path.encode()
        out += record(0x88, b'\0\xe9' + bytes(4) + bytes([len(name)]) + name)
    names = [entry['segment'].encode(), b'CODE', b'']
    out += record(0x96, b''.join(bytes([len(x)]) + x for x in names))
    out += record(0x98, b'\x28' + struct.pack('<H', len(code)) + b'\1\2\3')
    return out + record(0xA0, b'\1\0\0' + code) + record(0x8A, b'\0')


class AtomicAcceptTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.entries, self.controls = [], []
        for index, name in enumerate(('a', 'b')):
            self.entries.append({'id': name, 'source': 'src/' + name + '.cpp',
                'module': 'th05/' + name + '.cpp', 'segment': name.upper() + '_TEXT',
                'bindings_source': 'probes/bindings.asm', 'target_start': index * 8,
                'size': 4, 'functions': 1, 'origin': 'compiler-generated-cxx'})
            self.controls.append({'unit': name, 'source': 'src/' + name + '.cpp',
                'find': 'return 8;', 'replace': 'return 7;'})
            self.put('src/' + name + '.cpp', '#include "src/shared.hpp"\nunsigned far ' + name + '() { return 8; }\n')
        self.put('src/shared.hpp', '#ifndef OLD_GUARD\n#define OLD_GUARD\n#endif\n')
        self.put('probes/bindings.asm', '.386\nend\n')
        self.put('config/toolchain.toml', '# synthetic immutable tool pin\n')
        self.put('config/exact_units.toml', manifest(self.entries, self.controls))
        target = bytearray(executable(bytes(10)))
        for entry in self.entries:
            start = 48 + entry['target_start'];target[start:start + 4] = b'\xb8\x08\0\xcb'
        self.target_bytes = bytes(target)
        self.target = parse_mz(self.target_bytes)
        self.target_sha = __import__('hashlib').sha256(self.target_bytes).hexdigest()
        self.put('config/targets.toml', '[[artifacts]]\nid="th05-main"\nsha256="' + self.target_sha + '"\n')
        self.addCleanup(patch.stopall)
        patch.object(progress, 'load_unit_target', return_value=({'sha256': self.target_sha}, self.target, None)).start()
        self.old = [self.make_receipt(entry, 'old') for entry in self.entries]
        progress.accept_many(self.old, root=self.root)
        self.ledger = self.root / 'config/accepted_units.json'
        self.before = self.ledger.read_bytes()
        self.put('src/shared.hpp', '#ifndef DISTINCT_HEADER_GUARD\n#define DISTINCT_HEADER_GUARD\n#endif\n')
        self.fresh = [self.make_receipt(entry, 'fresh') for entry in self.entries]

    def put(self, name, text):
        path = self.root / name;path.parent.mkdir(parents=True, exist_ok=True);path.write_text(text)

    def make_receipt(self, entry, label):
        work = self.root / '.analysis' / (label + '-' + entry['id']);work.mkdir(parents=True)
        (work / 'exact-units.toml').write_bytes((self.root / 'config/exact_units.toml').read_bytes())
        tool = {'ready': True, 'identity_pass': True, 'execution_pass': True,
                'manifest_sha256': digest(self.root / 'config/toolchain.toml')}
        (work / 'toolchain-attestation.json').write_text(json.dumps(tool))
        paths = {entry['source'], 'src/shared.hpp', entry['bindings_source']}
        snapshots = snapshot_paths(self.root, paths)
        for path in paths:
            destination = work / 'inputs' / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes((self.root / path).read_bytes())
        mutation = next(x for x in self.controls if x['unit'] == entry['id'])
        omfs, comparisons = [], []
        for round_name in ('a', 'b', 'negative'):
            source = work / round_name / 'source';source.mkdir(parents=True)
            for path in paths:
                dst = source / path;dst.parent.mkdir(parents=True, exist_ok=True)
                dst.write_bytes((self.root / path).read_bytes())
            if round_name == 'negative':
                p = source / entry['source'];p.write_text(p.read_text().replace(mutation['find'], mutation['replace']))
            (source / 'bindings.asm').write_bytes((self.root / entry['bindings_source']).read_bytes())
            wrapper = source / entry['module'];wrapper.parent.mkdir(parents=True)
            wrapper.write_text('#include "' + entry['source'] + '"\n')
            code = b'\xb8' + (b'\x07' if round_name == 'negative' else b'\x08') + b'\0\xcb'
            obj = synthetic_object(entry, code)
            (source / (Path(entry['module']).stem + '.obj')).write_bytes(obj)
            raw = bytearray(self.target_bytes);start = 48 + entry['target_start'];raw[start:start + 4] = code
            (source / 'units.exe').write_bytes(raw)
            (source / 'units.map').write_text(' 0000:%04X 0004 C=CODE S=%s G=OWN M=%s ACBP=28\n' %
                                              (entry['target_start'], entry['segment'], entry['module']))
            candidate = parse_mz(bytes(raw))
            if round_name == 'negative':
                control = mapped_control_comparison(self.target, candidate, entry, source / 'units.map')
                negative_omf = {key: value for key, value in describe_omf(obj).items() if key != 'valid'}
            else:
                comparisons.append(compare_mapped_unit(self.target, candidate, source / 'units.map', entry))
                omfs.append({key: value for key, value in describe_omf(obj).items() if key != 'valid'})
        result = {'id': entry['id'], 'entry_sha256': entry_digest(entry), 'rounds': comparisons,
                  'object_normalized_equal': True, 'omfs': omfs, 'exact': True,
                  'source_inputs': snapshots, 'producer_paths': ['a/source', 'b/source']}
        receipt = {'schema_version': 1, 'kind': 'bounded-cxx-unit-exact-replay', 'pass': True,
                   'manifest_sha256': digest(work / 'exact-units.toml'),
                   'target_sha256': self.target_sha, 'toolchain_receipt_sha256': digest(work / 'toolchain-attestation.json'),
                   'source_inputs': snapshots, 'results': [result], 'compiled_negative_control': control,
                   'negative_control': {'unit_id': entry['id'], 'entry_sha256': entry_digest(entry),
                       'control_sha256': entry_digest(mutation), 'mutation': mutation,
                       'producer_path': 'negative/source', 'comparison': control, 'omf': negative_omf}}
        path = work / 'receipt.json';path.write_text(json.dumps(receipt));return path

    def test_two_stale_dependency_owners_replace_together_with_one_final_validation(self):
        with self.assertRaisesRegex(ValueError, 'accepted source changed'):
            progress.accept(self.fresh[0], root=self.root)
        self.assertEqual(self.ledger.read_bytes(), self.before)
        real_summary = progress.summarize
        with patch.object(progress, 'summarize', wraps=real_summary) as summary:
            progress.accept_many(self.fresh, root=self.root)
        self.assertEqual(summary.call_count, 1)
        self.assertEqual(progress.summarize(self.root)['unit_count'], 2)
        records = json.loads(self.ledger.read_text())['units']
        self.assertEqual([x['replay_receipt_sha256'] for x in records], [digest(p) for p in self.fresh])

    def test_stale_second_receipt_never_publishes_first(self):
        with self.assertRaisesRegex(ValueError, 'accepted source changed'):
            progress.accept_many([self.fresh[0], self.old[1]], root=self.root)
        self.assertEqual(self.ledger.read_bytes(), self.before)
        self.assertFalse(self.ledger.with_suffix('.json.tmp').exists())

    def test_bad_second_object_or_negative_leaves_ledger_untouched(self):
        for relative in ('a/source/b.obj', 'negative/source/units.exe'):
            path = self.fresh[1].parent / relative;old = path.read_bytes()
            path.write_bytes((old[:-1] + bytes([old[-1] ^ 1])) if relative.endswith('.obj')
                             else (self.fresh[1].parent / 'a/source/units.exe').read_bytes())
            with self.subTest(relative=relative), self.assertRaises(ValueError):
                progress.accept_many(self.fresh, root=self.root)
            self.assertEqual(self.ledger.read_bytes(), self.before)
            path.write_bytes(old)

    def test_batch_rejects_duplicate_receipts_units_and_ambiguous_subset(self):
        for paths, units in (([], None), ([self.fresh[0]] * 2, None), (self.fresh, ['a'])):
            with self.assertRaises(ValueError):progress.accept_many(paths, root=self.root, units=units)
        clone = self.root / '.analysis/duplicate';shutil.copytree(self.fresh[0].parent, clone)
        with self.assertRaisesRegex(ValueError, 'duplicate imported unit'):
            progress.accept_many([self.fresh[0], clone / 'receipt.json'], root=self.root)
        self.assertEqual(self.ledger.read_bytes(), self.before)

    def test_repeated_cli_accepts_one_batch_and_single_subset_still_works(self):
        arguments = ['progress.py', '--accept', str(self.fresh[0]), '--accept', str(self.fresh[1])]
        with patch.object(progress, 'ROOT', self.root), patch('sys.argv', arguments), \
             patch.object(progress, 'summarize_all', return_value={}), \
             patch.object(progress, 'render', return_value=('', '')), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(progress.main(), 0)
        progress.accept(self.fresh[0], root=self.root, units=['a'])
        records = json.loads(self.ledger.read_text())['units']
        self.assertEqual(records[0]['receipt_selected_subset'], ['a'])
        self.assertEqual(records[1]['replay_receipt_sha256'], digest(self.fresh[1]))


if __name__ == '__main__':
    unittest.main()
