// Input sensing that waits for the PC-98 keyboard to settle.
#pragma option -zCSHARED -k-
#include "src/shared/hardware/input_held.hpp"
#pragma codeseg SHARED

#define HELD_INPUT_DELAY_LOOPS 1024

int far input_reset_sense_held(void)
{
    input_reset_sense();
    // Port 5Fh supplies the original fixed I/O delay between input samples.
    // Exact OUT/LOOP timing is a hardware boundary, independent of C++ loops.
    asm {
        mov cx, HELD_INPUT_DELAY_LOOPS
    input_settle:
        out 5Fh, al
        loop input_settle
    }
    return input_sense();
}
