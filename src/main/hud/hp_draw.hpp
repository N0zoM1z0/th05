// Actual HP bar caption/drawing ABI; the separate HP animator stays unchanged.
#ifndef TH05_HUD_HP_DRAW_HPP
#define TH05_HUD_HP_DRAW_HPP
#include "src/shared/abi.hpp"

struct hud_bar9_t { unsigned char v[9]; };
struct hud_colors5_t { unsigned char v[5]; };
extern const hud_bar9_t gHUD_HP_BLANK;
extern const hud_colors5_t HUD_HP_COLORS;
extern const unsigned char gsENEMY[5];
static const unsigned int HUD_HP_DRAW_YELLOW = 0xC1;
static const unsigned int HUD_HP_DRAW_WHITE = 0xE1;

#pragma codeseg _TEXT
extern "C" void pascal far gaiji_putsa(unsigned int x, unsigned int y,
    const char far *text, unsigned int attribute);
#pragma codeseg HUD_HP_BAR_API_TEXT main_01
// Actual TH05 helper is near Pascal and consumes three complete stack words.
extern "C" void pascal near hud_bar_put(unsigned int y,
    int value, unsigned int attribute);
#pragma codeseg HUD_HP_DRAW_TEXT main_01
void pascal far hud_hp_put(int bar_value);
#pragma codeseg

typedef char hp_blank_is_9[(sizeof(hud_bar9_t) == 9) ? 1 : -1];
typedef char hp_colors_are_5[(sizeof(hud_colors5_t) == 5) ? 1 : -1];
#endif
