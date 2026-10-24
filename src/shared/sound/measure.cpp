// Natural GAME5 measure query from ReC98 b6ba5b0a th05/snd/delaymea.cpp
// and th02/snd/measure.hpp. Only the genuine driver register ABI is explicit.
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
