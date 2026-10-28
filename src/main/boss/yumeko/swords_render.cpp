// Draw all live swords in the actual custom-entity pool.
#pragma option -zCYUMEKO_UPDATE_MAIN01_TEXT -zPmain_01
#include "src/main/boss/yumeko/swords_render.hpp"
#pragma codeseg YUMEKO_UPDATE_MAIN01_TEXT main_01

extern "C" void pascal near swords_render(void)
{
    int patnum;
    sword_t near *sword;
    int i;
    _ES = SEG_PLANE_B;
    sword = swords;
    for(i = 1; i < 1 + SWORD_COUNT; i++, sword++) {
        if(sword->flag != F_FREE) {
            patnum = sword->patnum_tiny;
            yumeko_render_tiny32((sword->pos.cur.x.v >> 4) + 16,
                scroll_subpixel_y_to_vram_seg1(sword->pos.cur.y.v), patnum);
        }
    }
}
