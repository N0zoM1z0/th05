# TH05 reconstruction — live agent handoff (2026-11-13)

## Start here

1. Read [AGENTS.md](../AGENTS.md), [the workflow](RE_WORKFLOW.md) and the
   [exactness contract](ORACLES.md).
2. Inspect `git status -sb` and `git log -5 --oneline` before editing. The
   current worktree is clean; preserve any later agent's in-progress changes.
3. Use [generated progress](PROGRESS.md), the four accepted-unit ledgers and
   [`resources/ownership.json`](../resources/ownership.json) as the source of
   current counts and physical gaps. Do not maintain duplicate totals here.

The target is **98% authored bytes exact**, but the global authored-byte
 denominator remains **unmeasured**. The supplied Japanese game copy is
 `candidate-local-attested`, not independently confirmed pristine. ReC98 and
 sibling-project acceptance do not transfer to this repository.

## Current state

- Work on the live `main` repository. Commit locally as `gpt-web: ...`; do not
  push without permission.
- All six large MAIN Boss controllers (Sara, Shinki, Alice, EX-Alice, Yumeko,
  Mai/Yuki) have accepted complete-function coverage. Continue semantic
  analysis only where a concrete lifecycle or behavior question remains; do
  not recreate accepted extents.
- Recent Boss work clarified the fixed circular explosion API in the shared
  defeat path and typed Mai Solo's byte-10 laser-counter/revenge-angle reuse.
  Both changes preserve original bytes and have focused multi-owner receipts;
  see [`generic.md`](../src/main/boss/generic.md) and
  [`solo_scratch.md`](../src/main/boss/mai_yuki/solo_scratch.md).
- The 40-byte natural-C++ Scroll coordinate converter is also exact, but
  occupies the same physical interval as the accepted reviewed-ASM owner. It
  is an alternative implementation, not a second ownership claim; see
  [`coordinates.md`](../src/main/scroll/coordinates.md).
- The generated progress report currently records **538** accepted bounded
  C/C++ units and **126,566** authored C/C++ bytes across MAIN/OP/MAINE/ZUN.
  See [PROGRESS.md](PROGRESS.md) for the current artifact breakdown and the
  separately counted reviewed-ASM work.

## Highest-value open work

### 1. ZUN `-S` resident tail — physical ownership, not assumed code

The corrected 18,116-byte launcher ownership map now has **28 unknown bytes**
remaining in nine intervals. The early 583-byte CODE interval, 1,837 bytes
of stdio/path CODE, 610 resident DATA bytes, and the final 52-byte DATA/INITDATA
tail are verified against original Borland CT.LIB and Master 0.23 OMF members
with semantic relocation and public-symbol checks. See the [early CT.LIB review](reconstruction/ZUN_EARLY_CTLIB_2026-11-13.md),
[stdio/path CT.LIB review](reconstruction/ZUN_STDIO_CTLIB_2026-11-13.md),
[resident DATA review](reconstruction/ZUN_RESIDENT_DATA_2026-11-13.md),
[CT.LIB tail DATA review](reconstruction/ZUN_CTLIB_DATA_2026-11-13.md),
and the current ZUN ownership map.

| Outer `ZUN.COM` interval | Bytes | `-S` COM interval / note |
| --- | ---: | --- |
| `0x0D47..0x0D49` | 2 | Writable CRT CS runtime slot; intentionally uninitialized |
| `0x1EE5..0x1EE7` | 2 | `setargv` CODE SEGDEF prefix without LEDATA |
| `0x2026..0x2034` | 14 | Gap after `setargv` CODE LEDATA, before C0T DATA |
| `0x223F..0x2240` | 1 | Gap after Master `version` DATA |
| `0x224B..0x224C` | 1 | Gap between Master `grp` and `resdata` DATA |
| `0x225A..0x225C` | 2 | Gap before CT.LIB `_abort` DATA |
| `0x227B..0x227C` | 1 | Gap between `_abort` and `atexit` DATA |
| `0x23EE..0x23F0` | 2 | Gap between `files2` and `ioerror` DATA |
| `0x244B..0x244E` | 3 | Gap after `ioerror` DATA |

The original `CT.LIB` code is now verified for nine early runtime members and
ten stdio/path members. Six CT.LIB DATA segments and four original Master OMF
DATA members are verified, as are the seven tail DATA/INITDATA segments: 42
initialized bytes and ten uninitialized bytes in the original `setargv` DATA
SEGDEF. The remaining 28 unknown bytes are the writable CS slot and small
segment/data holes. Do not assume every unknown byte is executable.

Start with [the current ZUN ownership map](reconstruction/ZUN_OWNERSHIP_MAP_2026-11-13.md).
The accepted `-S` `brk`/`sbrk` and `nearheap` members are vendor code/data, not
authored credit; their focused checks are `scripts/review_zun_brk.py --check`
and `scripts/review_zun_nearheap.py --check`. The resident DATA and final
INITDATA passes are `scripts/review_zun_resident_data.py --check` and
`scripts/review_zun_ctlib_data.py --check`.

### 2. BB resource loader — unresolved C++ alternative, ASM owner already exact

The complete 55-byte function is already owned by reviewed original-language
ASM. The best natural C++ source emits the full extent and the correct `+7`
relocation but matches **51/55** bytes. The remaining four bytes are the
ordering difference `MOV AX,[bb_load_seg]; POP SI` versus native
`POP SI; MOV AX,[bb_load_seg]`. The CX-held DS experiment also emits 51 bytes
but shifts the relocation and relies on an unproved register lifetime. Do not
describe this as an uncovered executable gap. See
[`bb_load.md`](../src/main/formats/bb_load.md) and
[`bb_load_cpp_candidate.md`](../src/main/formats/bb_load_cpp_candidate.md).

### 3. Near Vector2 — unresolved C++ alternative, ASM owner already exact

The 55-byte near helper is already exactly owned as reviewed ASM. Natural C++
remains 67 bytes, with a 12-byte register-copy residual. The TCC `-S` pipeline
and near-context inline-`MOVSX` parser boundary are documented. See
[`vector2_near.md`](../src/shared/math/vector2_near.md).

### 4. Other physical gaps

Use the live intervals in `resources/ownership.json` and
[`UNACCEPTED_COHORTS.md`](reconstruction/UNACCEPTED_COHORTS.md). Confirm complete
source bounds, real consumers, initialized DATA versus uninitialized storage,
and original ordered relocations. In particular, all-zero bytes do not by
themselves establish variable identity or ownership.

## Exact-work loop

- For documentation-only changes, inspect the relevant source and diff. No
  compiler replay, preflight or full CI is required.
- For source changes, inspect `python3 scripts/replay_units.py --plan`, then
  replay only the complete affected owners and consumers. Use `--artifact op`,
  `maine` or `zun` for their separate ledgers. Never run a full cold replay to
  validate a local change.
- Exact C/C++ acceptance needs two deterministic producers, complete raw bytes,
  original ordered fixups and the shared compiled negative. ASM/vendor work uses
  its own focused replay and ownership decision. A successful build, size match
  or semantic note alone is not acceptance.
- Update `docs/PROGRESS.md` and ownership only when accepted facts change.
  `python3 scripts/ci.py` is the lightweight public consistency check; run
  specialized tooling tests only when the affected tool changes.

Typical focused commands:

```sh
python3 scripts/replay_units.py --plan
python3 scripts/replay_units.py --units UNIT_ID --output .analysis/unit-replays/RUN
python3 scripts/progress.py --accept .analysis/unit-replays/RUN/receipt.json --write
python3 scripts/ownership.py --write
python3 scripts/ci.py
```

## Local inputs and evidence

`.analysis/`, `_reference/`, `.tools/` and `ghidra-project/` are ignored local
state and are not transferred by Git. Preserve the pinned targets, Borland/Wine
toolchain, Ghidra project, current ledger-referenced receipts/producers,
accepted native/vendor evidence, and the unresolved CT.LIB scan. A Git clone
alone is not a complete handoff to another machine; transfer required ignored
inputs separately. Do not delete artifacts by age or name alone: first check
ledger hashes, tracked documentation references and whether the corresponding
problem is still open.

**Local evidence cleanup (2026-11-13):** `.analysis` is now approximately
**1.4 GiB**, down from **1.7 GiB**. The cleanup removed 34 accepted replay
folders only after verifying their complete raw-byte/fixup rounds against the
current ledgers and confirming no maintained document referenced them. It also
removed five incomplete first-producer folders and 195 unreferenced superseded
experiment directories. All **1,170** concrete `.analysis` paths in tracked
Markdown still resolve. Current Yumeko positive/negative/ASM/context evidence,
all documented BB-loader and Vector2 trials, ledger-root receipts, native
producers, calibration builds, ASM evidence, toolchain and Ghidra state remain.
