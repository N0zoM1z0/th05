// Character-specific constants for the original Yuuka bomb lifecycle.
#pragma option -zCYUUKA_BOMB_TEXT -zPmain_01
#include "src/main/player/long_bomb_control.hpp"
#pragma codeseg YUUKA_BOMB_TEXT main_01
void near yuuka_bomb_draw(void);
#define LONG_BOMB_FUNCTION bomb_yuuka
#define LONG_BOMB_DRAW yuuka_bomb_draw
#define LONG_BOMB_FADE_FRAME 160
#define LONG_BOMB_END_FRAME 192
#define LONG_BOMB_SCROLL_FRAME 161
#include "src/main/player/long_bomb_control.inl"
