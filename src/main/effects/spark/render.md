# spark_render(): the spark blitter (original assembly)

`spark_render` (in `render.asm`) draws one 8x8 spark cel into the VRAM plane
that ES already points to, with GRCG mode and color set up by the caller.

- Inputs: AX = left pixel, DX = top VRAM row, CL = cel (masked to 0-7).
  SI/DI are restored; AX/BX/CX/DX are clobbered. LODSW relies on a clear
  direction flag.
- Rows whose mask word is zero are skipped; if the high byte is zero, only
  one byte is written. The Y coordinate wraps after row 399. There is no
  horizontal clipping.
- The sprite bank at DS:14AA is 1024 bytes: 8 horizontal shifts x 8 cels x
  8 rows x 2 bytes, shift-major (unlike the point-number glyph bank, which is
  glyph-major).

The function ends with one `EVEN` alignment NOP. It uses a register-only
protocol and the same row macro as other ZUN blitters, which is why it is
kept as assembly. ReC98's `th04/main/spark_render.asm` and
`sprites/blit.inc` describe the same code.
