// Complete aimed volleys and random swords, with the native word-value aim ABI.
#ifndef TH05_YUMEKO_COMBINED_CONTEXT
#pragma option -zCB5_UPDATE_TEXT -zPmain_03
#endif
#include "src/main/boss/yumeko/phase_patterns.hpp"
#include "src/main/boss/yumeko/final_ring_scratch.hpp"
#include "src/main/boss/yumeko/angle_call.hpp"
#pragma codeseg B5_UPDATE_TEXT main_03

#define yumeko_angle_a yumeko_boss_scratch.aimed_swords.pattern_byte15.sword_pattern_angle_a
#define yumeko_angle_b yumeko_boss_scratch.aimed_swords.pattern_byte14.paired_angle_b
#define yumeko_phase4_fast yumeko_boss_scratch.aimed_swords.pattern_byte13.aimed_swords_accelerated
#define yumeko_volley_frames yumeko_boss_scratch.aimed_swords.volley_frames
#define yumeko_sword_interval yumeko_boss_scratch.aimed_swords.sword_spawn_interval

#include "src/main/boss/yumeko/aimed_swords.inl"
