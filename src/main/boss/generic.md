# Generic boss: exact defeat and six helpers; collision still pending

Current status: `main-boss-generic` independently accepts six functions / 352
CODE bytes; `main-boss-generic-data` accepts the complete 10-byte item-drop
DATA table. The full **414-byte defeat** controller is now accepted; only the separate
43-byte player-collision function remains unaccepted. The
preparation notes below are historical context; use the current ledgers for
acceptance.

Natural source adapts pinned nmlgc/ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`,
`th04/main/boss/boss.cpp`, specialized for GAME 5. The owner reuses the complete
accepted Boss and Midboss structures through `stage/setup.hpp`, resident/score
layout, BulletTemplate and physical geometry. It preserves shot damage,
player collision, item drops, phase transitions, timed defeat effects, bonuses,
stage-score storage, next-stage dispatch and the actual homing sentinel.
There is no handwritten ASM, instruction emission, fake object or barrier.
The reference collision helper's AX/DX aliases are ordinary signed subpixel
locals here: this calculation has no hardware or returned-register contract
that would justify forcing pseudoregisters. Natural register allocation remains
subject to the first producer's full comparison.

The independently reviewed original CODE is **`[1FA51,1FD7A)`**, **809 bytes**,
267 instructions and ten ordered MZ segment fixups, with no table or padding.
Private `.analysis/boss-generic-boundary-review.json` records exact original
boundaries, hashes, return sites, ordered fixups and every external call.

| Complete function | Original decoded span | Bytes |
| --- | --- | ---: |
| `boss_hittest_shots_damage(int,int,int)` | `1FA51..1FA90` | 63 |
| `midboss_hittest_shots_damage(int,int,int)` | `1FA90..1FAD0` | 64 |
| `boss_hittest_shots()` | `1FAD0..1FAFA` | 42 |
| `boss_hittest_shots_invincible()` | `1FAFA..1FB0C` | 18 |
| `boss_items_drop()` | `1FB0C..1FB61` | 85 |
| `boss_phase_next(explosion_type_t,int)` | `1FB61..1FBB1` | 80 |
| `boss_defeat_update(unsigned int)` | `1FBB1..1FD4F` | 414 |
| `boss_hittest_player()` | `1FD4F..1FD7A` | 43 |

Reference calibration's whole contribution is 815 bytes and its defeat
function is 420. Its fadeout branch contains a five-byte far
`score_delta_commit()` call at calibration `1FCDE`; the pinned original
proceeds directly from the fadeout comparison to the stage-ID comparison at
`1FCD0`. That extra reference call also lengthens one branch by a byte.
The restored owner follows the original-observed behavior and omits the absent
call. This is an explicit original/reference version difference, not an
optimization substitute or a discarded target operation. The reference's
non-semantic `optimization_barrier()` is also omitted. A fresh producer must
still establish natural code generation; this static review grants no credit.

Registered complete-contribution candidate: wrapper `th05/boss.cpp`, segment
`BOSS_TEXT`, `wrapper_options = "-zPmain_03"`, MAIN binary M, target `0x1fa51`,
size **352**, first **six** complete functions, `alignment_offsets = []`, and independent
`probes/units/boss_generic_bindings.asm`. Original main_03 frame is `1527`,
contribution slot `A7E1`; DS is `209D`. The first actual producer had natural
sizes 352, 408 and 46 for the six helpers, defeat and collision respectively.
The compiler merged two identical all-clear tails in defeat; ordinary collision
locals used different registers and made that function three bytes longer.
Neither complete defeat414 nor collision43 is registered or accepted.

The natural source now places the six helpers in `BOSS_TEXT`, the whole
408-byte defeat function in `BOSS_DEFEAT_TEXT`, and the whole 46-byte collision
function in `BOSS_COLLISION_TEXT`, all in true main_03. The scaffold supplies
one six-byte ORG interval `[1FD49,1FD4F)` after the actual defeat contribution
and before the collision contribution, restoring the collision's real address
for the accepted helpers' near call. This hole is inside the wholly unaccepted
original defeat range, outside every complete compiler function and every
accepted scope. The natural collision ends at `1FD7D`; an independent PARA
segment aligns after all source contributions to `1FD80`, then supplies only
the external tail to DS `209D`. No inside-function bytes are supplied. Actual
OMF/MAP extents must still be verified; an end beyond `1FD80` fails this context.
The binder has no `.stack`, helper bodies or game values.

Original near calls use 16-bit CS-relative IP arithmetic. For example, a flat
Capstone address may print `276DD` for the small explosion call; the true
wrapped destination is **`1527:246D` = `176DD`**. The big explosion and random
modulo routines likewise resolve to `1778B` and `152C0`. Those true frames and
offsets, not unwrapped load-address arithmetic or calibration coordinates,
anchor the binder. Real main_01 callbacks are declared before the shared ABI
header so their initial compiler declaration retains frame `0AE1`. Shared
sound/delay helpers retain frame `14AB`.

The sole source-owned initialized DATA is the genuine two-by-five local
`item_type_t` drop table, ten signed-byte enum values at DS `[1FBE,1FC8)`.
All members derive from item semantics; no opaque target-byte array is used.
There are no DATA fixups or source-owned BSS. The already accepted stage-owned
`boss_phase_timed_out` byte begins exactly at `1FC8` and remains external. The
binder stops its DATA prefix before the entire compiler-owned table, then
uses only labels in the following foreign BSS context for later DS objects.
It never duplicates the table or stage flag. This table is now independently
accepted as `main-boss-generic-data`; that DATA result grants no acceptance to
the pending defeat/collision CODE.

A natural compiled negative changes the unique
`boss.phase_state.patterns_seen = 0;` to `boss.phase_state.patterns_seen = 1;`
in `boss_phase_next`, changing real phase state inside the registered first
six functions. It affects only a staged copy and must be compiled and measured
as rejected. The retained failed 806-byte producer and two private diagnostic
variants remain unchanged: function-local documented `-O-` produced defeat424,
and reversed structured bonus conditions still produced defeat408. Neither
restored original414 or grants acceptance. This packet claims neither accepted
CODE, whole-executable layout nor packed-file exactness.

## Accepted six complete functions

`main-boss-generic-b` passes both independent producers for the real 352-byte
first contribution, all six complete functions, original ordered fixups and
the compiled patterns-seen reset negative. The entire original defeat (414)
and collision (43) functions stay unaccepted. Their maintained semantic bodies
produce 408 and 46 bytes; a six-byte context hole sits outside all compiler
functions and restores the original collision address for the accepted callers.
The final paragraph context preserves original DS. No hole, inexact helper
body, initialized DATA or whole executable contributes progress.

A later independent collision-only diagnostic gives both deltas ordinary
`register` declarations. This still emits46 bytes with DX/BX allocation,
against the original43-byte AX/DX function. It grants no credit; maintained
source and binder were restored exactly.
The accepted six-function owner and maintained baseline remain unchanged.

A later independent complete defeat-function trial uses a stage-ID `switch`
for dialog/bonus selection. It emits411 rather than414: the compiler still
merges the two all-clear call tails, while ordinary switch promotion adds
three bytes over the408-byte baseline. Experimental source
and binder were removed; no accepted dependency, order or byte was changed.

A later complete-action trial gives the Extra-stage all-clear branch both
existing homing resets and an immediate return. The normal compiler still
merges the two all-clear call sites and emits 408 rather than native 414;
its later fixups remain six bytes early. No barrier, extra state mutation or
compiler-register algorithm is introduced. The failed standalone source/binder
were removed. The accepted
generic CODE/DATA and all maintained source inputs remain unchanged. No second
producer, negative or new credit is added.

## 2026-11-10 focused defeat controller compiler trials

The standalone 414-byte `boss_defeat_update` trial links at the true original
`1FBB1` start and retains all six original ordered fixup sites. The maintained
source still generates a 408-byte *complete* function with actual fixups
`[389,359,345,331,254,33]`, versus target
`[395,365,351,337,254,33]`. Disassembly identifies the six-byte loss: the
original duplicates the final all-clear call and jump in two real stage paths,
while Turbo C++ common-tail merging emits only one copy. Four ordinary semantic
preserving branch variants (explicit local gotos, inverted conditions, and
reversed branch order) all still generate 408 bytes. Their first cold diagnostics
are retained in `.analysis/gpt-web-defeat-{v1,v2,v3,v4}-a/` (not acceptance).
No inert compiler barriers or fabricated function bytes were introduced. The
retained natural `generic.cpp` and six accepted helpers are unchanged.

## 2026-11-10 full-size defeat-call experiments

Thirteen genuine C++ stage-bonus/dialog branch layouts and three documented
compiler-option profiles were compiled as bounded first-producer diagnostics
without affecting the six accepted neighboring functions. Ordinary baseline
remains 408 against native 414. A reordered last-stage dispatch emits **414
bytes** but emits two dialog far-call relocation sites rather than the original one, so
fails original semantics and ordered-fixup comparison. A decoupled dialog
condition emits **415 bytes with the same six relocation sites**, shifted one
byte after the stage branches. `-O-` alternatives generally emit 417–429 bytes;
`-Z-` and `-G` do not fix the original merged all-clear tail. The original
requires *two* identical separate all-clear calls without duplicating
`dialog_animate` or manufacturing an inert branch. Source and accepted ledgers
are untouched. Private real trial roots:
`.analysis/gpt-web-boss-defeat-calls-*-a/` and
`.analysis/gpt-web-defeat-option-*-a/`.

## 2026-11-10 original bonus-call inline-language trial

The 414-byte `boss_defeat_update` remains unaccepted. A fresh isolated
Borland C++ producer again confirms the baseline 408-byte function, with
ordered fixups `[389,359,345,331,254,33]` rather than original
`[395,365,351,337,254,33]`. Five further genuinely source-level attempts
replaced only the Extra and/or last-stage *original near all-clear call* with
Turbo C++ inline `asm { call stage_allclear_bonus; }`, preserving the same
zero-argument near-Pascal side effect. Turbo C++ 4.02 rejected those function
operands with `Invalid combination of opcode and operands`; no compiling
alternate was produced. This disproves the simplistic direct inline-ASM
fallback without deriving an original symbol-level assembler operand.

Trial inputs and compiler error logs live in
`.analysis/gpt-web-defeat-inline-*-a/` with source copies
`.analysis/gpt-web-defeat-inline-*.cpp`. No compiler barrier, target byte,
relocation reordering, fake state mutation or change to already accepted six
Boss helpers was added. The natural duplicated all-clear behavior is still
correct but gets merged by Turbo C++; further work must reconstruct original
branch lowering or a genuine original assembler-language source interface.

## 2026-11-10: exact 414-byte Boss defeat C++ state machine

The original `boss_defeat_update(unsigned int)` now has a complete, accepted
natural C++ source owner `main-boss-defeat-update-complete` at
`[1FBB1,1FD4F)`. All **414/414 raw bytes**, original literal six-site
ordered relocation stream `[395,365,351,337,254,33]`, near-Pascal parameter
frame, original branch/call structure and full MAP/OMF boundaries match in
two fresh Borland/TLINK producers. The meaningful compiled negative reverses
the Extra Stage bonus selection and is rejected. The previously accepted six
352-byte Boss helpers and 10-byte item-drop DATA initializer were refreshed
in the same focused replay and remain strictly exact; they add no new bytes.

The final six-byte codegen gap arose because Turbo C++ was merging two real
`stage_allclear_bonus()` call exits in its common tail. The pinned ReC98
`th04/main/boss/boss.cpp` **actually** contains a call to
`optimization_barrier()` immediately after the **Extra Stage branch's**
all-clear reward; `decomp.hpp` implements this as an empty inlined function
returning `false`. Restoring exactly that authentic source-level statement
prevents the common-tail merger and naturally generates both distinct
original near calls and intervening jumps. Neither the barrier nor its inline
body emits a NOP, instruction template, stub, fake state mutation or source
DATA. Putting the same call at the last-stage exit, before the reward or in
other branches did not work; the original position is causally necessary.

The independent source-owned `BOSS_DEFEAT_TEXT` now has its genuine 414-byte
function extent, so the old six-byte source-free `BOSS_COLLISION_TEXT` bridge
was removed from the binder rather than credited. The following ordinary
collision C++ candidate still generates 46 versus the native complete 43;
its offset remains correctly anchored at original `1FD4F`, and it remains
**unaccepted**. There is no overlapping or partial acceptance.

Focused receipt:
`.analysis/unit-replays/gpt-web-main-boss-defeat-414-and-neighbors-20261110/receipt.json`.
The two accepted comparison rounds have unchanged original code and fixups;
all three selected negative-controlled real units passed. The 414 new
instruction bytes are counted only once as C++ CODE, and no packed-file or
whole-game completeness is implied. Earlier 408/411/414-but-wrong diagnostic
variants remain historical evidence superseded by this accepted source.
