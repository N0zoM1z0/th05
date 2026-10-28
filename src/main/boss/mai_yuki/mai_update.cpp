// Complete Mai solo state machine, including the compiler's switch table.
#pragma option -zCMAI_UPDATE_TEXT -zPmain_03
#include "src/main/boss/mai_yuki/mai_update.hpp"
// Canonical object types are complete before the compiler table alignment.
#pragma codeseg MAI_UPDATE_TEXT main_03
#pragma option -a2

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
    case 0:
        if(boss.phase_frame == 1) {
            boss.hp = 7800;
            boss.phase_end_hp = 5800;
            gather_template.radius.v = to_sp(64);
            gather_template.angle_delta = 2;
            gather_template.ring_points = 8;
            boss.sprite = 180;
            boss_sprite_left = 182;
            boss_sprite_right = 181;
            boss_sprite_stay = 180;
            b4ball_template.patnum_tiny_base = 212;
        }
        boss_hittest_shots_invincible();
        if(boss.phase_frame >= 64) {
            boss.phase++;
            boss.phase_frame = 0;
            snd_se_play(13);
            bg_render_bombing_func = mai_yuki_bg_render;
        }
        break;
    case 1:
        boss_hittest_shots_invincible();
        if(boss.phase_frame >= 64) {
            boss.sprite = 204;
            boss.phase++;
            boss.phase_frame = 0;
            boss_custombullets_render = b4balls_render;
        }
        break;
    case 2:
        boss_hittest_shots_invincible();
        if(boss_flystep_towards(to_sp(192), to_sp(96))) {
            boss.sprite = 188;
            boss.phase++;
            boss.phase_frame = 0;
            boss.mode = 1;
            boss.phase_state.patterns_seen = 0;
            boss_explode_small(ET_VERTICAL);
            circles_add_growing(boss.pos.cur.x, boss.pos.cur.y);
            boss_solo_pattern_current = mai_solo_widening_fans;
            boss_sprite_left = 190;
            boss_sprite_right = 189;
            boss_sprite_stay = 188;
        }
        break;
    case 3:
        switch(boss.mode) {
        case 0:
            if(boss_flystep_random(boss.phase_frame - 32)) {
                boss.phase_frame = 0;
                boss.mode++;
                boss.phase_state.patterns_seen++;
                if(boss.phase_state.patterns_seen >= 36) {
                    goto phase3_complete;
                }
                boss_solo_pattern_current = mai_solo_pattern_pair_first[
                    boss.phase_state.patterns_seen & 1];
            }
            break;
        case 1:
            boss_solo_pattern_current();
            break;
        }
        if(!boss_hittest_shots()) {
            break;
        }
        boss_score_bonus(10);
phase3_complete:
        boss_phase_next(ET_NW_SE, 2800);
        break;
    case 4:
        boss_hittest_shots();
        if(boss_flystep_towards(to_sp(192), to_sp(128))) {
            boss.phase++;
            boss.phase_frame = 0;
        }
        break;
    case 5:
        mai_solo_laser_cycle();
        if(boss.phase_frame < 5000) {
            if(!boss_hittest_shots()) {
                break;
            }
            boss_score_bonus(10);
        }
        for(i = 0; i < 10; i++) {
            laser_stop(i);
        }
        boss_phase_next(ET_HORIZONTAL, 1200);
        break;
    case 6:
        boss_hittest_shots();
        if(boss_flystep_towards(to_sp(192), to_sp(96))) {
            goto movement_complete;
        }
        break;
    case 7:
        switch(boss.mode) {
        case 0:
            if(boss_flystep_random(boss.phase_frame - 32)) {
                boss.phase_frame = 0;
                boss.mode++;
                boss.phase_state.patterns_seen++;
                if(boss.phase_state.patterns_seen >= 36) {
                    goto phase7_complete;
                }
                boss_solo_pattern_current = mai_solo_pattern_pair_middle[
                    boss.phase_state.patterns_seen & 1];
            }
            break;
        case 1:
            boss_solo_pattern_current();
            break;
        }
        if(!boss_hittest_shots()) {
            break;
        }
        boss_score_bonus(10);
phase7_complete:
        boss_phase_next(ET_NW_SE, 0);
        break;
    case 8:
        boss_hittest_shots();
        if(boss_flystep_towards(to_sp(192), to_sp(96))) {
movement_complete:
            boss.phase++;
            boss.phase_frame = 0;
            boss_statebyte[10] = 0x80;
            boss_statebyte[11] = static_cast<unsigned char>(-4);
        }
        break;
    case 9:
        switch(boss.mode) {
        case 0:
            if(boss_flystep_random(boss.phase_frame - 4)) {
                boss.phase_frame = 0;
                boss.mode++;
                boss.phase_state.patterns_seen++;
                if(boss.phase_state.patterns_seen >= 20) {
                    boss.phase_state.defeat_bonus = false;
                    goto defeat;
                }
                boss_solo_pattern_current = mai_solo_pattern_pair_final[
                    boss.phase_state.patterns_seen & 1];
            }
            break;
        case 1:
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
        boss.phase = 253;
        b4balls_reset();
        boss_custombullets_render = nullfunc_near;
        break;
    default:
        boss_defeat_update(70);
        return;
    }
    b4balls_update();
    hud_hp_update_and_render(boss.hp, 7800);
}
