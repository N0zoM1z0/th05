# Local storage and handoff cleanup

Private originals, tools, assets, databases and evidence remain ignored.
Cleanup changes no acceptance or compiler inputs of accepted units.

## Current cleanup, 2026-11-06

Private audit: `.analysis/cleanup-handoff/2026-11-06/`.

- `accepted-receipts.json`: **367** current C/C++ records resolve to **267**
  distinct receipt hashes, with no missing receipt. Transitive accepted-parent
  roots are retained. This is an identity/retention audit, not a cold replay.
- `selection.json`: 51 terminal raw-false historical producers whose current
  source inputs differ. Accepted/transitive dependencies, current baselines,
  raw-equal producers and the new OP ZUNsoft lead are excluded.
- `diagnostics.tar.xz`: all **2,148** selected files, individually compared
  against their original SHA-256 before the redundant originals were removed.
  Archive size **447,744 bytes**, SHA-256
  `2d5befd3b9ceeff23ed4c615af08028cd6f283a06fb0adba68ac423cf543346f`.
- `result.json`: original disk allocation 45,785,088 bytes; retained live
  metadata 7,790,592 bytes; net reclaimed **37,543,936 bytes (35.8 MiB)**.
- `protected-before.json` / `protected-after.json`: content identities for
  accepted replay roots, targets, decoded views, calibration/ASM/vendor inputs,
  installed compiler files and the current leading diagnostics.
- `retention-validation.json`: all 30,930 protected files are unchanged and all
  267 required receipt hashes still resolve.
- `cache-cleanup.json`: about 1.0 MiB of regenerable `scripts/` / `tests/` Python
  caches removed. Cleanup checks use `PYTHONDONTWRITEBYTECODE=1`.
- `git-storage.json`: `git repack -Ad` reclaimed another 17,133,568 bytes
  (16.3 MiB), with refs and HEAD unchanged. Capital `-A` retains unreachable
  packed objects as loose objects; no prune or history deletion was performed.

These operations reclaimed approximately **53.2 MiB** in total. All four
incremental plans are empty and the light public consistency check passes.
No compiler replay, whole test suite or target decoding was run during cleanup.

Archived producer directories keep their unchanged `native-diagnostic.json`
and an `ARCHIVED.json` pointer. Full CPP/ASM/OMF/MAP/MZ/log/source snapshots
remain recoverable from the archive; absence of those loose files is intentional.
Failed aggregate builds can contain accepted scopes, so names such as "failed"
are never sufficient grounds for deletion. No target, installed tool, accepted
receipt, shared sibling installation or Ghidra project was removed.

Restore only a needed archived producer, not the whole archive:

```sh
sha256sum .analysis/cleanup-handoff/2026-11-06/diagnostics.tar.xz
# Compare the hash above and inspect this path's ARCHIVED.json first.
tar -xJf .analysis/cleanup-handoff/2026-11-06/diagnostics.tar.xz \
    .analysis/native-producers/main-boss-defeat-complete-tail-a
```

Members use original repository-relative paths. Do not overlay an active trial;
use a fresh diagnostic directory for new work. Once a producer is restored,
remove its stale `ARCHIVED.json` marker. Historical worktree archives have their
own restoration instructions below. The active source/next work is in
[the current handoff](RE_HANDOFF.md), rather than the historical cleanup logs.

## Earlier cleanup, 2026-10-28

The private audit is `.analysis/cleanup-handoff/2026-10-28/`:

- `accepted-receipts.json`: all 328 C/C++ records then current resolve to 232 receipt
  hashes, with no missing receipt. Retained-parent receipt hashes also agree.
  This is an identity inventory, not a cold replay or full receipt re-import.
- `selection.json` / `result.json`: exact paths and hashes for 24 terminal
  alternative producers, duplicate source backups and unused DOS-assembler
  extraction. All 1,449 archived files were compared before original removal.
- `trial-summary.json`: compact results from the archived compiler trials.
- `diagnostics.tar.xz`: path-preserving private archive, 3,193,216 bytes,
  SHA-256 `2d9fbba6225f54748efe7e89ba27d81960fd8409b7b6eebc1366dc1151175b8e`.

Archiving reclaimed about 25.1 MiB of allocated storage. Regenerable Python
caches under `scripts/` and `tests/` were removed. Loose Git objects were
repacked without dropping history. Current baseline/raw-equal diagnostics,
all acceptance evidence and installed tools remain at their existing paths.
The alternative TASM16 extraction is archived; it was never added to the pinned
accepted toolchain.

Restore a specific historical trial only if needed. From the repository root:

```sh
sha256sum .analysis/cleanup-handoff/2026-10-28/diagnostics.tar.xz
# Compare with the SHA-256 above, then restore only the desired directory:
tar -xJf .analysis/cleanup-handoff/2026-10-28/diagnostics.tar.xz \
    .analysis/native-producers/main-yumeko-swords-decay-else-a
```

Archive members retain original repository-relative paths. Review
`selection.json` before restoring other members; do not overlay an active trial.
The removed experimental dialog/combined-Yumeko wrappers and binders also
remain in Git history and their frozen producer snapshots. Canonical semantic
bodies and current standalone wrappers are maintained under `src/`.

## Keep live for incremental reconstruction

- `.analysis/targets/` and `.analysis/decoded/`: pinned originals and decoded
  payload/receipt/ordered-relocation views.
- `.analysis/unit-replays/`: accepted receipts, both producers, controls, source
  snapshots and tool evidence. Retained-parent reviews can hash every file in
  their parent archive, including logs; those files are not disposable caches.
- Native ASM/vendor evidence under `.analysis/`, including calibration
  `.analysis/builds/`, ownership reviews and actual source/object/listing inputs.
- `.analysis/toolchain/`, `.tools/`, `_reference/` and `ghidra-project/`:
  installed compiler/Wine state, pinned analysis tools, references and projects.
  Shared installations and sibling repositories are not cleanup targets.
- Current baseline/raw-equal native producers and their reviews/proposals.
  A failed aggregate can still contain accepted complete scopes.

Public CI does not validate private evidence retention. Check actual path
ownership before further pruning; a filename containing “failed” proves nothing
about its dependencies. Ordinary source-tree Python caches can be regenerated;
use `PYTHONDONTWRITEBYTECODE=1` for cleanup checks.

## Earlier cleanup, 2026-10-25

Three dirty duplicate worktrees were archived and retired: `op-score-canonical`,
`verdict-full-context` and `staff-full-context`. Their verified archives and
base/branch/status metadata remain in `.analysis/cleanup-handoff/worktrees/`.
For example, restore the recorded branch/base first, then overlay its archive:

```sh
git worktree add .analysis/worktrees/staff-full-context reconstruction/staff-full-context
tar -xzf .analysis/cleanup-handoff/worktrees/staff-full-context.tar.gz \
    -C .analysis/worktrees/staff-full-context
```

Old producer commands may mention those retired worktree paths. Normal root
incremental replay does not require restoring them. The old
`.analysis/cleanup-current-receipt-guards.json` inventory describes 298 records
at that historical point; the current inventory is the 2026-11-06 one above.
