// Half-tile dirty-map fills, after ReC98 th04/main/tile/tile.cpp.
#pragma option -zCTILE_INVALIDATE_TEXT -zPmain_01 -k-
#include <dos.h>
#include "src/shared/abi.hpp"
#pragma codeseg TILE_INVALIDATE_TEXT main_01

// The game's bool is an unsigned byte.
extern uint8_t halftiles_dirty[50][32];

// ZUN bloat: memset(halftiles_dirty, value, sizeof(halftiles_dirty)).
// ZUN landmine: DF is not cleared before the backwards-capable REP STOSD.
// (A macro: TCC rejects inline assembly inside inline functions.)
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

#pragma codestring "\x90"

void near tiles_invalidate_all(void)
{
    tiles_invalidate_set_all(1ul);
}
