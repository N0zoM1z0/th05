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

Separately reviewed ASM now contributes **5,824 instruction bytes,
210 symbolic CODE-dispatch table bytes, 24 semantic CODE-coordinate bytes
and 64 semantic DATA bytes**. Its 6,179
complete compared bytes include 57 checked uncredited alignment, inert-branch
and runtime-placeholder bytes. C/C++ counters above are unchanged; unknown
ownership is now 162,327 bytes. The global denominator is still unreviewed,
and the ZUN child inference remains unpromoted.

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
now totals3777 bytes; unknown was168506 at that checkpoint. All authored counts, the observation
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

## Reviewed text-renderer assembly

The complete self-modifying renderer at OP D436..D590 and MAINE E91A..EA74
now passes independent fresh TASM producers from
`src/shared/graphics/text_fx_render.asm`. Each complete346-byte contribution
matches all raw bytes and empty original ordered MZ fixups. Its real local CS
and typed external word OMF fixups remain intact. Both artifacts have their own
16-to15 glyph-loop negative, retained under
`.analysis/textfx-render-native/replay-a/receipt.json`.

A separate explicit native-origin/source review supports genuine handwritten
assembly reconstruction: five CS writes, assembler-level dispatch deltas,
custom helper register contracts and deliberate fall-through. The maintained
source has semantic loops, hardware macros and symbolic labels, with no opcode
arrays, target-byte includes, numeric local CODE addresses or compiler-body
conversion. Pinned masters.lib's640 members contain no candidate identifiers
or native20-byte callback-delta bank. Literal historical source, original
assembler version and exclusion of all historical vendor derivations remain
unknown. See [review and limitations](reconstruction/TEXT_FX_ASM_OWNERSHIP.md).

`config/text_fx_asm_ownership.json` pins native evidence, complete receipts,
source, tools/verifiers, review notes and classification. The explicit decision
`config/reviewed_text_fx_asm_units.json` adopts exactly six scopes:346 CODE,
28 symbolic dispatch DATA and4 state DATA in each of OP and MAINE. Per artifact,
339 CODE bytes and32 DATA bytes receive separate authored ASM credit. The EVEN
byte at relative299 and six dummy1234h fields at222/293/343 compare normally
with zero credit. Actual hardware-delay NOPs at173/261 retain instruction credit.

The unchanged DATA source/receipt remains
`.analysis/textfx-data-native/asm-c/receipt.json`; its original inferred record
is not rewritten. Actual dependency identities and archived DATA producers
were revalidated without recompiling. Adoption also re-read the saved CODE
OMF/MAP/MZ, source aliases, argv/logs, public/operand boundaries, pinned decoded
views and tool proofs. At that checkpoint unknown ownership was167750 after classifying756 bytes;
64 intervening raster bytes remain unknown. No C/C++ source or accepted
C/C++ dependency changed, and no unrelated unit or unchanged tool probe ran.

The first CODE diagnostic measured344 bytes: EQU state bindings produced
immediate loads. Real word EXTDEFs plus symbol-only DATA definitions resolve
the type error. `diagnostic-b` passes the complete346-byte OP extent; neither
diagnostic is an accepted receipt. Earlier C++ state and ASM DATA diagnostics
remain private as documented in the DATA notes. MAIN has no corresponding
reviewed owner. Full program linkage/packing and the98% objective remain open.

## Complete native enemy VM assembly

`src/main/enemy/script.asm` and its complete type include reconstruct the
five-procedure family1538C..15870 in MAIN03/CS1527. The full1252-byte contribution
has1130 authored ASM instruction bytes,118 symbolic CODE-dispatch table bytes,
two checked EVEN bytes and a checked two-byte inert conditional jump. Its only
original ordered MZ fixup is family909 (sound far call14AB:0232). C/C++ counts
and all foreign Motion/vector/angle/RNG/sound providers remain unchanged.

Native and maintained-source review establishes a hidden DS:SI enemy API,
CF clipping return, private ES/register protocol and cross-handler continuations.
This is reviewed original-assembly reconstruction, not compiler-body conversion.
All59 symbolic table entries land on actual interpreter instructions;57 handlers
are distinct. The source preserves an unspecified AL result for invalid opcodes,
entry clear-DF assumption, original timed-frame behavior and a DL-clobber bug
in current-turn opcodes07/08. See [full source/ABI/origin notes](../src/main/enemy/script.md).

`.analysis/enemy-vm-native/replay-a/receipt.json` supplies two fresh deterministic
whole producers and its own minimum-interval16-to17 negative. Import re-read
actual source aliases, argv/logs, OMF/MAP/MZ, public/alias/table bounds, native
review and installed tool proofs. `config/enemy_vm_acceptance.json` records
exactness; `config/reviewed_enemy_vm_unit.json` explicitly adopts exactly this
one complete scope. The original59-entry table remains separate from compiler
switch tables. At that checkpoint unknown fell to166498 after classifying1252 previously unknown
bytes; all source-presence and global-denominator limitations remain explicit.

Initial diagnostics-a/-b stopped before linking on binder CS assumptions;
diagnostic-c matched all1252 raw bytes and ordered[909]. They are not accepted
receipts. The final source adds the independently reviewed DL-clobber note.
No accepted C/C++ dependency changed; no unrelated C/C++ unit or unchanged tool
execution probe was rebuilt. A bounded read-only survey of187 existing accepted
C/C++ owner/receipt contexts found no additional whole DATA matches, recorded
under`.analysis/semantic-data-routing/`; do not rerun it without changed inputs.

## Complete original-assembly bullet generation

The two new complete owners occupy MAIN171EA..173DE(500 bytes) and
1743C..17676(570 bytes), CS1527/DS209D. `spawn_groups.asm` preserves AL speed
tuning, four emission wrappers and the complete velocity/angle dispatcher.
`spawn_raw.asm` preserves allocation, the far emission trampoline and one
coherent232-byte Easy/Hard/Lunatic shared dispatcher. The middle C++ clip94
and following C++ tune66 stay separately accepted with unchanged evidence.

Independent native/source review confirms genuine private register and CS
self-modification protocols, complete Bullet32/Template14/gather-template14
layouts, symbolic tables and preserved stale-AH/signed-stack behavior. No
compiler body, opcode array or target-byte transcription was promoted. The
new credit is994 ASM instruction +68 symbolic CODE-table bytes. Four EVEN
bytes, an inert two-byte JMP and two dummy123 operands compare normally with
zero credit. All1070 complete bytes and empty ordered fixup streams pass.
See [complete source/ABI/origin notes](../src/main/bullet/spawn.md).

`.analysis/bullet-spawn-native/groups-a/receipt.json` and`raw-a/receipt.json`
have two fresh producers each and their own speed-cap128-to127 / gather-points
8-to9 negatives. Actual saved aliases, argv/logs, OMF/MAP/MZ, complete public,
patch/table bounds, native instructions/handlers and tool identities were
revalidated at atomic import. Groups' unchanged objects were reused when the
stricter DS-frame readback guard was added; no duplicate compilation was claimed.
Its historical verifier snapshot remains archived. All unchanged installed
execution probes were reused after identity checks.

The new opt-in generic lane is `scripts/replay_asm_family.py` with descriptors
in`config/asm_families.toml`, exact records in`accepted_asm_families.json` and
explicit per-record/note adoption in`reviewed_asm_families.json`. It supports
`--plan`, one selected `--unit`, and repeated atomic`--accept` arguments.
Manifest changes for an unrelated entry do not stale an unchanged owner;
actual shared assembler/semantic ABI input changes select their affected closure.
Review-note changes need explicit adoption, not unnecessary assembler replay.
Unknown ownership is now165428 after classifying1070 further bytes; the total
observation universe and unreviewed global denominator are unchanged.

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


## Reviewed image kernels

Five complete original-ASM contributions add 787 instruction bytes across 808
compared bytes: MAIN pellet top/bottom 249/252, MAIN/OP CDG alpha 146/148 each,
and OP/MAINE background rectangle 123/130 each. Nine alignment NOP bytes, four
conservatively uncredited jump bytes and eight runtime-patched placeholder bytes
compare normally with zero credit. No sprite/image assets, DATA or tables are
owned. C/C++ counters remain unchanged; unknown ownership is 164,620 bytes.
See [source/native review](reconstruction/IMAGE_KERNEL_ASM_OWNERSHIP.md).

Each owner has two fresh deterministic TASM producers and its own semantic
negative, with complete OMF/MAP/raw and literal empty ordered fixup streams.
Receipts under `.analysis/render-kernels-native/` are `main-pellet-render-b`,
`main-cdg-alpha-a`, `op-cdg-alpha-a`, `op-bgimage-rect-a` and
`maine-bgimage-rect-a`. The first pellet binder setup overflowed before source
assembly; correct real segment divisions fixed it. No failed result was adopted.
All five records and explicit ownership decisions are imported in the generic
ASM ledgers. Existing ASM/C++ owners and successful tool execution probes were
reused after dependency identity checks; no accepted owner was cold-replayed.

Preserve CDG's unconditional CLI/STI, clear DF and sentinel ES=0; rectangle's
self-modified fields and following jump may have a prefetch role, so do not
remove it. Preserve the pellet bottom's first nonadvancing MOV AX,[SI] before
later LODSW. Full 16-byte CDG, 8-byte cached-plane and 4-byte queue union layouts
are retained. MAIN CDG's true entry offset is 02B8, MAINE rectangle 04E4; do not
transfer calibration offsets. No MAINE CDG or MAIN rectangle copy is present.
Private independent vendor/source-origin and pellet native reviews are
`.analysis/image-kernels-origin-review.json` and
`.analysis/pellet-render-native-review.json`; public notes pin their hashes.
Historical original source and all historical vendor derivations remain unknown.


## Complete laser geometry/render/hit assembly

The full MAIN family D5C2..D71E (348 bytes) is explicitly accepted as reviewed
original-ASM reconstruction: private vector 56, point conversion 44, ray 160 and
hit 88. No NOP, padding, table, placeholder or asset bytes occur. Ordered native
MZ fixups are [228,245], real far clip/polygon providers at 0000:139E/18B4.
C/C++ counters remain unchanged; total reviewed ASM is now 4,187 credited bytes
(3,937 instructions, 186 symbolic CODE tables, 64 DATA), 4,234 compared bytes.
Unknown ownership is 164,272 bytes; the global denominator remains unreviewed.

`src/main/bullet/laser_render_hit.asm` uses semantic polar/point macros, complete
Laser 24/coords 10 and stack overlays, with no candidate opcode emits, compiler
body conversion or asset payload. Native BP choreography and private SS helper
contracts support whole-family ASM review; literal historical source and
assembly-heavy mixed-source possibilities remain unproved. No specific inspected
subspan has positive compiler-generated provenance. Independent native/source
reviews are `.analysis/laser-rh-native-review.json` and
`.analysis/laser-rh-maintained-source-review.json`; hashes and limitations are in
[owner notes](../src/main/bullet/laser_render_hit.md).

`.analysis/laser-rh-native/replay-e/receipt.json` has two fresh deterministic
complete TASM producers and its own hit-step 16-to-15 negative, with full raw,
ordered fixups, OMF/MAP/public/real-frame checks. Its record and explicit adoption
are imported in the generic ASM ledgers. Earlier attempts a..d stopped on
binder CS, union width selection, real ENTER/LEAVE frames or TLINK alias
presentation; none was adopted. Current source includes actual compiler EXTDEF
aliases, verified in PUBDEF and their demangled MAP entries. No prior accepted
source dependency changed; tool execution probes and accepted owners were reused.

Keep SS overrides on both line destinations, far SS:DI arguments (clip 12-byte,
polygon 6-byte cleanup), paired ENTER/LEAVE, and the hit helper's reversed DI/SI
save order. No DS=SS shortcut applies. Ray BP moves F,F-4,F-12,F; vector uses
signed 32-bit multiply/shift then word wrapping, and hit boxes remain 12 pixels wide
at 16-pixel intervals. Polygon helpers may change ES.

A read-only Shinki wing check retained the existing blocker without compilation:
original 386-byte wing fixups [76,305] are internally ascending. The retained
full natural enclosure has matching scoped order but raw call operands differ
because the earlier ball updater is four bytes short. Current evidence supplies no supported short standalone context or
prefix change that satisfies both claims; do not add arbitrary padding or
misbind an owned definition to a foreign symbol. Evidence is `.analysis/shinki-wing-native/read-only-order-review.json`
and the prior retained-order note; do not repeat those unchanged probes.


## Complete opaque CDG assembly

Three independently accepted copies of the same semantic original-ASM source
add 300 instruction bytes across 306 compared bytes: MAIN 14C70..14CD6,
OP D590..D5F6 and MAINE EA74..EADA, each 102 bytes. Two NOPs per copy at
relative 75/101 compare normally with zero credit. Original ordered fixups
are empty; RETF 6 is at relative 98. No image assets, slot DATA or tables are
owned. C/C++ counters remain unchanged. Reviewed ASM is now 4,487 credited
bytes (4,237 instructions, 186 symbolic CODE tables, 64 DATA), 4,540 compared;
unknown ownership is 163,966 bytes. The global denominator remains unreviewed.

Maintained source is `src/shared/graphics/cdg_opaque.asm`, reusing unchanged
full CDG16/64-slot types and external declarations from the alpha owner.
Current MAIN/OP/MAINE slot offsets are 306C/3A96/29FE in their actual DS frames
209D/0EFE/1011; native CS frames are 14AB/0D30/0E80. Preserve opaque's signed
SAR 3 (alpha uses SHR), BP width repurpose, stack E/G/R -> copy B/R/G/E,
DF clear, unchanged IF and final ES at E plane plus 5*top. No DS=SS assumption
or alpha sentinel behavior transfers. The internal NOP purpose is unknown;
both NOPs conservatively receive zero credit. See [owner notes](../src/shared/graphics/cdg_opaque.md).

`.analysis/cdg-opaque-native/{main-a,op-a,maine-a}/receipt.json` each has two
fresh deterministic whole producers and its own plane-count 4-to-3 assembled
negative, full raw/ordered-fixup and OMF/MAP/public/real-frame checks. All three
records and their explicit per-note ownership decisions are imported. Every
old accepted input identity remains unchanged; no old owner or installed
execution probe was cold-replayed. Independent native/source reviews are
`.analysis/cdg-noalpha-native-review.json` and
`.analysis/cdg-opaque-maintained-source-review.json`, hashed in the owner notes.
Native segment/string/BP protocols support reviewed original ASM; historical
mixed C/ASM and renamed vendor adaptations remain unproved. No inspected
portion has positive compiler-generated provenance, and synthetic reference
C++ register templates receive no C/C++ credit.


## EGC public rectangle procedures; setup helpers remain unknown

Two complete public owners at OP E2D8..E354 and MAINE F402..F47E add 246
reviewed ASM instruction bytes across 248 compared bytes. Each has RETF 8 at
relative 120, NOP 123 (checked, zero credit) and ordered MZ fixup [116] for
far EGC_OFF 0000:082C/083A. Actual CS frames are 0D30/0E80; the complete
foreign width word is DS 0EFE:3F1E / 1011:2E86. No DATA or asset bytes are
owned. Reviewed ASM totals 4,733 credited bytes (4,483 instructions, 186 CODE
tables, 64 DATA), 4,788 compared with 55 uncredited; unknown is 163,718 bytes.
C/C++ counters and the unreviewed global denominator remain unchanged.

Native/source review independently supports public ASM via BP stride repurpose,
private register roles and explicit page switching. The two 64-byte helpers at
E354..E394 and F47E..F4BE stay entirely unknown. A bounded 653-member vendor
search found positive resemblance between their last 34-byte setup and upstream
EGC_START, with changed zeroing and omitted calls; this supports neither blanket
original credit nor blanket vendor exclusion. Do not count or imitate them to
avoid their ownership question. The MAINE helper is distinct from the parked
cutscene helper A6D1. See [complete owner review](../src/shared/hardware/egc_rect_copy.md).

`.analysis/egc-rect-native/{op-a,maine-a}/receipt.json` each has two fresh
independent complete TASM producers and its own 400-to-399 clipping-bound negative.
Full raw/ordered fixups, OMF/MAP/public/real-frame checks pass; both records and
explicit adoption decisions are imported. Actual compiler aliases and near
helper addresses are bound without changing SHARED's no-group context. No old
source/dependency changed or required replay; tool execution proofs are reused.
Native/source reports are `.analysis/egc-rect-native-review.json` and
`.analysis/egc-rect-maintained-source-review.json`, hashed in the owner notes.

Keep left SAR4 versus width SHR4, DEC BX/JNS height (height 0 copies one row),
word wrapping and per-word signed/range clipping. If all words are clipped,
there is no page-port write; do not force page 0. GAME5 preserves DF/IF and
returns ES=A800. Helper bodies and their terminal NOPs receive no credit or
ownership exclusion in this change. Literal historical mixed-source possibilities
remain unproved; no inspected public portion has positive compiler-generated
provenance.


## Complete PI assembly kernels

Four complete contributions add 560 reviewed ASM instruction bytes across 562
compared bytes: OP masked DD10..DD97 (135), plain/palette/free DE80..DF12 (146),
and MAINE masked EEB8..EF3F / plain/palette/free F028..F0BA at the same sizes.
The second family has complete procedures at relative 0/58/96 and its only NOP
at 145, checked with zero credit. Masked has no NOP/padding. Ordered fixups are
[54,106] and [17,89,140], respectively, independently in both artifacts.
C/C++ stays 96,899 bytes / 306 units / 494 functions. Reviewed ASM now totals
5,293 credit (5,043 instructions, 186 CODE tables, 64 DATA), 5,350 compared with
57 uncredited; unknown is 163,156 bytes and the global denominator is unreviewed.

Maintained sources are `src/shared/graphics/pi_masked_rows.asm` and
`pi_rows_palette_free.asm`, plus full `pi_types.inc`: PiHeader 72, Palette 48,
eight complete headers 576 and eight far buffers 32. Mask words/images are
external, with no asset, DATA or provider-body credit. Native private BP=SP
frameless rowloops and BX stack frames independently support original ASM;
source algorithms come from pinned explicit ReC98 ASM, not opcode arrays or
compiler-body conversion. Positive vendor type/provider facts remain separate
from ownership of the game kernels. See [owner notes](../src/shared/graphics/pi_kernels.md).

`.analysis/pi-kernels-native/{op-masked-a,op-plain-a,maine-masked-a,maine-plain-a}/receipt.json`
each has two fresh deterministic complete TASM producers, full raw/ordered
fixup/OMF/MAP/public/frame checks and its own assembled negative: scratch row
400-to-399 or palette copy 16-to-15 with the full 16-color type unchanged. All four
records and explicit per-note decisions are imported. No prior accepted source
input changed, and old producers/tool execution probes were reused. Native and
current-source reports are `.analysis/pi-kernels-native-review.json` and
`.analysis/pi-kernels-maintained-source-review.json`, hashed in owner notes.

Preserve hidden ES:SI buffer/DI height and AX mask ID, BP clobber and RETN 8,
BX=SP followed by SS:[BX+4] far-argument access with RETF 2, exact `Palettes` (no underscore)
and actual C++ aliases. Palette copy requires DF-clear entry before its provider
CLD. Do not insert CLD or claim unconditional DF clearing on early-clipped pack
paths. Keep scratch row 400, top/offset word wrapping, real far pointers and
buffer-clear-before-free. Near mask helpers DD97/EF3F remain foreign and receive
no source or ownership claim. Historical mixed-source possibilities remain
unproved; no inspected kernel portion has positive compiler-generated provenance.


## Piano drawing and semantic CODE geometry

Three complete OP owners add 277 reviewed ASM bytes: FM 48 at D9E2..DA12,
keys/pressed/tables 209 at DA30..DB01 and label 20 at DB0D..DB21. They contain
229 instructions, 24 symbolic near-dispatch bytes and 24 semantic CODE-coordinate
bytes, with no NOPs/padding/fixups. C/C++ remains 96,899 bytes. Reviewed ASM now
has 5,272 instruction + 210 dispatch + 24 semantic CODE-table + 64 DATA bytes,
5,570 credited / 5,627 compared with 57 uncredited. Unknown ownership is 162,879;
global denominator remains unreviewed.

The current-note helper 30, sprite 12 and direct-color helper 26 (68 bytes total)
remain entirely unknown; DB3B..DB3C is an outside non-NOP gap and also unknown.
Native current-note protocol may admit natural C++; do not convert it or the
334-byte C++ piano setup/render context to ASM. Direct color has a 20-byte core
matching upstream GC_SETCO/native vendor code but a changed wrapper: neither
blanket original credit nor vendor exclusion is justified. External black-key
and font assets are addresses only. See [source/origin/contracts](../src/op/piano/piano.md).

`.analysis/piano-native/{fm-a,keys-a,label-b}/receipt.json` each has two fresh
complete TASM producers and its own color 5-to-6, black-height 9-to-10 or label-row
8-to-7 negative. Raw/ordered-fixup/OMF/MAP/real-frame checks pass; records and
explicit per-note adoption are imported. Label-a stopped at the first MAP gate:
WORD alignment moved native odd DB0D to DB0E. Only the new standalone label
contribution changed to BYTE, preserving the binder's real PARA SHARED frame.
No failed producer, padding mask or target patch was adopted.

The generic verifier adds only the narrowly modeled semantic CODE table role
piano-key-horizontal-positions: 12 word positions computed from left 384 / key width 4,
white degrees and half-key sharps. It rejects arbitrary/raw/pixel banks, invalid
roles/widths, overflow, overlap and changed native values; table 90h bytes never
become instruction NOPs. Counts distinguish semantic geometry from dispatch and
DATA. Old source inputs/counts/objects are unchanged and reused; archived old
verifier snapshots are preserved. Public tests include modeled/native negative
cases without recompiling old units. Private independent reviews are
`.analysis/piano-native-review.json` and
`.analysis/piano-maintained-source-model-review.json`, hashed in the owner notes.


## Complete original-ASM sound loaders

Three complete 184-byte loaders add 552 reviewed ASM instruction bytes: MAIN
14EA4..14F5C, OP DBBE..DC76, MAINE ED66..EE1E. Each has 71 instructions,
no NOP/padding/tables/DATA and ordered far-call fixups [70,78,87]. RETF 6 is
at relative 181. C/C++ remains 96,899 bytes. Reviewed ASM now totals 6,122
credited bytes (5,824 instructions, 210 dispatch, 24 semantic CODE tables, 64 DATA),
6,179 compared with 57 uncredited. Unknown ownership is 162,327; global denominator
remains unreviewed.

`src/shared/sound/load.asm` retains the real far Pascal filename16:16/function16
API, BP function reuse, DS/ES switches, DOS error routing and same-CS PUSHCS +
near-call entry to the real FAR SND_KAJA_INTERRUPT provider. It preserves actual
byte modes and the packed 15-byte extension bank with a MIDI dword overlapping
adjacent SE mode at+15. No false 4x4 padded DATA is introduced. The complete 13-byte
filename copy, unbounded scan, dot/extension writes before disabled returns,
infinite missing-file fallback and unchecked 65535-byte driver read remain.
Entry DF clear is required; no IF/ES restoration guarantee is invented.

Source/native origin is independently corroborated by reference history
01c92da1's explicit ZUN-written ASM attribution and actual manual register/segment
protocols. Vendor Beep/file bodies remain external; no substantial copied loader
body was found in the bounded 653-member review. No inspected subspan has positive
compiler-generated provenance. Literal historical source/assembler identity and
mixed-source possibilities remain unproved. See [owner review](../src/shared/sound/load.md).

`.analysis/sound-load-native/{main-a,op-a,maine-a}/receipt.json` each has two fresh
deterministic complete TASM producers, full raw/ordered-fixup/OMF/MAP/public/frame
checks and its own read-limit FFFF-to-FFFE negative. All three records and explicit
per-note adoptions are imported. No old accepted input or tool surface changed;
old objects and installed execution probes were reused. Private independent
reports `.analysis/sound-loader-native-review.json` and
`.analysis/sound-loader-maintained-source-review.json` are hashed in owner notes.
Filename/extension DATA, mode state, driver buffers, library implementations,
neighboring accepted Kaja functions and whole-program packing receive no new
ownership or credit from these CODE units.
