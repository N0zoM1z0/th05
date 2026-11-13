// Complete point-popup invalidation, retaining the previous-Y/current-X pair.
#pragma option -zCPOINTNUM_LIFE_TEXT -zPmain_01 -k-
#include "src/main/pointnum/lifecycle.hpp"
#pragma codeseg POINTNUM_LIFE_TEXT main_01

void near pointnums_invalidate(void)
{
    register pointnum_t near *pointnum;
    register int remaining;

    tile_invalidate_box.y = POINTNUM_H;
    pointnum = pointnums;
    remaining = POINTNUM_COUNT;
    do {
        if(pointnum->flag != F_FREE) {
            tile_invalidate_box.x = pointnum->width;
            // Keep current X in the original AX argument register before the
            // previous-Y/current-X Pascal argument pair is pushed.
            _AX = pointnum->center_cur.x.v;
            tiles_invalidate_around(
                pointnum->center_prev_y.v, static_cast<subpixel_t>(_AX)
            );
        }
        pointnum++;
    } while(--remaining != 0);
}
