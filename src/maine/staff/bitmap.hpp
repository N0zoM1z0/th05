// Declarations for bitmap.cpp and bitmap_snap_segmented.cpp, two plain C++
// versions of the verdict bitmap transfers that do not match the original
// code. The matching versions are in bitmap_hardware_context.inl.
#ifndef TH05_MAINE_STAFF_BITMAP_HPP
#define TH05_MAINE_STAFF_BITMAP_HPP

#include <dos.h>
#include <mem.h>
#include "src/shared/abi.hpp"

#if GAME != 5 || BINARY != 'E'
#error This header is for TH05 MAINE.EXE only
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

// Two copies of the 320×352 verdict screen, as rows of 40 bytes. Same type
// as in staff.cpp.
extern uint8_t verdict_bitmap[STAFF_BITMAP_COUNT]
    [STAFF_BITMAP_HEIGHT][STAFF_BITMAP_VISIBLE_BYTES];

#pragma codeseg _TEXT
extern "C" void pascal far grcg_setcolor(int mode, unsigned int color);
#pragma codeseg STAFF_BITMAP_TEXT group_01
// Copies a single verdict screen from
//	(0, 0) - (320, 352)
// on the E plane in VRAM to ([verdict_bitmap] + [bitmap_offset]).
// [bitmap_offset] can be any byte offset from 0 to 14080, which allows the
// staff roll to scroll between the two screens.
void pascal near verdict_bitmap_snap(size_t bitmap_offset);
// Blits a single verdict screen starting at
// ([verdict_bitmap] + [bitmap_offset]) to
//	(0, 0) - (320, 352)
// in VRAM.
void pascal near verdict_bitmap_put(size_t bitmap_offset);
#endif
