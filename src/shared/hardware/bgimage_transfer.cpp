// Four-plane original PC-98 background snapshot/restore through 386 MOVSD.
#pragma option -zCSHARED -k-
#include <dos.h>
#include "src/shared/hardware/bgimage_free.hpp"
#pragma codeseg _TEXT
extern "C" void __seg *pascal far hmem_allocbyte(unsigned int bytesize);
#pragma codeseg SHARED

extern "C" void far bgimage_snap(void)
{
    if(bgimage.B == 0) {
        bgimage.B = static_cast<unsigned char __seg *>(hmem_allocbyte(32000));
        bgimage.R = static_cast<unsigned char __seg *>(hmem_allocbyte(32000));
        bgimage.G = static_cast<unsigned char __seg *>(hmem_allocbyte(32000));
        bgimage.E = static_cast<unsigned char __seg *>(hmem_allocbyte(32000));
    }
    _DL = 4;
    asm { push ds }
    asm { push 0E000h }
    asm { push word ptr [_bgimage + 6] }
    asm { push 0B800h }
    asm { push word ptr [_bgimage + 4] }
    asm { push 0B000h }
    asm { push word ptr [_bgimage + 2] }
    asm { push 0A800h }
    asm { push word ptr [_bgimage] }
copy_plane_snap:
    asm { pop es }
    asm { pop ds }
    _SI = 0;
    _DI = 0;
    _CX = (32000 / 4);
    asm { rep movsd }
    asm { dec dl; jne copy_plane_snap }
    asm { pop ds }
}

extern "C" void far bgimage_put(void)
{
    _DL = 4;
    asm { push ds }
    asm { push 0E000h }
    asm { push word ptr [_bgimage + 6] }
    asm { push 0B800h }
    asm { push word ptr [_bgimage + 4] }
    asm { push 0B000h }
    asm { push word ptr [_bgimage + 2] }
    asm { push 0A800h }
    asm { push word ptr [_bgimage] }
copy_plane_put:
    asm { pop ds }
    asm { pop es }
    _SI = 0;
    _DI = 0;
    _CX = (32000 / 4);
    asm { rep movsd }
    asm { dec dl; jne copy_plane_put }
    asm { pop ds }
}
