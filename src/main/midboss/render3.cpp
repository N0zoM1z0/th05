// Complete stage3 midboss sprite animation, damage flash and defeat dispatch.
#pragma option -zCM3_RENDER_TEXT -zPmain_01
#include "src/main/midboss/render5.hpp"
#pragma codeseg M3_RENDER_TEXT main_01
extern unsigned char stage_frame_mod16;

void pascal near midboss3_render(void)
{
    int left;
    int top;
    int patnum;
    if(midboss.phase < MIDBOSS5_PHASE_EXPLODE_BIG) {
        if(midboss.pos.cur.y.v < 0) {
            return;
        }
        left = midboss.pos.cur.x.v >> 4;
        top = scroll_subpixel_y_to_vram_seg1(midboss.pos.cur.y.v - 16 * 16);
        if(midboss.sprite == 208) {
            patnum = 208 + stage_frame_mod16 / 8;
        } else {
            patnum = midboss.sprite;
        }
        if(midboss.damage_this_frame == 0) {
            super_roll_put(left, top, patnum);
        } else {
            super_roll_put_1plane(left, top, patnum, 0, 0xFFC0);
            midboss.damage_this_frame = 0;
        }
    } else if(midboss.phase == MIDBOSS5_PHASE_EXPLODE_BIG) {
        midboss_defeat_render();
    }
}
