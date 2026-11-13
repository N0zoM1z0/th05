// TH04 .BB allocation/loading flow, with TH05's unchecked direct DOS transfers.
#pragma option -zCBB_LOAD_TEXT -zPmain_01 -k-
#include <dos.h>
#include "src/main/formats/bb_load.hpp"
#pragma codeseg BB_LOAD_TEXT main_01

bb_tiles8_t __seg *pascal near bb_load(const char far *filename)
{
    register unsigned int original_ds;

    bb_load_seg = reinterpret_cast<bb_tiles8_t __seg *>(hmem_allocbyte(BB_SIZE));
    // hmem_allocbyte is near-Pascal and removes its own argument. The far
    // filename is therefore at SS:SP+4 after the saved SI; the compiler must
    // not form a BP frame just to name this ABI stack argument.
    _BX = _SP;
    original_ds = _DS;
    _AX = 0x3D00;
    asm { lds dx, dword ptr ss:[bx+4]; }
    geninterrupt(0x21);
    _BX = _AX;
    _DS = original_ds;
    _DS = reinterpret_cast<unsigned int>(bb_load_seg);
    _CX = BB_SIZE;
    _DX = 0;
    _AH = 0x3F;
    geninterrupt(0x21);
    _AH = 0x3E;
    geninterrupt(0x21);
    _DS = original_ds;
    return bb_load_seg;
}
