/* Explicit C model of the complete semantic overlay DATA objects. */
#ifndef TH05_HUD_OVERLAY_DATA_H
#define TH05_HUD_OVERLAY_DATA_H
#include "src/shared/abi.hpp"

/* These are glyph selectors, not pixels. Popup fragments occupy consecutive
 * named slots in the game's gaiji font; bold letters use the canonical order. */
typedef enum HudGaijiSelector {
    HG_NULL = 0,
    HG_EMPTY = 0x02,
    HG_HISCORE_ENTRY_FIRST = 0x40,
    HG_EXTEND_FIRST = 0x48,
    HG_FULL_POWERUP_FIRST = 0x50,
    HG_BONUS_FIRST = 0x58,
    HG_DREAMBONUS_MAX_FIRST = 0x65,
    HG_BOLD_0 = 0xA0,
    HG_BOLD_1, HG_BOLD_2, HG_BOLD_3, HG_BOLD_4,
    HG_BOLD_5, HG_BOLD_6, HG_BOLD_7, HG_BOLD_8, HG_BOLD_9,
    HG_BOLD_A, HG_BOLD_B, HG_BOLD_C, HG_BOLD_D, HG_BOLD_E,
    HG_BOLD_F, HG_BOLD_G, HG_BOLD_H, HG_BOLD_I, HG_BOLD_J,
    HG_BOLD_K, HG_BOLD_L, HG_BOLD_M, HG_BOLD_N, HG_BOLD_O,
    HG_BOLD_P, HG_BOLD_Q, HG_BOLD_R, HG_BOLD_S, HG_BOLD_T,
    HG_BOLD_U, HG_BOLD_V, HG_BOLD_W, HG_BOLD_X, HG_BOLD_Y,
    HG_BOLD_Z,
    HG_NONE = 0xFF
} HudGaijiSelector;

typedef union HudOverlayFade {
    uint8_t in_frame;
    unsigned char out_time;
} HudOverlayFade;

#pragma option -a2
typedef struct HudOverlayData {
    HudOverlayFade overlay_fade;
    unsigned char boss_bgm_frame;
    unsigned char popup_frame;
    uint16_t bb_txt_seg;
    HudGaijiSelector gStage_1[8];
    const HudGaijiSelector gFINAL_STAGE[12];
    const HudGaijiSelector gEXTRA_STAGE[12];
    const HudGaijiSelector gpHISCORE_ENTRY[9];
    const HudGaijiSelector gpEXTEND[6];
    const HudGaijiSelector gpBONUS[5];
    const HudGaijiSelector gpFULL_POWERUP[9];
    const HudGaijiSelector gpDREAMBONUS_MAX[11];
    const HudGaijiSelector far *POPUP_STRINGS[5];
    unsigned char dissolve_sprite;
    const uint8_t far *PLAYFIELD_BLANK_ROW;
    const HudGaijiSelector gDEMO_PLAY[10];
    const uint8_t blank_row[49];
} HudOverlayData;

extern HudOverlayData near hud_overlay_data;
typedef char hod_selector1[(sizeof(HudGaijiSelector) == 1) ? 1 : -1];
typedef char hod_fade1[(sizeof(HudOverlayFade) == 1) ? 1 : -1];
typedef char hod_segment2[(sizeof(uint16_t) == 2) ? 1 : -1];
typedef char hod_popup_far4[(sizeof(hud_overlay_data.POPUP_STRINGS[0]) == 4) ? 1 : -1];
typedef char hod_blank_far4[(sizeof(hud_overlay_data.PLAYFIELD_BLANK_ROW) == 4) ? 1 : -1];
typedef char hod_size164[(sizeof(HudOverlayData) == 164) ? 1 : -1];
typedef char hod_offset00[(offsetof(HudOverlayData, overlay_fade) == 0) ? 1 : -1];
typedef char hod_offset01[(offsetof(HudOverlayData, boss_bgm_frame) == 1) ? 1 : -1];
typedef char hod_offset02[(offsetof(HudOverlayData, popup_frame) == 2) ? 1 : -1];
typedef char hod_offset03[(offsetof(HudOverlayData, bb_txt_seg) == 4) ? 1 : -1];
typedef char hod_offset04[(offsetof(HudOverlayData, gStage_1) == 6) ? 1 : -1];
typedef char hod_offset05[(offsetof(HudOverlayData, gFINAL_STAGE) == 14) ? 1 : -1];
typedef char hod_offset06[(offsetof(HudOverlayData, gEXTRA_STAGE) == 26) ? 1 : -1];
typedef char hod_offset07[(offsetof(HudOverlayData, gpHISCORE_ENTRY) == 38) ? 1 : -1];
typedef char hod_offset08[(offsetof(HudOverlayData, gpEXTEND) == 47) ? 1 : -1];
typedef char hod_offset09[(offsetof(HudOverlayData, gpBONUS) == 53) ? 1 : -1];
typedef char hod_offset10[(offsetof(HudOverlayData, gpFULL_POWERUP) == 58) ? 1 : -1];
typedef char hod_offset11[(offsetof(HudOverlayData, gpDREAMBONUS_MAX) == 67) ? 1 : -1];
typedef char hod_offset12[(offsetof(HudOverlayData, POPUP_STRINGS) == 78) ? 1 : -1];
typedef char hod_offset13[(offsetof(HudOverlayData, dissolve_sprite) == 98) ? 1 : -1];
typedef char hod_offset14[(offsetof(HudOverlayData, PLAYFIELD_BLANK_ROW) == 100) ? 1 : -1];
typedef char hod_offset15[(offsetof(HudOverlayData, gDEMO_PLAY) == 104) ? 1 : -1];
typedef char hod_offset16[(offsetof(HudOverlayData, blank_row) == 114) ? 1 : -1];
#endif
