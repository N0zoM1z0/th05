// Natural TH05 stage-two movement and attack behavior. Pinned ReC98
// b6ba5b0a TH05 disassembly is evidence; no acceptance transfers from TH04.
#pragma option -zCB4_UPDATE_TEXT -zPmain_03
#include "src/main/midboss/stage2_patterns.hpp"
#include "src/main/midboss/stage2_scratch.hpp"
#pragma codeseg B4_UPDATE_TEXT main_03

// Original orbit and projectile payload constants, expressed in source units.
static const int MIDBOSS2_ORBIT_CENTER_LEFT_PX = 128;
static const int MIDBOSS2_ORBIT_CENTER_RIGHT_PX = 256;
static const int MIDBOSS2_ORBIT_DRIFT_STEP = 2;
static const int MIDBOSS2_ORBIT_RADIUS_STEP_PX = 1;
static const int MIDBOSS2_ORBIT_RADIUS_LIMIT_PX = 64;
static const int MIDBOSS2_ORBIT_ANGLE_STEP = 2;
static const int MIDBOSS2_NO_DECEL_SPAWN = 0x10;
static const int MIDBOSS2_CLOUD_NO_DECEL_SPAWN = 0x12;
static const int MIDBOSS2_RED_BALL_PATNUM = 48;
static const int MIDBOSS2_BLUE_BALL_PATNUM = 44;
static const int MIDBOSS2_PATTERN_STACK_COUNT = 3;
static const int MIDBOSS2_PATTERN_STACK_DELTA = 8;
static const int MIDBOSS2_PATTERN_SPEED_SP = 24;
static const int MIDBOSS2_CLOUD_SPREAD_BASE = 3;
static const int MIDBOSS2_CLOUD_SPREAD_MID = 4;
static const int MIDBOSS2_CLOUD_SPREAD_LOW = 6;
static const int MIDBOSS2_CLOUD_HP_MID = 800;
static const int MIDBOSS2_CLOUD_HP_LOW = 600;
static const int MIDBOSS2_FINAL_STACK_COUNT = 3;
static const int MIDBOSS2_FINAL_STACK_DELTA = 15;

#define midboss2_orbit_speed midboss2_scratch.orbit_center_drift
#define midboss2_orbit_contracting midboss2_scratch.orbit_contracting

void near midboss2_move(void)
{
    midboss.pos.prev = midboss.pos.cur;
    vector2_at(midboss.pos.cur, midboss2_orbit_center.x.v,
        midboss2_orbit_center.y.v, midboss.pos.velocity.x.v, midboss.angle);
    midboss2_orbit_center.x.v += static_cast<signed char>(midboss2_orbit_speed);
    if(midboss2_orbit_center.x.v < to_sp(MIDBOSS2_ORBIT_CENTER_LEFT_PX)) {
        midboss2_orbit_speed += MIDBOSS2_ORBIT_DRIFT_STEP;
    } else if(midboss2_orbit_center.x.v > to_sp(MIDBOSS2_ORBIT_CENTER_RIGHT_PX)) {
        midboss2_orbit_speed -= MIDBOSS2_ORBIT_DRIFT_STEP;
    }
    if(midboss2_orbit_contracting == MIDBOSS2_ORBIT_EXPANDING) {
        midboss.pos.velocity.x.v += to_sp(MIDBOSS2_ORBIT_RADIUS_STEP_PX);
        if(midboss.pos.velocity.x.v > to_sp(MIDBOSS2_ORBIT_RADIUS_LIMIT_PX)) {
            midboss2_orbit_contracting = MIDBOSS2_ORBIT_CONTRACTING;
        }
    } else {
        midboss.pos.velocity.x.v -= to_sp(MIDBOSS2_ORBIT_RADIUS_STEP_PX);
        if(midboss.pos.velocity.x.v <= to_sp(MIDBOSS2_ORBIT_RADIUS_STEP_PX)) {
            midboss2_orbit_contracting = MIDBOSS2_ORBIT_EXPANDING;
        }
    }
    midboss.angle -= MIDBOSS2_ORBIT_ANGLE_STEP;
}

void near midboss2_pattern(void)
{
    if(stage_frame_mod16 == 0) {
        bullet_template.spawn_type = MIDBOSS2_NO_DECEL_SPAWN; // No deceleration.
        bullet_template.patnum = MIDBOSS2_RED_BALL_PATNUM; // Red ball.
        bullet_template.group = BG_STACK;
        reinterpret_cast<uint16_t &>(bullet_template.stack) = (MIDBOSS2_PATTERN_STACK_COUNT | (MIDBOSS2_PATTERN_STACK_DELTA << 8));
        bullet_template.speed.v = MIDBOSS2_PATTERN_SPEED_SP;
        bullet_template.angle = randring2_next16();
        bullet_template_tune();
        bullets_add_regular();

        bullet_template.spawn_type = MIDBOSS2_CLOUD_NO_DECEL_SPAWN; // Forward cloud, no deceleration.
        bullet_template.patnum = 0;
        bullet_template.group = BG_RANDOM_ANGLE_AND_SPEED;
        bullet_template.spread = MIDBOSS2_CLOUD_SPREAD_BASE;
        if(midboss.hp <= MIDBOSS2_CLOUD_HP_LOW) {
            bullet_template.spread = MIDBOSS2_CLOUD_SPREAD_LOW;
        } else if(midboss.hp <= MIDBOSS2_CLOUD_HP_MID) {
            bullet_template.spread = MIDBOSS2_CLOUD_SPREAD_MID;
        }
        bullet_template.speed.v = MIDBOSS2_PATTERN_SPEED_SP;
        bullet_template.angle = randring2_next16();
        bullet_template_tune();
        bullets_add_regular();
    }
}

void near midboss2_pattern_final(void)
{
    if(stage_frame_mod4 == 0) {
        bullet_template.spawn_type = MIDBOSS2_NO_DECEL_SPAWN; // No deceleration.
        bullet_template.patnum = MIDBOSS2_BLUE_BALL_PATNUM; // Blue ball.
        bullet_template.group = BG_STACK;
        reinterpret_cast<uint16_t &>(bullet_template.stack) = (MIDBOSS2_FINAL_STACK_COUNT | (MIDBOSS2_FINAL_STACK_DELTA << 8));
        bullet_template.speed.v = MIDBOSS2_PATTERN_SPEED_SP;
        bullet_template.angle = randring2_next16();
        bullet_template_tune();
        bullets_add_regular();
    }
}
