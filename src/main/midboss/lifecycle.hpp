// Complete natural midboss lifecycle/HP/reward family; existing ABI reused.
#ifndef TH05_MAIN_MIDBOSS_LIFECYCLE_HPP
#define TH05_MAIN_MIDBOSS_LIFECYCLE_HPP

#pragma codeseg MIDBOSS_FAMILY_TEXT main_03
void far midboss_reset(void);
void far midboss_activate_if_stage_frame_is_midboss_start_frame(void);
void pascal near hud_hp_update_and_render(int hp_cur, int hp_max);
void pascal near midboss_score_bonus(unsigned int units);
void pascal near boss_score_bonus(unsigned int units);
void near midboss_defeat_update(void);
// Preserve RNG's real first declaration before the foreign callback context.
unsigned int pascal near randring2_next16_mod(unsigned int divisor);

#pragma codeseg MAI_TEXT main_01
#include "src/main/stage/setup.hpp"
void pascal near midboss_invalidate_func(void);
void pascal far hud_hp_put(int value);

#pragma codeseg MIDBOSS_FAMILY_TEXT main_03
extern unsigned int stage_frame;
extern bool midboss_active;
extern nearfunc_t_near midboss_invalidate;
extern nearfunc_t_near midboss_render;
extern func_t_near midboss_update;
extern int hud_hp_bar_value_prev;
extern unsigned long score_delta;
extern bool pointnum_times_2;
extern int playfield_shake_anim_time;
void pascal near pointnums_add_yellow(subpixel_t x, subpixel_t y, uint16_t points);

static const int BAR_MAX = 128;
static const unsigned int MIDBOSS_BONUS_UNIT_VALUE = 1280;
static const unsigned long BOSS_BONUS_UNIT_VALUE = 1000;
static const unsigned char PHASE_EXPLODE_BIG = 254;
static const unsigned char PHASE_NONE = 255;
static const unsigned char PAT_ENEMY_KILL_last = 11;
#endif
