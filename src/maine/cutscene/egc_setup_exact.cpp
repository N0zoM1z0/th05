// MAINE cutscene's real EGC interpage copy configuration and port semantics.
#pragma option -zCCUTSCENE_EGC_TEXT -zPgroup_01
#include <dos.h>
#pragma codeseg _TEXT
extern "C" void pascal far egc_on(void);
#pragma codeseg CUTSCENE_EGC_TEXT group_01
static inline void cutscene_egc_write(unsigned int port, unsigned int value) {
    _AX = value;
    _DX = port;
    outport(_DX, _AX);
}
void near egc_start_copy(void)
{
    egc_on();
    cutscene_egc_write(0x04A0, 0xFFF0);
    cutscene_egc_write(0x04A2, 0x00FF);
    cutscene_egc_write(0x04A4, 0x3100);
    cutscene_egc_write(0x04A8, 0xFFFF);
    asm { mov ax, 0 }
    _DX = 0x04AC;
    outport(_DX, _AX);
    cutscene_egc_write(0x04AE, 0x000F);
}
