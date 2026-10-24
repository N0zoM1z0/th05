"""Incremental scopes must preserve old evidence and reject hidden input drift."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import tomllib
from types import SimpleNamespace
from unittest.mock import patch
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import progress
import replay_units
from lib.replay_toolchain import (bindings_source, digest, entry_digest, freeze_toolchain,
    include_closure, required_input_paths, scoped_snapshot, snapshot_paths, staged_paths)
from lib.toolchain import tree_identity


class SourceScopeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for name, text in {
            'src/a.cpp': '#include "src/a.hpp"\nint a() { return 1; }\n',
            'src/a.hpp': '#include <stddef.h>\n',
            'src/b.cpp': '#include "src/b.hpp"\nint b() { return 2; }\n',
            'src/b.hpp': '// independent declaration\n',
            'src/unrelated.cpp': '// unrelated code\n',
            'probes/units/main_bindings.asm': '.386\nend\n',
            'probes/units/b_bindings.asm': '.386\n; independent scaffold\nend\n',
            'config/toolchain.toml': 'schema_version = 2\n',
        }.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
        self.entries = [{'id': name, 'source': f'src/{name}.cpp', 'module': f'th05/{name}.cpp',
                         'segment': name.upper() + '_TEXT', 'target_start': index * 8,
                         'size': 4, 'alignment_offsets': [], 'functions': 1}
                        for index, name in enumerate(('a', 'b'))]
        self.entries[1]['bindings_source'] = 'probes/units/b_bindings.asm'
        self.acceptance = {'units': [], 'toolchain_manifest_sha256': digest(self.root / 'config/toolchain.toml')}
        for entry in self.entries:
            dependencies = [entry['module'], entry['source'], f"src/{entry['id']}.hpp", r'C:\TC4\INCLUDE\stddef.h']
            result = {'omfs': [{'dependency_paths': list(dependencies)}, {'dependency_paths': list(dependencies)}]}
            snapshots = snapshot_paths(self.root, staged_paths(self.root, entry))
            self.acceptance['units'].append({'id': entry['id'], 'entry_sha256': entry_digest(entry),
                                             'source_inputs': snapshots, 'result': result})
        self.manifest = {'units': self.entries}

    def plan(self):
        return replay_units.select_units(self.root, self.manifest, None, self.acceptance)

    def test_no_work_and_unrelated_source_or_control_addition_do_not_select_old_units(self):
        self.assertEqual(self.plan()[0], [])
        (self.root / 'src/unrelated.cpp').write_text('new unrelated source\n')
        self.manifest['controls'] = [{'unit': 'elsewhere', 'find': 'x', 'replace': 'y'}]
        self.assertEqual(self.plan()[0], [])

    def test_only_changed_dependency_owner_is_selected(self):
        (self.root / 'src/b.hpp').write_text('changed declaration\n')
        units, reasons = self.plan()
        self.assertEqual([unit['id'] for unit in units], ['b'])
        self.assertEqual(reasons, {'b': 'source-changed'})

    def test_unrelated_new_unit_does_not_invalidate_old_entry_hashes(self):
        new = {**self.entries[0], 'id': 'new', 'source': 'src/new.cpp'}
        self.manifest['units'].append(new)
        self.assertEqual([unit['id'] for unit in self.plan()[0]], ['new'])

    def test_explicit_selection_never_pulls_in_an_unselected_control_unit(self):
        selected, reasons = replay_units.select_units(self.root, self.manifest, ['b'], self.acceptance)
        self.assertEqual([unit['id'] for unit in selected], ['b'])
        self.assertEqual(reasons, {'b': 'explicit'})

    def test_empty_default_plan_never_reads_target_or_probes_tools(self):
        config = 'artifact="target"\n' + '\n'.join(
            '[[units]]\n' + '\n'.join(f'{key}={json.dumps(value)}' for key, value in entry.items())
            for entry in self.entries)
        (self.root / 'config/exact_units.toml').write_text(config)
        (self.root / 'config/accepted_units.json').write_text(json.dumps(self.acceptance))
        with patch.object(replay_units, 'ROOT', self.root), patch('sys.argv', ['replay_units.py']), \
             patch.object(replay_units, 'read_verified_artifact', side_effect=AssertionError('target read')), \
             patch.object(replay_units, 'freeze_toolchain', side_effect=AssertionError('tool probes')), \
             patch.object(replay_units, 'cold_round', side_effect=AssertionError('unexpected compilation')):
            self.assertEqual(replay_units.main(), 0)

    def test_failed_first_map_extent_does_not_compile_a_second_positive(self):
        entry = self.entries[0]
        mutation = {'unit': 'a', 'source': 'src/a.cpp',
                    'find': 'return 1', 'replace': 'return 2'}
        config = 'artifact="th05-main"\n[[units]]\n' + '\n'.join(
            f'{key}={json.dumps(value)}' for key, value in entry.items())
        config += '\n[[controls]]\n' + '\n'.join(
            f'{key}={json.dumps(value)}' for key, value in mutation.items())
        (self.root / 'config/exact_units.toml').write_text(config)
        work = self.root / '.analysis/failed-first-scope'
        produced = []

        def first_round(directory, *args, **kwargs):
            produced.append(directory)
            source = directory / 'source'
            source.mkdir(parents=True)
            (source / 'units.map').write_text(
                ' 0000:0000 0003 C=CODE S=A_TEXT G=(none) M=th05/a.cpp ACBP=28\n')
            return {'source': source, 'candidate': SimpleNamespace()}

        with patch.object(replay_units, 'ROOT', self.root), \
             patch('sys.argv', ['replay_units.py', '--units', 'a', '--output', str(work)]), \
             patch.object(replay_units, 'load_unit_target', return_value=({}, SimpleNamespace(), None)), \
             patch.object(replay_units, 'freeze_toolchain', return_value={}), \
             patch.object(replay_units, 'cold_round', side_effect=first_round):
            with self.assertRaisesRegex(ValueError, 'complete-contribution size mismatch: 3'):
                replay_units.main()
        self.assertEqual(produced, [work / 'group-0/a'])
        self.assertTrue((produced[0] / 'source/units.map').is_file())
        self.assertFalse((work / 'group-0/b').exists())

    def test_custom_binding_drift_only_selects_its_owner(self):
        (self.root / 'probes/units/b_bindings.asm').write_text('changed scaffold\n')
        self.assertEqual([unit['id'] for unit in self.plan()[0]], ['b'])

    def test_scanning_and_real_omf_dependencies_cross_check(self):
        entry = self.entries[0]
        result = copy.deepcopy(self.acceptance['units'][0]['result'])
        for omf in result['omfs']:
            omf['dependency_paths'].append('src/unrelated.cpp')
        with self.assertRaisesRegex(ValueError, 'omitted by include scanning'):
            required_input_paths(self.root, entry, result)
        result['omfs'][0]['dependency_paths'].pop()
        with self.assertRaisesRegex(ValueError, 'closures disagree'):
            required_input_paths(self.root, entry, result)

    def test_legacy_whole_tree_snapshot_is_trimmed_without_new_source_credit(self):
        entry = self.entries[0]
        original = self.acceptance['units'][0]
        broad = snapshot_paths(self.root, {'src/a.cpp', 'src/a.hpp', 'src/b.cpp',
                                          'probes/units/main_bindings.asm'})
        for row in broad:
            if row['path'] == 'probes/units/main_bindings.asm':
                row['path'] = 'main_bindings.asm'
        trimmed = scoped_snapshot(self.root, entry, original['result'], broad)
        self.assertEqual({row['path'] for row in trimmed},
                         {'src/a.cpp', 'src/a.hpp', 'probes/units/main_bindings.asm'})
        broad = [row for row in broad if row['path'] != 'src/a.hpp']
        with self.assertRaisesRegex(ValueError, 'omits'):
            scoped_snapshot(self.root, entry, original['result'], broad)

    def test_relative_includes_are_resolved_without_allowing_repository_escape(self):
        (self.root / 'src/a.cpp').write_text('#include "../src/a.hpp"\n')
        self.assertEqual(include_closure(self.root, 'src/a.cpp'), {'src/a.cpp', 'src/a.hpp'})
        (self.root / 'src/a.cpp').write_text('#include "../../outside.hpp"\n')
        with self.assertRaises(ValueError):
            include_closure(self.root, 'src/a.cpp')

    def test_merge_preserves_old_per_unit_tool_and_replay_identity(self):
        config = 'artifact="target"\n' + '\n'.join(
            '[[units]]\n' + '\n'.join(f'{key}={json.dumps(value)}' for key, value in entry.items())
            for entry in self.entries)
        (self.root / 'config/exact_units.toml').write_text(config)
        previous = copy.deepcopy(self.acceptance)
        previous.update({'replay_receipt_sha256': 'old-replay',
                         'toolchain_manifest_sha256': 'old-tool',
                         'target_sha256': 'target',
                         'compiled_negative_control': {'historical': True}})
        imported = [{**previous['units'][0], 'toolchain_manifest_sha256': 'new-tool',
                     'replay_receipt_sha256': 'new-replay'}]
        merged = progress.merge_acceptance(self.root, previous, imported,
            target_sha='target', tool_sha='new-tool', replay_sha='new-replay', control={})
        old = next(row for row in merged['units'] if row['id'] == 'b')
        self.assertEqual(old['toolchain_manifest_sha256'], 'old-tool')
        self.assertEqual(old['replay_receipt_sha256'], 'old-replay')
        self.assertEqual(old['result'], previous['units'][1]['result'])
        self.assertEqual(old['compiled_negative_control'], {'historical': True})

    def test_cold_group_compiles_only_the_selected_unit_and_its_own_mutation(self):
        entry = self.entries[1]
        commands = []
        class FakeBuilder:
            def __init__(builder, source, prefix, msdos):
                builder.source, builder.msdos, builder.records = source, msdos, []
            def execute(builder, name, command):
                commands.append(command)
                if name.endswith('.obj'):
                    (builder.source / name).write_bytes(b'fake object')
                if name == 'link':
                    (builder.source / 'units.exe').write_bytes(b'fake executable')
        omf = {'valid': True, 'translator_comments': ['TC86 Borland C++ 4.02'],
               'sha256': 'hash', 'dependency_timestamp_normalized_sha256': 'normalized',
               'module_name': entry['module'], 'dependency_paths': []}
        with patch.object(replay_units, 'Builder', FakeBuilder), patch.object(replay_units, 'describe_omf', return_value=omf), patch.object(replay_units, 'parse_mz', return_value=SimpleNamespace(valid=True)):
            result = replay_units.cold_round(self.root / 'cold', self.root, [entry],
                paths=staged_paths(self.root, entry),
                mutation={'source': 'src/b.cpp', 'find': 'return 2', 'replace': 'return 3'})
        compiler_calls = [command for command in commands if 'tcc' in command]
        self.assertEqual([command[-1] for command in compiler_calls], ['th05/b.cpp'])
        self.assertFalse((result['source'] / 'src/a.cpp').exists())
        self.assertIn('return 3', (result['source'] / 'src/b.cpp').read_text())
        self.assertIn('return 2', (self.root / 'src/b.cpp').read_text())


class ToolchainReuseTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'config').mkdir()
        (self.root / 'tool.bin').write_bytes(b'pinned tool')
        (self.root / 'config/toolchain.toml').write_text(
            '[[surfaces]]\nid="compiler"\nkind="file"\npath="tool.bin"\n'
            f'sha256="{digest(self.root / "tool.bin")}"\nrequired=true\n')
        self.report = {'manifest_sha256': digest(self.root / 'config/toolchain.toml'),
            'ready': True, 'identity_pass': True, 'execution_pass': True,
            'execution': {'pass': True}, 'observed_utc': 'original-observation',
            'selected_surface_ids': ['compiler'],
            'surfaces': [{'id': 'compiler', 'pass': True,
                          'actual_sha256': digest(self.root / 'tool.bin'),
                          'expected_sha256': digest(self.root / 'tool.bin')}]}
        self.path = self.root / '.analysis/toolchain/attestation.json'
        self.path.parent.mkdir(parents=True)
        self.path.write_text(json.dumps(self.report))

    def test_reuse_rehashes_current_surfaces_and_preserves_original_report_bytes(self):
        destination = self.root / 'frozen/toolchain-attestation.json'
        with patch('lib.replay_toolchain.subprocess.run', side_effect=AssertionError('unexpected probes')):
            result = freeze_toolchain(self.root, destination)
        self.assertTrue(result['reused'])
        self.assertEqual(destination.read_bytes(), self.path.read_bytes())
        self.assertEqual(result['report']['observed_utc'], 'original-observation')
        self.assertTrue(destination.with_name('toolchain-reuse-proof.json').is_file())

    def test_manifest_drift_cannot_relabel_an_old_ready_probe(self):
        path = self.root / 'config/toolchain.toml'
        path.write_text(path.read_text() + '\n# changed pin\n')
        with self.assertRaisesRegex(ValueError, 'probes are required'):
            freeze_toolchain(self.root, self.root / 'out/report.json', allow_probes=False)

    def test_installed_tool_drift_forbids_probes_before_execution(self):
        (self.root / 'tool.bin').write_bytes(b'wrong tool')
        with patch('lib.replay_toolchain.subprocess.run', side_effect=AssertionError('unsafe execution')):
            with self.assertRaisesRegex(ValueError, 'static identity'):
                freeze_toolchain(self.root, self.root / 'out/report.json')

    def test_active_include_context_is_verified_without_rewriting_old_probe(self):
        installed = self.root / 'installed/INCLUDE'
        installed.mkdir(parents=True)
        (installed / 'header.h').write_text('pinned header\n')
        active = self.root / 'prefix/drive_c/TC4/INCLUDE'
        active.parent.mkdir(parents=True)
        shutil.copytree(installed, active)
        identity = tree_identity(installed)
        config = self.root / 'config/toolchain.toml'
        config.write_text('[paths]\nwine_prefix="prefix"\n' + config.read_text() +
            '[[surfaces]]\nid="tc40j-include"\nkind="tree"\npath="installed/INCLUDE"\n'
            f'sha256="{identity.sha256}"\nfile_count={identity.file_count}\nrequired=true\n')
        self.report['manifest_sha256'] = digest(config)
        self.report['selected_surface_ids'].append('tc40j-include')
        self.report['surfaces'].append({'id': 'tc40j-include', 'pass': True,
            'actual_sha256': identity.sha256, 'expected_sha256': identity.sha256})
        self.path.write_text(json.dumps(self.report))
        before = self.path.read_bytes()
        result = freeze_toolchain(self.root, self.root / 'good/report.json', allow_probes=False)
        self.assertIn('active-tc40j-include', result['required_surface_sha256'])
        self.assertEqual(before, self.path.read_bytes())
        (active / 'header.h').write_text('drifted actual compiler header\n')
        with patch('lib.replay_toolchain.subprocess.run', side_effect=AssertionError('unsafe probes')):
            with self.assertRaisesRegex(ValueError, 'active TC4 INCLUDE'):
                freeze_toolchain(self.root, self.root / 'bad/report.json')

    def test_incomplete_ready_report_is_not_reused(self):
        self.report['selected_surface_ids'] = []
        self.path.write_text(json.dumps(self.report))
        with self.assertRaisesRegex(ValueError, 'probes are required'):
            freeze_toolchain(self.root, self.root / 'out/report.json', allow_probes=False)


if __name__ == '__main__':
    unittest.main()
