// Puppet sprite bobbing, charge circles/beam and the complete Alice foreground.
#pragma option -zCALICE_FG_TEXT -zPmain_01
#include "src/main/boss/alice/foreground.hpp"

#define TH05_ALICE_FG_COMBINED
#include "src/main/boss/alice/puppets_render.cpp"
#undef TH05_ALICE_FG_COMBINED

void pascal near alice_fg_render(void)
{
    int top;
    int patnum;
    int left;
    left = boss.pos.cur.x.v >> 4;
    top = (boss.pos.cur.y.v >> 4) - 16;
    if(boss.phase == ALICE_FG_PHASE_EXPLODE_BIG) {
        super_large_put(left, top, boss.sprite);
    } else {
        patnum = boss.sprite;
        patnum += (patnum == ALICE_FG_PAT_STAY) ? (stage_frame_mod16 / 4) :
            ((patnum == ALICE_FG_PAT_ATTACK) ? stage_frame_mod2 : (stage_frame_mod8 / 4));
        if(boss.damage_this_frame == 0) {
            super_put(left, top, patnum);
        } else {
            super_put_1plane(left, top, patnum, 0, ALICE_FG_PUT_PLANES);
        }
        puppets_render();
    }
    explosions_small_update_and_render();
    explosions_big_update_and_render();
}
