// Complete TH05 tile-ring coordinates and near scroll converter interface.
#ifndef TH05_MAIN_SCROLL_RING_SET_HPP
#define TH05_MAIN_SCROLL_RING_SET_HPP
#include "src/shared/abi.hpp"
typedef int subpixel_t;
typedef int vram_y_t;
extern unsigned char scroll_active;
extern unsigned int tile_ring[25][32];
#pragma codeseg SCROLL_RSET_TEXT main_01
extern "C" vram_y_t pascal near scroll_subpixel_y_to_vram_seg1(subpixel_t y);
void pascal tile_ring_set_vo(subpixel_t x, subpixel_t y, unsigned int image_vo);
#pragma codeseg
#endif
