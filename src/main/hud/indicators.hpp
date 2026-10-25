// TH05 point/dream/graze/power indicators; real UI tables remain foreign.
#ifndef TH05_HUD_INDICATORS_HPP
#define TH05_HUD_INDICATORS_HPP
#include "src/shared/abi.hpp"

#if GAME != 5 || BINARY != 'M'
#error This owner implements TH05 MAIN HUD indicators
#endif

struct hud_dream_colors_t { unsigned char v[9]; };
struct hud_power_colors_t { unsigned char v[10]; };
typedef void (near pascal *near HudIndicatorOverlay)(void);
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

static const unsigned int HUD_INDICATOR_WHITE = 0xE1;
static const unsigned int HUD_INDICATOR_CYAN = 0xA1;
static const int HUD_INDICATOR_BAR_MAX = 128;
static const unsigned char HUD_INDICATOR_DREAM_MAX_POPUP = 4;

#pragma codeseg HUD_INDICATOR_MAIN03_TEXT main_03
void pascal far hud_5_digit_put(unsigned int x, unsigned int y,
    unsigned int value, unsigned int attribute);
#pragma codeseg HUD_INDICATOR_AFTER_TEXT main_01
// Genuine near Pascal API: canonical word value, even though the bar uses BL.
extern "C" void pascal near hud_bar_put(unsigned int y,
    int value, unsigned int attribute);
void pascal near overlay_popup_update_and_render(void);
#pragma codeseg HUD_INDICATORS_TEXT main_01
extern "C" {
    void pascal far hud_point_items_put(void);
    void pascal far hud_dream_put(void);
    void pascal far hud_power_put(void);
}
void far hud_graze_put(void);
#pragma codeseg

typedef char hud_dream_colors_are_9[(sizeof(hud_dream_colors_t) == 9) ? 1 : -1];
typedef char hud_power_colors_are_10[(sizeof(hud_power_colors_t) == 10) ? 1 : -1];
typedef char hud_overlay_is_near[(sizeof(HudIndicatorOverlay) == 2) ? 1 : -1];
#endif
