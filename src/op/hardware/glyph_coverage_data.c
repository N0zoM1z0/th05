/* Original glyph effect overlay stages in the separate TH05 OP binary. */
#pragma option -zCGLYPH_OVERLAY_OP_TEXT -zPop_01
#ifdef __cplusplus
#error OP glyph-coverage DATA must be built as a C initializer
#endif
#include "src/shared/hardware/glyph_coverage.h"

const unsigned int near GLYPH_OVERLAY_MASKS[4][4] = GLYPH_COVERAGE_ROWS;
typedef char op_glyph_word_size[(sizeof(unsigned int) == 2) ? 1 : -1];
typedef char op_glyph_pattern_size[(sizeof(GLYPH_OVERLAY_MASKS[0]) == 8) ? 1 : -1];
typedef char op_glyph_bank_size[(sizeof(GLYPH_OVERLAY_MASKS) == 32) ? 1 : -1];
