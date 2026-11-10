# TH05 handoff — 2026-11-10

> Current workflow: follow the **Highest priority** section in `AGENTS.md`.
> Prefer affected exact comparisons and useful Markdown knowledge. Ordinary
> notes do not require full CI, native replay or document-hash/pin refreshes.
> Older broad validation instructions apply only when their impact is relevant.


The OP ZUNsoft four-function CODE cohort has now passed focused two-producer
exact replay and entered the accepted OP ledger. Next, tackle its independent
54-byte filename DATA contribution, then revisit substantial MAIN boss gaps.

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

## Latest accepted packet: OP ZUNsoft CODE

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
Both ZUNsoft scopes are accepted. The next task is a substantial MAIN boss gap.

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
| Yumeko sword update, 283 | Current 280; genuine attack prefix remains three bytes short | [Swords](../src/main/boss/yumeko/swords_update.md) |
| Dialog opcode, 456 | Direct 455; compiler-assembly raw 456 has wrong fixup order | [Dialog](../src/main/dialog/opcode.md) |
| EMS boss-face preload, 154 | Raw exact; `[71,24,133,114]` order unresolved | [EMS](../src/main/ems/ems.md) |
| Generic boss defeat/collision, 414 / 43 | Current 408 / 46; complete all-clear tail still merges calls | [Generic boss](../src/main/boss/generic.md) |
| OP score decode, 169 | Ordinary key emits 181. TC4 rejects assembly inside inline/template functions | [Decoder](../src/shared/score/decode.md) |
| ZUN resident entry, 269 | Current 260; `-O-` emits 262 | [Resident](../src/zun/resident/initialize.md) |

Use [the candidate index](reconstruction/UNACCEPTED_COHORTS.md) and per-owner
notes for other gaps. Do not repeat unchanged failed profiles, insert barriers,
copy instruction sequences or promote failed C++ to ASM. Ordinary recovery
needs no new defensive tests, CPU models or per-function extra negatives.

## Local working state

Current accepted replay roots, calibration inputs and the pending ZUNsoft
producer remain available. Superseded builds and diagnostic archives have been
removed; use the findings in per-owner notes instead of archive restore recipes.
The independent Wine prefix, Ghidra project and Factory tool selectors are live.

Default `scripts/ci.py` checks the complete public checkout without private
inputs. Select comparator/build tests for tooling changes and exact replays for
new or affected source; `--full` remains an explicit broad tooling run.
