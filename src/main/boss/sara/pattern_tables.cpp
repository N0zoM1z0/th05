// Four attack choices in each of Sara's second and third phases.
#pragma option -zCB1_TABLES_TEXT -zPmain_03
#include "src/main/boss/sara/pattern_tables.hpp"

const pattern_loop_func_t SARA_PATTERNS_PHASE_2_3[2][4] = {
    {
        pattern_blue_curve_counterclockwise,
        pattern_blue_curve_clockwise,
        pattern_aimed_red_spread_stack,
        pattern_red_stacks
    },
    {
        pattern_pellet_arcs_at_expanding_random_angles,
        pattern_random_red_rings,
        pattern_accelerating_spirals_clockwise,
        pattern_accelerating_spirals_counterclockwise
    }
};
