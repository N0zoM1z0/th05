// Boss movement: random flight within the clamp rectangle, and flying
// towards a target point. Adapted from ReC98's th05/main/boss/move.cpp.
#pragma option -zCmain_032_TEXT

#include "src/main/boss/movement.hpp"

// Higher = slower approach in boss_flystep_towards().
#define BMD_TOWARDS_DIVISOR 16

bool pascal near boss_flystep_random(int frame)
{
    if(frame == 0) {
        if(boss.pos.cur.x.v < BOSS_FLYSTEP_RANDOM_FIELD_LEFT) {
            boss.angle = randring2_next8_ge_lt(-0x30, +0x30);
        } else if(boss.pos.cur.x.v > BOSS_FLYSTEP_RANDOM_FIELD_RIGHT) {
            // ZUN bug: [0x30, 0x91) is not a power-of-two range, so masking
            // with 0x60 only ever yields 0x30, 0x50, 0x70 and 0x90.
            boss.angle = randring2_next8_and_ge_lt(+0x30, +0x91);
        } else {
            boss.angle = randring2_next16();
        }
        if(
            (boss_flystep_random_next_y_direction == Y_UP) && (boss.angle < 0x80) ||
            (boss_flystep_random_next_y_direction == Y_DOWN) && (boss.angle >= 0x80)
        ) {
            boss.angle = -boss.angle;
        }
        boss_flystep_random_next_y_direction = Y_ANY;
    }
    if(frame >= 0) {
        vector2_near(boss.pos.velocity, boss.angle, (to_sp(4.0f) - (frame * 2)));
        boss.pos.cur.x.v += boss.pos.velocity.x.v;
        boss.pos.cur.y.v += boss.pos.velocity.y.v;
        if(boss.pos.velocity.x.v < 0) {
            boss.sprite = boss_sprite_left;
        } else {
            boss.sprite = boss_sprite_right;
        }
        if(boss.pos.cur.y.v < boss_flystep_random_clamp.top.v) {
            boss.pos.cur.y.v = boss_flystep_random_clamp.top.v;
            boss_flystep_random_next_y_direction = Y_DOWN;
        } else if(boss.pos.cur.y.v > boss_flystep_random_clamp.bottom.v) {
            boss.pos.cur.y.v = boss_flystep_random_clamp.bottom.v;
            boss_flystep_random_next_y_direction = Y_UP;
        }
        if(boss.pos.cur.x.v < boss_flystep_random_clamp.left.v) {
            boss.pos.cur.x.v = boss_flystep_random_clamp.left.v;
        } else if(boss.pos.cur.x.v > boss_flystep_random_clamp.right.v) {
            boss.pos.cur.x.v = boss_flystep_random_clamp.right.v;
        }
        if(frame >= BOSS_FLYSTEP_RANDOM_FRAMES) {
            boss.sprite = boss_sprite_stay;
            return true;
        }
    }
    return false;
}

static const int TOWARDS_FRACTION = BMD_TOWARDS_DIVISOR;

inline int towards(int val, int speed = 1) {
    return (val / (TOWARDS_FRACTION / speed));
}

bool pascal near boss_flystep_towards(subpixel_t target_x, subpixel_t target_y)
{
    int reached_dimensions = 0;
    subpixel_t dist;

    dist = (target_x - boss.pos.cur.x.v);
    if(towards(dist) != 0) { boss.pos.cur.x.v += towards(dist); }
    else if(towards(dist, 4) != 0) { boss.pos.cur.x.v += towards(dist, 4); }
    else {
        boss.pos.cur.x.v = target_x;
        reached_dimensions++;
    }
    if(dist < 0) {
        boss.sprite = boss_sprite_left;
    } else {
        boss.sprite = boss_sprite_right;
    }

    dist = (target_y - boss.pos.cur.y.v);
    if(towards(dist) != 0) { boss.pos.cur.y.v += towards(dist); }
    else if(towards(dist, 8) != 0) { boss.pos.cur.y.v += towards(dist, 8); }
    else {
        boss.pos.cur.y.v = target_y;
        reached_dimensions++;
    }

    if(reached_dimensions != 2) {
        return false;
    }
    boss.sprite = boss_sprite_stay;
    return true;
}
