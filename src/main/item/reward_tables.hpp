// Semantic initialized item tables; canonical item/state declarations stay shared.
#ifndef TH05_ITEM_REWARD_TABLES_HPP
#define TH05_ITEM_REWARD_TABLES_HPP
#include "src/main/item/update.hpp"

// th05/sprites/main_pat.h: the seven item sprites start the miko16 bank.
static const int ITEM_SPRITE_FIRST = 36;
static const int DREAM_SCORE_ITEM_COUNTS = 8;
// Legacy Dream-item reward schedule, in units of ten points. TH05 retains
// the complete table even though its revised collection code does not use it.
extern const unsigned int DREAM_SCORE_PER_ITEMS[DREAM_SCORE_ITEM_COUNTS];

typedef char item_sprite_table_is_14[(sizeof(ITEM_PATNUM) == 14) ? 1 : -1];
typedef char item_dream_table_is_16[(sizeof(DREAM_SCORE_PER_ITEMS) == 16) ? 1 : -1];
typedef char item_reward_tables_are_116[(sizeof(ITEM_PATNUM) +
    sizeof(POWER_OVERFLOW_BONUS) + sizeof(DREAM_SCORE_PER_ITEMS) == 116) ? 1 : -1];
#endif
