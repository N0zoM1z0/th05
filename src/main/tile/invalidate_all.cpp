// Full half-tile dirty map; use the real Borland memory-fill intrinsic.
#pragma option -zCTILE_INVALIDATE_TEXT -zPmain_01 -k-
#include <mem.h>
#include "src/shared/abi.hpp"
#pragma codeseg TILE_INVALIDATE_TEXT main_01

// The game's bool is an unsigned byte, also used by the canonical boss types.
extern uint8_t halftiles_dirty[50][32];

void near tiles_invalidate_all(void)
{
    __memset__(halftiles_dirty, 1, sizeof(halftiles_dirty));
}
