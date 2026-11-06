// MMD resident detection through the real-mode interrupt vector table.
#pragma option -zCSHARED -k-
#include <dos.h>
#include "src/shared/sound/resident.hpp"

extern "C" int far snd_mmd_resident(void)
{
    _ES = 0;
    if(KAJA_ISR_MAGIC(0x61, 'M', 'M', 'D')) {
        snd_interrupt_if_midi = 0x61;
        snd_midi_possible = 1;
        return 1;
    }
    return 0;
}
