// Shared declarations for the remaining small natural GAME5 MAIN owners.
// Natural-source provenance: ReC98@b6ba5b0a529edbb31efdf8c0e939263804f8ee47,
// slowdown.hpp, scroll.hpp, tile/tile.hpp, hud/hud.hpp, player/player.hpp.
#ifndef TH05_MAIN_RUNTIME_SMALL_HPP
#define TH05_MAIN_RUNTIME_SMALL_HPP

#include <dos.h>
#include "src/main/player/player.hpp"
#include "src/main/hud/resident.hpp"

#if GAME != 5 || BINARY != 'M'
#error These owners implement the TH05 MAIN ABI
#endif

typedef int vram_y_t;
typedef void (near pascal *near SmallRenderCallback)(void);
static const int PLAYFIELD_W = 384;
static const int PLAYFIELD_H = 368;
static const int RES_Y = 400;
static const int BAR_MAX = 128;
static const unsigned char ANGLE_PER_SPRITE = 8;
enum small_sprite_domain {
    PAT_BULLET16_V = 84, PAT_SWORD = 193,
    PAT_STAGE_last = 319, PAT_MAX = 320,
    _small_sprite_domain_FORCE_INT16 = 0x7FFF
};
static inline subpixel_t small_to_sp(float pixel_value) {
    return static_cast<subpixel_t>(pixel_value * 16);
}
#define TO_PIXEL(value) ((value) >> 4)

extern "C" volatile unsigned int vsync_Count1;
extern unsigned int slowdown_factor;
extern vram_y_t scroll_line;
extern bool scroll_active;
extern int hud_hp_bar_value_prev;
extern uint8_t tile_render_all_time;
extern SmallRenderCallback bg_render_not_bombing;
extern SmallRenderCallback midboss_invalidate;
extern SmallRenderCallback stage_invalidate;

// Explicit first-declaration context for foreign main_01 entry points,
// including the genuinely far-Pascal low-level HP renderer.
#pragma codeseg SMALL_MAIN01_CONTEXT main_01
void pascal far hud_hp_put(int value);
void near overlay_titles_invalidate(void);
void near player_invalidate(void);
void near shots_invalidate(void);
void near enemies_invalidate(void);
void near bullets_and_gather_invalidate(void);
void near items_invalidate(void);
void near sparks_invalidate(void);
void near pointnums_invalidate(void);
void pascal near tiles_redraw_invalidated(void);
void pascal near tiles_render_all(void);
#pragma codeseg

typedef char small_render_pointer_is_2[(sizeof(SmallRenderCallback) == 2) ? 1 : -1];
typedef char small_scroll_line_is_2[(sizeof(scroll_line) == 2) ? 1 : -1];
typedef char small_scroll_flag_is_1[(sizeof(scroll_active) == 1) ? 1 : -1];
typedef char small_hp_bar_word_is_2[(sizeof(hud_hp_bar_value_prev) == 2) ? 1 : -1];
typedef char small_sprite_domain_is_2[(sizeof(small_sprite_domain) == 2) ? 1 : -1];

#endif
