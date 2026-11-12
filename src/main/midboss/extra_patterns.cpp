// Natural TH05 Extra movement and attack semantics, independently recovered
// from the original target; ReC98 b6ba5b0a disassembly is behavior evidence.
#pragma option -zCMIDBOSSX_TEXT -zPmain_03
#include "src/main/midboss/extra_patterns.hpp"
#include "src/main/midboss/extra_scratch.hpp"
#include "src/main/midboss/extra_attack_rules.hpp"
#pragma codeseg MIDBOSSX_TEXT main_03

#define midbossx_ring_rotation midboss_extra_scratch.ring_rotation

bool pascal near midbossx_dash_update(int frame)
{
    if(frame >= MIDBOSSX_DASH_ANTICIPATION_FRAME) {
        if(frame < 0) {
            midboss.sprite = MEX_DASH_EARLY_SPRITE;
        } else if(frame < MIDBOSSX_DASH_MOVING_FRAMES) {
            if(frame == MEX_DASH_FIRST_ACTIVE_FRAME) {
                snd_se_play(MEX_DASH_START_SE);
            }
            frame *= MEX_DASH_MOVEMENT_CLOCK_SCALE;
            vector2_near(midboss.pos.velocity, midboss.angle, to_sp(MEX_DASH_VELOCITY_PX) - frame);
            midboss.pos.update_seg3();
            midboss.sprite = ((frame < MEX_DASH_FAST_SPRITE_BOUND) | (frame > MEX_DASH_SLOW_SPRITE_BOUND)) ? MEX_DASH_FACING_SPRITE : MEX_DASH_SPIN_SPRITE;
        } else if(frame < MIDBOSSX_DASH_ATTACK_START_FRAME) {
            if(frame == MIDBOSSX_DASH_MOVING_FRAMES) {
                snd_se_play(MEX_DASH_ATTACK_SE);
            }
            midboss.pos.prev = midboss.pos.cur;
            midboss.sprite = MEX_DASH_EARLY_SPRITE;
            midbossx_pattern();
        } else {
            midboss.sprite = MEX_DASH_ATTACK_SPRITE;
            return midbossx_pattern();
        }
    }
    return false;
}

bool near midbossx_pattern_wait(void)
{
    if(midboss.phase_frame >= MEX_WAIT_FINISH_FRAME) {
        return true;
    }
    return false;
}

bool near midbossx_pattern_spread(void)
{
    if(midboss.phase_frame == MIDBOSSX_RING_ROTATION_FRAME) {
        midbossx_ring_rotation = randring2_next16_and(MEX_RING_SIGN_RANDOM_MASK) ? MEX_RING_FORWARD_TURN : MEX_RING_REVERSE_TURN;
    }
    if(midboss.phase_frame <= MIDBOSSX_RING_ACTIVE_END_FRAME) {
        bullet_template.spawn_type = MEX_RING_NO_DECELERATE; // No deceleration.
        bullet_special.speed_delta.v = MEX_RING_SPEED_DELTA;
        bullet_template.special_motion = BSM_SPEEDUP;
        reinterpret_cast<uint16_t &>(bullet_template.spread) = (MEX_RING_SHOT_COUNT | (MEX_RING_ANGLE_STEP << 8));
        bullet_template.group = BG_RING;
        bullet_template.speed.v = MEX_RING_BASE_SPEED;
        bullet_template.patnum = MEX_RING_PATNUM;
        bullet_template.angle += midbossx_ring_rotation;
        bullets_add_special();
    }
    if(midboss.phase_frame >= MIDBOSSX_ATTACK_END_FRAME) {
        return true;
    }
    return false;
}

bool near midbossx_pattern_random(void)
{
    if(page_back != MEX_RANDOM_DISPLAY_PAGE) {
        bullet_template.spawn_type = MEX_RANDOM_REVERSE_CLOUD; // Forward cloud, no deceleration.
        bullet_template.group = BG_RANDOM_ANGLE_AND_SPEED;
        bullet_template.speed.v = MEX_RANDOM_BASE_SPEED;
        reinterpret_cast<uint16_t &>(bullet_template.spread) = (MEX_RANDOM_SHOT_COUNT | (MEX_RANDOM_SHOT_ANGLE_STEP << 8));
        bullet_template.patnum = MEX_RANDOM_PATNUM;
        bullets_add_regular();
    }
    if(midboss.phase_frame >= MIDBOSSX_ATTACK_END_FRAME) {
        return true;
    }
    return false;
}

bool near midbossx_pattern_decelerate(void)
{
    if((midboss.phase_frame % MEX_DECEL_VOLLEY_INTERVAL) == 0) {
        bullet_template.spawn_type = MEX_DECEL_BACKWARD_CLOUD; // Backward cloud, no deceleration.
        bullet_special.turns_max = MEX_DECEL_MAX_TURNS;
        bullet_template.special_motion = BSM_DECELERATE_THEN_TURN;
        bullet_template.group = BG_SPREAD_STACK;
        reinterpret_cast<uint32_t &>(bullet_template.spread) =
            (MEX_DECEL_SPREAD_COUNT | (MEX_DECEL_SPREAD_STEP << 8) | (MEX_DECEL_STACK_COUNT << 16) | (MEX_DECEL_STACK_SPEED_STEP << 24));
        bullet_template.speed.v = MEX_DECEL_BASE_SPEED;
        bullet_template.patnum = MEX_DECEL_PATNUM;
        bullet_template.angle = MEX_DECEL_LEFT_ANGLE;
        bullet_template_special_angle.turn_by = MEX_DECEL_LEFT_TURN;
        bullets_add_special();
        bullet_template.angle = MEX_DECEL_RIGHT_ANGLE;
        bullet_template_special_angle.turn_by = MEX_DECEL_RIGHT_TURN;
        bullets_add_special();
        snd_se_play(MEX_DECEL_FIRE_SE);
    }
    if(midboss.phase_frame >= MIDBOSSX_ATTACK_END_FRAME) {
        return true;
    }
    return false;
}
