// Complete TH05 point-popup records; pool/list storage belongs to foreign BSS.
#ifndef TH05_POINTNUM_LIFECYCLE_HPP
#define TH05_POINTNUM_LIFECYCLE_HPP
#include "src/main/player/reimu.hpp"
#include "src/main/hud/overlay.hpp"

// Same complete record as stage_state_init.hpp, without its unrelated pools.
struct pointnum_t {
    char flag;
    unsigned char age;
    SPPoint center_cur;
    Subpixel center_prev_y;
    unsigned int width;
    unsigned char digits_lebcd[5];
    signed char padding;
};
static const unsigned int POINTNUM_WHITE_COUNT = 200;
static const unsigned int POINTNUM_YELLOW_COUNT = 80;
static const unsigned int POINTNUM_COUNT = POINTNUM_WHITE_COUNT + POINTNUM_YELLOW_COUNT;
static const pixel_t POINTNUM_H = 8;
static const unsigned char POINTNUM_RISE_AGE = 24;
static const unsigned char POINTNUM_LAST_AGE = 36;
extern unsigned char pointnum_white_p;
extern unsigned char pointnum_yellow_p;
extern pointnum_t pointnums[POINTNUM_COUNT];
extern pointnum_t near *pointnums_alive[POINTNUM_COUNT + 1];
extern pointnum_t near *pointnum_first_yellow_alive;

#pragma codeseg POINTNUM_LIFE_TEXT main_01
extern "C" void near pointnums_init(void);
void near pointnums_invalidate(void);
extern "C" void near pointnums_update(void);

typedef char pointnum_record_is_16[(sizeof(pointnum_t) == 16) ? 1 : -1];
typedef char pointnum_current_at_2[(offsetof(pointnum_t, center_cur) == 2) ? 1 : -1];
typedef char pointnum_previous_at_6[(offsetof(pointnum_t, center_prev_y) == 6) ? 1 : -1];
typedef char pointnum_width_at_8[(offsetof(pointnum_t, width) == 8) ? 1 : -1];
typedef char pointnum_digits_at_10[(offsetof(pointnum_t, digits_lebcd) == 10) ? 1 : -1];
typedef char pointnum_padding_at_15[(offsetof(pointnum_t, padding) == 15) ? 1 : -1];
typedef char pointnum_pool_is_4480[(sizeof(pointnums) == 4480) ? 1 : -1];
typedef char pointnum_alive_is_562[(sizeof(pointnums_alive) == 562) ? 1 : -1];
typedef char pointnum_first_is_near[(sizeof(pointnum_first_yellow_alive) == 2) ? 1 : -1];
#endif
