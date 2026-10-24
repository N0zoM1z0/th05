// Later EX-Alice patterns, with the canonical shared bullet and boss ABI.
#ifndef TH05_MAIN_BOSS_EXALICE_LATER_HPP
#define TH05_MAIN_BOSS_EXALICE_LATER_HPP
#include "src/main/boss/exalice/patterns.hpp"
#include "src/main/player/player.hpp"

void pascal near firewaves_add(pixel_t amplitude, bool is_right);
extern unsigned int pellet_bottom_col;
extern PlayfieldPoint exalice_aim_origin;

#pragma codeseg EXALICE_LAT_TEXT main_03
bool near exalice_pattern_firewave_fans(void);
bool near exalice_pattern_gravity_stacks(void);
bool near exalice_pattern_diamond_rings(void);
#endif
