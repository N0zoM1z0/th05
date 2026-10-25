// Natural TH04 maintained alphabet_cursor.inl reused with TH05's actual row21.
// ReC98 b6ba5b0a529edbb31efdf8c0e939263804f8ee47, th05_maine.asm sub_BCED.
#pragma option -zCREG_ALPHA_TEXT -zPGROUP_01
#include "src/maine/registration/alphabet.hpp"
#pragma codeseg REG_ALPHA_TEXT GROUP_01

void pascal near alphabet_cursor_put(int col, int row, int attr)
{
    register int col_r = col;
    register int row_r = row;
    gaiji_putca(
        ((col_r * 2) + 23), (row_r + 21),
        gALPHABET[(row_r * REGISTRATION_ALPHABET_COLS) + col_r], attr
    );
}
