// PMD detection also resets the shared sound-mode selection state.
#pragma option -zCSHARED -k-
#include <dos.h>
#include "src/shared/sound/resident.hpp"

extern "C" int far snd_pmd_resident(void)
{
    int found = 0;
    snd_interrupt_if_midi = 0x60;
    snd_midi_possible = found;
    snd_bgm_mode = found;
    snd_se_mode = found;
    _ES = found;
    if(KAJA_ISR_MAGIC(0x60, 'P', 'M', 'D')) {
        found++;
    }
    return found;
}
