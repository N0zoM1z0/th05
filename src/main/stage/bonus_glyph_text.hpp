// Complete byte-selector text objects used by the real bonus gaiji-string calls.
#ifndef TH05_STAGE_BONUS_GLYPH_TEXT_HPP
#define TH05_STAGE_BONUS_GLYPH_TEXT_HPP
#include "src/shared/abi.hpp"

enum BonusGlyphCode {
    BG_NULL = 0,
    BG_EMPTY = 0x02,
    BG_CLEAR_FIRST = 0x4D,
    BG_BONUS_FIRST = 0x58,
    BG_CONGRAT_FIRST = 0x5C
};
extern const char near gpCLEAR_BONUS[9];
extern const char near gpCONGRATULATION[10];
typedef char bonus_glyph_char1[(sizeof(char) == 1) ? 1 : -1];
typedef char bonus_glyph_clear9[(sizeof(gpCLEAR_BONUS) == 9) ? 1 : -1];
typedef char bonus_glyph_congrat10[(sizeof(gpCONGRATULATION) == 10) ? 1 : -1];
typedef char bonus_glyph_pair19[((sizeof(gpCLEAR_BONUS) + sizeof(gpCONGRATULATION)) == 19) ? 1 : -1];
#endif
