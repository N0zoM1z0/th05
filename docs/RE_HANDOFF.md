# TH05 agent handoff

Project objective: at least 98% authored bytes exact. The global denominator
and percentage are still unreviewed; this objective has not been reached.
Repository: https://github.com/N0zoM1z0/th05 .
Commit messages: `gpt-6.1-sol: ...`. Keep maintained code and docs in English.

Current acceptance: **306 bounded C/C++ CODE/DATA units / 494 complete function occurrences**,
**96,899 authored bytes exact**: 81,630 CODE and 15,269 initialized DATA.
CODE is 80,938 instruction plus 692 semantic compiler-table bytes.
Complete compared extents total 96,978; 79 checked padding bytes receive
no credit. MAIN has 378 functions / 60,832 CODE / 3,091 DATA;
OP 61 / 11,218 / 8,649; MAINE 55 / 9,580 / 3,529.
Global denominator and percentage remain unreviewed.

## Retained evidence

Public acceptance lives in `config/accepted_units{,.op,.maine}.json`;
`docs/PROGRESS.md`, `resources/progress.svg` and `resources/ownership.json`
are generated from it. Per-owner source notes explain boundaries and ABIs.
The private receipt inventory is
`.analysis/cleanup-current-receipt-guards.json`: all 209 receipt hashes
for the preceding 298 records were found. The two newer verdict receipts and
MAIN transition and three sound DATA receipts below are also required; preserve
their whole directories. The newer HUD decimal and two bomb-family receipts below are also required.
See [local storage](LOCAL_STORAGE.md) before deleting any private artifacts.

Cleanup revalidated208 whole receipts using the existing private validator.
The remaining historical `main-stage-data-a` receipt contains an unselected
CODE descriptor whose padding classification later changed to offsets1153/1173;
the generic whole-receipt validator rejects that metadata drift. Its current
accepted DATA was separately rechecked against both actual MZ/MAP/OMF/source
producers and its own compiled negative, with no mismatch. No evidence or
metadata was rewritten to bypass the gate. Details are in
`.analysis/cleanup-handoff/stage-data-selected-native-review.json`.

The longer investigation log is archived in
[historical handoff](history/RE_HANDOFF_2026-10-25.md). Its numerical checkpoints
and pending statuses are historical, not the current acceptance state.

## Start here

Read `AGENTS.md`, [workflow](RE_WORKFLOW.md) and [oracle contract](ORACLES.md).
This workspace already has the pinned targets, toolchain, decoded views and
ReC98 checkout; no bootstrap, download or decoder rerun is necessary.

```sh
git status --short
python3 scripts/preflight.py
python3 scripts/replay_units.py --artifact main --plan
python3 scripts/replay_units.py --artifact op --plan
python3 scripts/replay_units.py --artifact maine --plan
python3 scripts/ci.py
```

All three replay plans are empty at this handoff. Follow the user's explicit
incremental preference: replay only new or demonstrated affected units. Reuse
unchanged accepted evidence and successful installed-tool probes. Serialize
Wine/Borland and Ghidra with `bash scripts/run_heavy.sh ...` (one CPU,35% quota,
768 MiB memory, no swap, low priority). Do not alter TH03/TH04 sibling repos,
shared processes, tool versions or compiler flags.

## Latest accepted additions

After `caa32aa` (96,003 bytes), two focused groups added247 bytes:

| Receipt under `.analysis/unit-replays/` | Complete ownership | Credit |
| --- | --- | ---: |
| `main-mai-yuki-hittest-a` | Two MAIN collision/state wrappers at177F0..1785F | 111 CODE |
| `maine-staff-filenames-data-a` | Fourteen MAINE filename objects at11862..118EA | 136 DATA |

Each has two independent fresh producers, full raw/OMF/MAP and literal ordered
relocation comparison, plus a meaningful compiled negative. Both are imported;
source, docs, configs and generated progress are included in the handoff commit.
The first group's real near-call offset wraps inside CS1527: its provider is
load1FAD0, not the naive linear-disassembler resultFAD0. Full Boss24/Point4,
AX damage return and byte damage storage are retained.

`caa32aa` added shot/hit-sprite invalidation94, ending dispatch92 (94 compared,
two excluded relaxation NOPs), MAINE line animation190 and all-cast DATA2989.
All-cast text uses47 distinct mutable byte arrays with const-pointee consumers;
the first const-array hypothesis pooled nine objects and failed at2263 versus
2787 bytes. The corrected text and affected202-byte pointer-table header
closure passed independently. Historical original declarations are unknown.
Line animation retains its full enum; direct decrement is supported by pinned
TC4.02 with its normal unsuppressed warning. See the per-owner notes.

## Latest verdict DATA acceptance

Two additional owners add 276 semantic DATA bytes, without changing accepted
CODE or shared dependencies:

| Receipt under `.analysis/unit-replays/` | Complete ownership | Credit |
| --- | --- | ---: |
| `maine-verdict-metric-ui-data-a` | 13 metric/heading objects at11730..117CC | 156 DATA |
| `maine-verdict-score-ui-data-a` | 12 score/resource/stage objects at117D2..1184A | 120 DATA |

Both have two fresh independent producers and their own compiled DATA mutation,
with complete raw/OMF/MAP, CP932 staging and ordered relocation validation.
The unchanged tool execution proof was reused. See
[verdict UI notes](../src/maine/verdict/ui_data.md). The remaining18 punctuation/
counter bytes stay unknown. The earlier294-byte monolith was never compiled.

## Shared sound arbitration DATA

Three independent DATA owners add102 bytes: two complete17-byte SE priority/
lifetime tables in each artifact. They share one maintained semantic source
without editing any accepted dependency. Receipts under`.analysis/unit-replays/`:
`main-se-priority-data-a`, `op-se-priority-data-b`, `maine-se-priority-data-a`.
Each has two fresh deterministic producers, full MAP/OMF/raw and empty ordered
relocation checks, and its own compiled48-to47 lifetime mutation. Tool execution
proofs were reused. The first OP attempt failed the MZ minimum-allocation check;
its corrected binder reserves only the independently accepted foreign Music
Room DATA end, supplying no values or artificial stack. See
[sound DATA notes](../src/shared/sound/se_priority_data.md).
Sound controller CODE remains entirely unaccepted; no register-template or
codestring probe was repeated. The source does not own adjacent state or gaps.

## Native leads

The MAIN dialog-to-boss callbacks are now accepted from
`.analysis/unit-replays/main-dialog-boss-transition-c/receipt.json`: two complete
functions at139F5..13A3E, 73 compared bytes / 72 authored CODE bytes. The original
far cdecl animation call shares AE1 context and retains its relaxation NOP at13A0D
(checked, zero credit). Real near cdecl STD and near/far Pascal boss callbacks
are preserved. See [owner notes](../src/main/dialog/boss_transition.md).
Earlier setup attempts `-a` and `-b` failed assembly/compilation before linking;
no size/raw mismatch or failed producer was accepted. Existing accepted headers
and consumers were not changed or replayed.

The decimal-table lead is now independently accepted: two complete adjacent
DWORD/word factor arrays at21DD6..21DFC,38 DATA bytes. Actual HUD, point-popup
and score-delta consumers establish widths, strides and decimal roles.
`.analysis/unit-replays/main-hud-decimal-tables-data-a/receipt.json` has two fresh
producers, full DATA/OMF/MAP/raw/empty ordered-fixup checks and its own compiled
million-place divisor mutation. See[owner notes](../src/main/hud/decimal_tables.md).
The previous stopped-lead file remains historical routing evidence only.

## Mima bomb control and canonical body refresh

The new genuine bomb family atFA50..1027B compiles13 complete procedures in one
2091-byte contribution. Both actual fresh producers match all raw context bytes
and all38 ordered original fixups. Actual OMF CODE records are0..1023,
1023..2041 and2041..2091; Mima control's real fixups1957/1985 and2065 straddle
the second cut and naturally restore its original local order[55,27,135].
`main-bomb-family-mima-b` accepts only its complete161-byte control function;
no context bytes are double-credited. Its own final-tone100-to101 mutation fails.

Nine CPPs reversibly factor their literal bodies into`player/bomb_body/`, while
all existing headers stay unchanged. Exactly eight accepted MAIN owners needed
source-current evidence: `main-bomb-body-canonical-refresh-b` has two fresh
producers per owner and one shared Reimu-star112-to111 negative. Both receipts
were imported atomically; unrelated MAIN, OP and MAINE evidence was reused.
The first family producer kept the Reimu circle call far; measured OMF context
and the real AE1/RETF4 provider justify explicit samecodeseg in the new header.
The first refresh failed its moved negative anchor and produced no receipt.
All attempts are preserved. See[bomb family notes](../src/main/player/bomb_family.md)
and`.analysis/bomb-family-source-factor/native-full-review.json`.

## Reviewed CL.LIB DATA ownership

No authored counter changes in this review. `review_vendor_data.py` verifies
24 complete ordinary relocation-free CL.LIB DATA contributions:8 members/619
bytes independently in each of MAIN, OP and MAINE,1857 bytes total. Complete
library/member hashes, MAP/MZ contributions, LEDATA coverage, unique native
whole-byte matches and empty original fixup streams pass. Public evidence is
`config/vendor_data_ownership.json`, source pins are`config/cl_data_sources.json`,
and the explicit adoption decision is`config/reviewed_vendor_data_units.json`.
Only those unknown spans move to verified-vendor-initialized-data. Vendor DATA
now totals3777 bytes; unknown remains168506. All authored counts, the observation
universe and the unreviewed global denominator remain unchanged. See
[CL DATA review](reconstruction/CL_DATA_OWNERSHIP.md). No compiler, Wine, Ghidra,
decoder or game was run, and no accepted C/C++ source owner needed replay.

Current-state audit also confirmed Music Room502/837 and hiscore menu312 are
already accepted; old historical failures are not new work. A cutscene audit
found no supported new context: old full2848 producers already restore all42
script relocations but script1556 remains raw-inexact; the current split gives
raw-exact1555 and different ordering. Do not repeat either unchanged build.
Native/private observations remain in`.analysis/vendor-data-routing/` and the
existing cutscene producer directories.

## Separate text-renderer ASM DATA evidence

`src/shared/graphics/text_fx_data.asm` reconstructs two symbolic DATA scopes in
each of OP and MAINE: 28 dispatch bytes and 4 mutable state bytes. The separate
`config/text_fx_data_acceptance.json` records 64 exact ASM DATA bytes, with
inferred handwritten origin and zero C/C++ or global authored credit. They
remain unknown in the ownership partition; all headline counts above stay
unchanged. 32 raster bytes per artifact and all renderer CODE are excluded.

`.analysis/textfx-data-native/asm-c/receipt.json` has two fresh producers per
artifact and an own assembled negative for each scope. Import re-read actual
saved OMF/MAP/MZ, source aliases, argv/logs, DGROUP frames, pinned decoded views
and the full private native review. Unchanged tool execution probes were reused.
See [owner notes](../src/shared/graphics/text_fx_data.md) for original boundary,
symbol, provenance and NOP review. `asm-a` stopped on the actual TASM MAP module
name; `asm-b` is a successful intermediate diagnostic. Neither is accepted.

Earlier byte-exact C++ state producers were not imported: the assembly context
does not justify increasing C/C++ origin counters. Their source/producer
snapshots remain private. No accepted C/C++ dependency changed; no unrelated
unit was rebuilt. Public CI and generated progress check this separate lane.
The next lead is the real self-modifying renderer, not a compiler-generated
function to transcribe; review any original-assembly claim separately. MAIN
has no corresponding reviewed owner. The 98% objective remains open.

## Parked work: preserve findings before trying variants

- Staff: [full-family notes](../src/maine/staff/full.md) describe17 real bodies,
  15 accepted functions/2742 instruction bytes. Updater626 and renderer861
  each compile three bytes shorter due to redundant-pointer reload lowering.
  No ABI/type defect or permission for a volatile/register/barrier workaround
  was found. `controller.cpp` reproduces991 raw bytes in one diagnostic but
  fails the original29-entry relocation order. `bitmap.cpp` is a valid
  source-present211-byte transfer model versus original126, not a prefix to
  force controller fixup order. Actual sources and failures remain frozen.
- B4-ball update: [notes](../src/main/boss/mai_yuki/b4ball_update.md) explain
  296 versus273. Full Point AX/DX/RET2 ABI is correct; the extra23 bytes are
  real spills/comparisons/branches. Only the new binder's BulletTemplate base
  was corrected5780 to577E, without recompiling. It remains outside the default
  manifest. Never retag the real aggregate return as int/void or force registers.
- MAINE cutscene script: natural full context retains1555-byte function/table
  boundaries; a split has exact raw bytes but wrong literal relocation order.
  The adjacent EGC helper has a one-byte MOV-zero/XOR-zero lowering difference.
  No independent FLAGS contract justifies hand-generating the missing byte.
- Other previously diagnosed gaps include one-byte switch/table zeros in
  stage/session, item collect and several Boss callbacks; scroll115 versus123; bullet rendering334
  versus330; item/shot render ABI kernels; OP piano/input/PI-load cases. Search
  the historical handoff and owner notes before repeating these probes.

Compiler-generated code must remain semantic C/C++; no opcode transcription,
raw target array, synthetic prefix, filler NOP, fixup sorting, forced volatile
reload or unsupported register/type/FLAGS trick receives authored credit.
Classify real original assembly separately and keep padding at zero credit.

## Target and reference context

The supplied Japanese copy is `candidate-local-attested`, not independently
proved pristine. MAIN uses its actual direct MZ load-module view; OP/MAINE use
cached `DecodedUnitImage` views and literal observed relocation streams via
`UnitContext/load_unit_target`. Do not wrap decoded payloads in fake MZ files.
Pinned identities are in `config/targets.toml` and private decoder receipts.

Main frames: MAIN01 AE10/CSAE1, SHARED14AB0/CS14AB, MAIN03 15270/CS1527,
DATA209D0/DS209D. MAINE frames: CODEA540/CSA54, SHAREDframeE800,
DATA10110/DS1011. Compiler/linker/assembler are pinned TC4.02/TLINK6.10/TASM5;
MSDOSplayer P0281 is supplied by pinned ReC98.
`_reference/ReC98` remains at `b6ba5b0a529edbb31efdf8c0e939263804f8ee47`.
ReC98 and TH03/TH04 are semantic references, never transferred acceptance.

## Finishing a bounded change

Import passing receipts with `scripts/progress.py --artifact ... --accept ...`
(`--accept` may repeat atomically within one artifact), then regenerate progress
and ownership, update owner notes, run public CI and `git diff --check`, commit
and push. Stop after the first actual size/boundary failure; do not run two more
producers for a known mismatch. A single diagnostic is not acceptance.
No compiled-source or dependency edit is harmless to source-hash freshness:
refresh only its actual affected closure before accepting new metadata.
