// Complete bomb-background restoration after dialog, from the maintained tail.
#pragma option -zCDIALOG_TAIL_TEXT -zPmain_01
#include <dos.h>
#include "src/main/dialog/tail.hpp"
#pragma option -a2

void near dialog_exit(void)
{
    if(Ems) {
        playchar_bomb_bg_load_from_ems();
    } else {
        switch(playchar) {
        case PLAYCHAR_REIMU:
            cdg_load_single_noalpha(CDG_BG_PLAYCHAR_BOMB, BOMB_BG_REIMU_FN, 0);
            break;
        case PLAYCHAR_MARISA:
            cdg_load_single_noalpha(CDG_BG_PLAYCHAR_BOMB, BOMB_BG_MARISA_FN, 0);
            break;
        case PLAYCHAR_MIMA:
            cdg_load_single_noalpha(CDG_BG_PLAYCHAR_BOMB, BOMB_BG_MIMA_FN, 0);
            break;
        case PLAYCHAR_YUUKA:
            cdg_load_single_noalpha(CDG_BG_PLAYCHAR_BOMB, BOMB_BG_YUUKA_FN, 0);
            break;
        }
    }
}
