// dialog_exit(): reloads the bomb background that dialog_animate() freed.
// tail.cpp keeps an identical copy for its own layout; built on its own,
// the late -a2 below gives the switch table its original one-byte alignment.
#pragma option -zCDIALOG_TAIL_TEXT -zPmain_01
#include <dos.h>
#include "src/main/dialog/tail.hpp"
#pragma option -a2

void near dialog_exit(void)
{
    // Copy the background back from EMS, or reload it from disk.
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
