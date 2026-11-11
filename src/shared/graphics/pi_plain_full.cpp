// Natural TH05 packed .PI full-image drawing through the real near row kernel.
#pragma option -zCSHARED -2 -k-
#include <dos.h>
extern void far *pi_buffers[8];
extern unsigned char pi_headers[8][72];
extern "C" void pascal near pi_put_8_rowloop(int left, int top, int width, int stride);
#pragma codeseg SHARED
void pascal far pi_put_8(int left, int top, int slot)
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
        call near ptr pi_put_8_rowloop
    }
}
