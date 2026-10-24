# Regular bullet update reconstruction

Natural-source provenance: nmlgc/ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`,
`th04/main/bullet/update.cpp` with GAME=5, wrapper `th05/bullet_u.cpp`.
The owner preserves the full pattern selection, turning, special motion,
cloud/deceleration, collision/graze, slowdown and zap algorithms. It retains
`-G` and the original `-a2` pragma after `bullet_update_patnum`.

The one handwritten reference sparks instruction macro is removed. It becomes
the true C++ Pascal far call
`sparks_add_random(Subpixel, Subpixel, subpixel_t, int)`. Its same-group original
call has NOP/PUSH CS/near CALL shape, with far-return semantics. Focused replay confirms natural linker
relaxation reproduces it. No instruction bytes, ASM, fake zero symbol,
ghost helper or optimization barrier is maintained in this owner.

Existing `template.hpp`, `geometry.hpp`, player declarations and HUD overlay
types are reused without edits. Geometry conveniences become equivalent `.v`
assignments, signed shifts and the real scrolling helper call. The true
PlayfieldPoint return of `pos.update_seg3()` and register-bound collision
expressions remain intact. The reference inline popup activation is expanded
into its two actual assignments to avoid changing an accepted HUD header.

## Independently reviewed original boundaries

Pinned MAIN SHA-256:
`c41f6e6b9a97b2433acc576ceaee800707c8d4ea7e498150a259663c8fa7d4f0`.
Original load-module range **`[1BE4E,1C4A1)`**, **1619 bytes**, SHA-256
`3e842642c097ad5b78c571318c8e24b5757ead778ce9a4be6c8ffb40fbe91809`.
Add the 4032-byte MZ header for file positions.

| Function | Original half-open span | Instructions | CODE-data |
| --- | --- | ---: | ---: |
| `bullet_update_patnum` | `1BE4E..1BE9C` | 78 | 0 |
| `bullet_turn_x` | `1BE9C..1BED4` | 56 | 0 |
| `bullet_turn_y` | `1BED4..1BF0C` | 56 | 0 |
| `bullet_update_special` | `1BF0C..1C0DF` | 447 | 20 |
| `bullets_update` | `1C0DF..1C4A1` | 962 | 0 |

Each function was routed independently by its unique diagnostic shape, then
read through its original terminal return. The complete extent contains **1599
instruction bytes / 552 instructions + 20 semantic switch-table bytes**, with
no padding. The first four helpers are near Pascal with real near references
and `RET 2`; `bullets_update` is a far C++ function ending in RETF.

The special-motion switch dispatch at `1BF24` reads ten near address words at
**`[1C0CB,1C0DF)`**, unit-relative **`[27D,291)`**. All ten point to original
instruction starts inside that function. The source retains a semantic switch;
no address array is supplied. The compiler must regenerate every table byte.
There are four original ordered MZ segment fixups. Classification never masks
the switch words, operand values or fixup positions.

## Real state and build context

The complete `bullet_t` is **32 bytes**: entity flag 0, signed age 1, real
12-byte motion 2, unused group byte 14, signed unused byte 15, current speed 16,
angle 17, spawn/move/special flags 18/19/20, final speed 21, two genuine byte
unions 22/23, pattern word 24, SPPoint origin 26, distance word 30. All union
alternatives are preserved, including the signed target angle. Every field,
enum width and complete size is asserted; no synthetic offset padding is used.

The real bullet pool has 400 entries / 12800 bytes; original reverse iteration
starts at its last slot and decrements by 32. The first 180 entries are pellets,
followed by 220 larger bullets. The full pellet render union is four bytes,
cloud render pointers are near words, and both render lists have 180 entries.
The special state and active/frame zap state remain genuine one-byte unions.

Wrapper `th05/bullet_u.cpp` should include `src/main/bullet/update.cpp`.
Use established MAIN flags, segment `BULLET_U_TEXT`, group `main_03`, retaining
the source pragmas. Original frame is **`1527`**, load base **`15270`**, unit
group offset **`6BDE`**; DGROUP frame is **`209D`**. This owner defines no data
payload; all global state is external and explicitly bound.

## Binding packet

Private `.analysis/bullet-update-boundary-review.json` retains the complete
target identity, function/table ranges, all 24 globals and operand sites,
callback destination and ordered fixups. Numeric operands come from original
bytes; calibration MAP/OMF names annotate them without transferring acceptance.

| Helper | Original destination | Actual ABI |
| --- | --- | --- |
| `@BULLET_PATNUM_FOR_ANGLE$QUIUC` | `16F52` / main_03:`1CE2` | near Pascal; unsigned base word, angle byte, byte return |
| `VECTOR2_NEAR` | `152DA` / main_03:`006A` | C near Pascal; SPPoint near reference, byte angle, signed length |
| `@PlayfieldMotion@update_seg3$qv` | `1527C` / main_03:`000C` | real near Pascal member; PlayfieldPoint in DX:AX |
| `@SPARKS_ADD_RANDOM$Q20%SUBPIXELBASE$TI$TI%T1II` | `16E86` / main_03:`1C16` | C++ far Pascal; two true Subpixel values and two signed words |
| `SCROLL_SUBPIXEL_Y_TO_VRAM_SEG3` | `16A30` / main_03:`17C0` | C near Pascal; signed Y word, signed-word return |
| `@POINTNUMS_ADD_WHITE$QIIUI` | `16E42` / main_03:`1BD2` | near Pascal; two signed coordinates, unsigned points |
| `@ITEMS_ADD$QII11ITEM_TYPE_T` | `1CC2B` / main_03:`79BB` | near Pascal; two signed coordinates, genuine signed-byte item enum |
| `IATAN2` | `0000:1F3A` | C far Pascal; two signed words, signed-word return |
| `VECTOR2_AT` | `14AB:03B0` | C far Pascal; true SPPoint near reference and four signed words |
| `@hud_graze_put$qv` | `0AE1:242E` | C++ far C order |
| `SELECT_FOR_RANK` | `0AE1:21A2` | C far Pascal; four signed words, signed-word return |

The `overlay2` callback store refers to
`@OVERLAY_POPUP_UPDATE_AND_RENDER$QV`, **`0AE1:7459`**, load `12269`.
This is a near address relative to main_01 even though this owner runs in
main_03; its frame must not be replaced with this TU's frame.

Key original DGROUP positions include the full bullets at `5F2A`, special state
`3F94`, zap/clear `3F96/3F97`, player motion `36D2`, player hit/invincibility
`36F3/36EE`, drawpoint `36FE`, cloud pointer list/count `C340/C4A8`, pellet
render list/count `912A/3F9C`, score delta `3712`, and popup bonus `4AC4`.
The private packet includes every remaining scalar and exact access site.

A natural negative control changes the unique
`bullet.angle = (0x80 - bullet.angle);` reflection to use `0x81`.
If the typed sparks call needs further compiler investigation, the first four
complete helpers form an independently reviewable 657-byte prefix (637
instructions +20 table bytes); no partial function or switch table is omitted.
Two isolated producers in `.analysis/unit-replays/bullet-update-d` reproduce
all 1619 bytes and the four original ordered MZ fixups. Their normalized OMF
outputs are deterministic, actual dependency identities are frozen, and the
compiled X-reflection mutation is rejected. Acceptance rechecks the saved
producers without rebuilding unchanged earlier units.

The popup callback's first declaration explicitly retains main_01, and its
empty CODE segment is placed within that group in the symbol-only context.
The complete sprite enum retains its real full domain (`PAT_STAGE_last=319`,
`PAT_MAX=320`, original word-width sentinel), not merely the low constants used
by this function. A narrowed byte enum changed the decay-pattern ternary to
AL/AH operations; preserving the true two-byte type restores the original AX
operations naturally. No instruction spelling or optimizer barrier is supplied.
Whole-program linkage remains outside this scope.
