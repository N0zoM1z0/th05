// Candidate adapted from nmlgc/ReC98@b6ba5b0a; requires local cold replay.
#pragma option -zCBOSS_EXP_TEXT

#include <dos.h>
#include "src/main/boss/explosion.hpp"

#define explosion_update(p) { \
    (p).radius_cur.x.v += (p).radius_delta.x.v; \
    (p).radius_cur.y.v += (p).radius_delta.y.v; \
    (p).age++; \
    if((p).age >= 32) { \
        (p).alive = false; \
    } \
}

void near explosions_small_update_and_render(void)
{
    enum {
        SPRITE_W = 16,
        SPRITE_H = 16,
        SPRITES = 64
    };

    _ES = SEG_PLANE_B;
    grcg_setmode_rmw();

    Explosion near *p;
    int sprite;
    Subpixel center_x;
    Subpixel center_y;
    int i;

    for((p = explosions_small, i = 0); i < EXPLOSION_SMALL_COUNT; (i++, p++)) {
        if(!p->alive) {
            continue;
        }
        sprite = 0;
        unsigned char angle = 0x00;
        while(sprite < SPRITES) {
            #define left _AX
            #define top _DX

            center_x.v = polar_x(p->center.x, p->radius_cur.x, angle);
            center_y.v = polar_y(p->center.y, p->radius_cur.y, p->angle_y(angle));
            top = explosion_to_screen_top(center_y, SPRITE_H);
            left = explosion_to_screen_left(center_x, SPRITE_W);
            if(!explosion_clip_small(left, top, SPRITE_W, SPRITE_H)) {
                z_super_roll_put_tiny_16x16(left, top, PAT_EXPLOSION_SMALL);
            }
            sprite++;
            angle += (0x100 / SPRITES);

            #undef top
            #undef left
        }
        explosion_update(*p);
    }

    outportb(0x7c, 0);
}

void near explosions_big_update_and_render(void)
{
    enum {
        // Retain the original 64x64 assumption although the sprite is 48x48.
        SPRITE_W = 64,
        SPRITE_H = 64,
        SPRITES = 16
    };

    #define frame explosion_big_frame
    Explosion near &p = explosions_big;
    int sprite;

    subpixel_t x;
    #define x_center x
    #define x_left static_cast<int>(x)
    union { Subpixel center; int top; } y;

    if(p.alive) {
        sprite = 0;
        unsigned char angle = 0x00;
        while(sprite < SPRITES) {
            x_center = polar_x(p.center.x, p.radius_cur.x, angle);
            x_left = explosion_to_screen_left(x_center, SPRITE_W);
            y.center.v = polar_y(p.center.y, p.radius_cur.y, p.angle_y(angle));
            y.top = explosion_to_screen_top(y.center, SPRITE_H);
            if(!explosion_clip_large(x_left, y.top, SPRITE_W, SPRITE_H)) {
                super_put(x_left, y.top, PAT_EXPLOSION_BIG);
            }
            sprite++;
            angle += (0x100 / SPRITES);
        }
        explosion_update(p);

        frame++;
        if((frame < 8) && (frame & 1)) {
            palette_settone_deferred(150);
        } else if((frame >= 8) && (frame < 16)) {
            palette_settone_deferred(100 + (16 * 6) - (frame * 6));
        } else {
            palette_settone_deferred(100);
        }
    } else {
        frame = 0;
    }

    #undef frame
    #undef x_left
    #undef x_center
}

#undef explosion_update
