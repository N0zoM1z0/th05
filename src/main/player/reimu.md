# Reimu shot-control candidate

`reimu.cpp` adapts nmlgc/ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`, `th05/p_reimu.cpp`, into a
maintained local producer. `reimu.hpp` owns the complete 18-byte TH05 Shot and
two-byte ShotAddIterator declarations, with size/offset assertions. Existing
accepted source and shared class definitions are unchanged.

The source uses natural C++ and the compiler's AL pseudoregister. There are no
instruction-emission directives, inline ASM, synthetic linker-zero symbols or
game asset arrays. Option offsets and two direct shot offsets expand the
original Subpixel arithmetic into equivalent signed `.v` assignments in Q12.4;
the shared class is not replaced or given a different definition.

## Target extent

Pinned MAIN SHA-256:
`c41f6e6b9a97b2433acc576ceaee800707c8d4ea7e498150a259663c8fa7d4f0`.
The complete load-module extent is `[0xE6FB,0xEB92)`, **1175 bytes**, SHA-256
`3d30963c8771ea2c1f91b365a0fe6dff2c6bcb90aff20ae4f82fc994fd2f9ddd`.
All eight function boundaries end with real returns. There are no NOP
exclusions and no MZ relocation words overlapping the contribution.

| Function | Target load offset | Bytes |
| --- | --- | ---: |
| `SHOT_REIMU_L2` | `0xE6FB` | 129 |
| `SHOT_REIMU_L3` | `0xE77C` | 132 |
| `SHOT_REIMU_L4` | `0xE800` | 132 |
| `SHOT_REIMU_L5` | `0xE884` | 157 |
| `SHOT_REIMU_L6` | `0xE921` | 157 |
| `SHOT_REIMU_L7` | `0xE9BE` | 157 |
| `SHOT_REIMU_L8` | `0xEA5B` | 129 |
| `SHOT_REIMU_L9` | `0xEADC` | 182 |

These are load-module offsets; the original MZ file header is 4032 bytes.
The survey's unique masked match is a routing observation, not acceptance.
The original instructions, operand widths, call destinations and final returns
were read independently after using it to locate this complete span.

## Local ABI and bindings

Use wrapper `th05/p_reimu.cpp` including `src/main/player/reimu.cpp`, with
segment `MAIN_01_TEXT`, group `main_01`, and the established MAIN flags
`-O -b- -3 -Z -d -DGAME=5 -ml -DBINARY='M'`. The original group frame is
relative segment `0AE1` (load offset `AE10`); this contribution starts at group
offset `38EB`. All external code dependencies are near calls in that group.

| External symbol | Target load destination | Original main_01 offset | ABI |
| --- | --- | --- | --- |
| `@RANDRING1_NEXT16_AND$QUI` | `0xC70E` | `18FE` | near Pascal, unsigned-word mask |
| `@SHOT_VELOCITY_SET$QP7SPPOINTUC` | `0xE3C4` | `35B4` | near Pascal, real SPPoint near pointer and angle word slot |
| `@shots_add$qv` | `0xE38C` | `357C` | near C++, returns Shot near pointer |
| `@shot_cycle_init$qv` | `0xE644` | `3834` | near C++, returns byte in AL |

No external data symbol is referenced directly by this contribution. Numeric
destinations are observed in the target. Symbol names and semantic roles are
corroborated by candidate source and the calibration object's EXTDEF records.

The real Shot fields are flag/age at offsets 0/1, complete Motion at 2,
patnum/type/damage/angle at 14/15/16/17. Its motion velocity is at offset 10.
The original velocity setter writes a packed four-byte velocity at its passed
pointer and the shot angle at pointer+7. Thus its SPPoint pointer must actually
refer to a Shot's embedded velocity; treating it as an arbitrary standalone
point loses part of the original interface. The local declaration preserves
the actual SPPoint return type, rather than inventing a void return to alter
code generation.

The iterator deliberately initializes only its counter, leaving the angle
uninitialized until the original branches assign it. Level 5 and Level 6 retain
their separately compiled equal bodies. Neither fact is an invitation to add
new initialization or merge functions in the exact branch.

No compilation, raw exactness, helper implementation, shot-pool ownership or
whole-program layout is accepted by this packet. The new producer requires its
focused cold byte/OMF/fixup replay before credit; earlier accepted units can be
reused only with their unchanged inputs and evidence.
