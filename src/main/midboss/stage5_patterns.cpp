// Complete natural movement and pattern prefix, original MAIN16724..168F2.
#include "src/main/midboss/stage5_patterns.hpp"
#include "src/main/midboss/stage5_scratch.hpp"
#include "src/main/midboss/stage5_attack_rules.hpp"

bool near midboss5_flystep(void)
{
    if(midboss.phase_frame == M5R_INITIAL_FLY_FRAME) {
        if((midboss5_scratch.horizontal_step == M5R_LEFT_STEP_INDEX) || (midboss5_scratch.horizontal_step == M5R_LAST_LEFT_STEP_INDEX)) {
            midboss.pos.velocity.x.v = to_sp(-M5R_DASH_SPEED_PX);
        } else {
            midboss.pos.velocity.x.v = to_sp(M5R_DASH_SPEED_PX);
        }
        midboss5_scratch.horizontal_step++;
        midboss5_scratch.horizontal_step &= M5R_STEP_INDEX_MASK;
    }
    midboss.pos.update_seg3();
    if(midboss.phase_frame >= M5R_DASH_FRAME_LIMIT) {
        return true;
    }
    return false;
}

void near midboss5_pattern_update(void)
{
    if(midboss.phase_frame < M5R_PATTERN_START_FRAME) {
        gather_add_only_3stack(midboss.phase_frame - M5R_CHARGE_FRAME, M5R_CHARGE_GATHER_FIRST_COLOR, M5R_CHARGE_GATHER_OTHER_COLOR);
        if(midboss.phase_frame == M5R_CHARGE_FRAME) {
            snd_se_play(M5R_CHARGE_SOUND);
        }
        if((midboss.phase_frame == M5R_SHOOT_SPRITE_FRAME_A) || (midboss.phase_frame == M5R_SHOOT_SPRITE_FRAME_B) ||
           (midboss.phase_frame == M5R_SHOOT_SPRITE_FRAME_C)) {
            midboss.sprite++;
        }
        bullet_template.angle = player_angle_from(
            midboss.pos.cur.x, midboss.pos.cur.y, M5R_ANGLE_FROM_PLAYER_EXTRA);
        return;
    }
    if((midboss.sprite < MIDBOSS5_SPRITE_SHOOT_LAST) &&
       ((midboss.phase_frame % M5R_SPRITE_ANIMATION_INTERVAL) == 0)) {
        midboss.sprite++;
    }
    if(midboss5_pattern_func()) {
        midboss.phase_frame = 0;
        midboss5_scratch.current_pattern_phase = 0;
        midboss.sprite = MIDBOSS5_SPRITE_CHARGE;
    }
}

bool near midboss5_pattern_blue_spread(void)
{
    if((midboss.phase_frame % M5R_BLUE_FIRE_INTERVAL) == 0) {
        bullet_template.spawn_type =
            MIDBOSS5_SPAWN_CLOUD_FORWARDS | MIDBOSS5_SPAWN_NO_DECELERATE;
        bullet_template.patnum = MIDBOSS5_PAT_BULLET_V_BLUE;
        bullet_template.speed.v = midboss5_speed(M5R_BLUE_SHOT_SPEED_PX);
        bullet_template.group = BG_SPREAD;
        midboss5_set_spread(M5R_BLUE_SPREAD_COUNT, M5R_BLUE_SPREAD_STEP);
        bullets_add_regular();
        snd_se_play(M5R_BLUE_FIRE_SOUND);
    }
    return (midboss.phase_frame >= M5R_BLUE_LAST_FRAME);
}

bool near midboss5_pattern_green_rings(void)
{
    if((midboss.phase_frame % M5R_GREEN_FIRE_INTERVAL) == 0) {
        bullet_template.spawn_type = MIDBOSS5_SPAWN_NO_DECELERATE;
        bullet_template.patnum = MIDBOSS5_PAT_BULLET_D_GREEN;
        bullet_template.speed.v = midboss5_speed(M5R_GREEN_SPEED_PX);
        bullet_template.group = BG_RING;
        bullet_template.spread = M5R_GREEN_RING_COUNT;
        bullet_template.origin.x.v +=
            randring2_next16_mod(to_sp(M5R_GREEN_POSITION_JITTER_PX)) - to_sp(M5R_GREEN_POSITION_BIAS_PX);
        bullet_template.origin.y.v +=
            randring2_next16_mod(to_sp(M5R_GREEN_POSITION_JITTER_PX)) - to_sp(M5R_GREEN_POSITION_BIAS_PX);
        bullet_template.angle = randring2_next16();
        bullets_add_regular();
        snd_se_play(3);
    }
    return (midboss.phase_frame >= M5R_GREEN_LAST_FRAME);
}

bool near midboss5_pattern_aimed_stacks(void)
{
    if(midboss.phase_frame == M5R_AIMED_FIRE_FRAME) {
        bullet_template.spawn_type =
            MIDBOSS5_SPAWN_CLOUD_FORWARDS | MIDBOSS5_SPAWN_NO_DECELERATE;
        bullet_template.patnum = M5R_AIMED_SPRITE_INDEX;
        bullet_template.group = BG_SPREAD_STACK_AIMED;
        bullet_template.angle = 0;
        midboss5_set_spread_stack(M5R_AIMED_SPREAD_COUNT, M5R_AIMED_SPREAD_STEP, M5R_AIMED_STACK_COUNT, M5R_AIMED_STACK_STEP);
        bullet_template.speed.v = midboss5_speed(M5R_AIMED_SPEED_PX);
        bullets_add_regular();
        bullet_template.group = BG_RING_STACK_AIMED;
        bullet_template.stack_speed_delta.v = midboss5_speed(M5R_AIMED_RING_STEP);
        bullet_template.spread = M5R_AIMED_RING_COUNT;
        bullets_add_regular();
        snd_se_play(M5R_AIMED_FIRE_SOUND);
    }
    return (midboss.phase_frame >= M5R_AIMED_LAST_FRAME);
}
