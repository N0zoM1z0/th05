// Alice's final spread and complete boss state machine.
#pragma option -zCB4_UPDATE_TEXT -zPmain_03
#include "src/main/boss/alice/update.hpp"
#include "src/main/boss/alice/beam_phase.hpp"
#include "src/main/boss/alice/scratch.hpp"
// Canonical object layouts are already parsed. Keep ordinary word alignment
// and the genuine preceding spread; the whole-owner table gap remains open.
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
    case ALICE_PHASE_SETUP:
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

    case ALICE_PHASE_READY:
        boss_hittest_shots_invincible();
        if(boss.phase_frame >= 64) {
            boss.phase++;
            boss.phase_frame = 0;
            boss.mode = ALICE_MODE_ATTACK;
            boss.phase_state.patterns_seen = 0;
            alice_scratch.ready_seed = 24;
            alice_scratch.beam_phase = ALICE_BEAM_INACTIVE;
        }
        break;

    case ALICE_PHASE_PUPPET_ENTRANCE:
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
                boss.mode = ALICE_MODE_REPOSITION;
                boss.phase_frame = 0;
                boss.phase_state.patterns_seen = 0;
                alice_scratch.attack_wave = 0;
                alice_beam_burst_window = 160;
            }
        }
        break;

    case ALICE_PHASE_PATTERN_WAVE_1:
    case ALICE_PHASE_PATTERN_WAVE_2:
    case ALICE_PHASE_PATTERN_WAVE_3:
    case ALICE_PHASE_PATTERN_WAVE_4:
        switch(boss.mode) {
        case ALICE_MODE_REPOSITION:
            if(boss_flystep_random(boss.phase_frame - 8)) {
                boss.mode = ALICE_MODE_ATTACK;
                boss.phase_frame = 0;
                boss.phase_state.patterns_seen++;
                if(boss.phase_state.patterns_seen >= 24) {
                    goto phase_complete;
                }
                alice_pattern_current =
                    alice_pattern_table[alice_scratch.attack_wave][randring2_next16_mod(3)];
            }
            break;
        case ALICE_MODE_ATTACK:
            alice_pattern_current();
            break;
        }
        if(!boss_hittest_shots()) {
            break;
        }
        boss_score_bonus(7);
        boss_items_drop();
phase_complete:
        alice_scratch.attack_wave++;
        if(bullet_clear_time < 20) {
            bullet_clear_time = 20;
        }
        boss_explode_small(ET_NW_SE);
        boss.phase++;
        boss.phase_frame = 0;
        boss.phase_state.patterns_seen = 0;
        boss.mode = ALICE_MODE_REPOSITION;
        boss.hp = boss.phase_end_hp;
        if(boss.phase < ALICE_PHASE_PATTERN_WAVE_4) {
            boss.phase_end_hp -= 2200;
        } else {
            boss.phase_end_hp = 0;
        }
        alice_beam_frame = 0;
        break;

    case ALICE_PHASE_BEAM_APPROACH_1:
    case ALICE_PHASE_BEAM_APPROACH_2:
    case ALICE_PHASE_BEAM_APPROACH_3:
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

    case ALICE_PHASE_BEAM_ATTACK_1:
    case ALICE_PHASE_BEAM_ATTACK_2:
    case ALICE_PHASE_BEAM_ATTACK_3:
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
        alice_scratch.beam_phase = ALICE_BEAM_INACTIVE;
        alice_puppet0.pos.prev.x.v = to_sp(320);
        alice_puppet0.pos.prev.y.v = to_sp(96);
        alice_puppet1.pos.prev.x.v = to_sp(64);
        alice_puppet1.pos.prev.y.v = to_sp(96);
        alice_puppet0.phase_frame = alice_puppet1.phase_frame = 0;
        alice_puppet_pattern0 = alice_puppet_spread;
        alice_puppet_pattern1 = alice_puppet_spread;
        break;

    case ALICE_PHASE_RING_APPROACH:
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

    case ALICE_PHASE_FINAL_SPREAD:
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
    if(boss.phase >= ALICE_PHASE_PATTERN_WAVE_1 && boss.phase < ALICE_PHASE_EXPLODE_BIG) {
        alice_puppets_update();
    }
}
