// Full canonical Shinki ABI; no abbreviated entity or HP views.
#ifndef TH05_SHINKI_DEVIL_HPP
#define TH05_SHINKI_DEVIL_HPP
#pragma codeseg B6_DEVIL_TEXT main_03
void near pattern_devil(void);
#pragma codeseg SHARED
extern "C" void pascal far snd_se_play(int new_se);
#pragma codeseg MAIN_0_TEXT main_01
extern "C" int pascal far select_for_rank(int easy, int normal, int hard, int lunatic);
#pragma codeseg
#include "src/main/boss/shinki/shinki.hpp"
#include "src/main/boss/shinki/hp.inl"
#include "src/main/boss/shinki/wing_coordinates.inl"
#endif
