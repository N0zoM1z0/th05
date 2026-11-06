// Full canonical interface and real void near attack callbacks.
#ifndef TH05_SARA_PATTERN_TABLES_HPP
#define TH05_SARA_PATTERN_TABLES_HPP
#include "src/main/boss/sara/sara.hpp"

#pragma codeseg B1_UPDATE_TEXT main_03
void near pattern_blue_curve_counterclockwise(void);
void near pattern_blue_curve_clockwise(void);
void near pattern_aimed_red_spread_stack(void);
void near pattern_red_stacks(void);
void near pattern_pellet_arcs_at_expanding_random_angles(void);
void near pattern_random_red_rings(void);
void near pattern_accelerating_spirals_clockwise(void);
void near pattern_accelerating_spirals_counterclockwise(void);
#pragma codeseg B1_TABLES_TEXT main_03

extern const pattern_loop_func_t SARA_PATTERNS_PHASE_2_3[2][4];
typedef char sara_table_pointer_is_2[(sizeof(pattern_loop_func_t) == 2) ? 1 : -1];
typedef char sara_phase_table_is_16[(sizeof(SARA_PATTERNS_PHASE_2_3) == 16) ? 1 : -1];
#endif
