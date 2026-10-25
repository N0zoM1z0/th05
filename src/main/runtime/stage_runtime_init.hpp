// Full canonical motion and real per-stage state/reset interfaces.
#ifndef TH05_STAGE_RUNTIME_HPP
#define TH05_STAGE_RUNTIME_HPP
#include "src/main/player/player.hpp"
#include "src/main/hud/resident.hpp"

#if GAME != 5 || BINARY != 'M'
#error This owner implements TH05 MAIN per-stage runtime initialization
#endif

typedef int vram_y_t;
typedef bool (near *near RuntimeStdCallback)(void);
typedef void (near pascal *near nearfunc_t_near)(void);

extern unsigned int stage_frame;
extern bool bombing_disabled;
extern vram_y_t scroll_line;
extern unsigned int tile_ring_scroll_row_prev;
extern vram_y_t scroll_line_on_page[2];
extern SubpixelLength8 scroll_subpixel_line;
extern unsigned char scroll_row_advance_current;
extern unsigned char scroll_row_advance_previous;
extern pixel_t playfield_shake_x;
extern pixel_t playfield_shake_y;
extern unsigned char player_miss_animation_frame;
extern unsigned char miss_time;
extern unsigned char player_is_hit;
extern unsigned char player_invincibility_time;
extern unsigned char stage_point_items_collected;
extern unsigned char shot_time;
extern RuntimeStdCallback std_update;
extern bool scroll_active;
extern nearfunc_t_near bg_render_bombing_func;

#pragma codeseg STAGE_RUNTIME_TEXT main_01
void near stage_runtime_init(void);
extern "C" void near stage_state_init(void);
// Exact current C/Pascal far interface from the accepted item owner.
extern "C" void pascal far shot_level_update(void);
#pragma samecodeseg shot_level_update
void near randring_fill(void);
void near bomb_reset(void);
extern "C" void near sparks_init(void);
extern "C" void pascal near hud_score_put(void);
extern "C" void pascal near pointnums_init(void);
void far hud_put(void);
#pragma samecodeseg hud_put
void pascal near tiles_render_all(void);
void near tiles_invalidate_reset(void);
bool near std_update_frames_then_animate_dialog_and_activate_boss_if_done(void);
#pragma codeseg STAGE_RUNTIME_MAIN03_CONTEXT main_03
void far items_init(void);
#pragma codeseg

typedef char stage_runtime_motion_is_full[(sizeof(PlayfieldMotion) == 12) ? 1 : -1];
typedef char stage_runtime_scroll_fraction_is_1[(sizeof(scroll_subpixel_line) == 1) ? 1 : -1];
typedef char stage_runtime_scroll_pages_is_4[(sizeof(scroll_line_on_page) == 4) ? 1 : -1];
typedef char stage_runtime_std_callback_is_2[(sizeof(RuntimeStdCallback) == 2) ? 1 : -1];
typedef char stage_runtime_background_callback_is_2[(sizeof(nearfunc_t_near) == 2) ? 1 : -1];
#endif
