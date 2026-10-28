// Genuine adjacent final Mai/Yuki patterns and complete shared Boss updater.
// Only the updater is a new accepted scope; the ten patterns already have credit.
#pragma option -zCMAIN_035_TEXT -zPmain_03
#include "src/main/boss/mai_yuki/update.hpp"
#pragma codeseg MAIN_035_TEXT main_03
#include "src/main/boss/mai_yuki/remaining_patterns.inl"

// All canonical object types precede ordinary compiler-table word alignment.
#pragma option -a2

void pascal far mai_yuki_update(void)
{
    int i;
    int state_result;

    if(boss.pos.cur.y.v > boss2.pos.cur.y.v) {
        homing_target = boss.pos.cur;
    } else {
        homing_target = boss2.pos.cur;
    }
    boss.phase_frame++;

    switch(boss.phase) {
    case 0:
        if(boss.phase_frame == 1) {
            boss.hp = MY_SHARED_HP;
            boss.phase_end_hp = 0;
            boss2.hp = MY_SHARED_HP;
            boss2.phase_end_hp = 0;
            gather_template.radius.v = to_sp(64);
            gather_template.angle_delta = 2;
            gather_template.ring_points = 8;
            for(i = MY_TINY_FIRST; i < MY_TINY_END; i++) {
                super_convert_tiny(i);
            }
        }
        boss_hittest_shots_invincible();
        yuki_hittest_shots_damage(to_sp(24), to_sp(24), 10);
        if(boss.phase_frame >= 128) {
            boss.phase++;
            boss.phase_frame = 0;
            snd_se_play(13);
            bg_render_bombing_func = mai_yuki_bg_render;
        }
        break;

    case 1:
        boss_hittest_shots_invincible();
        yuki_hittest_shots_damage(to_sp(24), to_sp(24), 10);
        if(boss.phase_frame < 64) {
            break;
        }
        boss.phase++;
        boss.phase_frame = 0;
        boss.mode = 1;
        boss.phase_state.patterns_seen = 0;
        mai_pattern_current = mai_pattern_random_crosses;
        yuki_pattern_current = yuki_pattern_random_aimed_fan;
        boss_custombullets_render = cheetos_render;
        break;

    case 2:
        switch(boss.mode) {
        case 0:
            if((boss.phase_state.patterns_seen == 9) ||
               (boss.phase_state.patterns_seen == 14)) {
                state_result = boss.phase_frame - 64;
                if(boss.phase_frame == 16) {
                    if(bullet_clear_time < 20) {
                        bullet_clear_time = 20;
                    }
                    snd_se_play(15);
                    boss_explode_small(ET_NW_SE);
                    boss2_explode_small(2);
                }
            } else {
                state_result = boss.phase_frame - 16;
            }
            if(mai_yuki_flystep_random(state_result)) {
                boss.phase_frame = 0;
                boss.mode++;
                boss.phase_state.patterns_seen++;
                if(boss.phase_state.patterns_seen < 10) {
                    mai_pattern_current = MAI_PATTERNS_FIRST[boss.phase_state.patterns_seen & 3];
                    yuki_pattern_current = YUKI_PATTERNS_FIRST[boss.phase_state.patterns_seen & 3];
                } else if(boss.phase_state.patterns_seen < 15) {
                    mai_pattern_current = mai_pattern_tracking_laser;
                    yuki_pattern_current = YUKI_PATTERNS_LASER[boss.phase_state.patterns_seen & 3];
                } else if(boss.phase_state.patterns_seen < 36) {
                    mai_pattern_current = MAI_PATTERNS_FINAL[boss.phase_state.patterns_seen & 3];
                    yuki_pattern_current = YUKI_PATTERNS_FINAL[boss.phase_state.patterns_seen & 3];
                } else {
                    boss.phase_state.patterns_seen = 0;
                    state_result = 1;
                    goto start_small_explosion;
                }
            }
            break;
        case 1:
            mai_pattern_update();
            yuki_pattern_update();
            break;
        }
        if(((boss.hp + boss2.hp) < 5500) && (boss.phase_state.patterns_seen < 9)) {
            boss.mode = 0;
            boss.phase_frame = 0;
            boss.phase_state.patterns_seen = 9;
        } else if(((boss.hp + boss2.hp) < 2250) &&
                  (boss.phase_state.patterns_seen < 14)) {
            boss.mode = 0;
            boss.phase_frame = 0;
            boss.phase_state.patterns_seen = 14;
        }
        state_result = mai_yuki_hittest_shots();
        if(state_result == 0) {
            break;
        }
        boss.phase_state.defeat_bonus = true;
    start_small_explosion:
        boss2.phase_state.patterns_seen = state_result - 1;
        boss.phase = MY_PHASE_EXPLODE_SMALL;
        boss.phase_frame = 0;
        if(lasers[0].flag != LF_FREE) {
            laser_stop(0);
        }
        break;

    case MY_PHASE_EXPLODE_SMALL:
        if(boss.phase_frame == 16) {
            if(boss2.phase_state.patterns_seen == 0) {
                boss_explode_small(ET_VERTICAL);
            } else {
                boss2_explode_small(4);
            }
            break;
        }
        if(boss.phase_frame == 32) {
            if(boss2.phase_state.patterns_seen == 0) {
                boss_explode_big_circle();
                boss.sprite = 4;
                boss2.sprite = PAT_B4_STILL;
            } else {
                boss2_explode_big_circle();
                boss2.sprite = 4;
                boss.sprite = PAT_B4_STILL;
            }
            boss.phase++;
            bullet_zap.active = boss.phase_state.defeat_bonus;
            boss.phase_frame = 0;
            snd_se_play(12);
            player_invincibility_time = 255;
        }
        break;

    case MY_PHASE_EXPLODE_BIG:
        if(boss.phase_frame < 12) {
            playfield_shake_x = (stage_frame_mod2 == 0) ? -4 : 4;
            playfield_shake_y = (stage_frame_mod4 <= 1) ? -4 : 4;
        }
        bg_render_bombing_func = tiles_render_all;
        slowdown_factor = 2;
        if((boss.phase_frame % 8) == 0) {
            if(boss2.phase_state.patterns_seen == 0) {
                boss.sprite++;
            } else {
                boss2.sprite++;
            }
            if(boss.phase_frame >= 64) {
                boss.phase++;
                boss.phase_frame = 0;
            }
        }
        break;

    case MY_PHASE_SURVIVOR_DIALOG:
        PaletteTone = 60;
        palette_changed = true;
        if(boss.phase_frame == 1) {
            if(boss2.phase_state.patterns_seen == 0) {
                dialog_load(MY_DIALOG_YUKI);
                boss_bgm_title = MY_BGM_TITLE_YUKI;
                boss.pos.cur = boss2.pos.cur;
                boss_update = yuki_update;
            } else {
                dialog_load(MY_DIALOG_MAI);
                boss_bgm_title = MY_BGM_TITLE_MAI;
                boss_update = mai_update;
            }
            dialog_animate();
            overlay1 = overlay_boss_bgm_update_and_render;
            boss.phase = 0;
            boss.phase_frame = 0;
            boss_fg_render = mai_yuki_survivor_render;
            boss.hp = MY_SURVIVOR_HP;
        }
        break;
    }
    cheetos_update();
    hud_hp_update_and_render(boss.hp + boss2.hp, MY_BOTH_HP_TOTAL);
}
