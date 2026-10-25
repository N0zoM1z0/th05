// Natural complete measure/wait family in the observed ungrouped SHARED.
#pragma option -zCSHARED
#include "src/shared/sound/measure.cpp"
void pascal far frame_delay(int frames);

void pascal far snd_delay_until_measure(int measure, unsigned int frames_if_no_bgm)
{
    int measure_cur;
    do {
        measure_cur = snd_bgm_measure();
        if(measure_cur < 0) {
            frame_delay(frames_if_no_bgm);
            return;
        }
    } while(measure_cur < measure);
}
