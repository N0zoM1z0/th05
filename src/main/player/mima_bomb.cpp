// Mima's bomb drawing and control.
#pragma option -zCMIMA_BOMB_TEXT -zPmain_01
#include "src/main/player/mima_bomb.hpp"
#pragma codeseg MIMA_BOMB_TEXT main_01

#include "src/main/player/bomb_body/mima_draw.inl"
// The control code is also built on its own; when included here, it skips
// its own segment pragma.
#define TH05_MIMA_BOMB_COMBINED 1
#include "src/main/player/mima_bomb_control.cpp"
#undef TH05_MIMA_BOMB_COMBINED
