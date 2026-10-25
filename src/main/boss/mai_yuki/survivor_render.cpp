// Complete foreground dispatch after the shared fight leaves a single boss.
#pragma option -zCSURVIVOR_FG_TEXT -zPmain_01
#include "src/main/boss/foreground.hpp"
#pragma codeseg SURVIVOR_FG_TEXT main_01

void pascal near mai_yuki_survivor_render(void)
{
    int left;
    int top;
    int patnum;
    left = boss.pos.cur.x.v >> 4;
    top = (boss.pos.cur.y.v >> 4) - 16;
    if(boss.phase == BOSS_FG_PHASE_EXPLODE_BIG) {
        super_large_put(left, top, boss.sprite);
    } else {
        patnum = boss.sprite;
        if(boss.sprite == 208 || boss.sprite == 192) {
            patnum += stage_frame_mod8 / 2;
        }
        if(boss.damage_this_frame == 0) {
            super_put(left, top, patnum);
        } else {
            super_put_1plane(left, top, patnum, 0, BOSS_FG_PUT_PLANES);
        }
    }
    explosions_small_update_and_render();
    explosions_big_update_and_render();
}
