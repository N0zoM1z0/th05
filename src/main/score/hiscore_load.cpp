// hiscore_load(): loads the score list for the current character and rank,
// and copies its top score, converted from gaiji, into [hiscore].
#pragma option -zCHISCORE_LOAD_TEXT -zPmain_01 -k-
#include <dos.h>
#include "src/op/hiscore/view.hpp"
// Declared here instead of including current.hpp, which would pull the
// SHARED code segment into main_01 and overflow the 64 KiB group.
#pragma codeseg SCORE_IO_TEXT main_01
void near scoredat_load_for_cur(void);

extern score_lebcd_t hiscore;
#pragma codeseg HISCORE_LOAD_TEXT main_01
void near hiscore_load(void)
{
    scoredat_load_for_cur();
    _BX = 0;
    _CX = SCORE_DIGITS;
    digit_loop: {
        _AL = hi.score.g_score[0].digits[_BX];
        _AL -= gb_0;
        hiscore.digits[_BX++] = _AL;
        asm { loop digit_loop }
    }
}
