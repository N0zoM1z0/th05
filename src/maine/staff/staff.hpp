// Basic types and the clip-window setter shared by the staff roll sources.
#ifndef TH05_MAINE_STAFF_HPP
#define TH05_MAINE_STAFF_HPP

#include "src/shared/geometry.hpp"

#if GAME != 5 || BINARY != 'E'
#error This header is for TH05 MAINE.EXE only
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

#endif
