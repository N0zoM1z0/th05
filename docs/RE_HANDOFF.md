# TH05 reconstruction — agent handoff (2026-11-13)

## Start here

Work in the live `main` repository. Read [AGENTS.md](../AGENTS.md),
[the focused workflow](RE_WORKFLOW.md) and [the exactness contract](ORACLES.md).
Start with `git status -sb` and `git log -5 --oneline`. Preserve any dirty work;
do not reset, stash or discard it. Commit substantive progress as
`gpt-web: ...`; do not push without permission.

Use the generated [progress report](PROGRESS.md), accepted-unit ledgers and
[`resources/ownership.json`](../resources/ownership.json) as the current
counts and gap inventory. Do not maintain a second handwritten progress table.
The 98% goal is still **unmeasured** because the global authored-byte
denominator has not been accepted. The pinned Japanese game copy remains
candidate-local-attested rather than independently confirmed pristine.

For documentation-only changes, inspect the relevant source and diff; no
compiler replay, preflight or full CI is needed. For source changes, replay only
the complete affected owners and shared consumers. Never run a full cold replay
just to confirm a local change.

## Current ZUN state

The resident `-S` entry is no longer an open compiler problem:

- `zun-resident-main`: natural C++ `main()`, **269/269 bytes**, two independent
  cold producers, no relocations. The source-comment cleanup was followed by
  a focused two-producer replay; the compiled negative remains rejected. See
  [`initialize.md`](../src/zun/resident/initialize.md).
- `zun-resident-config`: exact 322-byte `cfg_init()`.
- `zun-resident-semantic-initialized-data`: exact 320-byte initialized DATA.
- Original C0T CRT: 613 source-written CODE bytes and 110 initialized DATA
  bytes. Its two-byte writable CS runtime slot remains deliberately unowned.
- Master resident memory/graphics family: 226 bytes (224 instruction bytes,
  two alignment bytes); Master file/DOS family: 830 bytes (823 instruction
  bytes, seven alignment bytes). Both are vendor-origin, zero authored credit.
- Borland CT.LIB `brk`/`sbrk`: 127 exact relocated CODE bytes, five OMF
  relocations. `___brk` and `___sbrk` are the nearheap call targets; `_errno`
  and `___brklvl` resolve into the accepted CRT DATA.
- Borland CT.LIB `nearheap`: 631 exact relocated CODE bytes plus six exact
  initialized DATA bytes, 26 OMF relocations. Both modules are vendor-origin,
  zero authored credit. Their parsers and acceptance records are
  `scripts/review_zun_brk.py` / `config/zun_brk_acceptance.json` and
  `scripts/review_zun_nearheap.py` / `config/zun_nearheap_acceptance.json`.

The ZUN view currently has **3,110 unknown bytes** in five outer-file
intervals. They are intentionally left unknown and are not all assumed to be
code:

| Outer `ZUN.COM` interval | Bytes | Corresponding `-S` COM interval / note |
| --- | ---: | --- |
| `0x0D47..0x0D49` | 2 | Writable CRT CS runtime slot |
| `0x13BA..0x1601` | 583 | `0x09D6..0x0C1D` |
| `0x18F7..0x2034` | 1,853 | `0x0F13..0x1650` |
| `0x21E2..0x244E` | 620 | `0x17FE..0x1A6A` |
| `0x2454..0x2488` | 52 | `0x1A70..0x1AA4` |

The next useful ZUN investigation is the remaining `-S` resident code and
storage. A local CT.LIB sequence scan is retained as
`.analysis/gpt-web-zun-clib-scan.py`. It found promising *heuristic* candidates
in the first two intervals:

- `0x09D6..0x0C1D`: `exit`, `setupio`, `ioerror`, `lseek` and `atexit`.
- `0x0F13..0x1650`: `fseek`, `write`, `setargv`, `setvbuf`, `_pathops`,
  `fflush`, `writea`, `flushall` and `xfflush`.

These are byte-sequence leads only, not accepted ownership. For each candidate,
identify the complete original OMF member and public boundaries, resolve every
FIXUPP using the actual segment/group/external context, and compare the whole
scope. Do not promote a percentage match or infer that all remaining bytes are
library code. The later resident tail and the 52-byte pre-`-G` interval still
need CODE/DATA/INIT/BSS boundary analysis.

The full ZUN ownership summary and current intervals are in
[`ZUN_OWNERSHIP_MAP_2026-11-13.md`](reconstruction/ZUN_OWNERSHIP_MAP_2026-11-13.md).

## Recent closure

- **Yumeko `swords_update()` source refinement (2026-11-13)**: the complete
  283-byte updater now has a fully natural C++ source that reproduces the
  complete 2,139-byte MAIN03 original-order context in two fresh native
  producers; its compiled twirl-step negative is rejected. The reviewed ASM
  family remains the sole CODE owner, so no duplicate credit is claimed. See
  [`swords_update.md`](../src/main/boss/yumeko/swords_update.md).
- **Alice ready-byte lifetime (2026-11-13)**: original DS:C68C / `boss_statebyte[10]`
  has exactly one Alice-owned access, a value-24 store at the Ready transition;
  no Alice-owned callback reads it. The source now names the write
  `ready_phase_store_only` / `ALICE_READY_PHASE_STORE_VALUE`, without implying
  a consumed seed or timer. The complete 939-byte Alice updater and its five
  accepted scratch-header consumers were replayed together (six full owners),
  twice byte/fixup exact with the existing negative rejected. No new CODE or
  storage credit is claimed. See
  [`alice/update.md`](../src/main/boss/alice/update.md).
- **EX-Alice later-pattern scratch lifecycle (2026-11-13)**: bytes 13/14 now
  have explicit Firewave and Spiral views over the same original 16-byte Boss
  state array. Byte 13 is their shared turn phase; byte 14 is the firewave
  angle or spiral acceleration step. A bounded original-code xref also proved
  byte 15 is a Ready-time direction seed consumed by the second wave-1 pattern
  (turning rings), not an initial-fan substate. Eight complete C++ owners,
  including the 1,060-byte update controller, and the separate 334-byte
  TCC-S/TASM32 spiral owner all replay exact with their original relocations;
  compiled negatives are rejected. No new CODE/storage credit is claimed.
  See [`exalice/full_context.md`](../src/main/boss/exalice/full_context.md).
- **Shinki Devil angle protocol (2026-11-13)**: the 802-byte
  `pattern_devil()` now names the remaining 2,500-frame fast-stage gate,
  prelude and turn-angle increments, three-pellet decorative spread, zero
  angle origin and shared 0x80 laser/bullet mirror. A focused 12-unit replay
  covers the Devil leaf, all `shinki.cpp` consumers and the complete 959-byte
  controller; two native Borland/TLINK producers match every original byte
  and ordered relocation, and the 2500→2501 compiled negative is rejected.
  The attempt also pinned a TC4.02 codegen constraint: postfix byte INC/DEC
  must remain postfix to preserve the direct memory instructions. No duplicate
  CODE credit is claimed. See [`shinki/devil.md`](../src/main/boss/shinki/devil.md).
- **Sara cross-wave pattern history (2026-11-13)**: the one physical
  `boss_statebyte[10]` previous-mode selector is initialized once at the
  entrance, retained through the blue/red-to-spinning-rings phase transition,
  and prevents the first mode of phase three from repeating the last mode of
  phase two. The complete 1,824-byte / 12-function controller passed two fresh
  Borland/TLINK producers, all original bytes and ordered fixups, and its
  existing compiled negative. No duplicate CODE credit. See
  [`sara.md`](../src/main/boss/sara/sara.md).
- **BB loader return-order boundary (2026-11-13)**: further actual TC++ 4.02
  producers show that lexical scope and an explicit AX return do not move the
  saved-SI restore ahead of the return-value load. Explicit SI preservation
  duplicates the compiler's save/restore and shifts the allocator relocation.
  The best natural C++ source remains 51/55 with the correct +7 relocation;
  the remaining four bytes are solely `MOV AX,[4204]; POP SI` versus native
  `POP SI; MOV AX,[4204]`. The exact 55-byte reviewed ASM remains sole owner.
  See [`bb_load.md`](../src/main/formats/bb_load.md).
- **Louise shared Boss-mode and scratch-byte protocol (2026-11-13)**:
  mode 0 is reposition, mode 1 is blue-spread/sweeping-laser, and mode 2 is
  red-stack/turning-ring. Byte 14 alternates the later laser/ring selector;
  byte 15 is toggled by blue spreads, consumed by red stacks, then overwritten
  by the later laser's random side. The complete 429+603+582+122-byte Louise
  source closure replays exact twice with original ordered fixups and the
  compiled fan-angle negative rejected. No duplicate CODE credit. See
  [`louise/update.md`](../src/main/boss/louise/update.md).
- **Vector2 near MOVSX frontend/register boundary (2026-11-13)**: TCC-S near
  Pascal trials reject inline `MOVSX` from BP/table operands and register
  operands, even with far-vector-style C-linkage declarations. Ordinary inline
  MOV succeeds. Direct `_EDX = length` and reordered table reads still use EAX
  as TCC's signed-load scratch; compound pseudoregister products can become
  the wrong multiply and logical shift. The semantically correct natural C++
  remains 67 bytes; the 55-byte ASM remains sole exact owner. See
  [`vector2_near.md`](../src/shared/math/vector2_near.md).
- **Mai/Yuki defeated-character lifetime (2026-11-13)**: the one byte of
  `boss2.phase_state` is now explicitly viewed as `patterns_seen` during
  combat and `defeated_character` after the result-minus-one handoff (Mai=0,
  Yuki=1). A one-byte overlay and named accessor preserve the canonical
  24-byte Boss layout. The complete 1,018-byte controller, 194-byte foreground,
  111-byte hit provider and 75-byte sprite helper replay exact twice with all
  original ordered fixups; the compiled negative is rejected. No duplicate
  CODE credit. See [`update_context.md`](../src/main/boss/mai_yuki/update_context.md).
- **Pointnum invalidator natural-C++ exact alternative (2026-11-13)**:
  `pointnums_invalidate()` now stages current X in DOS `_AX` before the
  previous-Y/current-X Pascal call. Two fresh native Borland/TLINK producers
  match all44 original bytes and the empty ordered relocation stream; the
  compiled height8→9 negative is rejected. The reviewed ASM remains sole
  credited owner, so no duplicate CODE bytes are added. See
  [`invalidate.md`](../src/main/pointnum/invalidate.md).
- **Gather template-copy leaf (2026-11-13)**: the 27-byte exact ASM owner
  remains authoritative. New natural C++ alternatives were compiled: indexed
  WORD loop 50 bytes, SI/DI pointer loop 44 bytes, best register do/while loop
  42 bytes, byte-count loop 44 bytes; explicit `memcpy()` links unsuccessfully
  on `_memcpy`. None replaces the original inline seven-WORD `REP MOVSW`, and
  these first-producer diagnostics receive no acceptance or CODE credit. See
  [`gather/copy.md`](../src/main/gather/copy.md).
- **B4-ball updater (2026-11-13)**: `b4balls_update()` remains exact at 273
  bytes with ordered fixups `[235,156,118]`. The unused false-return helper
  was simplified to an empty inline `void`; two fresh positives and the
  compiled 550→551 negative pass. This is source cleanup, not new byte credit.
  See [`b4ball_update.md`](../src/main/boss/mai_yuki/b4ball_update.md).
- **`vector2_near()` small-leaf boundary (2026-11-13)**: natural C++ remains
  67 bytes against the 55-byte reviewed ASM body. TCC `-S`/TASM32 produces the
  same 67-byte shape; semantic inline-MOVSX attempts in this near TU fail at
  the TCC frontend. The 12-byte register-copy residual is documented, and
  the reviewed ASM remains the only exact owner. No C++ credit is claimed.
  See [`vector2_near.md`](../src/shared/math/vector2_near.md).

## Other open work

1. **BB resource loader**: its 55-byte function is already exactly owned as
   original-language ASM. The maintained C++ context candidate matches 51/55
   bytes in two producers with the original +7 relocation; the only residual
   is `MOV AX,[bb_load_seg]; POP SI` versus native `POP SI; MOV AX,[bb_load_seg]`.
   A CX-held/stack-DS alternative reproduces 51 bytes twice but shifts the
   relocation to +6 and relies on CX surviving DOS open, so it remains a
   diagnostic only. `-k`, `-r`, `-O-` and explicit-SI matrices do not solve the
   epilogue order. The exact ASM remains sole owner. See
   [`bb_load.md`](../src/main/formats/bb_load.md).
2. **Remaining physical ownership gaps**: use the live intervals in
   `resources/ownership.json` and the current
   [`UNACCEPTED_COHORTS.md`](reconstruction/UNACCEPTED_COHORTS.md). Check
   physical source bounds, real consumers, initialized data versus uninitialized
   storage, and original ordered relocations before making a claim.

The large MAIN Boss control/update contexts for Sara, Shinki, Alice, EX-Alice,
Yumeko and Mai/Yuki already have accepted full-function coverage. Continue
working on demonstrated large semantic gaps; do not invent functions from
zero-filled unknown storage or duplicate accepted ASM/C++ extents.

## Focused verification

For the current ZUN workstream, these bounded checks cover the recent resident
ownership changes without a full cold replay:

```sh
python3 scripts/review_zun_brk.py --check
python3 scripts/review_zun_nearheap.py --check
python3 scripts/replay_zun_crt.py --check
python3 scripts/replay_zun_resdata.py --check
python3 scripts/replay_zun_file_native.py --check
python3 scripts/ownership.py --check
python3 scripts/progress.py --check
python3 scripts/ci.py
git diff --check
```

For a C/C++ edit, inspect `scripts/replay_units.py --plan`, replay every
complete affected owner and accept its receipt into the correct artifact
ledger. For ASM or native vendor changes, use that scope's focused replay and
preserve the original ordered relocation proof. Two deterministic producers,
full raw bytes and the appropriate compiled/assembled negative are required;
a successful build or a same-sized result is not acceptance.

## Local state and storage

`.analysis/`, `_reference/`, `.tools/` and `ghidra-project/` are ignored local
state and are not transferred by Git. Preserve original targets, the pinned
Borland/Wine toolchain, Ghidra project, current ledger-referenced replay
receipts and producers, accepted native/vendor evidence, and the unresolved
ZUN CT.LIB scan. The obsolete failed ZUN `main()` compiler matrices and their
one-off scripts/results have been removed now that the natural entry is accepted. The
cleanup removed 223 superseded experiment directories (4.88 MiB), the old
`.analysis/zun-resident` scratch tree (1.32 MiB), 41 one-off scripts/results,
and seven unreferenced replay folders (7.78 MiB): **14.14 MiB total**. Those
seven replay folders had no receipt hash in any of the four accepted ledgers and no
direct tracked path reference. All other ledger-matched or directly referenced
replay folders were retained. The `.analysis/zun-resident-review` ABI notes,
Borland toolchain, current receipts, and CT.LIB scan were preserved.

The analysis store still occupies about **1.5 GiB**, mostly pinned toolchain,
accepted producer evidence, builds and unresolved work. Do not remove more by
age or name alone; repeat the ledger-hash and direct-reference audit before
any further replay cleanup. A handoff to another computer requires transferring
the necessary ignored inputs separately; a Git clone is not sufficient.

This is the live handoff, not a running change log. Historical experiments
that no longer affect an open decision belong in Git history, not in a long
current-status document.
