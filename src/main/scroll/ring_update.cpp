// scroll_tile_ring_update(): when scrolling enters a new tile row, loads that
// row of the current MAP section into the tile ring, then draws the newly
// exposed strip (sub_BD20 in ReC98 th05_main.asm). Called by scroll_driver().
#pragma option -zCSCROLL_RING_CONTEXT
#include <dos.h>
#include "src/main/scroll/driver.hpp"
#pragma codeseg SCROLL_RING_CONTEXT main_01
extern unsigned int std_seg;
extern unsigned int map_seg;
extern unsigned int std_map_section_p;
extern unsigned int std_scroll_speed;
extern signed char tile_row_in_section;
extern unsigned int scroll_tile_row;
extern unsigned int TILE_SECTION_OFFSETS[32];
extern unsigned int tile_ring[25][32];
#pragma codeseg SCROLL_RING_CONTEXT main_01
extern void near egc_start_copy_noframe(void);
extern "C" void near tiles_copy_scroll_strip(void);
#pragma codeseg _TEXT
extern "C" void pascal far EGC_OFF(void);
#pragma codeseg SCROLL_RING_CONTEXT main_01

void near scroll_tile_ring_update(void)
{
    unsigned char previous_advance;
    if((scroll_row_advance_current == 0) &&
       (scroll_row_advance_previous == 0)) {
        return;
    }
    if(scroll_speed.v == 0) {
        return;
    }

    // Load a new tile row whenever scroll_line enters one.
    _AX = scroll_line;
    _AX >>= 4;
    if(_AX != scroll_tile_row) {
        scroll_tile_row = _AX;
        _BX = std_seg;
        _ES = _BX;
        // Each section has 5 rows; after the last one, move to the next
        // section and its scroll speed. A speed of 0 stops scrolling.
        asm { dec tile_row_in_section; jns scroll_ring_row_ready; }
        {
            tile_row_in_section = 4;
            std_map_section_p++;
            std_scroll_speed++;
            _BX = std_scroll_speed;
            _DL = *reinterpret_cast<unsigned char __es *>(_BX);
            scroll_speed.v = _DL;
            if(_DL == 0) {
                scroll_line = 0;
                scroll_row_advance_previous = 0;
                scroll_row_advance_current = 0;
                return;
            }
        }
    scroll_ring_row_ready:
        // DI = &tile_ring[row]; 64 bytes per ring row.
        _AX <<= 6;
        _AX += (unsigned int)tile_ring;
        asm { mov di, ax; }
        asm { xor ax, ax; }
        // SI = section offset + row * 64 inside the MAP segment. TH05 STD files
        // store section IDs pre-multiplied by 2, so the ID is used directly
        // as a byte offset into the WORD table.
        _AL = tile_row_in_section;
        _AX <<= 6;
        _BX = std_map_section_p;
        _BL = *reinterpret_cast<unsigned char __es *>(_BX);
        asm { xor bh, bh; }
        asm { mov bx, word ptr TILE_SECTION_OFFSETS[bx]; }
        asm { mov si, ax; }
        asm { add si, bx; }
        // Copy the 24 visible tiles of the row from the MAP segment.
        asm {
            push ds
            pop es
            push ds
            mov ax, map_seg
            mov ds, ax
            mov cx, 24
            rep movsw
            pop ds
        }
    }

    // Draw the strip that scrolled into view. The back page was last drawn
    // two frames ago, so the strip covers both frames' advance.
    previous_advance = scroll_row_advance_previous;
    scroll_row_advance_previous = scroll_row_advance_current;
    scroll_row_advance_current += previous_advance;
    if(stage_id == 5 || !scroll_active) {
        scroll_row_advance_current = 0;
        return;
    }
    egc_start_copy_noframe();
    tiles_copy_scroll_strip();
    scroll_row_advance_current = 0;
    EGC_OFF();
}
