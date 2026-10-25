// Named message-fragment codepoints, not the bitmap of the gaiji font.
#pragma option -zCBONUS_GLYPH_DATA_TEXT -zPmain_03
#include "src/main/stage/bonus_glyph_text.hpp"

#define BG_FRAG3(first) (first), ((first) + 1), ((first) + 2)
#define BG_FRAG4(first) BG_FRAG3(first), ((first) + 3)
#define BG_FRAG9(first) BG_FRAG4(first), BG_FRAG4((first) + 4), ((first) + 8)

const char near gpCLEAR_BONUS[9] = {
    BG_FRAG3(BG_CLEAR_FIRST),
    BG_EMPTY,
    BG_FRAG4(BG_BONUS_FIRST),
    BG_NULL
};

const char near gpCONGRATULATION[10] = {
    BG_FRAG9(BG_CONGRAT_FIRST),
    BG_NULL
};

#undef BG_FRAG9
#undef BG_FRAG4
#undef BG_FRAG3
