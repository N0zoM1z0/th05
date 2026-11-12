# Source-backed Master JS/PAL/MEM uninitialized state in three MZs

Three additional original Master 0.23 writable state blocks are verified
inside the real `_BSS` contribution of MAIN, OP and MAINE. The pinned
archived source declares each member with the assembler `?`, not an
initialized zero:

| State | Source | Complete original source reserve |
| --- | --- | ---: |
| `js_stat[2]` | `JS.ASM`: `DW ?, ?` | 4 bytes |
| `_Palettes` | `PAL.ASM`: `DB 48 dup(?)` | 48 bytes |
| `mem_OutSeg`, `mem_TopHeap`, `mem_FirstHole`, `mem_EndMark` | `MEM.ASM`: four `DW ?` words | 8 bytes |

| Original MZ | Joystick BSS | Writable palette BSS | MEM work BSS |
| --- | --- | --- | --- |
| MAIN | `23016..2301A` | `2301A..2304A` | `23054..2305C` |
| OP | `11DFA..11DFE` | `11DFE..11E2E` | `11E38..11E40` |
| MAINE | `11EA6..11EAA` | `11EAA..11EDA` | `11EE4..11EEC` |

The actual retained TASM objects have exact `_BSS` PUBDEF placements for
all nine scopes, zero LEDATA/LIDATA writes in the BSS segment, and linked
calibration file images that end before the source reserves. The original
MZ target views materialize the complete ranges as zeroes, with no original
MZ fixups. For every scope, the original author's ASM and the retained
TASM `[bss]` source independently agree on the type, word count and uninitialized
storage semantics.

The **ten-byte gap between `_Palettes` and the first MEM work word in each
program remains unknown**; neither the original source nor this review
assigns that space to a nearby symbol. The initialized palette defaults,
MEM allocator defaults and the large SUPERPA arrays are separately reviewed
and not double-counted.

`python3 scripts/review_master_compact_bss.py --check` verifies all original
source declarations, real object/MAP/BSS identities and target extents.
`config/reviewed_master_compact_bss.json` adopts exactly **180 additional
zero-credit third-party uninitialized storage bytes**, never newly authored
C/C++ DATA, CODE or instructions.
