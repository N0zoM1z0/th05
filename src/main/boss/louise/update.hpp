// Natural complete Louise callback and real shared Boss interfaces.
#ifndef TH05_MAIN_BOSS_LOUISE_UPDATE_HPP
#define TH05_MAIN_BOSS_LOUISE_UPDATE_HPP

// This genuine near rendering callback belongs to main_01 before the shared
// setup header repeats its declaration. Its assigned pointer is only16 bits.
#pragma codeseg LOUISE_UPDATE_MAIN01_TEXT main_01
void pascal near louise_bg_render(void);
#pragma codeseg B4_UPDATE_TEXT main_03
#include "src/main/boss/louise/later.hpp"
#include "src/main/boss/generic.hpp"
#pragma codeseg B4_UPDATE_TEXT main_03

static const int LOUISE_HP_TOTAL = 4400;
// Original movement helper: signed speed/frame words, Pascal RET4, truth in AL.
bool pascal near louise_flystep(subpixel_t speed, int end_frame);
bool near boss_hittest_shots(void);
void near boss_hittest_shots_invincible(void);
void pascal near boss_phase_next(explosion_type_t type, int next_end_hp);
void pascal near boss_defeat_update(unsigned int bonus_units);
void pascal near hud_hp_update_and_render(int hp, int total);
void pascal far louise_update(void);

#endif
