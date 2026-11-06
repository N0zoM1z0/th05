// TH04 .BB allocation/loading flow, with TH05's unchecked direct DOS transfers.
#pragma option -zCBB_LOAD_TEXT -zPmain_01 -k-
#include <dos.h>
#include "src/main/formats/bb_load.hpp"
#pragma codeseg BB_LOAD_TEXT main_01

bb_tiles8_t __seg *pascal near bb_load(const char far *filename)
{
    register unsigned int original_ds;

    bb_load_seg = reinterpret_cast<bb_tiles8_t __seg *>(hmem_allocbyte(BB_SIZE));
    original_ds = _DS;
    _AX = 0x3D00;
    // DOS consumes the actual far filename in DS:DX. Let the compiler resolve
    // its declared parameter; no hard-coded stack displacement is supplied.
    asm { lds dx, filename; }
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
