// Semantic table definitions, not an encoded asset or target-byte image.
// Candidate provenance: ReC98 b6ba5b0a th04/main/item/items[data].asm,
// th02/main/power_overflow[data].asm and th05/sprites/main_pat.h. The actual
// supplied TH05 DATA boundaries/values are reviewed independently in the notes.
#pragma option -zCITEM_REWARD_TABLE_CONTEXT -zPmain_03
#include "src/main/item/reward_tables.hpp"

const int ITEM_PATNUM[IT_COUNT] = {
    ITEM_SPRITE_FIRST + IT_POWER,
    ITEM_SPRITE_FIRST + IT_POINT,
    ITEM_SPRITE_FIRST + IT_DREAM,
    ITEM_SPRITE_FIRST + IT_BIGPOWER,
    ITEM_SPRITE_FIRST + IT_BOMB,
    ITEM_SPRITE_FIRST + IT_1UP,
    ITEM_SPRITE_FIRST + IT_FULLPOWER
};

// Index0 also supplies the ordinary reward before reaching full power.
// Further full-power pickups advance the index, saturating at42.
int POWER_OVERFLOW_BONUS[ITEM_POWER_OVERFLOW_MAX + 1] = {
    1,
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
    20, 30, 40, 50, 60, 70, 80, 90, 100,
    150, 200, 250, 300, 350, 400, 450, 500,
    550, 600, 650, 700, 750, 800, 850, 900, 950,
    1000, 1050, 1100, 1200, 1250, 1280
};

const unsigned int DREAM_SCORE_PER_ITEMS[DREAM_SCORE_ITEM_COUNTS] = {
    0, 100, 200, 400, 600, 800, 1000, 1280
};
