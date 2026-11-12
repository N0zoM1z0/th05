# Source-backed Master JS/PAL/VSYNC/MEM uninitialized state in three MZs

Five original Master 0.23 writable state blocks are verified
inside the real `_BSS` contribution of MAIN, OP and MAINE. The pinned
archived source declares each member with the assembler `?`, not an
initialized zero:

| State | Source | Complete original source reserve |
| --- | --- | ---: |
| `js_stat[2]` | `JS.ASM`: `DW ?, ?` | 4 bytes |
| `_Palettes` | `PAL.ASM`: `DB 48 dup(?)` | 48 bytes |
| `_vsync_Count1`, `_vsync_Count2`, `vsync_OldVect` | `VS.ASM`: two `DW ?` counters and one `DD ?` vector | 8 bytes |
| `vsync_delay_count` | `VSYNC.ASM`: `DW ?` | 2 bytes |
| `mem_OutSeg`, `mem_TopHeap`, `mem_FirstHole`, `mem_EndMark` | `MEM.ASM`: four `DW ?` words | 8 bytes |

| Original MZ | Joystick BSS | Writable palette BSS | VSYNC core + delay | MEM work BSS |
| --- | --- | --- | --- | --- |
| MAIN | `23016..2301A` | `2301A..2304A` | `2304A..23054` | `23054..2305C` |
| OP | `11DFA..11DFE` | `11DFE..11E2E` | `11E2E..11E38` | `11E38..11E40` |
| MAINE | `11EA6..11EAA` | `11EAA..11EDA` | `11EDA..11EE4` | `11EE4..11EEC` |

The actual retained TASM objects have exact `_BSS` PUBDEF placements for
all fifteen scopes, zero LEDATA/LIDATA writes in the BSS segment, and linked
calibration file images that end before the source reserves. The original
MZ target views materialize the complete ranges as zeroes, with no original
MZ fixups. For every scope, the original author's ASM and the retained
TASM `[bss]` source independently agree on the type, word count and uninitialized
storage semantics.

The formerly unknown ten bytes between `_Palettes` and the first MEM
work word are the two VSYNC counters, old interrupt vector and delay
counter. Native gameplay and VSYNC routines independently access these
actual DGROUP offsets. The initialized palette defaults, MEM allocator
defaults and SUPERPA arrays remain separately reviewed and are not
recredited.

`python3 scripts/review_master_compact_bss.py --check` verifies all original
source declarations, real object/MAP/BSS identities and target extents.
`config/reviewed_master_compact_bss.json` adopts exactly **210 total
zero-credit third-party uninitialized storage bytes** (30 more than the previous proof), never newly authored
C/C++ DATA, CODE or instructions.
