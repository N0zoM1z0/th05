// Natural TH05 sound-effect controller from ReC98 th02/snd/se.cpp,
// b6ba5b0a529edbb31efdf8c0e939263804f8ee47. The real 16-bit Pascal
// argument and priority-table register protocols coexist with C++ state logic.
#pragma option -zCSHARED -k-
#include <dos.h>
#include "src/shared/sound/se.hpp"

#include "src/shared/sound/se_driver_play.inl"
#include "src/shared/sound/se_play_body.inl"
#include "src/shared/sound/se_update_body.inl"
