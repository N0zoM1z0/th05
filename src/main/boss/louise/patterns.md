# Louise initial charging and alternating patterns

The original MAIN owner is **1D938..1DAE5**, **429 bytes / three complete
functions**. The accepted stage-setup callback at1467C identifies Louise's
real update at1DD40. Its calls at1DE30/1DE35 identify these two initial attack
patterns; both call the shared charging function immediately before them.
Native decoding covers all429 bytes with148 instructions, and every direct
branch lands on a real instruction start within its function. No RET is
followed by a compiler table, zero or gap before the next function.

| Complete function | Original interval | Bytes |
| --- | --- | ---: |
| charging state update | 1D938..1D99A | 98 |
| paired blue spreads | 1D99A..1DA5A | 192 |
| rotating red stacks | 1DA5A..1DAE5 | 139 |

The original ordered relative loader fixups are **[407,352,196,50]**. They are
actual far sound/rank-call segment relocations. The following function at1DAE5
is a separate four-way pattern and remains external. No larger function was
fragmented and no padding was added to reach the selected size.

ReC98 `b6ba5b0a529edbb31efdf8c0e939263804f8ee47` still retains these functions
as `sub_18C32`, `sub_18C94` and `sub_18D54` in `th05_main.asm`. This source
recovers their ordinary animation and bullet behavior in C++, using the full
canonical24-byte Boss,14-byte BulletTemplate, gather and callback interfaces.
No accepted source/header changed. The owner contains no assembly, opcode
emissions, pseudo-register operations, optimization barriers or opaque arrays.

The shared charging function has a real signed-word duration argument,
Pascal RET2 and four distinct return values in AL. Before16 frames it returns
inactive. During16..31 it selects the charging sprite184, calls the genuine
gather operation with frame-16 and colors9 then8, and plays SE8 on frame16.
On32 it selects firing sprite188 and returns initialization; later frames
return firing while below the supplied duration and completion otherwise.
The byte enum records those actual0/1/2/3 results, with a compiler size check.
This is a complete recovered function with both actual consumers, not an
invented flags interface or shim.

The blue-spread pattern uses a64-frame duration. Initialization selects normal
blue balls, a five-shot spread with delta6 and exact-linear motion, initializes
speed from the actual state byte, toggles sweep direction and selects angle20
or60 hex. It invokes the real tuning callback and SE15, then increases the
state speed by4 up to24 hex. Initialization falls through to firing on its
even frame. Every even firing frame adds a spread, reverses angle by80 hex,
adds the opposite spread, advances angle by87 or79 hex according to direction,
and increases current speed by4. Completion restores Boss mode0, timer0 and
sprite180.

The red-stack pattern uses a96-frame duration. Initialization selects cloud
forward/no-deceleration red V bullets, speed2, the real per-rank stack count
and speed delta, and angle-40 hex. It emits from subsequent even firing frames,
turning by-8 or+8 according to the same direction and playing SE15. Completion
restores the same real state. Rank pairs are easy(10,0.3125), normal(12,0.3125),
hard(12,0.375), lunatic(14,0.375). Typed little-endian field setters follow the
reference BulletTemplate interface and existing accepted Sara convention.

Packed Pascal arguments were independently checked: gather PUSH00090008 is
first color9 then8, while the two rank pushes carry050A/050C/060C/060E in
left-to-right order. No opaque table or manually copied data is defined.
The real rank selector is far0AE1:21A2 (loadCFB2), first declared in its genuine
main_01 context before shared headers repeat the interface. Sound is C Pascal
far14AB:0232. Near gather and bullet-add are1527:1DED/1F94 (1705D/17204).
Bullet tuning is the original near Pascal callback at DS41DE. Other foreign
state is bullet_template577E(14), boss5ABA(24) and boss_statebyteC682(16).
All state and callback objects remain external; DATA/BSS credit is zero.

The symbol-only binder supplies only those actual addresses and outside-source
ORG gaps. The whole compiler contribution occupies the source slot; a separate
paragraph context starts1DAF0 after the original complete end1DAE5 and anchors
real DS209D. It has no instructions, initialized values, inside-function holes
or `.stack`. Every ORG is smaller than64KiB.

`.analysis/louise-initial-patterns-boundary-review.json` pins original hashes,
all per-function boundaries/calls/branches/returns and the complete fixup order.
`.analysis/louise-initial-patterns-candidate.json` proposes the valid DOS8.3
module `th05/louisep.cpp` in B4_UPDATE_TEXT/main_03, one whole-owner spread5→6
negative, and three optional complete-function scopes with independent natural
negatives. Native closure, classification and unique-mutation checks pass.
Preparation ran no compiler or Wine. Two real cold producers, full raw/ordered
comparison and rejected compiled negative remain required for acceptance.


Accepted in `main-louise-initial-patterns-a/receipt.json`: both independent fresh deterministic
producers reproduce all429 raw bytes and all four original ordered fixups.
The compiled blue spread5→6 mutation is rejected.
Credit is3 complete function(s) and429 authored instruction bytes;
there is no owned table, padding, DATA or BSS. No previously accepted source
or ABI header was changed to obtain this result.
