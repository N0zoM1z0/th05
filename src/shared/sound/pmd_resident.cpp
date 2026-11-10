// PMD detection also resets the shared sound-mode selection state.
#pragma option -zCSHARED -k-
#include <dos.h>
#include "src/shared/sound/resident.hpp"

extern "C" int far snd_pmd_resident(void)
{
    // The original PMD test uses AX both as the zero state shared with ES
    // and as the returned result. This is a real DOS register contract.
    _AX = 0;
    snd_interrupt_if_midi = 0x60;
    snd_midi_possible = _AX;
    snd_bgm_mode = _AX;
    snd_se_mode = _AX;
    _ES = _AX;
    if(KAJA_ISR_MAGIC(0x60, 'P', 'M', 'D')) {
        ++_AX;
    }
    return _AX;
}
