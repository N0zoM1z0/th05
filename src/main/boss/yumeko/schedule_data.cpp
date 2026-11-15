// Attack banks for Yumeko's two mobile waves. yumeko_update() alternates
// between the first two entries of each bank.
#pragma option -zCYUMEKO_SCHEDULE_TEXT -zPmain_03
#include "src/main/boss/yumeko/schedule_data.hpp"

yumeko_pattern_func_t yumeko_patterns_phase2[4] = {
    yumeko_pattern_sword_fan, yumeko_pattern_red_ring, 0, 0
};
yumeko_pattern_func_t yumeko_patterns_phase5[12] = {
    yumeko_pattern_counterrotating_spreads, yumeko_pattern_mirrored_spreads
};
