// Enemy statistics for the whole game: enemies that left the playfield or
// were killed, and enemies killed. Saved to the resident structure when MAIN
// hands over to another binary.
#pragma option -zCENEMY_LIFETIME_TOTALS_DATA_TEXT -zPmain_01
#include "src/shared/abi.hpp"

unsigned int enemies_gone = 0;
unsigned int enemies_killed = 0;

typedef char enemies_gone_is_word[(sizeof(enemies_gone) == 2) ? 1 : -1];
typedef char enemies_killed_is_word[(sizeof(enemies_killed) == 2) ? 1 : -1];
