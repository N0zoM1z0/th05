// Natural TH05 sound-effect controller from ReC98 th02/snd/se.cpp,
// b6ba5b0a529edbb31efdf8c0e939263804f8ee47. Ordinary parameter and table
// access stay C++; only the real PMD/Beep driver protocol uses registers.
#pragma option -zCSHARED -k-
#include <dos.h>
#include "src/shared/sound/se.hpp"

inline void se_driver_play(void)
{
    // PMD consumes AH=function and AL=effect; Beep consumes the same selected
    // effect zero-extended to the real Pascal word parameter.
    _AL = snd_se_playing;
    if(snd_se_mode != SND_SE_BEEP) {
        _AH = PMD_SE_PLAY;
        geninterrupt(SE_PMD_INTERRUPT);
    } else {
        _AH ^= _AH;
        bgm_sound(_AX);
    }
}

extern "C" void pascal far snd_se_play(int new_se)
{
    register int se = new_se;
    if(snd_se_mode == SND_SE_OFF) {
        return;
    }
    if(snd_se_playing == SE_NONE) {
        snd_se_playing = se;
    } else if(snd_se_priorities[snd_se_playing] <= snd_se_priorities[se]) {
        snd_se_playing = se;
        snd_se_frame = 0;
    }
}

// No codestring/NOP injection or manual alignment bytes between functions.
extern "C" void far snd_se_update(void)
{
    if((snd_se_mode == SND_SE_OFF) || (snd_se_playing == SE_NONE)) {
        return;
    }
    if(snd_se_frame == 0) {
        se_driver_play();
    }
    snd_se_frame++;
    if(snd_se_priority_frames[snd_se_playing] < snd_se_frame) {
        snd_se_frame = 0;
        snd_se_playing = SE_NONE;
    }
}
