// Set by items_update() while items are pulled to the player. ZUN bloat: TH04
// doubles new point numbers while it is set; in TH05 nothing reads it.
// ReC98: th04/main/pointnum/pointnum[data].asm, followed by an alignment byte.
#pragma option -zCPOINTNUM_TWICE_INIT_TEXT -zPmain_01
#include "src/main/hud/resident.hpp"

bool pointnum_times_2 = false;
typedef char pointnum_double_abi_is_one_byte[(sizeof(pointnum_times_2) == 1) ? 1 : -1];
