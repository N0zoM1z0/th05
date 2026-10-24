// Natural default midboss/boss reward interfaces, GAME=5.
#ifndef TH05_MAIN_MIDBOSS_DEFAULT_HPP
#define TH05_MAIN_MIDBOSS_DEFAULT_HPP

#pragma codeseg MB_DFT_TEXT main_03
// RNG belongs to main_03 before the foreign main_01 callback declarations.
unsigned int pascal near randring2_next16_mod(unsigned int divisor);
#include "src/main/midboss/state.hpp"
#pragma codeseg MB_DFT_TEXT main_03

static const unsigned int MIDBOSS_BONUS_UNIT_VALUE = 1280;
static const unsigned long BOSS_BONUS_UNIT_VALUE = 1000;
static const unsigned char PHASE_EXPLODE_BIG = 254;
static const unsigned char PHASE_NONE = 255;
static const unsigned char PAT_ENEMY_KILL_last = 11;
// PLAYFIELD_W is provided by the canonical stage/setup.hpp declaration.

extern unsigned long score_delta;
extern bool pointnum_times_2;
extern int playfield_shake_anim_time;

uint16_t pascal near randring2_next16_mod(uint16_t divisor);
void pascal near pointnums_add_yellow(subpixel_t x, subpixel_t y, uint16_t points);
void pascal near midboss_score_bonus(unsigned int units);
void pascal near boss_score_bonus(unsigned int units);
void near midboss_defeat_update(void);

#endif
