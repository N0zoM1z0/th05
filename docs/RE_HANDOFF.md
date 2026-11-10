# TH05 handoff — 2026-11-10

> Current workflow: follow the **Highest priority** section in `AGENTS.md`.
> Prefer affected exact comparisons and useful Markdown knowledge. Ordinary
> notes do not require full CI, native replay or document-hash/pin refreshes.
> Older broad validation instructions apply only when their impact is relevant.


The original MAIN `tiles_invalidate_all` is now fully recovered as a 22-byte
register-level ASM kernel (`BD38..BD4E`). Two independent TASM/TLINK producers
and its own dirty-value negative pass: true ES:DI/32-bit REP STOSD of the 1600-byte
flag bank. This adds reviewed ASM ownership, **not C++ CODE credit**. The failed
16-byte natural C++ intrinsic is unchanged. See
[tile invalidation](../src/main/tile/invalidate_all.md).

Yumeko's two large Boss attacks now pass independent exact MAIN source replays:
aimed swords354 and laser/swords428 (782 new authored C++ bytes). Their genuine
ten-function C++ context restores the original unsorted OMF relocation order,
while the 283-byte sword updater remains size-exact but raw-inexact. Four
changed accepted standalone wrappers were refreshed only in affected local
replays. See [Yumeko attack context](../src/main/boss/yumeko/attacks_context.md)
and [detailed attack evidence](../src/main/boss/yumeko/laser_swords.md).

A complete native-ASM `CDG_FREE_ALL` loop now passes MAIN focused replay: 14
bytes and a semantic negative, using its true same-CS FAR Pascal provider and
BYTE-aligned original shared segment. See
[src/main/formats/cdg_free_all.md](../src/main/formats/cdg_free_all.md).
The PMD resident detector is now exact across MAIN, OP and MAINE: three
independent 46-byte C++ source owners (138 total), each passing two fresh
producers, ordered fixups and an own compiled negative.
OP ZUNsoft CODE **and** its independent filename DATA also pass focused
individual two-producer exact replays and are committed. A separate attempt on
MAIN's larger boss/attack controllers identified reproducible code-generation
gaps without claiming byte credit: boss defeat 414/408, B4 ball 273/278 (or
274 without optimization), and Mai tracking laser 186/185. MAINE's1034-byte
menu remains raw-exact but ordered-relocation-inexact even via TCC-S/TASM32.

Start with `git status --short` and `python3 scripts/preflight.py`. Read
[workflow](RE_WORKFLOW.md) and [acceptance](ORACLES.md). Reuse the existing attested
tools and decoded targets; do not bootstrap or cold-replay unchanged units.

Private first-diagnostic helpers are `.analysis/single-main-native-producer.py`
(MAIN), `.analysis/single_op_producer.py` (OP), and
`.analysis/single_native_producer.py` (MAINE). They produce one diagnostic,
never an acceptance receipt; formal replay remains the normal workflow.

## Authoritative accepted state

Use the [generated progress](PROGRESS.md), accepted-unit ledgers and
[ownership inventory](../resources/ownership.json) for current totals and scopes.
The global authored denominator remains unreviewed. The supplied Japanese copy
is candidate-local-attested.

## Latest exact cross-artifact leaf: PMD detector

`src/shared/sound/pmd_resident.cpp` now preserves the real AX/ES interrupt
vector and return contract. The old local result compiled to 51 bytes; using
the native `_AX` result yields the full 46 bytes and zero fixups in all three
independently built MAIN, OP and MAINE targets. Own 60h→61h compiler negatives
are rejected in each. Focused receipts:
`.analysis/unit-replays/gpt-web-{main,op,maine}-pmd-resident-20261110/receipt.json`.
Only these three functions (138 authored CODE bytes) are newly credited.

## Previous accepted packet: OP ZUNsoft CODE

Four natural C++ functions, including the 654-byte logo controller, now own the
complete decoded OP `B616..BA94` extent: **1150/1150 raw bytes** and all
**33/33 original ordered relocations** in both independent cold producers.
The compiled spawn-speed negative was rejected. Of the 1150 bytes, 1102 are
instructions and 48 are the controller's compiler switch table; no padding.

- Maintained source: [ZUNsoft](../src/op/zunsoft/zunsoft.md).
- Accepted unit: `op-zunsoft` in `config/exact_units.op.toml` and
  `config/accepted_units.op.json`.
- Focused receipt: `.analysis/unit-replays/gpt-web-op-zunsoft-20261110/receipt.json`.
- Native preliminary review remains at `.analysis/op-zunsoft-native-review.json`.

The independent six-filename initialized DATA contribution at decoded OP
`FECA..FF00` now also passes: 54/54 bytes, two cold producers and a compiled
filename-mutation negative. The early standalone link needed an original
foreign DATA suffix through DS:2817 to satisfy DOS MZ stack bounds; the
compiler-owned `_DATA` remains complete at DS:0EEA..0F20. The separate receipt
is `.analysis/unit-replays/gpt-web-op-zunsoft-filenames-b-20261110/receipt.json`.
Both ZUNsoft scopes are accepted. Continue the substantial MAIN Boss gaps,
especially the Shinki ball updater and generic defeat controller.

## 2026-11-10 Boss and Staff investigation (unaccepted)

Focused native/actual compiler analysis continued on substantial owner
functions. Shinki's ball updater has a 221-byte natural `-O-` trial against
native 220 (last short/near branch-layout difference); Yumeko's sword updater
can now compile the original 283-byte complete *size* with fixup `[75]`, but
still differs in twirl branch output; the generic boss-player collision
remains 43 target versus 45 best candidate. Source/ABI outcomes, failed
variants and next codegen questions are recorded in each owner Markdown.

The two Staff verdict VRAM transfer routines now have one maintained semantic
ASM candidate covering all 126 native instruction bytes, but pinned TASM32
emits three different XOR opcode-direction bytes and reverses two ordered
fixups. It remains **outside** the live ASM manifest and earns zero credit;
see `src/maine/staff/bitmap.md`. Unmodified accepted C++/ASM owners were never
replayed. All these diagnostics are available privately under
`.analysis/gpt-web-*/`; no full-set cold replay was performed.

## Settled and pending work

MAIN current-score load/save are independently accepted, 55 bytes each. Load's
source `-O-` profile preserves its native early RET; the combined optimized
wrapper remains 109 versus 110 and is not a whole-TU acceptance. MAINE's score
insertion/rendering five-function family (1443 compared / 1440 authored) and
creation/animation pair (1062 compared / 1060 authored) are accepted. Major boss
update callbacks already have accepted owners; check the current manifests
before relying on old census/routing files.

| Still unaccepted | Current evidence | Notes |
| --- | --- | --- |
| MAINE registration menu, 1034 | Raw exact; original relocation order differs | [Menu](../src/maine/registration/menu.md) |
| MAIN shot collision, 399 + 210 | Current pair 419 + 233; quotient gaps remain. Selector transfer now correctly NOP/PUSH CS/CALL, far Pascal RETF8 | [Shots](../src/main/player/shot_runtime.md) |
| Staff updater/render, 626 / 861 | Current 623 / 858. Renderer `-O-` still byte-identical 858; `-Z-` and documented source trials fail | [Staff](../src/maine/staff/full.md) |
| Staff controller, 991 | Raw exact; ordered fixups differ. Bitmap prefix remains inexact | [Controller](../src/maine/staff/controller.md) |
| Yumeko sword update, 283 | Current 283 matches size and fixup but differs in twirl branches; both later large attacks accepted separately | [Swords](../src/main/boss/yumeko/swords_update.md) |
| Dialog opcode, 456 | Direct 455; compiler-assembly raw 456 has wrong fixup order | [Dialog](../src/main/dialog/opcode.md) |
| EMS boss-face preload, 154 | Raw exact; `[71,24,133,114]` order unresolved | [EMS](../src/main/ems/ems.md) |
| Generic boss defeat/collision, 414 / 43 | Current 408 / 46; four new natural branch trials still merge all-clear calls | [Generic boss](../src/main/boss/generic.md) |
| OP score decode, 169 | Ordinary key emits 181. TC4 rejects assembly inside inline/template functions | [Decoder](../src/shared/score/decode.md) |
| ZUN resident entry, 269 | Current 260; `-O-` emits 262 | [Resident](../src/zun/resident/initialize.md) |

Use [the candidate index](reconstruction/UNACCEPTED_COHORTS.md) and per-owner
notes for other gaps. Do not repeat unchanged failed profiles, insert barriers,
copy instruction sequences or promote failed C++ to ASM. Ordinary recovery
needs no new defensive tests, CPU models or per-function extra negatives.

## Local working state

Current accepted replay roots, calibration inputs and the completed ZUNsoft
producer receipts remain available. Superseded builds and diagnostic archives have been
removed; use the findings in per-owner notes instead of archive restore recipes.
The independent Wine prefix, Ghidra project and Factory tool selectors are live.

Default `scripts/ci.py` checks the complete public checkout without private
inputs. Select comparator/build tests for tooling changes and exact replays for
new or affected source; `--full` remains an explicit broad tooling run.
