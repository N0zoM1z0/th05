// Original Music Room VRAM B-plane restore: typed hardware pointer and memcpy.
#pragma option -zCNP_B_TEXT -zPop_01
#include <dos.h>
#include <mem.h>
extern unsigned int nopoly_B;
#pragma codeseg NP_B_TEXT op_01
void near nopoly_B_put(void)
{
    asm { push ds }
    _ES = 0xA800;
    _AX = nopoly_B;
    _DS = _AX;
    asm { xor di, di }
    asm { xor si, si }
    _CX = 32000 / 2;
    asm { rep movsw }
    asm { pop ds }
}
