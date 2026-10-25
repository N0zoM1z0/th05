# Local storage and evidence retention

This document covers the private workspace, not files distributed by GitHub.
Targets, assets, tools, projects, evidence and archives remain ignored.

## Handoff cleanup, 2026-10-25

Cleanup reclaimed approximately48 MiB net, including the retained compressed
backups. It removed
three duplicate worktree checkouts after full compressed backup and comparison,
removed regenerable Python/Ruff caches, and packed loose Git objects. Git
branches and history were retained. No target, toolchain, reference checkout,
accepted producer, compiled negative or parked native diagnostic was deleted.

The three dirty checkouts were `op-score-canonical`, `verdict-full-context`
and `staff-full-context`. Complete archives, original base/branch/status,
SHA-256 identities and verification results are private under
`.analysis/cleanup-handoff/worktrees/`. Archives exclude only worktree `.git`
registration and regenerable Python/Ruff caches; symlinks were stored without
following them. Uncommitted and untracked source was preserved. The three
archives total about3.8 MiB, replacing roughly30 MiB of duplicate checkout files.

To restore one, first read its JSON metadata and verify the archive SHA-256.
For example, from the repository root:

```sh
git worktree add .analysis/worktrees/staff-full-context reconstruction/staff-full-context
tar -xzf .analysis/cleanup-handoff/worktrees/staff-full-context.tar.gz \
    -C .analysis/worktrees/staff-full-context
```

The archive overlays the original dirty state on its preserved branch/base.
Historical producer command lines may mention these retired checkout paths;
actual frozen producer artifacts and source snapshots remain in their original
retained evidence directories. Restore a checkout if a historical investigation
specifically needs its old working path. It is not required for normal root
incremental replay.

## Preserve these trees

- `.analysis/targets/` and `.analysis/decoded/`: attested originals and actual
  decoded views/ordered relocation streams. Do not replace decoded images with
  fabricated MZ files or rerun decoders merely to restore local state.
- `.analysis/unit-replays/`: two independent producers, own/shared negative,
  source snapshots, manifests, argv, tool proofs and target views. A failed
  whole producer can contain accepted complete scopes. Seven derived reviews
  hash every file in their parent archives, including logs. Do not trim them.
- `.analysis/native-producers/`, native reviews and candidate freezes: retained
  limitations prevent repeated invalid source/ABI hypotheses. Failure names
  are not evidence that their contents are unused.
- `.analysis/builds/` and `.analysis/vendor-review/`: calibration binaries,
  listings, objects and source closures support library ownership and some
  retained DATA evidence. Keep their original paths and contents.
- `.analysis/toolchain/`: installed tools, attestations and independent active
  TC4 headers/libraries inside the Wine prefix are all checked. The approximately
  1.3 GiB Wine environment is operational state, not a disposable build cache.
- `.tools/`, `_reference/ReC98` and `ghidra-project/`: keep the pinned analysis
  tools, donor checkout/MSDOSplayer and databases. Many analysis-tool files are
  already hard-linked to reused immutable installations; removing them would
  not necessarily reclaim physical storage. Never modify sibling repositories.

The private `.analysis/EVIDENCE_STORAGE_GUARDS.md` and
`.analysis/cleanup-current-receipt-guards.json` identify the209 current receipts
supporting298 accepted records. Unlisted paths are not automatically disposable.
Public CI checks source/config consistency; it alone does not prove private
producers still exist. Cleanup additionally compared33,159 protected files
before/after, with identical tree hashes, and retained the audit records under
`.analysis/cleanup-handoff/`. The existing private validator rechecked208 whole
receipts. One historical stage DATA receipt rejects whole-receipt re-import
because an unselected CODE descriptor later received corrected NOP padding
metadata; its accepted DATA was separately rechecked against both actual
producers and its own negative. This pre-existing descriptor drift is recorded
in the handoff; cleanup did not modify the receipt or any protected file.

Further storage reduction needs a path-aware evidence audit. Avoid blanket
`rm` operations on `.analysis`, build logs, old-looking receipts or the Wine
prefix. Ordinary Python/Ruff caches can be regenerated. Run public checks with
`PYTHONDONTWRITEBYTECODE=1` if you want to avoid rebuilding bytecode caches.
