// Yumeko's entrance overlay, normal animation and damage-flash consumption.
#pragma option -zCYUMEKO_FG_TEXT -zPmain_01
#include "src/main/boss/late_foreground.hpp"

void pascal near yumeko_fg_render(void)
{
    int patnum;
    int entrance_left;
    int entrance_top;
    int left;
    int top;
    left = boss.pos.cur.x.v >> 4;
    top = (boss.pos.cur.y.v >> 4) - 16;
    if(boss.phase == LATE_FG_PHASE_EXPLODE_BIG) {
        super_large_put(left, top, boss.sprite);
    } else {
        if(boss.phase == LATE_FG_PHASE_HP_FILL) {
            entrance_left = boss2.pos.cur.x.v >> 4;
            entrance_top = (boss2.pos.cur.y.v >> 4) - 16;
            super_put_rect(entrance_left, entrance_top, YUMEKO_FG_ENTRANCE_PATNUM);
        }
        patnum = boss.sprite + stage_frame_mod16 / 4;
        if(boss.damage_this_frame == 0) {
            super_put(left, top, patnum);
        } else {
            super_put_1plane(left, top, patnum, 0, LATE_FG_PUT_PLANES);
        }
        boss.damage_this_frame = 0;
    }
    explosions_small_update_and_render();
    explosions_big_update_and_render();
}
