/* Semantic four-stage character-overlay masks for TH05 MAINE. */
#pragma option -zCGLYPH_OVERLAY_DATA_TEXT -zPgroup_01
#ifdef __cplusplus
#error The glyph-coverage bank must be owned by an actual C object
#endif
#include "src/shared/hardware/glyph_coverage.h"

const unsigned int near GLYPH_OVERLAY_MASKS[4][4] = GLYPH_COVERAGE_ROWS;
typedef char glyph_overlay_word_size[(sizeof(unsigned int) == 2) ? 1 : -1];
typedef char glyph_overlay_stage_size[(sizeof(GLYPH_OVERLAY_MASKS[0]) == 8) ? 1 : -1];
typedef char glyph_overlay_bank_size[(sizeof(GLYPH_OVERLAY_MASKS) == 32) ? 1 : -1];
