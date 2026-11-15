// scroll_subpixel_y_to_vram_seg1(): subpixel Y to VRAM Y, applying the scroll
// origin while scrolling is active (ReC98 th04/main/scroll_y_1.asm).
// The built version is coordinates.asm; this C++ version compiles to the same
// 40 bytes and is kept as its readable equivalent.
#pragma option -zCSCROLL_COORDINATE_TEXT -zPmain_01 -k-
#include <dos.h>
#include "src/main/scroll/coordinates.hpp"
#pragma codeseg SCROLL_COORDINATE_TEXT main_01

extern "C" vram_y_t pascal near scroll_subpixel_y_to_vram_seg1(subpixel_t y)
{
    // No BP frame: read the parameter through SP, and keep the value in AX.
    _BX = _SP;
    _AX = static_cast<int>(peek(_SS, (_BX + 2)));
    _AX = static_cast<short>(_AX) >> 4;
    if(scroll_active) {
        _AX += scroll_line;
    }
    // The pseudo-registers are unsigned, so the casts are needed to get SAR
    // above and signed comparisons here. Wraps by only one ring height.
    if(static_cast<short>(_AX) < 0) {
        _AX += SCROLL_RING_HEIGHT;
    } else if(static_cast<short>(_AX) >= SCROLL_RING_HEIGHT) {
        _AX -= SCROLL_RING_HEIGHT;
    }
    return _AX;
}
