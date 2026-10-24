// Natural remaining Mai/Yuki laser, ring, stack and Cheeto attack providers.
#ifndef TH05_MAIN_BOSS_MAI_YUKI_LATER_PATTERNS_HPP
#define TH05_MAIN_BOSS_MAI_YUKI_LATER_PATTERNS_HPP

#pragma codeseg _TEXT
extern "C" int far pascal iatan2(int y, int x);
#pragma codeseg MAIN_035_TEXT main_03
#include "src/main/boss/mai_yuki/initial_patterns.hpp"
#include "src/main/bullet/laser.hpp"
#pragma codeseg MAIN_035_TEXT main_03
#include "src/main/bullet/cheeto.hpp"
#pragma codeseg MAIN_035_TEXT main_03

static const unsigned char MY_PAT_SMALL_BALL_RED = 50;
static const unsigned char MY_PAT_BALL_RED = 48;

bool near mai_pattern_tracking_laser(void);
bool near mai_pattern_reversing_rings(void);
bool near yuki_pattern_random_aimed_fan(void);
bool near yuki_pattern_random_rings(void);
bool near yuki_pattern_small_ball_stacks(void);
bool near yuki_pattern_small_ball_fan(void);
bool near yuki_pattern_ball_stacks(void);
bool near yuki_pattern_random_pellets(void);
bool near yuki_pattern_reversing_rings(void);
bool near yuki_pattern_cheetos(void);
bool near mai_pattern_cheetos(void);

#endif
