// Character-specific constants for the original Reimu bomb lifecycle.
#pragma option -zCREIMU_BOMB_TEXT -zPmain_01
#include "src/main/player/long_bomb_control.hpp"
#pragma codeseg REIMU_BOMB_TEXT main_01
void near reimu_bomb_draw(void);
#define LONG_BOMB_FUNCTION bomb_reimu
#define LONG_BOMB_DRAW reimu_bomb_draw
#define LONG_BOMB_FADE_FRAME 128
#define LONG_BOMB_END_FRAME 160
#define LONG_BOMB_SCROLL_FRAME 130
#include "src/main/player/long_bomb_control.inl"
