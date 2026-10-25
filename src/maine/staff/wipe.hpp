// Real six-word Pascal text-wipe API; three states are returned in AL.
#ifndef TH05_MAINE_STAFF_WIPE_HPP
#define TH05_MAINE_STAFF_WIPE_HPP

#include <dos.h>
#include "src/shared/abi.hpp"

enum StaffWipeStatus {
    STAFF_WIPE_ACTIVE = 0,
    STAFF_WIPE_CLEARED = 1,
    STAFF_WIPE_COVERED = 2
};

// Byte text selectors in the staff font, not font bitmap data.
enum StaffWipeGlyph {
    STAFF_WIPE_GLYPH_EMPTY = 0x02,
    STAFF_WIPE_GLYPH_COVER = 0x98,
    STAFF_WIPE_GLYPH_FADE_LAST = 0x9F
};
static const int STAFF_WIPE_SCREEN_W = 640;
static const int STAFF_WIPE_GAIJI_W = 16;
static const int STAFF_WIPE_GAIJI_H = 16;
static const int STAFF_WIPE_TEXT_BYTE_W = 8;
static const int STAFF_WIPE_TEXT_COLS = 80;
static const int STAFF_WIPE_FADE_LAST_CEL = 7;
static const int STAFF_WIPE_GRCG_RMW = 0xC0;
static const unsigned int STAFF_WIPE_TEXT_BLACK = 0x01;

extern unsigned char staff_text_clear_requested;

#pragma codeseg _TEXT
extern "C" {
    void pascal far grcg_setcolor(int mode, unsigned int color);
    void pascal far grcg_byteboxfill_x(int left, int top, int right, int bottom);
    void pascal far gaiji_putsa(unsigned int x, unsigned int y,
        const char far *text, unsigned int attribute);
}

#ifdef TH05_STAFF_FULL_FAMILY
#pragma codeseg STAFF_FULL_TEXT group_01
#else
#pragma codeseg STAFF_WIPE_TEXT group_01
#endif
// Identical to the shared image_phase.hpp API; no bool or enum-return alias.
unsigned char pascal near staff_text_wipe(int left, int top, int width,
    int height, int extent, int direction);

typedef char staff_wipe_selector_is_1[(sizeof(char) == 1) ? 1 : -1];
typedef char staff_wipe_word_is_2[(sizeof(int) == 2) ? 1 : -1];

#endif
