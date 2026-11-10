// Exact native fixed-point scrolling, original TH05 sub_10214.
// Semantic donor: maintained TH04 src/main/scroll/driver.cpp. Original TH05
// instructions and ReC98 corroborate the stage-six gate, actual 8/16-bit
// accumulator and the native signed word subtraction flags.
#pragma option -zCSCROLL_DRIVER_TEXT -zPmain_01
#include <dos.h>
#include "src/main/scroll/driver.hpp"
#pragma codeseg SCROLL_DRIVER_TEXT main_01

void near scroll_driver(void)
{
    if(stage_id == 5) {
        scroll_active = 0;
    }
    scroll_line_on_page[page_back] = scroll_line;
    if(scroll_row_advance_previous && scroll_active && (stage_id != 5)) {
        graph_scrollup(static_cast<unsigned int>(scroll_line));
    }

    scroll_last_delta.v = 0;
    _AL = scroll_subpixel_line.v;
    _AL += scroll_speed.v;
    scroll_subpixel_line.v = _AL;
    if(_AL >= 16) {
        _AH = 0;
        _AX >>= 4;
        asm {
            sub word ptr scroll_line, ax
            jns scroll_native_nowrap
        }
        scroll_line += 400;
    scroll_native_nowrap:;
        scroll_row_advance_current = _AL;
        scroll_subpixel_line.v &= 15;
        _AX <<= 4;
        scroll_last_delta.v = _AX;
    }
    scroll_tile_ring_update();
}
