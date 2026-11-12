// Two full four-slot original attack banks, including their reserved nulls.
#pragma option -zCYUMEKO_SCHEDULE_TEXT -zPmain_03
#include "src/main/boss/yumeko/schedule_data.hpp"

yumeko_pattern_func_t yumeko_patterns_phase2[4] = {
    yumeko_pattern_sword_fan, yumeko_pattern_red_ring, 0, 0
};
yumeko_pattern_func_t yumeko_patterns_phase5[4] = {
    yumeko_pattern_counterrotating_spreads, yumeko_pattern_mirrored_spreads, 0, 0
};
