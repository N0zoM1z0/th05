// Native segmented VRAM capture, with the intrinsic owning the row copy.
// The canonical full buffer and near Pascal interface remain unchanged.
#pragma option -zCSTAFF_BITMAP_TEXT -zPgroup_01
#include "src/maine/staff/bitmap.hpp"

void pascal near verdict_bitmap_snap(size_t bitmap_offset)
{
    uint8_t __es *destination;
    const uint8_t near *source;
    int rows;

    // The PC-98 E plane is read through DS, while ES retains the RAM segment.
    // Keep the caller's DS around this real hardware segment transition.
    asm { push ds; }
    _ES = _DS;
    _DS = STAFF_BITMAP_E_SEGMENT;
    source = 0;
    destination = reinterpret_cast<uint8_t __es *>(verdict_bitmap) + bitmap_offset;
    rows = STAFF_BITMAP_HEIGHT;
    do {
        __memcpy__(destination, source, STAFF_BITMAP_VISIBLE_BYTES);
        destination += STAFF_BITMAP_VISIBLE_BYTES;
        source += STAFF_BITMAP_VRAM_STRIDE;
    } while(--rows != 0);
    asm { pop ds; }
}
