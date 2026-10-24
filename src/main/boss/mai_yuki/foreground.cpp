// Sprite animation, damage silhouettes and shared/solo defeat rendering.
#pragma option -zCMY_FG_TEXT -zPmain_01
#include "src/main/boss/mai_yuki/foreground.hpp"

#define TH05_MY_FG_COMBINED
#include "src/main/boss/mai_yuki/sprite_put.cpp"
#undef TH05_MY_FG_COMBINED

void pascal near mai_yuki_fg_render(void)
{
    int yuki_left;
    int yuki_top;
    int mai_left;
    int mai_top;
    mai_left = boss.pos.cur.x.v >> 4;
    mai_top = (boss.pos.cur.y.v >> 4) - 16;
    yuki_left = boss2.pos.cur.x.v >> 4;
    yuki_top = (boss2.pos.cur.y.v >> 4) - 16;

    if(boss.phase == MY_FG_PHASE_EXPLODE_BIG) {
        if(boss2.phase_state.patterns_seen == 0) {
            super_large_put(mai_left, mai_top, boss.sprite);
            mai_yuki_sprite_put(yuki_left, yuki_top, boss2.sprite + MY_FG_CELS,
                boss2.damage_this_frame);
        } else {
            super_large_put(yuki_left, yuki_top, boss2.sprite);
            mai_yuki_sprite_put(mai_left, mai_top, boss.sprite,
                boss.damage_this_frame);
        }
    } else {
        if(boss.phase <= MY_FG_PHASE_EXPLODE_SMALL ||
            boss2.phase_state.patterns_seen != 0) {
            mai_yuki_sprite_put(mai_left, mai_top, boss.sprite,
                boss.damage_this_frame);
        }
        if(boss.phase <= MY_FG_PHASE_EXPLODE_SMALL ||
            boss2.phase_state.patterns_seen == 0) {
            mai_yuki_sprite_put(yuki_left, yuki_top, boss2.sprite + MY_FG_CELS,
                boss2.damage_this_frame);
        }
    }
    explosions_small_update_and_render();
    explosions_big_update_and_render();
    boss.damage_this_frame = 0;
    boss2.damage_this_frame = 0;
}
