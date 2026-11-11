// PC-98 EGC setup for interpage copy, using Borland's hardware registers.
#pragma option -zCEGC_SETUP_TEXT -zPmain_01 -k-
#include <dos.h>
#pragma codeseg EGC_SETUP_TEXT main_01
void near egc_start_copy_noframe(void)
{
    _AL = 0;
    asm { out 07ch, al }
    _AL = 7;
    asm { out 06ah, al }
    _AL = 5;
    asm { out 06ah, al }
    _AL = 0x80;
    asm { out 07ch, al }
    _AL = 6;
    asm { out 06ah, al }
    _AX = 0xfff0;
    _DX = 0x04a0;
    asm { out dx, ax }
    _AX = 0x00ff;
    _DX = 0x04a2;
    asm { out dx, ax }
    _AX = 0x3100;
    _DX = 0x04a4;
    asm { out dx, ax }
    _AX = 0xffff;
    _DX = 0x04a8;
    asm { out dx, ax }
    asm { mov ax, 0 }
    _DX = 0x04ac;
    asm { out dx, ax }
    _AX = 0x000f;
    _DX = 0x04ae;
    asm { out dx, ax }
}
