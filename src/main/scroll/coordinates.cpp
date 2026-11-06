// TH04/TH05 scroll_y_1.asm supplies semantics and the actual near Pascal ABI.
// Only the real entry-stack word transport is explicit; arithmetic stays C++.
#pragma option -zCSCROLL_COORDINATE_TEXT -zPmain_01 -k-
#include <dos.h>
#include "src/main/scroll/coordinates.hpp"
#pragma codeseg SCROLL_COORDINATE_TEXT main_01

extern "C" vram_y_t pascal near scroll_subpixel_y_to_vram_seg1(subpixel_t y)
{
    // A near return occupies two bytes. This read occurs before any stack use.
    _BX = _SP;
    int pixel_y = static_cast<int>(peek(_SS, (_BX + 2))) >> 4;
    if(scroll_active) {
        pixel_y += scroll_line;
    }
    // The original applies one correction; it does not normalize arbitrary Y.
    if(pixel_y < 0) {
        pixel_y += SCROLL_RING_HEIGHT;
    } else if(pixel_y >= SCROLL_RING_HEIGHT) {
        pixel_y -= SCROLL_RING_HEIGHT;
    }
    return pixel_y;
}
