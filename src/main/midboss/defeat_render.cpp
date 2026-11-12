// Sixteen real rotating sprites whose radius grows to the defeat-ring limit.
#pragma option -zCMID_DEFEAT_TEXT -zPmain_01
#include "src/main/boss/late_game_state_publics.h"
#include "src/main/midboss/defeat_render.hpp"
#include "src/main/midboss/defeat_ring_geometry.hpp"
#pragma codeseg MID_DEFEAT_TEXT main_01

void near midboss_defeat_render(void)
{
    int i;
    subpixel_t radius;
    subpixel_t x;
    subpixel_t y;
    radius = midboss.phase_frame << MDR_SUBPIXEL_SHIFT;
    if(radius >= MDR_RING_MAX_RADIUS_PX * 16) {
        radius = MDR_RING_MAX_RADIUS_PX * 16;
        midboss_defeat_angle += MDR_ORBIT_ROTATION_PER_FRAME;
    }
    for(i = 0; i < MDR_ORBIT_SPRITE_COUNT; i++, midboss_defeat_angle += MDR_ORBIT_ANGLE_STEP) {
        x = polar_x(midboss.pos.cur.x.v, radius, midboss_defeat_angle);
        y = polar_y(midboss.pos.cur.y.v, radius, midboss_defeat_angle);
        if(y > -MDR_SPRITE_CLIP_MARGIN_PX * 16 && y < (MDR_MAX_CLIP_Y_PX + MDR_SPRITE_CLIP_MARGIN_PX) * 16 &&
            x > -MDR_SPRITE_CLIP_MARGIN_PX * 16 && x < (MDR_MAX_CLIP_X_PX + MDR_SPRITE_CLIP_MARGIN_PX) * 16) {
            x = (x >> MDR_SUBPIXEL_SHIFT) + MDR_SCREEN_X_OFFSET_PX;
            y = scroll_subpixel_y_to_vram_seg1(y);
            super_roll_put(x, y, midboss.sprite);
        }
    }
}
