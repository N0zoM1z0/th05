// Native 88-byte PC-98 dialog tile-box drawing, source-backed by ReC98 shared.cpp.
// The original GRCG and register-directed row loop use the actual 16-bit ABI.
#pragma option -zCDIALOG_RUN_TEXT -zPmain_01
#include <dos.h>
#include "src/main/dialog/runtime.hpp"
#pragma codeseg DIALOG_RUN_TEXT main_01
extern "C" void pascal far grcg_setcolor(int mode, int color);
extern const unsigned char BOX_TILES[24];
void pascal near dialog_box_put(uscreen_x_t left, uvram_y_t top, int tile)
{
    grcg_setcolor(0xc0, 1);
    _ES = 0xa800;
    _AX = left;
    _DX = top;
    _AX >>= 3;
    _DX <<= 6;
    asm { add ax, dx; }
    _DX >>= 2;
    asm { add ax, dx; }
    asm { mov di, ax; }
    _BX = tile;
    _BX <<= 3;
    _DX = 48;
    box_tile_row:
    {
        _CX = 20;
        _AX = *reinterpret_cast<const unsigned short near *>(BOX_TILES + _BX);
        asm { rep stosw; }
        _BX += 2;
        asm {
            test bx, 7
            jne box_tile_not_wrapped
            sub bx, 8
        box_tile_not_wrapped:
        }
        _DI += 40;
        asm {
            dec dx
            jne box_tile_row
        }
    }
    _DX = 0x7c;
    _AL = 0;
    outportb(_DX, _AL);
}
