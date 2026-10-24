// Natural ReC98 b6ba5b0a: th04/main/boss/backdrop.cpp, GAME5.
#pragma option -zCBOSS_BD_TEXT -zPmain_01
#include <dos.h>
#include "src/main/boss/backdrop.hpp"

void pascal near boss_backdrop_render(screen_x_t left, vram_y_t top, vc_t col)
{
    cdg_put_noalpha_8(left, top, CDG_BG_BOSS);
    grcg_setmode_tdw();
    grcg_setcolor_direct(col);
    boss_backdrop_colorfill();
    grcg_off();
}
