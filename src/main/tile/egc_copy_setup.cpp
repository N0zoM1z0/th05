// egc_start_copy_noframe(): turns on the EGC and sets it up for VRAM-to-VRAM
// copies through its latch (ReC98 th01/hardware/egc_impl.hpp, egc_on() +
// egc_setup_copy()). The tile renderers call it before copying tiles.
#pragma option -zCEGC_SETUP_TEXT -zPmain_01 -k-
#include <dos.h>
#pragma codeseg EGC_SETUP_TEXT main_01

// EGC word registers
#define EGC_ACTIVEPLANEREG 0x04a0
#define EGC_READPLANEREG 0x04a2
#define EGC_MODE_ROP_REG 0x04a4
#define EGC_MASKREG 0x04a8
#define EGC_ADDRRESSREG 0x04ac
#define EGC_BITLENGTHREG 0x04ae

// EGC_COMPAREREAD | EGC_WS_PATREG | EGC_RL_MEMREAD
#define EGC_MODE_COPY 0x3100

void near egc_start_copy_noframe(void)
{
    // egc_on(): GRCG off, allow a graphics mode change (port 6Ah = 07h),
    // select EGC mode (05h), GRCG on in TDW mode (80h), lock the mode (06h).
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

    // egc_setup_copy()
    _AX = 0xfff0;
    _DX = EGC_ACTIVEPLANEREG;
    asm { out dx, ax }
    _AX = 0x00ff;
    _DX = EGC_READPLANEREG;
    asm { out dx, ax }
    _AX = EGC_MODE_COPY;
    _DX = EGC_MODE_ROP_REG;
    asm { out dx, ax }
    _AX = 0xffff;
    _DX = EGC_MASKREG;
    asm { out dx, ax }
    // The original uses MOV AX,0 here; `_AX = 0` would compile to XOR AX,AX.
    asm { mov ax, 0 }
    _DX = EGC_ADDRRESSREG;
    asm { out dx, ax }
    _AX = 0x000f;   // bit length - 1: 16 bits
    _DX = EGC_BITLENGTHREG;
    asm { out dx, ax }
}
