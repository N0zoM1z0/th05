// TH05 item progress counters, in their actual native DGROUP order.
// Source semantics: ReC98 th04/main/item/items[data].asm (GAME=5).
#pragma option -zCITEM_STATE_DATA_TEXT -zPmain_01
#include "src/main/hud/resident.hpp"

int power_overflow = 0;
unsigned int items_spawned = 0;
unsigned int items_collected = 0;
unsigned int extend_point_items_collected = 0;
unsigned int total_point_items_collected = 0;
unsigned int total_max_valued_point_items_collected = 0;
bool items_pull_to_player = false;

typedef char item_overflow_state_is_word[(sizeof(power_overflow) == 2) ? 1 : -1];
typedef char item_spawned_state_is_word[(sizeof(items_spawned) == 2) ? 1 : -1];
typedef char item_collected_state_is_word[(sizeof(items_collected) == 2) ? 1 : -1];
typedef char item_extend_state_is_word[(sizeof(extend_point_items_collected) == 2) ? 1 : -1];
typedef char item_point_state_is_word[(sizeof(total_point_items_collected) == 2) ? 1 : -1];
typedef char item_max_point_state_is_word[(sizeof(total_max_valued_point_items_collected) == 2) ? 1 : -1];
typedef char item_pull_state_is_byte[(sizeof(items_pull_to_player) == 1) ? 1 : -1];
