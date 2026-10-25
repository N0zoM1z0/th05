// Full canonical staff objects and actual master graphics interfaces.
#ifndef TH05_MAINE_STAFF_RENDER_HPP
#define TH05_MAINE_STAFF_RENDER_HPP
#include <dos.h>
#include "src/maine/staff/lifecycle.hpp"

extern screen_point_t space_window_center;
extern unsigned char staff_orb_sprite_frame;
static const int STAFF_STAR_BIG = 6;
static const int STAFF_ORB_FIRST = 8;
static const int STAFF_ORB_W = 32;
static const int STAFF_ORB_H = 32;
static const int STAFF_GRCG_RMW = 0xC0;

#pragma codeseg _TEXT
extern "C" {
    void pascal far grcg_setcolor(int mode, unsigned int color);
    void pascal far grcg_boxfill(int left, int top, int right, int bottom);
    void pascal far grcg_circlefill(int x, int y, unsigned int radius);
    void pascal far super_put_rect(int x, int y, int pattern);
    void pascal far super_put_tiny_small(int x, int y, int pattern);
}
#ifdef TH05_STAFF_FULL_FAMILY
#pragma codeseg STAFF_FULL_TEXT group_01
#else
#pragma codeseg STAFF_DRAW_TEXT group_01
#endif
void near staff_scene_render(void);
#endif
