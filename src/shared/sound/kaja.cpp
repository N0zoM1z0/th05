// Calls into the PMD/MMD music driver interrupt (ReC98 th02/snd/kajaint.cpp).
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
    // No BP frame: the Pascal word argument is read at SS:SP+4.
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
