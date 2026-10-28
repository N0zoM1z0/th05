// Sprite animation, damage silhouettes and shared/solo defeat rendering.
#pragma option -zCMY_FG_TEXT -zPmain_01
#include "src/main/boss/mai_yuki/foreground.hpp"

#define TH05_MY_FG_COMBINED
#include "src/main/boss/mai_yuki/sprite_put.cpp"
#undef TH05_MY_FG_COMBINED

#include "src/main/boss/mai_yuki/foreground_body.inl"
