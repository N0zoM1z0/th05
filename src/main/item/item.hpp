// Full TH05 item ABI. Semantic donor: maintained TH04 src/main/item/item.hpp.
// Layout corroboration: ReC98 b6ba5b0a th04/main/item/item.hpp and items[bss].asm;
// actual TH05 pool count, operands and caller frames reviewed independently.
#ifndef TH05_MAIN_ITEM_ITEM_HPP
#define TH05_MAIN_ITEM_ITEM_HPP
#include "src/main/bullet/update.hpp"

static const int ITEM_COUNT = 40;
static const int ITEM_W = 16;
static const int ITEM_H = 16;
static const int ITEM_PULL_SPEED = 10;
static const int ITEM_MISS_COUNT = 5;
enum item_miss_field_t {
    MISS_FIELD_LEFT = 0, MISS_FIELD_CENTER = 1, MISS_FIELD_RIGHT = 2,
    MISS_FIELD_COUNT = 3
};
struct item_t {
    entity_flag_t flag;
    char unused;
    PlayfieldMotion pos;
    unsigned char type;
    char unknown;
    int patnum;
    // Genuine word boolean, unlike the game's one-byte bool fields.
    int pulled_to_player;
};
extern item_t items[ITEM_COUNT];
extern const int ITEM_PATNUM[IT_COUNT];
extern const unsigned char ENEMY_DROPS[64];
// Original table is field/axis/slot, with Y first and X second.
extern const Subpixel ITEM_MISS_VELOCITIES[MISS_FIELD_COUNT][2][ITEM_MISS_COUNT];
extern unsigned char item_drop_cycle;
extern bool items_pull_to_player;
extern unsigned int items_spawned;
extern unsigned char lives;

typedef char item_is_20[(sizeof(item_t) == 20) ? 1 : -1];
typedef char item_flag_at_0[(offsetof(item_t, flag) == 0) ? 1 : -1];
typedef char item_unused_at_1[(offsetof(item_t, unused) == 1) ? 1 : -1];
typedef char item_motion_at_2[(offsetof(item_t, pos) == 2) ? 1 : -1];
typedef char item_type_at_14[(offsetof(item_t, type) == 14) ? 1 : -1];
typedef char item_unknown_at_15[(offsetof(item_t, unknown) == 15) ? 1 : -1];
typedef char item_patnum_at_16[(offsetof(item_t, patnum) == 16) ? 1 : -1];
typedef char item_pull_at_18[(offsetof(item_t, pulled_to_player) == 18) ? 1 : -1];
typedef char item_pull_is_word[(sizeof(((item_t *)0)->pulled_to_player) == 2) ? 1 : -1];
typedef char item_pool_is_800[(sizeof(items) == 800) ? 1 : -1];
typedef char item_miss_velocity_table_is_60[(sizeof(ITEM_MISS_VELOCITIES) == 60) ? 1 : -1];
#endif
