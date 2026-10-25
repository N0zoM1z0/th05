// Natural shot invalidation: active shots and decaying hit sprites.
#pragma option -zCSHOT_INVALIDATE_TEXT -zPmain_01
#include "src/main/player/shot_invalidate.hpp"
#pragma codeseg SHOT_INVALIDATE_TEXT main_01

void near shots_invalidate(void)
{
    register Shot near *shot;
    hitshot_t near *hitshot;
    int i;

    tile_invalidate_box.x = 16;
    tile_invalidate_box.y = 16;
    shot = shots;
    hitshot = hitshots;
    for(i = 0; i < SHOT_RUNTIME_COUNT; i++, shot++) {
        if(shot->flag != F_FREE) {
            tiles_invalidate_around(shot->pos.prev.y.v, shot->pos.prev.x.v);
        }
    }
    for(i = 0; i < HITSHOT_COUNT; i++, hitshot++) {
        if(hitshot->age != 0) {
            tiles_invalidate_around(hitshot->pos.prev.y.v, hitshot->pos.prev.x.v);
        }
    }
}
