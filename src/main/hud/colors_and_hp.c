/* Main HUD palette selectors, empty HP strip and two editable Japanese captions. */
#pragma option -zCHUD_COLORS_TEXT -zPmain_01
#ifdef __cplusplus
#error Semantic HUD DATA requires a C producer
#endif
#include "src/main/hud/overlay_data.h"

enum HudTramColor {
    HC_BLUE = 0x21, HC_RED = 0x41, HC_MAGENTA = 0x61,
    HC_GREEN = 0x81, HC_CYAN = 0xA1, HC_YELLOW = 0xC1,
    HC_WHITE = 0xE1
};

/* The leading zero is separately observed in the original HUD DATA source,
 * but its purpose is unknown. It gets no authored semantic-byte credit. */
typedef struct HudBarResources {
    unsigned char unidentified_zero;
    unsigned char dream_colors[9];
    unsigned char power_colors[10];
    unsigned char hp_empty[9];
    unsigned char hp_colors[5];
    char hp_caption[11];
    char hp_caption_copy[11];
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
typedef char hud_bar_captions[(offsetof(HudBarResources, hp_caption) == 34) ? 1 : -1];
typedef char hud_bar_second_caption[(offsetof(HudBarResources, hp_caption_copy) == 45) ? 1 : -1];
