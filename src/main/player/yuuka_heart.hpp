// Full shared bomb storage and real pixel-space polar/sprite interfaces.
#ifndef TH05_YUUKA_HEART_HPP
#define TH05_YUUKA_HEART_HPP
#include "src/main/player/bombanim.hpp"
#pragma codeseg SHARED
extern "C" void pascal far vector2_at(SPPoint near &ret, subpixel_t origin_x,
    subpixel_t origin_y, subpixel_t length, int angle);
#pragma codeseg YUUKA_HEART_TEXT main_01
static const unsigned int BOMB_PLANE_PUT = 0xFFC0;
void near yuuka_heart_update_and_render(void);
#endif
