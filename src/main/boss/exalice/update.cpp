// Complete EX-Alice boss state machine, including its real compiler tables.
#pragma option -zCEXALICE_UPD_TEXT -zPmain_03
#include "src/main/boss/exalice/update.hpp"

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
    case 0:
        if(boss.phase_frame == 1) {
            boss.hp = 26500;
            boss.phase_end_hp = 23800;
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
        if(boss.phase_frame >= 192) {
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
    case 1:
        boss_hittest_shots_invincible();
        if(boss.phase_frame >= 64) {
            boss.phase++;
            boss.mode = 1;
            boss.phase_state.patterns_seen = 0;
            boss.phase_frame = 0;
            boss_custombullets_render = exalice_custombullets_render;
            boss_statebyte[15] = 0;
            exalice_pattern = exalice_pattern_random_fan;
            boss_statebyte[9] = 0;
        }
        break;
    case 2:
regular_attack:
        switch(boss.mode) {
        case 0:
            if(boss_flystep_random(boss.phase_frame - 32)) {
                boss.phase_frame = 0;
                boss.phase_state.patterns_seen++;
                boss.mode++;
                exalice_pattern = exalice_patterns_by_phase[boss_statebyte[9]][
                    boss.phase_state.patterns_seen & 1];
                if(boss.phase_state.patterns_seen >= 32) {
                    goto regular_complete;
                }
            }
            break;
        case 1:
            exalice_charge_update();
            break;
        }
        if(!exalice_hittest_shots()) {
            break;
        }
        boss_score_bonus(20);
regular_complete:
        switch(boss_statebyte[9]) {
        case 0:
            exalice_phase_next(ET_CIRCLE, 21000);
            exalice_pattern = exalice_pattern_firewave_fans;
            break;
        case 1:
            exalice_phase_next(ET_NW_SE, 15100);
            exalice_pattern = exalice_pattern_bouncing_rings;
            break;
        case 2:
            exalice_phase_next(ET_SW_NE, 9600);
            exalice_pattern = exalice_pattern_sweeping_lasers;
            break;
        case 3:
            exalice_phase_next(ET_HORIZONTAL, 3400);
            exalice_pattern = exalice_pattern_spiral_gather;
            break;
        }
        break;
    case 3:
        if(Palettes.colors[0].c.r < 96) {
            Palettes.colors[0].c.r += 2;
            palette_changed = true;
        }
        // The other approach phases share this movement without a red fade.
    case 7:
    case 11:
    case 15:
approach:
        if(boss_flystep_towards(to_sp(192), to_sp(64))) {
            boss.phase_frame = 0;
            boss.phase++;
            boss.mode = 1;
        }
        exalice_hittest_shots();
        break;
    case 4:
        if(Palettes.colors[0].c.r < 96) {
            Palettes.colors[0].c.r += 2;
            palette_changed = true;
        }
    case 8:
    case 12:
charge_attack:
        exalice_charge_update();
        if(boss.phase_frame > 4000) {
            goto charge_complete;
        }
charge_hittest:
        if(!exalice_hittest_shots()) {
            break;
        }
        boss_score_bonus(20);
charge_complete:
        switch(boss_statebyte[9]) {
        case 0:
            exalice_phase_next(ET_NW_SE, 18100);
            exalice_pattern = exalice_pattern_gravity_stacks;
            break;
        case 1:
            exalice_phase_next(ET_SW_NE, 12600);
            exalice_pattern = exalice_pattern_fixed_laser_fan;
            break;
        case 2:
            exalice_phase_next(ET_HORIZONTAL, 6800);
            exalice_pattern = exalice_pattern_cross_cheetos;
            break;
        case 3:
            exalice_phase_next(ET_VERTICAL, 0);
            break;
        }
        pellet_bottom_col = 9;
        exalice_backdrop_patnum = 200;
        boss_statebyte[9]++;
        break;
    case 5:
    case 6:
        if(Palettes.colors[0].c.b < 96) {
            Palettes.colors[0].c.b += 2;
            Palettes.colors[0].c.r -= 2;
            palette_changed = true;
        }
        if(boss.phase == 5) {
            goto approach;
        }
        goto regular_attack;
    case 9:
    case 10:
        if(Palettes.colors[0].c.r < 48) {
            Palettes.colors[0].c.r++;
            Palettes.colors[0].c.b--;
            palette_changed = true;
        }
        if(boss.phase == 9) {
            goto approach;
        }
        goto regular_attack;
    case 13:
    case 14:
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
        if(boss.phase == 13) {
            goto approach;
        }
        goto regular_attack;
    case 16:
        if(exalice_charge_update()) {
            boss.phase_state.patterns_seen++;
            if(boss.phase_state.patterns_seen > 8) {
                goto charge_complete;
            }
        }
        goto charge_hittest;
    case 17:
        if(boss_statebyte[10] == 0) {
            if(Palettes.colors[0].c.g > 0) {
                Palettes.colors[0].c.g--;
            } else {
                boss_statebyte[10] = 1;
            }
        } else if(boss_statebyte[10] == 1) {
            Palettes.colors[0].c.r += 2;
            Palettes.colors[0].c.g++;
            Palettes.colors[0].c.b += 2;
            if(Palettes.colors[0].c.r >= 128) {
                boss_statebyte[10] = 2;
            }
        } else {
            Palettes.colors[0].c.r -= 2;
            Palettes.colors[0].c.g--;
            Palettes.colors[0].c.b -= 2;
            if(Palettes.colors[0].c.r == 0) {
                boss_statebyte[10] = 1;
            }
        }
        palette_changed = true;
        exalice_pattern_final_fan();
        if(boss.phase_frame <= 5000) {
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
    hud_hp_update_and_render(boss.hp, 26500);
}
