// Real consecutive bomb procedures, in native order. No synthetic prefix.
#pragma option -zCBOMB_FAMILY_TEXT -zPmain_01
#include "src/main/player/bomb_family.hpp"
#pragma codeseg BOMB_FAMILY_TEXT main_01
#include "src/main/player/bomb_body/runtime.inl"
#include "src/main/player/bomb_body/reimu_stars.inl"
#undef reimu_star_put
#include "src/main/player/bomb_body/reimu_draw.inl"
#define LONG_BOMB_FUNCTION bomb_reimu
#define LONG_BOMB_DRAW reimu_bomb_draw
#define LONG_BOMB_FADE_FRAME 128
#define LONG_BOMB_END_FRAME 160
#define LONG_BOMB_SCROLL_FRAME 130
#include "src/main/player/long_bomb_control.inl"
#undef LONG_BOMB_FUNCTION
#undef LONG_BOMB_DRAW
#undef LONG_BOMB_FADE_FRAME
#undef LONG_BOMB_END_FRAME
#undef LONG_BOMB_SCROLL_FRAME
#include "src/main/player/bomb_body/marisa_lasers.inl"
#undef bomb_beam_color
#include "src/main/player/bomb_body/marisa_draw.inl"
#include "src/main/player/bomb_body/marisa_control.inl"
#include "src/main/player/bomb_body/mima_circles.inl"
#include "src/main/player/bomb_body/mima_draw.inl"
#include "src/main/player/bomb_body/mima_control.inl"
