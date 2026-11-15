// tile_ring_set_vo(): replaces the tile image (as a VRAM offset) at a
// playfield subpixel position (ReC98 th04/main/tile/set.cpp).
#pragma option -zCSCROLL_RSET_TEXT -zPmain_01
#include "src/main/scroll/ring_set.hpp"
#pragma codeseg SCROLL_RSET_TEXT main_01
void pascal tile_ring_set_vo(subpixel_t x_, subpixel_t y_, unsigned int image_vo)
{
    int x = x_;
    vram_y_t y = y_;
    x = x >> 4;
    unsigned char was_scroll_active = scroll_active;
    scroll_active = 1;
    // Temporarily force scrolling so that Y maps into the tile ring. The
    // 16-pixel offset is the playfield's top edge in VRAM.
    y = scroll_subpixel_y_to_vram_seg1(16 * 16 + y);
    tile_ring[y / 16][x / 16] = image_vo;
    scroll_active = was_scroll_active;
}
