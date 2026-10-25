// Natural TH05 cache/hitshot renderer, using maintained TH04 rendering
// semantics and independently reviewed original TH05 records and behavior.
#pragma option -zCSHOT_RENDER_TEXT -zPmain_01
#include "src/main/player/shot_render.hpp"
#pragma codeseg SHOT_RENDER_TEXT main_01

void near shots_render(void)
{
    Shot near *shot;
    shot_alive_t near *alive;
    hitshot_t near *hitshot;
    int i;
    int sprite;

    _ES = SHOT_RENDER_VRAM_PLANE;
    grcg_setmode_rmw();
    for((alive = shots_alive, i = 0); i < shots_alive_count; (i++, alive++)) {
        if(alive->pos.x.v == SHOT_SUBPIXEL_NONE) {
            continue;
        }
        shot = alive->shot;
        // The original animation adds age parity within an unsigned byte;
        // carry never propagates into the high byte of the sprite number.
        sprite = static_cast<unsigned char>(
            static_cast<unsigned char>(shot->patnum_base) + (shot->age & 1));
        shot_render_tiny(
            (alive->pos.x.v >> 4) + SHOT_RENDER_LEFT - (SHOT_RENDER_W / 2),
            scroll_subpixel_y_to_vram_seg1(
                alive->pos.y.v + ((SHOT_RENDER_TOP - (SHOT_RENDER_H / 2)) * 16)),
            sprite);
    }

    for((hitshot = hitshots, i = 0); i < HITSHOT_COUNT; (i++, hitshot++)) {
        if((hitshot->age < (HITSHOT_FRAMES + 1)) && (hitshot->age > 0)) {
            sprite = hitshot->patnum;
            shot_render_tiny(
                (hitshot->pos.cur.x.v >> 4) + SHOT_RENDER_LEFT - (SHOT_RENDER_W / 2),
                scroll_subpixel_y_to_vram_seg1(
                    hitshot->pos.cur.y.v + ((SHOT_RENDER_TOP - (SHOT_RENDER_H / 2)) * 16)),
                sprite);
        }
    }
    outportb(0x7C, 0);
}
