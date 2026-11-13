// Two complete later Yumeko spreads, independent of the aimed-sword candidate.
#ifndef TH05_YUMEKO_COMBINED_CONTEXT
#pragma option -zCB5_UPDATE_TEXT -zPmain_03
#endif
#include "src/main/boss/yumeko/phase_patterns.hpp"
#include "src/main/boss/yumeko/final_ring_scratch.hpp"
#pragma codeseg B5_UPDATE_TEXT main_03
#define yumeko_angle_a yumeko_pattern_scratch.pattern_byte15.sword_pattern_angle_a
#define yumeko_angle_b boss_statebyte[14]
#include "src/main/boss/yumeko/spreads.inl"
