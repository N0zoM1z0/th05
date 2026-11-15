# Item splash dot renderer

`item_splash_dot_render()` (MAIN `[E152,E16E)`, 28 bytes) sets one pixel of
an item spawn splash. It takes the screen X in AX and the VRAM Y in DX, and
writes into the VRAM plane that the caller selected in ES. The row offset is
computed as Y * 64 + Y * 16 (80 bytes per row), plus X / 8, and the
pixel's bit mask is written to that byte; the caller's GRCG setup turns this
into a single-pixel draw. There is no clipping; `item_splashes_render()`
clips before calling it.

The original is hand-written assembly, matching ReC98's
`th04/main/item/splash_dot_render.asm`; `splash_dot_exact.asm` reproduces
it. The equivalent C in `dot_render.cpp` compiles to 42 bytes and is not
built.
