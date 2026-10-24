// Alice's charged laser/bullet patterns, sharing the validated full game ABI.
#ifndef TH05_MAIN_BOSS_ALICE_CHARGE_PATTERNS_HPP
#define TH05_MAIN_BOSS_ALICE_CHARGE_PATTERNS_HPP

#include "src/main/boss/alice/beam.hpp"
#include "src/main/bullet/laser.hpp"

#pragma codeseg B4_UPDATE_TEXT main_03
void pascal near gather_add_only_3stack(int frame,
    unsigned int first_color, unsigned int other_color);
#pragma codeseg _TEXT
extern "C" int pascal far iatan2(int y, int x);
#pragma codeseg

void near alice_pattern_laser_fan(void);
void near alice_pattern_paired_stacks(void);
void near alice_pattern_rotating_ring(void);

#endif
