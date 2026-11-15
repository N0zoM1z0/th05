// scroll_driver(): advances the background scroll by the current stage's
// speed once per frame (sub_10214 in ReC98 th05_main.asm). Stage 6 (ID 5)
// never scrolls.
#pragma option -zCSCROLL_DRIVER_TEXT -zPmain_01
#include <dos.h>
#include "src/main/scroll/driver.hpp"
#pragma codeseg SCROLL_DRIVER_TEXT main_01

void near scroll_driver(void)
{
    if(stage_id == 5) {
        scroll_active = 0;
    }
    // Remember which origin the back page was drawn with.
    scroll_line_on_page[page_back] = scroll_line;
    if(scroll_row_advance_previous && scroll_active && (stage_id != 5)) {
        graph_scrollup(static_cast<unsigned int>(scroll_line));
    }

    // The speed is in 1/16 pixels per frame. Once the fraction reaches a
    // whole pixel, scroll_line moves back by that many lines.
    scroll_last_delta.v = 0;
    _AL = scroll_subpixel_line.v;
    _AL += scroll_speed.v;
    scroll_subpixel_line.v = _AL;
    if(_AL >= 16) {
        _AH = 0;
        _AX >>= 4;
        // The original tests the sign flag of the subtraction itself; C++
        // would reload scroll_line and compare it.
        asm {
            sub word ptr scroll_line, ax
            jns scroll_line_in_range
        }
        scroll_line += 400;
    scroll_line_in_range:;
        scroll_row_advance_current = _AL;
        scroll_subpixel_line.v &= 15;
        _AX <<= 4;
        scroll_last_delta.v = _AX;
    }
    scroll_tile_ring_update();
}
