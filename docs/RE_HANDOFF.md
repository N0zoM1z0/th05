# TH05 handoff — 2026-11-10

> Current workflow: follow the **Highest priority** section in `AGENTS.md`.
> Prefer affected exact comparisons and useful Markdown knowledge. Ordinary
> notes do not require full CI, native replay or document-hash/pin refreshes.
> Older broad validation instructions apply only when their impact is relevant.


The next source packet is OP ZUNsoft, described below. The last reconstruction
checkpoint is `84a5de9`; acceptance is unchanged.

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

## Best next source packet: OP ZUNsoft

[Source and ABI notes](../src/op/zunsoft/zunsoft.md) describe four new C++
functions at decoded OP `B616..BA94`: 1150 bytes = 1102 instructions + 48
compiler switch-table bytes, no padding. Maintained TH04 bodies are adapted to
TH05's actual input ordering and provider frames. The complete 14-byte pyro,
256-slot pool and 48-byte palette types are retained; runtime state is foreign.

The first actual diagnostic matches **all 1150 raw bytes and all 33 original
ordered fixups**:

- Proposal: `.analysis/op-zunsoft-unit-proposal.json`.
- Actual frozen producer: `.analysis/native-producers/op-zunsoft-a/`.
- Comparison: its `native-diagnostic.json`, SHA-256
  `e6b0709a0805b577d40aa3e2b3e19eb11d9aa14a67050a8316dcc93cb2acb163`.
- Native/source/ABI review: `.analysis/op-zunsoft-native-review.json`, SHA-256
  `9f5f028a3a56700d90886b98a4a95a6adde2507e9c6936b499e46901e2703d84`.

**Not accepted:** only one producer, no compiled negative, no live manifest or
ledger entry. No progress is credited. When reconstruction resumes, review the
packet, register it, then run the normal focused two-producer/shared-control
replay. The proposed control changes spawn-speed bias 64 to 65. Preserve the
current CODE source/binder identities unless a real correction is required.

The earlier `super_free` convention concern is resolved: pinned
`libs/master.lib/func.hpp` expands `MASTER_RET` to **far pascal** in large model;
`MASTER_CRET` is the distinct cdecl form. The current source declaration agrees.
Descriptive scalar coordinate parameters preserve four real Pascal words and
RET8; original source grouping/spelling is not proved.

A separate `filenames.cpp` and `op_zunsoft_filenames_bindings.asm` prepare the
six genuine source strings at OP `FECA..FF00` (DS `0EEA..0F20`), 54 bytes.
`.analysis/op-zunsoft-filenames-proposal.json` records this **unbuilt** DATA
candidate. It has no producer or credit and needs its own complete DATA scope
and compiled DATA mutation. The image/font contents are not source-owned here.

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
