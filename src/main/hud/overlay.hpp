// Candidate local HUD ABI, adapted from nmlgc/ReC98@b6ba5b0a529edbb3:
// th04/main/hud/overlay.hpp, th02/main/hud/overlay.hpp, pc98.h,
// th04/gaiji/gaiji.h and the matching Borland/master.lib declarations.
#ifndef TH05_MAIN_HUD_OVERLAY_HPP
#define TH05_MAIN_HUD_OVERLAY_HPP

#include "src/shared/geometry.hpp"
#include "src/main/hud/resident.hpp"

typedef int tram_x_t;
typedef int tram_y_t;
typedef int vram_x_t;
typedef int vram_y_t;
typedef int shiftjis_ank_amount_t;
typedef int shiftjis_kanji_amount_t;
typedef unsigned int ushiftjis_kanji_amount_t;
typedef uint8_t shiftjis_t;
typedef void (near pascal *near nearfunc_t_near)(void);

struct point_t {
    pixel_t x;
    pixel_t y;
};

// Only the glyph identifiers used by this producer are named here. The type
// still has the original one-byte enum representation, including value FFh.
typedef enum {
    g_NULL = 0,
    g_EMPTY = 0x02,
    g_OVERLAY_FADE = 0x38,
    g_OVERLAY_FADE_last = 0x3f,
    gb_0 = 0xa0,
    gb_1 = 0xa1,
    g_NONE = 0xff
} gaiji_th04_t;

enum popup_id_t {
    POPUP_ID_HISCORE_ENTRY = 0,
    POPUP_ID_EXTEND = 1,
    POPUP_ID_BONUS = 2,
    POPUP_ID_FULL_POWERUP = 3,
    POPUP_ID_DREAMBONUS_MAX = 4,
    _popup_id_t_FORCE_UINT8 = 0xff
};

#define PLAYFIELD_LEFT 32
#define PLAYFIELD_TOP 16
#define PLAYFIELD_W 384
#define PLAYFIELD_H 368
#define PLAYFIELD_RIGHT (PLAYFIELD_LEFT + PLAYFIELD_W)
#define PLAYFIELD_BOTTOM (PLAYFIELD_TOP + PLAYFIELD_H)
#define GLYPH_HALF_W 8
#define GLYPH_H 16
#define GLYPH_FULL_W 16
#define GAIJI_W 16
#define GAIJI_TRAM_W 2
#define PLAYFIELD_TRAM_LEFT (PLAYFIELD_LEFT / 8)
#define PLAYFIELD_TRAM_TOP (PLAYFIELD_TOP / GLYPH_H)
#define PLAYFIELD_TRAM_RIGHT (PLAYFIELD_RIGHT / 8)
#define PLAYFIELD_TRAM_BOTTOM (PLAYFIELD_BOTTOM / GLYPH_H)
#define PLAYFIELD_TRAM_CENTER_X ((PLAYFIELD_LEFT + (PLAYFIELD_W / 2)) / GLYPH_HALF_W)
#define PLAYFIELD_TRAM_CENTER_Y ((PLAYFIELD_TOP + (PLAYFIELD_H / 2)) / GLYPH_H)
#define TO_SP(v) ((v) << 4)
#define TO_PIXEL(v) ((v) >> 4)

#define TX_BLACK 0x01
#define TX_YELLOW 0xc1
#define TX_WHITE 0xe1
#define TX_BLINK 2
#define TX_REVERSE 4
#define V_WHITE 15
#define SEG_PLANE_B 0xa800
#define OVERLAY_FADE_CELS 8
#define BB_TXT_H 32
#define BB_TXT_IN_SPRITE 16
#define BB_TXT_IN_CELS 8
#define BB_TXT_OUT_SPRITE 0
#define BB_TXT_OUT_CELS 16

static const int OVERLAY_FADE_INTERVAL = 8;
static const int OVERLAY_FADE_FRAMES = ((OVERLAY_FADE_CELS + 1) * OVERLAY_FADE_INTERVAL);

inline subpixel_t to_sp(float pixel_v) {
    return static_cast<subpixel_t>(pixel_v * 16);
}

extern "C" {
    void far pascal gaiji_putca(unsigned x, unsigned y, unsigned glyph, unsigned attribute);
    void far pascal gaiji_putsa(unsigned x, unsigned y, const char far *text, unsigned attribute);
    void far pascal text_putca(unsigned x, unsigned y, unsigned character, unsigned attribute);
    void far pascal text_putsa(unsigned x, unsigned y, const char far *text, unsigned attribute);
    void pascal near tiles_invalidate_around(subpixel_t center_y, subpixel_t center_x);
    vram_y_t pascal near scroll_subpixel_y_to_vram_seg1(subpixel_t y);
    void pascal near nullfunc_near(void);
}

void near grcg_setmode_rmw(void);
void near grcg_setcolor_direct_raw(void);
void __fastcall near bb_txt_put_8_raw(unsigned int left, unsigned int top);
void far pascal hud_points_put(unsigned int left, unsigned int y, unsigned long points);

#define tiles_invalidate_around_xy(center_x, center_y) tiles_invalidate_around(center_y, center_x)
#define grcg_setcolor_direct(col) _AH = col; grcg_setcolor_direct_raw()
#define grcg_off() outportb(0x7c, 0)
#define bb_txt_put_8(left, top, sprite) _CX = sprite; bb_txt_put_8_raw(left, top)

#define overlay_line_fill(y, attribute) { \
    extern const shiftjis_t *PLAYFIELD_BLANK_ROW; \
    text_putsa(PLAYFIELD_TRAM_LEFT, y, PLAYFIELD_BLANK_ROW, attribute); \
}
#define overlay_fill(attribute) { \
    for(tram_y_t y = PLAYFIELD_TRAM_TOP; y < PLAYFIELD_TRAM_BOTTOM; y++) { \
        overlay_line_fill(y, attribute); \
    } \
}

extern point_t tile_invalidate_box;
extern nearfunc_t_near overlay1;
extern nearfunc_t_near overlay2;
extern popup_id_t overlay_popup_id_new;
extern unsigned long overlay_popup_bonus;
extern unsigned char stage_id;
extern unsigned char bgm_title_id;
extern shiftjis_t far *stage_title;
extern shiftjis_t far *stage_bgm_title;
extern shiftjis_t far *boss_bgm_title;

void near overlay_wipe(void);
void near overlay_black(void);
void pascal near overlay_stage_enter_update_and_render(void);
void pascal near overlay_stage_leave_update_and_render(void);
void near overlay_titles_invalidate(void);
void pascal near overlay_titles_update_and_render(void);
void pascal near overlay_boss_bgm_update_and_render(void);
void pascal near overlay_popup_update_and_render(void);

typedef char th05_overlay_callback_is_2[(sizeof(nearfunc_t_near) == 2) ? 1 : -1];
typedef char th05_overlay_point_is_4[(sizeof(point_t) == 4) ? 1 : -1];
typedef char th05_overlay_gaiji_is_1[(sizeof(gaiji_th04_t) == 1) ? 1 : -1];
typedef char th05_overlay_popup_id_is_1[(sizeof(popup_id_t) == 1) ? 1 : -1];
typedef char th05_overlay_shiftjis_is_1[(sizeof(shiftjis_t) == 1) ? 1 : -1];

#endif
