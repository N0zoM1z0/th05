// Natural maintained TH04 splashes.inl algorithms, adapted to canonical TH05
// geometry without changing shared class definitions. Init stays foreign.
#pragma option -zCITEM_SPLASH_TEXT -zPmain_03
#include "src/main/item/splash.hpp"
#pragma codeseg ITEM_SPLASH_TEXT main_03

void pascal near item_splashes_add(Subpixel center_x, Subpixel center_y)
{
    item_splash_t near &splash = item_splashes[item_splash_last_id];
    item_splash_last_id++;
    if(item_splash_last_id >= ITEM_SPLASH_COUNT) {
        item_splash_last_id = 0;
    }
    if(splash.flag != F_FREE) {
        return;
    }
    splash.flag = F_ALIVE;
    splash.center.x = center_x;
    splash.center.y = center_y;
    splash.radius_cur.v = ITEM_SPLASH_RADIUS_START * 16;
    splash.time = ITEM_SPLASH_RADIUS_END / ITEM_SPLASH_RADIUS_DELTA;
    splash.radius_prev.v = ITEM_SPLASH_RADIUS_START * 16;
}

void near item_splashes_update(void)
{
    item_splash_t near *p;
    int i;
    for((p = item_splashes, i = 0); i < ITEM_SPLASH_COUNT; (i++, p++)) {
        if(p->flag == F_FREE) {
            continue;
        } else if(p->flag == F_REMOVE) {
            p->flag = F_FREE;
        } else {
            p->radius_prev = p->radius_cur;
            p->radius_cur.v += ITEM_SPLASH_RADIUS_DELTA * 16;
            if(p->radius_cur.v >= ITEM_SPLASH_RADIUS_END * 16) {
                p->flag = F_REMOVE;
            }
        }
    }
}
