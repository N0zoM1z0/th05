# TH05 current handoff

Goal: at least 98% authored bytes exact. Commit prefix: `gpt-6.1-sol:`.
Repository: https://github.com/N0zoM1z0/th05 .

Current acceptance: **140 bounded C++ CODE/DATA units / 267 complete function occurrences**,
**48,241 authored bytes exact**: 39,384 CODE and 8,857 initialized DATA.
CODE is 38,902 instruction plus 482 semantic compiler-table bytes.
Complete compared extents total 48,269; 28 checked padding bytes receive
no credit. MAIN has 185 functions / 26,819 CODE / 199 DATA;
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
Every unclassified interval remains unknown. Only 31 complete CL.LIB CODE
contributions / 2,901 bytes are separately reviewed as third-party, with
pinned native OMF/FIXUPP evidence and explicit member decisions in
`config/reviewed_vendor_units.json`. Two members with unwritten CODE ranges
remain unknown. No vendor byte contributes authored source credit.
`scripts/review_vendor.py --check` replays private inputs without compiling;
`--structural-check` verifies public metadata only. Regenerate the inventory
with `scripts/ownership.py --write` after accepted source changes.

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
