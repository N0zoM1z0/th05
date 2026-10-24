# Stage setup reconstruction

Natural-source provenance: nmlgc/ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`, `th05/main014.cpp`,
`th04/main/boss/reset.cpp`, `th04/formats/bb_boss.cpp` and
`th05/main/stage/setup.cpp`. The owner preserves reset, BB allocation/freeing
and seven stage setup algorithms. It reuses the existing Boss/Motion/geometry
types from `movement.hpp`; unavailable convenience methods become equivalent
Q12.4 field assignments with their original assignment order.

`setup.hpp` retains the complete 22-byte midboss structure, every field offset,
two-byte near callbacks, four-byte far callbacks and segment-only allocation
handles. `yuki` and `boss2` are aliases for the same original 24-byte object.
No alternate same-named geometry class or edit to accepted dependencies is used.

The reference's stage-5 `SELECT_FOR_RANK` instruction macro is removed. The
source instead calls real C Pascal far
`select_for_rank(int,int,int,int)` and assigns the result to the actual byte
state fields. This follows the algorithm documented by the reference and the
observed original calls. Focused replay confirms that the linker naturally produces the original
same-segment far-call sequence; no
instruction emissions, optimization barriers or ghost helpers are retained.

## Complete original code boundary

Pinned MAIN SHA-256:
`c41f6e6b9a97b2433acc576ceaee800707c8d4ea7e498150a259663c8fa7d4f0`.
The reviewed original range is **`[144C3,14AA9)`**, **1510 bytes**, SHA-256
`d12425527e83261d732853ff35f14d80747fe638585d6ec60f20c527b378ba34`.
Addresses are hexadecimal MZ load-module offsets; add the 4032-byte MZ header
to obtain file offsets.

| Function | Original half-open span | Instruction bytes |
| --- | --- | ---: |
| `boss_reset` | `144C3..14510` | 77 |
| `bb_boss_load` | `14510..14521` | 17 |
| `bb_boss_free` | `14521..1453C` | 27 |
| `stage1_setup` | `1453C..1460B` | 207 |
| `stage2_setup` | `1460B..146C8` | 189 |
| `stage3_setup` | `146C8..14797` | 207 |
| `stage4_setup` | `14797..14871` | 218 |
| `stage5_setup` | `14871..1496E` | 253 |
| `stage6_setup` | `1496E..149FE` | 144 |
| `stagex_setup` | `149FE..14AA9` | 171 |

All 335 instructions decode contiguously, every function ends in its real
return, and all local jumps land on instruction starts. No CODE-data, switch
table or alignment bytes occur inside this extent. The original ordered MZ
fixup list contains 30 segment words, including callback address stores and
far calls. Both fresh producers reproduce the full raw bytes and ordered fixups.

The earlier survey's 1528-byte reference contribution is only routing. Its
extra 18-byte `score_delta_commit` function is absent from the original
adjacent location. The original range ends at `stagex_setup`'s return, followed
by another rendering contribution. This owner therefore excludes that score
function and does not extend its boundary using reference link order. It also
does not claim the reference's unreferenced static BSS scratch array.

## Build and binding packet

Wrapper `th05/main014.cpp` should include `src/main/stage/setup.cpp`.
Use the established MAIN flags `-O -b- -3 -Z -d -DGAME=5 -ml -DBINARY='M'`,
with the owner's original override `-d-`, `MAIN_01_TEXT` and group `main_01`.
Original main_01 frame is **`0AE1`**, load base **`AE10`**, with this code at
group offset **`96B3`**. DGROUP frame is **`209D`**.

Private `.analysis/stage-setup-boundary-review.json` records original function
boundaries, all 21 directly referenced global objects, 43 callback targets with
real frames/offsets/near-or-far ABI, call sites and the ordered 30 MZ fixups.
Calibration names annotate original operand observations; they are not
reconstruction acceptance. In particular, most callback objects store near
addresses in main_01, while boss and midboss update callbacks store true far
addresses with original frame `1527`.

| Actual external call | Original destination | Required ABI |
| --- | --- | --- |
| `@BB_LOAD$QNXC` | load `F930`, main_01:`4B20` | near Pascal, far filename pointer; segment-only handle return |
| `SELECT_FOR_RANK` | load `CFB2`, main_01:`21A2` | C Pascal far, 4 signed words, signed-word return |
| `@explosions_small_reset$qv` | `1527:245E`, load `176CE` | C++ far C order |
| `HMEM_FREE` | `0000:291E`, load `291E` | C Pascal far, segment-only pointer |
| `SUPER_ENTRY_BFNT` | `0000:2D16`, load `2D16` | C Pascal far, far filename pointer; signed-word return |
| `CDG_LOAD_ALL_NOALPHA` | `14AB:0726`, load `151D6` | C Pascal far, slot word and far filename pointer |

The two original selector call sites have NOP / PUSH CS / near CALL shape,
preserving a far return to this same code group. The maintained source supplies
the actual far function prototype and delegates instruction selection/link
relaxation to the compiler and linker.

## Source-owned data placement

This owner defines the true `bool boss_phase_timed_out = false` and uses 20
natural filename string literals, including the repeated `st03.bb`. They form
189 observed original bytes at **DGROUP `[1FC8,2085)`**, load-module
`[22998,22A55)`, SHA-256
`df449c20947a5df4569dead7a1bb02e29b025282b80c8575debb0715c1babf93`.
Their raw contents independently equal the calibration's 189-byte DATA extent
at DGROUP `[1FDA,2097)`; this is diagnostic evidence of the data layout only.
The source contains no target-derived data array. The filename text is part of
the maintained stage loading algorithm, not game image/sound assets.

The focused scaffold must position the compiler-owned DATA at `1FC8`, keeping
the byte flag at its beginning and literal offsets from the private packet.
Do not also define `_boss_phase_timed_out` in an external-symbol scaffold.
Code operands depend on these exact DATA offsets. Those 189 bytes require a
separate raw acceptance claim if counted as authored data; they are not added
to the 1510-byte authored code potential here.

A small natural negative control changes the unique stage-1
`midboss.frames_until = 2500;` to 2501. This changes a real unsigned-word
initialization without altering the structure, function boundaries or API.

The focused replay `.analysis/unit-replays/stage-setup-a` passes two isolated
cold producers, normalized OMF determinism, full code raw/fixup equality and
the compiled frame-2501 negative control. The importer rechecks saved producers
and dependencies; unchanged accepted units were not rebuilt. A separate
private observation also verifies all 189 compiler DATA bytes in both producers,
without adding them to authored code credit. Full-game layout remains open.
