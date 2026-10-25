/* Semantic selector strings and state; the gaiji font bitmap remains foreign. */
#pragma option -zCHUD_DATA_TEXT -zPmain_01
#ifdef __cplusplus
#error This initialized semantic DATA producer requires C mode
#endif
#include "src/main/hud/overlay_data.h"

/* Consecutive fragment glyphs form the named popup message in the gaiji font. */
#define HG_FRAG4(first) (first), ((first) + 1), ((first) + 2), ((first) + 3)
#define HG_FRAG5(first) HG_FRAG4(first), ((first) + 4)
#define HG_FRAG8(first) HG_FRAG4(first), HG_FRAG4((first) + 4)
#define HG_FRAG10(first) HG_FRAG8(first), ((first) + 8), ((first) + 9)

HudOverlayData near hud_overlay_data = {
    { 0 },
    0,
    0,
    0,
    { HG_BOLD_S, HG_BOLD_T, HG_BOLD_A, HG_BOLD_G, HG_BOLD_E,
      HG_EMPTY, HG_BOLD_1, HG_NULL },
    { HG_BOLD_F, HG_BOLD_I, HG_BOLD_N, HG_BOLD_A, HG_BOLD_L,
      HG_EMPTY, HG_BOLD_S, HG_BOLD_T, HG_BOLD_A, HG_BOLD_G, HG_BOLD_E, HG_NULL },
    { HG_BOLD_E, HG_BOLD_X, HG_BOLD_T, HG_BOLD_R, HG_BOLD_A,
      HG_EMPTY, HG_BOLD_S, HG_BOLD_T, HG_BOLD_A, HG_BOLD_G, HG_BOLD_E, HG_NULL },
    { HG_FRAG8(HG_HISCORE_ENTRY_FIRST), HG_NULL },
    { HG_FRAG5(HG_EXTEND_FIRST), HG_NULL },
    { HG_FRAG4(HG_BONUS_FIRST), HG_NULL },
    { HG_FRAG8(HG_FULL_POWERUP_FIRST), HG_NULL },
    { HG_FRAG10(HG_DREAMBONUS_MAX_FIRST), HG_NULL },
    {
        &hud_overlay_data.gpHISCORE_ENTRY[0],
        &hud_overlay_data.gpEXTEND[0],
        &hud_overlay_data.gpBONUS[0],
        &hud_overlay_data.gpFULL_POWERUP[0],
        &hud_overlay_data.gpDREAMBONUS_MAX[0]
    },
    0,
    &hud_overlay_data.blank_row[0],
    { HG_BOLD_D, HG_BOLD_E, HG_BOLD_M, HG_BOLD_O, HG_EMPTY,
      HG_BOLD_P, HG_BOLD_L, HG_BOLD_A, HG_BOLD_Y, HG_NULL },
    "                                                "
};

#undef HG_FRAG10
#undef HG_FRAG8
#undef HG_FRAG5
#undef HG_FRAG4
