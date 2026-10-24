# Stage-two midboss update candidate

This owner recovers the ordinary state machine of the original TH05 MAIN
callback at **1527:0B7B**, load **15DEB..15F74**, **393 bytes / one function**.
The original stage-setup callback at load14614 supplies the far pointer; its
native target was independently decoded. All 113 instructions cover the entire
extent, both RETF paths are present, and all 13 local branch targets are actual
instruction starts. There are no CODE tables, padding, owned DATA or BSS.
Original ordered relative loader fixups are **350,241,210**.

ReC98 `b6ba5b0a529edbb31efdf8c0e939263804f8ee47` still represents this
routine as `@midboss2_update$qv` in `th05_main.asm`. The source here expresses
its phase, timeouts, shot damage, rewards, movement and defeat behavior in
natural C++. The genuine common hit/damage wrapper is described in
`th04/main/midboss/midboss.hpp`; it stores the returned damage byte before
subtracting it from signed HP. No instruction body, register loop, flags test,
byte array, fake helper implementation or artificial side effect is imported.
The initial packet was uncompiled; retained producer observations are recorded
below.

The complete accepted22-byte midboss,24-byte Boss and14-byte BulletTemplate
layouts are reused. The orbit center is an actual separate4-byte point at
DS:3726, used by the original movement helper; its descriptive recovered name
is local to this packet. State bytes14/15 retain the real16-byte Boss state
array at DS:C682. Other foreign globals are homing_target3F8A,
bullet_zap3F96, bullet_clear_time3F97, bullet_template577E and midboss5AA4.
All game state is external and the symbol-only context supplies no values.

Phase0 moves while invulnerable and transitions at256 frames. Phase1 runs the
original pattern and orbit helpers, takes real shot damage, and transitions at
1000 frames or HP<=400; only the HP path grants5 bonus units and bullet clear.
The transition changes the real sprite to206, emits32 sparks at4 pixels, plays
SE15, and computes velocity toward (192,64). Phase2 uses its actual separate
pattern, movement and shot damage; before800 frames, HP defeat grants15 units,
activates bullet zap and adds the genuine bomb item. Both defeat paths enter
phase254/sprite4 and emit48 sparks at8 pixels with SE12. Default delegates to
the real defeat updater and returns after HP rendering; live phases additionally
publish the current homing point. Total HP is1400.

Foreign near helpers are independently anchored in the real1527 group:

| Interface | Load destination |
| --- | --- |
| `PlayfieldMotion::update_seg3()` | 1527C |
| orbit movement / first pattern / final pattern | 15CC1 / 15D43 / 15DB8 |
| circle sparks | 16EE8 |
| HP update / bonus / defeat updater | 1C4F6 / 1C54E / 1C628 |
| item addition / shot damage | 1CC2B / 1FA90 |

The three stage-specific helpers take no arguments and return near, as verified
from their complete native bodies and call sites; they remain uncredited and
external. The damage target must be interpreted in16-bit CS coordinates:
Capstone's linear displayFA90 wraps to actual1527:A820 =1FA90. Sound and vector
construction are genuine far Pascal calls at14AB:0232 and14AB:004E. The vector
API retains two far reference outputs under the genuine large-model ABI.

`probes/units/midboss_stage2_bindings.asm` anchors SHARED and the real main03
prefix, then reserves the source slot entirely for the compiler contribution.
A separate PARA context begins at15F80 for the original393-byte end, and labels
later foreign near helpers before the real DS209D boundary. Every ORG is below
64KiB. No gap is credited or inserted inside the function. Actual MAP size and
all frames must be reviewed before any exact claim; a sufficiently changed
natural producer can move the paragraph context and remains inexact.

Private `.analysis/midboss-stage2-boundary-review.json` records complete native
branches, calls, globals and ordered fixups. `.analysis/midboss-stage2-candidate.json`
contains a proposed whole-contribution entry and a meaningful compiled negative
changing only the HP transition threshold from400 to401. The preparation agent performed only native static checks. Actual compiler
observations below grant no acceptance or authored credit.


## Retained native producer observations

`main-midboss-stage2-a` reached linking and failed only because the symbol-only
scaffold used mixed case for the Pascal sparks public. The actual compiler
EXTDEF is `@SPARKS_ADD_CIRCLE$Q20%SUBPIXELBASE$TI$TI%T1II`; the context was
corrected to that real spelling without changing ABI or helper code.

The first positive producer of `main-midboss-stage2-b` linked a complete
395-byte contribution instead of393. The size gate stopped before another
positive compile. Native instruction alignment identifies exactly one added
instruction: `EB00` at15E98 after the packet's inline bullet-clear function.
The original falls through there. ReC98 and the existing generic Boss owner
express this operation as an ordinary statement macro; introducing an inline
function also introduced a return boundary. Root restored the ordinary
conditional assignment at its call site and removed the unused inline helper.

The same native comparison found a separate genuine source error: the packed
Pascal argument push is original `0C000400` versus candidate `04000C00`.
Because Pascal pushes arguments left to right, the original vector target is
(192,64), and the packet had reversed those two coordinates. Root corrected
this gameplay value. The original ordered fixups350,241,210 had all moved by
exactly2 in the395-byte producer. All other aligned instruction mnemonics and
operands agree after local branch displacement operands are excluded, including
all actual foreign near/far targets and DS state operands. This alignment is
for diagnosis only; it is not the raw or ordered-fixup oracle.

`.analysis/midboss-stage2-b-forensic.json` pins the retained MZ/MAP hashes,
records the two concrete instruction differences and keeps both fixup lists
in their original order. The source corrections are independently justified
by real control semantics and argument order, without flags, barriers or
instruction forcing. `main-midboss-stage2-c` is the subsequent focused replay.


## Accepted complete callback

`main-midboss-stage2-c/receipt.json` passes both independent cold producers for
the complete393-byte callback. Full raw bytes and original ordered fixups
350,241,210 agree in both rounds. The compiled HP-threshold negative400→401
changes real code bytes and is rejected while preserving the same fixup list.
The ledger accepts `main-midboss-stage2-update`: one complete function,
393 instruction/authored-code bytes, zero CODE tables or padding, and no owned
DATA/BSS credit. The two source corrections above are retained explicitly;
no target bytes, fixup reordering or artificial branch/padding was introduced.
