// Original near-function arrays for Yumeko's two mobile attack waves.
#ifndef TH05_YUMEKO_SCHEDULE_DATA_HPP
#define TH05_YUMEKO_SCHEDULE_DATA_HPP
#include "src/shared/abi.hpp"
typedef void (near *near yumeko_pattern_func_t)(void);
#pragma codeseg B5_UPDATE_TEXT main_03
void near yumeko_pattern_sword_fan(void);
void near yumeko_pattern_red_ring(void);
void near yumeko_pattern_counterrotating_spreads(void);
void near yumeko_pattern_mirrored_spreads(void);
#pragma codeseg YUMEKO_SCHEDULE_TEXT main_03
extern yumeko_pattern_func_t yumeko_patterns_phase2[4];
extern yumeko_pattern_func_t yumeko_patterns_phase5[4];
typedef char yumeko_schedules_near2[(sizeof(yumeko_pattern_func_t) == 2) ? 1 : -1];
typedef char yumeko_schedules_size16[(sizeof(yumeko_patterns_phase2) + sizeof(yumeko_patterns_phase5) == 16) ? 1 : -1];
#endif
