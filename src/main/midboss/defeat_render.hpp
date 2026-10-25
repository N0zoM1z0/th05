// Complete canonical midboss and real polar/scroll/sprite interfaces.
#ifndef TH05_MIDBOSS_DEFEAT_RENDER_HPP
#define TH05_MIDBOSS_DEFEAT_RENDER_HPP
#pragma codeseg SHARED
int far pascal polar(int center, int radius, int ratio);
#pragma codeseg MID_DEFEAT_TEXT main_01
#include "src/main/midboss/render5.hpp"
#include "src/main/boss/explosion.hpp"

extern unsigned char midboss_defeat_angle;
typedef char defeat_render_full_midboss[(sizeof(midboss_stuff_t) == 22) ? 1 : -1];
#endif
