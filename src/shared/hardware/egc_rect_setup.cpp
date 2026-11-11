// PC-98 rectangle-copy EGC setup: BDA/GRCG mode and the hardware word ports.
#pragma option -zCSHARED -k-
#include <dos.h>
#pragma codeseg SHARED
void near egc_rect_setup(void)
{
    asm {
        push es
        push 0
        pop es
        pushf
        cli
        mov al, 080h
        out 07Ch, al
        mov byte ptr es:[0495h], al
        popf
        pop es
    }
    _AL = 7;
    asm { out 06Ah, al }
    _AL = 5;
    asm { out 06Ah, al }
    _AL = 6;
    asm { out 06Ah, al }
    _DX = 0x04A0;
    _AX = 0xFFF0;
    asm { out dx, ax }
    _DX = 0x04A2;
    _AX = 0x00FF;
    asm { out dx, ax }
    _DX = 0x04A8;
    _AX = 0xFFFF;
    asm { out dx, ax }
    _DX = 0x04AC;
    asm { sub ax, ax; out dx, ax }
    _DX = 0x04AE;
    _AX = 0x000F;
    asm { out dx, ax }
}
