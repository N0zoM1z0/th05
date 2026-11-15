// Sound effects: priority arbitration and per-frame playback (ReC98
// th02/snd/se.cpp). Register reads mirror ZUN's pseudo-register code.
#pragma option -zCSHARED -k-
#include <dos.h>
#include "src/shared/sound/se.hpp"

#include "src/shared/sound/se_driver_play.inl"
#include "src/shared/sound/se_play_body.inl"
#include "src/shared/sound/se_update_body.inl"
