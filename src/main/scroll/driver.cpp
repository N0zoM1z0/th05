// Ordinary fixed-point scrolling semantics, original TH05 sub_10214.
// Semantic donor: maintained TH04 src/main/scroll/driver.cpp. Original TH05
// instructions and ReC98 b6ba5b0a529edbb31efdf8c0e939263804f8ee47 corroborate
// the stage-six gate and all byte/word state widths independently.
#pragma option -zCSCROLL_DRIVER_TEXT -zPmain_01
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
    if((scroll_subpixel_line.v += scroll_speed.v) >= 16) {
        int advance = (scroll_subpixel_line.v >> 4);
        if((scroll_line -= advance) < 0) {
            scroll_line += 400;
        }
        scroll_row_advance_current = advance;
        scroll_subpixel_line.v &= 15;
        scroll_last_delta.v = (advance << 4);
    }
    scroll_tile_ring_update();
}
