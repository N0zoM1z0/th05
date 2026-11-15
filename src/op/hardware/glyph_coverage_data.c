/* OP.EXE's copy of the four 4x4-pixel coverage masks used by the glyph
 * fade-in effect renderer (grppsafx). MAINE.EXE has its own identical copy. */
#pragma option -zCGLYPH_OVERLAY_OP_TEXT -zPop_01
#ifdef __cplusplus
#error Compile this file as C
#endif
#include "src/shared/hardware/glyph_coverage.h"

const unsigned int near GLYPH_OVERLAY_MASKS[4][4] = GLYPH_COVERAGE_ROWS;
