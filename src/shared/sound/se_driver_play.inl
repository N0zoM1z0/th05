// Shared genuine PMD/Beep hardware interface used by the SE updater.
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

