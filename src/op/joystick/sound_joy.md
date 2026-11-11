# OP SOUND_JOY: separate 18-byte PSG reader

Original OP `_TEXT` `[2CA8,2CBA)` is its own near `SOUND_JOY`, **not** the
tail of the preceding `draw_trapezoid` rasterizer. The complete 18 bytes
select PSG register 15, call the foreign `SOUND_O` at `20D4`, and read the
inverted joystick data at port 018Ah. The final `EVEN` NOP at offset 17 is
checked but excluded from authored instruction credit.

This ordinary source-level ASM has no copied foreign instructions, initialized
DATA or invented BSS. The original OP CODE and DGROUP frames and full native
DATA/BSS sizes are held by a zero-LEDATA binder. The maintained source is a
TH05-specific PC-98 joystick port. The original historical ASM file is not
independently known. The related `JS_SENSE` function is a separate source
owner; the single trailing zero at `2CCF` is left unowned.

## Accepted local replay

Two independent real TASM/TLINK source builds matched **18/18 original
bytes**, including the original near call displacement to `SOUND_O` and the
empty ordered MZ relocation list. A compiled mutation of the PSG input
register from 0Eh to 0Dh was rejected. Receipt:
`.analysis/asm-replays/gpt-web-op-sound-joy-verified-20261111/receipt.json`.
