// Canonical complete Shinki types and actual first-declaration contexts.
#ifndef TH05_SHINKI_WING_PREPARATION_HPP
#define TH05_SHINKI_WING_PREPARATION_HPP
#include "src/main/boss/movement.hpp"
#pragma codeseg B6_WING_TEXT main_03
bool near pattern_wing_preparation(void);
#pragma codeseg SHARED
extern "C" void pascal far snd_se_play(int new_se);
#pragma codeseg
#include "src/main/boss/shinki/shinki.hpp"
#include "src/main/boss/shinki/wing_coordinates.inl"
#endif
