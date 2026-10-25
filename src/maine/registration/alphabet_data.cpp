// Named selectable glyphs and navigation keys, preserving the writable byte ABI.
#pragma option -zCREG_ALPHA_DATA_TEXT -zPGROUP_01
#include "src/maine/registration/alphabet_data.hpp"

uint8_t gALPHABET[REGISTRATION_ALPHABET_ROWS * REGISTRATION_ALPHABET_COLS] = {
    RA_A, RA_B, RA_C, RA_D, RA_E, RA_F, RA_G, RA_H, RA_I,
    RA_J, RA_K, RA_L, RA_M, RA_N, RA_O, RA_P, RA_Q,

    RA_R, RA_S, RA_T, RA_U, RA_V, RA_W, RA_X, RA_Y, RA_Z,
    RA_CENTER_DOT, RA_FULL_STOP, RA_NOTES, RA_HEART_2,
    RA_EXCLAMATION, RA_QUESTION, RA_ELLIPSIS, RA_SIDDHAM_HAM_DUP,

    RA_0, RA_1, RA_2, RA_3, RA_4, RA_5, RA_6, RA_7, RA_8,
    RA_9, RA_TEN, RA_YUME, RA_TAMA, RA_ARROW_LEFT,
    RA_ARROW_RIGHT, RA_SPACE, RA_END
};
