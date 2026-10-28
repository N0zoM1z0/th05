// Complete canonical B4 storage and the existing hybrid sprite provider.
#ifndef TH05_B4BALL_RENDER_HPP
#define TH05_B4BALL_RENDER_HPP
#include <dos.h>
#include "src/main/boss/mai_yuki/b4ball.hpp"
#pragma codeseg BULLET_RENDER_TEXT main_01
extern "C" {
    int pascal near scroll_subpixel_y_to_vram_seg1(subpixel_t y);
    void pascal near z_super_roll_put_tiny_32x32_raw(int patnum);
}
static const unsigned int B4_RENDER_VRAM_SEGMENT = 0xA800;
// Real foreign-call contract: AX=left, DX=top, ES=VRAM, one Pascal word.
#define b4_render_tiny32(left_value, top_value, pattern_value) \
    _DX = top_value; _AX = left_value; \
    z_super_roll_put_tiny_32x32_raw(pattern_value)
#endif
