// Complete shared bullet/laser ABI for later EX-Alice pattern callbacks.
#ifndef TH05_MAIN_BOSS_EXALICE_LASER_PATTERNS_HPP
#define TH05_MAIN_BOSS_EXALICE_LASER_PATTERNS_HPP
#include "src/main/boss/exalice/patterns.hpp"
#include "src/main/player/player.hpp"
#include "src/main/bullet/laser.hpp"

#pragma codeseg EXALICE_LSR_TEXT main_03
extern int exalice_laser_slot;
bool near exalice_pattern_bouncing_rings(void);
bool near exalice_pattern_fixed_laser_fan(void);
bool near exalice_pattern_speedup_fans(void);
bool near exalice_pattern_sweeping_lasers(void);
#endif
