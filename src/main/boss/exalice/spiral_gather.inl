#include "src/main/boss/exalice/final_attack_rules.hpp"
#include "src/main/boss/exalice/boss_scratch.hpp"
bool near exalice_pattern_spiral_gather(void)
{
    bullet_template.origin.y.v += to_sp(EXF_SPIRAL_ORIGIN_Y_OFFSET_PX);
    gather_template.center.x.v = bullet_template.origin.x.v = exalice_sweep_x;
    if(boss.phase_frame == EXF_SPIRAL_INIT_FRAME) {
        cheeto_template.angle = static_cast<unsigned char>(EXF_SPIRAL_CHEETO_INIT_ANGLE);
        bullet_template.angle = EXF_SPIRAL_BULLET_INIT_ANGLE;
        cheeto_template.speed.v = to_sp(EXF_SPIRAL_CHEETO_SPEED_PX);
        bullet_template.speed.v = to_sp(EXF_SPIRAL_BULLET_SPEED_PX);
        bullet_template.spawn_type = 0x02 | 0x10;
        bullet_template.group = BG_SPREAD;
        exalice_set_spread(EXF_SPIRAL_SPREAD_COUNT, EXF_SPIRAL_SPREAD_STEP);
        bullet_template.patnum = EXF_SPIRAL_PATNUM;
        exalice_boss_scratch.pattern_byte15.spiral_angle_offset = 0;
        exalice_boss_scratch.later_pattern_state.spiral.acceleration_step = 0;
        exalice_boss_scratch.later_pattern_state.spiral.turn_phase = 0;
        snd_se_play(EXF_SPIRAL_GATHER_SE);
    }
    if(boss.phase_frame < EXF_SPIRAL_RISE_FRAME) {
        if((boss.phase_frame % EXF_SPIRAL_GATHER_INTERVAL) == 0) {
            gather_template.col = EXF_SPIRAL_GATHER_COLOR;
            gather_template.center.y = bullet_template.origin.y;
            gather_template.radius.v = to_sp(EXF_SPIRAL_GATHER_RADIUS_PX);
            if((boss.phase_frame % EXF_SPIRAL_GATHER_ROTATE_INTERVAL) == 0) {
                gather_template.angle_delta = EXF_SPIRAL_GATHER_STEP;
            } else {
                gather_template.angle_delta = static_cast<unsigned char>(-EXF_SPIRAL_GATHER_STEP);
            }
            gather_add_only();
        }
    } else if((boss.phase_frame % EXF_SPIRAL_SHOT_CADENCE) == 0) {
        if((boss.phase_frame % EXF_SPIRAL_GATHER_ROTATE_INTERVAL) == 0) {
            gather_template.center.y = bullet_template.origin.y;
            gather_template.radius.v = to_sp(EXF_SPIRAL_GATHER_SHORT_RADIUS_PX);
            if((boss.phase_frame % EXF_SPIRAL_GATHER_ALT_INTERVAL) == 0) {
                gather_template.angle_delta = EXF_SPIRAL_GATHER_STEP;
            } else {
                gather_template.angle_delta = static_cast<unsigned char>(-EXF_SPIRAL_GATHER_STEP);
            }
            gather_add_only();
        }
        bullet_template.angle = EXF_SPIRAL_MIRROR_ANGLE - bullet_template.angle;
        bullets_add_regular_fixedspeed();
        bullet_template.angle = EXF_SPIRAL_MIRROR_ANGLE - bullet_template.angle;
        bullets_add_regular_fixedspeed();
        snd_se_play(EXF_SPIRAL_SHOT_SE);
        bullet_template.angle -= exalice_boss_scratch.pattern_byte15.spiral_angle_offset;
        if((boss.phase_frame % EXF_SPIRAL_GATHER_ALT_INTERVAL) == 0) {
            exalice_boss_scratch.pattern_byte15.spiral_angle_offset += exalice_boss_scratch.later_pattern_state.spiral.acceleration_step;
            if(exalice_boss_scratch.later_pattern_state.spiral.turn_phase == 0) {
                exalice_boss_scratch.later_pattern_state.spiral.acceleration_step++;
                if(exalice_boss_scratch.later_pattern_state.spiral.acceleration_step >= EXF_SPIRAL_TURN_LIMIT) {
                    exalice_boss_scratch.later_pattern_state.spiral.turn_phase++;
                }
            } else {
                exalice_boss_scratch.later_pattern_state.spiral.acceleration_step--;
                if(exalice_boss_scratch.later_pattern_state.spiral.acceleration_step == 0) {
                    exalice_sweep_x = player_pos.cur.x;
                    return true;
                }
            }
        }
    }
    return false;
}
