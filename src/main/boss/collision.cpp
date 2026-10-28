// Complete player/boss overlap test using the canonical geometry and state.
#pragma option -zCBOSS_COLLISION_TEXT -zPmain_03
#include "src/main/boss/generic.hpp"
#pragma codeseg BOSS_COLLISION_TEXT main_03

void near boss_hittest_player(void)
{
    subpixel_t delta_y;
    subpixel_t delta_x;
    delta_x = boss.pos.cur.x.v;
    delta_y = boss.pos.cur.y.v;
    delta_x -= player_pos.cur.x.v;
    delta_y -= player_pos.cur.y.v;
    if(overlap_wh_inplace_fast(
        delta_y, delta_x, to_sp(BOSS_H / 2), to_sp(BOSS_W / 2)
    )) {
        player_is_hit = true;
    }
}
