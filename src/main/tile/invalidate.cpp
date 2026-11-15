// Clearing and setting every flag of the half-tile dirty map (ReC98
// th04/main/tile/tile.cpp). tiles_redraw_invalidated() redraws flagged halves.
#pragma option -zCTILE_INVALIDATE_TEXT -zPmain_01 -k-
#include <dos.h>
#include "src/shared/abi.hpp"
#pragma codeseg TILE_INVALIDATE_TEXT main_01

// The game's bool is an unsigned byte.
extern uint8_t halftiles_dirty[50][32];

// ZUN bloat: memset(halftiles_dirty, value, sizeof(halftiles_dirty)), which
// Borland would compile to REP STOSW instead of the original REP STOSD.
// ZUN landmine: the direction flag is never cleared before the REP STOSD.
// This is a macro because Turbo C++ rejects inline assembly in inline
// functions.
#define tiles_invalidate_set_all(value) { \
    _ES = FP_SEG(halftiles_dirty); \
    _DI = FP_OFF(halftiles_dirty); \
    _EAX = ((value) | ((value) << 8) | ((value) << 16) | ((value) << 24)); \
    _CX = (sizeof(halftiles_dirty) / sizeof(uint32_t)); \
    asm { rep stosd; } \
}

void near tiles_invalidate_reset(void)
{
    tiles_invalidate_set_all(0ul);
}

// Alignment NOP between the two functions
#pragma codestring "\x90"

void near tiles_invalidate_all(void)
{
    tiles_invalidate_set_all(1ul);
}
