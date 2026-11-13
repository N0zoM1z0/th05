// Complete final EX-Alice patterns, preserving actual signed frame arithmetic.
#pragma option -zCEXALICE_FIN_TEXT -zPmain_03
#include "src/main/boss/exalice/final_patterns.hpp"
#include "src/main/boss/exalice/update_phases.hpp"
#include "src/main/boss/exalice/final_attack_rules.hpp"
#include "src/main/boss/exalice/boss_scratch.hpp"

// Cross and turning Cheetos use the same real aim-and-fire flow. Each
// caller supplies its own 16/128-frame flip clock and forward/reverse aim.
// Keep the player-angle call, actual spawn and sound in their native order.
#define EXALICE_AIM_AND_FIRE_CHEETO(flip_period, aim, reverse_aim) { \
    if((boss.phase_frame % flip_period) == 0) { \
        cheeto_template.angle = player_angle_from( \
            cheeto_template.origin.x, cheeto_template.origin.y, aim); \
    } else { \
        cheeto_template.angle = player_angle_from( \
            cheeto_template.origin.x, cheeto_template.origin.y, \
            static_cast<unsigned char>(reverse_aim)); \
    } \
    cheetos_add(); \
    snd_se_play(EXF_CHEETO_SHOT_SE); \
}

bool near exalice_pattern_cross_cheetos(void)
{
    if((boss.phase_frame % EXF_CROSS_BULLET_CADENCE) == 0) {
        bullet_template.speed.v = to_sp(EXF_CROSS_BULLET_SPEED_PX);
        bullet_template.spawn_type = 0x02 | 0x10;
        bullet_template.group = BG_SPREAD_AIMED;
        bullet_template.patnum = EXF_CROSS_BULLET_PATNUM;
        bullet_template.angle = 0;
        exalice_set_spread(EXF_CROSS_SPREAD_COUNT, EXF_CROSS_SPREAD_STEP);
        bullets_add_regular();
        if((boss.phase_frame % EXF_CROSS_CHEETO_CADENCE) == 0) {
            cheeto_template.col = EXF_CROSS_CHEETO_COLOR;
            cheeto_template.speed.v = to_sp(EXF_CROSS_CHEETO_SPEED_PX);
            EXALICE_AIM_AND_FIRE_CHEETO(EXF_CROSS_CHEETO_FLIP_PERIOD, EXF_CROSS_CHEETO_AIM, EXF_CROSS_CHEETO_AIM_REVERSE);
        }
    }
    return (boss.phase_frame == EXF_CROSS_DONE_FRAME);
}

bool near exalice_pattern_turning_cheetos(void)
{
    if((boss.phase_frame % EXF_TURN_CHEETO_CADENCE) == 0) {
        cheeto_template.col = EXF_CROSS_CHEETO_COLOR;
        cheeto_template.speed.v = to_sp(EXF_TURN_CHEETO_SPEED_PX);
        EXALICE_AIM_AND_FIRE_CHEETO(EXF_TURN_CHEETO_FLIP_CADENCE, EXF_TURN_CHEETO_AIM, EXF_TURN_CHEETO_REVERSE);
    }
    boss_flystep_random(boss.phase_frame % EXF_TURN_FLYSTEP_PERIOD);
    return (boss.phase_frame == EXF_TURN_DONE_FRAME);
}

#include "src/main/boss/exalice/spiral_gather.inl"

// The controller calls this leaf before its inclusive frame-5000 HP gate.
// Its two-frame cadence therefore emits a real volley on frame 5000 itself.
void near exalice_pattern_final_fan(void)
{
    gather_add_only_3stack(boss.phase_frame - EXF_FAN_CHARGE_FRAME, EXF_FAN_BLUE_GATHER_COLOR, EXF_FAN_OTHER_GATHER_COLOR);
    if(boss.phase_frame == EXF_FAN_CHARGE_FRAME) {
        boss.sprite = EXF_FAN_SPRITE;
        snd_se_play(EXF_FAN_CHARGE_SE);
        bullet_template.patnum = EXF_FAN_BULLET_PATNUM;
        bullet_template.group = BG_SPREAD;
        bullet_template.angle = randring2_next16();
        exalice_set_spread(EXF_FAN_SPREAD_COUNT, EXF_FAN_SPREAD_STEP);
        exalice_boss_scratch.pattern_byte15.final_fan_angle = 0;
        boss.pos.velocity.x.v = 0;
    }
    if(boss.phase_frame >= EXF_FAN_FIRE_START) {
        if((boss.phase_frame % EXF_FAN_FIRE_CADENCE) == 0) {
            bullet_template.speed.v =
                (static_cast<unsigned long>(EXALICE_HP_WAVE4_REGULAR_END - boss.hp) * EXF_FAN_HP_SPEED_SCALE / EXALICE_HP_WAVE4_REGULAR_END) + to_sp(EXF_FAN_MIN_SPEED_PX);
            bullets_add_regular();
            bullet_template.angle += EXF_FAN_OPPOSITE_ANGLE;
            bullets_add_regular();
            bullet_template.angle += EXF_FAN_ROTATION_STEP;
            snd_se_play(EXF_FAN_VOLLEY_SE);
        }
        boss.pos.cur.x.v = polar(to_sp(EXF_FAN_CENTER_X_PX), boss.pos.velocity.x.v,
            SinTable8[exalice_boss_scratch.pattern_byte15.final_fan_angle]);
        exalice_boss_scratch.pattern_byte15.final_fan_angle += EXF_FAN_ANGLE_STEP;
        // The radius spans64 pixels, converted to16 subpixels per pixel.
        boss.pos.velocity.x.v =
            ((static_cast<unsigned long>(EXALICE_HP_WAVE4_REGULAR_END - boss.hp) * EXF_FAN_RADIUS_SCALE_PX) * 16) / EXALICE_HP_WAVE4_REGULAR_END;
    }
}

#undef EXALICE_AIM_AND_FIRE_CHEETO
