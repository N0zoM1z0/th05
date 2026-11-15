// The Music Room's nopoly_B_put(): copies the saved B plane (a segment) back
// to VRAM. The explicit XOR instructions reproduce the original `31 FF` /
// `31 F6` encodings that __memcpy__ does not; this also needs a direct
// `tcc -c` compile, since TASM picks the other encoding.
#pragma option -zCNP_B_TEXT -zPop_01
#include <dos.h>
#include <mem.h>
extern unsigned int nopoly_B;
#pragma codeseg NP_B_TEXT op_01
void near nopoly_B_put(void)
{
    asm { push ds }
    _ES = 0xA800; // B plane
    _AX = nopoly_B;
    _DS = _AX;
    asm { xor di, di }
    asm { xor si, si }
    _CX = 32000 / 2; // PLANE_SIZE in words
    asm { rep movsw }
    asm { pop ds }
}
