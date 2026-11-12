# MAIN HUD: one shared nine-byte writable decimal glyph scratch row

The original decoded MAIN `[21DFC,21E05)` is a complete **nine-byte**
initialized near-C DATA contribution at DGROUP `209D:142C`. This is
the actual writable PC-98 HUD decimal display work row, with **eight
output glyph cells and one NUL terminator**. It is reused by three
already accepted source-reviewed original hardware renderers:
`main-hud-bar` (the bar-number formatter), `main-hud-score` (the
actual score digits), and `main-hud-numbers` (the variable-width
number drawer). All three are verified ASM in separate CODE extents;
they use the original DS:142C pointer and rewrite the same row, rather
than each having an independent temporary C array.

The maintained natural C source expresses that purpose directly:
`unsigned char near hud_decimal_glyphs[8+1] = {0};` initializes a
single nine-cell writable row, with the byte count derived from its
glyph and terminator semantics. Its bytes are **not** a copied bitmap,
font resource or hand-written machine-code table. The original
source's exact public variable spelling or historical translation-unit
grouping is not inferred from the numerical pointer addresses;
`hud_decimal_glyphs` is the maintained semantic name for a complete
nine-byte initialized C contribution.

The `hud` renderers already put their actual glyph codes into this
storage before copying to PC-98 VRAM. No new draw algorithm or
additional runtime buffer is provided here. The source-free binder
uses only the existing authentic MAIN code frames and DATA prefix at
`209D:142C`; it contributes no candidate data or instructions.
The separately accepted HUD decimal divisor table immediately
precedes this interval at `[21DD6,21DFC)`; the immediately following
**single unknown zero byte** `[21E05,21E06)` is the original
word-alignment gap and deliberately remains uncredited. The separately
accepted Boss default movement clamp starts at `[21E06,21E0E)`.

The focused native receipt
`.analysis/unit-replays/gpt-web-hud-decimal-scratch-a/receipt.json`
passes two independent pinned Borland C producers, all **9/9 raw
original bytes**, the complete OMF/LEDATA and MAP initialized-DATA
extent and original empty ordered MZ fixup stream. A real compiled
semantic negative changes the initializer's first glyph cell from
zero to one and is rejected. The three original HUD ASM CODE owners
are unchanged and are not recredited. No full game cold replay was
executed.
