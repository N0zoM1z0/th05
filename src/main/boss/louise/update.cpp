// Complete natural Louise state machine, original MAIN1527:8AD0.
#include "src/main/boss/louise/update.hpp"
#include "src/main/boss/louise/scratch.hpp"
#include "src/main/boss/louise/phase_choreography.hpp"

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
    case LOUISE_PHASE_SETUP:
        if(boss.phase_frame == LOUISE_FIRST_FRAME) {
            boss.hp = LOUISE_HP_TOTAL;
            boss.phase_end_hp = LOUISE_HP_AFTER_SETUP;
            gather_template.radius.v = to_sp(LOUISE_GATHER_RADIUS_PX);
            gather_template.angle_delta = LOUISE_GATHER_ANGLE_DELTA;
            gather_template.ring_points = LOUISE_GATHER_RING_POINTS;
        }
        boss_hittest_shots_invincible();
        if(boss.phase_frame >= LOUISE_HP_FILL_FRAMES) {
            boss.phase++;
            boss.phase_frame = 0;
            snd_se_play(LOUISE_SOUND_ENTRANCE);
            bg_render_bombing_func = louise_bg_render;
        }
        break;

    case LOUISE_PHASE_READY:
        boss_hittest_shots_invincible();
        if(boss.phase_frame >= LOUISE_READY_FRAMES) {
            boss.phase++;
            boss.phase_frame = 0;
            boss.mode = LOUISE_MODE_BLUE_SPREADS;
            boss.phase_state.patterns_seen = 0;
            louise_scratch.charge_speed = LOUISE_INITIAL_CHARGE_SPEED;
            louise_scratch.spread_or_laser_direction = LOUISE_FIRST_PATTERN_BLUE;
        }
        break;

    case LOUISE_PHASE_BLUE_RED_SPREADS:
        switch(boss.mode) {
        case LOUISE_MODE_REPOSITION:
            if(louise_flystep(to_sp(1.0f), LOUISE_BLUE_RED_REPOSITION_FRAMES)) {
                boss.phase_frame = 0;
                boss.phase_state.patterns_seen++;
                boss.mode = (boss.phase_state.patterns_seen & LOUISE_BLUE_RED_PATTERN_PARITY) + LOUISE_MODE_BLUE_SPREADS;
                if(boss.phase_state.patterns_seen >= LOUISE_BLUE_RED_PATTERN_LIMIT) {
                    goto first_phase_done;
                }
            }
            break;
        case LOUISE_MODE_BLUE_SPREADS:
            louise_pattern_blue_spreads();
            break;
        case LOUISE_MODE_RED_STACKS:
            louise_pattern_red_stacks();
            break;
        }
        if(!boss_hittest_shots()) {
            break;
        }
        boss_score_bonus(LOUISE_PATTERN_HIT_BONUS);
    first_phase_done:
        boss_phase_next(ET_NW_SE, LOUISE_HP_AFTER_BLUE_RED_WAVES);
        break;

    case LOUISE_PHASE_FIRE_TRANSITION_FIRST:
        boss_hittest_shots();
        if(boss.phase_frame >= LOUISE_FIRE_TRANSITION_FRAMES) {
            boss.phase_frame = 0;
            boss.phase++;
            boss.sprite = LOUISE_SPRITE_FIRE;
        }
        break;

    case LOUISE_PHASE_MIRRORED_FANS:
        louise_pattern_mirrored_fans();
        if(louise_flystep(to_sp(0.875f), LOUISE_MIRRORED_FAN_REPOSITION_FRAMES)) {
            boss.phase_frame = 0;
            boss.phase_state.patterns_seen++;
            if(boss.phase_state.patterns_seen >= LOUISE_MIRRORED_FAN_PATTERN_LIMIT) {
                goto fan_phase_done;
            }
        }
        if(!boss_hittest_shots()) {
            break;
        }
        boss_score_bonus(LOUISE_PATTERN_HIT_BONUS);
    fan_phase_done:
        boss_phase_next(ET_SW_NE, LOUISE_HP_AFTER_MIRRORED_FANS);
        louise_scratch.next_second_phase_pattern = LOUISE_LATER_PATTERN_SWEEP;
        louise_scratch.charge_speed = LOUISE_LATER_CHARGE_SPEED;
        break;

    case LOUISE_PHASE_LASERS_AND_RINGS:
        switch(boss.mode) {
        case LOUISE_MODE_REPOSITION:
            if(louise_flystep(to_sp(3.0f), LOUISE_LASER_RING_REPOSITION_FRAMES)) {
                boss.mode = louise_scratch.next_second_phase_pattern + LOUISE_MODE_SWEEPING_LASERS;
                louise_scratch.next_second_phase_pattern = LOUISE_SECOND_PATTERN_TOGGLE - louise_scratch.next_second_phase_pattern;
                boss.phase_frame = 0;
                boss.phase_state.patterns_seen++;
                if(boss.phase_state.patterns_seen >= LOUISE_LASER_RING_PATTERN_LIMIT) {
                    goto second_phase_done;
                }
            }
            break;
        case LOUISE_MODE_SWEEPING_LASERS:
            louise_pattern_sweeping_lasers();
            break;
        case LOUISE_MODE_TURNING_RINGS:
            louise_pattern_turning_rings();
            break;
        }
        if(!boss_hittest_shots()) {
            break;
        }
        boss_score_bonus(LOUISE_PATTERN_HIT_BONUS);
    second_phase_done:
        boss_phase_next(ET_NW_SE, LOUISE_HP_AFTER_LASER_RINGS);
        break;

    case LOUISE_PHASE_FIRE_TRANSITION_SECOND:
        boss_hittest_shots();
        if(boss.phase_frame >= LOUISE_FIRE_TRANSITION_FRAMES) {
            boss.phase_frame = 0;
            boss.phase++;
            boss.sprite = LOUISE_SPRITE_FIRE;
        }
        break;

    case LOUISE_PHASE_AIMED_PELLETS:
        louise_pattern_aimed_pellets();
        if(louise_flystep(to_sp(0.5f), LOUISE_FINAL_REPOSITION_FRAMES)) {
            boss.phase_frame = 0;
            boss.phase_state.patterns_seen++;
            if(boss.phase_state.patterns_seen >= LOUISE_AIMED_PELLET_PATTERN_LIMIT) {
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
        boss_defeat_update(LOUISE_DEFEAT_BONUS);
    }
    hud_hp_update_and_render(boss.hp, LOUISE_HP_TOTAL);
}
