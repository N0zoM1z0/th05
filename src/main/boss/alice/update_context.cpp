// Genuine adjacent Alice charge patterns, final spread and complete updater.
// Only the final callback is proposed for new authored credit.
#pragma option -zCB4_UPDATE_TEXT -zPmain_03
#include "src/main/boss/alice/update.hpp"
#include "src/main/boss/alice/puppet_choreography.hpp"
#include "src/main/boss/alice/beam_phase.hpp"
#include "src/main/boss/alice/beam_weapon_rules.hpp"
#include "src/main/boss/alice/scratch.hpp"
#include "src/main/boss/alice/charged_attack_rules.hpp"
#include "src/main/boss/alice/charge_patterns.hpp"

// The four normal waves share one countdown but the *current* HP is set
// from the previous threshold before the next threshold is installed.
// The four real regular-wave HP gates are 7400 -> 5200 -> 3000 -> 800,
// and the final transition installs zero for the following attack.
static const int ALICE_WAVE_ONE_END_HP = 7400;
static const int ALICE_WAVE_HP_DECREMENT = 2200;
static const int ALICE_REGULAR_WAVE_PATTERN_LIMIT = 24;
static const int ALICE_REGULAR_WAVE_VARIANTS = 3;
static const int ALICE_RANDOM_FLYSTEP_LEAD_FRAMES = 8;
static const int ALICE_SETUP_ENTRY_FRAME = 1;
static const int ALICE_SETUP_EXIT_FRAME = 128;
static const int ALICE_READY_EXIT_FRAME = 64;
static const int ALICE_PUPPET_APPEAR_FRAME = 128;
static const int ALICE_FINAL_SPREAD_TIMEOUT = 1000;
static const int ALICE_BULLET_CLEAR_MIN_FRAMES = 20;
static const int ALICE_REGULAR_WAVE_BONUS = 7;
#pragma codeseg B4_UPDATE_TEXT main_03

#include "src/main/boss/alice/charge_patterns_body.inl"


#pragma option -a2
#include "src/main/boss/alice/final_spread.inl"

// Both beam approach and beam attack hold the paired puppets at the same
// prev-position anchors with full HP and the held-pattern callbacks.
#define ALICE_BEAM_PUPPETS_HOLD() \
    alice_puppet0.pos.prev.x.v = to_sp(ALICE_PUPPET_BEAM_LEFT_X_PX); \
    alice_puppet0.pos.prev.y.v = to_sp(ALICE_PUPPET_BEAM_Y_PX); \
    alice_puppet1.pos.prev.x.v = to_sp(ALICE_PUPPET_BEAM_RIGHT_X_PX); \
    alice_puppet1.pos.prev.y.v = to_sp(ALICE_PUPPET_BEAM_Y_PX); \
    alice_puppet0.hp = ALICE_PUPPET_HP; \
    alice_puppet1.hp = ALICE_PUPPET_HP; \
    alice_puppet_pattern0 = alice_puppet_pattern1 = alice_puppet_hold

// Ring approach and final spread begin from the same previous-position
// anchors, but only the approach resets puppet HP.
#define ALICE_RING_PUPPETS_ANCHOR() \
    alice_puppet0.pos.prev.x.v = to_sp(ALICE_PUPPET_RING_LEFT_X_PX); \
    alice_puppet0.pos.prev.y.v = to_sp(ALICE_PUPPET_RING_Y_PX); \
    alice_puppet1.pos.prev.x.v = to_sp(ALICE_PUPPET_RING_RIGHT_X_PX); \
    alice_puppet1.pos.prev.y.v = to_sp(ALICE_PUPPET_RING_Y_PX)

// Two attack-bank handoffs require the same minimum bullet-clear window.
// Do not increase an already longer clear time or change the check order.
#define ALICE_ENSURE_CLEAR_WINDOW() { \
    if(bullet_clear_time < ALICE_BULLET_CLEAR_MIN_FRAMES) { \
        bullet_clear_time = ALICE_BULLET_CLEAR_MIN_FRAMES; \
    } \
}

// Only transitions that advance one ordinary phase and then reset the clock
// use this ordering; the shared ring-approach label intentionally resets
// its clock before incrementing the phase and is left unchanged.
#define ALICE_NEXT_PHASE_AND_RESET_CLOCK() { \
    boss.phase++; \
    boss.phase_frame = 0; \
}

// The two entering puppets receive identical state setup except their
// separate sweep-in angles. Use the real near `p` and preserve field order.
#define ALICE_START_PUPPET(entrance_angle) { \
    p->flag = ALICE_PUPPET_ACTIVE; \
    p->patnum = ALICE_PUPPET_IDLE_PATNUM; \
    p->radius.radius_motion = to_sp(ALICE_PUPPET_ENTRANCE_RADIUS_PX); \
    p->angle = entrance_angle; \
    p->hp = ALICE_PUPPET_HP; \
    p->pos.cur.x.v = to_sp(ALICE_PUPPET_HIDDEN_X_PX); \
}

void pascal far alice_update(void)
{
    AlicePuppet near *p;

    homing_target.x = boss.pos.cur.x;
    homing_target.y = boss.pos.cur.y;
    boss.phase_frame++;
    bullet_template.spawn_type = BST_NORMAL;
    bullet_template.origin.x = boss.pos.cur.x;
    bullet_template.origin.y.v = boss.pos.cur.y.v + to_sp(ALICE_BULLET_ORIGIN_OFFSET_Y_PX);
    gather_template.center = bullet_template.origin;

    switch(boss.phase) {
    case ALICE_PHASE_SETUP:
        if(boss.phase_frame == ALICE_SETUP_ENTRY_FRAME) {
            boss.hp = ALICE_HP_TOTAL;
            boss.phase_end_hp = ALICE_WAVE_ONE_END_HP;
            gather_template.radius.v = to_sp(ALICE_GATHER_RADIUS_PX);
            gather_template.angle_delta = ALICE_GATHER_ANGLE_STEP;
            gather_template.ring_points = ALICE_GATHER_RING_POINTS;
        }
        boss_hittest_shots_invincible();
        if(boss.phase_frame >= ALICE_SETUP_EXIT_FRAME) {
            ALICE_NEXT_PHASE_AND_RESET_CLOCK();
            snd_se_play(ALICE_BOSS_ENTER_SE);
            bg_render_bombing_func = alice_bg_render;
        }
        break;

    case ALICE_PHASE_READY:
        boss_hittest_shots_invincible();
        if(boss.phase_frame >= ALICE_READY_EXIT_FRAME) {
            ALICE_NEXT_PHASE_AND_RESET_CLOCK();
            boss.mode = ALICE_MODE_ATTACK;
            boss.phase_state.patterns_seen = 0;
            alice_scratch.ready_phase_store_only = ALICE_READY_PHASE_STORE_VALUE;
            alice_scratch.beam_phase = ALICE_BEAM_INACTIVE;
        }
        break;

    case ALICE_PHASE_PUPPET_ENTRANCE:
        alice_pattern_opening();
        boss_hittest_shots();
        if(boss.phase_frame == ALICE_PUPPET_APPEAR_FRAME) {
            p = &alice_puppet0;
            ALICE_START_PUPPET(ALICE_PUPPET_ENTRANCE_LEFT_ANGLE);
            p++;
            ALICE_START_PUPPET(ALICE_PUPPET_ENTRANCE_RIGHT_ANGLE);
            alice_puppet_pattern0 = alice_puppet_initial;
            alice_puppet_pattern1 = alice_puppet_initial;
        } else if(boss.phase_frame > ALICE_PUPPET_APPEAR_FRAME) {
            alice_puppets_entrance();
            if(alice_puppet0.radius.radius_motion == 0) {
                boss.phase++;
                boss.mode = ALICE_MODE_REPOSITION;
                boss.phase_frame = 0;
                boss.phase_state.patterns_seen = 0;
                alice_scratch.attack_wave = 0;
                alice_beam_burst_window = ALICE_BEAM_BURST_INITIAL_WINDOW;
            }
        }
        break;

    case ALICE_PHASE_PATTERN_WAVE_1:
    case ALICE_PHASE_PATTERN_WAVE_2:
    case ALICE_PHASE_PATTERN_WAVE_3:
    case ALICE_PHASE_PATTERN_WAVE_4:
        switch(boss.mode) {
        case ALICE_MODE_REPOSITION:
            if(boss_flystep_random(boss.phase_frame - ALICE_RANDOM_FLYSTEP_LEAD_FRAMES)) {
                boss.mode = ALICE_MODE_ATTACK;
                boss.phase_frame = 0;
                boss.phase_state.patterns_seen++;
                if(boss.phase_state.patterns_seen >= ALICE_REGULAR_WAVE_PATTERN_LIMIT) {
                    goto phase_complete;
                }
                alice_pattern_current =
                    alice_pattern_table[alice_scratch.attack_wave][randring2_next16_mod(ALICE_REGULAR_WAVE_VARIANTS)];
            }
            break;
        case ALICE_MODE_ATTACK:
            alice_pattern_current();
            break;
        }
        if(!boss_hittest_shots()) {
            break;
        }
        boss_score_bonus(ALICE_REGULAR_WAVE_BONUS);
        boss_items_drop();
phase_complete:
        alice_scratch.attack_wave++;
        ALICE_ENSURE_CLEAR_WINDOW();
        boss_explode_small(ET_NW_SE);
        ALICE_NEXT_PHASE_AND_RESET_CLOCK();
        boss.phase_state.patterns_seen = 0;
        boss.mode = ALICE_MODE_REPOSITION;
        boss.hp = boss.phase_end_hp;
        if(boss.phase < ALICE_PHASE_PATTERN_WAVE_4) {
            boss.phase_end_hp -= ALICE_WAVE_HP_DECREMENT;
        } else {
            boss.phase_end_hp = 0;
        }
        alice_beam_frame = 0;
        break;

    case ALICE_PHASE_BEAM_APPROACH_1:
    case ALICE_PHASE_BEAM_APPROACH_2:
    case ALICE_PHASE_BEAM_APPROACH_3:
        ALICE_BEAM_PUPPETS_HOLD();
        if(boss_flystep_towards(to_sp(ALICE_BOSS_APPROACH_X_PX), to_sp(ALICE_BOSS_APPROACH_Y_PX))) {
            goto movement_complete;
        }
        goto movement_hittest;

    case ALICE_PHASE_BEAM_ATTACK_1:
    case ALICE_PHASE_BEAM_ATTACK_2:
    case ALICE_PHASE_BEAM_ATTACK_3:
        ALICE_BEAM_PUPPETS_HOLD();
        alice_puppet_beam_pattern();
        boss_hittest_shots();
        if(boss.phase_frame < ALICE_BEAM_ATTACK_TIMEOUT) {
            break;
        }
        boss_score_bonus(ALICE_BEAM_WAVE_BONUS);
        boss_explode_small(ET_NW_SE);
        ALICE_ENSURE_CLEAR_WINDOW();
        ALICE_NEXT_PHASE_AND_RESET_CLOCK();
        alice_scratch.beam_phase = ALICE_BEAM_INACTIVE;
        alice_puppet0.pos.prev.x.v = to_sp(ALICE_PUPPET_POST_BEAM_LEFT_X_PX);
        alice_puppet0.pos.prev.y.v = to_sp(ALICE_PUPPET_POST_BEAM_Y_PX);
        alice_puppet1.pos.prev.x.v = to_sp(ALICE_PUPPET_POST_BEAM_RIGHT_X_PX);
        alice_puppet1.pos.prev.y.v = to_sp(ALICE_PUPPET_POST_BEAM_Y_PX);
        alice_puppet0.phase_frame = alice_puppet1.phase_frame = 0;
        alice_puppet_pattern0 = alice_puppet_spread;
        alice_puppet_pattern1 = alice_puppet_spread;
        break;

    case ALICE_PHASE_RING_APPROACH:
        ALICE_RING_PUPPETS_ANCHOR();
        alice_puppet0.hp = ALICE_PUPPET_HP;
        alice_puppet1.hp = ALICE_PUPPET_HP;
        alice_puppet_pattern0 = alice_puppet_pattern1 = alice_puppet_rings;
        if(!boss_flystep_towards(to_sp(ALICE_BOSS_APPROACH_X_PX), to_sp(ALICE_BOSS_APPROACH_Y_PX))) {
            goto movement_hittest;
        }
movement_complete:
        boss.phase_frame = 0;
        boss.phase++;
movement_hittest:
        boss_hittest_shots();
        break;

    case ALICE_PHASE_FINAL_SPREAD:
        ALICE_RING_PUPPETS_ANCHOR();
        alice_puppet_pattern0 = alice_puppet_pattern1 = alice_puppet_rings;
        alice_pattern_final_spread();
        if(boss.phase_frame < ALICE_FINAL_SPREAD_TIMEOUT) {
            if(!boss_hittest_shots()) {
                break;
            }
            boss.phase_state.defeat_bonus = true;
        }
        boss.phase_frame = 0;
        boss.phase = ALICE_PHASE_EXPLODE_SMALL;
        alice_puppet0.flag = ALICE_PUPPET_DEFEAT_ANIMATION;
        alice_puppet1.flag = ALICE_PUPPET_DEFEAT_ANIMATION;
        break;

    default:
        boss_defeat_update(ALICE_DEFEAT_BONUS);
        break;
    }

    hud_hp_update_and_render(boss.hp, ALICE_HP_TOTAL);
    if(boss.phase >= ALICE_PHASE_PATTERN_WAVE_1 && boss.phase < ALICE_PHASE_EXPLODE_BIG) {
        alice_puppets_update();
    }
}

#undef ALICE_RING_PUPPETS_ANCHOR
#undef ALICE_BEAM_PUPPETS_HOLD

#undef ALICE_NEXT_PHASE_AND_RESET_CLOCK
#undef ALICE_ENSURE_CLEAR_WINDOW

#undef ALICE_START_PUPPET
