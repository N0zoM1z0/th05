# Complete original Master SMEM, VSYNC and memory CODE in OP/MAINE

Twenty-four complete source-written procedures from the separately pinned
Master 0.23 source archive now reconstruct **1,172 originally unknown CODE
bytes**: 586 bytes each in OP and MAINE. No C++ source, assets or unrelated
CODE spans are counted.

| Original Master procedures | OP CODE | MAINE CODE | Bytes each |
| --- | --- | --- | ---: |
| `SMEM_RELEASE` | `2088..209E` | `2222..2238` | 22 |
| `SMEM_WGET` | `209E..20FE` | `2238..2298` | 96 |
| `VSYNC_START` | `2162..21CC` | `2320..238A` | 106 |
| `CRTBIOS_COOK` private | `21CC..21D6` | `238A..2394` | 10 |
| `VSYNC_COUNT` private | `21D6..2210` | `2394..23CE` | 58 |
| `VSYNC_END` | `2210..2258` | `23CE..2416` | 72 |
| `VSYNC_WAIT` | `2258..227E` | `2416..243C` | 38 |
| `HMEM_LALLOCATE` | `227E..22B2` | `24BC..24F0` | 52 |
| `MEM_ASSIGN_DOS` | `22B2..22D4` | `24F0..2512` | 34 |
| `MEM_ASSIGN` | `22D4..22FA` | `2512..2538` | 38 |
| `MEM_ASSIGN_ALL` | `22FA..2322` | `2538..2560` | 40 |
| `HMEM_ALLOCBYTE` | `2322..2336` | `2560..2574` | 20 |

Every complete function body is matched to its original author's `SMEMREL`,
`SMEMWGET`, `VSYNC`, `VSYNCWAI`, `HMEMLALC`, `MEMASDOS`, `MEMASSIG` or
`MEMHEAP` ASM procedure. The archived source and actual retained native TASM
input are identical under strictly limited normalizations. For VSYNC only,
original far `DOS_SETVECT` calls have genuine native linker `NOPCALL`
relaxations; the original `IMR` hardware port is named `VSYNC_IMR`, and one
near `VSYNC_LEAVE` declaration uses TASM `PROC` instead of the author's
`CALLMODEL`. No instructions or state fields are normalized away.

The complete VSYNC core physically includes **three separate procedures**
between the public `VSYNC_START` and `VSYNC_END` entries. `CRTBIOS_COOK` and
`VSYNC_COUNT` do not export publics in the original MAP; their 10/58-byte
boundaries are independently established by their complete ASM source blocks
and the genuine 106-byte `VSYNC_START` public plus the next `VSYNC_END`
public at relative `+174`. These private workers are never counted twice as
part of an inferred 174-byte monolithic starter.

Actual original retained TASM OP/MAINE OMFs each contain full ordinary CODE
LEDATA for all twelve procedures, with **44 ordered FIXUPP actions each**.
Original and calibration complete code bytes are identical after linking
through each real `_TEXT`/DGROUP frame. The original ordered MZ fixup stream
of each VSYNC_COUNT includes a segment relocation at function-relative `+3`;
all other listed procedures have empty original MZ segment streams. Every
source-backed extent occurs uniquely at its reviewed original coordinate.

Evidence is in [`context_memory_vsync.json`](../../config/context_memory_vsync.json)
with a separate explicit adoption in
[`reviewed_context_memory_vsync.json`](../../config/reviewed_context_memory_vsync.json).
`python3 scripts/review_context_memory_vsync.py --check` rereads actual native
objects and both original decoded artifacts for this **bounded** scope.
Public CI runs only `--structural-check`. All 1,172 bytes remain third-party
Master CODE with **zero game-authored C++ or ASM credit**; unrelated
unreviewed game DATA, CODE and vendor buffers remain unknown. No full cold
replay or whole-executable claim is made.
