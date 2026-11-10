// Complete real two-function TH05 held-key settle and UI wait source.
// Preserved ReC98 th05/hardware/inp_h_w.cpp C++/register semantics.
#pragma option -zCSHARED -k-
#include <dos.h>
#include "src/shared/abi.hpp"
#include "src/shared/hardware/input_held.hpp"
#pragma codeseg SHARED
extern "C" volatile unsigned int vsync_Count1;
int far input_reset_sense_held(void)
{
    asm { push cs; call near ptr input_reset_sense; }
    _CX = 1024;
input_settle:
    asm {
        out 5Fh, al
        loop input_settle
    }
    asm { push cs; call near ptr input_sense; }
    return _AX;
}
#pragma option -k.
int pascal far input_wait_for_change(int frames)
{
#define time _BP
    while(input_reset_sense_held()) {}
    time = frames;
    do {
        if(input_reset_sense_held()) {
            return _AX;
        }
        _AX = vsync_Count1;
        while(_AX == vsync_Count1) {}
        if(time) {
            time--;
            if(_FLAGS & 0x40) {
                break;
            }
        }
    } while(1);
    return _AX;
#undef time
}
