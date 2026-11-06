// Mark the previous 8x8 footprint of each active stage-two particle dirty.
#pragma option -zCSTAGE2_INVALIDATE_TEXT -zPmain_01
#include "src/main/stage/background2.hpp"
#pragma codeseg STAGE2_INVALIDATE_TEXT main_01

// Canonical two-word dirty rectangle and the real Pascal y/x interface.
struct point_t { pixel_t x; pixel_t y; };
extern point_t tile_invalidate_box;
extern "C" void pascal near tiles_invalidate_around(subpixel_t y, subpixel_t x);

void pascal near stage2_invalidate(void)
{
    s2particle_t near *p;
    int i;
    tile_invalidate_box.x = 8;
    tile_invalidate_box.y = 8;
    for(p = s2particles, i = 0; i < S2PARTICLE_COUNT; i++, p++) {
        if(p->flag) {
            tiles_invalidate_around(p->pos.prev.y.v, p->pos.prev.x.v);
        }
    }
}
