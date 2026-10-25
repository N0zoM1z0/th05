// Natural runtime VRAM transfer candidate; no generated-size/exactness claim.
#pragma option -zCSTAFF_BITMAP_TEXT -zPgroup_01
#include "src/maine/staff/bitmap.hpp"

void pascal near verdict_bitmap_snap(size_t bitmap_offset)
{
    uint8_t far *destination =
        reinterpret_cast<uint8_t far *>(verdict_bitmap) + bitmap_offset;
    const uint8_t far *source = reinterpret_cast<const uint8_t far *>(
        MK_FP(STAFF_BITMAP_E_SEGMENT, 0));
    int row;

    for(row = 0; row < STAFF_BITMAP_HEIGHT; row++) {
        __memcpy__(destination, source, STAFF_BITMAP_VISIBLE_BYTES);
        destination += STAFF_BITMAP_VISIBLE_BYTES;
        source += STAFF_BITMAP_VRAM_STRIDE;
    }
}

void pascal near verdict_bitmap_put(size_t bitmap_offset)
{
    uint8_t far *destination = reinterpret_cast<uint8_t far *>(
        MK_FP(STAFF_BITMAP_B_SEGMENT, 0));
    const uint8_t far *source =
        reinterpret_cast<const uint8_t far *>(verdict_bitmap) + bitmap_offset;
    int row;

    grcg_setcolor(STAFF_BITMAP_GRCG_TDW, 1);
    for(row = 0; row < STAFF_BITMAP_HEIGHT; row++) {
        // TDW uses the real tile color; incoming CPU data is ignored.
        __memset__(destination, 0, STAFF_BITMAP_VISIBLE_BYTES);
        destination += STAFF_BITMAP_VRAM_STRIDE;
    }

    grcg_setcolor(STAFF_BITMAP_GRCG_RMW, 13);
    destination = reinterpret_cast<uint8_t far *>(
        MK_FP(STAFF_BITMAP_B_SEGMENT, 0));
    for(row = 0; row < STAFF_BITMAP_HEIGHT; row++) {
        __memcpy__(destination, source, STAFF_BITMAP_VISIBLE_BYTES);
        destination += STAFF_BITMAP_VRAM_STRIDE;
        source += STAFF_BITMAP_VISIBLE_BYTES;
    }
    outportb(0x7C, 0);
}
