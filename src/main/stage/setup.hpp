// Stage setup interfaces adapted from natural C++ in nmlgc/ReC98
// b6ba5b0a529edbb31efdf8c0e939263804f8ee47: th04/main/midboss/midboss.hpp,
// th04/main/boss/boss.hpp, th05/main/stage/setup.cpp and platform.h.
#ifndef TH05_MAIN_STAGE_SETUP_HPP
#define TH05_MAIN_STAGE_SETUP_HPP

#include "src/main/boss/movement.hpp"

typedef void (near pascal *near nearfunc_t_near)(void);
typedef void (far pascal *near func_t_near)(void);
typedef unsigned char bb_tiles8_t;

#define PLAYFIELD_W 384
#define PLAYFIELD_H 368

struct midboss_stuff_t {
    PlayfieldMotion pos;
    unsigned int frames_until;
    int hp;
    unsigned char sprite;
    unsigned char phase;
    int phase_frame;
    unsigned char damage_this_frame;
    unsigned char angle;
};

extern midboss_stuff_t midboss;
extern boss_stuff_t boss2;
extern boss_stuff_t yuki;
extern SPPoint boss_hitbox_radius;
extern unsigned char boss_statebyte[16];
extern nearfunc_t_near midboss_render_func;
extern func_t_near midboss_update_func;
extern func_t_near boss_update;
extern nearfunc_t_near boss_fg_render;
extern nearfunc_t_near boss_custombullets_render;
extern func_t_near boss_update_func;
extern nearfunc_t_near boss_bg_render_func;
extern nearfunc_t_near boss_fg_render_func;
extern nearfunc_t_near boss_backdrop_colorfill;
extern nearfunc_t_near stage_render;
extern nearfunc_t_near stage_invalidate;
extern bb_tiles8_t __seg *bb_boss_seg;
extern bool boss_phase_timed_out;

void near boss_reset(void);
void far explosions_small_reset(void);
bb_tiles8_t __seg *pascal near bb_load(const char far *fn);
void pascal near bb_boss_load(const char far *fn);
void near bb_boss_free(void);
extern "C" {
    void pascal near nullfunc_near(void);
    void pascal far nullfunc_far(void);
    void pascal far hmem_free(void __seg *block);
    int pascal far super_entry_bfnt(const char far *filename);
    void pascal far cdg_load_all_noalpha(int slot, const char far *filename);
    int pascal far select_for_rank(int easy, int normal, int hard, int lunatic);
}

#define STAGE_MIDBOSS_DECL(stage_token) \
    void pascal far midboss##stage_token##_update(void); \
    void pascal near midboss##stage_token##_render(void)
STAGE_MIDBOSS_DECL(1);
STAGE_MIDBOSS_DECL(2);
STAGE_MIDBOSS_DECL(3);
STAGE_MIDBOSS_DECL(4);
STAGE_MIDBOSS_DECL(5);
STAGE_MIDBOSS_DECL(x);

#define STAGE_BOSS_DECL(name_token) \
    void pascal far name_token##_update(void); \
    void pascal near name_token##_fg_render(void); \
    void pascal near name_token##_bg_render(void)
STAGE_BOSS_DECL(sara);
STAGE_BOSS_DECL(louise);
STAGE_BOSS_DECL(alice);
STAGE_BOSS_DECL(mai_yuki);
STAGE_BOSS_DECL(yumeko);
STAGE_BOSS_DECL(shinki);
STAGE_BOSS_DECL(exalice);

void pascal near sara_backdrop_colorfill(void);
void pascal near louise_backdrop_colorfill(void);
void pascal near alice_backdrop_colorfill(void);
void pascal near mai_yuki_backdrop_colorfill(void);
void pascal near yumeko_backdrop_colorfill(void);
void pascal near shinki_stage_backdrop_colorfill(void);
void pascal near stage2_update(void);
void pascal near stage2_invalidate(void);

static const unsigned char PHASE_HP_FILL = 0;
static const int CDG_BG_BOSS = 16;
static const int CDG_BG_2 = 17;
static const int PAT_SARA_STAY = 180;
static const int PAT_SARA_RIGHT = 184;
static const int PAT_SARA_LEFT = 186;
static const int PAT_SHINKI_STILL = 180;
static const pixel_t BOSS_HITBOX_DEFAULT_W = 24;
static const pixel_t BOSS_HITBOX_DEFAULT_H = 24;

// Natural expansion of MotionBase::init; retain its x/x/y/y assignment order.
#define STAGE_MOTION_INIT(motion_value, screen_x_value, screen_y_value) \
    motion_value.cur.x.v = to_sp(screen_x_value); \
    motion_value.prev.x.v = to_sp(screen_x_value); \
    motion_value.cur.y.v = to_sp(screen_y_value); \
    motion_value.prev.y.v = to_sp(screen_y_value)
#define STAGE_POINT_SET(point_value, screen_x_value, screen_y_value) \
    point_value.x.v = to_sp(screen_x_value); \
    point_value.y.v = to_sp(screen_y_value)

typedef char th05_stage_midboss_is_22[(sizeof(midboss_stuff_t) == 22) ? 1 : -1];
typedef char th05_stage_midboss_pos_at_0[(offsetof(midboss_stuff_t, pos) == 0) ? 1 : -1];
typedef char th05_stage_midboss_frames_at_12[(offsetof(midboss_stuff_t, frames_until) == 12) ? 1 : -1];
typedef char th05_stage_midboss_hp_at_14[(offsetof(midboss_stuff_t, hp) == 14) ? 1 : -1];
typedef char th05_stage_midboss_sprite_at_16[(offsetof(midboss_stuff_t, sprite) == 16) ? 1 : -1];
typedef char th05_stage_midboss_phase_at_17[(offsetof(midboss_stuff_t, phase) == 17) ? 1 : -1];
typedef char th05_stage_midboss_phase_frame_at_18[(offsetof(midboss_stuff_t, phase_frame) == 18) ? 1 : -1];
typedef char th05_stage_midboss_damage_at_20[(offsetof(midboss_stuff_t, damage_this_frame) == 20) ? 1 : -1];
typedef char th05_stage_midboss_angle_at_21[(offsetof(midboss_stuff_t, angle) == 21) ? 1 : -1];
typedef char th05_stage_near_callback_is_2[(sizeof(nearfunc_t_near) == 2) ? 1 : -1];
typedef char th05_stage_far_callback_is_4[(sizeof(func_t_near) == 4) ? 1 : -1];
typedef char th05_stage_segment_pointer_is_2[(sizeof(bb_tiles8_t __seg *) == 2) ? 1 : -1];

#endif
