// Complete canonical Shot/cache/hit-animation records; genuine VRAM API only.
#ifndef TH05_SHOT_RENDER_HPP
#define TH05_SHOT_RENDER_HPP
#include <dos.h>
#include "src/main/player/shot_runtime.hpp"

static const int SHOT_RENDER_W = 16;
static const int SHOT_RENDER_H = 16;
static const int SHOT_RENDER_LEFT = 32;
static const int SHOT_RENDER_TOP = 16;
static const unsigned int SHOT_RENDER_VRAM_PLANE = 0xA800;

#pragma codeseg SHOT_RENDER_TEXT main_01
void near grcg_setmode_rmw(void);
extern "C" {
    int pascal near scroll_subpixel_y_to_vram_seg1(subpixel_t y);
    // Real hybrid interface: AX=left, DX=top, ES=VRAM plane,
    // one signed-word sprite argument on the Pascal stack; RET2.
    void pascal near z_super_roll_put_tiny_16x16_raw(int patnum);
}
void near shots_render(void);
#pragma codeseg

// This is the existing graphics interface from ReC98 th04/formats/super.h
// and accepted explosion.hpp. It transports coordinates, not compiler math.
#define shot_render_tiny(left_value, top_value, pattern_value) { \
    _DX = (top_value); \
    _AX = (left_value); \
    z_super_roll_put_tiny_16x16_raw(pattern_value); \
}

typedef char shot_render_shot_is_18[(sizeof(Shot) == 18) ? 1 : -1];
typedef char shot_render_cache_is_6[(sizeof(shot_alive_t) == 6) ? 1 : -1];
typedef char shot_render_hitshot_is_14[(sizeof(hitshot_t) == 14) ? 1 : -1];
#endif
