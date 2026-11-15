// pointnums_invalidate(): marks the tiles under every live point popup for
// redrawing. Not built (invalidate.asm is), but this C++ version compiles to
// the same 44 bytes.
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
            // Popups only move vertically, so previous Y and current X give
            // the position drawn last frame. Loading X into AX first (TH04
            // adjusts it there) gives the original `PUSH AX`; passing the
            // field directly would push it from memory.
            _AX = pointnum->center_cur.x.v;
            tiles_invalidate_around(
                pointnum->center_prev_y.v, static_cast<subpixel_t>(_AX)
            );
        }
        pointnum++;
    } while(--remaining != 0);
}
