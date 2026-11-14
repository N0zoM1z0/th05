// Natural animation, movement and patterns immediately before Stage3 update.
#include "src/main/midboss/stage3_patterns.hpp"
#include "src/main/midboss/stage3_scratch.hpp"

// Exact movement, charge and projectile values shared by the five leaves.
static const int MIDBOSS3_REPOSITION_TICK_MASK = 3;
static const int MIDBOSS3_REPOS_SPRITE_LIMIT = 220;
static const int MIDBOSS3_REPOS_SPRITE_LAST = 219;
static const int MIDBOSS3_REPOSITION_Y_STEP_PX = 12;
static const int MIDBOSS3_ARENA_LEFT_PX = 64;
static const int MIDBOSS3_ARENA_RIGHT_PX = 320;
static const int MIDBOSS3_SPRITE_STILL = 208;
static const int MIDBOSS3_GATHER_COLOR_FIRST = 11;
static const int MIDBOSS3_GATHER_COLOR_SECOND = 10;
static const int MIDBOSS3_CHARGE_SOUND = 8;
static const int MIDBOSS3_CHARGE_SPRITE_FIRST = 210;
static const int MIDBOSS3_CHARGE_SPRITE_SECOND = 211;
static const int MIDBOSS3_BULLET_SOUND = 15;
static const int MIDBOSS3_VERTICAL_STEP_PX = 4;
static const int MIDBOSS3_P1_FIRST_SPREAD = 3;
static const int MIDBOSS3_P1_FIRST_DELTA = 16;
static const int MIDBOSS3_P1_STACK_COUNT = 4;
static const int MIDBOSS3_P1_SECOND_SPREAD = 4;
static const int MIDBOSS3_P1_SECOND_DELTA = 5;
static const int MIDBOSS3_P1_THIRD_SPREAD = 7;
static const int MIDBOSS3_P1_THIRD_DELTA = 10;
static const int MIDBOSS3_P1_INITIAL_ANGLE = 0x40;
static const int MIDBOSS3_P2_STACK_COUNT = 8;
static const int MIDBOSS3_P2F_E_COUNT = 1;
static const int MIDBOSS3_P2F_E_STEP = 1;
static const int MIDBOSS3_P2F_N_COUNT = 2;
static const int MIDBOSS3_P2F_N_STEP = 4;
static const int MIDBOSS3_P2F_H_COUNT = 3;
static const int MIDBOSS3_P2F_H_STEP = 3;
static const int MIDBOSS3_P2F_L_COUNT = 4;
static const int MIDBOSS3_P2F_L_STEP = 4;
static const int MIDBOSS3_P2T_E_COUNT = 1;
static const int MIDBOSS3_P2T_E_STEP = 1;
static const int MIDBOSS3_P2T_N_COUNT = 3;
static const int MIDBOSS3_P2T_N_STEP = 5;
static const int MIDBOSS3_P2T_H_COUNT = 4;
static const int MIDBOSS3_P2T_H_STEP = 5;
static const int MIDBOSS3_P2T_L_COUNT = 5;
static const int MIDBOSS3_P2T_L_STEP = 4;
static const int MIDBOSS3_P3_FIRST_SPREAD = 16;
static const int MIDBOSS3_P3_FIRST_DELTA = 8;
static const int MIDBOSS3_P3_SECOND_SPREAD = 21;
static const int MIDBOSS3_P3_SECOND_DELTA = 4;

void near midboss3_reposition(void)
{
    if((midboss.phase_frame & MIDBOSS3_REPOSITION_TICK_MASK) == 0) {
        if(midboss3_scratch.reposition_returning == 0) {
            midboss.sprite++;
            if(midboss.sprite >= MIDBOSS3_REPOS_SPRITE_LIMIT) {
                midboss.sprite = MIDBOSS3_REPOS_SPRITE_LAST;
                midboss.pos.cur.y.v += to_sp(MIDBOSS3_REPOSITION_Y_STEP_PX);
                midboss.pos.cur.x = player_pos.cur.x;
                if(midboss.pos.cur.x.v < to_sp(MIDBOSS3_ARENA_LEFT_PX)) {
                    midboss.pos.cur.x.v = to_sp(MIDBOSS3_ARENA_LEFT_PX);
                } else if(midboss.pos.cur.x.v > to_sp(MIDBOSS3_ARENA_RIGHT_PX)) {
                    midboss.pos.cur.x.v = to_sp(MIDBOSS3_ARENA_RIGHT_PX);
                }
                midboss3_scratch.reposition_returning++;
            }
        } else {
            midboss.sprite--;
            if(midboss.sprite < 212) {
                midboss.sprite = MIDBOSS3_SPRITE_STILL;
                midboss3_scratch.reposition_returning = 0;
                midboss.phase_frame = 0;
                midboss3_scratch.active_attack = 0;
            }
        }
    }
}

void near midboss3_gather_charge(void)
{
    gather_add_only_3stack(midboss.phase_frame - 1, MIDBOSS3_GATHER_COLOR_FIRST, MIDBOSS3_GATHER_COLOR_SECOND);
    if(midboss.phase_frame == 1) {
        snd_se_play(MIDBOSS3_CHARGE_SOUND);
        midboss.sprite = MIDBOSS3_CHARGE_SPRITE_FIRST;
        return;
    }
    if(midboss.phase_frame == 16) {
        midboss.sprite = MIDBOSS3_CHARGE_SPRITE_SECOND;
    }
}

void near midboss3_pattern_1(void)
{
    if(midboss.phase_frame < MIDBOSS3_CHARGE_FRAMES) {
        midboss3_gather_charge();
        return;
    }
    if(midboss.phase_frame == MIDBOSS3_VOLLEY_FIRST_FRAME) {
        bullet_template.spawn_type = MIDBOSS3_SPAWN_CLOUD_FORWARDS;
        bullet_template.patnum = MIDBOSS3_PAT_BALL_BLUE;
        bullet_template.speed.v = midboss3_speed(1.5f);
        bullet_template.group = BG_SPREAD_STACK;
        midboss3_set_spread_stack(MIDBOSS3_P1_FIRST_SPREAD, MIDBOSS3_P1_FIRST_DELTA, MIDBOSS3_P1_STACK_COUNT, 0.5f);
        bullet_template.angle = MIDBOSS3_P1_INITIAL_ANGLE;
    fire:
        bullet_template_tune();
        bullets_add_regular();
        snd_se_play(MIDBOSS3_BULLET_SOUND);
        midboss.pos.prev.y = midboss.pos.cur.y;
        midboss.pos.cur.y.v -= to_sp(MIDBOSS3_VERTICAL_STEP_PX);
        return;
    }
    if(midboss.phase_frame == MIDBOSS3_VOLLEY_SECOND_FRAME) {
        bullet_template.patnum = MIDBOSS3_PAT_BALL_RED;
        bullet_template.speed.v = midboss3_speed(3.0f);
        midboss3_set_spread_stack(MIDBOSS3_P1_SECOND_SPREAD, MIDBOSS3_P1_SECOND_DELTA, MIDBOSS3_P1_STACK_COUNT, 0.5f);
        goto fire;
    }
    if(midboss.phase_frame == MIDBOSS3_VOLLEY_THIRD_FRAME) {
        bullet_template.patnum = MIDBOSS3_PAT_BALL_BLUE;
        bullet_template.speed.v = midboss3_speed(2.0f);
        midboss3_set_spread_stack(MIDBOSS3_P1_THIRD_SPREAD, MIDBOSS3_P1_THIRD_DELTA, MIDBOSS3_P1_STACK_COUNT, 0.5f);
        goto fire;
    }
    if(midboss.phase_frame >= MIDBOSS3_PATTERN_REPOSITION_FRAME) {
        midboss3_reposition();
    }
}

void near midboss3_pattern_2(void)
{
    if(midboss.phase_frame < MIDBOSS3_CHARGE_FRAMES) {
        midboss3_gather_charge();
        return;
    }
    if(midboss.phase_frame == MIDBOSS3_VOLLEY_FIRST_FRAME) {
        bullet_template.spawn_type =
            MIDBOSS3_SPAWN_CLOUD_FORWARDS | MIDBOSS3_SPAWN_NO_DECELERATE;
        bullet_template.patnum = MIDBOSS3_PAT_BALL_BLUE;
        bullet_template.speed.v = midboss3_speed(1.5f);
        bullet_template.group = BG_STACK_AIMED;
        midboss3_set_stack(MIDBOSS3_P2_STACK_COUNT, 0.5f);
        bullet_template.angle = 0;
        goto fire;
    }
    if(midboss.phase_frame == MIDBOSS3_VOLLEY_SECOND_FRAME) {
        bullet_template.group = BG_SPREAD_STACK_AIMED;
        bullet_template.patnum = MIDBOSS3_PAT_BALL_RED;
        midboss3_set_spread_for_rank(MIDBOSS3_P2F_E_COUNT, MIDBOSS3_P2F_E_STEP, MIDBOSS3_P2F_N_COUNT, MIDBOSS3_P2F_N_STEP, MIDBOSS3_P2F_H_COUNT, MIDBOSS3_P2F_H_STEP, MIDBOSS3_P2F_L_COUNT, MIDBOSS3_P2F_L_STEP);
    stack:
        midboss3_set_stack(MIDBOSS3_P2_STACK_COUNT, 0.5f);
    fire:
        bullets_add_regular();
        snd_se_play(MIDBOSS3_BULLET_SOUND);
        midboss.pos.prev.y = midboss.pos.cur.y;
        midboss.pos.cur.y.v -= to_sp(MIDBOSS3_VERTICAL_STEP_PX);
        return;
    }
    if(midboss.phase_frame == MIDBOSS3_VOLLEY_THIRD_FRAME) {
        bullet_template.patnum = MIDBOSS3_PAT_BALL_BLUE;
        midboss3_set_spread_for_rank(MIDBOSS3_P2T_E_COUNT, MIDBOSS3_P2T_E_STEP, MIDBOSS3_P2T_N_COUNT, MIDBOSS3_P2T_N_STEP, MIDBOSS3_P2T_H_COUNT, MIDBOSS3_P2T_H_STEP, MIDBOSS3_P2T_L_COUNT, MIDBOSS3_P2T_L_STEP);
        goto stack;
    }
    if(midboss.phase_frame >= MIDBOSS3_PATTERN_REPOSITION_FRAME) {
        midboss3_reposition();
    }
}

void near midboss3_pattern_3(void)
{
    if(midboss.phase_frame < MIDBOSS3_CHARGE_FRAMES) {
        midboss3_gather_charge();
        return;
    }
    if(midboss.phase_frame == MIDBOSS3_VOLLEY_FIRST_FRAME) {
        bullet_template.spawn_type =
            MIDBOSS3_SPAWN_CLOUD_FORWARDS | MIDBOSS3_SPAWN_NO_DECELERATE;
        bullet_template.patnum = MIDBOSS3_PAT_DIAMOND_BLUE;
        bullet_template.speed.v = midboss3_speed(3.0f);
        bullet_template.group = BG_SPREAD;
        bullet_template.spread = MIDBOSS3_P3_FIRST_SPREAD;
        bullet_template.spread_angle_delta = MIDBOSS3_P3_FIRST_DELTA;
        bullet_template.angle = MIDBOSS3_P1_INITIAL_ANGLE;
    fire:
        bullet_template_tune();
        bullets_add_regular();
        snd_se_play(MIDBOSS3_BULLET_SOUND);
        midboss.pos.prev.y = midboss.pos.cur.y;
        midboss.pos.cur.y.v -= to_sp(MIDBOSS3_VERTICAL_STEP_PX);
        return;
    }
    if(midboss.phase_frame == MIDBOSS3_VOLLEY_SECOND_FRAME) {
        bullet_template.speed.v = midboss3_speed(3.0f);
        bullet_template.spread = MIDBOSS3_P3_SECOND_SPREAD;
        bullet_template.spread_angle_delta = MIDBOSS3_P3_SECOND_DELTA;
        goto fire;
    }
    if(midboss.phase_frame == MIDBOSS3_VOLLEY_THIRD_FRAME) {
        bullet_template.spread = MIDBOSS3_P3_FIRST_SPREAD;
        bullet_template.spread_angle_delta = MIDBOSS3_P3_FIRST_DELTA;
        goto fire;
    }
    if(midboss.phase_frame >= MIDBOSS3_PATTERN_REPOSITION_FRAME) {
        midboss3_reposition();
    }
}
