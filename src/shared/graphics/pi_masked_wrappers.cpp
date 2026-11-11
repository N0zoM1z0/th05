// TH05 .PI masked draws: full-screen and quadrant, real Turbo C++ Pascal ABI.
#pragma option -zCSHARED
#include <dos.h>
extern void far *pi_buffers[8];
// The real 72-byte PI header has X/Y dimensions at offsets 20 and 22.
// Actual palette and other header fields are external and not emitted here.
extern unsigned char pi_headers[8][72];
extern "C" void pascal near pi_put_masked_8_rowloop(int left, int top, int width, int stride);
#pragma codeseg SHARED

void pascal far pi_put_masked_8(int left, int top, int slot, int mask_id)
{
    _SI = slot;
    _DI = _SI;
    _SI <<= 2;
    asm { les si, pi_buffers[si] }
    asm { imul di, di, 72 }
    asm {
        push left
        push top
        mov ax, word ptr pi_headers[di+20]
        push ax
        shr ax, 1
        push ax
        mov di, word ptr pi_headers[di+22]
        mov ax, mask_id
        call near ptr pi_put_masked_8_rowloop
    }
}

void pascal far pi_put_quarter_masked_8(int left, int top, int slot, int quarter, int mask_id)
{
    _AX = 0;
    _DX = 0;
    _SI = slot;
    _CL = quarter;
    if (_CL & 1) {
        _AX = 160;
    }
    if (_CL & 2) {
        _DX = 4000;
    }
    _SI <<= 2;
    asm { les si, pi_buffers[si] }
    _SI += _AX;
    _ES += _DX;
    asm {
        mov di, 200
        push left
        push top
        push 320
        push 320
        mov ax, mask_id
        call near ptr pi_put_masked_8_rowloop
    }
}
