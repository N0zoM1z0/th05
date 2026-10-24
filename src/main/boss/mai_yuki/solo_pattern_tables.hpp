// Real near callback banks used by the two survivor state machines.
#ifndef TH05_B4_SOLO_TABLES_HPP
#define TH05_B4_SOLO_TABLES_HPP
#include "src/shared/abi.hpp"

// Turbo C++ 4.02 uses the same byte boolean as the canonical game headers.
typedef unsigned char bool;

#if GAME != 5 || BINARY != 'M'
#error These callback banks belong to TH05 MAIN
#endif

// Canonical callback types from initial_patterns.hpp and
// mai_solo_laser_cycle.hpp. The laser subpatterns do not return a bool.
typedef bool (near *near MaiYukiPattern)(void);
typedef void (near *near MaiSoloLaserPattern)(void);

#pragma codeseg MAIN_035_TEXT main_03
bool near yuki_solo_ring_sweep(void);
bool near yuki_solo_random_spreads(void);
bool near yuki_solo_random_rings(void);
bool near yuki_solo_snow_fan(void);
bool near yuki_solo_snow_cross(void);
bool near yuki_solo_vector_stacks(void);
void near mai_solo_rotating_fans(void);
void near mai_solo_rotating_rings(void);
void near mai_solo_snow_rings(void);
bool near mai_solo_fans_and_snow(void);
bool near mai_solo_turning_fans(void);
bool near mai_solo_revenge_snow(void);
bool near mai_solo_laser_bounce(void);
bool near mai_solo_widening_fans(void);
bool near mai_solo_turning_stacks(void);
#pragma codeseg

extern MaiYukiPattern yuki_solo_pattern_pair1[2];
extern MaiYukiPattern yuki_solo_pattern_pair2[2];
extern MaiYukiPattern yuki_solo_pattern_final[5];
extern MaiSoloLaserPattern mai_solo_laser_patterns[3];
extern MaiYukiPattern mai_solo_pattern_pair_middle[2];
extern MaiYukiPattern mai_solo_pattern_pair_final[2];
extern MaiYukiPattern mai_solo_pattern_pair_first[2];

typedef char b4_solo_bool_callback_is_2[(sizeof(MaiYukiPattern) == 2) ? 1 : -1];
typedef char b4_solo_void_callback_is_2[(sizeof(MaiSoloLaserPattern) == 2) ? 1 : -1];
#endif
