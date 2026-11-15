/* Miss and bomb totals at the end of the previous stage, compared against
 * the current totals for the No Miss and No Bomb bonuses. */
#pragma option -zCSTAGE_PREVIOUS_COUNTS_TEXT -zPmain_01
#ifdef __cplusplus
#error This file must be compiled as C
#endif

#include "src/main/stage/bonus_previous_resources.h"

unsigned char near bonus_previous_miss_count = 0;
unsigned char near bonus_previous_bomb_count = 0;
typedef char previous_stage_miss_is_byte[(sizeof(bonus_previous_miss_count) == 1) ? 1 : -1];
typedef char previous_stage_bombs_is_byte[(sizeof(bonus_previous_bomb_count) == 1) ? 1 : -1];
typedef char previous_stage_two_counters_are_two[
    (sizeof(bonus_previous_miss_count) + sizeof(bonus_previous_bomb_count) == 2) ? 1 : -1];
