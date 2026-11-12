// Complete natural initial Louise charge and alternating spread/stack patterns.
#include "src/main/boss/louise/patterns.hpp"
#include "src/main/boss/louise/scratch.hpp"
#include "src/main/boss/louise/charged_weapon_rules.hpp"

louise_charge_state_t pascal near louise_charge_update(int end_frame)
{
    if(boss.phase_frame >= LC_CHARGE_FIRST_FRAME) {
        if(boss.phase_frame < LC_CHARGE_INITIALIZE) {
            boss.sprite = LOUISE_SPRITE_CHARGE;
            gather_add_only_3stack(boss.phase_frame - LC_CHARGE_FIRST_FRAME, LC_CHARGE_COLOR_FIRST, LC_CHARGE_COLOR_SECOND);
            if(boss.phase_frame == LC_CHARGE_FIRST_FRAME) {
                snd_se_play(LC_CHARGE_SE);
            }
        } else {
            if(boss.phase_frame == LC_CHARGE_INITIALIZE) {
                boss.sprite = LOUISE_SPRITE_FIRE;
                return LOUISE_CHARGE_INITIALIZE;
            }
            if(boss.phase_frame < end_frame) {
                return LOUISE_CHARGE_FIRE;
            }
            return LOUISE_CHARGE_FINISH;
        }
    }
    return LOUISE_CHARGE_INACTIVE;
}

void near louise_pattern_blue_spreads(void)
{
    switch(louise_charge_update(LC_BLUE_PHASE_END)) {
    case LOUISE_CHARGE_INITIALIZE:
        bullet_template.spawn_type = BST_NORMAL;
        bullet_template.patnum = LOUISE_PAT_BALL_BLUE;
        bullet_template.group = BG_SPREAD;
        bullet_template.speed.v = louise_scratch.charge_speed;
        louise_set_spread(LC_BLUE_VOLLEY_COUNT, LC_BLUE_VOLLEY_STEP);
        bullet_template.special_motion = BSM_EXACT_LINEAR;
        louise_scratch.spread_or_laser_direction = LC_SWEEP_SIDE_MASK - louise_scratch.spread_or_laser_direction;
        if(louise_scratch.spread_or_laser_direction) {
            bullet_template.angle = LC_BLUE_ANGLE_LEFT;
        } else {
            bullet_template.angle = LC_BLUE_ANGLE_RIGHT;
        }
        bullet_template_tune();
        snd_se_play(LC_FIRE_SPRITE_SE);
        if(louise_scratch.charge_speed < LC_BLUE_MAX_SPEED) {
            louise_scratch.charge_speed += LC_CHARGE_SPEED_ADD;
        }
        // Initialization also emits the first pair on its even frame.
    case LOUISE_CHARGE_FIRE:
        if((boss.phase_frame % LC_BLUE_FIRE_INTERVAL) == 0) {
            bullets_add_regular();
            bullet_template.angle += LC_BLUE_OTHER_SIDE_ANGLE;
            bullets_add_regular();
            if(louise_scratch.spread_or_laser_direction) {
                bullet_template.angle += LC_BLUE_LEFT_SPIN_STEP;
            } else {
                bullet_template.angle += LC_BLUE_RIGHT_SPIN_STEP;
            }
            bullet_template.speed.v += LC_CHARGE_SPEED_ADD;
        }
        break;
    case LOUISE_CHARGE_FINISH:
        boss.mode = 0;
        boss.phase_frame = 0;
        boss.sprite = LOUISE_SPRITE_STILL;
        break;
    }
}

void near louise_pattern_red_stacks(void)
{
    switch(louise_charge_update(LC_RED_PHASE_END)) {
    case LOUISE_CHARGE_INITIALIZE:
        bullet_template.spawn_type =
            LOUISE_SPAWN_CLOUD_FORWARDS | LOUISE_SPAWN_NO_DECELERATE;
        bullet_template.patnum = LOUISE_PAT_V_RED;
        bullet_template.group = BG_STACK;
        bullet_template.speed.v = louise_speed(LC_RED_BASE_SPEED);
        louise_set_stack_for_rank(LC_RED_STACK_EASY, LC_RED_STACK_STEP_EASY, LC_RED_STACK_NORMAL, LC_RED_STACK_STEP_NORMAL,
            LC_RED_STACK_HARD, LC_RED_STACK_STEP_HARD, LC_RED_STACK_LUNATIC, LC_RED_STACK_STEP_LUNATIC);
        bullet_template.angle = static_cast<unsigned char>(LC_RED_STACK_INITIAL_ANGLE);
        break;
    case LOUISE_CHARGE_FIRE:
        if((boss.phase_frame % LC_RED_FIRE_INTERVAL) == 0) {
            bullets_add_regular();
            if(louise_scratch.spread_or_laser_direction) {
                bullet_template.angle -= LC_RED_TURN_ANGLE;
            } else {
                bullet_template.angle += LC_RED_TURN_ANGLE;
            }
            snd_se_play(LC_FIRE_SPRITE_SE);
        }
        break;
    case LOUISE_CHARGE_FINISH:
        boss.mode = 0;
        boss.phase_frame = 0;
        boss.sprite = LOUISE_SPRITE_STILL;
        break;
    }
}
