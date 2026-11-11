// Natural TH04/TH05 tile-ring entry; retains the signed subpixel-to-VRAM ABI.
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
    y = scroll_subpixel_y_to_vram_seg1(16 * 16 + y);
    tile_ring[y / 16][x / 16] = image_vo;
    scroll_active = was_scroll_active;
}
