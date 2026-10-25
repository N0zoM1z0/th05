// Original verdict settings and five semantic glyph strings, without font pixels.
#pragma option -zCVERDICT_STATE_DATA_TEXT -zPgroup_01
#include "src/maine/verdict/state_data.hpp"

enum VerdictDataGlyph {
    VERDICT_GLYPH_NULL = 0,
    VERDICT_GLYPH_EMPTY = 0x02
};

// GAME5's bold alphabet is sequential; unlike the older definition, M precedes N.
enum VerdictRankGlyph {
    VR_A = 0xAA, VR_B, VR_C, VR_D, VR_E, VR_F, VR_G, VR_H, VR_I,
    VR_J, VR_K, VR_L, VR_M, VR_N, VR_O, VR_P, VR_Q, VR_R, VR_S,
    VR_T, VR_U, VR_V, VR_W, VR_X, VR_Y, VR_Z
};

int verdict_text_left = 336;
unsigned int verdict_text_color = 2;
unsigned int verdict_comment_color = 6;
int verdict_text_top = 48;
bool skill_subtract = false;
char verdict_rank_glyphs[5][8] = {
    { VERDICT_GLYPH_EMPTY, VERDICT_GLYPH_EMPTY, VERDICT_GLYPH_EMPTY,
      VR_E, VR_A, VR_S, VR_Y, VERDICT_GLYPH_NULL },
    { VERDICT_GLYPH_EMPTY, VR_N, VR_O, VR_R, VR_M, VR_A, VR_L,
      VERDICT_GLYPH_NULL },
    { VERDICT_GLYPH_EMPTY, VERDICT_GLYPH_EMPTY, VERDICT_GLYPH_EMPTY,
      VR_H, VR_A, VR_R, VR_D, VERDICT_GLYPH_NULL },
    { VR_L, VR_U, VR_N, VR_A, VR_T, VR_I, VR_C, VERDICT_GLYPH_NULL },
    { VERDICT_GLYPH_EMPTY, VERDICT_GLYPH_EMPTY,
      VR_E, VR_X, VR_T, VR_R, VR_A, VERDICT_GLYPH_NULL }
};
bool graph_3_digit_put_as_fixed_2_digit = false;

typedef char verdict_rank_rows_check[(sizeof(verdict_rank_glyphs) == 40) ? 1 : -1];
typedef char verdict_rank_stride_check[(sizeof(verdict_rank_glyphs[0]) == 8) ? 1 : -1];
