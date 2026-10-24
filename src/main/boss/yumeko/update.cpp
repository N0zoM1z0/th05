// Natural final pattern and full Yumeko state machine from original TH05
// behavior. ReC98 b6ba5b0a disassembly is evidence, not an instruction template.
#pragma option -zCB5_UPDATE_TEXT -zPmain_03
#include "src/main/boss/yumeko/update.hpp"
#pragma codeseg B5_UPDATE_TEXT main_03
// Applied after canonical record declarations. The original semantic switch
// table has a genuine word boundary relative to this odd-address contribution.
#pragma option -a2

#define yumeko_final_angle boss_statebyte[14]
#define yumeko_final_rings boss_statebyte[15]
static const int YUMEKO_HP_TOTAL = 8300;

void near yumeko_pattern_final_ring(void)
{
    if(boss.phase_frame < 32) {
        gather_add_only_3stack(boss.phase_frame - 16, 7, 6);
        if(boss.phase_frame == 16) {
            boss.sprite = YUMEKO_SPRITE_CHARGE;
            bullet_template.spawn_type = YUMEKO_NO_DECELERATE;
            bullet_template.patnum = 116; // Blue directional vector bullet.
            bullet_template.group = BG_RING;
            bullet_template.spread = 18;
            bullet_template.special_motion = BSM_DECELERATE_THEN_TURN;
            bullet_template.speed.v = 2 * 16 + 6;
            bullet_template_tune();
            snd_se_play(8);
            yumeko_final_rings = 0;
            bullet_special.turns_max = 2;
            yumeko_final_angle = 0;
        }
        return;
    }
    if((boss.phase_frame % 16) == 0) {
        bullet_template.angle = yumeko_final_angle;
        if((yumeko_final_rings & 1) != 0) {
            bullet_template_special_angle.turn_by = 0x40;
            bullet_template.angle = 0x80 - bullet_template.angle;
        } else {
            bullet_template_special_angle.turn_by = -0x40;
        }
        bullets_add_special_fixedspeed();
        yumeko_final_angle++;
        yumeko_final_rings++;
        snd_se_play(3);
    }
}

void pascal far yumeko_update(void)
{
    int patnum;
    homing_target = boss.pos.cur;
    bullet_template.origin = boss.pos.cur;
    gather_template.center = boss.pos.cur;
    sword_template.origin = boss.pos.cur;
    boss.phase_frame++;

    switch(boss.phase) {
    case 0:
        if(boss.phase_frame == 1) {
            boss.hp = YUMEKO_HP_TOTAL;
            boss.phase_end_hp = 7500;
            gather_template.radius.v = to_sp(64);
            gather_template.angle_delta = 2;
            gather_template.ring_points = 8;
            boss.sprite = YUMEKO_SPRITE_STILL;
            boss.pos.velocity.x.v = to_sp(4);
            for(patnum = 193; patnum < 229; patnum++) {
                super_convert_tiny(patnum);
            }
            boss_sprite_left = 180;
            boss_sprite_right = 180;
            boss_sprite_stay = 180;
        }
        if(boss2.pos.cur.y.v >= -to_sp(32)) {
            boss2.pos.cur.y.v -= to_sp(1);
            shot_hitbox_radius.x.v = to_sp(24);
            shot_hitbox_radius.y.v = to_sp(24);
            shot_hitbox_center = boss2.pos.cur;
            if(shots_hittest()) {
                snd_se_play(10);
            }
        }
        if(boss.phase_frame < 64) {
            boss_hittest_shots_invincible();
            break;
        }
        boss.sprite = YUMEKO_SPRITE_MOVE;
        boss.pos.cur.x.v += to_sp(2);
        if(boss.pos.cur.x.v >= to_sp(192)) {
            boss.sprite = YUMEKO_SPRITE_STILL;
            boss.phase++;
            boss.phase_frame = 0;
            snd_se_play(13);
            bg_render_bombing_func = yumeko_bg_render;
        }
        break;

    case 1:
        boss_hittest_shots_invincible();
        if(boss.phase_frame >= 64) {
            boss.phase++;
            boss.phase_frame = 0;
            boss.mode = 1;
            boss.phase_state.patterns_seen = 0;
            yumeko_pattern = yumeko_pattern_sword_fan;
            boss_custombullets_render = swords_render;
        }
        break;

    case 2:
    case 5:
        switch(boss.mode) {
        case 0:
            if(yumeko_flystep_bounce(to_sp(2), 64)) {
                boss.phase_frame = 0;
                boss.mode++;
                boss.phase_state.patterns_seen++;
                if(boss.phase_state.patterns_seen >= 20) {
                    goto moving_phase_end;
                }
                if(boss.phase == 2) {
                    yumeko_pattern = yumeko_patterns_phase2[boss.phase_state.patterns_seen & 1];
                } else {
                    yumeko_pattern = yumeko_patterns_phase5[boss.phase_state.patterns_seen & 1];
                }
            }
            break;
        case 1:
            yumeko_pattern();
            break;
        }
        if(boss.mode == 0) {
            break;
        }
        if(!boss_hittest_shots()) {
            break;
        }
        boss_score_bonus(10);
    moving_phase_end:
        if(boss.phase == 2) {
            boss_phase_next(ET_CIRCLE, 5700);
        } else {
            boss_phase_next(ET_HORIZONTAL, 2700);
        }
        break;

    case 3:
    case 6:
        boss_hittest_shots();
        if(boss_flystep_towards(to_sp(192), to_sp(64))) {
            boss.phase++;
            boss.phase_frame = 0;
            if(boss.phase == 4) {
                yumeko_pattern = yumeko_pattern_aimed_swords;
            } else {
                yumeko_pattern = yumeko_pattern_laser_swords;
            }
        }
        break;

    case 4:
    case 7:
        yumeko_pattern();
        if(boss.phase_frame < 2000) {
            if(!boss_hittest_shots()) {
                break;
            }
            boss_score_bonus(10);
        }
        if(boss.phase == 4) {
            boss_phase_next(ET_NW_SE, 4500);
            yumeko_pattern = yumeko_pattern_counterrotating_spreads;
        } else {
            boss_phase_next(ET_NW_SE, 1200);
        }
        boss.mode = 1;
        break;

    case 8:
        yumeko_pattern_sword_sweep();
        if(boss.phase_frame < 2000) {
            if(!boss_hittest_shots()) {
                break;
            }
            boss_score_bonus(10);
        }
        boss_phase_next(ET_NW_SE, 0);
        break;

    case 9:
        boss_hittest_shots();
        if(boss_flystep_towards(to_sp(192), to_sp(96))) {
            boss.phase++;
            boss.phase_frame = 0;
            boss.phase_state.patterns_seen = 0;
        }
        break;

    case 10:
        yumeko_pattern_final_ring();
        if(boss.phase_frame < 1200) {
            if(!boss_hittest_shots()) {
                break;
            }
            boss.phase_state.defeat_bonus = true;
        }
        boss_explode_small(ET_VERTICAL);
        boss.phase_frame = 0;
        boss.phase = PHASE_BOSS_EXPLODE_SMALL;
        boss_custombullets_render = nullfunc_near;
        break;

    default:
        boss_defeat_update(65);
        return;
    }
    swords_update();
    hud_hp_update_and_render(boss.hp, YUMEKO_HP_TOTAL);
}
