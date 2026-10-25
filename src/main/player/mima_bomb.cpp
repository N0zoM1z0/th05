// Natural complete adjacent Mima draw and existing control contribution.
// ReC98 b6ba5b0a th05_main.asm supplies disassembly/semantic evidence only.
#pragma option -zCMIMA_BOMB_TEXT -zPmain_01
#include "src/main/player/mima_bomb.hpp"
#pragma codeseg MIMA_BOMB_TEXT main_01

#include "src/main/player/bomb_body/mima_draw.inl"
// Preserve the existing natural control body and its standalone producer.
// Only its initial compiler segment pragma is conditional in combined mode.
#define TH05_MIMA_BOMB_COMBINED 1
#include "src/main/player/mima_bomb_control.cpp"
#undef TH05_MIMA_BOMB_COMBINED
