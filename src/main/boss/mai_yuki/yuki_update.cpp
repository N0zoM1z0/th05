// Complete Yuki solo state machine, retaining the full post-return switch table.
#pragma option -zCYUKI_UPDATE_TEXT -zPmain_03
#include "src/main/boss/mai_yuki/yuki_update.hpp"
#include "src/main/boss/mai_yuki/solo_scratch.hpp"
#include "src/main/boss/mai_yuki/yuki_solo_choreography.hpp"
#include "src/main/boss/mai_yuki/solo_wave_common.hpp"

// The native ten-stage solo Boss switch and two alternating attack modes.
static const unsigned char YUKI_SOLO_PHASE_SETUP = 0;
static const unsigned char YUKI_SOLO_PHASE_READY = 1;
static const unsigned char YUKI_SOLO_PHASE_ENTRANCE = 2;
static const unsigned char YUKI_SOLO_PHASE_WAVE_FIRST = 3;
static const unsigned char YUKI_SOLO_PHASE_WAVE_SECOND_APPROACH = 4;
static const unsigned char YUKI_SOLO_PHASE_WAVE_SECOND = 5;
static const unsigned char YUKI_SOLO_PHASE_SPEEDUP_APPROACH = 6;
static const unsigned char YUKI_SOLO_PHASE_SPEEDUP = 7;
static const unsigned char YUKI_SOLO_PHASE_FINAL_APPROACH = 8;
static const unsigned char YUKI_SOLO_PHASE_WAVE_FINAL = 9;
static const unsigned char YUKI_SOLO_MODE_REPOSITION = 0;
static const unsigned char YUKI_SOLO_MODE_ATTACK = 1;
static const unsigned char YUKI_SOLO_PHASE_DEFEAT = 253;
static const unsigned char YUKI_SOLO_WAVE_FIRST_LIMIT = 12;
static const unsigned char YUKI_SOLO_WAVE_SECOND_LIMIT = 24;
static const unsigned char YUKI_SOLO_WAVE_FINAL_LIMIT = 36;

extern "C" void pascal far yuki_update(void)
{
    homing_target = boss.pos.cur;
    bullet_template.origin = boss.pos.cur;
    gather_template.center = boss.pos.cur;
    b4ball_template.origin = boss.pos.cur;
    boss.phase_frame++;

    switch(boss.phase) {
    case YUKI_SOLO_PHASE_SETUP:
        if(boss.phase_frame == YUKI_SOLO_FIRST_FRAME) {
            boss.hp = YUKI_SOLO_HP_TOTAL;
            boss.phase_end_hp = YUKI_SOLO_HP_SETUP_GATE;
            gather_template.radius.v = to_sp(YUKI_SOLO_GATHER_RADIUS_PX);
            gather_template.angle_delta = YUKI_SOLO_GATHER_ANGLE_DELTA;
            gather_template.ring_points = YUKI_SOLO_GATHER_RING_POINTS;
            boss.sprite = YUKI_SOLO_SPRITE_STILL;
            boss_sprite_left = YUKI_SOLO_SPRITE_MOVE_LEFT;
            boss_sprite_right = YUKI_SOLO_SPRITE_MOVE_RIGHT;
            boss_sprite_stay = YUKI_SOLO_SPRITE_STILL;
            b4ball_template.patnum_tiny_base = YUKI_SOLO_BALL_FIRST_SPRITE;
        }
        boss_hittest_shots_invincible();
        if(boss.phase_frame >= YUKI_SOLO_HP_FILL_FRAMES) {
            boss.phase++;
            boss.phase_frame = 0;
            snd_se_play(YUKI_SOLO_ENTRY_SOUND);
            bg_render_bombing_func = mai_yuki_bg_render;
        }
        break;
    case YUKI_SOLO_PHASE_READY:
        boss_hittest_shots_invincible();
        if(boss.phase_frame >= YUKI_SOLO_READY_FRAMES) {
            boss.sprite = YUKI_SOLO_SPRITE_ATTACK_STILL;
            boss.phase++;
            boss.phase_frame = 0;
            boss_custombullets_render = b4balls_render;
        }
        break;
    case YUKI_SOLO_PHASE_ENTRANCE:
        boss_hittest_shots_invincible();
        if(boss_flystep_towards(to_sp(YUKI_SOLO_CENTER_X_PX), to_sp(YUKI_SOLO_CENTER_Y_PX))) {
            boss.sprite = YUKI_SOLO_SPRITE_ATTACK_STILL;
            boss.phase++;
            boss.phase_frame = 0;
            boss.mode = YUKI_SOLO_MODE_ATTACK;
            boss.phase_state.patterns_seen = 0;
            boss2.pos.cur.x = boss.pos.cur.x;
            boss2.pos.cur.y.v = boss.pos.cur.y.v + to_sp(YUKI_SOLO_SHADOW_Y_OFFSET_PX);
            circles_add_growing(boss.pos.cur.x, boss.pos.cur.y);
            boss_explode_small(ET_VERTICAL);
            boss_solo_pattern_current = yuki_solo_ring_sweep;
            boss_sprite_left = YUKI_SOLO_SPRITE_ATTACK_LEFT;
            boss_sprite_right = YUKI_SOLO_SPRITE_ATTACK_RIGHT;
            boss_sprite_stay = YUKI_SOLO_SPRITE_ATTACK_STILL;
        }
        break;
    case YUKI_SOLO_PHASE_WAVE_FIRST:
        switch(boss.mode) {
        case YUKI_SOLO_MODE_REPOSITION:
            if(boss_flystep_towards(boss2.pos.cur.x, boss2.pos.cur.y)) {
                boss2.pos.cur.x = boss.pos.cur.x;
                boss2.pos.cur.y.v = to_sp(YUKI_SOLO_CENTER_Y_PX);
                MY_SOLO_NEXT_PATTERN();
                if(boss.phase_state.patterns_seen >= YUKI_SOLO_WAVE_FIRST_LIMIT) {
                    goto phase3_complete;
                }
                boss_solo_pattern_current = yuki_solo_pattern_pair1[
                    boss.phase_state.patterns_seen & YUKI_SOLO_PATTERN_VARIANT_MASK];
            }
            break;
        case YUKI_SOLO_MODE_ATTACK:
            boss_solo_pattern_current();
            break;
        }
        MY_SOLO_HIT_BONUS_OR_BREAK(YUKI_SOLO_HIT_SCORE_BONUS);
phase3_complete:
        boss_phase_next(ET_NW_SE, YUKI_SOLO_HP_FIRST_WAVE_END);
        break;
    case YUKI_SOLO_PHASE_WAVE_SECOND_APPROACH:
        boss_hittest_shots();
        if(boss_flystep_towards(to_sp(YUKI_SOLO_CENTER_X_PX), to_sp(YUKI_SOLO_CENTER_Y_PX))) {
            boss.phase++;
            boss.phase_frame = 0;
            boss_solo_pattern_current = yuki_solo_random_rings;
            boss.mode = YUKI_SOLO_MODE_ATTACK;
        }
        break;
    case YUKI_SOLO_PHASE_WAVE_SECOND:
        switch(boss.mode) {
        case YUKI_SOLO_MODE_REPOSITION:
            if(boss_flystep_towards(boss.pos.cur.x, to_sp(96))) {
                MY_SOLO_NEXT_PATTERN();
                if(boss.phase_state.patterns_seen >= YUKI_SOLO_WAVE_SECOND_LIMIT) {
                    goto phase5_complete;
                }
                boss_solo_pattern_current = yuki_solo_pattern_pair2[
                    boss.phase_state.patterns_seen & YUKI_SOLO_PATTERN_VARIANT_MASK];
            }
            break;
        case YUKI_SOLO_MODE_ATTACK:
            boss_solo_pattern_current();
            break;
        }
        MY_SOLO_HIT_BONUS_OR_BREAK(YUKI_SOLO_HIT_SCORE_BONUS);
phase5_complete:
        boss_phase_next(ET_SW_NE, YUKI_SOLO_HP_SECOND_WAVE_END);
        break;
    case YUKI_SOLO_PHASE_SPEEDUP_APPROACH:
        boss_hittest_shots();
        if(boss_flystep_towards(to_sp(YUKI_SOLO_CENTER_X_PX), to_sp(YUKI_SOLO_CENTER_Y_PX))) {
            boss.phase++;
            boss.phase_frame = 0;
        }
        break;
    case YUKI_SOLO_PHASE_SPEEDUP:
        yuki_solo_speedup();
        if(boss.phase_frame < YUKI_SOLO_SPEEDUP_TIMEOUT_FRAMES) {
            if(!boss_hittest_shots()) {
                break;
            }
            boss_score_bonus(YUKI_SOLO_HIT_SCORE_BONUS);
        }
        boss_phase_next(ET_HORIZONTAL, YUKI_SOLO_HP_SPEEDUP_END);
        break;
    case YUKI_SOLO_PHASE_FINAL_APPROACH:
        boss_hittest_shots();
        if(boss_flystep_towards(to_sp(YUKI_SOLO_CENTER_X_PX), to_sp(YUKI_SOLO_CENTER_Y_PX))) {
            boss.phase++;
            boss.phase_frame = 0;
            boss_solo_pattern_current = yuki_solo_snow_cross;
            boss.mode = YUKI_SOLO_MODE_ATTACK;
            yuki_solo_scratch.snow_angle_step = YUKI_SOLO_FINAL_SNOW_ANGLE_STEP;
            yuki_solo_scratch.snow_angle = YUKI_SOLO_FINAL_SNOW_INITIAL_ANGLE;
            yuki_solo_scratch.snow_step = static_cast<unsigned char>(YUKI_SOLO_FINAL_SNOW_STEP_SIGNED);
        }
        break;
    case YUKI_SOLO_PHASE_WAVE_FINAL:
        switch(boss.mode) {
        case YUKI_SOLO_MODE_REPOSITION:
            if(boss.phase_frame >= YUKI_SOLO_FINAL_WAVE_DELAY_FRAMES) {
                MY_SOLO_NEXT_PATTERN();
                if(boss.phase_state.patterns_seen >= YUKI_SOLO_WAVE_FINAL_LIMIT) {
                    boss.phase_state.patterns_seen = 0;
                    goto defeat;
                }
                boss_solo_pattern_current = yuki_solo_pattern_final[
                    boss.phase_state.patterns_seen % YUKI_SOLO_FINAL_PATTERN_COUNT];
            }
            break;
        case YUKI_SOLO_MODE_ATTACK:
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
        boss.phase = YUKI_SOLO_PHASE_DEFEAT;
        b4balls_reset();
        boss_custombullets_render = nullfunc_near;
        break;
    default:
        boss_defeat_update(YUKI_SOLO_DEFEAT_BONUS);
        return;
    }
    b4balls_update();
    hud_hp_update_and_render(boss.hp, YUKI_SOLO_HP_TOTAL);
}
