// Louise's update function and the shared boss functions it calls.
#ifndef TH05_MAIN_BOSS_LOUISE_UPDATE_HPP
#define TH05_MAIN_BOSS_LOUISE_UPDATE_HPP

// louise_bg_render() is in main_01. Turbo C++ binds a function to the segment
// that is active at its first declaration, so declare it before setup.hpp.
#pragma codeseg LOUISE_UPDATE_MAIN01_TEXT main_01
void pascal near louise_bg_render(void);
#pragma codeseg B4_UPDATE_TEXT main_03
#include "src/main/boss/louise/later.hpp"
#include "src/main/boss/generic.hpp"
#pragma codeseg B4_UPDATE_TEXT main_03

static const int LOUISE_HP_TOTAL = 4400;
// Phases. 3 and 6 are short pauses before the next attack phase.
static const unsigned char LOUISE_PHASE_SETUP = 0;
static const unsigned char LOUISE_PHASE_READY = 1;
static const unsigned char LOUISE_PHASE_BLUE_RED_SPREADS = 2;
static const unsigned char LOUISE_PHASE_FIRE_TRANSITION_FIRST = 3;
static const unsigned char LOUISE_PHASE_MIRRORED_FANS = 4;
static const unsigned char LOUISE_PHASE_LASERS_AND_RINGS = 5;
static const unsigned char LOUISE_PHASE_FIRE_TRANSITION_SECOND = 6;
static const unsigned char LOUISE_PHASE_AIMED_PELLETS = 7;
bool pascal near louise_flystep(subpixel_t speed, int end_frame);
bool near boss_hittest_shots(void);
void near boss_hittest_shots_invincible(void);
void pascal near boss_phase_next(explosion_type_t type, int next_end_hp);
void pascal near boss_defeat_update(unsigned int bonus_units);
void pascal near hud_hp_update_and_render(int hp, int total);
void pascal far louise_update(void);

#endif
