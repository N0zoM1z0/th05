# Cheeto allocation and update reconstruction

Natural C++ provenance: nmlgc/ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`,
`th05/main/bullet/cheeto_u.cpp`, `th05/main/bullet/cheeto.hpp`,
`th04/main/custom.hpp`, `th01/math/overlap.hpp` and the playfield macros.
The maintained source preserves the original `-G` setting, seven-entity loops, trail
shift order, wrapped byte speeds, angle-snapping algorithm and inclusive
unsigned collision tests. No ASM, emitted instructions, fake helpers or asset
arrays are used.

## Original code and frame

Pinned MAIN SHA-256:
`c41f6e6b9a97b2433acc576ceaee800707c8d4ea7e498150a259663c8fa7d4f0`.
Original load-module range **`[1A82E,1AA7E)`**, **592 bytes**, SHA-256
`fa5f7b4e3527a5a024b7c2953adbe32a302702ada73fa9d224ab2ff765198063`.
Add the 4032-byte MZ header for file offsets.

| Function | Half-open load span | Bytes |
| --- | --- | ---: |
| `cheetos_add` | `1A82E..1A8CD` | 159 |
| `cheetos_update` | `1A8CD..1AA7E` | 433 |

All 216 instructions decode contiguously through the two terminal returns.
All 31 local jump targets are instruction starts. No embedded CODE-data,
switch tables, padding or MZ relocation words occur in this extent. Candidate
opcode IDs and widths corroborate routing, but are not an exact oracle.

Wrapper `th05/cheeto_u.cpp` should include `src/main/bullet/cheeto.cpp`.
Use established MAIN flags and the owner's retained `-G`, segment
`CHEETO_U_TEXT`, group `main_03`. Original frame **`1527`**, load base
**`15270`**, contribution group offset **`55BE`**; DGROUP frame **`209D`**.

## Complete state ABI

The header represents all fields of the genuine 26-byte `custom_t` slot,
26-byte Cheeto head, 25-byte template overlay and 82-byte trail. Every field
offset and complete size is asserted, including unused members and the actual
scalar byte at slot offset 25. The template's unused six-word member is the
original overlay of previous position, velocity and two custom value words;
it is not a fabricated spacer inserted to reach used offsets. Its ordinary
trailing alignment is not counted as reconstructed code.

| Layout | Real field offsets |
| --- | --- |
| `custom_t` | flag 0, angle 1, motion 2, val1 14, val2 16, sprite 18, val3 20, damage 22, speed 24, unused byte 25 |
| `cheeto_head_t` | flag 0, angle 1, motion 2, age 14, unused word 16, sprite 18, unused long 20, speed 24, unused byte 25 |
| `cheeto_template_t` | unused flag 0, angle 1, origin 2, unused six words 6, color word 18, unused long 20, speed 24 |
| `cheeto_trail_t` | flag 0, color byte 1, 16 PlayfieldPoint nodes 2, 16 sprite bytes 66 |

The target uses a `1A`-byte head stride and `52`-byte trail stride. The template
is custom slot zero, and the seven heads begin at custom slot one. The real
trail declaration has eight elements even though these update loops use seven;
it is preserved. Unused field types/names are reference-corroborated full
layout declarations; the original code independently checks touched offsets,
copy widths, byte operations and complete entity strides.

The accepted player/geometry declarations remain unchanged. In particular,
`PlayfieldMotion::update_seg3()` returns the real **PlayfieldPoint**, not void
or a fabricated packed integer. The original helper at `1527C` takes a near
`this` on the stack, updates real current/previous coordinates, returns X in
AX and Y in DX, then executes `RET 2`. The owner retains the original register
collision expression immediately after that call and obtains `_AX`/`_DX` from
the genuine `<dos.h>` declarations.

## External observations

All four callees are near inside the original main_03 frame.

| Original EXTDEF | Load destination | Group offset | ABI |
| --- | --- | --- | --- |
| `VECTOR2_NEAR` | `152DA` | `006A` | C Pascal, SPPoint near reference, byte angle promoted to word, signed length word |
| `@BULLET_PATNUM_FOR_ANGLE$QUIUC` | `16F52` | `1CE2` | C++ Pascal; unsigned base word and byte angle; byte return |
| `@PlayfieldMotion@update_seg3$qv` | `1527C` | `000C` | existing near Pascal member; real PlayfieldPoint return |
| `@PLAYER_ANGLE_FROM$Q20%SUBPIXELBASE$TI$TI%T1UC` | `171CC` | `1F5C` | existing near Pascal; two real Subpixel values plus byte angle, byte return |

| Global | DGROUP offset | Full declared size |
| --- | --- | ---: |
| `custom_entities` | `B3F4` | 1664 = 64 real custom slots |
| `cheeto_trails` | `C0AA` | 656 = 8 real trails |
| `player_pos` | `36D2` | 12 |
| `player_is_hit` | `36F3` | 1 |
| `stage_frame_mod2` | `5766` | 1 |

Original absolute operands establish the template and scalar global locations;
the head pointer immediate is `B40E` (custom base +26), and trail pointer
immediates are `C0AA`. Private `.analysis/cheeto-update-boundary-review.json`
retains all corresponding sites, function extents and target identity. These
bindings do not establish ownership of those external data bytes or helpers.

A natural negative control changes the unique
`HEAD_KILLBOX_W = TO_SP(16)` to `TO_SP(15)`, changing the real horizontal head
collision extent. Two fresh producers in `.analysis/unit-replays/cheeto-update-b` pass full raw
bytes, ordered fixup lists (empty here), normalized OMF determinism and actual
compiler dependency checks. The compiled head-collision-width mutation is
rejected. Acceptance independently rechecks the saved artifacts; no unchanged
unit is rebuilt and tool execution probes are reused after identity checks.
This remains bounded contribution acceptance rather than whole-game linkage.
