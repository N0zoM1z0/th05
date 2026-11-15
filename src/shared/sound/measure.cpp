// The current BGM measure (ReC98 th05/snd/delaymea.cpp, th02/snd/measure.hpp).
#pragma option -zCSHARED
#include <dos.h>
#include "src/shared/abi.hpp"
extern "C" unsigned char snd_bgm_mode;

int far snd_bgm_measure(void)
{
    if(!snd_bgm_mode) {
        return -1;
    }
    _AH = 0x05; // KAJA_GET_SONG_MEASURE
    if(snd_bgm_mode != 3) {
        geninterrupt(0x60);
    } else {
        _DX = (48 * 4); // MMD ticks per quarter note, original hardcoded4/4.
        geninterrupt(0x61);
    }
    return _AX;
}
