// Complete Extra-stage twin: same real geometry/sprite algorithm as stage5.
// Geometry operations are expanded directly against the canonical fields.
#pragma option -zCMX_RENDER_TEXT -zPmain_01
#include "src/main/midboss/render5.hpp"
#pragma codeseg MX_RENDER_TEXT main_01

void pascal near midbossx_render(void)
{
    if(midboss.phase < MIDBOSS5_PHASE_EXPLODE_BIG) {
        if(midboss.pos.cur.y.v <
            ((MIDBOSS5_H / 2) - MIDBOSS5_PLAYFIELD_ROLL_MARGIN) * 16) {
            return;
        }
        int left = MIDBOSS5_PLAYFIELD_LEFT +
            (midboss.pos.cur.x.v >> 4) - (MIDBOSS5_W / 2);
        int top = scroll_subpixel_y_to_vram_seg1(
            midboss.pos.cur.y.v +
            (MIDBOSS5_PLAYFIELD_TOP - (MIDBOSS5_H / 2)) * 16
        );
        if(midboss.damage_this_frame == 0) {
            super_roll_put(left, top, midboss.sprite);
        } else {
            super_roll_put_1plane(left, top, midboss.sprite, 0, 0xFFC0);
            midboss.damage_this_frame = 0;
        }
    } else if(midboss.phase == MIDBOSS5_PHASE_EXPLODE_BIG) {
        midboss_defeat_render();
    }
}
