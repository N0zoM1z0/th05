// Complete canonical fixed-point values and actual TH05 scroll state.
#ifndef TH05_SCROLL_DRIVER_HPP
#define TH05_SCROLL_DRIVER_HPP
#include "src/shared/geometry.hpp"
#if GAME != 5 || BINARY != 'M'
#error This owner is the TH05 MAIN scrolling driver
#endif

typedef int vram_y_t;
extern unsigned char stage_id;
extern unsigned char page_back;
extern unsigned char scroll_active;
extern vram_y_t scroll_line;
extern vram_y_t scroll_line_on_page[2];
extern SubpixelLength8 scroll_subpixel_line;
extern SubpixelLength8 scroll_speed;
extern Subpixel scroll_last_delta;
extern unsigned char scroll_row_advance_previous;
extern unsigned char scroll_row_advance_current;

#pragma codeseg _TEXT
extern "C" void pascal far graph_scrollup(unsigned int line);
#pragma codeseg SCROLL_RING_CONTEXT main_01
void near scroll_tile_ring_update(void);
#pragma codeseg SCROLL_DRIVER_TEXT main_01
void near scroll_driver(void);
#pragma codeseg

typedef char scroll_driver_fraction_is_1[(sizeof(scroll_subpixel_line) == 1) ? 1 : -1];
typedef char scroll_driver_speed_is_1[(sizeof(scroll_speed) == 1) ? 1 : -1];
typedef char scroll_driver_delta_is_2[(sizeof(scroll_last_delta) == 2) ? 1 : -1];
typedef char scroll_driver_line_is_2[(sizeof(scroll_line) == 2) ? 1 : -1];
typedef char scroll_driver_page_origins_are_4[(sizeof(scroll_line_on_page) == 4) ? 1 : -1];
#endif
