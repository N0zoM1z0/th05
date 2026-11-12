# HFLIP LUT: three complete 256-byte game-source BSS arrays

The original TH05 MZ programs each preserve one horizontal-flip lookup
buffer with the real symbol `_hflip_lut`. The pinned ReC98
`th03/formats/hfliplut[bss].asm` source declares exactly
`_hflip_lut db 100h dup(?)`; the retained native TASM sources in all three
programs contain the identical declaration. This is a runtime-writable
source reserve, not a table of written zeros.

| Original MZ | Full 256-byte reserved extent | Actual calibration MAP public |
| --- | --- | --- |
| MAIN | `2385E..2395E` | `209E:2EA0` |
| OP | `12642..12742` | `0EFE:3662` |
| MAINE | `126EE..127EE` | `1010:25DE` |

For each executable, the real TASM object's `_BSS` PUBDEF locates this
symbol at the exact local offset, and the entire source `_BSS` segment
contains no initialized LEDATA or LIDATA. The retained calibration MZ
ends before the runtime-allocated BSS; the original decoded MZ target
materializes the complete array as 256 zero bytes with no loader fixups.

`python3 scripts/review_hflip_lut_reservations.py --check` repeats the
source, OMF, MAP, target-identity and relocation comparisons. The inventory
now classifies exactly **768 formerly unknown bytes** as
`reviewed-uninitialized-game-storage`, with **zero source-authored
initialized DATA, CODE or instruction credit**. The two-byte `linebyte`
reserve immediately before each array, and all later BSS, remain separately
unclassified unless independently verified.
