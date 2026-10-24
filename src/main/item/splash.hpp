// Full spawn-splash record and genuine main_03 calls; ReC98 b6ba5b0a
// th04/main/item/splash.hpp and maintained TH04 splash owner provenance.
#ifndef TH05_MAIN_ITEM_SPLASH_HPP
#define TH05_MAIN_ITEM_SPLASH_HPP
#include "src/main/item/item.hpp"

static const int ITEM_SPLASH_COUNT = 8;
static const int ITEM_SPLASH_DOTS = 32;
static const int ITEM_SPLASH_RADIUS_START = 2;
static const int ITEM_SPLASH_RADIUS_DELTA = 2;
static const int ITEM_SPLASH_RADIUS_END = 32;
struct item_splash_t {
    entity_flag_t flag;
    char time;
    SPPoint center;
    Subpixel radius_cur;
    Subpixel radius_prev;
};
extern item_splash_t item_splashes[ITEM_SPLASH_COUNT];
extern unsigned char item_splash_last_id;

#pragma codeseg ITEM_SPLASH_TEXT main_03
void pascal near item_splashes_add(Subpixel center_x, Subpixel center_y);
void near item_splashes_update(void);
#pragma codeseg

typedef char item_splash_is_10[(sizeof(item_splash_t) == 10) ? 1 : -1];
typedef char item_splash_time_at_1[(offsetof(item_splash_t, time) == 1) ? 1 : -1];
typedef char item_splash_center_at_2[(offsetof(item_splash_t, center) == 2) ? 1 : -1];
typedef char item_splash_current_at_6[(offsetof(item_splash_t, radius_cur) == 6) ? 1 : -1];
typedef char item_splash_previous_at_8[(offsetof(item_splash_t, radius_prev) == 8) ? 1 : -1];
typedef char item_splash_pool_is_80[(sizeof(item_splashes) == 80) ? 1 : -1];
#endif
