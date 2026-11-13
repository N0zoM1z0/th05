// TH04/TH05 scroll_y_1.asm supplies semantics and the actual near Pascal ABI.
// Only the real entry-stack word transport is explicit; arithmetic stays C++.
#pragma option -zCSCROLL_COORDINATE_TEXT -zPmain_01 -k-
#include <dos.h>
#include "src/main/scroll/coordinates.hpp"
#pragma codeseg SCROLL_COORDINATE_TEXT main_01

extern "C" vram_y_t pascal near scroll_subpixel_y_to_vram_seg1(subpixel_t y)
{
    // Preserve the original AX accumulator and read the real Pascal stack word
    // before any stack use. DOS intrinsics describe registers; no instruction
    // text or emitted opcode is present in this source.
    _BX = _SP;
    _AX = static_cast<int>(peek(_SS, (_BX + 2)));
    _AX = static_cast<short>(_AX) >> 4;
    if(scroll_active) {
        _AX += scroll_line;
    }
    // AX is a 16-bit signed pixel coordinate; retain the original one-step wrap.
    if(static_cast<short>(_AX) < 0) {
        _AX += SCROLL_RING_HEIGHT;
    } else if(static_cast<short>(_AX) >= SCROLL_RING_HEIGHT) {
        _AX -= SCROLL_RING_HEIGHT;
    }
    return _AX;
}
