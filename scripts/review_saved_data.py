#!/usr/bin/env python3
"""Review retained cold CODE producers' whole DATA; compile only a fresh DATA negative.

The two positive producers are archived byte-for-byte. This lane never claims
that a new positive compilation happened, and cannot review another review.
"""
from __future__ import annotations
import argparse
import copy
import fcntl
import json
from pathlib import Path
import shutil
import tomllib

from lib.omf import describe_omf
from lib.pc98 import parse_mz
from lib.replay_toolchain import (bindings_source, compiler_dependencies, digest, entry_digest,
    freeze_toolchain, scoped_snapshot, static_toolchain, validate_full_toolchain, validate_snapshot)
from lib.unit_context import UnitContext, compiler_arguments, load_unit_target, unit_binary
from lib.unit_extents import initialized_data_omf_scope, unit_extent_kind
from lib.unit_oracle import compare_mapped_unit, function_scoped
from lib.unit_sources import producer_snapshot, source_encoding, validate_producer_inputs
from replay_units import OMF_FIELDS, cold_round, mapped_control_comparison
from review_saved_scopes import archive_hashes

ROOT = Path(__file__).resolve().parents[1]
KIND = 'reviewed-initialized-data-of-retained-cold-producers'
PARENT_KIND = 'bounded-cxx-unit-exact-replay'


def producer_identity(entry: dict, context: UnitContext) -> tuple:
    return (entry['source'], entry['module'], entry.get('wrapper_options', ''),
            bindings_source(entry), unit_binary(entry, context.binary), source_encoding(entry),
            tuple(compiler_arguments(entry, context.binary)))


def selected_entry(config: dict, unit_id: str) -> tuple[dict, dict]:
    entries = [entry for entry in config['units'] if entry['id'] == unit_id]
    controls = [row for row in config.get('controls', []) if row['unit'] == unit_id]
    if len(entries) != 1 or len(controls) != 1 or unit_extent_kind(entries[0]) != 'initialized-data':
        raise ValueError('select exactly one configured complete initialized DATA and its own mutation')
    return entries[0], controls[0]


def parent_owner(parent: dict, parent_config: dict, entry: dict, context: UnitContext) -> tuple[dict, dict]:
    if parent.get('kind') != PARENT_KIND or parent.get('schema_version', 1) < 2:
        raise ValueError('DATA review requires original bounded producers, never a review or legacy relabelling')
    entries = {row['id']: row for row in parent_config['units']}
    matches = []
    for result in parent['results']:
        original = entries[result['id']]
        if (unit_extent_kind(original) == 'code' and not function_scoped(original) and
                producer_identity(original, context) == producer_identity(entry, context)):
            matches.append((original, result))
    if not matches:
        raise ValueError('DATA changes parent source/module/flags/bindings/binary/encoding or lacks whole CODE owner')
    # Several original CODE contributions may come from one actual TU. They
    # must identify the very same two actual producers and canonical closure.
    first = matches[0][1]
    for _, result in matches:
        if (result.get('producer_paths') != first.get('producer_paths') or
                result.get('source_inputs', parent['source_inputs']) != first.get('source_inputs', parent['source_inputs'])):
            raise ValueError('ambiguous retained translation-unit producer or source closure')
        if not result['object_normalized_equal'] or len(result['rounds']) != 2:
            raise ValueError('retained independent compiler objects are not deterministic')
    return matches[0]


def actual_arguments(source: Path, entry: dict, context: UnitContext) -> list[str]:
    expected = compiler_arguments(entry, context.binary)
    path = source / 'compiler-arguments.json'
    if not path.is_file() or json.loads(path.read_text()).get(entry['module']) != expected:
        raise ValueError('retained producer lacks matching saved actual compiler argv; inferred argv is insufficient')
    prefix = ('#pragma option ' + entry['wrapper_options'] + '\n') if entry.get('wrapper_options') else ''
    if (source / entry['module']).read_text() != prefix + '#include "' + entry['source'] + '"\n':
        raise ValueError('retained compiler wrapper changes source or pragma flags')
    return expected


def positive_result(root: Path, work: Path, config: dict, entry: dict) -> tuple[dict, dict, object, object]:
    context = UnitContext(root, config['artifact'].removeprefix('th05-'))
    parent_work = work / 'parent'
    parent = json.loads((parent_work / 'receipt.json').read_text())
    parent_config = tomllib.loads((parent_work / 'exact-units.toml').read_text())
    original, old_result = parent_owner(parent, parent_config, entry, context)
    artifact, target, target_view = load_unit_target(context, config)
    if parent['target_sha256'] != artifact['sha256'] or parent.get('target_view') != target_view:
        raise ValueError('DATA parent target or decoded view differs')
    paths = old_result.get('producer_paths', [])
    if len(paths) != 2 or paths[0] == paths[1]:
        raise ValueError('two distinct retained cold producer paths are required')
    comparisons, omfs, arguments, encoded = [], [], [], []
    for index, relative in enumerate(paths):
        source = parent_work / relative
        source.resolve().relative_to(parent_work.resolve())
        arguments.append(actual_arguments(source, entry, context))
        if old_result.get('compiler_arguments') != [arguments[-1]] * 2:
            raise ValueError('parent actual compiler argv metadata differs')
        raw = (source / (Path(entry['module']).stem + '.obj')).read_bytes()
        obj = describe_omf(raw)
        if not obj['valid'] or any(obj[key] != value for key, value in old_result['omfs'][index].items()):
            raise ValueError('retained compiler OBJ identity differs')
        omf = {key: obj[key] for key in OMF_FIELDS}
        omf['initialized_data_scope'] = initialized_data_omf_scope(raw, entry)
        omfs.append(omf)
        image = parse_mz((source / 'units.exe').read_bytes())
        if not image.valid:
            raise ValueError('invalid retained positive MZ')
        comparisons.append(compare_mapped_unit(target, image, source / 'units.map', entry))
    result = {'id': entry['id'], 'entry_sha256': entry_digest(entry), 'rounds': comparisons,
              'object_normalized_equal': len({obj['dependency_timestamp_normalized_sha256'] for obj in omfs}) == 1,
              'omfs': omfs, 'producer_paths': ['parent/' + path for path in paths],
              'compiler_arguments': arguments}
    snapshots = scoped_snapshot(root, entry, result, old_result.get('source_inputs', parent['source_inputs']))
    validate_snapshot(root, snapshots)
    if snapshots != old_result.get('source_inputs', parent['source_inputs']):
        raise ValueError('DATA canonical dependency closure differs from actual parent closure')
    result['source_inputs'] = snapshots
    for path in paths:
        source = parent_work / path
        validate_producer_inputs(root, source, entry, snapshots)
        encoded.append(producer_snapshot(source, entry, snapshots))
    if source_encoding(entry) == 'cp932':
        result['producer_source_inputs'] = encoded
    result['exact'] = result['object_normalized_equal'] and all(row['exact'] for row in comparisons)
    if not result['exact']:
        raise ValueError('retained whole DATA is not raw and original ordered-fixup exact')
    return result, parent, target, target_view


def negative_tool_proof(root: Path, work: Path, parent: dict) -> dict:
    directory = work / 'negative-toolchain'
    report_path, proof_path = directory / 'toolchain-attestation.json', directory / 'toolchain-reuse-proof.json'
    report, proof = json.loads(report_path.read_text()), json.loads(proof_path.read_text())
    manifest_sha, surfaces = static_toolchain(root)
    validate_full_toolchain(report, manifest_sha, surfaces)
    if (manifest_sha != parent['toolchain_manifest_sha256'] or proof.get('manifest_sha256') != manifest_sha or
            proof.get('reused') is not True or proof.get('original_full_receipt_sha256') != digest(report_path) or
            proof.get('required_surface_sha256') != {row['id']: row['actual_sha256'] for row in surfaces} or
            proof.get('active_context') != [row for row in surfaces if row.get('derived_from')]):
        raise ValueError('fresh negative toolcache proof differs from actual required tool identities')
    return {'receipt_sha256': digest(report_path), 'proof_sha256': digest(proof_path),
            'manifest_sha256': manifest_sha, 'reused': True}


def derive_review(root: Path, work: Path, config: dict, unit_id: str) -> dict:
    """Mechanical rederivation from actual old positives and one actual new negative."""
    from progress import validate_control, validate_data_scope_evidence
    entry, mutation = selected_entry(config, unit_id)
    context = UnitContext(root, config['artifact'].removeprefix('th05-'))
    result, parent, target, target_view = positive_result(root, work, config, entry)
    snapshots = result['source_inputs']
    if mutation['source'] not in {row['path'] for row in snapshots}:
        raise ValueError('DATA mutation lies outside the retained actual dependency closure')
    source = work / 'negative/source'
    arguments = actual_arguments(source, entry, context)
    steps = json.loads((work / 'negative/steps.json').read_text())
    compiles = [row for row in steps if 'tcc' in row.get('command', [])]
    expected_command = ['wine', str(root / '_reference/ReC98/bin/msdos.exe'), '-e', '-x', 'tcc', *arguments]
    if len(compiles) != 1 or compiles[0]['command'] != expected_command or any(row['returncode'] != 0 for row in steps):
        raise ValueError('DATA review must record exactly one successful fresh negative compiler invocation')
    validate_producer_inputs(root, source, entry, snapshots, mutation=mutation)
    raw = (source / (Path(entry['module']).stem + '.obj')).read_bytes()
    obj = describe_omf(raw)
    if not obj['valid'] or obj['translator_comments'] != ['TC86 Borland C++ 4.02']:
        raise ValueError('invalid fresh negative compiler OBJ')
    omf = {key: obj[key] for key in OMF_FIELDS}
    omf['initialized_data_scope'] = initialized_data_omf_scope(raw, entry, require_size=False)
    if compiler_dependencies(entry, [omf]) != compiler_dependencies(entry, result['omfs']):
        raise ValueError('negative DATA compiler dependency closure differs')
    candidate = parse_mz((source / 'units.exe').read_bytes())
    if not candidate.valid:
        raise ValueError('invalid fresh negative MZ')
    control = mapped_control_comparison(target, candidate, entry, source / 'units.map')
    validate_control(control)
    validate_data_scope_evidence(entry, control, omf['initialized_data_scope'])
    negative = {'unit_id': unit_id, 'entry_sha256': entry_digest(entry), 'mutation': mutation,
                'control_sha256': entry_digest(mutation), 'producer_path': 'negative/source',
                'comparison': control, 'omf': omf, 'compiler_arguments': arguments}
    if source_encoding(entry) == 'cp932':
        negative['producer_source_inputs'] = producer_snapshot(source, entry, snapshots)
    receipt = {key: copy.deepcopy(parent[key]) for key in (
        'schema_version', 'target_sha256', 'toolchain_receipt_sha256', 'toolchain_manifest_sha256',
        'toolchain_reused', 'toolchain_reuse_proof_sha256')}
    parent_path = work / 'parent/receipt.json'
    receipt.update(kind=KIND, compiler_invocations=1, retained_cold_producer_count=2,
        parent_receipt_path='parent/receipt.json', parent_receipt_sha256=digest(parent_path),
        parent_manifest_sha256=digest(work / 'parent/exact-units.toml'), parent_aggregate_pass=parent['pass'],
        parent_artifacts=archive_hashes(work / 'parent'), negative_artifacts=archive_hashes(work / 'negative'),
        fresh_negative_toolchain=negative_tool_proof(root, work, parent),
        manifest_sha256=digest(work / 'exact-units.toml'), source_inputs=snapshots,
        results=[result], selected_units=[unit_id], negative_control=negative,
        compiled_negative_control=control, complete_executable_exact=False, **{'pass': True})
    if target_view is not None:
        receipt.update(artifact=context.artifact, target_view=target_view)
    return receipt


def validate_review(path: Path, *, root: Path, artifact_name: str, validate_parent) -> None:
    work = path.parent
    receipt = json.loads(path.read_text())
    if (receipt.get('parent_receipt_path') != 'parent/receipt.json' or receipt.get('compiler_invocations') != 1 or
            receipt.get('retained_cold_producer_count') != 2 or len(receipt.get('selected_units', [])) != 1):
        raise ValueError('DATA review cannot relabel retained positives as fresh compiles')
    parent_path = work / 'parent/receipt.json'
    if (json.loads(parent_path.read_text()).get('kind') != PARENT_KIND or
            digest(parent_path) != receipt.get('parent_receipt_sha256') or
            archive_hashes(work / 'parent') != receipt.get('parent_artifacts')):
        raise ValueError('retained parent receipt or artifacts changed')
    validate_parent(parent_path)
    config = tomllib.loads((work / 'exact-units.toml').read_text())
    if config['artifact'] != 'th05-' + artifact_name:
        raise ValueError('DATA review artifact context differs')
    expected = derive_review(root, work, config, receipt['selected_units'][0])
    if receipt != expected:
        raise ValueError('DATA receipt is not the mechanical review of intact retained producers and fresh negative')


def review(root: Path, artifact_name: str, parent_path: Path, unit_id: str, output: Path) -> Path:
    from progress import accept
    context = UnitContext(root, artifact_name)
    parent_path, output = parent_path.resolve(), output.resolve()
    parent_work = parent_path.parent
    output.relative_to((root / '.analysis').resolve())
    if output.is_relative_to(parent_work) or parent_work.is_relative_to(output):
        raise ValueError('new DATA review output must be separate from its intact parent')
    if parent_path.name != 'receipt.json' or json.loads(parent_path.read_text()).get('kind') != PARENT_KIND:
        raise ValueError('DATA review needs an original bounded replay receipt')
    accept(parent_path, root=root, artifact_name=artifact_name, validate_only=True)
    before = archive_hashes(parent_work)
    output.mkdir(parents=True, exist_ok=False)
    shutil.copytree(parent_work, output / 'parent')
    if before != archive_hashes(output / 'parent') or before != archive_hashes(parent_work):
        raise ValueError('retained producers changed during archival')
    shutil.copyfile(context.manifest, output / 'exact-units.toml')
    for name in ('inputs', 'target-view'):
        if (parent_work / name).is_dir():
            shutil.copytree(parent_work / name, output / name)
    # Preserve the original positive executable tool evidence byte-for-byte.
    for name in ('toolchain-attestation.json', 'toolchain-reuse-proof.json', 'toolchain.toml'):
        shutil.copyfile(parent_work / name, output / name)
    config = tomllib.loads((output / 'exact-units.toml').read_text())
    entry, mutation = selected_entry(config, unit_id)
    result, _, _, _ = positive_result(root, output, config, entry)
    paths = {row['path'] for row in result['source_inputs']}
    if mutation['source'] not in paths:
        raise ValueError('DATA mutation lies outside retained source closure')
    with (root / '.analysis/borland.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        freeze_toolchain(root, output / 'negative-toolchain/toolchain-attestation.json', allow_probes=False)
        negative = cold_round(output / 'negative', output / 'inputs', [entry],
                              paths=paths, mutation=mutation, binary=context.binary)
        (output / 'negative/steps.json').write_text(json.dumps(negative['steps'], indent=2) + '\n')
        # cold_round omits this file for historical default-M units. This is
        # actual argv returned from this fresh invocation, never inferred old evidence.
        argv_path = negative['source'] / 'compiler-arguments.json'
        if not argv_path.exists():
            argv_path.write_text(json.dumps({entry['module']: negative['compiler_arguments'][unit_id]}, indent=2) + '\n')
    live_entry, live_mutation = selected_entry(context.config(), unit_id)
    if entry_digest(live_entry) != entry_digest(entry) or live_mutation != mutation:
        raise ValueError('selected DATA configuration or mutation changed during its one negative build')
    receipt = derive_review(root, output, config, unit_id)
    destination = output / 'receipt.json'
    destination.write_text(json.dumps(receipt, indent=2) + '\n')
    accept(destination, root=root, artifact_name=artifact_name, validate_only=True)
    if before != archive_hashes(parent_work):
        raise ValueError('original parent changed while reviewing DATA')
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--artifact', choices=('main', 'op', 'maine'), default='main')
    parser.add_argument('--from-receipt', type=Path, required=True)
    parser.add_argument('--unit', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    receipt = review(ROOT, args.artifact, args.from_receipt, args.unit, args.output)
    print(json.dumps({'receipt': str(receipt), 'compiler_invocations': 1,
                      'retained_cold_producer_count': 2, 'ledger_written': False}, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
