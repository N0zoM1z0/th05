# TH05 current handoff

Goal: at least 98% authored bytes exact. Commit prefix: `gpt-6.1-sol:`.
Repository: https://github.com/N0zoM1z0/th05 .

Current acceptance: **233 bounded C++ CODE/DATA units / 434 complete function occurrences**,
**79,142 authored bytes exact**: 70,053 CODE and 9,089 initialized DATA.
CODE is 69,403 instruction plus 650 semantic compiler-table bytes.
Complete compared extents total 79,208; 66 checked padding bytes receive
no credit. MAIN has 352 functions / 57,488 CODE / 431 DATA;
OP 56 / 9,471 / 8,615; MAINE 26 / 3,094 / 43.
Global denominator and percentage remain unreviewed.

## Retained evidence

All paths below are under private `.analysis/unit-replays/`.

| Scope | Receipt directory |
| --- | --- |
| Player angle, bullet tuning, Boss movement, resident CFG | `boss-cfg-a` |
| Boss explosion | `boss-explosion-a` |
| HUD overlay | `hud-overlay-a` |
| Four character shot owners | `reimu-shots-a`, `marisa-shots-a`, `yuuka-shots-a`, `mima-shots-b` |
| Bullet generation clipping | `bullet-clip-d` |
| Stage initialization | `stage-setup-a` |
| 17 complete Boss background functions | `boss-background-functions-a` (explicit subset) |
| Cheeto allocation/homing | `cheeto-update-b` |
| Regular/special bullet update | `bullet-update-d` |
| Enemy rendering from maintained TH04 C++ | `enemies-render-b` |
| Sound interrupt in MAIN / OP / MAINE | `main-kaja-a`, `op-kaja-a`, `maine-kaja-a` |
| OP startup and main menu | `op-main-menu-b` |
| OP setup and character selection | `op-setup-menu-a`, `op-character-menu-a` |
| Seven OP high-score viewer functions | `op-hiscore-scopes-a` (retained producer review) |
| OP configuration and music prefix | `op-config-b`, `op-music-prefix-b` |
| Eight OP music suffix functions | `op-music-functions-a` |
| Nine MAINE cutscene functions | `maine-cutscene-a` |
| Shared polar/vector in all three games | `main-vector-a`, `op-vector-b`, `maine-vector-a` |
| OP title animation | `op-title-b` |
| MAINE all-cast, staff clip and entry | `maine-allcast-a`, `maine-staff-clip-a`, `maine-entry-a` |
| MAIN growing/shrinking circle effects | `main-circles-b` |
| EX-Alice firewaves and Mai/Yuki flight | `main-firewaves-b`, `main-mai-yuki-flight-b` |
| Playfield shake and gather | `main-playfield-shake-a`, `main-gather-b` |
| MAINE high-score lifecycle | `maine-score-end-b` |
| Sara complete stage-one behavior | `main-sara-a` |
| Stage-two and three movement/pattern helpers | `main-midboss-stage2-patterns-a`, `main-midboss-stage3-patterns-a` |
| Stage-four transition movement | `main-midboss-transition4-a` |
| Louise movement and Yumeko opening patterns | `main-louise-flystep-a`, `main-yumeko-patterns-b` |
| Alice final spread and five complete puppet callbacks | `main-alice-final-spread-a`, `main-alice-puppet-scopes-a` |
| Louise complete phase callback | `main-louise-update-a` |
| Louise later and Alice charge patterns | `main-louise-later-patterns-d`, `main-alice-charge-patterns-a` |
| Louise charge/initial patterns and Alice puppet beam | `main-louise-initial-patterns-a`, `main-alice-puppet-beam-a` |
| Stage-five and Extra movement/pattern helpers | `main-midboss5-extra-patterns-a` |
| Stage-one, two, three, five and Extra midboss logic | `main-midboss-stage1-a`, `main-midboss-stage2-c`, `main-midboss-stage3-a`, `main-midboss5-extra-b` |
| Midboss state and two reward functions | `main-midboss-state-d`, `main-midboss-bonuses-b` |
| Six complete generic Boss functions | `main-boss-generic-b` |
| Ten strict Shinki functions | `main-shinki-functions-c` (passing subset), `main-shinki-scopes-d` (retained review) |
| Eight small MAIN owners | `main-slowdown-a`, `main-hud-hp-a`, `main-player-position-a`, `main-bullet-pattern-a`, `main-scroll-convert-a`, `main-tile-render-a`, `main-midboss-invalidate-b`, `main-boss-backdrop-c` |
| OP initialized UI/state DATA | `op-setup-data-a`, `op-main-data-a` |
| OP music/title/character/score/config DATA | `op-music-data-retained-a`, `op-title-data-retained-a`, `op-character-menu-data-retained-a`, `op-hiscore-view-data-retained-a`, `op-config-data-retained-a` |
| MAIN stage initialized DATA and refreshed CODE evidence | `main-stage-data-a` |
| MAINE entry and MAIN Boss drop-table DATA | `maine-entry-data-retained-a`, `main-boss-generic-data-a` |
| Dialog-file loading and demo loading | `main-dialog-file-a`, `main-demo-b` (passing load subset) |
| MAIN/OP/MAINE core initialization | `main-core-init-a`, `op-core-init-a`, `maine-core-init-a` |
| OP/MAINE BGM measure query | `op-bgm-measure-a`, `maine-bgm-measure-a` |
| Sound mode selection in all three artifacts | `main-sound-modes-b`, `op-sound-modes-b`, `maine-sound-modes-a` |
| Generic shot control | `main-player-shot-common-a` |
| Three EMS cache functions | `main-ems-scopes-c` from raw-exact/ordered-inexact `main-ems-cache-b` |
| Item extend and miss penalty | `main-item-extends-a`, `main-item-miss-penalty-d` |
| Dialog wipe/fade box helpers, runner and face/sprite tail | `main-dialog-box-b`, `main-dialog-run-d`, `main-dialog-tail-scopes-c` |
| Item creation/death drops, splashes and tile invalidation | `main-item-spawn-b`, `main-item-splashes-a`, `main-items-invalidate-a` |
| Reimu bomb stars and stage-five midboss rendering | `main-reimu-bomb-stars-a`, `main-midboss5-render-a` |
| Enemy tile invalidation and allocation | `main-enemies-invalidate-c`, `main-enemy-allocation-a` |
| Laser creation/control, state update and rendering | `main-laser-control-a`, `main-laser-update-b`, `main-laser-render-a` |

Each accepted scope has two independent deterministic producers, full raw and
ordered-fixup comparisons, pinned tools, actual OMF dependencies and a compiled
semantic mutation control. Import rechecks saved MZ/MAP/OMF, wrappers and actual
compiler inputs. Symbol-only context is uncredited; whole-game linkage remains
open. Per-owner notes hold complete boundaries, ABI and bindings.

Three independent acceptance ledgers are `config/accepted_units.json`,
`accepted_units.op.json` and `accepted_units.maine.json`. OP/MAINE use pinned
retained decoded views, not fabricated MZ headers. Their proof includes packed
identity, original relocation order and two decoder load observations. Public
summaries need no private game/cache files. No packed-file equality is claimed.

Standalone ZUN `-M` is separately accepted: 311 complete COM bytes (142 code,
169 data), from semantic ASM with inferred original style. Evidence:
`.analysis/zun-memory/first-b` and `config/zun_memory_acceptance.json`. It does
not contribute C++ credit or establish complete outer ZUN equality.

## Ownership inventory

`resources/ownership.json` covers all 319,268 observed payload/COM bytes.
Every unclassified interval remains unknown. Reviewed third-party ownership
covers31 complete CL.LIB CODE contributions/2,901 bytes and20 complete Master
procedures/376 bytes, totaling3,277. CL uses pinned native OMF/FIXUPP evidence
and explicit member decisions in `config/reviewed_vendor_units.json`. Master
uses independently pinned original source, actual macro context, complete
OMF/MAP/MZ and ordered-fixup equality, with the separate explicit decision in
`config/reviewed_master_procedures.json`. Its376 bytes include9 library-owned
padding bytes and grant no authored credit. Two CL members with unwritten CODE,
all other Master procedures and every surrounding gap remain unknown.
Both reviewers have `--structural-check` for public metadata and `--check` for
actual retained private evidence, with zero compilation. Regenerate inventory
using `scripts/ownership.py --write`; add `--verify-targets` to replay native
vendor/target evidence without decoding or compiling. The global denominator
and percentage remain unreviewed.

## Incremental work

User steering: accelerate and replay only new or affected units. Use
`replay_units.py --plan` and `--units ID...`; add `--artifact op` or `maine` for
those contexts. No-work exits before tools/targets. Tool execution probes are
reused after manifest and actual installed tool/header/library identity checks.
Do not cold-replay old units, redo calibration or re-decode unchanged targets.

Multiple complete-function scopes in one TU compile once per fresh round.
Their MAP boundaries include unaccepted neighbors. `progress.py --accept
RECEIPT --units ID...` imports an explicitly passing subset without recompiling;
all saved results and the negative-control owner still undergo validation.
The original mixed receipt and aggregate verdict are unchanged.

Initialized semantic DATA opts into `extent_kind="initialized-data"`, zero
functions, explicit source roles and one complete real MAP DATA contribution.
The actual OMF DATA SEGDEF must have complete nonoverlapping LEDATA coverage;
BSS, assets, CODE tables and unproved transformations are rejected. Each DATA
unit requires its own compiled DATA mutation; a CODE-only change cannot prove
it. Focus one DATA unit per replay; positives sharing a TU still compile once.
Current accepted DATA: OP setup 1,075 bytes, main menu 1,089, music 6,217,
title 154, character selection 8, score viewer 53 and configuration 19; MAIN
stage setup 189 and Boss drop types 10; MAINE entry filenames/pointer 43.
Total DATA 8,857 is reported separately from CODE. Five new
OP DATA owners reuse their two archived, revalidated actual CODE producers and
compile only one fresh DATA negative each. MAIN stage uses a fresh combined
CODE/DATA replay because its older CODE evidence lacked saved actual argv.
No original BSS is credited. `scripts/review_saved_data.py` preserves the full
original parent, including any failed CODE results, and validates every saved
MZ/MAP/OMF and the complete canonical/encoded dependency closure.

New Japanese owners opt into `source_encoding = "cp932"`. Canonical maintained
inputs and snapshots stay UTF8; real compiler bytes have separate identities.
Import reconstructs positive/negative encoding and verifies the assembled alias.
Old MAIN owners remain raw. OP menu exercises actual CP932 Borland producers.
MAIN/MAINE shared sound units explicitly retain binary O; genuine MAINE source
uses a mixture of M/O/E contexts, so inspect real reference producer arguments.

## Open scopes and current next work

Boss background has 17 accepted functions / 2,891 bytes. Its particle renderer
remains 158 versus original 159 bytes (OR AX,AX versus CMP AX,0). The following
compiler contribution uses one uncredited origin hole outside all functions.
The entire 159-byte original particle function stays unaccepted. Hexagram
rendering's 204 raw bytes match, but ordered MZ fixups differ across a compiler
LEDATA boundary, so that whole function also stays unaccepted. Never sort or
normalize those differences.

Stage initialization's 189 initialized DATA bytes and OP menu's 1,089 DATA
bytes / 26 ordered fixups now have separate accepted DATA evidence and their
own compiled DATA mutations. Source BSS locations are checked,
not treated as initialized file bytes. OP menu's first scaffold stack displaced
BSS by 84h; omitting artificial stack allocation fixed layout without modifying
the game algorithm. See `BORLAND_NOTES.md` and owner notes for type/ABI lessons.

OP setup adds 1,439 code bytes / 12 functions, character selection 1,181 / 4,
and seven high-score viewer functions add 1,099 bytes. The latter reuse two
unchanged independently produced cold artifacts through the retained-scope
reviewer, which validates the entire original parent and mechanical scope
derivation without recompiling. The remaining 312-byte registration menu has
identical raw code but differing ordered fixups and stays unaccepted.
OP configuration adds 379 bytes / 3 functions and music prefix 381 / 4.
Eight music suffix functions add 646 bytes after a new focused replay with
an accepted comment-loader negative; the previous suffix negative belonged to
an excluded menu function and could not support subset acceptance. Polygon
update (502 bytes) and music menu (837) remain raw-exact but ordered-inexact.
Shinki adds ten complete functions / 1,486 instruction bytes. The mixed parent
retains raw-exact but ordered-inexact later code. Seven functions are reviewed
from unchanged retained producers, carrying the real unchanged negative owner;
no new compiler invocation is claimed. Static phase102, ball update220 and four
ordered-inexact functions (386/169/802/959) remain unaccepted.
Generic Boss adds six complete functions / 352 bytes. The original 414-byte
defeat function is 408 under natural C++ because TC merges two common call
tails; the original 43-byte collision function is 46 with ordinary signed
locals. Both entire functions stay unaccepted. A six-byte outside-contribution
hole restores the real collision address for accepted caller bytes; no ASM,
pseudoregister math or inert barrier is used. Private documented optimization
variants failed strict comparisons and remain diagnostic only.
Sara adds twelve complete functions / 1,823 authored code bytes, with ten
semantic switch-table bytes and one excluded alignment byte. Midboss state
adds 85 bytes / two functions; reward functions add 218 / two. The natural
midboss defeat function remains 66 versus original 65 bytes and stays unaccepted.
The failed whole midboss/music candidate entries are removed from normal replay
selection; their retained failed artifacts and owner notes remain available.
OP title adds 618 bytes / three functions. MAINE all-cast adds 611 / three,
staff clip 104 / one, entry 336 / four, and high-score lifecycle 416 / three.
MAIN adds circle effects 257 / four, firewaves 94 / two, Mai/Yuki flight 248 /
two, playfield shake 273 / one, and six gather functions 549 bytes. Gather's two
original 27-byte ASM structure-copy helpers are external and uncredited; their
holes are outside the two real compiler contributions.
Nine MAINE cutscene functions add 1,241 bytes (1,225 instructions, 16 tables),
with Return-key animation period as the compiled negative. The cutscene's
52-byte EGC helper and 1,555-byte opcode dispatcher remain unaccepted.
The MAINE helper frames come from original bytes: sound's real frame E80
differs from calibration E7F. Maintain full enum domains and real structures;
no opaque opcode arrays, fake symbols, compiler-body ASM or inert barriers.

## Cached targets, routing and tools

`config/targets.toml` pins the supplied copy; provenance remains
candidate-local-attested. MAIN is ordinary MZ, OP/MAINE DIET-packed MZ, ZUN COM.
Decoded payloads/receipts are in `.analysis/decoded`. Reference calibration
builds complete but fail whole-file equality and create zero credit:
`main-calibration-b` (83 steps), `op-calibration-a` (47),
`maine-calibration-a` (36), under `.analysis/builds/`.

Private surveys route 21 OP shapes / 12,288 candidate bytes, 17 MAINE shapes /
5,678 bytes, and 63 maintained TH04 function shapes / 4,439 bytes. They are
routing only, including possible false complete boundaries and overlaps with
already accepted code. Reuse these maps; independently review original extents.

Pinned Borland tools have independent Wine state. Ghidra 12.1.3 / Temurin 21
are installed; `ghidra-project/TH05-main-loader` passes loader database byte /
fixup attestation and bounded disassembly. Full autoanalysis exceeded 768 MiB;
use loader-only and bounded ranges. Failed old projects are not evidence.
Serialize heavy tools with `.analysis/borland.lock` and `run_heavy.sh` (one CPU,
35% quota, 768 MiB, no swap, low priority). TH03 has unrelated dirty work: never
modify it. TH04 is a read-only reference.

Enemy tile invalidation adds one complete 43-byte function. The observed
near Pascal entry consumes four bytes and RET4; a documented Borland typed
view of the existing symbol naturally emits PUSH dword. Shared ABI definitions
are unchanged. The complete enemy allocator separately adds 252 bytes through its own
whole natural C++ producer and compiled interval mutation. The STD runner and
update remain unaccepted: five raw bytes
and one loader relocation differ in each owner at real far-call shortening.
A private ordered common-SEGDEF diagnostic did not resolve them. Failed scopes
are removed from normal selection; source/notes and evidence stay retained.

Laser creation/control adds five complete functions / 448 bytes; update adds
one / 312, including a 14-byte compiler switch table. See
`src/main/bullet/laser.md`. Each has its own two independent positive producers
and compiled gameplay mutation; rendering adds one / 582 with its own minimum-radius mutation. State buffers
and all foreign API bodies remain uncredited.

Dialog file loading adds202 instruction bytes across three complete functions;
demo loading adds94 across one. Demo playback114 retains its genuine far-call
shortening mismatch and stays unaccepted, with its failed parent retained.
Shared initialization adds72 in each of MAIN/MAINE. Sound-mode selection adds
154 MAIN instruction bytes plus two compared, excluded shortening NOPs. Full
original SE enum domain is essential for the exact ternary expression.

Sound mode selection now also adds154 each in OP/MAINE, with separately
reviewed real frames and own compiled controls. Generic shots add three
functions /182 authored CODE bytes (150 instructions +32 compiler table),
excluding one checked zero padding byte. Reimu bomb stars add466 instruction
bytes, excluding one original linker NOP; stage-five midboss rendering adds101.
The Extra-stage same-shaped renderer is independently identified and uncredited.

OP core initialization adds one complete124-byte function, including genuine
Borland port-I/O intrinsics. Item splashes and invalidation add130/2 functions
and75/1; the real invalidation loop visits32 slots even though the full item
pool has40, preserving the original behavior. Owned DATA/BSS remain zero.

Item creation/death drops add385 instruction bytes across two functions. All
three initial item owners now pass590 bytes /five functions. The parity check
uses the real byte bit test; the following signed modulo64 operation remains
as observed. No other item source/header changed. The already failed whole
Shinki3552 candidate was removed from default selection; its archived failed
producer and accepted retained function scopes are unchanged.

EMS cache adds three complete functions /529 CODE bytes:521 instructions,
eight compiler switch-table bytes and one excluded checked zero. Its two
684-byte producers match all raw code, but whole ordering and the154-byte
boss-face preload ordering fail. Only the strict three scopes are reviewed
from retained artifacts, using the same actual compiled negative and no new
compiler run. The failed whole is removed from default selection.

Item extend and miss penalty add79 and70 instruction bytes through independent
complete scopes and actual compiled controls. Collection's natural689-byte
producer is missing one original checked zero before its seven-word table;
normal `-a2` did not fix it and was removed. Collection remains entirely
unaccepted, including its known original ordering risk. Main item update is
248 versus241 due to genuine typed coordinate spills; ABI and pre-clamp
semantics are correct, and no register template or flag variants were added.

Dialog box wipe/fade adds106 instruction bytes/two complete functions. Its
835-byte full runtime candidate remains unaccepted; command handler459 differs
from456 while the separate270-byte runner has a correct size. Box bodies are
shared through `box.inl`, with a focused real106-byte producer and its own
timing negative. The documented TH04 `-B` hypothesis did not restore Shinki's
missing4 bytes; one unchanged-source compiler diagnostic and zero-size foreign
segment integration evidence are retained in `shinki-bmode-a`, with zero credit.

OP/MAINE each add the complete35-byte BGM measure query with independent
producers and a MIDI-meter negative. The first-positive MAP boundary gate now
stops a size-invalid replay before a needless second compile. Real player
invalidation176/145 and movement174/134 diagnostics prove that early exit,
while both new measure owners still produce two positives plus a negative.
Those player candidates are parked with zero exact credit and no flag/register
variants. Public CI includes a regression for the first-MAP failure behavior.


### Dialog runner incremental acceptance

`main-dialog-run-d` accepts the independent270-byte runner from the unchanged
natural `run.inl` body. Two cold positives and a compiled wait-argument negative
pass. The corrected unsigned filename pointer removes the command handler's
sign extension, but the full runtime is831 versus832 because its original
switch-table prefix zero is absent; that whole contribution remains unaccepted.
Only the new runner was replayed; accepted box/file owners remain unchanged.


### Dialog face and sprite tail

`main-dialog-tail-scopes-c` accepts the complete248-byte face cache loader and
67-byte Extra-Alice sprite cleanup from the unmodified four-function C++ TU.
Both have two fresh raw/ordered positives and compiled semantic controls.
Whole tail-b is619 versus620 and remains unaccepted; animation and exit do not
receive credit. The original full620-byte result is preserved privately,
including the failing far-call relocation and exit table-prefix difference.


### Stage-two midboss update

`main-midboss-stage2-c` accepts the entire393-byte state machine with both
returns, original ordered fixups350/241/210, two fresh deterministic builds and
an HP-threshold negative400→401. The first natural395-byte candidate exposed
an unnecessary inline-helper exit jump and a transposed vector destination;
original instructions establish the ordinary direct clear update and actual
(192,64) target. Both were corrected semantically before acceptance. Movement
and pattern helpers remain genuine foreign functions; no bodies or target
instruction templates are supplied by the binder.


### Stage-one and three midboss logic

`main-midboss-stage1-a` accepts all three complete movement/pattern/update
functions from the natural ReC98 C++ owner. All543 bytes, five original ordered
fixups and the16→17 firing-interval negative are checked; credit is542 bytes
(534 instructions,8 compiler-table bytes), excluding the single checked zero.
The genuine packed-word spread setter and canonical ABI produce the original
code without instruction templates.

`main-midboss-stage3-a` accepts the complete332-byte callback including its
trailing compiler table:323 instructions, one checked zero and8 table bytes,
331 authored bytes. The sole original relocation at relative280 and both
cold raw producers agree; invincibility threshold192→193 is rejected. The
original RETF ends the instruction stream, not the function contribution: the
four-word table remains part of the complete comparison. All unrelated
accepted evidence is reused unchanged.


### Stage-five and Extra complete updates

`main-midboss5-extra-b` accepts independent318-byte stage-five and366-byte
Extra callbacks. Each has two fresh deterministic raw/ordered producers. The batch control is
bonus30→31; Extra has the supplementary HP1000→1001 control described below. Neither owns a
CODE table, padding, DATA or BSS. Real near pattern-pointer tables remain
external. The initial stage-five wrapper stem had nine characters, so TCC
emitted a short-name object; only its generated DOS alias was corrected before
the successful replay. The replay command now rejects invalid DOS8.3 wrapper
paths before accessing targets or running tools, with a CLI regression check.


### Stage-five and Extra helper algorithms

`main-midboss5-extra-patterns-a` accepts five complete stage-five functions
(462 bytes) and five Extra functions (440 bytes), each from its own frozen
natural C++ producer group. Both groups have two fresh deterministic raw and original ordered-fixup
positives. The batch control mutates stage five; Extra has a supplementary
owner-specific speed control described below.
These902 bytes are entirely instructions; no tables, padding, DATA or BSS
receive credit. Full canonical bullet-special union declarations are preserved
in the independent Extra ABI header; accepted update/bullet headers stay
unchanged, with no opaque object-byte view used as a substitute.


### Independent supplemental negative controls

The normal batch driver compiles one named negative owner. Earlier notes that
implied one negative per batched producer group were corrected. Extra update's
HP1000→1001 mutation is actually compiled in `main-midboss-extra-negative-c`;
Extra helper speed8→9 is actually compiled in
`main-midboss-extra-pattern-negative-b`. Both reports retain/revalidate their
parent's two immutable positive producers and compile one additional negative
each, using the identical pinned tool receipt. They change no acceptance or
byte totals. `scripts/supplement_negative.py --check PATH/receipt.json` checks
the full saved parent and negative artifacts without running a compiler.

### Stage-four complete natural prefix and update

`main-midboss-stage4-b` accepts all798 raw bytes across three real pattern
helpers and the complete callback, including its switch table. Credit is797
bytes (789 instructions,8 table bytes), with the original zero excluded. The
first producer's797-byte result isolated the missing word-alignment context;
restoring the donor's actual alignment option after all ABI declarations yields
two exact deterministic producers, all seven original ordered fixups, and a
rejected entrance-threshold192→193 control. No instruction or inside-function
padding bytes were supplied by the binder or source.


### Stage-two and three complete helper owners

`main-midboss-stage2-patterns-a` accepts298 instruction bytes/three complete
movement/pattern functions with the original single ordered fixup and its
orbit-bound128→129 control. Its own prologue establishes the odd start15CC1;
no alignment gap was inferred from the neighboring accepted owner.
`main-midboss-stage3-patterns-a` accepts616 instruction bytes/five complete
functions with original ordered fixups546/424/405/235/144 and a spread3→4
control. Genuine rank-selector and gather packed parameters are preserved.
Both owners have two fresh deterministic positives, no table/padding/DATA/BSS,
and reuse unchanged accepted update headers.

### New natural Boss and transition owners

Louise's complete four-state charge helper and two initial patterns are
accepted429 bytes/three functions in `main-louise-initial-patterns-a`; the blue
spread5→6 mutation is rejected. Alice's puppet beam pattern is accepted354
bytes/one function in `main-alice-puppet-beam-a`, with the width56→55 control.
The full26-byte puppet type, real far shot-hit helper and complete point
comparison preserve the original ABI, without compiler-body ASM.
The previously foreign stage-four transition helper now passes208 bytes/one
function in `main-midboss-transition4-a`, with sound13→14 control. Each receipt
has its own negative and two fresh deterministic positives; no tables,
padding, DATA or BSS receive credit for these new instruction-only owners.


### Louise later patterns and Alice charge patterns

`main-louise-later-patterns-d` accepts603 instruction bytes/four complete
functions. Two typed byte-speed updates use a real integral wrapped negative
delta, retaining defined modulo256 semantics without ASM or idle work. The
fan-angle24→25 control is rejected. The earlier597-byte compound-assignment
producer and603-byte raw-inexact alternatives remain failed; the negative-float
candidate was outside the unchanged speed helper's valid domain and discarded.
`main-alice-charge-patterns-a` accepts499 instruction bytes/three complete
laser/stack/ring functions with all six original ordered fixups and its own
laser-width8→9 control. Every owner has two fresh deterministic raw/ordered
positives; source headers already accepted for beam/laser/charge are unchanged.


### Independently reviewed Master procedure attribution

The public `scripts/review_master.py` revalidates20 complete literal procedures
from the author's pinned0.23 archive against the actual historical listing,
OMF and original/linked MZ. Active FAR/data-model macro alternatives and all
frozen source dependencies are checked, with no byte/source normalization
beyond source encoding/newlines. Forty absent/ambiguous/different source blocks
and196 uncovered gap bytes remain unknown; the mixed prefix is not excluded.
The unchanged proposal metadata and a separate explicit20-name decision are
recorded by independent hashes. MAIN combines CL and Master claims through the
same overlap-rejecting overlay and retains separate decision digests. A native
`ownership.py --write --verify-targets` run confirms all319,268 coordinates and
3,277 vendor bytes, while authored bytes and the null denominator are unchanged.


### Louise phase callback

`main-louise-update-a` accepts the full582-byte far callback, including the
original table-prefix zero and eight-word switch table. Authored credit is581
bytes (565 instructions plus16 table bytes), one complete function. Both fresh
raw/ordered producers agree, including the sole relocation at relative121;
phase-end HP3000→3001 is rejected. The actual movement API remains a truthful
near Pascal(speed,duration) helper; all four packed calls and background
callback context are preserved. Existing charge, bullet and laser helpers and
headers remain unchanged.


### Louise movement, Yumeko and complete Alice helper scopes

Louise's genuine Pascal movement passes122 bytes in `main-louise-flystep-a`.
Yumeko's bounce/sword/ring group passes435 bytes/three functions in
`main-yumeko-patterns-b`; the only initial semantic error was reversed gather
colors, corrected from(frame,6,7) to(frame,7,6). Both independent receipts have
their own336→335 boundary control and two fresh deterministic raw/ordered
positives, with no table/padding/DATA/BSS credit.

Alice's final spread passes as a standalone63-byte owner with true external
frames and its own speed2→3 mutation. Five puppet callbacks pass individually
in `main-alice-puppet-scopes-a` (556 bytes total). The two real TU producers
are shared, but every complete function's raw bytes, immediate public
boundary and original ordered fixup[22] are checked separately. The aiming
control is compiled in the second spread scope; no whole556-byte global
fixup-order claim or independent negative per sibling is made.

The natural Alice update remains unaccepted: its939-byte callback lacks one
original table-prefix zero, despite retaining the real63-byte predecessor.
The complete entrance/dispatcher owner now passes 643 instruction bytes/two
functions in `main-alice-puppet-motion-d`. Early FAR/NEAR helper-reference
producers emitted 710/690 bytes. Direct field easing removed address
temporaries but emitted 634; a shared ordinary integer temporary across the
mutually exclusive delta and callback-result paths recovered the original
register allocation. Both fresh full raw/ordered producers pass, and the
entrance angle decrement2→3 control is rejected. The failed whole update
owner remains outside default replay and receives no callback credit.


### Alice recovery and opening patterns

`main-alice-opening-patterns-a` accepts461 instruction bytes/six complete
functions: real near Pascal puppet recovery/hold callbacks and four charged
opening patterns. Both fresh producers agree on the entire raw contribution
and original ordered fixups[437,313,182]; the ring count28→27 control is
rejected. No DATA, BSS, padding or compiler tables receive credit.


### EX-Alice initial patterns

`main-exalice-initial-patterns-c` accepts314 instruction bytes/three complete
functions with two fresh deterministic full raw/ordered positives. The real
fan spread5→6 control is rejected. The initial broad bullet-update include
conflicted with the independent HUD speed helper; the owner now uses unchanged
canonical types plus the complete two-alternative special-state union. The
first314-byte producer only reversed two gather color operands; correcting
the real Pascal call to(frame-48,6,7) restores both bytes. No DATA, BSS,
padding or compiler tables receive credit.


### EX-Alice later patterns

`main-exalice-later-patterns-a` accepts600 instruction bytes/three complete
functions with two fresh deterministic full raw/ordered producers. The
first-fan speed5→4 control is rejected. The real firewave Pascal call, full
player-angle Subpixel parameters, point state and word pellet color preserve
actual storage and ABI. No DATA, BSS, compiler tables or padding receive credit.
The separate Alice context review found no original TH05 source TU boundary
evidence; its missing table-prefix zero does not justify speculative context
compiles. The bounded review remains in ignored analysis evidence.


### Yumeko standalone spreads and EX-Alice laser patterns

`main-yumeko-spreads-a` accepts518 instruction bytes/two complete spread
functions with a rejected reset-frame256→257 control. The three-function
872-byte parent emitted875: first-function Subpixel coordinate construction
adds one3-byte stack store, and the whole original relocation stream also
has a genuine nonmonotone first entry. The aimed-sword354-byte function
remains unaccepted. Unchanged real spread bodies are shared in spreads.inl,
with independently correct standalone symbol/DS context; no source acceptance
is transferred from the failed parent.

`main-exalice-laser-patterns-a` accepts645 instruction bytes/four complete
callbacks, with original ordered fixups[422,98] and a compiled fixed-laser
grow age47→48 control in the second function. Full canonical Laser storage,
real Pascal spawn API and genuine first16-slot loop are preserved. Both
owners have two fresh deterministic full raw/ordered positives and no DATA,
BSS, compiler-table or padding credit.


### Mai/Yuki initial patterns and EX-Alice phase/final scopes

`main-mai-yuki-initial-patterns-a` accepts543 instruction bytes/six complete
functions with original ordered fixups[525,433,324,233,51] and the real attack
stack2→3 negative. `main-exalice-phase-a` accepts111 instruction bytes/two
complete functions (far hit gating33 plus Pascal phase transition78), with
an empty original fixup stream and immunity39→40 negative. Both owners have
two fresh deterministic full raw/ordered positives and no tables/padding/data.

`main-exalice-final-scopes-b` accepts475 bytes/three complete functions from
the real809-byte TU: cross143, turning109 and final fan223. Two fresh whole
producers supply all selected actual boundaries/raw/ordered comparisons, with
one shared cheeto speed3→4 negative in the first function. Branch-local real
aim calls and gather assignments recover the original control/data flow; the
earlier conditional-expression producer emitted787 bytes. No shared ABI,
flags, fake calls or barriers were changed. The remaining spiral334 function
is raw exact in both saved positives but has target ordered fixups[86,256]
versus producer[256,86]; it remains outside live selection and uncredited.
The complete809-byte ordered claim remains unaccepted.


### Yumeko complete update and final ring

`main-yumeko-update-a` accepts the complete884-byte owner:165-byte final
ring helper plus719-byte far callback, including the real original zero and
22-byte eleven-word switch table. Authored credit is883 bytes (861 instructions
and22 semantic table bytes), two complete functions. Both fresh raw/ordered
producers agree, including the original six relocation sites; the actual
final-ring turns2→3 mutation is compiled and rejected for this whole owner.
No independent helper/callback negative per sibling is claimed. Full canonical
Sword/Boss/special state, actual main01 rendering pointers, near generic
helpers and all table destinations retain their true ABI and storage.


### Yumeko sword lifecycle helpers and standalone Mai/Yuki attacks

`main-yumeko-sweep-a` accepts321 instruction bytes/one complete function,
with its real speed-limit6→7 mutation. `main-yumeko-swords-add-a` accepts121
bytes/one complete allocator, with circle color9→10 mutation. Actual full
Sword/template/pool state and real Pascal/fastcall helpers are preserved;
the283-byte updater stays unwritten due its genuine DX:AX struct-return
lowering issue. Both owners have two fresh full raw/ordered positives.

`main-mai-yuki-remaining-patterns-a` accepts939 bytes/ten complete attacks,
with original ordered fixups[920,833,462,136] and the first selected angle
0x20→0x21 control. The first tracking-laser candidate emits185 versus186,
and the failed full1124-byte TU shifts later near-call displacements. Its
unchanged real later bodies are shared in remaining_patterns.inl and have
their own correct standalone source/binder context; no padding byte or
acceptance transfer from the failed ten-scope receipt is used. The tracker
remains uncredited, including its original fixup order[38,130].

The complete EX-Alice update1060 remains unaccepted after two first-positive
1064-byte gates. Four actual OMF far calls become TLINK's five-byte
NOP/PUSH-CS/near-CALL sequences instead of original four-byte sequences.
The true same-CS first declaration does not repair this; no further flag,
padding or binding probes are justified. All1008 semantic instruction bytes
and52 switch-table bytes remain in the natural candidate, with no trimming
or normalization. Actual source TU/callee-definition context remains open.
The failed owner is removed from live replay selection.


### Mai solo opening patterns

`main-mai-solo-initial-patterns-a` accepts456 instruction bytes/three complete
functions (164/198/94), with original ordered fixups[306,107] and a real
first-fan spread2→3 negative. Both fresh deterministic full raw/ordered
producers agree. The first two real bool callbacks retain completion/movement
semantics, while the third signed-cycle pattern is truthfully void. Full
canonical Boss/template/special state and byte-rank ABI are preserved without
editing shared accepted headers. No DATA, BSS, tables or padding receive credit.


### Mai solo snow patterns and complete Yuki update

`main-mai-solo-later-patterns-b` accepts496 instruction bytes/three complete
functions (89/141/266), with original ordered fixup[365] and ring count24→25
control. Its first496-byte producer differed only in one outlined-blue sprite
constant44; the actual outlined sprite is45. The unchanged new fullB4Ball26/
template25/bool16 ABI is shared with Yuki and checked against custom slots.
`main-yuki-update-a` accepts the complete826-byte far callback,806 instruction
plus20 switch-table bytes, with original ordered fixups[256,140] and actual
HP threshold4600→4500 control. Both owners have two fresh deterministic full
raw/ordered positives. No padding, initialized DATA or BSS receive credit.

The shared Mai/Yuki update remains unaccepted: the initial broadHUD include
conflicted with movement's to_sp definition. The candidate now declares only
the real canonical byte-text FAR title pointer and preserves existing function
contexts; the next first positive emits1023 versus1018. Two word shake assignments each add3 instruction bytes, while the original
zero disappears. A natural shared-store dataflow repair remains unverified.
The failed owner receives no credit or default replay selection.


### Survivor callback identities, guards and atomic evidence import

Actual shared Yuki dispatch usesDS4430; both survivor callbacks useDS4438,
now truthfully named boss_solo_pattern_current, while Mai's inner void bank
uses443A. Yuki826 was replayed asmain-yuki-update-c with unchanged complete
raw bytes/fixups and its own negative. The native accepted-MAIN audit now
checks131CODE units/3883 actual scoped DATA references/223 names with no
remaining same-name/different-offset collision. It excludes2DATA owners and
actualBINARY-O Kaja;60legacy owners lack saved argv and remain explicitly
separate from71actualsaved-M owners. This is a bounded identity audit, not
a whole-program or denominator proof.

Long common Mai-solo header guards collided under the old compiler. Short
distinct guards compose all required full interfaces; only the two affected
accepted owners were replayed (initial456-b/later496-c). The importer now
validates multiple complete receipt inputs before one merge, final global
source-current check and atomic publish. Repeated --accept handles changed
header closures without recompiling already-valid independent positives.
Five real MAP/MZ/OMF/source/negative regression cases cover atomic failure
and existing single-subset compatibility. Actual six-receipt import succeeds.

Yuki solo owners509/670 pass independently (1179 instruction bytes/seven
functions), with their own speed54→55/snow64→80 controls and original ordered
streams. Mai advanced615-b passes three complete functions and real fan
speed3→4 control. Mai laser-cycle461-a passes its complete bool function,
empty fixups and rank-count+5→+6 control; its inner void bank is separate
from the270-byte bounce attack. Every owner has two fresh deterministic
complete raw/ordered positives, with no DATA/BSS/padding/table credit.

Shared Mai/Yuki c now emits1017 vs1018 after the supported conditional-word
store repair; its original table-prefix zero remains absent. Mai solo
update a emits785 vs786, likewise lacking the original zero before its
complete20-byte table. Both natural callbacks remain unaccepted and outside
default replay. No padding insertion, clipping, normalization or speculative
flag/context probes are used. The shared owner retains its full24-byte
value/destination tables, and the solo owner retains all20 table bytes.


### Coherent EX-Alice updater and real B4Ball allocation

`main-exalice-update-full-context-a` accepts the complete1060-byte updater:
1008 instructions plus52 switch-table bytes, one complete function. The
real33-byte far shot gate and78-byte phase helper are now actual preceding
definitions in the same TU/CODE contribution. All three natural bodies are
verbatim to the maintained standalone sources, and ABI/flags are unchanged.
This resolves the four extra far-call relaxation NOPs; declaration context
alone had not done so. Both fresh producers pass the selected raw/ordered
[198,161] scope and its own HP23800→23700 negative. Independent saved-output
review also confirms the whole1171-byte context and original[309,272] order.
Prefix111 remains credited once through its existing owner; only1060 is new.
The previously failed standalone updater is retained as a failed alternative,
while the target callback is now accepted through full_context.cpp.

`main-b4ball-spawn-a` accepts132 instruction bytes/two complete reset27 and
allocator105 functions, empty original fixups and new-ball damage0→1 control.
Both actual caller ABIs are void near Pascal; no CF-return contract is invented.
The complete frozen B4Ball/template/custom-pool storage is unchanged. The273
updater remains unimplemented because its return-register use needs separate
source reconstruction. Both new owners have two fresh deterministic complete
raw/ordered producers and no DATA, BSS or padding credit.

## Spark lifecycle and survivor callback tables

The focused `main-spark-lifecycle-a` and `main-mai-yuki-solo-pattern-data-a`
receipts add two complete Spark functions (68 CODE bytes) and seven semantic
near-callback banks (36 DATA bytes). Both have two fresh positive producers,
full raw/ordered-fixup equality and independent compiled mutations. The callback
banks retain distinct bool/void callback types and all 18 genuine function
pointers. Spark preserves the original 96-record traversal over a 64-record
active pool and low-byte writes to word fields. No unchanged owner was rebuilt.

## Mima and Yuuka bomb shapes

`main-mima-circles-b` and `main-yuuka-heart-d` add two complete independent
callbacks, 307 instruction bytes with no padding/tables. Their own compiled
distance mutations reject, and two fresh producers match raw bytes and original
ordered fixups. Full existing bomb/player storage and true polar/sprite/fill
interfaces are preserved. Pixel-space polar centers are intentionally unscaled.
See `src/main/player/bomb_shapes.md`; no unchanged owner was rebuilt.

`main-marisa-bomb-lasers-b` adds the complete 335-byte eight-beam callback
with seven original ordered fixups, two fresh producers and its own rejected
radius mutation. Together the three bomb-shape callbacks add 642 CODE bytes.
The original Spark callback boundary and player reload are preserved.

## Complete new-game initialization

`main-gameplay-session-init-a` adds one complete 468-byte new-game function:
450 instruction bytes plus 18 bytes of compiler-generated rank/character switch
tables. Two fresh producers match all raw bytes with no relocations/padding;
the independent dream-initialization mutation rejects. The actual four-by-ten
shot dispatch table, resident object and near callback ABIs remain full size.
Stage-session initialization is a separate unaccepted owner.

## Additional foreground, pause and bomb control owners

`main-alice-puppets-whole-a` proves the complete 381-byte C/Pascal puppet
renderer as its own natural TU. Its body is literally unchanged from the
archived full candidate; the neighboring 150-byte Alice callback remains
unaccepted against original140. No C-public function-scope guard was relaxed.
`main-session-cleanup-pause-a` proves both complete stage cleanup and pause,
334 instruction bytes. Its Q-result mutation is an owner-level control;
cleanup has no separate mutation claim. TH05's input-release behavior and
resource ranges remain intact.

The complete Marisa161, Reimu193 and Yuuka193 bomb-control callbacks also
pass two fresh producers, full raw/ordered fixups and independent tone mutations.
Mima161 remains raw-exact but ordered-inexact and receives zero credit; its
original relocation order stays untouched. No unchanged owner was replayed.

## Additional complete foreground scopes and retained Mima draw

Standalone Louise116, Mai/Yuki sprite-helper75, Yumeko161 and Shinki160
now pass their own focused double producers and semantic mutations. Source
factors preserve literal complete bodies; their larger failed cohorts remain
unaccepted. Marisa drawing60 also passes independently.

The raw-exact but ordered-inexact Mima366 producer supplies its complete205-byte
drawing function through `main-mima-bomb-draw-a`: two retained cold producers,
no new compiler invocation, the original negative radius mutation, real next
function MAP boundary, and all eleven scoped ordered fixups. The failed whole
parent stays archived unchanged, and Mima control161 still receives no credit.

The session shot-dispatch pointer typedef now uses its true near Pascal ABI,
matching all actual shot providers. Only the affected initialization468 was
replayed (`main-gameplay-session-init-b`); counts are unchanged by this fix.
Known failed runtime/shot/background2/full-foreground entries are absent from
the default replay manifest, with natural candidate sources retained separately.

## Shot dispatch DATA and EX-Alice foreground

The complete four-character, ten-level `SHOT_FUNCS` table passes as semantic
initialized DATA80 (`main-shot-function-table-data-a`), with forty genuine near
Pascal function pointers, thirty-four unique reviewed providers, two fresh
producers and its own compiled Reimu L2/L3 swap. EX-Alice's complete foreground
callback163 also passes independently (`main-exalice-foreground-a`), including
all four original ordered fixups and its own sprite-bank mutation.

Natural failed candidates are retained with zero exact credit; see
`docs/reconstruction/UNACCEPTED_COHORTS.md`. Their known failures are not in the
default incremental replay manifest.

## Character bomb preludes and EX-Alice custom bullets

`main-reimu-bomb-draw-a` and `main-yuuka-bomb-draw-a` add the complete84/120
instruction-byte callbacks, with two fresh producers and independent palette
mutations. `main-exalice-custom-render-a` adds the complete308-byte firewave
fill/sprite/collision renderer and cheeto-render dispatch, retaining all three
original ordered fixups and its own phase-step mutation. All use full existing
storage and genuine graphics interfaces. Together these add512 CODE bytes.

Stage-session initialization803 stopped at first producer802: mandatory zero
missing and three unchanged-length far-transfer mismatches. Shot rendering's
safe word-local producer173 also remains unaccepted against164. The one genuine
byte-domain experiment175 clobbered the raw renderer's AX left argument; it was
abandoned and the safe original source restored exactly. These failures did not
run second or negative builds. No flags, padding or physical-register algorithm
variants followed. The default replay plan is empty for unchanged evidence.

## Process handoff, midboss rendering and stage reset

`main-process-handoff-a` proves the adjacent score-save34 and GameExecl159
callbacks as one complete193-byte owner with seven original ordered fixups.
The compiled gone/killed-counter mutation covers that coherent owner; there
is no separate score-save mutation claim. Actual process.h far strings and
four-byte variadic NULL preserve the real process handoff.

`main-midboss-render-124-a` proves the complete stage1/2/4 callbacks192/135/127
as three scopes of one real TU. Two fresh producers are shared, and one compiled
phase-two-cel mutation belongs to the first scope; the other two share that
oracle control. Original per-function relocation orders pass without a whole
454-byte relocation-order claim or normalization.

`main-stage-runtime-init-a` proves the complete174-byte per-stage state reset,
with its own invincibility mutation. Real donor samecodeseg annotations preserve
far signatures for the two verified AE1 services; linked NOP/PUSH-CS/call bytes
and the one original relocation match. See `BORLAND_NOTES.md` for the observed
context lesson. No 803-byte session-init acceptance is implied.

## Padding correction and recovered enemy call contexts

A native instruction-NOP scan across accepted MAIN/OP/MAINE identified five
uncounted relaxation padding bytes: two in setup1510, one in bullet-update1619,
and two in reset174. They now receive zero credit through three focused fresh
replacement receipts, atomically imported. Complete raw bytes and original
fixups remain unchanged; no OP/MAINE omissions were found. No other accepted
unit was replayed. The five-byte credit correction is included in the counters.

Truthful samecodeseg declarations then recovered the two old enemy blockers:
`main-enemy-samecodeseg-a` passes std89 and update576 from one actual TU per
cold round. The far interfaces and verified CS1527/RETF0/RETF8 contracts are
unchanged; two NOP padding bytes are checked and excluded, adding663 authored
instruction bytes. The compiled STD condition mutation controls the pair;
there is no independent update-mutation claim. Allocation and invalidation
accepted dependencies remain unchanged.

## Complete game-over flow and additional motion/render owners

`main-gameover-a` adds four complete callbacks in one869-byte owner, with four
checked/uncredited NOP bytes:865 authored instructions. Both fresh producers,
all27 original ordered fixups and the coherent owner's credit-limit mutation
pass. `main-player-miss-a` adds the complete307-byte death handler with five
checked NOPs:302 authored instructions and its own power-cap mutation.

`main-midboss3-render-a` adds127 instructions. `main-midboss-defeat-render-b`
adds170 instructions; its ordinary for-update clause now reflects the actual
counter-before-angle order, without dummy work or register forcing. Both have
their own compiled animation mutations and original ordered fixups.

`main-stage2-update-abi-a` adds the complete653-byte updater through the genuine
packed Motion return boundary. `main-shots-update-abi-b` adds the complete408
bytes:400 instructions plus8 compiler switch-table bytes. Both keep the real
full return type/records and have their own rejected mutations. Direct signed
return-word reads end at the actual ABI boundary; ordinary algorithms are not
mapped onto physical registers. See `BORLAND_NOTES.md` for proof and limits.
The stage-two initializer remains unaccepted; no prefix credit transfers.

## Complete stage-two background and remaining renderer state

`main-stage2-particle-initializer-a` adds492 complete instruction bytes. The
only correction from the retained476 body is four real scalar rvalue scaling
assignments; both fresh producers, ordered fixups and the independent zoom
mutation pass. Together with acceptedupdate653, both original stage-two
background functions are covered. No combined-TU equality or prefix double
credit is claimed. The shared ABI header and updater receipts are unchanged.

`main-midboss-extra-render-a` and `main-mai-yuki-survivor-render-a` add101/126
complete instruction bytes, each with two fresh producers, original ordered
fixups and its own compiled animation mutation. Extra's distinct identity is
proved by the actual stage-setup callback assignment, rather than inherited
from its similar stage-five renderer.

Item241 remains open: the single235 experiment failed at its first size gate
and incorrectly clobbered the long-borrowed return X during pickup arithmetic.
The original typed safe248 source was restored exactly; no second/negative or
register-algorithm variants followed. Immediate return-ABI consumers653/408
remain accepted and unchanged. Bullet rendering334 likewise remains open
against330; no prologue or register-forcing workaround was added.

## Initialized item reward tables

`main-item-reward-tables-data-a` adds116 initialized semantic DATA bytes:
seven word sprite selectors, forty-three word overflow rewards and the eight
legacy Dream rewards. The complete three-array DATA contribution passes two
fresh producers, empty original fixups and its own compiled150-to151 reward
mutation. No BSS, padding, asset image or code bytes receive credit here.

## Player update and stage-bonus modifiers

`main-player-update-b` adds the complete281-byte player lifecycle callback,
with its own deathbomb-window mutation and no padding. Its preceding286-byte
candidate stored the byte movement return in a single-use temporary; consuming
that result directly in the ordinary retry condition recovers the original
flow. Real Motion, Point and near Pascal callback declarations remain intact.

`main-stage-bonus-helpers-a` adds two complete helpers /305 bytes:297
instructions plus eight generated rank-table bytes, no padding. Two fresh
producers, the original ordered relocation and its own divisor mutation pass.
The actual TH05 near description pointers replace the donor's far table type.
The full later bonus flows remain separate work; no context receives duplicate
credit. Existing accepted owners were reused without cold replay.

`main-std-free-a` adds23 complete instructions with its own guard mutation.
MAP release27 differs from original23 and stopped at the first boundary gate;
the natural source and failure remain, without a default replay entry.
`main-entry-c` adds109 instructions from the complete110-byte entry, excluding
its checked relaxation NOP. The actual accepted GameExecl's same-CS/RETF4
contract establishes the far-call context; the gameplay loop stays open.

`main-stage-bonus-full-a` then passes the complete normal561/allclear579
functions in their genuine1445-byte family context, preserving allclear's
nonmonotone original fixup order. Only the two later scopes receive new credit:
1124 instructions after16 checked NOPs, with no duplicate helper credit.
Both share the compiled stage-clear factor mutation; the configured allclear
mutation was not independently compiled. Source notes preserve these limits.
