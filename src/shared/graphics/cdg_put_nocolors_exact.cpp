// TH05 CDG single-plane blitter, native 16-bit Pascal and register semantics.
#pragma option -zCSHARED
#include <dos.h>
extern unsigned char cdg_slots[64][16];
#pragma codeseg SHARED
void pascal far cdg_put_nocolors_8(int left, int top, int slot)
{
    _SI = slot;
    _SI <<= 4;
    _SI += FP_OFF(cdg_slots);
    _DI = left;
    asm { sar di, 3 }
    _DI += *reinterpret_cast<unsigned int near *>(_SI + 6);
    _AX = *reinterpret_cast<unsigned int near *>(_SI + 8);
    _BX = _AX;
    _AX <<= 2;
    _AX += 80;
    _DX = _AX;
    _AX = top;
    _CX = _AX;
    _AX <<= 2;
    _AX += _CX;
    _AX += 0xA800;
    _ES = _AX;
    asm { push ds }
    asm { mov ds, word ptr [si+12] }
    _SI = 0;
next_row:
    _CX = _BX;
    asm { rep movsd }
    asm { sub di,dx; jns next_row }
    asm { pop ds }
}
