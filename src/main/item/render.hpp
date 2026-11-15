// Item and item-splash rendering.
#ifndef TH05_MAIN_ITEM_RENDER_HPP
#define TH05_MAIN_ITEM_RENDER_HPP
#include <dos.h>
#include "src/main/item/splash.hpp"

#pragma codeseg SHARED
extern "C" void pascal far vector2_at(SPPoint near &ret,
    subpixel_t origin_x, subpixel_t origin_y, subpixel_t length, int angle);
#pragma codeseg ITEM_RENDER_TEXT main_01
void near grcg_setcolor_direct_raw(void); // Actual color input is AH.
extern "C" {
    int pascal near scroll_subpixel_y_to_vram_seg1(subpixel_t y);
    // Fastcall: AX = x, DX = VRAM y, ES = plane, no stack arguments.
    void __fastcall near item_splash_dot_render(int x, int vram_y);
    // AX = left, DX = top, ES = plane, plus the sprite as one Pascal word.
    void pascal near z_super_roll_put_tiny_16x16_raw(int patnum);
    void pascal near item_splashes_render(void);
    void pascal near items_render(void);
}
#endif
