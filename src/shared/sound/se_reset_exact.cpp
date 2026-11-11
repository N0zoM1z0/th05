// Reset the current effect and its frame counter in the original shared ABI.
#pragma option -zCSHARED -k-
#include "src/shared/sound/se.hpp"
#pragma codeseg SHARED
void far snd_se_reset(void)
{
    snd_se_frame = 0;
    snd_se_playing = SE_NONE;
}
