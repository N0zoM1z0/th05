// Candidate adapted from nmlgc/ReC98@b6ba5b0a; requires local cold replay.
#pragma option -zCBOSS_EXP_TEXT

#include <dos.h>
#include "src/main/boss/explosion_frame.h"
#include "src/main/boss/explosion.hpp"
#include "src/main/boss/explosion_choreography.hpp"

#define explosion_update(p) { \
    (p).radius_cur.x.v += (p).radius_delta.x.v; \
    (p).radius_cur.y.v += (p).radius_delta.y.v; \
    (p).age++; \
    if((p).age >= BEXP_LIFETIME_FRAMES) { \
        (p).alive = false; \
    } \
}

void near explosions_small_update_and_render(void)
{
    enum {
        SPRITE_W = BEXP_SMALL_SPRITE_W,
        SPRITE_H = BEXP_SMALL_SPRITE_H,
        SPRITES = BEXP_SMALL_RING_SPRITES
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
            angle += (BEXP_FULL_CIRCLE_ANGLE / SPRITES);

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
        SPRITE_W = BEXP_BIG_CLIP_ASSUMED_W,
        SPRITE_H = BEXP_BIG_CLIP_ASSUMED_H,
        SPRITES = BEXP_BIG_RING_SPRITES
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
            angle += (BEXP_FULL_CIRCLE_ANGLE / SPRITES);
        }
        explosion_update(p);

        frame++;
        if((frame < BEXP_BIG_FLASH_END_FRAME) && (frame & BEXP_BIG_ODD_FRAME_MASK)) {
            palette_settone_deferred(BEXP_BIG_FLASH_TONE);
        } else if((frame >= BEXP_BIG_FLASH_END_FRAME) && (frame < BEXP_BIG_FADE_END_FRAME)) {
            palette_settone_deferred(BEXP_BASE_TONE + (BEXP_BIG_FADE_END_FRAME * BEXP_FADE_TONE_PER_FRAME) - (frame * BEXP_FADE_TONE_PER_FRAME));
        } else {
            palette_settone_deferred(BEXP_BASE_TONE);
        }
    } else {
        frame = 0;
    }

    #undef frame
    #undef x_left
    #undef x_center
}

#undef explosion_update
