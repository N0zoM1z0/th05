// Canonical full item/splash geometry and genuine graphics interfaces.
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
    // Real fastcall AX/DX coordinates, ES plane, no stack arguments, RET.
    void __fastcall near item_splash_dot_render(int x, int vram_y);
    // Real hybrid AX/DX coordinates, ES plane, one Pascal word, RET2.
    void pascal near z_super_roll_put_tiny_16x16_raw(int patnum);
    void pascal near item_splashes_render(void);
    void pascal near items_render(void);
}
#endif
