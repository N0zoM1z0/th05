// Sound arbitration policy, shared by all three TH05 executables.
// Each slot is a sound-effect ID, not an encoded sound or music payload.
#pragma option -zCSE_PRIORITY_DATA_TEXT
#include "src/shared/sound/se.hpp"

// A new effect replaces the current effect when its priority is at least as
// high. The parallel frame limits release the current priority after playback.
unsigned char snd_se_priorities[SE_PRIORITY_COUNT] = {
    0, 0, 32, 16, 2, 18, 18, 64, 16, 17, 2, 18, 32, 32, 32, 32, 0
};
unsigned char snd_se_priority_frames[SE_PRIORITY_COUNT] = {
    0, 0, 36, 16, 4, 16, 8, 48, 80, 17, 4, 11, 80, 80, 80, 32, 0
};
