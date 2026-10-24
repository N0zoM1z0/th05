// Extra boss collision gating and phase transition, with complete shared ABI.
#ifndef TH05_MAIN_BOSS_EXALICE_PHASE_HPP
#define TH05_MAIN_BOSS_EXALICE_PHASE_HPP
#pragma codeseg EXALICE_PHASE_TEXT main_03
#include "src/main/boss/generic.hpp"

extern bool bombing;
extern unsigned char exalice_bomb_invincibility;
extern bool bullet_zap_drop_point_items;
#pragma codeseg BOSS_TEXT main_03
bool near boss_hittest_shots(void);
void near boss_items_drop(void);
#pragma codeseg EXALICE_PHASE_TEXT main_03
int far exalice_hittest_shots(void);
void pascal near exalice_phase_next(explosion_type_t type, int next_end_hp);
#endif
