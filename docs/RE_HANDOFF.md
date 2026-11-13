# TH05 reconstruction — agent handoff (2026-11-13)

## First actions

Work in the live `main` repository. Read [AGENTS.md](../AGENTS.md),
[the focused workflow](RE_WORKFLOW.md) and [exactness criteria](ORACLES.md).
Check `git status -sb`, run `python3 scripts/preflight.py`, then inspect
`python3 scripts/replay_units.py --plan`. **Carry forward any dirty work**;
it belongs to this workstream. Commit substantive progress as
`gpt-web: ...`, and do not push without permission. Never use a full cold
replay just to confirm one changed unit.

## Verified current state

| Canonical measure | Value |
| --- | ---: |
| Accepted C/C++ units (MAIN / OP / MAINE / ZUN) | **537** (351 / 75 / 109 / 2) |
| Source-authored exact C/C++ CODE | **108,784 B** |
| Source-authored initialized C/C++ DATA | **17,513 B** |
| Combined source-authored C/C++ exact bytes | **126,297 B** |
| Unclassified decoded bytes (MAIN / OP / MAINE / ZUN) | **303 / 2,370 / 1,795 / 8,559** |
| Total unclassified decoded bytes | **13,027 B** |

Read the **live** [generated progress](PROGRESS.md),
`config/accepted_units*.json`, `config/exact_units*.toml` and
`resources/ownership.json` before updating any count. The global **98%
authored-byte target is not yet measurable**: a reliable authored-byte
denominator has not been established. There is no accepted full packed
EXE/COM reconstruction. The pinned Japanese game copy is
*candidate-local-attested*, not independently established as pristine.

## Highest-value unresolved work

1. **ZUN resident `main()`**, original 269 bytes in the `-S` COM at
   `[04A9,05B6)`: natural source is still **not exact**. The retained
   success-first first-producer candidate emits 269 bytes with **252 matching
   byte positions and 17 differences**, all around the `-R` removal block.
   Error-first alternatives typically emit 260 bytes because the compiler
   merges error exits. Do not mistake the 252 *matches* for 252 differences,
   accept identical length alone, or repeat the 90 lexical-return / 16 nested
   error-path variants. See [the specific compiler findings](reconstruction/ZUN_RESIDENT_REMOVAL_BRANCH_2026-11-12.md).
   The independently accepted `cfg_init()` and resident DATA remain exact. Three shared-error-tail and two comma-return
   first-producer variants have also failed; do not repeat them without a new
   control-flow hypothesis.
2. **Yumeko `swords_update()`**: the actual 283-byte function already has
   an exact **reviewed ASM** owner. Its *natural C++ alternative* is not
   exact in the nine-function original context: `-O` makes the correct near
   conditional jumps but drops two short joins, yielding 2,135 bytes versus
   2,139 original. The `-O-`, local-switch and final-Y/GOTO experiments also
   failed. Use [the compiler review](reconstruction/YUMEKO_TWIRL_COMPILER_2026-11-11.md),
   not fabricated NOPs, padding or side effects. This is a language-source
   improvement, **not newly uncovered executable CODE**. Additional `-G`/`-Z`, while/do-while/for-ever, helper extraction
   and explicit `register` hint trials also failed to retain the two original
   short joins; see the updated compiler review before proposing an equivalent
   variant. Manual loop-tail `continue` once matched 2,139 bytes and fixups but
   bypassed the manual increment, so it is semantically invalid. The correct
   explicit-goto variants and clip/hit label, `do/break`, and trampoline forms
   also fail; do not revive the invalid size match.
3. **BB resource loader**: the 55-byte function is already exactly owned
   as [original-language ASM](../src/main/formats/bb_load.md). Its natural
   C++ alternative still emits 56 bytes with a different stack-frame and
   register-save order. Do not double-count the ASM bytes.
4. **Original ownership gaps**: use the current intervals in
   `resources/ownership.json`, not an old gap list. Verify physical source
   boundaries, native consumers, initializers versus `?` storage, and
   ordered original relocations. See [open candidates](reconstruction/UNACCEPTED_COHORTS.md)
   and the [CDG slot storage discrepancy](reconstruction/CDG_STORAGE_TARGET_BOUNDARY_2026-11-13.md).
   CDG's TASM `_BSS` declaration alone does **not** justify treating original
   nonzero or out-of-file bytes as a zero-filled owner.

## Already solved — avoid duplicate CODE credit

The maintained natural C/C++ already reproduces major complete Boss
contexts: [Sara's 12-function 1,824 B](../src/main/boss/sara/sara.md),
[Shinki's 959 B update and 802 B Devil](reconstruction/SHINKI_DEVIL_COLUMN_PROTOCOL_2026-11-13.md),
[Alice's 939 B controller and 499 B charged attacks](reconstruction/ALICE_CHARGED_ATTACKS_SHARED_SOURCE_2026-11-12.md),
[EX-Alice's 1,060 B controller](reconstruction/EXALICE_WAVES_CONTROL_FLOW_2026-11-13.md),
[Yumeko's 884 B controller](../src/main/boss/yumeko/update.md),
and [Mai/Yuki's 1,018 B paired update](reconstruction/MAI_YUKI_STACK_CHEETO_CLOSURE_2026-11-13.md).
Shinki's [19-function, 3,254 B background family](reconstruction/SHINKI_SPINLINE_FAMILY_2026-11-12.md)
was also recovered. Source refactors have been replayed across complete
affected owners; **their accepted CODE must not be credited again**.

Separate ownership lanes include reviewed ASM, foreign Master/CL startup
CODE, bitmap/font resources, compiler-authored initialized C/C++ DATA,
and source-backed **uninitialized** storage. Recent Master
[BGM track/effect BSS](reconstruction/MASTER_BGM_TRACK_BSS_2026-11-13.md)
(198 B per MZ) and [VSYNC state](reconstruction/MASTER_COMPACT_BSS_2026-11-12.md)
(10 B per MZ) reduced unknown by 624 B but earned **zero initialized C/C++
DATA or CODE credit**. The original game
[point-number doubling flag](../src/main/item/pointnum_twice_initial.md)
was independently accepted as one initialized C++ byte. The Master 0.23 GRCG/graphics review now covers **24 complete
procedures / 3,988 vendor CODE bytes**, including the newly source-verified
six-byte `GRCG_BOXFILL_RETURN` entry at `0EA0..0EA6`; see [the full source
review](reconstruction/MASTER_GRCG_NATIVE.md). For a corrected
example of ambiguous zero-valued data, see
[the physical ownership correction](../src/main/stage/bonus_previous_resources.md).

## Fast, bounded verification

For a C/C++ change, first inspect `scripts/replay_units.py --plan`; a shared
header/`.inl` may affect several units. Rebuild **every selected complete
owner**, then accept the receipt into the appropriate artifact ledger:

```sh
python3 scripts/replay_units.py --units UNIT_ID --output .analysis/unit-replays/UNIQUE_RUN
python3 scripts/progress.py --artifact main --accept .analysis/unit-replays/UNIQUE_RUN/receipt.json --write
python3 scripts/ownership.py --write
python3 scripts/replay_units.py --plan
python3 scripts/ci.py
git diff --check
```

Use `--artifact op|maine|zun` for the other target ledgers, including in
`replay_units.py`. Two actual deterministic compiler/linker producers,
full raw bytes, OMF scope, ordered original loader fixups and the compiled
negative must pass; no source-language credit from copied bytes or a
source-free binder. **Documentation-only edits need no compiler replay or
new acceptance receipt.** Consult [the full short workflow](RE_WORKFLOW.md)
for ASM and special-context details.

## Local evidence and storage for the successor

`.analysis/`, `_reference/`, `.tools/` and `ghidra-project/` are ignored
**local state**, not transferred with Git. Keep original pinned targets,
calibration object/MAP pairs and original source copies, the game's Wine
prefix/compiler toolchain, Ghidra project, all current ledger-referenced
`unit-replays` receipts with their two producers and negative snapshots,
and accepted ASM/native review evidence. Keep the distinct unresolved
ZUN/Yumeko scripts and diagnostic summaries needed to avoid repeating known
failed compiler hypotheses. Stale, unreferenced historical replay clones
can be removed **only after checking current receipt hashes and references**.
A handoff to a different computer requires transferring the necessary
ignored inputs separately; `git clone` alone is insufficient.

On 2026-11-13, **88 obsolete, unreferenced** `.analysis/unit-replays/`
folders were deleted (about **85.3 MiB** of allocated files). They were
neither current ledger receipt-SHA matches nor directly referenced from
tracked repository content. All **386 distinct current receipt hashes**
were checked before and after; the separately referenced historical
folders, the original inputs, active toolchain and diagnostic worktrees
were retained. Repeat this inventory check before any further deletion.

This is the live handoff, not a running change log. Historical results and
failed experiments belong in the linked per-function notes and Git history.
