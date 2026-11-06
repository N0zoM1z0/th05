// The two alternating attacks for each of Shinki's second and third phases.
#pragma option -zCB6_TABLES_TEXT -zPmain_03
#include "src/main/boss/shinki/pattern_tables.hpp"

const pattern_oneshot_func_t SHINKI_PATTERNS_PHASE_2_3[2][2] = {
    { pattern_curved_rings, pattern_dualspeed_rings },
    { pattern_random_directional_and_kunai, pattern_dense_blue_stacks }
};
