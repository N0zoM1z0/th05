// Complete runtime verdict buffers and real device-copy interfaces.
#ifndef TH05_MAINE_STAFF_BITMAP_HPP
#define TH05_MAINE_STAFF_BITMAP_HPP

#include <dos.h>
#include <mem.h>
#include "src/shared/abi.hpp"

#if GAME != 5 || BINARY != 'E'
#error This owner is the TH05 MAINE runtime verdict bitmap transfer
#endif

static const int STAFF_BITMAP_COUNT = 2;
static const int STAFF_BITMAP_HEIGHT = 352;
static const int STAFF_BITMAP_VISIBLE_BYTES = 320 / 8;
static const int STAFF_BITMAP_VRAM_STRIDE = 640 / 8;
static const size_t STAFF_BITMAP_SCREEN_SIZE =
    STAFF_BITMAP_HEIGHT * STAFF_BITMAP_VISIBLE_BYTES;
static const unsigned int STAFF_BITMAP_E_SEGMENT = 0xE000;
static const unsigned int STAFF_BITMAP_B_SEGMENT = 0xA800;
static const int STAFF_BITMAP_GRCG_TDW = 0x80;
static const int STAFF_BITMAP_GRCG_RMW = 0xC0;

// Same complete unsigned-byte array as staff.cpp; that TU owns the BSS.
extern uint8_t verdict_bitmap[STAFF_BITMAP_COUNT]
    [STAFF_BITMAP_HEIGHT][STAFF_BITMAP_VISIBLE_BYTES];

#pragma codeseg _TEXT
extern "C" void pascal far grcg_setcolor(int mode, unsigned int color);
#pragma codeseg STAFF_BITMAP_TEXT group_01
// bitmap_offset is a byte offset0..14080 into the full two-screen buffer.
void pascal near verdict_bitmap_snap(size_t bitmap_offset);
void pascal near verdict_bitmap_put(size_t bitmap_offset);

typedef char staff_bitmap_total_is_28160[(sizeof(verdict_bitmap) == 28160) ? 1 : -1];
typedef char staff_bitmap_row_is_40[(sizeof(verdict_bitmap[0][0]) == 40) ? 1 : -1];
typedef char staff_bitmap_screen_is_14080[(sizeof(verdict_bitmap[0]) == 14080) ? 1 : -1];
typedef char staff_bitmap_offset_is_2[(sizeof(size_t) == 2) ? 1 : -1];
typedef char staff_bitmap_far_pointer_is_4[(sizeof(uint8_t far *) == 4) ? 1 : -1];

#endif
