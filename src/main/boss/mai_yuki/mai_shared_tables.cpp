// Shared-fight semantic near-callback schedules; real providers stay foreign.
#pragma option -zCMAIN_035_TEXT -zPmain_03
#include "src/main/boss/mai_yuki/shared_pattern_tables.hpp"

const MaiYukiPattern MAI_PATTERNS_FIRST[4] = {
    mai_pattern_random_crosses,
    mai_pattern_sweeping_pellets,
    mai_pattern_turning_fan,
    mai_pattern_small_ball_fan
};

const MaiYukiPattern MAI_PATTERNS_FINAL[4] = {
    mai_pattern_cheetos,
    mai_pattern_sweeping_pellets,
    mai_pattern_reversing_rings,
    mai_pattern_reversing_rings
};
