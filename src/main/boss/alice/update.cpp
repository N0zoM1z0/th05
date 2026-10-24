// Alice's final spread and complete boss state machine.
#pragma option -zCB4_UPDATE_TEXT -zPmain_03
#include "src/main/boss/alice/update.hpp"
// Canonical object layouts are already parsed. Retain the real CODE-table
// alignment using the genuine preceding63-byte spread function.
#pragma option -a2

#include "src/main/boss/alice/final_spread.inl"

void pascal far alice_update(void)
{
    AlicePuppet near *p;

    homing_target.x = boss.pos.cur.x;
    homing_target.y = boss.pos.cur.y;
    boss.phase_frame++;
    bullet_template.spawn_type = BST_NORMAL;
    bullet_template.origin.x = boss.pos.cur.x;
    bullet_template.origin.y.v = boss.pos.cur.y.v + to_sp(-8);
    gather_template.center = bullet_template.origin;

    switch(boss.phase) {
    case 0:
        if(boss.phase_frame == 1) {
            boss.hp = ALICE_HP_TOTAL;
            boss.phase_end_hp = 7400;
            gather_template.radius.v = to_sp(64);
            gather_template.angle_delta = 2;
            gather_template.ring_points = 8;
        }
        boss_hittest_shots_invincible();
        if(boss.phase_frame >= 128) {
            boss.phase++;
            boss.phase_frame = 0;
            snd_se_play(13);
            bg_render_bombing_func = alice_bg_render;
        }
        break;

    case 1:
        boss_hittest_shots_invincible();
        if(boss.phase_frame >= 64) {
            boss.phase++;
            boss.phase_frame = 0;
            boss.mode = 1;
            boss.phase_state.patterns_seen = 0;
            boss_statebyte[10] = 24;
            boss_statebyte[9] = 0;
        }
        break;

    case 2:
        alice_pattern_opening();
        boss_hittest_shots();
        if(boss.phase_frame == 128) {
            p = &alice_puppet0;
            p->flag = 1;
            p->patnum = 190;
            p->radius.radius_motion = to_sp(256);
            p->angle = 0x60;
            p->hp = ALICE_PUPPET_HP;
            p->pos.cur.x.v = to_sp(-999);
            p++;
            p->flag = 1;
            p->patnum = 190;
            p->radius.radius_motion = to_sp(256);
            p->angle = 0x20;
            p->hp = ALICE_PUPPET_HP;
            p->pos.cur.x.v = to_sp(-999);
            alice_puppet_pattern0 = alice_puppet_initial;
            alice_puppet_pattern1 = alice_puppet_initial;
        } else if(boss.phase_frame > 128) {
            alice_puppets_entrance();
            if(alice_puppet0.radius.radius_motion == 0) {
                boss.phase++;
                boss.mode = 0;
                boss.phase_frame = 0;
                boss.phase_state.patterns_seen = 0;
                boss_statebyte[7] = 0;
                alice_beam_burst_window = 160;
            }
        }
        break;

    case 3:
    case 6:
    case 9:
    case 12:
        switch(boss.mode) {
        case 0:
            if(boss_flystep_random(boss.phase_frame - 8)) {
                boss.mode = 1;
                boss.phase_frame = 0;
                boss.phase_state.patterns_seen++;
                if(boss.phase_state.patterns_seen >= 24) {
                    goto phase_complete;
                }
                alice_pattern_current =
                    alice_pattern_table[boss_statebyte[7]][randring2_next16_mod(3)];
            }
            break;
        case 1:
            alice_pattern_current();
            break;
        }
        if(!boss_hittest_shots()) {
            break;
        }
        boss_score_bonus(7);
        boss_items_drop();
phase_complete:
        boss_statebyte[7]++;
        if(bullet_clear_time < 20) {
            bullet_clear_time = 20;
        }
        boss_explode_small(ET_NW_SE);
        boss.phase++;
        boss.phase_frame = 0;
        boss.phase_state.patterns_seen = 0;
        boss.mode = 0;
        boss.hp = boss.phase_end_hp;
        if(boss.phase < 12) {
            boss.phase_end_hp -= 2200;
        } else {
            boss.phase_end_hp = 0;
        }
        alice_beam_frame = 0;
        break;

    case 4:
    case 7:
    case 10:
        alice_puppet0.pos.prev.x.v = to_sp(128);
        alice_puppet0.pos.prev.y.v = to_sp(128);
        alice_puppet1.pos.prev.x.v = to_sp(256);
        alice_puppet1.pos.prev.y.v = to_sp(128);
        alice_puppet0.hp = ALICE_PUPPET_HP;
        alice_puppet1.hp = ALICE_PUPPET_HP;
        alice_puppet_pattern0 = alice_puppet_pattern1 = alice_puppet_hold;
        if(boss_flystep_towards(to_sp(192), to_sp(64))) {
            goto movement_complete;
        }
        goto movement_hittest;

    case 5:
    case 8:
    case 11:
        alice_puppet0.pos.prev.x.v = to_sp(128);
        alice_puppet0.pos.prev.y.v = to_sp(128);
        alice_puppet1.pos.prev.x.v = to_sp(256);
        alice_puppet1.pos.prev.y.v = to_sp(128);
        alice_puppet0.hp = ALICE_PUPPET_HP;
        alice_puppet1.hp = ALICE_PUPPET_HP;
        alice_puppet_pattern0 = alice_puppet_pattern1 = alice_puppet_hold;
        alice_puppet_beam_pattern();
        boss_hittest_shots();
        if(boss.phase_frame < 600) {
            break;
        }
        boss_score_bonus(5);
        boss_explode_small(ET_NW_SE);
        if(bullet_clear_time < 20) {
            bullet_clear_time = 20;
        }
        boss.phase++;
        boss.phase_frame = 0;
        boss_statebyte[9] = 0;
        alice_puppet0.pos.prev.x.v = to_sp(320);
        alice_puppet0.pos.prev.y.v = to_sp(96);
        alice_puppet1.pos.prev.x.v = to_sp(64);
        alice_puppet1.pos.prev.y.v = to_sp(96);
        alice_puppet0.phase_frame = alice_puppet1.phase_frame = 0;
        alice_puppet_pattern0 = alice_puppet_spread;
        alice_puppet_pattern1 = alice_puppet_spread;
        break;

    case 13:
        alice_puppet0.pos.prev.x.v = to_sp(64);
        alice_puppet0.pos.prev.y.v = to_sp(128);
        alice_puppet1.pos.prev.x.v = to_sp(320);
        alice_puppet1.pos.prev.y.v = to_sp(128);
        alice_puppet0.hp = ALICE_PUPPET_HP;
        alice_puppet1.hp = ALICE_PUPPET_HP;
        alice_puppet_pattern0 = alice_puppet_pattern1 = alice_puppet_rings;
        if(!boss_flystep_towards(to_sp(192), to_sp(64))) {
            goto movement_hittest;
        }
movement_complete:
        boss.phase_frame = 0;
        boss.phase++;
movement_hittest:
        boss_hittest_shots();
        break;

    case 14:
        alice_puppet0.pos.prev.x.v = to_sp(64);
        alice_puppet0.pos.prev.y.v = to_sp(128);
        alice_puppet1.pos.prev.x.v = to_sp(320);
        alice_puppet1.pos.prev.y.v = to_sp(128);
        alice_puppet_pattern0 = alice_puppet_pattern1 = alice_puppet_rings;
        alice_pattern_final_spread();
        if(boss.phase_frame < 1000) {
            if(!boss_hittest_shots()) {
                break;
            }
            boss.phase_state.defeat_bonus = true;
        }
        boss.phase_frame = 0;
        boss.phase = ALICE_PHASE_EXPLODE_SMALL;
        alice_puppet0.flag = 2;
        alice_puppet1.flag = 2;
        break;

    default:
        boss_defeat_update(10);
        break;
    }

    hud_hp_update_and_render(boss.hp, ALICE_HP_TOTAL);
    if(boss.phase >= 3 && boss.phase < ALICE_PHASE_EXPLODE_BIG) {
        alice_puppets_update();
    }
}
