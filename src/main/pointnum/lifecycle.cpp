// Point-popup init, invalidation and per-frame update as one plain C++ file.
// Not built: compiles to 184 bytes against the original 166 (see NOTES.md).
// The built versions are init.cpp, invalidate.asm and update.asm.
#pragma option -zCPOINTNUM_LIFE_TEXT -zPmain_01 -k-
#include "src/main/pointnum/lifecycle.hpp"
#pragma codeseg POINTNUM_LIFE_TEXT main_01

#include "src/main/pointnum/init.inl"

void near pointnums_invalidate(void)
{
    register pointnum_t near *pointnum;
    register unsigned int remaining;
    tile_invalidate_box.y = POINTNUM_H;
    pointnum = pointnums;
    remaining = POINTNUM_COUNT;
    do {
        if(pointnum->flag != F_FREE) {
            tile_invalidate_box.x = pointnum->width;
            // Position drawn last frame; popups only move vertically.
            tiles_invalidate_around(pointnum->center_prev_y.v, pointnum->center_cur.x.v);
        }
        pointnum++;
    } while(--remaining != 0);
}

extern "C" void pascal near pointnums_update(void)
{
    register pointnum_t near *pointnum;
    register unsigned int remaining;
    pointnum_t near * near *alive;
    unsigned char age;
    subpixel_t y;

    pointnum_first_yellow_alive = 0;
    alive = pointnums_alive;
    pointnum = pointnums;
    remaining = POINTNUM_COUNT;
    do {
        if(pointnum->flag != F_FREE) {
            if(pointnum->flag == F_REMOVE) {
                pointnum->flag = F_FREE;
            } else {
                age = pointnum->age;
                y = pointnum->center_cur.y.v;
                pointnum->center_prev_y.v = y;
                if(age >= POINTNUM_RISE_AGE) {
                    y -= to_sp(0.5f);
                }
                pointnum->center_cur.y.v = y;
                if(y <= TO_SP(-(POINTNUM_H / 2))) {
                    pointnum->flag = F_REMOVE;
                } else {
                    age++;
                    pointnum->age = age;
                    if(age > POINTNUM_LAST_AGE) {
                        pointnum->flag = F_REMOVE;
                    } else {
                        *alive = pointnum;
                        if(remaining <= POINTNUM_YELLOW_COUNT && !pointnum_first_yellow_alive) {
                            pointnum_first_yellow_alive = pointnum;
                        }
                        alive++;
                    }
                }
            }
        }
        pointnum++;
    } while(--remaining != 0);
    *alive = 0;
}
