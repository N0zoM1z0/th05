// Actual writable 3x17 gaiji-selector keyboard; no font bitmap is defined here.
#ifndef TH05_MREG_ALPHABET_DATA_HPP
#define TH05_MREG_ALPHABET_DATA_HPP
#include "src/maine/registration/glyphball.hpp"

enum RegistrationAlphabetCode {
    RA_0 = 0xA0,
    RA_1, RA_2, RA_3, RA_4, RA_5, RA_6, RA_7, RA_8, RA_9,
    RA_A = 0xAA,
    RA_B, RA_C, RA_D, RA_E, RA_F, RA_G, RA_H, RA_I, RA_J,
    RA_K, RA_L, RA_M, RA_N, RA_O, RA_P, RA_Q, RA_R, RA_S,
    RA_T, RA_U, RA_V, RA_W, RA_X, RA_Y, RA_Z,
    RA_CENTER_DOT = 0xC4,
    RA_FULL_STOP = 0xC5,
    RA_NOTES = 0x03,
    RA_HEART_2 = 0x06,
    RA_EXCLAMATION = 0x07,
    RA_QUESTION = 0x08,
    RA_ELLIPSIS = 0x0C,
    RA_SIDDHAM_HAM_DUP = 0x0F,
    RA_TEN = 0xE6,
    RA_YUME = 0xE7,
    RA_TAMA = 0xE8,
    RA_ARROW_LEFT = 0xCE,
    RA_ARROW_RIGHT = 0xCF,
    RA_SPACE = 0xCD,
    RA_END = 0xD5
};
typedef char reg_alphabet_rows3[(REGISTRATION_ALPHABET_ROWS == 3) ? 1 : -1];
typedef char reg_alphabet_cols17[(REGISTRATION_ALPHABET_COLS == 17) ? 1 : -1];
#endif
