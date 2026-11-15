// Draws one wipe step over the given pixel rectangle on the text layer.
// Column [i] (counted from the left if [direction] is positive, or from the
// right otherwise) shows fade cel ([extent] - [i]): fully black from 7 and
// up, transparent below 0. A negative [extent] instead requests clearing the
// whole text layer on the next frame, and an [extent] beyond
// ([width] / 16 + 7) fills the rectangle with color 1 in graphics VRAM.
unsigned char pascal near staff_text_wipe(int left, int top, int width,
    int height, int extent, int direction)
{
    int i;
    int column;
    // One 640-pixel row of 16-pixel gaiji, plus the terminator.
    char row[(STAFF_WIPE_SCREEN_W / STAFF_WIPE_GAIJI_W) + 1];

    if(extent < 0) {
        staff_text_clear_requested = 1;
        return STAFF_WIPE_CLEARED;
    }
    if(extent > ((width / STAFF_WIPE_GAIJI_W) + STAFF_WIPE_FADE_LAST_CEL)) {
        grcg_setcolor(STAFF_WIPE_GRCG_RMW, 1);
        grcg_byteboxfill_x(left / STAFF_WIPE_TEXT_BYTE_W, top,
            (left + width - 1) / STAFF_WIPE_TEXT_BYTE_W, top + height - 1);
        outportb(0x7C, 0); // grcg_off()
        return STAFF_WIPE_COVERED;
    }

    left /= STAFF_WIPE_TEXT_BYTE_W;
    top /= STAFF_WIPE_GAIJI_H;
    width /= STAFF_WIPE_GAIJI_W;
    height /= STAFF_WIPE_GAIJI_H;
    if(direction > 0) {
        column = 0;
    } else {
        column = width - 1;
    }
    // The three increments must stay in the `for` clause to match the
    // original evaluation order.
    for(i = 0; i < width; (i++, column += direction, extent--)) {
        if(extent >= STAFF_WIPE_FADE_LAST_CEL) {
            row[column] = STAFF_WIPE_GLYPH_COVER;
        } else if(extent < 0) {
            row[column] = STAFF_WIPE_GLYPH_EMPTY;
        } else {
            row[column] = STAFF_WIPE_GLYPH_FADE_LAST - extent;
        }
    }
    row[width] = 0;
    // ZUN quirk: Inclusive, just like the cover loops of the image functions.
    for(i = 0; i <= height; i++, top++) {
        if(left < STAFF_WIPE_TEXT_COLS) {
            gaiji_putsa(left, top, row, STAFF_WIPE_TEXT_BLACK);
        }
    }
    return STAFF_WIPE_ACTIVE;
}
