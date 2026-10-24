# Yuuka shot-control candidate

`yuuka.cpp` localizes nmlgc/ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`, `th05/p_yuuka.cpp`, as natural
C++. `yuuka.hpp` reuses the existing Shot/ShotAddIterator declarations from
`reimu.hpp`; no same-named replacement types or edits to accepted headers are
introduced. Pixel offsets and the velocity setter are expanded into equivalent
signed Q12.4 `.v` assignments inside this owner.

The source contains no instruction emission, inline ASM, fake linker symbols,
table arrays or asset arrays. Its nine semantic switch tables must be generated
by the pinned compiler. The original source-local `#pragma option -a2` remains.

## Target and complete boundaries

Pinned MAIN SHA-256:
`c41f6e6b9a97b2433acc576ceaee800707c8d4ea7e498150a259663c8fa7d4f0`.
The original contribution is `[0x1245E,0x12AC4)` relative to its MZ load module,
**1638 bytes**, SHA-256
`1713e85501552609afe1f0dd6f32ce1ebd68e68bc11d44f92ea62c9275dc37bb`.
Its location was established through a unique first-function diagnostic match,
then independent reading of the original instructions, branch targets, tables
and function ends. It follows the original HUD contribution; it is **not**
immediately after Marisa/Mima merely because the reference link orders them so.
The MZ file header is 4032 bytes; all offsets below are load-module offsets.

| Function | Whole contribution span | Instruction bytes |
| --- | --- | ---: |
| `SHOT_YUUKA_L2` | `1245E..124D6` | 120 |
| `SHOT_YUUKA_L3` | `124D6..12561` | 139 |
| `SHOT_YUUKA_L4` | `12561..125FF` | 158 |
| `SHOT_YUUKA_L5` | `125FF..126BE` | 182 |
| `SHOT_YUUKA_L6` | `126BE..127A7` | 216 |
| `SHOT_YUUKA_L7` | `127A7..128A9` | 238 |
| `SHOT_YUUKA_L8` | `128A9..129AA` | 234 |
| `SHOT_YUUKA_L9` | `129AA..12AC4` | 256 |

Every instruction region decodes contiguously through a real terminal return.
The unit separates into **1543 instruction bytes + 92 compiler-generated CODE
table bytes + 3 observed zero-padding bytes**. If cold replay accepts it, the
potential authored code credit is **1635**, with padding excluded and instruction
and CODE-data subtotals retained separately.

## Switch-table evidence

Each CS:[BX+table] operand identifies its table relative to original `main_01`.
All **46 of 46** entries land on real instruction starts inside their own
function. The table guard maxima independently agree with the following counts.
Ranges are hexadecimal, half-open; entries are original near code addresses.
No address-word array is supplied by the maintained source.

| Level / switch | Target table span | Unit-relative span | Bytes | Entries |
| --- | --- | --- | ---: | ---: |
| L5 outer | `126B6..126BE` | `258..260` | 8 | 4 |
| L6 outer | `12797..1279F` | `339..341` | 8 | 4 |
| L6 inner | `1279F..127A7` | `341..349` | 8 | 4 |
| L7 outer | `12895..128A1` | `437..443` | 12 | 6 |
| L7 inner | `128A1..128A9` | `443..44B` | 8 | 4 |
| L8 outer | `12994..129A0` | `536..542` | 12 | 6 |
| L8 inner | `129A0..129AA` | `542..54C` | 10 | 5 |
| L9 outer | `12AAA..12ABA` | `64C..65C` | 16 | 8 |
| L9 inner | `12ABA..12AC4` | `65C..666` | 10 | 5 |

The observed zero bytes are at target offsets `126B5`, `12796`, `12993`, or
unit offsets **`257`, `338`, `535`** (hexadecimal). They are not NOP instructions
and receive no authored credit. Complete unit comparison still includes them.
A private structured target-only review is at
`.analysis/yuuka-boundary-review.json`; that diagnostic file is not acceptance.

## Build context and external bindings

Use wrapper `th05/p_yuuka.cpp` including `src/main/player/yuuka.cpp`, segment
`MAIN_01_TEXT`, group `main_01`, established flags
`-O -b- -3 -Z -d -DGAME=5 -ml -DBINARY='M'`, plus the retained `-a2` pragma.
The original group frame is relative segment `0AE1`, load offset `AE10`.
This unit starts at group offset **`764E`**. Those frame-relative positions must
be preserved for compiler-generated table words as well as near calls.

| External symbol | Target load destination | Group offset | ABI |
| --- | --- | --- | --- |
| `@RANDRING1_NEXT16_AND$QUI` | `C70E` | `18FE` | near Pascal, unsigned-word mask |
| `@SHOT_VELOCITY_SET$QP7SPPOINTUC` | `E3C4` | `35B4` | near Pascal; true embedded SPPoint near pointer and angle |
| `@shots_add$qv` | `E38C` | `357C` | near C++, real Shot near-pointer return |
| `@shot_cycle_init$qv` | `E644` | `3834` | near C++, byte return in AL |

No external data symbol is directly referenced, and the ordered MZ fixup list
is empty. The names/roles are corroborated by source and calibration EXTDEFs;
numeric destinations, instruction widths and table topology are target evidence.

A natural negative-control candidate changes the unique L2 primary-shot
assignment `shot->damage = 9;` to `shot->damage = 8;`. The corresponding original
instruction is a byte store to Shot.damage, so this probes a real semantic
change without removing functions, replacing returns or changing the API.

No exact acceptance is claimed by this packet. Focused cold compilation,
complete raw instructions/tables/padding, OMF and fixup comparison remain
required. This unit does not establish its borrowed helpers, shot pool, full
game layout or runtime behavior.
