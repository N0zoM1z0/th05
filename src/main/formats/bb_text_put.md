# `bb_txt_put_8_raw()`: text-dissolve sprite blitter (ASM)

`bb_text_put.asm` is the near fastcall assembly routine at MAIN
`[E51A,E57C)`, following ReC98 `th04/formats/bb_txt_put.asm`. It takes the
left/top coordinates in AX/DX and the sprite number in CX, points ES:DI at
VRAM and DS:SI at the 128-byte sprite in the text-mask segment, and copies
32 rows of 32 pixels as DWORDs. Rows that cross line 400 wrap around by one
32,000-byte VRAM plane.

ZUN landmine: the routine never clears the direction flag and relies on the
caller having done so.

The two `EVEN` NOPs at offsets 39 and 97 are part of the comparison but carry
no source credit. The replay's negative control changes the 32-row copy to
31 rows.
