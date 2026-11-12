# MAINE character effect: four original glyph-overlay coverage masks

The complete decoded MAINE interval `[107AC,107CC)` owns a 32-byte natural
C near-DATA bank of four 4-row, 16-pixel glyph-coverage patterns. These
belong to the actual `th04/hardware/grppsafx.asm` hardware text-rendering
pipeline reused by TH05, not to a sprite, font bitmap or copied image.
Each row repeats one four-bit coverage nibble across sixteen pixels:

- first stage: 8/0/2/0 (sparse character highlight)
- second: 8/4/2/1 (alternating single bits)
- third: A/4/A/1 (interleaved two-bit highlights)
- fourth: A/5/A/5 (alternating checkerboard)

The maintained initializer represents those graphic operations as named
nibble choices multiplied by the natural 16-bit repetition constant,
not literal target-machine byte arrays. The native source reference
`_reference/ReC98/th04/hardware/grppsafx.asm` preserves all four stages,
with the original internal `_grppsafx_mask_1..4` labels; the pointer table
that selects the stages remains unowned and is not provided by the
scaffold.

The source's `GLYPH_OVERLAY_MASKS[4][4]` is one ordinary C initializer with
no CODE, BSS, inside hole or relocation. The symbol-only binder preserves
MAINE group_01 `A540`, SHARED `E800`, DATA `10110:069C` and only the
outside DATA prefix. Two independent Borland C producers match every one
of the original 32 bytes and exact OMF/MAP boundaries; an actual compiled
change from the fourth mask's nibble 5 to 4 is rejected. Scoped receipt:
`.analysis/unit-replays/gpt-web-maine-glyph-coverage-c/receipt.json`.
No other accepted unit or entire MAINE image was recompiled.
