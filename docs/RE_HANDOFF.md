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

The corrected 18,116-byte launcher ownership map has **3,110 unknown bytes**
remaining in five intervals:

| Outer `ZUN.COM` interval | Bytes | `-S` COM interval / note |
| --- | ---: | --- |
| `0x0D47..0x0D49` | 2 | Writable CRT CS runtime slot; intentionally uninitialized |
| `0x13BA..0x1601` | 583 | `0x09D6..0x0C1D` |
| `0x18F7..0x2034` | 1,853 | `0x0F13..0x1650` |
| `0x21E2..0x244E` | 620 | `0x17FE..0x1A6A` |
| `0x2454..0x2488` | 52 | `0x1A70..0x1AA4` |

A local CT.LIB sequence scan at `.analysis/gpt-web-zun-clib-scan.py` found
heuristic leads in the first two resident intervals (`exit`, `setupio`,
`ioerror`, `lseek`, `atexit`, then `fseek`, `write`, `setargv`, `setvbuf`,
`_pathops`, `fflush`, `writea`, `flushall`, `xfflush`). These are search leads,
not identifications. Recover complete original OMF members, public boundaries,
segment/group context and ordered FIXUPP semantics before assigning CODE,
DATA, INIT or BSS. Do not assume every unknown byte is executable.

Start with [the current ZUN ownership map](reconstruction/ZUN_OWNERSHIP_MAP_2026-11-13.md).
The accepted `-S` `brk`/`sbrk` and `nearheap` members are vendor code/data, not
authored credit; their focused checks are `scripts/review_zun_brk.py --check`
and `scripts/review_zun_nearheap.py --check`.

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
