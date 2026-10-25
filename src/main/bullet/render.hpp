// Full canonical bullet/pellet storage and real PC-98 hardware render APIs.
#ifndef TH05_BULLET_RENDER_HPP
#define TH05_BULLET_RENDER_HPP
#include <dos.h>
// Import the existing genuine tiny-sprite API before overlay.hpp defines its
// SEG_PLANE_B macro. No accepted provider or canonical type is changed.
#include "src/main/boss/explosion.hpp"
#include "src/main/bullet/update.hpp"

static const int BR_PAT_N_RED = 48;
static const int BR_CLOUD_BLUE = 12;
static const int BR_CLOUD_RED = 16;
static const int BR_CLOUD_PELLET = 148;
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

// The same real AX/DX sprite and AH GRCG contracts used by the frozen renderers.
#define bullet_render_tiny32(left_value, top_value, pattern_value) \
    _DX = top_value; _AX = left_value; \
    z_super_roll_put_tiny_32x32_raw(pattern_value)
#define bullet_render_color(color_value) \
    _AH = color_value; grcg_setcolor_direct_raw()

typedef char bullet_render_full_32[(sizeof(bullet_t) == 32) ? 1 : -1];
typedef char bullet_render_patnum_24[(offsetof(bullet_t, patnum) == 24) ? 1 : -1];
typedef char bullet_render_full_400[(sizeof(bullets) == 400 * 32) ? 1 : -1];
typedef char bullet_render_cloud_slots_180[(sizeof(pellet_clouds_render) == 180 * 2) ? 1 : -1];
#endif
