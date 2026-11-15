// The two alternating attacks of each of EX-Alice's four regular phases.
#pragma option -zCEXALICE_PAIR_DATA_TEXT -zPmain_03
#include "src/main/boss/exalice/pattern_pairs.hpp"

exalice_pattern_t exalice_patterns_by_phase[4][2] = {
    { exalice_pattern_random_fan, exalice_pattern_turning_rings },
    { exalice_pattern_gravity_stacks, exalice_pattern_diamond_rings },
    { exalice_pattern_bouncing_rings, exalice_pattern_speedup_fans },
    { exalice_pattern_cross_cheetos, exalice_pattern_turning_cheetos }
};
