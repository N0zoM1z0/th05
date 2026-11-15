/* The four dither masks that the hardware text renderer (ReC98
 * th04/hardware/grppsafx.asm) uses to fade glyphs in, from sparse (8/0/2/0)
 * to a full checkerboard (A/5/A/5). Each row repeats a 4-pixel nibble. */
#pragma option -zCGLYPH_OVERLAY_DATA_TEXT -zPgroup_01
#ifdef __cplusplus
#error This file is compiled as C
#endif
#include "src/shared/hardware/glyph_coverage.h"

const unsigned int near GLYPH_OVERLAY_MASKS[4][4] = GLYPH_COVERAGE_ROWS;
typedef char glyph_overlay_word_size[(sizeof(unsigned int) == 2) ? 1 : -1];
typedef char glyph_overlay_stage_size[(sizeof(GLYPH_OVERLAY_MASKS[0]) == 8) ? 1 : -1];
typedef char glyph_overlay_bank_size[(sizeof(GLYPH_OVERLAY_MASKS) == 32) ? 1 : -1];
