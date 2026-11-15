// Declarations for the bullet, bullet cloud and pellet renderer.
#ifndef TH05_BULLET_RENDER_HPP
#define TH05_BULLET_RENDER_HPP
#include <dos.h>
// explosion.hpp must come first: it declares `static const SEG_PLANE_B`,
// which the SEG_PLANE_B macro from overlay.hpp (via update.hpp) would break.
#include "src/main/boss/explosion.hpp"
#include "src/main/bullet/update.hpp"

// Sprite numbers, named after ReC98's th05/sprites/main_pat.h:
static const int BR_PAT_N_RED = 48;     // PAT_BULLET16_N_RED
static const int BR_CLOUD_BLUE = 12;    // PAT_CLOUD_BULLET16_BLUE
static const int BR_CLOUD_RED = 16;     // PAT_CLOUD_BULLET16_RED
static const int BR_CLOUD_PELLET = 148; // PAT_CLOUD_PELLET
// Frames per cloud animation cel
static const int BR_CLOUD_RATE = 4;
extern unsigned int pellet_bottom_col;

#pragma codeseg BULLET_RENDER_TEXT main_01
extern "C" {
    int pascal near scroll_subpixel_y_to_vram_seg1(subpixel_t y);
    void pascal near z_super_roll_put_tiny_32x32_raw(int patnum);
    void near pellets_render_top(void);
    void near pellets_render_bottom(void);
    void pascal near bullets_render(void);
}
void near grcg_setcolor_direct_raw(void);

// The tiny-sprite blitter takes left in AX and top in DX; the GRCG color
// setter takes the color in AH.
#define bullet_render_tiny32(left_value, top_value, pattern_value) \
    _DX = top_value; _AX = left_value; \
    z_super_roll_put_tiny_32x32_raw(pattern_value)
#define bullet_render_color(color_value) \
    _AH = color_value; grcg_setcolor_direct_raw()

// Layout checks
typedef char bullet_render_full_32[(sizeof(bullet_t) == 32) ? 1 : -1];
typedef char bullet_render_patnum_24[(offsetof(bullet_t, patnum) == 24) ? 1 : -1];
typedef char bullet_render_full_400[(sizeof(bullets) == 400 * 32) ? 1 : -1];
typedef char bullet_render_cloud_slots_180[(sizeof(pellet_clouds_render) == 180 * 2) ? 1 : -1];
#endif
