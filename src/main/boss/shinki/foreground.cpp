// Shinki's normal sprite and four adjacent full wing parts.
#pragma option -zCSHINKI_FG_TEXT -zPmain_01
#include "src/main/boss/late_foreground.hpp"

void pascal near shinki_fg_render(void)
{
    int top;
    int i;
    register int left;
    int patnum;
    left = boss.pos.cur.x.v >> 4;
    top = (boss.pos.cur.y.v >> 4) - 16;
    if(boss.phase == LATE_FG_PHASE_EXPLODE_BIG) {
        super_large_put(left, top, boss.sprite);
    } else {
        patnum = boss.sprite;
        if(patnum < SHINKI_FG_WING_FIRST) {
            if(boss.damage_this_frame == 0) {
                super_put(left, top, patnum);
            } else {
                super_put_1plane(left, top, patnum, 0, LATE_FG_PUT_PLANES);
            }
        } else {
            left -= (SHINKI_FG_WING_W - 64) / 2;
            top -= 16;
            if(boss.damage_this_frame != 0) {
                patnum += SHINKI_FG_PART_COUNT;
            }
            for(i = 0; i < SHINKI_FG_PART_COUNT; i++, left += SHINKI_FG_PART_W, patnum++) {
                super_put_8(left, top, patnum);
            }
        }
        boss.damage_this_frame = 0;
    }
    explosions_small_update_and_render();
    explosions_big_update_and_render();
}
