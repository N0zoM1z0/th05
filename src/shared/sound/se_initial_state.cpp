// Original SE playback state; separate initialized DATA from the policy tables.
// Values and byte types follow the native TH05 sound consumer ABI.
#pragma option -zCSE_PLAYBACK_DATA_TEXT
#include "src/shared/sound/se.hpp"

extern "C" {
unsigned char snd_se_playing = SE_NONE;
unsigned char snd_se_frame = 0;
}

typedef char sound_playing_state_is_byte[(sizeof(snd_se_playing) == 1) ? 1 : -1];
typedef char sound_elapsed_frame_is_byte[(sizeof(snd_se_frame) == 1) ? 1 : -1];
