// Complete real75-byte sprite helper, shared by the coherent foreground TU.
#ifndef TH05_MY_FG_COMBINED
#pragma option -zCMY_FG_TEXT -zPmain_01
#include "src/main/boss/mai_yuki/foreground.hpp"
#endif

void pascal near mai_yuki_sprite_put(int left, int top, int patnum, int damaged)
{
    if(patnum == MY_FG_PAT_MAI_ANIMATED || patnum == MY_FG_PAT_YUKI_ANIMATED) {
        patnum += stage_frame_mod8 / 2;
    }
    if(damaged == 0) {
        super_put(left, top, patnum);
    } else {
        super_put_1plane(left, top, patnum, 0, MY_FG_PUT_PLANES);
    }
}
