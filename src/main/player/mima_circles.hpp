// Full canonical bomb/player state and actual polar/fill APIs.
#ifndef TH05_MIMA_CIRCLES_HPP
#define TH05_MIMA_CIRCLES_HPP
#include "src/main/player/bombanim.hpp"
#include "src/main/player/player.hpp"
static const pixel_t BOMB_PIXEL_NONE = -999;
extern unsigned int PaletteTone;
extern bool palette_changed;
uint16_t near randring1_next16(void);
#pragma codeseg _TEXT
extern "C" void pascal far grcg_circlefill(int x, int y, unsigned int radius);
#pragma codeseg SHARED
extern "C" void pascal far vector2_at(SPPoint near &ret, subpixel_t origin_x,
    subpixel_t origin_y, subpixel_t length, int angle);
#pragma codeseg MIMA_CIRCLES_TEXT main_01
void near mima_circles_update_and_render(void);
#endif
