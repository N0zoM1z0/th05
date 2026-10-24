# Mima shot-control candidate

`mima.cpp` adapts natural C++ from nmlgc/ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`, `th05/p_mima.cpp`.
It preserves the eight shot algorithms, case order, iterator layout, byte-sized
angles, option offsets and source-local `-a2` pragma. `mima.hpp` includes the
accepted `reimu.hpp` for the single real Shot/ShotAddIterator definitions;
velocity and position operations expand into equivalent signed Q12.4 `.v`
assignments without changing accepted headers.

There is no instruction emission, inline ASM, fake external zero symbol, byte
array, address-word array or code-generation barrier. The seven semantic switch
tables must be produced by the compiler. All numeric target observations below
come from the pinned original; reference code and calibration metadata provide
candidate names and routing, not reconstruction acceptance.

## Original boundaries and classification

Pinned MAIN SHA-256:
`c41f6e6b9a97b2433acc576ceaee800707c8d4ea7e498150a259663c8fa7d4f0`.
The original complete contribution is load-module range
**`[0xF3E8,0xF92F)`**, **1351 bytes**, SHA-256
`646f579c4310b18a2d2d18d25d6f50c0b1a83766879dd10fd2e1af30028662e6`.
The MZ header is 4032 bytes. All target offsets here are relative to the load
module, not the container file. A unique first-function diagnostic shape located
the contribution; original instruction sequences, calls, returns, switch guards
and table entries were then read independently. This contribution follows
Marisa in the original, but reference ordering alone does not establish that.

| Function | Complete span | Instructions | CODE-data | Padding |
| --- | --- | ---: | ---: | ---: |
| `SHOT_MIMA_L2` | `F3E8..F453` | 107 | 0 | 0 |
| `SHOT_MIMA_L3` | `F453..F4CB` | 120 | 0 | 0 |
| `SHOT_MIMA_L4` | `F4CB..F564` | 144 | 8 | 1 |
| `SHOT_MIMA_L5` | `F564..F5FB` | 143 | 8 | 0 |
| `SHOT_MIMA_L6` | `F5FB..F6A7` | 164 | 8 | 0 |
| `SHOT_MIMA_L7` | `F6A7..F75F` | 171 | 12 | 1 |
| `SHOT_MIMA_L8` | `F75F..F826` | 187 | 12 | 0 |
| `SHOT_MIMA_L9` | `F826..F92F` | 245 | 20 | 0 |

Each instruction range decodes contiguously through its real terminal return.
The complete unit contains **1281 instruction bytes + 68 compiler-generated
CODE-data bytes + 2 zero-padding bytes**. Potential authored code credit after
acceptance is **1349**, keeping instructions and semantic table data separately
reported and excluding padding. Complete raw comparison must include all 1351
bytes.

## Semantic switch tables

Original CS:[BX+table] operands resolve through the `main_01` frame. Guard
maxima independently agree with the counts below, and all **34 of 34** table
words point to instruction starts inside their corresponding functions.
Ranges are hexadecimal and half-open.

| Level / switch | Target table span | Unit-relative span | Bytes | Entries |
| --- | --- | --- | ---: | ---: |
| L4 option | `F55C..F564` | `174..17C` | 8 | 4 |
| L5 option | `F5F3..F5FB` | `20B..213` | 8 | 4 |
| L6 option | `F69F..F6A7` | `2B7..2BF` | 8 | 4 |
| L7 option | `F753..F75F` | `36B..377` | 12 | 6 |
| L8 option | `F81A..F826` | `432..43E` | 12 | 6 |
| L9 primary | `F91B..F923` | `533..53B` | 8 | 4 |
| L9 option | `F923..F92F` | `53B..547` | 12 | 6 |

The two zero bytes occur at original offsets **`F55B`, `F752`**, or unit-relative
**`173`, `36A`**. They are alignment, receive no authored credit, and remain
inside full comparison. The original L9 compiler places the primary-shot table
before the option table in its tail despite the opposite dispatch order.
Private target-only metadata is at `.analysis/mima-boundary-review.json`.

## Build context and bindings

Use source wrapper `th05/p_mima.cpp` including
`src/main/player/mima.cpp`, segment `MAIN_01_TEXT`, group `main_01`, flags
`-O -b- -3 -Z -d -DGAME=5 -ml -DBINARY='M'`, with retained `-a2` pragma.
The true original group frame is relative segment **`0AE1`**, load offset
**`AE10`**; the contribution begins at group offset **`45D8`**. Both the
compiler-generated table operands and their near-address words depend on this
frame and must be checked without operand normalization or masking.

| External symbol | Load destination | Group offset | ABI |
| --- | --- | --- | --- |
| `@RANDRING1_NEXT16_AND$QUI` | `C70E` | `18FE` | near Pascal; unsigned-word mask |
| `@SHOT_VELOCITY_SET$QP7SPPOINTUC` | `E3C4` | `35B4` | near Pascal; real SPPoint near pointer and byte angle |
| `@shots_add$qv` | `E38C` | `357C` | near C++; Shot near-pointer return |
| `@shot_cycle_init$qv` | `E644` | `3834` | near C++; byte return in AL |

There are no direct external data references or far calls, and the ordered MZ
fixup list is empty. Mima uses 23 external near calls: 8 cycle initializations,
8 pool allocations, 6 velocity setters and 1 random-ring call. Helper names and
roles are corroborated by the natural source and calibration EXTDEFs; the
destinations and call widths are original-target observations.

A natural negative control changes the unique L2 `shot->damage = 8;` assignment
to `shot->damage = 7;`. The original operation writes the true Shot.damage byte
at structure offset 16. This changes game semantics without replacing bodies,
removing returns or altering the public API.

No exact acceptance is claimed here. Focused cold compilation, complete raw
comparison and OMF/fixup checks are still required. This contribution does not
establish its borrowed helper bodies, the shot pool, whole-program layout or
runtime behavior.
