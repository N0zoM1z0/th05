# MAINE EGC text-box wipe mask stages

The complete 40-byte original decoded interval `[10842,1086A)` is restored
as a real C `_BOX_MASKS` initializer, with five 4-row patterns of 16-bit
pixel coverage. This is not a sprite or bitmap payload: each mask word is a
four-pixel nibble repeated across the EGC's 16-bit row. The named stages
progress from sparse interleaved pixels to complete coverage, including the
actual asymmetry of the third and fourth mask rows.

The already accepted full MAINE cutscene command interpreter calls
`box_1_to_0_masked()`, which indexes `BOX_MASKS[mask][y & 3]`. The symbol
and complete 5×4×2-byte ABI therefore directly connect this contribution
to a previously accepted genuine hardware consumer. The original source
`_reference/ReC98/th03/cutscene/cutscene[data].asm` supplies the five
semantic stages. The C initializer computes words from named four-bit
coverage masks rather than copying opaque image assets or opcodes.

The binder preserves group_01 `A540`, SHARED `E800`, DGROUP `10110`, and
the complete DATA prefix at DS:0732. It supplies no candidate mask byte,
CODE instruction, or external DATA body. The two native producers in
`.analysis/unit-replays/gpt-web-maine-box-mask-patterns-a/receipt.json`
match all 40 raw bytes, one complete compiler DATA SEGDEF/LEDATA and real
MAP boundaries, with the original empty relocation stream. A compiled
change to the fourth mask's final row is rejected. The adjacent PI/Vendor
banks remain unowned and no unrelated accepted function was recompiled.
