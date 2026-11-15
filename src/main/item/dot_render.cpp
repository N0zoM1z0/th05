// C version of item_splash_dot_render(), which sets one pixel in the VRAM
// plane in ES. Not built: Borland compiles it to 42 bytes instead of the
// original 28. The game uses splash_dot_exact.asm.
#pragma option -zCITEM_DOT_TEXT -zPmain_01 -k-
#include "src/shared/abi.hpp"

extern "C" void __fastcall near item_splash_dot_render(int x, int vram_y)
{
    unsigned int offset = ((vram_y * 80) + (x >> 3));
    unsigned char mask = (0x80U >> (x & 7));
    *reinterpret_cast<unsigned char __es *>(offset) = mask;
}
