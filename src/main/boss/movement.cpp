// Candidate adapted from nmlgc/ReC98@b6ba5b0a; not accepted before cold replay.
#pragma option -zCmain_032_TEXT

#include "src/main/boss/movement.hpp"
#include "src/main/boss/movement_dynamics.hpp"

bool pascal near boss_flystep_random(int frame)
{
    if(frame == BMD_FIRST_MOTION_FRAME) {
        if(boss.pos.cur.x.v < BOSS_FLYSTEP_RANDOM_FIELD_LEFT) {
            boss.angle = randring2_next8_ge_lt(BMD_RAND_LEFT_MIN_ANGLE, BMD_RAND_LEFT_MAX_ANGLE);
        } else if(boss.pos.cur.x.v > BOSS_FLYSTEP_RANDOM_FIELD_RIGHT) {
            // Preserve the original AND selection even though this is not
            // a power-of-two interval.
            boss.angle = randring2_next8_and_ge_lt(BMD_RAND_RIGHT_MIN_ANGLE, BMD_RAND_RIGHT_MAX_ANGLE);
        } else {
            boss.angle = randring2_next16();
        }
        if(
            (boss_flystep_random_next_y_direction == Y_UP) && (boss.angle < BMD_VERTICAL_SPLIT_ANGLE) ||
            (boss_flystep_random_next_y_direction == Y_DOWN) && (boss.angle >= BMD_VERTICAL_SPLIT_ANGLE)
        ) {
            boss.angle = -boss.angle;
        }
        boss_flystep_random_next_y_direction = Y_ANY;
    }
    if(frame >= BMD_FIRST_MOTION_FRAME) {
        vector2_near(boss.pos.velocity, boss.angle, (to_sp(BMD_INITIAL_RANDOM_SPEED_PX) - (frame * BMD_RANDOM_DECEL_SUBPX)));
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

inline int towards(int val, int speed = BMD_TOWARDS_DEFAULT_SPEED) {
    return (val / (TOWARDS_FRACTION / speed));
}

bool pascal near boss_flystep_towards(subpixel_t target_x, subpixel_t target_y)
{
    int reached_dimensions = 0;
    subpixel_t dist;

    dist = (target_x - boss.pos.cur.x.v);
    if(towards(dist) != 0) { boss.pos.cur.x.v += towards(dist); }
    else if(towards(dist, BMD_TOWARDS_FINE_X_SPEED) != 0) { boss.pos.cur.x.v += towards(dist, BMD_TOWARDS_FINE_X_SPEED); }
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
    else if(towards(dist, BMD_TOWARDS_FINE_Y_SPEED) != 0) { boss.pos.cur.y.v += towards(dist, BMD_TOWARDS_FINE_Y_SPEED); }
    else {
        boss.pos.cur.y.v = target_y;
        reached_dimensions++;
    }

    if(reached_dimensions != BMD_REACHED_DIMENSIONS) {
        return false;
    }
    boss.sprite = boss_sprite_stay;
    return true;
}
