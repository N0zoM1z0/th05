Remaining small MAIN natural C++ candidates
==========================================

These six owners adapt natural nmlgc/ReC98 source at
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`, with the maintained TH04
slowdown, tile rendering, scroll conversion, player-position, and HUD score
implementations consulted for semantic reuse. Donor acceptance never
transfers. The cached surveys only route investigation; every interval below
was independently checked against complete original TH05 instructions and
return boundaries. No build or reconstruction acceptance is performed here.

| Owner/source | Original interval | Functions | Instruction bytes |
|---|---|---:|---:|
| runtime/slowdown.cpp | AE1E..AE38 | 1 | 26 |
| hud/hp.cpp | 1C4F6..1C54E | 1 | 88 |
| player/position.cpp | CAD2..CB0A | 1 | 56 |
| bullet/patnum.cpp | 16F52..16F6F | 1 | 29 |
| scroll/convert.cpp | 16A30..16A79 | 2 | 73 |
| tile/render.cpp | BD4E..BDAD | 4 | 95 |

Total candidate coverage is367 instruction bytes in ten complete functions,
with no semantic tables or owned padding. All source-owned initialized DATA
and BSS sizes are zero. There is one original segment fixup, in the HP
renderer call, and no segment fixups in the other five intervals. All real
branch destinations and external calls are recorded in the private packet.
No accepted/shared source header is edited. The new local scalar surface
`small.hpp` reuses the canonical player/motion and resident definitions;
its new `small_to_sp` helper has internal linkage rather than introducing a
different definition of an existing shared inline function.

Slowdown uses the real volatile unsigned-word VSync count and unsigned-word
delay factor. It waits for the configured number of events, clears the count,
and resets the delay factor to one. It is a near-cdecl function in
SLOWDOWN_TEXT/main_01, module `th04/slowdown.cpp`. A natural negative changes
the reset factor from1 to2. Both referenced objects remain foreign.

HP interpolation is near-Pascal, taking two signed words and returning void,
in HUD_HP_TEXT/main_03, module `th04/hud_hp.cpp`. It preserves the full signed
long multiply/divide, 128-unit bar, one-unit rising animation, immediate
falling update, and the genuine far-Pascal low-level renderer at0AE1:247B.
Its only state is the foreign word at DS1A5E. The negative changes the rising
step from1 to2. This is the natural GAME5 version of
`th04/main/hud/hp.cpp`, also present in the maintained TH04 midboss donor.

Player-position clamping preserves the actual PlayfieldPoint return type of
`PlayfieldMotion::update_seg1`, full12-byte motion storage, original DX:AX
consumer, signed comparisons, and subpixel margins. It is near-cdecl in
PLAYER_P_TEXT/main_01, module `th04/player_p.cpp`. The method remains an
external near call at0AE1:100A; no helper body is supplied. The negative changes
the real bottom margin from16 to24 pixels. DOS register intrinsics are used
as in the natural source, without assembly or a false void/integer method ABI.

Bullet pattern selection preserves the genuine byte return despite its
word-sized calculation, two word-sized stack slots, near-Pascal cleanup,
real SP/SS parameter access via DOS intrinsics, and distinction between
180-degree and360-degree sprite domains. Full word sprite-domain bounds are
retained. It is BULLET_P_TEXT/main_03, module `th05/bullet_p.cpp`, using -k-.
The negative changes the half-sprite angular offset from3 to4. The survey's
30th byte at16F6F is an explicit trailing reference NOP, outside the complete
29-byte function; it is omitted rather than counted or manufactured.

Scroll conversion preserves two genuine signed near-Pascal functions, with
word argument/result, -k-/-G, actual SP/SS stack access, Q12.4 shift, optional
or unconditional scroll addition, and one-step signed400-line wrap. The
40-byte conditional function ends at16A58; the33-byte unconditional one ends
at16A79. Both are SCROLLY3_TEXT/main_03, module `th04/scrolly3.cpp`.
The negative reverses the conditional scroll addition. The trailing NOP at
16A79 is excluded; the producer source does not import a codestring byte.

Tile rendering takes the complete natural suffix of
`th04/main/tile/tile.cpp`, in TILE_TEXT/main_01, module `th04/tile.cpp`:
tiles_render40, the real static timed renderer25, tiles_activate11, and the
far-Pascal activation-with-duration function19. The main renderer invalidates
the actual ten subsystems before redrawing; stage and midboss invalidators
are real two-byte near-Pascal callback objects. The activation wrapper is
genuinely far-cdecl, while duration activation is far-Pascal with one word
stack slot for its byte parameter. Existing callback types, foreign timer,
and real near helper targets are retained. The negative decrements the timer
by2 instead of1. No callback table or gameplay state is defined.

The preceding reset helper `[BD24,BD37)` and invalidate helper
`[BD38,BD4E)` use explicit REP STOSD register/emitted assembly. They remain
foreign and receive no pure C++ credit. The NOP atBD37 is also foreign.
No fake memset substitute, transcribed helper body, or byte array is supplied.

Private integration packet: `.analysis/main-small-natural-boundary-review.json`
and the six corresponding `.analysis/main-small-bindings/*.asm` files.
They identify the actual modules, segments/groups, original DS209D operands,
full function returns, per-owner natural negative, source options, and
ordered relocations. Each context is address-only: no instructions, global
values, assets, source-owned state, or `.stack`. The main_01 context includes
the low-level HP renderer's actual first-declaration frame independently of
the caller's main_03 frame. Source is ASCII-compatible UTF-8 and uses the
normal optimized Borland large-model GAME5 MAIN flags plus the explicit
per-source options noted above.

Two fresh focused producers, full raw-byte and ordered-fixup agreement,
OMF integrity, and compiled negative rejection remain necessary. Unknown
ownership and the excluded helpers/NOPs remain outside this candidate's
authored numerator; this packet establishes no standalone executable layout.

Additional midboss invalidation and boss backdrop owners
--------------------------------------------------------

Two independently reviewed neighbors add90 instruction bytes and two complete
functions: `midboss/invalidate.cpp` at `[109BD,109F0)`,51 bytes,
MB_INV_TEXT/main_01 (`th04/mb_inv.cpp`); `boss/backdrop.cpp` at
`[109F0,10A17)`,39 bytes, BOSS_BD_TEXT/main_01 (`th04/boss_bd.cpp`).
These are background tile invalidation and backdrop rendering, respectively;
they are not shot invincibility or boss-bound calculations. They were absent
from the accepted midboss state/generic-boss extents and do not overlap them.
The maintained TH04 natural invalidation/backdrop algorithms were consulted,
then the actual TH05 instructions and complete RET boundaries checked anew.

Midboss invalidation reuses the complete canonical22-byte midboss and4-byte
point_t. It invalidates the previous64x64 sprite while phase<254, otherwise
an expanded128x128 kill-animation area around the current position. The
foreign tile helper is declared with the same genuine two-word Pascal y/x
ABI as the accepted overlay source. Explicit real point fields replace the
reference's alternate SPPoint-by-value declaration, whose stack representation
is those same four bytes; no conflicting helper signature or substitute body
is introduced. Its foreign globals are tile_invalidate_box at DS3502 and
midboss at DS5AA4. A meaningful negative expands the normal width by8 pixels.

Backdrop rendering preserves two signed coordinate words, a real byte color
in a word stack slot, near-Pascal RET6, the far CDG call at14AB:01C0, real
GRCG mode/direct-color near helpers at0AE1:13EE/13F4, AH color contract,
actual near-Pascal fill callback at DS4446, and the genuine outportb primitive.
Its only segment relocation is the far CDG call. The negative changes the
selected CDG slot from16 to17. No helper opcode bodies or asset values are
provided. All accepted physical/interface headers are reused read-only.

The extra private packet is `.analysis/main-small-extra-boundary-review.json`,
with two more address-only binders beside the original six. These sources
also own zero DATA/BSS and require fresh focused producers and normal exact
checks. Combined preparation is eight owners, twelve complete functions and
457 instruction bytes, with two original far segment fixups total. All
excluded REPSTOSD functions and three NOP bytes remain uncredited.

Accepted focused replays
------------------------

All eight reviewed owners now pass independent cold producers, complete raw
comparison, original ordered fixups and their real compiled mutation controls.
The first six use their `-a` receipt directories; midboss invalidation uses
`main-midboss-invalidate-b` and Boss backdrop uses `main-boss-backdrop-c`. Total:
12 complete functions / 457 instruction bytes, no owned initialized DATA/BSS.
The scroll macro's unused expression and self-assignment were removed before
its first build; its real SS:SP argument protocol and semantic wrap remain.

Two compiler interface collisions were resolved locally: invalidation retains
the canonical full point layout without combining unrelated `to_sp` helper
definitions; backdrop declares the actual near Pascal color callback alongside
the existing graphics interface without duplicate producer-local phase values.
The foreign shared segment has an explicit CS assumption. No accepted shared
header or algorithm was changed. Tile's two assembly fill helpers and all three
reviewed outside-function NOP bytes remain uncredited.
