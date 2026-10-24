// EX-Alice's bomb-invincibility bank, damage silhouette and animated backdrop.
#pragma option -zCEXALICE_FG_TEXT -zPmain_01
#include "src/main/boss/exalice/foreground.hpp"

void pascal near exalice_fg_render(void)
{
    int left;
    int top;
    int patnum;
    left = boss.pos.cur.x.v >> 4;
    top = (boss.pos.cur.y.v >> 4) - 16;
    if(boss.phase == EX_FG_PHASE_EXPLODE_BIG) {
        super_large_put(left, top, boss.sprite);
    } else {
        patnum = boss.sprite;
        if(exalice_bomb_invincibility % 2 != 0) {
            patnum += 8;
        }
        if(boss.damage_this_frame == 0) {
            super_put(left, top, patnum);
        } else {
            super_put_1plane(left, top, patnum, 0, EX_FG_PUT_PLANES);
            boss.damage_this_frame = 0;
        }
        if(patnum <= 181 && boss.phase >= 2) {
            patnum = (stage_frame_mod16 / 4) + exalice_backdrop_patnum;
            super_put(left, top, patnum);
        }
    }
    explosions_small_update_and_render();
    explosions_big_update_and_render();
}
