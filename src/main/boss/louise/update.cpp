// Complete natural Louise state machine, original MAIN1527:8AD0.
#include "src/main/boss/louise/update.hpp"

// The original full callback ends with its real eight-word compiler switch
// table at an even boundary. Apply ordinary word alignment only after every
// canonical ABI declaration above is complete.
#pragma option -a2

void pascal far louise_update(void)
{
    homing_target.x = boss.pos.cur.x;
    homing_target.y = boss.pos.cur.y;
    boss.phase_frame++;
    bullet_template.spawn_type = BST_NORMAL;
    bullet_template.origin = boss.pos.cur;
    gather_template.center = boss.pos.cur;

    switch(boss.phase) {
    case 0:
        if(boss.phase_frame == 1) {
            boss.hp = LOUISE_HP_TOTAL;
            boss.phase_end_hp = 3000;
            gather_template.radius.v = to_sp(64);
            gather_template.angle_delta = 2;
            gather_template.ring_points = 8;
        }
        boss_hittest_shots_invincible();
        if(boss.phase_frame >= 128) {
            boss.phase++;
            boss.phase_frame = 0;
            snd_se_play(13);
            bg_render_bombing_func = louise_bg_render;
        }
        break;

    case 1:
        boss_hittest_shots_invincible();
        if(boss.phase_frame >= 64) {
            boss.phase++;
            boss.phase_frame = 0;
            boss.mode = 1;
            boss.phase_state.patterns_seen = 0;
            boss_statebyte[10] = 0x18;
            boss_statebyte[15] = 0;
        }
        break;

    case 2:
        switch(boss.mode) {
        case 0:
            if(louise_flystep(to_sp(1.0f), 96)) {
                boss.phase_frame = 0;
                boss.phase_state.patterns_seen++;
                boss.mode = (boss.phase_state.patterns_seen & 1) + 1;
                if(boss.phase_state.patterns_seen >= 20) {
                    goto first_phase_done;
                }
            }
            break;
        case 1:
            louise_pattern_blue_spreads();
            break;
        case 2:
            louise_pattern_red_stacks();
            break;
        }
        if(!boss_hittest_shots()) {
            break;
        }
        boss_score_bonus(10);
    first_phase_done:
        boss_phase_next(ET_NW_SE, 1900);
        break;

    case 3:
        boss_hittest_shots();
        if(boss.phase_frame >= 64) {
            boss.phase_frame = 0;
            boss.phase++;
            boss.sprite = LOUISE_SPRITE_FIRE;
        }
        break;

    case 4:
        louise_pattern_mirrored_fans();
        if(louise_flystep(to_sp(0.875f), 128)) {
            boss.phase_frame = 0;
            boss.phase_state.patterns_seen++;
            if(boss.phase_state.patterns_seen >= 20) {
                goto fan_phase_done;
            }
        }
        if(!boss_hittest_shots()) {
            break;
        }
        boss_score_bonus(10);
    fan_phase_done:
        boss_phase_next(ET_SW_NE, 500);
        boss_statebyte[14] = 0;
        boss_statebyte[10] = 0x14;
        break;

    case 5:
        switch(boss.mode) {
        case 0:
            if(louise_flystep(to_sp(3.0f), 48)) {
                boss.mode = boss_statebyte[14] + 1;
                boss_statebyte[14] = 1 - boss_statebyte[14];
                boss.phase_frame = 0;
                boss.phase_state.patterns_seen++;
                if(boss.phase_state.patterns_seen >= 20) {
                    goto second_phase_done;
                }
            }
            break;
        case 1:
            louise_pattern_sweeping_lasers();
            break;
        case 2:
            louise_pattern_turning_rings();
            break;
        }
        if(!boss_hittest_shots()) {
            break;
        }
        boss_score_bonus(10);
    second_phase_done:
        boss_phase_next(ET_NW_SE, 0);
        break;

    case 6:
        boss_hittest_shots();
        if(boss.phase_frame >= 64) {
            boss.phase_frame = 0;
            boss.phase++;
            boss.sprite = LOUISE_SPRITE_FIRE;
        }
        break;

    case 7:
        louise_pattern_aimed_pellets();
        if(louise_flystep(to_sp(0.5f), 128)) {
            boss.phase_frame = 0;
            boss.phase_state.patterns_seen++;
            if(boss.phase_state.patterns_seen >= 10) {
                boss.phase_state.defeat_bonus = false;
                goto explode_small;
            }
        }
        if(!boss_hittest_shots()) {
            break;
        }
        boss.phase_state.defeat_bonus = true;
    explode_small:
        boss.phase_frame = 0;
        boss.phase = PHASE_BOSS_EXPLODE_SMALL;
        break;

    default:
        boss_defeat_update(10);
    }
    hud_hp_update_and_render(boss.hp, LOUISE_HP_TOTAL);
}
