// Natural ReC98 b6ba5b0a: th04/main/midboss/inv.cpp, GAME5 physical ABI.
#pragma option -zCMB_INV_TEXT -zPmain_01
#include "src/main/midboss/invalidate.hpp"

void pascal near midboss_invalidate_func(void)
{
    if(midboss.phase < PHASE_EXPLODE_BIG) {
        tile_invalidate_box.x = MIDBOSS_W_MAX;
        tile_invalidate_box.y = MIDBOSS_H_MAX;
        tiles_invalidate_around(midboss.pos.prev.y.v, midboss.pos.prev.x.v);
    } else {
        tile_invalidate_box.x = (ENEMY_KILL_W * 4);
        tile_invalidate_box.y = (ENEMY_KILL_H * 4);
        tiles_invalidate_around(midboss.pos.cur.y.v, midboss.pos.cur.x.v);
    }
}
