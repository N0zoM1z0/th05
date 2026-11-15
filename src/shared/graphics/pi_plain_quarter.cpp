// Draws one quarter of a .PI image, using 386 addressing for the source.
#pragma option -zCSHARED -2 -k-
#include <dos.h>
extern void far *pi_buffers[8];
extern "C" void pascal near pi_put_8_rowloop(int left, int top, int width, int stride);
#pragma codeseg SHARED
void pascal far pi_put_quarter_8(int left, int top, int slot, int quarter)
{
    _AX = 0;
    _DX = 0;
    _SI = slot;
    _CL = quarter;
    if(_CL & 1) {
        _AX = 160;
    }
    if(_CL & 2) {
        _DX = 4000;
    }
    _SI <<= 2;
    asm { les si, pi_buffers[si] }
    _SI += _AX;
    _ES += _DX;
    asm {
        push left
        push top
        push 320
        push 320
        mov di, 200
        call near ptr pi_put_8_rowloop
    }
}
