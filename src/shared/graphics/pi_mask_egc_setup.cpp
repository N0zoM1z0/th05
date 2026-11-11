// .PI masked row EGC setup: native register, port and mask-advance semantics.
#pragma option -zCSHARED -2 -k-
#include <dos.h>
extern "C" void far EGC_ON(void);
extern unsigned int pi_mask_ptr;
extern unsigned int pi_mask_y;
#pragma codeseg SHARED
void near pi_mask_setup_egc_and_advance(void)
{
    EGC_ON();
    _AX = 0xFFF0;
    _DX = 0x04A0;
    asm { out dx, ax }
    _AX = 0x00FF;
    _DX = 0x04A2;
    asm { out dx, ax }
    _AX = 0x3100;
    _DX = 0x04A4;
    asm { out dx, ax }
    asm { mov ax, 0 }
    _DX = 0x04AC;
    asm { out dx, ax }
    _AX = 0x000F;
    _DX = 0x04AE;
    asm { out dx, ax }
    _BX = pi_mask_ptr;
    _AX = pi_mask_y;
    _AX &= 3;
    asm { shl ax, 1 }
    _BX += _AX;
    _AX = *reinterpret_cast<unsigned int near *>(_BX);
    _DX = 0x04A8;
    asm { out dx, ax }
    pi_mask_y++;
}
