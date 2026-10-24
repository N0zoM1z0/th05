// Complete physical declarations used by the natural TH05 staff-roll owner.
#ifndef TH05_MAINE_STAFF_HPP
#define TH05_MAINE_STAFF_HPP

#include "src/shared/geometry.hpp"

#if GAME != 5 || BINARY != 'E'
#error This owner is the TH05 MAINE staff-roll implementation
#endif

typedef int screen_x_t;
typedef int screen_y_t;
typedef int vram_byte_amount_t;
typedef uint8_t dots8_t;
struct screen_point_t { screen_x_t x; screen_y_t y; };
enum x_direction_t { X_RIGHT = 0, X_LEFT = 1 };

#define BYTE_DOTS 8
extern "C" void pascal far grc_setclip(int left, int top, int right, int bottom);
void pascal near space_window_set(screen_x_t center_x, screen_y_t center_y, pixel_t w, pixel_t h);

typedef char th05_staff_point_is_4[(sizeof(screen_point_t) == 4) ? 1 : -1];
typedef char th05_staff_wide_point_is_8[(sizeof(SPPointBase< SubpixelBase<long, pixel_t> >) == 8) ? 1 : -1];
typedef char th05_staff_direction_is_1[(sizeof(x_direction_t) == 1) ? 1 : -1];

#endif
