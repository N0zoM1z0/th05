# Louise complete update callback

The accepted stage-setup far pointer at **1467C** identifies MAIN
**1527:8AD0**, load **1DD40..1DF86**, **582 bytes / one complete function**.
Native decoding covers166 instructions/565 bytes through the real RETF at
1DF74. It is followed by one original zero at1DF75 and the complete eight-word
compiler switch table at1DF76..1DF86. All39 direct branches and all eight table
entries land on actual instruction starts. The next function begins1DF86.
Original ordered relative MZ fixups are **[121]**, the genuine far sound call.
Classification is581 authored-code bytes:565 instructions plus16 compiler-table
bytes, excluding the one zero. No byte is supplied by the symbol context.

ReC98 `b6ba5b0a529edbb31efdf8c0e939263804f8ee47` retains the routine as
`@louise_update$qv` in `th05_main.asm`. This source recovers its eight phases
and two three-mode pattern dispatches in ordinary C++, using the frozen
accepted Louise initial/later interfaces and full canonical Boss24,
BulletTemplate14, gather14, resident and generic Boss interfaces. All existing
accepted source/header files remain unchanged. No ASM, opcode templates,
pseudo-register operations, flags interface or inert barrier is introduced.

Each frame publishes the actual homing position, increments the phase timer,
sets normal bullet spawning and copies the Boss position to bullet/gather
origins. Phase0 initializes4400 HP, the3000 HP boundary and gathering geometry;
after128 invulnerable frames it starts SE13 and assigns the real Louise
background callback. Phase1 waits64 more invulnerable frames and initializes
the initial alternating blue/red mode, count and speed/direction state.
Phase2 alternates real movement and the two accepted initial patterns. Movement
completion selects the next mode, and20 completed cycles advance regardless
of collision; otherwise a real shot hit grants10 bonus units before advancing
to the1900 HP boundary with the actual NW/SE explosion.

Phase3 waits64 collision-active frames before advancing the visual state.
Phase4 runs the accepted mirrored fan while moving, ends after20 cycles or a
rewarded shot hit, and transitions to the500 HP boundary with SW/NE explosion,
resetting later-pattern selection and speed state. Phase5 alternates movement
with the accepted sweeping-laser and turning-ring patterns; its20-cycle/hit
transition uses NW/SE explosion and the0 HP boundary. Phase6 performs the same
64-frame visual wait. Phase7 runs the accepted final aimed pellets during
movement;10 completed cycles select defeat without reward, while a shot hit
sets the genuine defeat-bonus flag. Both enter the real small-explosion phase.
Other phases call the actual generic defeat updater with10 bonus units. All
paths render current HP against4400. Counter/bonus uses the complete canonical
Boss union rather than a shortened state layout.

The movement helper is a real complete foreign function at1D8BE..1D938,
Pascal RET4, signed speed word atBP+6, signed end-frame atBP+4 and truth inAL.
Its four actual calls pass (16,96), (14,128), (48,48) and (8,128) in Pascal
left-to-right order, corresponding to speeds1/0.875/3/0.5 pixels. This interface
is observed directly from both callee and callers, not a synthetic flags API.
The accepted initial/later pattern functions remain foreign near calls at
1D99A/1DA5A/1DAE5/1DBC3/1DC62/1DCE8. Generic near helpers retain1527:
HP1C4F6, bonus1C5B8, hit1FAD0, invulnerable hit1FAFA, phase-next1FB61 and
defeat1FBB1. Foreign implementation byte ownership is not transferred.

The assigned background function is genuine Pascal near0AE1:5C6F, load10A7F;
it is first declared in main_01 before the shared stage surface repeats it.
Its two-byte pointer is at DS350A. Sound is genuine C Pascal far14AB:0232.
Other state is homing_target3F8A(4), bullet_template577E(14), boss5ABA(24),
gather_template9EA6(14) and boss_statebyteC682(16). No DATA/BSS is defined.

The original even word table motivates ordinary `-a2` only after all complete
ABI declarations; there is no source padding. The symbol-only binder merges
actual empty foreign segments at their real main_01/main03 contexts, leaves
the complete source contribution to the compiler and starts a separate
paragraph at1DF90 after original full end1DF86 to anchor DS209D. It supplies
only addresses and external holes, with no initialized values, helper code,
inside-function holes or `.stack`; every ORG is below64KiB.

`.analysis/louise-update-boundary-review.json` pins original hashes and all
branches, calls, returns, table destinations, padding and true globals.
`.analysis/louise-update-candidate.json` proposes valid DOS8.3 module
`th05/louiseu.cpp`, B4_UPDATE_TEXT/main_03 and the meaningful compiled negative
changing the initial HP boundary3000→3001. Native closure, classification and
unique-mutation checks pass. Preparation ran no compiler or Wine. Actual two
cold producers, full raw/ordered comparison and rejected compiled negative
remain required before authored acceptance.


`main-louise-update-a/receipt.json` accepts the complete582-byte callback,
including the original zero and all sixteen compiler-table bytes. Both fresh
deterministic producers reproduce the raw extent and sole ordered relocation
at relative121. The phase-end HP3000→3001 compiled control is rejected.
Credit is one complete function and581 authored bytes (565 instructions plus
16 compiler-table bytes); the original padding byte is checked and excluded.
No previously accepted helper source or header was changed.

The eight original switch states and both three-mode pattern dispatches now
use named phase/mode constants, preserving the numeric state machine.

## Recovered shared charge-state layout

The Louise updater and both pattern source files now use the same typed
`LouiseScratch` view of the original 16-byte `boss_statebyte` array. Its
byte-10 speed starts at `0x18` before blue spreads, increases during the
first charged attacks, and is explicitly reinitialized to `0x14` before the
later turning-ring pattern. Byte 14 selects the alternating second-wave
sweeping-laser and turning-ring modes; the updater resets it at the fan-to-
second-wave transition. Byte 15 is a first-wave alternating spread direction,
then later overwritten by the sweeping-laser's randomized direction.
These are aliases with phase-specific lifetimes, not independent fields or
new allocations. Size and offset assertions protect the original physical
layout without changing the binary ABI.

A focused Borland replay of all three edited source units—`main-louise-update`
(582 bytes), `main-louise-initial-patterns` (429 bytes) and
`main-louise-later-patterns` (603 bytes)—exactly matches all 1,614 original
bytes and ordered relocations in two deterministic builds. The genuine
compiled semantic negative is rejected. Accepted local evidence:
`.analysis/unit-replays/gpt-web-louise-scratch-20261111/receipt.json`.
There is no new authored-byte credit, because all three functions already had
accepted exact owners.

## Eight-phase Louise choreography, HP transitions and alternating modes (2026-11-12)

The actual 582-byte far-Pascal Louise Boss controller now explicitly names
its complete HP ladder **4,400 → 3,000 → 1,900 → 500 → 0**, instead of
mixing the next-phase HP values into unnamed call literals. The original
phase-next calls still install those exact *end* thresholds; no HP is
implicitly subtracted from the current Boss state. The named independent
clocks distinguish the 128-frame HP filling, 64-frame ready wait, both
64-frame fire transitions, and 96/128/48/128-frame movement intervals.
The first three attack waves terminate after 20 completed patterns, while
the final aimed-pellet cycle terminates after ten. Hit and timeout
transitions preserve their original different defeat-bonus semantics.

The two three-mode dispatches now name their actual relationship to the
shared 16-byte Louise scratch object: the first selects alternating blue
spreads and red stacks via parity, while the later wave toggles between
sweeping lasers and turning rings. Charge-speed scratch initialization
remains `0x18` for the first wave and `0x14` for the later wave. The
0/1 alternation is an actual selector state, not a new field or prebuilt
function table. The original gather geometry, entrance sound, pattern
score bonus and final defeat bonus have explicit source-level names. No
additional storage, branch calls, artificial compiler operations or
replacement graphics resources are introduced.

The modified natural source uses `phase_choreography.hpp`, which encodes
compile-time thresholds only. Both independent Borland producers in
`.analysis/unit-replays/gpt-web-louise-phases-a/receipt.json` match the
whole **582-byte** source contribution, including the genuine one-byte
alignment, 16-byte compiler switch table and original ordered far sound
relocation. The compiled HP-gate mutation from 3,000 to 3,001 was
rejected. Already accepted Louise CODE is not credited a second time;
no full MAIN or unrelated cold replay was performed.

## Two fire-break phases and three regular hit gates

The complete 582-byte Louise controller now shares the original two 64-frame
fire-break transitions through `LOUISE_FINISH_FIRE_TRANSITION()`, preserving
each phase's preceding hit test and its own unchanged state. The three
regular attack waves also share `LOUISE_HIT_BONUS_OR_BREAK()`: a missed shot
breaks directly out of the original Boss phase switch, while a successful
shot awards the same bonus before the existing phase transition.

Both Turbo C++/TLINK producers match all 582 original bytes, the real switch
table and original ordered relocation `[121]`. The compiled HP-boundary
negative was rejected. Evidence:
`.analysis/unit-replays/gpt-web-louise-shared-fire-hits-20261112-a/receipt.json`.
The accepted code receives no duplicate authored-byte credit.

## 2026-11-13: shared mode domain and cross-pattern scratch lifetimes

The Boss `mode` byte has one shared numeric protocol across the two three-way
attack phases: `0` is reposition, `1` is the active blue-spread / sweeping-
laser callback, and `2` is the active red-stack / turning-ring callback. The
phase determines which callback owns modes 1 and 2; they are not six distinct
Boss states. Both first-phase charged callbacks and both later charged
callbacks return to the same reposition value. The compile-time mode constants
now live beside the shared charge/pattern declarations, with assertions that
the two pairs intentionally share values.

The 16-byte Louise scratch view now names the actual sequential lifetimes of
its final two bytes. Byte 14 (`next_laser_ring_mode`) is initialized to zero
when mirrored fans end, selects laser mode 1 on the next reposition, toggles
to ring mode 2, and continues alternating until the 20-pattern phase ends.
Byte 15 (`blue_red_or_laser_direction`) is initialized to zero at Ready;
each blue-spread initialization toggles it, the red-stack pattern consumes the
same direction without resetting it, and the later sweeping-laser initializer
overwrites it with a fresh random side bit. Byte 10 remains the charge-speed
byte: it is initialized to `0x18` for the first blue wave and reinitialized to
`0x14` for the laser/ring wave. All three are views of the original
`boss_statebyte`; no new storage or transition reset is added.

The complete four-unit Louise closure was replayed twice after the rename:
429-byte initial patterns, 603-byte later patterns, 582-byte far-Pascal Boss
controller and 122-byte flystep helper. Every original byte and ordered MZ
relocation matches in both Borland/TLINK producers, and the existing compiled
fan-angle negative is rejected. Receipt:
`.analysis/unit-replays/gpt-web-louise-cross-wave-byte15-byte14-final-20261113/receipt.json`.
This is a semantic refinement of already accepted owners; no duplicate CODE
credit is claimed.
