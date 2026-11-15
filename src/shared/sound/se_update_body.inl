// snd_se_update(): starts a new effect and releases it after its frame count.
extern "C" void far snd_se_update(void)
{
    if((snd_se_mode == SND_SE_OFF) || (snd_se_playing == SE_NONE)) {
        return;
    }
    if(snd_se_frame == 0) {
        se_driver_play();
    }
    snd_se_frame++;
    _BL = snd_se_playing;
    _BH ^= _BH;
    if(snd_se_priority_frames[_BX] < snd_se_frame) {
        snd_se_frame = 0;
        snd_se_playing = SE_NONE;
    }
}
