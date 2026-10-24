// Natural maintained TH04 player invalidation, with independently observed
// TH05 unsigned radius arithmetic and genuine complete point arguments.
#pragma option -zCPLAYER_INVALIDATE_TEXT -zPmain_01 -k-
#include "src/main/player/invalidate.hpp"
#pragma codeseg PLAYER_INVALIDATE_TEXT main_01

void near player_invalidate(void)
{
    unsigned char angle;
    register int i;
    register unsigned int radius;
    tile_invalidate_box.y = PLAYER_SPRITE_H;
    if(miss_time != 0) {
        tile_invalidate_box.x = MISS_EXPLOSION_W;
        radius = miss_explosion_radius - MISS_EXPLOSION_RADIUS_VELOCITY;
        i = 0;
        angle = miss_explosion_angle - MISS_EXPLOSION_ANGLE_VELOCITY;
        for(; i < MISS_EXPLOSION_COUNT;
            i++, angle += 256 / (MISS_EXPLOSION_COUNT / 2)) {
            if(i == MISS_EXPLOSION_COUNT / 2) {
                radius /= 2;
                angle = -angle;
            }
            vector2_at(drawpoint, player_pos.cur.x.v, player_pos.cur.y.v,
                static_cast<subpixel_t>(radius), angle);
            if((drawpoint.y.v < (PLAYFIELD_TOP - MISS_EXPLOSION_H / 2) * 16) ||
                (drawpoint.y.v >= (PLAYFIELD_BOTTOM - 8) * 16) ||
                (drawpoint.x.v < (PLAYFIELD_LEFT - 40) * 16) ||
                (drawpoint.x.v >= (PLAYFIELD_RIGHT - MISS_EXPLOSION_W / 2) * 16)) {
                continue;
            }
            reinterpret_cast<PlayerPointInvalidator>(
                &tiles_invalidate_around
            )(drawpoint);
        }
    } else {
        tile_invalidate_box.x = PLAYER_SPRITE_W;
        reinterpret_cast<PlayerPointInvalidator>(
            &tiles_invalidate_around
        )(player_pos.prev);
        tile_invalidate_box.x =
            PLAYER_OPTION_SPRITE_W + PLAYER_SPRITE_W + PLAYER_OPTION_SPRITE_W;
        tile_invalidate_box.y = PLAYER_OPTION_SPRITE_H;
        reinterpret_cast<PlayerPointInvalidator>(
            &tiles_invalidate_around
        )(player_option_pos_prev);
    }
}
