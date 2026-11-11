// Complete shared Mai/Yuki update, original MAIN17FDB..183D5.
#include "src/main/boss/mai_yuki/update.hpp"

// The shared hit selector's return values distinguish which Boss was hit.
// Its nonzero result is stored minus one in boss2.phase_state.patterns_seen
// during the survivor dialogue, so the *stored* loss codes are 0/1.
static const unsigned char MY_HIT_NEITHER = 0;
static const unsigned char MY_HIT_MAI = 1;
static const unsigned char MY_HIT_YUKI = 2;
static const unsigned char MY_DEFEATED_MAI = MY_HIT_MAI - 1;
static const unsigned char MY_DEFEATED_YUKI = MY_HIT_YUKI - 1;

// One shared fight: the entry, each reposition, and the chosen survivor
// observe different clocks. These remain compiler constants, never new state.
static const int MY_SETUP_ENTRY_FRAME = 1;
static const int MY_SETUP_EXIT_FRAME = 128;
static const int MY_READY_EXIT_FRAME = 64;
static const int MY_SHARED_RING_RADIUS_PIXELS = 64;
static const int MY_SETUP_HIT_RADIUS_PIXELS = 24;
static const int MY_SETUP_HIT_EFFECT = 10;
static const int MY_REPOSITION_LASER_LEAD_FRAMES = 64;
static const int MY_REPOSITION_NORMAL_LEAD_FRAMES = 16;
static const int MY_REPOSITION_CLEAR_FRAME = 16;
static const int MY_BULLET_CLEAR_MINIMUM = 20;
static const int MY_PATTERN_VARIANT_MASK = 3;
static const int MY_SMALL_EXPLOSION_FIRST_FRAME = 16;
static const int MY_SMALL_EXPLOSION_BIG_FRAME = 32;
static const int MY_BIG_EXPLOSION_SHAKE_FRAMES = 12;
static const int MY_BIG_EXPLOSION_SPRITE_FRAMES = 8;
static const int MY_BIG_EXPLOSION_EXIT_FRAME = 64;
static const int MY_SURVIVOR_DIALOG_ENTRY_FRAME = 1;
static const int MY_SURVIVOR_DIALOG_PALETTE_TONE = 60;

// All canonical physical interfaces are complete before ordinary word
// alignment of the real six-value/six-destination compiler switch data.
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
    case MY_PHASE_SETUP:
        if(boss.phase_frame == MY_SETUP_ENTRY_FRAME) {
            boss.hp = MY_SHARED_HP;
            boss.phase_end_hp = 0;
            boss2.hp = MY_SHARED_HP;
            boss2.phase_end_hp = 0;
            gather_template.radius.v = to_sp(MY_SHARED_RING_RADIUS_PIXELS);
            gather_template.angle_delta = 2;
            gather_template.ring_points = 8;
            for(i = MY_TINY_FIRST; i < MY_TINY_END; i++) {
                super_convert_tiny(i);
            }
        }
        boss_hittest_shots_invincible();
        yuki_hittest_shots_damage(to_sp(MY_SETUP_HIT_RADIUS_PIXELS), to_sp(MY_SETUP_HIT_RADIUS_PIXELS), MY_SETUP_HIT_EFFECT);
        if(boss.phase_frame >= MY_SETUP_EXIT_FRAME) {
            boss.phase++;
            boss.phase_frame = 0;
            snd_se_play(13);
            bg_render_bombing_func = mai_yuki_bg_render;
        }
        break;

    case MY_PHASE_READY:
        boss_hittest_shots_invincible();
        yuki_hittest_shots_damage(to_sp(MY_SETUP_HIT_RADIUS_PIXELS), to_sp(MY_SETUP_HIT_RADIUS_PIXELS), MY_SETUP_HIT_EFFECT);
        if(boss.phase_frame < MY_READY_EXIT_FRAME) {
            break;
        }
        boss.phase++;
        boss.phase_frame = 0;
        boss.mode = MY_MODE_ATTACK;
        boss.phase_state.patterns_seen = 0;
        mai_pattern_current = mai_pattern_random_crosses;
        yuki_pattern_current = yuki_pattern_random_aimed_fan;
        boss_custombullets_render = cheetos_render;
        break;

    case MY_PHASE_COMBAT:
        switch(boss.mode) {
        case MY_MODE_REPOSITION:
            if((boss.phase_state.patterns_seen == MY_PATTERN_HP_GATE_FIRST) ||
               (boss.phase_state.patterns_seen == MY_PATTERN_HP_GATE_SECOND)) {
                state_result = boss.phase_frame - MY_REPOSITION_LASER_LEAD_FRAMES;
                if(boss.phase_frame == MY_REPOSITION_CLEAR_FRAME) {
                    if(bullet_clear_time < MY_BULLET_CLEAR_MINIMUM) {
                        bullet_clear_time = MY_BULLET_CLEAR_MINIMUM;
                    }
                    snd_se_play(15);
                    boss_explode_small(ET_NW_SE);
                    boss2_explode_small(2);
                }
            } else {
                state_result = boss.phase_frame - MY_REPOSITION_NORMAL_LEAD_FRAMES;
            }
            if(mai_yuki_flystep_random(state_result)) {
                boss.phase_frame = 0;
                boss.mode++;
                boss.phase_state.patterns_seen++;
                if(boss.phase_state.patterns_seen < MY_PATTERN_FIRST_END) {
                    mai_pattern_current = MAI_PATTERNS_FIRST[boss.phase_state.patterns_seen & MY_PATTERN_VARIANT_MASK];
                    yuki_pattern_current = YUKI_PATTERNS_FIRST[boss.phase_state.patterns_seen & MY_PATTERN_VARIANT_MASK];
                } else if(boss.phase_state.patterns_seen < MY_PATTERN_LASER_END) {
                    mai_pattern_current = mai_pattern_tracking_laser;
                    yuki_pattern_current = YUKI_PATTERNS_LASER[boss.phase_state.patterns_seen & MY_PATTERN_VARIANT_MASK];
                } else if(boss.phase_state.patterns_seen < MY_PATTERN_FINAL_END) {
                    mai_pattern_current = MAI_PATTERNS_FINAL[boss.phase_state.patterns_seen & MY_PATTERN_VARIANT_MASK];
                    yuki_pattern_current = YUKI_PATTERNS_FINAL[boss.phase_state.patterns_seen & MY_PATTERN_VARIANT_MASK];
                } else {
                    boss.phase_state.patterns_seen = 0;
                    // Pattern exhaustion selects Mai's defeat (Yuki survives).
                    state_result = MY_HIT_MAI;
                    goto start_small_explosion;
                }
            }
            break;
        case MY_MODE_ATTACK:
            mai_pattern_update();
            yuki_pattern_update();
            break;
        }
        if(((boss.hp + boss2.hp) < MY_HP_GATE_FIRST) && (boss.phase_state.patterns_seen < MY_PATTERN_HP_GATE_FIRST)) {
            boss.mode = MY_MODE_REPOSITION;
            boss.phase_frame = 0;
            boss.phase_state.patterns_seen = MY_PATTERN_HP_GATE_FIRST;
        } else if(((boss.hp + boss2.hp) < MY_HP_GATE_SECOND) &&
                  (boss.phase_state.patterns_seen < MY_PATTERN_HP_GATE_SECOND)) {
            boss.mode = MY_MODE_REPOSITION;
            boss.phase_frame = 0;
            boss.phase_state.patterns_seen = MY_PATTERN_HP_GATE_SECOND;
        }
        state_result = mai_yuki_hittest_shots();
        if(state_result == MY_HIT_NEITHER) {
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
        if(boss.phase_frame == MY_SMALL_EXPLOSION_FIRST_FRAME) {
            if(boss2.phase_state.patterns_seen == MY_DEFEATED_MAI) {
                boss_explode_small(ET_VERTICAL);
            } else {
                boss2_explode_small(4);
            }
            break;
        }
        if(boss.phase_frame == MY_SMALL_EXPLOSION_BIG_FRAME) {
            if(boss2.phase_state.patterns_seen == MY_DEFEATED_MAI) {
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
        if(boss.phase_frame < MY_BIG_EXPLOSION_SHAKE_FRAMES) {
            playfield_shake_x = (stage_frame_mod2 == 0) ? -4 : 4;
            playfield_shake_y = (stage_frame_mod4 <= 1) ? -4 : 4;
        }
        bg_render_bombing_func = tiles_render_all;
        slowdown_factor = 2;
        if((boss.phase_frame % MY_BIG_EXPLOSION_SPRITE_FRAMES) == 0) {
            if(boss2.phase_state.patterns_seen == MY_DEFEATED_MAI) {
                boss.sprite++;
            } else {
                boss2.sprite++;
            }
            if(boss.phase_frame >= MY_BIG_EXPLOSION_EXIT_FRAME) {
                boss.phase++;
                boss.phase_frame = 0;
            }
        }
        break;

    case MY_PHASE_SURVIVOR_DIALOG:
        PaletteTone = MY_SURVIVOR_DIALOG_PALETTE_TONE;
        palette_changed = true;
        if(boss.phase_frame == MY_SURVIVOR_DIALOG_ENTRY_FRAME) {
            if(boss2.phase_state.patterns_seen == MY_DEFEATED_MAI) {
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
