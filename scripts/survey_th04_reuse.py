#!/usr/bin/env python3
"""Route maintained TH04 C++ function candidates into TH05; grant zero credit.

Read-only cross-game discovery. Original TH04 file-backed function boundaries
and its acceptance are hypotheses only for TH05, which needs independent review
and complete fresh raw/fixup evidence from its own maintained source.
"""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path
import re
import subprocess

from lib.pc98 import digest_file, parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from survey_cpp_candidates import shape

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('th04', type=Path)
    parser.add_argument('--output', type=Path, default=ROOT / '.analysis/th04-source-reuse-survey.json')
    args = parser.parse_args()
    reference = args.th04.resolve()
    ledger = reference / 'config/th04_main_authored_functions.csv'
    previous = find_artifact(load_target_manifest(reference / 'config/targets.toml'), 'th04-main')
    old_raw = read_verified_artifact(reference, previous)
    old_image = parse_mz(old_raw)
    artifact = find_artifact(load_target_manifest(ROOT / 'config/targets.toml'), 'th05-main')
    target = parse_mz(read_verified_artifact(ROOT, artifact))
    if not old_image.valid or not target.valid:
        raise ValueError('invalid original MZ view')
    rows = []
    with ledger.open(newline='') as stream:
        for item in csv.DictReader(stream):
            if item['state'] != 'exact':
                continue
            size, start = int(item['size'], 0), int(item['file_offset'], 0)
            source = (reference / item['source']).resolve()
            source.relative_to(reference / 'src')
            if not source.is_file() or size < 16 or size > 4096:
                continue
            if start < old_image.header.header_size or start + size > old_image.header.header_size + len(old_image.program_image):
                raise ValueError('reference function extends outside file-backed original image')
            row = {'reference_id': item['id'], 'name': item['name'], 'source': item['source'],
                   'source_sha256': digest_file(source), 'reference_file_start': start,
                   'size': size, 'status': 'diagnostic-only-no-authored-credit'}
            discovered = shape(old_raw[start:start + size], start - old_image.header.header_size)
            if discovered is None:
                row['reason'] = 'incomplete decode or insufficient fixed bytes'
            else:
                pattern, fixed = discovered
                positions = [match.start() for match in re.finditer(pattern, target.program_image, re.DOTALL)]
                row.update(fixed_bytes=fixed, match_count=len(positions), target_candidates=positions[:8])
            rows.append(row)
    output = args.output.resolve()
    output.relative_to((ROOT / '.analysis').resolve())
    result = {'kind': 'cross-game-maintained-source-routing-only',
              'target_sha256': artifact['sha256'], 'reference_target_sha256': previous['sha256'],
              'reference_git_head': subprocess.check_output(['git', '-C', str(reference), 'rev-parse', 'HEAD'], text=True).strip(),
              'reference_ledger_sha256': digest_file(ledger), 'candidates': rows,
              'authored_credit': 0,
              'limitations': ['All immediates and displacements are masked for routing only.',
                              'TH04 ownership, boundaries, source ABI and acceptance do not transfer to TH05.',
                              'All TH05 extents need independent operand/boundary review and fresh source oracle evidence.']}
    output.write_text(json.dumps(result, indent=2) + '\n')
    unique = [row for row in rows if row.get('match_count') == 1]
    print(f'Diagnostic only: {len(rows)} maintained-source candidates, {len(unique)} unique shapes / {sum(row["size"] for row in unique):,} bytes; zero credit')
    for row in sorted(unique, key=lambda row: row['size'], reverse=True)[:25]:
        print(f'{row["target_candidates"][0]:05X} {row["size"]:5} {row["name"]} -> {row["source"]}')
    print(f'Private evidence: {output}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
