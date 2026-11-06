// Real MAIN01 near Pascal coordinate conversion, independent of rendering.
#ifndef TH05_MAIN_SCROLL_COORDINATES_HPP
#define TH05_MAIN_SCROLL_COORDINATES_HPP
#include "src/main/runtime/small.hpp"

extern bool scroll_active;
extern vram_y_t scroll_line;
static const int SCROLL_RING_HEIGHT = 400;

#pragma codeseg SCROLL_COORDINATE_TEXT main_01
extern "C" vram_y_t pascal near scroll_subpixel_y_to_vram_seg1(subpixel_t y);
#pragma codeseg
#endif
