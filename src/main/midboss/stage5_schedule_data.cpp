// Stage-five midboss: compiler-linked near callbacks in the real attack order.
#pragma option -zCMIDBOSS5_SCHED_TEXT -zPmain_03
#include "src/main/midboss/stage5_patterns.hpp"
#pragma codeseg MIDBOSS5_SCHED_TEXT main_03

const midboss5_pattern_func_t near MIDBOSS5_PATTERNS[3] = {
    midboss5_pattern_blue_spread,
    midboss5_pattern_green_rings,
    midboss5_pattern_aimed_stacks
};

typedef char stage5_callback_is_two[(sizeof(midboss5_pattern_func_t) == 2) ? 1 : -1];
typedef char stage5_three_callbacks_are_six[(sizeof(MIDBOSS5_PATTERNS) == 6) ? 1 : -1];
