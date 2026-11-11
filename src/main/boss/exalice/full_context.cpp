// Actual adjacent33-byte far gate,78-byte phase helper and full update.
// All real bodies are maintained source, with no instruction or layout filler.
#pragma option -zCEXALICE_FULL_TEXT -zPmain_03
#include "src/main/boss/exalice/full_context.hpp"
#include "src/main/boss/exalice/update_phases.hpp"
#include "src/main/boss/exalice/boss_scratch.hpp"
#pragma codeseg EXALICE_FULL_TEXT main_03

int far exalice_hittest_shots(void)
{
    if(bombing) {
        exalice_bomb_invincibility = 39;
    }
    if(exalice_bomb_invincibility == 0) {
        return boss_hittest_shots();
    }
    return 0;
}

void pascal near exalice_phase_next(explosion_type_t type, int next_end_hp)
{
    if(type != ET_NONE) {
        boss_explode_small(type);
        if(!boss_phase_timed_out) {
            bullet_zap_drop_point_items = true;
            bullet_zap.active = true;
            boss_items_drop();
        }
    }
    boss_phase_timed_out = true;
    boss.phase++;
    boss.phase_frame = 0;
    boss.mode = EXALICE_MODE_REPOSITION;
    boss.phase_state.patterns_seen = 0;
    boss.hp = boss.phase_end_hp;
    boss.phase_end_hp = next_end_hp;
}

void pascal far exalice_update(void)
{
    if(exalice_bomb_invincibility != 0) {
        exalice_bomb_invincibility--;
    }
    homing_target = boss.pos.cur;
    bullet_template.origin = boss.pos.cur;
    gather_template.center = boss.pos.cur;
    laser_template.coords.origin = boss.pos.cur;
    cheeto_template.origin = boss.pos.cur;
    boss.phase_frame++;

    switch(boss.phase) {
    case EXALICE_PHASE_SETUP:
        if(boss.phase_frame == 1) {
            boss.hp = EXALICE_HP_INITIAL;
            boss.phase_end_hp = EXALICE_HP_SETUP_END;
            gather_template.radius.v = to_sp(128);
            gather_template.angle_delta = 2;
            gather_template.ring_points = 8;
            boss.sprite = 180;
            boss_sprite_left = 186;
            boss_sprite_right = 184;
            boss_sprite_stay = 180;
            exalice_bomb_invincibility = 0;
            boss_flystep_random_clamp.left.v = to_sp(64);
            boss_flystep_random_clamp.right.v = to_sp(320);
            boss_flystep_random_clamp.top.v = to_sp(48);
            boss_flystep_random_clamp.bottom.v = to_sp(96);
            for(int i = 204; i < 220; i++) {
                super_convert_tiny(i);
            }
        }
        boss_hittest_shots_invincible();
        if(boss.phase_frame >= EXALICE_SETUP_END_FRAME) {
            boss.phase_frame = 0;
            boss.phase++;
            snd_se_play(13);
            Palettes.colors[0].c.r = 0;
            Palettes.colors[0].c.g = 0;
            Palettes.colors[0].c.b = 0;
            palette_changed = true;
            exalice_backdrop_patnum = 196;
            bg_render_bombing_func = exalice_bg_render;
        }
        break;
    case EXALICE_PHASE_READY:
        boss_hittest_shots_invincible();
        if(boss.phase_frame >= EXALICE_READY_END_FRAME) {
            boss.phase++;
            boss.mode = EXALICE_MODE_CHARGE;
            boss.phase_state.patterns_seen = 0;
            boss.phase_frame = 0;
            boss_custombullets_render = exalice_custombullets_render;
            exalice_boss_scratch.initial_fan_substate = 0;
            exalice_pattern = exalice_pattern_random_fan;
            exalice_boss_scratch.wave_index = 0;
        }
        break;
    case EXALICE_PHASE_WAVE1_REGULAR:
regular_attack:
        switch(boss.mode) {
        case EXALICE_MODE_REPOSITION:
            if(boss_flystep_random(boss.phase_frame - EXALICE_RANDOM_FLYSTEP_LEAD_FRAMES)) {
                boss.phase_frame = 0;
                boss.phase_state.patterns_seen++;
                boss.mode++;
                exalice_pattern = exalice_patterns_by_phase[exalice_boss_scratch.wave_index][
                    boss.phase_state.patterns_seen & EXALICE_REGULAR_PATTERN_ALTERNATION_MASK];
                if(boss.phase_state.patterns_seen >= EXALICE_REGULAR_PATTERN_LIMIT) {
                    goto regular_complete;
                }
            }
            break;
        case EXALICE_MODE_CHARGE:
            exalice_charge_update();
            break;
        }
        if(!exalice_hittest_shots()) {
            break;
        }
        boss_score_bonus(20);
regular_complete:
        switch(exalice_boss_scratch.wave_index) {
        case EXALICE_WAVE_1:
            exalice_phase_next(ET_CIRCLE, EXALICE_HP_WAVE1_REGULAR_END);
            exalice_pattern = exalice_pattern_firewave_fans;
            break;
        case EXALICE_WAVE_2:
            exalice_phase_next(ET_NW_SE, EXALICE_HP_WAVE2_REGULAR_END);
            exalice_pattern = exalice_pattern_bouncing_rings;
            break;
        case EXALICE_WAVE_3:
            exalice_phase_next(ET_SW_NE, EXALICE_HP_WAVE3_REGULAR_END);
            exalice_pattern = exalice_pattern_sweeping_lasers;
            break;
        case EXALICE_WAVE_4:
            exalice_phase_next(ET_HORIZONTAL, EXALICE_HP_WAVE4_REGULAR_END);
            exalice_pattern = exalice_pattern_spiral_gather;
            break;
        }
        break;
    case EXALICE_PHASE_WAVE1_APPROACH:
        if(Palettes.colors[0].c.r < 96) {
            Palettes.colors[0].c.r += 2;
            palette_changed = true;
        }
        // The other approach phases share this movement without a red fade.
    case EXALICE_PHASE_WAVE2_APPROACH_SECOND:
    case EXALICE_PHASE_WAVE3_APPROACH_SECOND:
    case EXALICE_PHASE_WAVE4_APPROACH_SECOND:
approach:
        if(boss_flystep_towards(to_sp(192), to_sp(64))) {
            boss.phase_frame = 0;
            boss.phase++;
            boss.mode = EXALICE_MODE_CHARGE;
        }
        exalice_hittest_shots();
        break;
    case EXALICE_PHASE_WAVE1_CHARGE:
        if(Palettes.colors[0].c.r < 96) {
            Palettes.colors[0].c.r += 2;
            palette_changed = true;
        }
    case EXALICE_PHASE_WAVE2_CHARGE:
    case EXALICE_PHASE_WAVE3_CHARGE:
charge_attack:
        exalice_charge_update();
        if(boss.phase_frame > EXALICE_CHARGE_TIMEOUT_FRAME) {
            goto charge_complete;
        }
charge_hittest:
        if(!exalice_hittest_shots()) {
            break;
        }
        boss_score_bonus(20);
charge_complete:
        switch(exalice_boss_scratch.wave_index) {
        case EXALICE_WAVE_1:
            exalice_phase_next(ET_NW_SE, EXALICE_HP_WAVE1_CHARGE_END);
            exalice_pattern = exalice_pattern_gravity_stacks;
            break;
        case EXALICE_WAVE_2:
            exalice_phase_next(ET_SW_NE, EXALICE_HP_WAVE2_CHARGE_END);
            exalice_pattern = exalice_pattern_fixed_laser_fan;
            break;
        case EXALICE_WAVE_3:
            exalice_phase_next(ET_HORIZONTAL, EXALICE_HP_WAVE3_CHARGE_END);
            exalice_pattern = exalice_pattern_cross_cheetos;
            break;
        case EXALICE_WAVE_4:
            exalice_phase_next(ET_VERTICAL, EXALICE_HP_LAST_CHARGE_END);
            break;
        }
        pellet_bottom_col = 9;
        exalice_backdrop_patnum = 200;
        exalice_boss_scratch.wave_index++;
        break;
    case EXALICE_PHASE_WAVE2_APPROACH_FIRST:
    case EXALICE_PHASE_WAVE2_REGULAR:
        if(Palettes.colors[0].c.b < 96) {
            Palettes.colors[0].c.b += 2;
            Palettes.colors[0].c.r -= 2;
            palette_changed = true;
        }
        if(boss.phase == EXALICE_PHASE_WAVE2_APPROACH_FIRST) {
            goto approach;
        }
        goto regular_attack;
    case EXALICE_PHASE_WAVE3_APPROACH_FIRST:
    case EXALICE_PHASE_WAVE3_REGULAR:
        if(Palettes.colors[0].c.r < 48) {
            Palettes.colors[0].c.r++;
            Palettes.colors[0].c.b--;
            palette_changed = true;
        }
        if(boss.phase == EXALICE_PHASE_WAVE3_APPROACH_FIRST) {
            goto approach;
        }
        goto regular_attack;
    case EXALICE_PHASE_WAVE4_APPROACH_FIRST:
    case EXALICE_PHASE_WAVE4_REGULAR:
        if(Palettes.colors[0].c.g < 64) {
            if(Palettes.colors[0].c.r > 0) {
                Palettes.colors[0].c.r--;
            }
            Palettes.colors[0].c.g++;
            if(Palettes.colors[0].c.b > 0) {
                Palettes.colors[0].c.b--;
            }
            palette_changed = true;
        }
        if(boss.phase == EXALICE_PHASE_WAVE4_APPROACH_FIRST) {
            goto approach;
        }
        goto regular_attack;
    case EXALICE_PHASE_WAVE4_CHARGE:
        if(exalice_charge_update()) {
            boss.phase_state.patterns_seen++;
            if(boss.phase_state.patterns_seen > EXALICE_FINAL_CHARGE_PATTERN_LAST) {
                goto charge_complete;
            }
        }
        goto charge_hittest;
    case EXALICE_PHASE_FINAL_FAN:
        if(exalice_boss_scratch.palette_step == EXALICE_PALETTE_DRAIN_GREEN) {
            if(Palettes.colors[0].c.g > 0) {
                Palettes.colors[0].c.g--;
            } else {
                exalice_boss_scratch.palette_step = EXALICE_PALETTE_BRIGHTEN;
            }
        } else if(exalice_boss_scratch.palette_step == EXALICE_PALETTE_BRIGHTEN) {
            Palettes.colors[0].c.r += 2;
            Palettes.colors[0].c.g++;
            Palettes.colors[0].c.b += 2;
            if(Palettes.colors[0].c.r >= 128) {
                exalice_boss_scratch.palette_step = EXALICE_PALETTE_DIM;
            }
        } else {
            Palettes.colors[0].c.r -= 2;
            Palettes.colors[0].c.g--;
            Palettes.colors[0].c.b -= 2;
            if(Palettes.colors[0].c.r == 0) {
                exalice_boss_scratch.palette_step = EXALICE_PALETTE_BRIGHTEN;
            }
        }
        palette_changed = true;
        exalice_pattern_final_fan();
        if(boss.phase_frame <= EXALICE_FINAL_FAN_TIMEOUT_FRAME) {
            if(!exalice_hittest_shots()) {
                break;
            }
            boss.phase_state.defeat_bonus = true;
        }
        boss_explode_small(ET_VERTICAL);
        boss.phase_frame = 0;
        boss.phase = PHASE_BOSS_EXPLODE_SMALL;
        boss_custombullets_render = nullfunc_near;
        bullet_zap_drop_point_items = false;
        break;
    default:
        boss_defeat_update(200);
        break;
    }
    cheetos_update();
    firewaves_update();
    hud_hp_update_and_render(boss.hp, EXALICE_HP_INITIAL);
}
