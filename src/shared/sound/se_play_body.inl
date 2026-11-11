// Real far Pascal SE priority arbitration, one complete function.
extern "C" void pascal far snd_se_play(int new_se)
{
    // This far Pascal entry receives its single word at SS:[SP+4].  Read
    // through the compiler's real stack-register bindings, not a fake local.
    _BX = _SP;
    _DX = peek(_SS, (_BX + 4));
    if(snd_se_mode == SND_SE_OFF) {
        return;
    }
    if(snd_se_playing == SE_NONE) {
        snd_se_playing = _DL;
        return;
    }
    _BL = snd_se_playing;
    _BH ^= _BH;
    _AL = snd_se_priorities[_BX];
    _BX = _DX;
    if(_AL <= snd_se_priorities[_BX]) {
        snd_se_playing = _DL;
        snd_se_frame = 0;
    }
}

