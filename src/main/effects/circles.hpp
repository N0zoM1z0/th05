// Full circle state, adapted from pinned ReC98 th04/main/circle.cpp.
#ifndef TH05_MAIN_EFFECTS_CIRCLES_HPP
#define TH05_MAIN_EFFECTS_CIRCLES_HPP
#include <dos.h>
#include "src/main/player/reimu.hpp"
struct circle_screen_point_t { int x; int y; };
struct circle_t {
    entity_flag_t flag;
    unsigned char age;
    circle_screen_point_t center;
    pixel_t radius_cur;
    pixel_t radius_delta;
};
extern circle_t circles[8];
extern unsigned char circles_color;
void pascal circles_add_growing(subpixel_t center_x, subpixel_t center_y);
void pascal circles_add_shrinking(subpixel_t center_x, subpixel_t center_y);
void near circles_update(void);
void near circles_render(void);
void near grcg_setcolor_direct_raw(void);
extern "C" void pascal far grcg_circle(int x, int y, int radius);
#define grcg_setcolor_direct(col) _AH = col; grcg_setcolor_direct_raw()
#define PLAYFIELD_LEFT 32
#define PLAYFIELD_TOP 16
#define SUBPIXEL_FACTOR 16
typedef char th05_circle_size_10[(sizeof(circle_t) == 10) ? 1 : -1];
typedef char th05_circle_radius_at_6[(offsetof(circle_t, radius_cur) == 6) ? 1 : -1];
#endif
