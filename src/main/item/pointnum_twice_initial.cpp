// Original game point-number doubling flag, before its separate EVEN byte.
// Pinned ReC98 th04/main/pointnum/pointnum[data].asm: db 0; evendata.
#pragma option -zCPOINTNUM_TWICE_INIT_TEXT -zPmain_01
#include "src/main/hud/resident.hpp"

bool pointnum_times_2 = false;
typedef char pointnum_double_abi_is_one_byte[(sizeof(pointnum_times_2) == 1) ? 1 : -1];
