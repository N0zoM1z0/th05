// Original MAIN automatic enemy-item drop selector, one mutable byte.
#pragma option -zCMAIN_ITEM_DROP_CYCLE_DATA_TEXT -zPmain_01
#include "src/shared/abi.hpp"

unsigned char item_drop_cycle = 0;
typedef char item_drop_cycle_is_byte[(sizeof(item_drop_cycle) == 1) ? 1 : -1];
