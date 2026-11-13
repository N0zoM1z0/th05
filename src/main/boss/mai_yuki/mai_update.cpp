// Complete Mai solo state machine, including the compiler's switch table.
#pragma option -zCMAI_UPDATE_TEXT -zPmain_03
#include "src/main/boss/mai_yuki/mai_update.hpp"
#include "src/main/boss/mai_yuki/solo_scratch.hpp"
#include "src/main/boss/mai_yuki/mai_solo_choreography.hpp"
#include "src/main/boss/mai_yuki/solo_wave_common.hpp"
// Canonical object types are complete before the compiler table alignment.
#pragma codeseg MAI_UPDATE_TEXT main_03
#pragma option -a2

// The native ten-stage solo Boss switch and two alternating attack modes.
static const unsigned char MAI_SOLO_PHASE_SETUP = 0;
static const unsigned char MAI_SOLO_PHASE_READY = 1;
static const unsigned char MAI_SOLO_PHASE_ENTRANCE = 2;
static const unsigned char MAI_SOLO_PHASE_WAVE_FIRST = 3;
static const unsigned char MAI_SOLO_PHASE_LASER_APPROACH = 4;
static const unsigned char MAI_SOLO_PHASE_LASER_CYCLE = 5;
static const unsigned char MAI_SOLO_PHASE_WAVE_MIDDLE_APPROACH = 6;
static const unsigned char MAI_SOLO_PHASE_WAVE_MIDDLE = 7;
static const unsigned char MAI_SOLO_PHASE_FINAL_APPROACH = 8;
static const unsigned char MAI_SOLO_PHASE_WAVE_FINAL = 9;
static const unsigned char MAI_SOLO_MODE_REPOSITION = 0;
static const unsigned char MAI_SOLO_MODE_ATTACK = 1;
static const unsigned char MAI_SOLO_PHASE_DEFEAT = 253;
static const unsigned char MAI_SOLO_WAVE_FIRST_LIMIT = 36;
static const unsigned char MAI_SOLO_WAVE_MIDDLE_LIMIT = 36;
static const unsigned char MAI_SOLO_WAVE_FINAL_LIMIT = 20;

extern "C" void pascal far mai_update(void)
{
    int i;
    homing_target = boss.pos.cur;
    bullet_template.origin = boss.pos.cur;
    gather_template.center = boss.pos.cur;
    laser_template.coords.origin = boss.pos.cur;
    b4ball_template.origin = boss.pos.cur;
    boss.phase_frame++;

    switch(boss.phase) {
    case MAI_SOLO_PHASE_SETUP:
        if(boss.phase_frame == MAI_SOLO_FIRST_FRAME) {
            boss.hp = MAI_SOLO_HP_TOTAL;
            boss.phase_end_hp = MAI_SOLO_HP_SETUP_GATE;
            gather_template.radius.v = to_sp(MAI_SOLO_GATHER_RADIUS_PX);
            gather_template.angle_delta = MAI_SOLO_GATHER_ANGLE_DELTA;
            gather_template.ring_points = MAI_SOLO_GATHER_RING_POINTS;
            boss.sprite = MAI_SOLO_SPRITE_STILL;
            boss_sprite_left = MAI_SOLO_SPRITE_MOVE_LEFT;
            boss_sprite_right = MAI_SOLO_SPRITE_MOVE_RIGHT;
            boss_sprite_stay = MAI_SOLO_SPRITE_STILL;
            b4ball_template.patnum_tiny_base = MAI_SOLO_BALL_FIRST_SPRITE;
        }
        boss_hittest_shots_invincible();
        if(boss.phase_frame >= MAI_SOLO_HP_FILL_FRAMES) {
            boss.phase++;
            boss.phase_frame = 0;
            snd_se_play(MAI_SOLO_ENTRY_SOUND);
            bg_render_bombing_func = mai_yuki_bg_render;
        }
        break;
    case MAI_SOLO_PHASE_READY:
        boss_hittest_shots_invincible();
        if(boss.phase_frame >= MAI_SOLO_READY_FRAMES) {
            boss.sprite = MAI_SOLO_SPRITE_READY;
            boss.phase++;
            boss.phase_frame = 0;
            boss_custombullets_render = b4balls_render;
        }
        break;
    case MAI_SOLO_PHASE_ENTRANCE:
        boss_hittest_shots_invincible();
        if(boss_flystep_towards(to_sp(MAI_SOLO_CENTER_X_PX), to_sp(MAI_SOLO_CENTER_Y_PX))) {
            boss.sprite = MAI_SOLO_SPRITE_ATTACK_STILL;
            boss.phase++;
            boss.phase_frame = 0;
            boss.mode = MAI_SOLO_MODE_ATTACK;
            boss.phase_state.patterns_seen = 0;
            boss_explode_small(ET_VERTICAL);
            circles_add_growing(boss.pos.cur.x, boss.pos.cur.y);
            boss_solo_pattern_current = mai_solo_widening_fans;
            boss_sprite_left = MAI_SOLO_SPRITE_ATTACK_LEFT;
            boss_sprite_right = MAI_SOLO_SPRITE_ATTACK_RIGHT;
            boss_sprite_stay = MAI_SOLO_SPRITE_ATTACK_STILL;
        }
        break;
    case MAI_SOLO_PHASE_WAVE_FIRST:
        switch(boss.mode) {
        case MAI_SOLO_MODE_REPOSITION:
            if(boss_flystep_random(boss.phase_frame - MAI_SOLO_REPOSITION_LEAD_FRAMES)) {
                MY_SOLO_NEXT_PATTERN();
                if(boss.phase_state.patterns_seen >= MAI_SOLO_WAVE_FIRST_LIMIT) {
                    goto phase3_complete;
                }
                boss_solo_pattern_current = mai_solo_pattern_pair_first[
                    boss.phase_state.patterns_seen & MAI_SOLO_PATTERN_PARITY_MASK];
            }
            break;
        case MAI_SOLO_MODE_ATTACK:
            boss_solo_pattern_current();
            break;
        }
        MY_SOLO_HIT_BONUS_OR_BREAK(MAI_SOLO_HIT_SCORE_BONUS);
phase3_complete:
        boss_phase_next(ET_NW_SE, MAI_SOLO_HP_FIRST_WAVE_END);
        break;
    case MAI_SOLO_PHASE_LASER_APPROACH:
        boss_hittest_shots();
        if(boss_flystep_towards(to_sp(MAI_SOLO_CENTER_X_PX), to_sp(MAI_SOLO_LASER_APPROACH_Y_PX))) {
            boss.phase++;
            boss.phase_frame = 0;
        }
        break;
    case MAI_SOLO_PHASE_LASER_CYCLE:
        mai_solo_laser_cycle();
        if(boss.phase_frame < MAI_SOLO_LASER_TIMEOUT_FRAMES) {
            if(!boss_hittest_shots()) {
                break;
            }
            boss_score_bonus(MAI_SOLO_HIT_SCORE_BONUS);
        }
        for(i = 0; i < MAI_SOLO_LASER_STOP_COUNT; i++) {
            laser_stop(i);
        }
        boss_phase_next(ET_HORIZONTAL, MAI_SOLO_HP_LASER_CYCLE_END);
        break;
    case MAI_SOLO_PHASE_WAVE_MIDDLE_APPROACH:
        boss_hittest_shots();
        if(boss_flystep_towards(to_sp(MAI_SOLO_CENTER_X_PX), to_sp(MAI_SOLO_CENTER_Y_PX))) {
            goto movement_complete;
        }
        break;
    case MAI_SOLO_PHASE_WAVE_MIDDLE:
        switch(boss.mode) {
        case MAI_SOLO_MODE_REPOSITION:
            if(boss_flystep_random(boss.phase_frame - MAI_SOLO_REPOSITION_LEAD_FRAMES)) {
                MY_SOLO_NEXT_PATTERN();
                if(boss.phase_state.patterns_seen >= MAI_SOLO_WAVE_MIDDLE_LIMIT) {
                    goto phase7_complete;
                }
                boss_solo_pattern_current = mai_solo_pattern_pair_middle[
                    boss.phase_state.patterns_seen & MAI_SOLO_PATTERN_PARITY_MASK];
            }
            break;
        case MAI_SOLO_MODE_ATTACK:
            boss_solo_pattern_current();
            break;
        }
        MY_SOLO_HIT_BONUS_OR_BREAK(MAI_SOLO_HIT_SCORE_BONUS);
phase7_complete:
        boss_phase_next(ET_NW_SE, MAI_SOLO_HP_MIDDLE_WAVE_END);
        break;
    case MAI_SOLO_PHASE_FINAL_APPROACH:
        boss_hittest_shots();
        if(boss_flystep_towards(to_sp(MAI_SOLO_CENTER_X_PX), to_sp(MAI_SOLO_CENTER_Y_PX))) {
movement_complete:
            boss.phase++;
            boss.phase_frame = 0;
            mai_solo_scratch.pattern_byte10.revenge_snow_angle = MAI_SOLO_REVENGE_SNOW_ANGLE;
            mai_solo_scratch.revenge_snow_step = static_cast<unsigned char>(MAI_SOLO_REVENGE_SNOW_SIGNED_STEP);
        }
        break;
    case MAI_SOLO_PHASE_WAVE_FINAL:
        switch(boss.mode) {
        case MAI_SOLO_MODE_REPOSITION:
            if(boss_flystep_random(boss.phase_frame - MAI_SOLO_FINAL_REPOSITION_LEAD_FRAMES)) {
                MY_SOLO_NEXT_PATTERN();
                if(boss.phase_state.patterns_seen >= MAI_SOLO_WAVE_FINAL_LIMIT) {
                    boss.phase_state.defeat_bonus = false;
                    goto defeat;
                }
                boss_solo_pattern_current = mai_solo_pattern_pair_final[
                    boss.phase_state.patterns_seen & MAI_SOLO_PATTERN_PARITY_MASK];
            }
            break;
        case MAI_SOLO_MODE_ATTACK:
            boss_solo_pattern_current();
            break;
        }
        if(!boss_hittest_shots()) {
            break;
        }
        boss.phase_state.defeat_bonus = true;
defeat:
        boss_explode_small(ET_VERTICAL);
        boss.phase_frame = 0;
        boss.phase = MAI_SOLO_PHASE_DEFEAT;
        b4balls_reset();
        boss_custombullets_render = nullfunc_near;
        break;
    default:
        boss_defeat_update(MAI_SOLO_DEFEAT_BONUS);
        return;
    }
    b4balls_update();
    hud_hp_update_and_render(boss.hp, MAI_SOLO_HP_TOTAL);
}
