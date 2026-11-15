/* Glyph row shared by the HUD number renderers in bar.asm, score.asm and
 * numbers.asm. Each fills in up to eight glyphs and draws the row with
 * gaiji_putsa(). */
#pragma option -zCHUD_DECIMAL_SCRATCH_TEXT -zPmain_01
#ifdef __cplusplus
#error This file must be compiled as C
#endif

#define HUD_DECIMAL_RENDER_CELLS 8
#define HUD_DECIMAL_TERMINATOR_CELLS 1

unsigned char near hud_decimal_glyphs[
    HUD_DECIMAL_RENDER_CELLS + HUD_DECIMAL_TERMINATOR_CELLS
] = { 0 };

typedef char hud_decimal_row_is_nine[
    (sizeof(hud_decimal_glyphs) == 9) ? 1 : -1];
