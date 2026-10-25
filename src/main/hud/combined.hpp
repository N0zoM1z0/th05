// Genuine whole HUD source context. Frozen owner headers are not included:
// their first declarations select separate producer segments. These complete
// declarations retain the same canonical types and real calling conventions.
#ifndef TH05_HUD_COMBINED_HPP
#define TH05_HUD_COMBINED_HPP
#include "src/main/hud/resident.hpp"

struct hud_dream_colors_t { unsigned char v[9]; };
struct hud_power_colors_t { unsigned char v[10]; };
struct hud_bar9_t { unsigned char v[9]; };
struct hud_colors5_t { unsigned char v[5]; };
typedef void (near pascal *near HudIndicatorOverlay)(void);

extern score_lebcd_t score;
extern unsigned long score_delta;
extern unsigned long score_delta_frame;
extern unsigned char hiscore_popup_shown;
extern unsigned char lives;
extern signed char bombs;
extern const char hud_lives_extra[11];
extern const char hud_bombs_extra[11];
extern const hud_dream_colors_t HUD_DREAM_COLORS;
extern const hud_power_colors_t HUD_POWER_COLORS;
extern unsigned char dream_prev;
extern unsigned char dream;
extern unsigned char power;
extern unsigned char shot_level;
extern unsigned char stage_point_items_collected;
extern unsigned int extend_point_items_collected;
extern unsigned int stage_graze;
extern unsigned char bullet_clear_time;
extern unsigned char overlay_popup_id_new;
extern HudIndicatorOverlay overlay2;
extern const hud_bar9_t gHUD_HP_BLANK;
extern const hud_colors5_t HUD_HP_COLORS;
extern unsigned char playchar;
extern unsigned char rank;

extern const unsigned char glEASY[40];
extern const unsigned char gsSCORE[5];
extern const unsigned char gsHISCORE[5];
extern const unsigned char gsREIGEKI[5];
extern const unsigned char gsREIMU[5];
extern const unsigned char gsREIRYOKU[5];
extern const unsigned char gsBOMB[5];
extern const unsigned char gsPLAYER[5];
extern const unsigned char gsPOWER[5];
extern const unsigned char gsENEMY[5];
extern const unsigned char gsRUIKEI[5];

static const unsigned int HUD_RESOURCE_EMPTY = 0x02;
static const unsigned int HUD_RESOURCE_DIGIT_ZERO = 0xA0;
static const unsigned int HUD_RESOURCE_BOMB = 0xD3;
static const unsigned int HUD_RESOURCE_YINYANG = 0xD4;
static const unsigned int HUD_RESOURCE_WHITE = 0xE1;
static const unsigned int HUD_INDICATOR_WHITE = 0xE1;
static const unsigned int HUD_INDICATOR_CYAN = 0xA1;
static const int HUD_INDICATOR_BAR_MAX = 128;
static const unsigned char HUD_INDICATOR_DREAM_MAX_POPUP = 4;
static const unsigned int HUD_HP_DRAW_YELLOW = 0xC1;
static const unsigned int HUD_HP_DRAW_WHITE = 0xE1;

static const int HUD_FULL_REIMU = 0;
static const int HUD_FULL_MARISA = 1;
static const int HUD_FULL_MIMA = 2;
static const int HUD_FULL_YUUKA = 3;
static const unsigned int HUD_FULL_GREEN = 0x81;
static const unsigned int HUD_FULL_CYAN = 0xA1;
static const unsigned int HUD_FULL_YELLOW = 0xC1;
static const unsigned int HUD_FULL_MAGENTA = 0x61;
static const unsigned int HUD_FULL_RED = 0x41;
static const unsigned int HUD_FULL_POINT_GLYPH = 0xE6;
static const unsigned int HUD_FULL_DREAM_GLYPH = 0xE7;
static const unsigned int HUD_FULL_GRAZE_GLYPH = 0xE8;

#pragma codeseg _TEXT
extern "C" {
    void far pascal gaiji_putca(unsigned x, unsigned y,
        unsigned glyph, unsigned attribute);
    void far pascal text_putsa(unsigned x, unsigned y,
        const char far *text, unsigned attribute);
    void pascal far gaiji_putsa(unsigned int x, unsigned int y,
        const char far *text, unsigned int attribute);
}
#pragma codeseg HUD_COMBINED_MAIN03 main_03
void pascal far hud_5_digit_put(unsigned int x, unsigned int y,
    unsigned int value, unsigned int attribute);
#pragma codeseg HUD_COMBINED_AFTER_TEXT main_01
extern "C" void pascal near hud_bar_put(unsigned int y,
    int value, unsigned int attribute);
extern "C" void pascal near hud_score_put(void);
void pascal near overlay_popup_update_and_render(void);

#pragma codeseg HUD_COMBINED_TEXT main_01
void near score_reset(void);
void far hud_lives_put(void);
void far hud_bombs_put(void);
extern "C" {
    void pascal far hud_point_items_put(void);
    void pascal far hud_dream_put(void);
    void pascal far hud_power_put(void);
}
void far hud_graze_put(void);
void pascal far hud_hp_put(int bar_value);
void far hud_put(void);
#pragma codeseg

typedef char hud_combined_resident_is_128[(sizeof(resident_t) == 128) ? 1 : -1];
typedef char hud_combined_score_is_8[(sizeof(score) == 8) ? 1 : -1];
typedef char hud_combined_dream_is_9[(sizeof(hud_dream_colors_t) == 9) ? 1 : -1];
typedef char hud_combined_power_is_10[(sizeof(hud_power_colors_t) == 10) ? 1 : -1];
typedef char hud_combined_blank_is_9[(sizeof(hud_bar9_t) == 9) ? 1 : -1];
typedef char hud_combined_colors_are_5[(sizeof(hud_colors5_t) == 5) ? 1 : -1];
typedef char hud_combined_overlay_is_2[(sizeof(HudIndicatorOverlay) == 2) ? 1 : -1];
#endif
