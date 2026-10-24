# TH05 generic boss behavior candidate

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
It never duplicates the table or stage flag. DATA remains uncredited pending
its own validation/ownership acceptance.

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
