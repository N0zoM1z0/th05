// Complete Yuki solo state machine, retaining the full post-return switch table.
#pragma option -zCYUKI_UPDATE_TEXT -zPmain_03
#include "src/main/boss/mai_yuki/yuki_update.hpp"
#include "src/main/boss/mai_yuki/solo_scratch.hpp"

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
        if(boss.phase_frame == 1) {
            boss.hp = 7900;
            boss.phase_end_hp = 4600;
            gather_template.radius.v = to_sp(64);
            gather_template.angle_delta = 2;
            gather_template.ring_points = 8;
            boss.sprite = 196;
            boss_sprite_left = 198;
            boss_sprite_right = 197;
            boss_sprite_stay = 196;
            b4ball_template.patnum_tiny_base = 216;
        }
        boss_hittest_shots_invincible();
        if(boss.phase_frame >= 64) {
            boss.phase++;
            boss.phase_frame = 0;
            snd_se_play(13);
            bg_render_bombing_func = mai_yuki_bg_render;
        }
        break;
    case YUKI_SOLO_PHASE_READY:
        boss_hittest_shots_invincible();
        if(boss.phase_frame >= 64) {
            boss.sprite = 204;
            boss.phase++;
            boss.phase_frame = 0;
            boss_custombullets_render = b4balls_render;
        }
        break;
    case YUKI_SOLO_PHASE_ENTRANCE:
        boss_hittest_shots_invincible();
        if(boss_flystep_towards(to_sp(192), to_sp(96))) {
            boss.sprite = 204;
            boss.phase++;
            boss.phase_frame = 0;
            boss.mode = YUKI_SOLO_MODE_ATTACK;
            boss.phase_state.patterns_seen = 0;
            boss2.pos.cur.x = boss.pos.cur.x;
            boss2.pos.cur.y.v = boss.pos.cur.y.v + to_sp(16);
            circles_add_growing(boss.pos.cur.x, boss.pos.cur.y);
            boss_explode_small(ET_VERTICAL);
            boss_solo_pattern_current = yuki_solo_ring_sweep;
            boss_sprite_left = 206;
            boss_sprite_right = 205;
            boss_sprite_stay = 204;
        }
        break;
    case YUKI_SOLO_PHASE_WAVE_FIRST:
        switch(boss.mode) {
        case YUKI_SOLO_MODE_REPOSITION:
            if(boss_flystep_towards(boss2.pos.cur.x, boss2.pos.cur.y)) {
                boss2.pos.cur.x = boss.pos.cur.x;
                boss2.pos.cur.y.v = to_sp(96);
                boss.phase_frame = 0;
                boss.mode++;
                boss.phase_state.patterns_seen++;
                if(boss.phase_state.patterns_seen >= YUKI_SOLO_WAVE_FIRST_LIMIT) {
                    goto phase3_complete;
                }
                boss_solo_pattern_current = yuki_solo_pattern_pair1[
                    boss.phase_state.patterns_seen & 1];
            }
            break;
        case YUKI_SOLO_MODE_ATTACK:
            boss_solo_pattern_current();
            break;
        }
        if(!boss_hittest_shots()) {
            break;
        }
        boss_score_bonus(10);
phase3_complete:
        boss_phase_next(ET_NW_SE, 3200);
        break;
    case YUKI_SOLO_PHASE_WAVE_SECOND_APPROACH:
        boss_hittest_shots();
        if(boss_flystep_towards(to_sp(192), to_sp(96))) {
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
                boss.phase_frame = 0;
                boss.mode++;
                boss.phase_state.patterns_seen++;
                if(boss.phase_state.patterns_seen >= YUKI_SOLO_WAVE_SECOND_LIMIT) {
                    goto phase5_complete;
                }
                boss_solo_pattern_current = yuki_solo_pattern_pair2[
                    boss.phase_state.patterns_seen & 1];
            }
            break;
        case YUKI_SOLO_MODE_ATTACK:
            boss_solo_pattern_current();
            break;
        }
        if(!boss_hittest_shots()) {
            break;
        }
        boss_score_bonus(10);
phase5_complete:
        boss_phase_next(ET_SW_NE, 1200);
        break;
    case YUKI_SOLO_PHASE_SPEEDUP_APPROACH:
        boss_hittest_shots();
        if(boss_flystep_towards(to_sp(192), to_sp(96))) {
            boss.phase++;
            boss.phase_frame = 0;
        }
        break;
    case YUKI_SOLO_PHASE_SPEEDUP:
        yuki_solo_speedup();
        if(boss.phase_frame < 2000) {
            if(!boss_hittest_shots()) {
                break;
            }
            boss_score_bonus(10);
        }
        boss_phase_next(ET_HORIZONTAL, 0);
        break;
    case YUKI_SOLO_PHASE_FINAL_APPROACH:
        boss_hittest_shots();
        if(boss_flystep_towards(to_sp(192), to_sp(96))) {
            boss.phase++;
            boss.phase_frame = 0;
            boss_solo_pattern_current = yuki_solo_snow_cross;
            boss.mode = YUKI_SOLO_MODE_ATTACK;
            yuki_solo_scratch.snow_angle_step = 8;
            yuki_solo_scratch.snow_angle = 0x10;
            yuki_solo_scratch.snow_step = static_cast<unsigned char>(-8);
        }
        break;
    case YUKI_SOLO_PHASE_WAVE_FINAL:
        switch(boss.mode) {
        case YUKI_SOLO_MODE_REPOSITION:
            if(boss.phase_frame >= 8) {
                boss.phase_frame = 0;
                boss.mode++;
                boss.phase_state.patterns_seen++;
                if(boss.phase_state.patterns_seen >= YUKI_SOLO_WAVE_FINAL_LIMIT) {
                    boss.phase_state.patterns_seen = 0;
                    goto defeat;
                }
                boss_solo_pattern_current = yuki_solo_pattern_final[
                    boss.phase_state.patterns_seen % 5];
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
        boss_defeat_update(50);
        return;
    }
    b4balls_update();
    hud_hp_update_and_render(boss.hp, 7900);
}
