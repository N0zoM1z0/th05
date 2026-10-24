// TH05 candidate bullet ABI, adapted from nmlgc/ReC98@b6ba5b0a529edbb3:
// th04/main/bullet/bullet.hpp, bullet.inc and th05/main/bullet/types.h.
// Every data member is represented; no omitted fields or offset padding.
#ifndef TH05_MAIN_BULLET_TEMPLATE_HPP
#define TH05_MAIN_BULLET_TEMPLATE_HPP

#include "src/shared/geometry.hpp"

#define BGC0_STATIC 0
#define BGC0_AIMED 1
#define BGCC_SPREAD 2
#define BGCC_RING 4
#define BGCS_STACK 6
#define BGCF_SINGLE 14

typedef enum {
    BG_SINGLE = BGC0_STATIC,
    BG_SINGLE_AIMED = BGC0_AIMED,
    BG_SPREAD = BGCC_SPREAD,
    BG_SPREAD_AIMED = BGCC_SPREAD + BGC0_AIMED,
    BG_RING = BGCC_RING,
    BG_RING_AIMED = BGCC_RING + BGC0_AIMED,
    BG_STACK = BGCS_STACK,
    BG_STACK_AIMED = BGCS_STACK + BGC0_AIMED,
    BG_SPREAD_STACK = BGCS_STACK + BGCC_SPREAD,
    BG_SPREAD_STACK_AIMED = BGCS_STACK + BGCC_SPREAD + BGC0_AIMED,
    BG_RING_STACK = BGCS_STACK + BGCC_RING,
    BG_RING_STACK_AIMED = BGCS_STACK + BGCC_RING + BGC0_AIMED,
    BG_RANDOM_ANGLE = 12,
    BG_RANDOM_ANGLE_AND_SPEED = 13,
    BG_FORCESINGLE = BGCF_SINGLE,
    BG_FORCESINGLE_AIMED = BGCF_SINGLE + BGC0_AIMED
} bullet_group_t;

enum bullet_special_motion_t {
    _bullet_special_motion_t_offset = 0,
    BSM_DECELERATE_THEN_TURN_AIMED,
    BSM_DECELERATE_THEN_TURN,
    BSM_SPEEDUP,
    BSM_DECELERATE_TO_ANGLE,
    BSM_BOUNCE_LEFT_RIGHT,
    BSM_BOUNCE_TOP_BOTTOM,
    BSM_BOUNCE_LEFT_RIGHT_TOP_BOTTOM,
    BSM_BOUNCE_LEFT_RIGHT_TOP,
    BSM_GRAVITY,
    BSM_EXACT_LINEAR,
    BSM_NONE = 0xff
};

struct BulletTemplate {
    uint8_t spawn_type;
    unsigned char patnum;
    PlayfieldPoint origin;
    bullet_group_t group;
    bullet_special_motion_t special_motion;
    unsigned char spread;
    unsigned char spread_angle_delta;
    unsigned char stack;
    SubpixelLength8 stack_speed_delta;
    unsigned char angle;
    SubpixelLength8 speed;
};

// -b- is part of this producer's recorded compiler contract.
typedef char th05_bullet_group_is_1[(sizeof(bullet_group_t) == 1) ? 1 : -1];
typedef char th05_bullet_motion_is_1[(sizeof(bullet_special_motion_t) == 1) ? 1 : -1];
typedef char th05_bullet_template_is_14[(sizeof(BulletTemplate) == 14) ? 1 : -1];
typedef char th05_template_spawn_at_0[(offsetof(BulletTemplate, spawn_type) == 0) ? 1 : -1];
typedef char th05_template_patnum_at_1[(offsetof(BulletTemplate, patnum) == 1) ? 1 : -1];
typedef char th05_template_origin_at_2[(offsetof(BulletTemplate, origin) == 2) ? 1 : -1];
typedef char th05_template_group_at_6[(offsetof(BulletTemplate, group) == 6) ? 1 : -1];
typedef char th05_template_motion_at_7[(offsetof(BulletTemplate, special_motion) == 7) ? 1 : -1];
typedef char th05_template_spread_at_8[(offsetof(BulletTemplate, spread) == 8) ? 1 : -1];
typedef char th05_template_spread_angle_at_9[(offsetof(BulletTemplate, spread_angle_delta) == 9) ? 1 : -1];
typedef char th05_template_stack_at_10[(offsetof(BulletTemplate, stack) == 10) ? 1 : -1];
typedef char th05_template_stack_speed_at_11[(offsetof(BulletTemplate, stack_speed_delta) == 11) ? 1 : -1];
typedef char th05_template_angle_at_12[(offsetof(BulletTemplate, angle) == 12) ? 1 : -1];
typedef char th05_template_speed_at_13[(offsetof(BulletTemplate, speed) == 13) ? 1 : -1];

#endif
