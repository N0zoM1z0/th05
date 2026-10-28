// Canonical full Sword state and the genuine AX/DX tiny32 sprite boundary.
#ifndef TH05_YUMEKO_SWORDS_RENDER_HPP
#define TH05_YUMEKO_SWORDS_RENDER_HPP
#include <dos.h>
#include "src/main/boss/yumeko/update.hpp"
#pragma codeseg BULLET_RENDER_TEXT main_01
extern "C" {
    int pascal near scroll_subpixel_y_to_vram_seg1(subpixel_t y);
    void pascal near z_super_roll_put_tiny_32x32_raw(int patnum);
}
#define yumeko_render_tiny32(left_value, top_value, pattern_value) \
    _DX = top_value; _AX = left_value; \
    z_super_roll_put_tiny_32x32_raw(pattern_value)
#endif
