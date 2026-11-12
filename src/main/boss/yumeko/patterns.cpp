// Natural movement and attack behavior independently recovered from original
// TH05. ReC98 b6ba5b0a disassembly supports semantics, not source acceptance.
#ifndef TH05_YUMEKO_COMBINED_CONTEXT
#pragma option -zCB5_UPDATE_TEXT -zPmain_03
#endif
#include "src/main/boss/yumeko/patterns.hpp"
#include "src/main/boss/yumeko/final_ring_scratch.hpp"
#include "src/main/boss/yumeko/mobile_attack_rules.hpp"
#pragma codeseg B5_UPDATE_TEXT main_03

#define yumeko_fan_mirrored yumeko_fan_scratch.mirrored_side

// Both finite mobile attacks finish by entering genuine reposition mode
// and restarting the shared phase clock, without altering their own timers.
#define YUMEKO_PATTERNS_ENTER_REPOSITION() { \
    boss.phase_frame = 0; \
    boss.mode = YUMEKO_MODE_REPOSITION; \
}

// In the sword fan the same actual side flag mirrors the shot direction
// before the fire position is calculated, then restores the base direction.
#define YUMEKO_SWORD_FAN_MIRROR() \
    if(yumeko_fan_mirrored != YUMEKO_FAN_NORMAL_SIDE) { \
        sword_template.angle = YM_FAN_MIRROR_ANGLE - sword_template.angle; \
    }

bool pascal near yumeko_flystep_bounce(subpixel_t length, int end_frame)
{
    unsigned char angle;
    if(boss.phase_frame == YM_BOUNCE_START_FRAME) {
        angle = randring2_next16();
        vector2(boss.pos.velocity.x.v, boss.pos.velocity.y.v, angle, length);
        boss.sprite = YUMEKO_SPRITE_MOVE;
    }
    boss.pos.cur.x.v += boss.pos.velocity.x.v;
    boss.pos.cur.y.v += boss.pos.velocity.y.v;
    if((boss.pos.cur.x.v <= to_sp(YM_BOUNCE_LEFT_PX)) || (boss.pos.cur.x.v >= to_sp(YM_BOUNCE_RIGHT_PX))) {
        boss.pos.velocity.x.v *= YM_BOUNCE_REVERSE_SIGN;
    }
    if((boss.pos.cur.y.v <= to_sp(YM_BOUNCE_TOP_PX)) || (boss.pos.cur.y.v >= to_sp(YM_BOUNCE_BOTTOM_PX))) {
        boss.pos.velocity.y.v *= YM_BOUNCE_REVERSE_SIGN;
    }
    if(boss.phase_frame >= end_frame) {
        boss.sprite = YUMEKO_SPRITE_STILL;
        return true;
    }
    return false;
}

void near yumeko_pattern_sword_fan(void)
{
    if(boss.phase_frame == YM_FAN_CHARGE_FRAME) {
        boss.sprite = YUMEKO_SPRITE_CHARGE;
        sword_template.twirl_time = YM_FAN_TWIRL_FRAMES;
        sword_template.speed.v = YM_FAN_INITIAL_SPEED_SUBPX;
        sword_template.angle = YM_FAN_INITIAL_ANGLE;
        yumeko_fan_mirrored = randring2_next16_and(YM_FAN_RANDOM_SIDE_MASK);
        return;
    }
    if((boss.phase_frame > YM_FAN_FIRST_SHOT_AFTER) && ((boss.phase_frame % YM_FAN_SHOT_INTERVAL) == 0)) {
        YUMEKO_SWORD_FAN_MIRROR();
        vector2_at(sword_template.origin, boss.pos.cur.x.v, boss.pos.cur.y.v,
            to_sp(YM_FAN_RADIUS_PX), sword_template.angle);
        swords_add();
        YUMEKO_SWORD_FAN_MIRROR();
        sword_template.angle -= YM_FAN_ANGLE_STEP;
        if(sword_template.angle <= YM_FAN_STOP_ANGLE) {
            YUMEKO_PATTERNS_ENTER_REPOSITION();
        }
    }
}

void near yumeko_pattern_red_ring(void)
{
    if(boss.phase_frame < YM_RING_CHARGE_END_FRAME) {
        gather_add_only_3stack(
            boss.phase_frame - YM_RING_GATHER_LEAD_FRAMES,
            YM_RING_GATHER_FIRST_COLOR, YM_RING_GATHER_SECOND_COLOR);
        if(boss.phase_frame == YM_RING_CHARGE_SOUND_FRAME) {
            boss.sprite = YUMEKO_SPRITE_CHARGE;
            bullet_template.spawn_type = YUMEKO_CLOUD_BACKWARDS | YUMEKO_NO_DECELERATE;
            bullet_template.patnum = YUMEKO_BALL_RED;
            bullet_template.group = BG_RING;
            bullet_template.speed.v = YM_RING_SPEED_SUBPX;
            bullet_template.spread = YM_RING_BULLET_COUNT;
            bullet_template_tune();
            snd_se_play(YM_RING_CHARGE_SOUND);
        }
        return;
    }
    if((boss.phase_frame % YM_RING_FIRE_INTERVAL) == 0) {
        bullet_template.angle = randring2_next16();
        vector2_at(bullet_template.origin, boss.pos.cur.x.v, boss.pos.cur.y.v,
            randring2_next16_mod(to_sp(YM_RING_ORIGIN_JITTER_PX)), bullet_template.angle);
        bullets_add_regular();
        snd_se_play(YM_RING_FIRE_SOUND);
    }
    if(boss.phase_frame == YM_RING_END_FRAME) {
        YUMEKO_PATTERNS_ENTER_REPOSITION();
    }
}

#undef YUMEKO_SWORD_FAN_MIRROR
#undef YUMEKO_PATTERNS_ENTER_REPOSITION
