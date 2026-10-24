// Complete Mima draw/control context using the accepted full circle/bomb ABI.
#ifndef TH05_MIMA_BOMB_HPP
#define TH05_MIMA_BOMB_HPP
#include <dos.h>
#pragma codeseg MIMA_BOMB_TEXT main_01
#include "src/main/player/mima_circles.hpp"

typedef unsigned int vc2;
#pragma codeseg _TEXT
extern "C" {
    void pascal far grcg_setcolor(int mode, vc2 color);
    void pascal far grcg_vline(int x, int top, int bottom);
    void pascal far grcg_circle(int x, int y, unsigned int radius);
}
#pragma codeseg SHARED
extern "C" void pascal far cdg_put_noalpha_8(int left, int top, int slot);
#pragma codeseg MIMA_BOMB_FOREIGN_TEXT main_01
// Actual foreign custom VRAM backdrop routine, preserved as a near API.
void near mima_bomb_backdrop_render(void);
#pragma codeseg MIMA_BOMB_TEXT main_01
void near grcg_setcolor_direct_raw(void);
void near mima_bomb_draw(void);
void pascal near bomb_mima(void);
#pragma codeseg

static const unsigned int MIMA_BOMB_GRCG_RMW = 0xC0;
typedef char mima_bomb_radius_is_2[(sizeof(int) == 2) ? 1 : -1];
#endif
