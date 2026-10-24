// Complete shared Cheeto, gather, bullet and boss interfaces for final patterns.
#ifndef TH05_MAIN_BOSS_EXALICE_FINAL_PATTERNS_HPP
#define TH05_MAIN_BOSS_EXALICE_FINAL_PATTERNS_HPP
#include "src/main/boss/exalice/patterns.hpp"
#include "src/main/bullet/cheeto.hpp"
#include "src/main/gather/gather.hpp"
#pragma codeseg SHARED
#include "src/shared/math/vector.hpp"
#pragma codeseg EXALICE_PAT_TEXT main_03
void near gather_add_only(void);
extern "C" void near bullets_add_regular_fixedspeed(void);

#pragma codeseg EXALICE_FIN_TEXT main_03
extern subpixel_t exalice_sweep_x;
bool near exalice_pattern_cross_cheetos(void);
bool near exalice_pattern_turning_cheetos(void);
bool near exalice_pattern_spiral_gather(void);
void near exalice_pattern_final_fan(void);
#endif
