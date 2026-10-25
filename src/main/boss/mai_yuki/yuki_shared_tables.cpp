// Shared-fight semantic near-callback schedules; real providers stay foreign.
#pragma option -zCMAIN_035_TEXT -zPmain_03
#include "src/main/boss/mai_yuki/shared_pattern_tables.hpp"

const MaiYukiPattern YUKI_PATTERNS_FIRST[4] = {
    yuki_pattern_random_aimed_fan,
    yuki_pattern_small_ball_stacks,
    yuki_pattern_random_rings,
    yuki_pattern_small_ball_fan
};

const MaiYukiPattern YUKI_PATTERNS_LASER[4] = {
    yuki_pattern_random_rings,
    yuki_pattern_random_pellets,
    yuki_pattern_ball_stacks,
    yuki_pattern_random_aimed_fan
};

const MaiYukiPattern YUKI_PATTERNS_FINAL[4] = {
    yuki_pattern_cheetos,
    yuki_pattern_reversing_rings,
    yuki_pattern_reversing_rings,
    yuki_pattern_small_ball_stacks
};
