// Natural later Yumeko attacks recovered from original TH05 behavior.
// ReC98 b6ba5b0a disassembly is evidence; no compiler body is transcribed.
#pragma option -zCB5_UPDATE_TEXT -zPmain_03
#include "src/main/boss/yumeko/phase_patterns.hpp"
#pragma codeseg B5_UPDATE_TEXT main_03

#define yumeko_angle_a boss_statebyte[15]
#define yumeko_angle_b boss_statebyte[14]
#define yumeko_phase4_fast boss_statebyte[13]
#define yumeko_volley_frames boss_statebyte[12]
#define yumeko_sword_interval boss_statebyte[0]

#include "src/main/boss/yumeko/angle_call.hpp"
#include "src/main/boss/yumeko/aimed_swords.inl"

#include "src/main/boss/yumeko/spreads.inl"
