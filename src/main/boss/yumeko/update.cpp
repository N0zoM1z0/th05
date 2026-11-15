// Yumeko's final ring attack and her main update function.
#pragma option -zCB5_UPDATE_TEXT -zPmain_03
#include "src/main/boss/yumeko/update.hpp"
#include "src/main/boss/yumeko/final_ring_scratch.hpp"
#include "src/main/boss/yumeko/phase_timing.hpp"
#pragma codeseg B5_UPDATE_TEXT main_03
// The phase switch table in yumeko_update() is word-aligned, which needs -a2.
// It must come after the declarations above, which require byte alignment.
#pragma option -a2

#define yumeko_final_angle yumeko_final_scratch.pattern_byte14.final_ring_angle
#define yumeko_final_rings yumeko_final_scratch.pattern_byte15.final_ring_count
static const int YUMEKO_HP_TOTAL = 8300;

// Number of direction changes of each final-ring bullet. (The sweep's YSW_
// prefix is misleading, but the name is used by this unit's negative control in
// config/exact_units.toml.)
#define YSW_FINAL_TURNS_MAX 2

enum YumekoPhase {
    YUMEKO_PHASE_HP_FILL = 0,
    YUMEKO_PHASE_ENTRANCE_WAIT = 1,
    YUMEKO_PHASE_MOBILE_FIRST = 2,
    YUMEKO_PHASE_APPROACH_FIRST = 3,
    YUMEKO_PHASE_STATIONARY_FIRST = 4,
    YUMEKO_PHASE_MOBILE_SECOND = 5,
    YUMEKO_PHASE_APPROACH_SECOND = 6,
    YUMEKO_PHASE_STATIONARY_SECOND = 7,
    YUMEKO_PHASE_SWORD_SWEEP = 8,
    YUMEKO_PHASE_FINAL_APPROACH = 9,
    YUMEKO_PHASE_FINAL_RING = 10
};

// 18-way rings of decelerating bullets that turn twice by 0x40, every 16
// frames starting at frame 32. The ring angle advances by 1 for every ring;
// every odd ring is mirrored along the vertical axis and turns the other way.
// The phase ends at frame 1200 at the latest, after 74 rings.
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
            bullet_template.speed.v = (2 * 16 + 6);
            bullet_template_tune();
            snd_se_play(8);
            yumeko_final_rings = 0;
            bullet_special.turns_max = YSW_FINAL_TURNS_MAX;
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

#undef YSW_FINAL_TURNS_MAX

// The stationary attacks and the sword sweep end either on a timeout or once
// their HP is depleted, with a score bonus for every hit until then. The
// `break` leaves the phase switch.
#define YUMEKO_STATIONARY_HIT_WINDOW() \
    if(boss.phase_frame < YUMEKO_STATIONARY_TIMEOUT_FRAMES) { \
        if(!boss_hittest_shots()) { \
            break; \
        } \
        boss_score_bonus(YUMEKO_PATTERN_BONUS); \
    }

#define YUMEKO_ADVANCE_PHASE_CLOCK() \
    boss.phase++; \
    boss.phase_frame = 0

// The mobile waves alternate between the first two attacks of their bank.
#define YUMEKO_SELECT_MOBILE_BANK(bank) \
    yumeko_pattern = bank[boss.phase_state.patterns_seen & 1]

#define YUMEKO_FINISH_MOBILE_WAVE(explosion, hp_end) \
    boss_phase_next(explosion, hp_end)

void pascal far yumeko_update(void)
{
    int patnum;
    homing_target = boss.pos.cur;
    bullet_template.origin = boss.pos.cur;
    gather_template.center = boss.pos.cur;
    sword_template.origin = boss.pos.cur;
    boss.phase_frame++;

    switch(boss.phase) {
    case YUMEKO_PHASE_HP_FILL:
        if(boss.phase_frame == YUMEKO_INITIAL_FRAME) {
            boss.hp = YUMEKO_HP_TOTAL;
            boss.phase_end_hp = YUMEKO_HP_AFTER_SETUP;
            gather_template.radius.v = to_sp(YUMEKO_GATHER_RADIUS_PX);
            gather_template.angle_delta = YUMEKO_GATHER_ANGLE_DELTA;
            gather_template.ring_points = YUMEKO_GATHER_RING_POINTS;
            boss.sprite = YUMEKO_SPRITE_STILL;
            boss.pos.velocity.x.v = to_sp(YUMEKO_INITIAL_VELOCITY_X_PX);
            for(patnum = YUMEKO_TINY_SPRITE_FIRST; patnum < YUMEKO_TINY_SPRITE_AFTER_LAST; patnum++) {
                super_convert_tiny(patnum);
            }
            boss_sprite_left = 180;
            boss_sprite_right = 180;
            boss_sprite_stay = 180;
        }
        if(boss2.pos.cur.y.v >= -to_sp(YUMEKO_GATE_EXIT_Y_PX)) {
            boss2.pos.cur.y.v -= to_sp(YUMEKO_GATE_SPEED_PX);
            shot_hitbox_radius.x.v = to_sp(YUMEKO_GATE_HITBOX_RADIUS_PX);
            shot_hitbox_radius.y.v = to_sp(YUMEKO_GATE_HITBOX_RADIUS_PX);
            shot_hitbox_center = boss2.pos.cur;
            if(shots_hittest()) {
                snd_se_play(YUMEKO_GATE_HIT_SE);
            }
        }
        if(boss.phase_frame < YUMEKO_ENTER_INVINCIBLE_END_FRAME) {
            boss_hittest_shots_invincible();
            break;
        }
        boss.sprite = YUMEKO_SPRITE_MOVE;
        boss.pos.cur.x.v += to_sp(YUMEKO_ENTER_MOVE_X_STEP_PX);
        if(boss.pos.cur.x.v >= to_sp(YUMEKO_ARENA_CENTER_X_PX)) {
            boss.sprite = YUMEKO_SPRITE_STILL;
            YUMEKO_ADVANCE_PHASE_CLOCK();
            snd_se_play(YUMEKO_ENTRANCE_END_SE);
            bg_render_bombing_func = yumeko_bg_render;
        }
        break;

    case YUMEKO_PHASE_ENTRANCE_WAIT:
        boss_hittest_shots_invincible();
        if(boss.phase_frame >= YUMEKO_READY_END_FRAME) {
            YUMEKO_ADVANCE_PHASE_CLOCK();
            boss.mode = YUMEKO_MODE_ATTACK;
            boss.phase_state.patterns_seen = 0;
            yumeko_pattern = yumeko_pattern_sword_fan;
            boss_custombullets_render = swords_render;
        }
        break;

    case YUMEKO_PHASE_MOBILE_FIRST:
    case YUMEKO_PHASE_MOBILE_SECOND:
        switch(boss.mode) {
        case YUMEKO_MODE_REPOSITION:
            if(yumeko_flystep_bounce(to_sp(YUMEKO_BOUNCE_SPEED_PX), YUMEKO_MOBILE_REPOSITION_FRAMES)) {
                boss.phase_frame = 0;
                boss.mode++;
                boss.phase_state.patterns_seen++;
                // The first attack of each wave was already selected when
                // entering its phase, so a wave consists of 20 attacks. The
                // 20th reposition ends the wave without a hit test.
                if(boss.phase_state.patterns_seen >= YUMEKO_WAVE_PATTERN_LIMIT) {
                    goto moving_phase_end;
                }
                if(boss.phase == YUMEKO_PHASE_MOBILE_FIRST) {
                    YUMEKO_SELECT_MOBILE_BANK(yumeko_patterns_phase2);
                } else {
                    YUMEKO_SELECT_MOBILE_BANK(yumeko_patterns_phase5);
                }
            }
            break;
        case YUMEKO_MODE_ATTACK:
            yumeko_pattern();
            break;
        }
        if(boss.mode == YUMEKO_MODE_REPOSITION) {
            break;
        }
        if(!boss_hittest_shots()) {
            break;
        }
        boss_score_bonus(YUMEKO_PATTERN_BONUS);
    moving_phase_end:
        if(boss.phase == YUMEKO_PHASE_MOBILE_FIRST) {
            YUMEKO_FINISH_MOBILE_WAVE(ET_CIRCLE, YUMEKO_HP_AFTER_MOBILE_FIRST);
        } else {
            YUMEKO_FINISH_MOBILE_WAVE(ET_HORIZONTAL, YUMEKO_HP_AFTER_MOBILE_SECOND);
        }
        break;

    case YUMEKO_PHASE_APPROACH_FIRST:
    case YUMEKO_PHASE_APPROACH_SECOND:
        boss_hittest_shots();
        if(boss_flystep_towards(to_sp(YUMEKO_ARENA_CENTER_X_PX), to_sp(YUMEKO_WAVE_APPROACH_Y_PX))) {
            YUMEKO_ADVANCE_PHASE_CLOCK();
            if(boss.phase == YUMEKO_PHASE_STATIONARY_FIRST) {
                yumeko_pattern = yumeko_pattern_aimed_swords;
            } else {
                yumeko_pattern = yumeko_pattern_laser_swords;
            }
        }
        break;

    case YUMEKO_PHASE_STATIONARY_FIRST:
    case YUMEKO_PHASE_STATIONARY_SECOND:
        yumeko_pattern();
        YUMEKO_STATIONARY_HIT_WINDOW();
        if(boss.phase == YUMEKO_PHASE_STATIONARY_FIRST) {
            boss_phase_next(ET_NW_SE, YUMEKO_HP_AFTER_STATIONARY_FIRST);
            yumeko_pattern = yumeko_pattern_counterrotating_spreads;
        } else {
            boss_phase_next(ET_NW_SE, YUMEKO_HP_AFTER_STATIONARY_SECOND);
        }
        boss.mode = YUMEKO_MODE_ATTACK;
        break;

    case YUMEKO_PHASE_SWORD_SWEEP:
        yumeko_pattern_sword_sweep();
        YUMEKO_STATIONARY_HIT_WINDOW();
        boss_phase_next(ET_NW_SE, YUMEKO_HP_AFTER_SWEEP);
        break;

    case YUMEKO_PHASE_FINAL_APPROACH:
        boss_hittest_shots();
        if(boss_flystep_towards(to_sp(YUMEKO_ARENA_CENTER_X_PX), to_sp(YUMEKO_FINAL_APPROACH_Y_PX))) {
            YUMEKO_ADVANCE_PHASE_CLOCK();
            // [patterns_seen] and [defeat_bonus] share the same byte. This
            // clears the bonus for the case of a timeout in the final phase.
            boss.phase_state.patterns_seen = 0;
        }
        break;

    case YUMEKO_PHASE_FINAL_RING:
        // Frame 1200 still fires the 74th ring before the timeout. Only
        // depleting the HP awards the defeat bonus.
        yumeko_pattern_final_ring();
        if(boss.phase_frame < YUMEKO_FINAL_RING_TIMEOUT_FRAMES) {
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
        boss_defeat_update(YUMEKO_DEFEAT_BONUS);
        return;
    }
    swords_update();
    hud_hp_update_and_render(boss.hp, YUMEKO_HP_TOTAL);
}

#undef YUMEKO_ADVANCE_PHASE_CLOCK
#undef YUMEKO_STATIONARY_HIT_WINDOW

#undef YUMEKO_FINISH_MOBILE_WAVE
#undef YUMEKO_SELECT_MOBILE_BANK
