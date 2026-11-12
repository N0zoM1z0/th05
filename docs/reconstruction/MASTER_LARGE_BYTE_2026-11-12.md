# Master LARGE_BYTE: 16 bytes of CODE-class lookup data

MAIN `[2038,2048)` is the original Master 0.23 `LARGE_BYTE` table, placed
between source-verified `draw_trapezoidx` and `SUPER_LARGE_PUT` in the native
`_TEXT` segment. These 16 bytes expand each four-bit color nibble into four
separate two-bit pixel pairs. The neighboring `SUPER_LARGE_PUT` source reads
it using `CS:LARGE_BYTE[BX]` and `CS:LARGE_BYTE[BP]`; it is not executable
machine code.

The independent original ReC98 source `libs/master.lib/large_byte.asm` names
one exported `LARGE_BYTE` and emits exactly two 8-byte rows. The actual
calibration TASM object's `_TEXT` PUBDEF resolves its label at local
`1DC6`, following the 626-byte startup prefix, to original `0000:2038`.
One complete ordinary CODE-class LEDATA supplies all 16 bytes. The saved
MAP exports this exact address; original MAIN and calibration both match all
source-derived bytes, with no original MZ relocation inside this table.

Focused check: `python3 scripts/review_master_large_byte.py --check`.
Public proof and narrow adoption:
`config/reviewed_master_large_byte.json`. The ownership inventory labels
all 16 bytes as a **foreign CODE-segment lookup table with zero instructions**,
not authored C++ and not an additional Master routine. This closes the only
previously unowned table between those two verified Master functions.
