// Natural TH05 C++ adapted from nmlgc/ReC98
// b6ba5b0a529edbb31efdf8c0e939263804f8ee47: th02/snd/kajaint.cpp.
#pragma option -zCSHARED -k-
#include <dos.h>

extern "C" {
extern unsigned char snd_bgm_mode;

int far pascal snd_kaja_interrupt(int ax)
{
    // Preserve the caller's current AX when background music is disabled.
    if (!snd_bgm_mode) {
        return _AX;
    }
    // The real far Pascal word argument is at SS:SP+4 without a BP frame.
    _BX = _SP;
    _AX = peek(_SS, (_BX + 4));
    if (snd_bgm_mode != 3) {
        geninterrupt(0x60);
    } else {
        geninterrupt(0x61);
    }
    return _AX;
}
}
