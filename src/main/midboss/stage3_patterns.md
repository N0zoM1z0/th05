# Stage-three midboss movement and patterns

The original MAIN prefix is **1BA9A..1BD02**, **616 bytes / five complete
functions**, immediately before the accepted Stage3 update. Native decoding
covers every byte with 177 instructions. No return is followed by a compiler
table, zero or gap before the next function. All direct branches land on real
instruction starts inside their own function.

| Complete function | Original interval | Bytes |
| --- | --- | ---: |
| vanish/reposition/reappear animation | 1BA9A..1BB0D | 115 |
| gather charging animation | 1BB0D..1BB41 | 52 |
| spread-stack sequence | 1BB41..1BBD8 | 151 |
| aimed stack/rank spread sequence | 1BBD8..1BC77 | 159 |
| diamond spread sequence | 1BC77..1BD02 | 139 |

The complete original ordered relative loader fixups are **[546,424,405,235,144]**.
All five are genuine far call segment relocations. The following byte is the
accepted callback's PUSH BP, which is outside this owner. No DATA or BSS is
defined, and external callback tables remain external.

ReC98 `b6ba5b0a529edbb31efdf8c0e939263804f8ee47` retains these routines as
`sub_19280`, `sub_192F3`, `sub_19327`, `sub_193BE` and `sub_1945D` in
`th05_main.asm`. This owner expresses their ordinary animation, movement and
firing algorithms in C++. It includes the accepted Stage3 ABI and complete
canonical point/motion, midboss, bullet and gather declarations read-only.
Accepted sources and headers are unchanged. There is no inline ASM, emitted
opcode, pseudo-register loop, opaque target data or artificial side effect.

The movement animation ticks every four frames. On disappearing, it advances
sprites through220, keeps the last visible sprite219, moves down12 pixels,
tracks the player's actual horizontal position clamped to64..320, and marks
the return phase. Reappearing decrements sprites until212, then restores208,
clears animation state and resets the pattern timer/phase. The charge helper
calls the genuine three-stack gather operation with frame-1 and colors
**11 then10**, plays SE8 and selects sprite210 on frame1, and advances to211
on frame16. Packed Pascal PUSH000B000A confirms that color order.

All three patterns charge until32 frames and then perform real scheduled shots
at32/48/64 before repositioning from96 onward. Pattern1 uses cloud-forward
spread stacks with 3/4/7 shots, spread deltas16/5/10, four layers at delta0.5,
blue/red/blue patnums and speeds1.5/3/2. It invokes the real bullet tuning
callback before adding bullets. Pattern2 starts eight aimed stack layers at
delta0.5 and speed1.5, then adds the genuine per-rank spread settings, without
the tune callback. Its frame48 pairs are easy(1,1), normal(2,4), hard(3,3),
lunatic(4,4); frame64 pairs are (1,1)/(3,5)/(4,5)/(5,4). Packed argument pushes
were independently decoded in Pascal left-to-right order. Pattern3 uses blue
diamonds at speed3 with spread/delta16/8,21/4,16/8 and the real tune callback.
Each shot advances previous Y, moves the boss upward4 pixels and plays SE15.

The source's shared `fire` and `stack` labels express those common gameplay
actions in the same function; they do not alias target addresses or supply
instructions. Typed16/32-bit setters follow the real reference BulletTemplate
interface and the already maintained Sara implementation, combining only its
asserted adjacent semantic fields. Pattern3 deliberately assigns its two
spread fields separately, as in the original behavior. No source or compiler
flag alternatives have been tried.

The rank selector is a genuine C Pascal **far** interface at
**0AE1:21A2**, loadCFB2. It is first declared in a main_01 context before the
shared stage header repeats its signature, preserving the real call frame.
Sound is C Pascal far14AB:0232. Foreign near gather/bullet helpers are
1527:1DED / 1527:1F94, load1705D/17204. Bullet tuning is the actual two-byte
near Pascal callback at DS41DE; its body remains unimplemented here.
Other globals are player_pos DS36D2 (full12-byte motion), bullet_template577E
(14), midboss5AA4 (22) and boss_statebyteC682 (16).

The binder contains only these real labels and outside-contribution ORG gaps.
It leaves the whole source slot to the actual compiler contribution, then
uses a separate paragraph context at1BD10 after the original end1BD02 to
anchor DS209D. There are no helper bodies, initialized values, inside-function
holes or `.stack`; every ORG is below64KiB.

`.analysis/midboss-stage3-patterns-boundary-review.json` pins original hashes,
complete per-function boundaries, instructions, calls, branches and fixups.
`.analysis/midboss-stage3-patterns-candidate.json` proposes whole module
`th05/mb3pat.cpp` in B4_UPDATE_TEXT/main_03 and a meaningful compiled negative
changing the first spread from3 to4. It also records the five complete
function scopes and independent natural negatives for later review if needed.
Native closure, classification and unique-mutation checks pass. Preparation
ran no compiler or Wine; real cold raw/ordered verification and negative
rejection remain required before any authored credit.


## Accepted complete prefix

`main-midboss-stage3-patterns-a/receipt.json` passes two independent cold
producers for all five complete functions and616 raw instruction bytes. Both
rounds preserve the original ordered fixups[546,424,405,235,144]. The separately
compiled spread3→4 mutation changes actual code and is rejected. The ledger
accepts `main-midboss-stage3-patterns`: five functions,616 authored-code and
instruction bytes, no tables, padding or DATA/BSS credit. Source, ABI header
and symbol-only binder stayed frozen throughout replay.
