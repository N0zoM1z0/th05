/* HUD bar colors, the blank HP bar, and the "x" strings for life and bomb
 * counts above five. */
#pragma option -zCHUD_COLORS_TEXT -zPmain_01
#ifdef __cplusplus
#error This file must be compiled as C
#endif
#include "src/main/hud/overlay_data.h"

enum HudTramColor {
    HC_BLUE = 0x21, HC_RED = 0x41, HC_MAGENTA = 0x61,
    HC_GREEN = 0x81, HC_CYAN = 0xA1, HC_YELLOW = 0xC1,
    HC_WHITE = 0xE1
};

/* The two "x" strings are identical and must not be const: Borland would then
 * merge them into one. The leading zero byte has no known use, but it keeps
 * the following data at its original even address. */
typedef struct HudBarResources {
    unsigned char unidentified_zero;
    unsigned char dream_colors[9];
    unsigned char power_colors[10];
    unsigned char hp_empty[9];
    unsigned char hp_colors[5];
    char lives_extra[11];
    char bombs_extra[11];
} HudBarResources;

HudBarResources near hud_bar_resources = {
    0,
    { HC_RED, HC_RED, HC_MAGENTA, HC_MAGENTA, HC_BLUE,
      HC_GREEN, HC_CYAN, HC_YELLOW, HC_WHITE },
    { HC_RED, HC_RED, HC_RED, HC_MAGENTA, HC_MAGENTA,
      HC_BLUE, HC_GREEN, HC_CYAN, HC_YELLOW, HC_WHITE },
    { HG_EMPTY, HG_EMPTY, HG_EMPTY, HG_EMPTY, HG_EMPTY,
      HG_EMPTY, HG_EMPTY, HG_EMPTY, HG_NULL },
    { HC_RED, HC_MAGENTA, HC_CYAN, HC_YELLOW, HC_WHITE },
    "　　×　　",
    "　　×　　"
};

typedef char hud_bar_size[(sizeof(HudBarResources) == 56) ? 1 : -1];
typedef char hud_bar_dream[(offsetof(HudBarResources, dream_colors) == 1) ? 1 : -1];
typedef char hud_bar_power[(offsetof(HudBarResources, power_colors) == 10) ? 1 : -1];
typedef char hud_bar_empty[(offsetof(HudBarResources, hp_empty) == 20) ? 1 : -1];
typedef char hud_bar_hp_colors[(offsetof(HudBarResources, hp_colors) == 29) ? 1 : -1];
typedef char hud_bar_lives_extra[(offsetof(HudBarResources, lives_extra) == 34) ? 1 : -1];
typedef char hud_bar_bombs_extra[(offsetof(HudBarResources, bombs_extra) == 45) ? 1 : -1];
