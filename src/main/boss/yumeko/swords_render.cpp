// Draw all live swords in the actual custom-entity pool.
#ifndef TH05_YUMEKO_COMBINED_CONTEXT
#pragma option -zCYUMEKO_UPDATE_MAIN01_TEXT -zPmain_01
#endif
#include "src/main/boss/yumeko/swords_render.hpp"
#include "src/main/boss/yumeko/sword_pool_rules.hpp"
#pragma codeseg YUMEKO_UPDATE_MAIN01_TEXT main_01

extern "C" void pascal near swords_render(void)
{
    int patnum;
    sword_t near *sword;
    int i;
    _ES = SEG_PLANE_B;
    sword = swords;
    for(i = YMS_FIRST_ACTIVE_SLOT; i < 1 + SWORD_COUNT; i++, sword++) {
        if(sword->flag != F_FREE) {
            patnum = sword->patnum_tiny;
            yumeko_render_tiny32((sword->pos.cur.x.v >> YMS_RENDER_SUBPIXEL_SHIFT) + YMS_RENDER_X_PIXELS,
                scroll_subpixel_y_to_vram_seg1(sword->pos.cur.y.v), patnum);
        }
    }
}
