// Declarations for swords_add().
#ifndef TH05_MAIN_BOSS_YUMEKO_SWORDS_ADD_HPP
#define TH05_MAIN_BOSS_YUMEKO_SWORDS_ADD_HPP
#include "src/main/boss/yumeko/update.hpp"
#pragma codeseg CIRCLE_TEXT main_01
void pascal far circles_add_shrinking(subpixel_t center_x, subpixel_t center_y);
#pragma codeseg B5_UPDATE_TEXT main_03
extern unsigned char circles_color;
// Takes and returns the speed in AL.
extern "C" unsigned char __fastcall near playperf_speedtune(unsigned char speed);
#pragma codeseg
#endif
