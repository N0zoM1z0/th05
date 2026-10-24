// TH05 item reward/update interfaces. Natural TH04 algorithm donor plus
// independent supplied-TH05 behavior review; ReC98 b6ba5b0a corroborates names.
#ifndef TH05_MAIN_ITEM_UPDATE_HPP
#define TH05_MAIN_ITEM_UPDATE_HPP
#include "src/main/item/item.hpp"
#include "src/main/item/splash.hpp"

static const unsigned char ITEM_POWER_MAX = 128;
static const int ITEM_POWER_OVERFLOW_MAX = 42;
static const unsigned char ITEM_EXTEND_LIVES_MAX = 99;
static const int ITEM_EXTEND_POINT_INTERVAL = 100;

extern unsigned char extends_gained;
extern unsigned int extend_point_items_collected;
extern unsigned char power;
extern int power_overflow;
extern int POWER_OVERFLOW_BONUS[ITEM_POWER_OVERFLOW_MAX + 1];
extern unsigned char dream;
extern unsigned int item_point_score_at_full_dream;
extern unsigned char item_playperf_raise;
extern unsigned int items_collected;
extern unsigned int total_point_items_collected;
extern unsigned int total_max_valued_point_items_collected;
// Actual TH05 standalone byte at DS36F5, immediately preceding dream.
extern unsigned char stage_point_items_collected;
extern signed char bombs;
extern unsigned char miss_time;
extern bool pointnum_times_2;

#pragma codeseg ITEM_UPDATE_MAIN01 main_01
extern "C" {
    void pascal far playperf_raise(char delta);
    void pascal far playperf_lower(char delta);
    void pascal far hud_point_items_put(void);
    void pascal far hud_dream_put(void);
    void pascal far shot_level_update(void);
}
void far hud_lives_put(void);
void far hud_bombs_put(void);
#pragma codeseg ITEM_EXTEND_TEXT main_03
void near item_extend_check(void);
#pragma codeseg ITEM_REWARD_TEXT main_03
void pascal near item_collect(item_t near *item);
void pascal near item_miss_penalty(item_t near *item);
#pragma codeseg ITEM_UPDATE_TEXT main_03
extern "C" void pascal far items_update(void);
void pascal near pointnums_add_yellow(subpixel_t x, subpixel_t y, unsigned int points);
#pragma codeseg
extern "C" void pascal far snd_se_play(int effect);

// Ordinary state transitions; no emitted calls, barriers or register templates.
#define ITEM_CLEAR_BULLETS() { \
    if(bullet_clear_time < 20) { bullet_clear_time = 20; } \
}
#define ITEM_SHOW_POPUP(popup_value) { \
    overlay_popup_id_new = popup_value; \
    overlay2 = overlay_popup_update_and_render; \
}

typedef char item_point_counter_is_byte[(sizeof(stage_point_items_collected) == 1) ? 1 : -1];
typedef char item_overflow_is_word[(sizeof(power_overflow) == 2) ? 1 : -1];
typedef char item_overflow_table_is_86[(sizeof(POWER_OVERFLOW_BONUS) == 86) ? 1 : -1];
#endif
