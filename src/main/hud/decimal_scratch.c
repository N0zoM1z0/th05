/* One real writable nine-cell PC-98 HUD decimal glyph staging row. */
#pragma option -zCHUD_DECIMAL_SCRATCH_TEXT -zPmain_01
#ifdef __cplusplus
#error Native near HUD scratch initialized DATA is produced by C
#endif

/* The original bar, score and variable-length number raster writers
 * all rewrite the same eight glyph cells, plus the trailing NUL byte. */
#define HUD_DECIMAL_RENDER_CELLS 8
#define HUD_DECIMAL_TERMINATOR_CELLS 1

unsigned char near hud_decimal_glyphs[
    HUD_DECIMAL_RENDER_CELLS + HUD_DECIMAL_TERMINATOR_CELLS
] = { 0 };

typedef char hud_decimal_row_is_nine[
    (sizeof(hud_decimal_glyphs) == 9) ? 1 : -1];
