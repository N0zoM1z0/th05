// Sixteen real rotating sprites whose radius grows to the defeat-ring limit.
#pragma option -zCMID_DEFEAT_TEXT -zPmain_01
#include "src/main/midboss/defeat_render.hpp"
#pragma codeseg MID_DEFEAT_TEXT main_01

void near midboss_defeat_render(void)
{
    int i;
    subpixel_t radius;
    subpixel_t x;
    subpixel_t y;
    radius = midboss.phase_frame << 4;
    if(radius >= 48 * 16) {
        radius = 48 * 16;
        midboss_defeat_angle += 1;
    }
    for(i = 0; i < 16; i++, midboss_defeat_angle += 0x10) {
        x = polar_x(midboss.pos.cur.x.v, radius, midboss_defeat_angle);
        y = polar_y(midboss.pos.cur.y.v, radius, midboss_defeat_angle);
        if(y > -16 * 16 && y < (368 + 16) * 16 &&
            x > -16 * 16 && x < (384 + 16) * 16) {
            x = (x >> 4) + 16;
            y = scroll_subpixel_y_to_vram_seg1(y);
            super_roll_put(x, y, midboss.sprite);
        }
    }
}
