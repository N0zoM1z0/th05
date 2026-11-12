// Original MAIN single-byte Boss collision arbitration state.
// Zero outside hit tests; the Boss and midboss gates toggle it around calls.
#pragma option -zCMAIN_SHOT_BOSS_FLAG_DATA_TEXT -zPmain_01
#include "src/main/hud/resident.hpp"

bool shots_hittest_against_boss = false;
typedef char original_shot_boss_flag_is_byte[(sizeof(shots_hittest_against_boss) == 1) ? 1 : -1];
