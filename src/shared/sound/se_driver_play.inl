// Starts the current effect on PMD or the beeper; used by snd_se_update().
inline void se_driver_play(void)
{
    // PMD takes AH = function, AL = effect; the beeper takes the effect as a
    // zero-extended Pascal word.
    _AL = snd_se_playing;
    if(snd_se_mode != SND_SE_BEEP) {
        _AH = PMD_SE_PLAY;
        geninterrupt(SE_PMD_INTERRUPT);
    } else {
        _AH ^= _AH;
        bgm_sound(_AX);
    }
}

