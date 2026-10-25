// Canonical byte-bool near callbacks used by the shared Mai/Yuki scheduler.
#ifndef TH05_MAI_YUKI_SHARED_TABLES_HPP
#define TH05_MAI_YUKI_SHARED_TABLES_HPP
#include "src/shared/abi.hpp"
typedef unsigned char bool;
typedef bool (near *near MaiYukiPattern)(void);
#if GAME != 5 || BINARY != 'M'
#error These callback banks belong to TH05 MAIN
#endif
#pragma codeseg MAIN_035_TEXT main_03
bool near mai_pattern_random_crosses(void);
bool near mai_pattern_turning_fan(void);
bool near mai_pattern_sweeping_pellets(void);
bool near mai_pattern_small_ball_fan(void);
bool near mai_pattern_reversing_rings(void);
bool near yuki_pattern_random_aimed_fan(void);
bool near yuki_pattern_random_rings(void);
bool near yuki_pattern_small_ball_stacks(void);
bool near yuki_pattern_small_ball_fan(void);
bool near yuki_pattern_ball_stacks(void);
bool near yuki_pattern_random_pellets(void);
bool near yuki_pattern_reversing_rings(void);
bool near yuki_pattern_cheetos(void);
bool near mai_pattern_cheetos(void);
#pragma codeseg
extern const MaiYukiPattern MAI_PATTERNS_FIRST[4];
extern const MaiYukiPattern MAI_PATTERNS_FINAL[4];
extern const MaiYukiPattern YUKI_PATTERNS_FIRST[4];
extern const MaiYukiPattern YUKI_PATTERNS_LASER[4];
extern const MaiYukiPattern YUKI_PATTERNS_FINAL[4];
typedef char shared_pattern_pointer_is_2[(sizeof(MaiYukiPattern) == 2) ? 1 : -1];
#endif
