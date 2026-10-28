// Complete state machine with actual foreign helpers, no substitute bodies.
#ifndef TH05_SHINKI_UPDATE_STANDALONE_HPP
#define TH05_SHINKI_UPDATE_STANDALONE_HPP
#pragma codeseg SHARED
extern "C" void pascal far snd_se_play(int new_se);
#pragma codeseg
#include "src/main/boss/shinki/shinki.hpp"
#include "src/main/boss/shinki/hp.inl"

#pragma codeseg B6_UPDATE_TEXT main_03
void near phase_2_3_with_pattern(void);
bool near pattern_wing_preparation(void);
bool near pattern_random_directional_and_kunai(void);
void near pattern_random_rain_and_spreads_from_wings(void);
void near pattern_cheetos_within_spread_walls(void);
bool near pattern_wings_to_purple(void);
void near pattern_aimed_b6balls_and_symmetric_spreads(void);
void near pattern_devil(void);
void near pattern_circles_and_alternating_spirals(void);
void near shinki_move_float(void);
extern pattern_oneshot_func_t shinki_phase_2_3_pattern;
extern pattern_loop_func_t shinki_wing_pattern;
#define phase_2_3_pattern shinki_phase_2_3_pattern
#define wing_pattern shinki_wing_pattern
static const int PHASE_2_3_PATTERN_START_FRAME = 32;
#endif
