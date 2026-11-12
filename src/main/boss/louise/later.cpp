// Four complete natural patterns immediately before the original Louise update.
#include "src/main/boss/louise/later.hpp"
#include "src/main/boss/louise/scratch.hpp"
#include "src/main/boss/louise/charged_weapon_rules.hpp"

// The alternating mirror fan has two initial axes but one identical shot
// sequence. Keep every byte-speed update and shot call in its original order.
#define LOUISE_MIRROR_FAN(first_angle, reflect_axis) { \
    bullet_template.angle = first_angle; \
    for(i = 0; i < LC_MIRROR_COUNT; i++) { \
        saved_angle = bullet_template.angle; \
        bullets_add_regular(); \
        bullet_template.angle += LC_MIRROR_ANGLE; \
        bullets_add_regular(); \
        bullet_template.angle = reflect_axis - bullet_template.angle; \
        bullets_add_regular(); \
        bullet_template.angle += LC_MIRROR_ANGLE; \
        bullets_add_regular(); \
        bullet_template.angle = saved_angle; \
        bullet_template.speed.v = bullet_template.speed.v + static_cast<subpixel_length_8_t>(-louise_speed(LC_MIRROR_SPEED_DECAY)); \
        bullet_template.angle += LC_MIRROR_SWEEP_STEP; \
    } \
}

void near louise_pattern_mirrored_fans(void)
{
    int i;
    unsigned char saved_angle;
    if((boss.phase_frame % LC_MIRROR_INTERVAL) == 0) {
        bullet_template.spawn_type = LOUISE_SPAWN_CLOUD_BACKWARDS;
        bullet_template.group = BG_SINGLE;
        bullet_template.patnum = 0;
        bullet_template_tune();
        bullet_template.speed.v = louise_speed(LC_MIRROR_BASE_SPEED);
        if((boss.phase_frame % LC_MIRROR_HALF_INTERVAL) == 0) {
            LOUISE_MIRROR_FAN(LC_MIRROR_FIRST_ANGLE, LC_MIRROR_FIRST_AXIS);
        } else {
            LOUISE_MIRROR_FAN(LC_MIRROR_SECOND_ANGLE, LC_MIRROR_SECOND_AXIS);
        }
    }
}

void near louise_pattern_sweeping_lasers(void)
{
    switch(louise_charge_update(LC_SWEEP_PHASE_END)) {
    case LOUISE_CHARGE_INITIALIZE:
        laser_template.coords.origin = boss.pos.cur;
        laser_template.coords.width.nonshrink = LC_SWEEP_WIDTH;
        laser_template.col = LC_SWEEP_COLOR;
        laser_template.coords.angle = static_cast<unsigned char>(LC_SWEEP_INITIAL_ANGLE);
        laser_template.active_at_age.moveout = LC_SWEEP_MOVEOUT;
        laser_template.shootout_speed.v = to_sp(LC_SWEEP_SPEED);
        louise_scratch.spread_or_laser_direction = randring2_next16_and(LC_SWEEP_SIDE_MASK);
        // Initialization also launches at its real even four-frame boundary.
    case LOUISE_CHARGE_FIRE:
        if((laser_template.coords.angle >= LC_SWEEP_ANGLE_UPPER) ||
           (laser_template.coords.angle <= LC_SWEEP_ANGLE_LOWER)) {
            if((boss.phase_frame % LC_SWEEP_FIRE_INTERVAL) == 0) {
                if(louise_scratch.spread_or_laser_direction) {
                    lasers_shootout_add();
                } else {
                    laser_template.coords.angle = LC_SWEEP_MIRROR - laser_template.coords.angle;
                    lasers_shootout_add();
                    laser_template.coords.angle = LC_SWEEP_MIRROR - laser_template.coords.angle;
                }
                laser_template.coords.angle += LC_SWEEP_TURN_STEP;
            }
        }
        break;
    case LOUISE_CHARGE_FINISH:
        boss.mode = 0;
        boss.phase_frame = 0;
        boss.sprite = LOUISE_SPRITE_STILL;
        break;
    }
}

void near louise_pattern_turning_rings(void)
{
    switch(louise_charge_update(LC_BLUE_PHASE_END)) {
    case LOUISE_CHARGE_INITIALIZE:
        bullet_template.spawn_type =
            LOUISE_SPAWN_CLOUD_FORWARDS | LOUISE_SPAWN_NO_DECELERATE;
        bullet_template.patnum = LOUISE_PAT_V_RED;
        bullet_template.group = BG_RING_STACK_AIMED;
        bullet_template.speed.v = louise_scratch.charge_speed;
        if(louise_scratch.charge_speed < LC_RED_MAX_SPEED) {
            louise_scratch.charge_speed += LC_CHARGE_SPEED_ADD;
        }
        louise_set_spread_stack(LC_TURN_RING_SPREAD, LC_TURN_RING_ANGLE_STEP, LC_TURN_RING_STACK, LC_TURN_RING_SPEED_STEP);
        bullet_template.angle = 0;
        bullet_template.special_motion = BSM_DECELERATE_THEN_TURN;
        bullet_special.turns_max = LC_TURN_RING_MAX_TURNS;
        if(randring2_next16_and(LC_TURN_RING_RANDOM_SIDE)) {
            bullet_template_special_angle.turn_by = LC_TURN_RING_CLOCKWISE;
        } else {
            bullet_template_special_angle.turn_by = static_cast<unsigned char>(LC_TURN_RING_COUNTERCLOCKWISE);
        }
        bullet_template_tune();
        snd_se_play(LC_FIRE_SPRITE_SE);
        bullets_add_special();
        break;
    case LOUISE_CHARGE_FINISH:
        boss.mode = 0;
        boss.phase_frame = 0;
        boss.sprite = LOUISE_SPRITE_STILL;
        break;
    }
}

void near louise_pattern_aimed_pellets(void)
{
    if((boss.phase_frame % LC_PELLET_FIRE_INTERVAL) == 0) {
        bullet_template.spawn_type =
            LOUISE_SPAWN_CLOUD_FORWARDS | LOUISE_SPAWN_NO_DECELERATE;
        bullet_template.group = BG_SPREAD_AIMED;
        bullet_template.patnum = 0;
        bullet_template.special_motion = BSM_EXACT_LINEAR;
        bullet_template.speed.v = louise_speed(LC_PELLET_BASE_SPEED);
        louise_set_spread(LC_PELLET_SPREAD_COUNT, LC_PELLET_SPREAD_STEP);
        bullet_template_tune();
        if((boss.phase_frame % LC_PELLET_SIDE_INTERVAL) == 0) {
            bullet_template.angle = LC_PELLET_AIM_LEFT;
        } else {
            bullet_template.angle = static_cast<unsigned char>(LC_PELLET_AIM_RIGHT);
        }
        bullets_add_special();
        snd_se_play(LC_PELLET_SOUND);
    }
}

#undef LOUISE_MIRROR_FAN
