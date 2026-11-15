// "CLEAR BONUS" and "CONGRATULATIONS" captions, as strings of gaiji codes.
// The font contains each caption word as a run of consecutive glyphs.
#pragma option -zCBONUS_GLYPH_DATA_TEXT -zPmain_03
#include "src/main/stage/bonus_glyph_text.hpp"

// [n] consecutive gaiji codes, starting at [first]
#define GLYPH_RUN3(first) (first), ((first) + 1), ((first) + 2)
#define GLYPH_RUN4(first) GLYPH_RUN3(first), ((first) + 3)
#define GLYPH_RUN9(first) GLYPH_RUN4(first), GLYPH_RUN4((first) + 4), ((first) + 8)

const char near gpCLEAR_BONUS[9] = {
    GLYPH_RUN3(BG_CLEAR_FIRST),
    BG_EMPTY,
    GLYPH_RUN4(BG_BONUS_FIRST),
    BG_NULL
};

const char near gpCONGRATULATION[10] = {
    GLYPH_RUN9(BG_CONGRAT_FIRST),
    BG_NULL
};

#undef GLYPH_RUN9
#undef GLYPH_RUN4
#undef GLYPH_RUN3
