# EX-Alice charge and initial patterns

Three complete functions fill original MAIN `1989B..199D5`: the 72-byte
charge wrapper, 86-byte random fan and 156-byte alternating turning rings.
Their 108 instructions own no padding, switch tables, initialized DATA or
BSS. Every direct branch lands at an observed instruction boundary and all
three complete returns were reviewed in the pinned original. Per-function
ordered fixups are `[36]`, `[67]`, `[127]`; the full original stream is
`[285,139,36]`, without sorting or normalization.

The wrapper charges with the real gather colors `(frame-48,6,7)`, advances
the sprite at 48, then calls the genuine near bool callback after frame 64.
Completion resets frame and mode. The random fan varies speed and quantized
angle, emits five aimed bullets, and finishes at 128. The ring pattern
alternates ordinary and aimed-turning bullets, rotates in the selected
direction, and starts random movement after frame 100.

Boss, motion and BulletTemplate use the unchanged full canonical definitions.
The complete two-alternative `BulletSpecialState` union matches the accepted
bullet updater's ODR definition. Its broader header cannot be included with
Boss movement because the independent HUD surface also defines `to_sp()`;
the initial compile exposed this integration conflict. No shared header was
changed. The foreign callback pointer, union and state arrays have no supplied
contents and receive no ownership credit.

All near calls and callback addresses belong to frame 1527. Sound is far
Pascal at 14AB:0232, and DS is 209D. The symbol-only binder supplies actual
foreign coordinates and the outside paragraph tail after 199E0. It supplies
no instructions, state values, stack or hole inside the complete owner.
ReC98 `th05_main.asm` lines 17646..17794 provides semantic evidence. Cached
calibration matches all three instruction shapes, supplying routing evidence
only; original boundaries, operands and relocations were checked separately.

`main-exalice-initial-patterns-b` had the full 314 bytes and correct ordered
fixups, with only two gather color bytes reversed. Correcting the actual
arguments to `(frame-48,6,7)` produces `main-exalice-initial-patterns-c`: two
fresh deterministic full raw/ordered positives and a rejected fan spread
count 5→6 mutation. All three functions and 314 instruction bytes are accepted.


## 2026-11-13: Ready-time direction seed

The Ready transition seeds Boss byte 15 with zero. The first wave's pattern
pair is random fan followed by turning rings: random fan does not access this
byte, while turning rings toggles the seed at frame 64 and then uses it as its
rotation direction. The next wave's diamond-ring callback toggles the same
physical byte again. The shared `ExAlicePatternByte15` union now calls the
Ready view `ready_direction_seed`, not an initial-fan substate. The byte's
size and offset are unchanged; the complete 314-byte initial-pattern owner
remains byte/fixup exact.
