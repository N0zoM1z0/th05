// Complete canonical state plus real four-function generic bomb-control ABI.
#ifndef TH05_BOMB_RUNTIME_HPP
#define TH05_BOMB_RUNTIME_HPP
#include "src/main/boss/movement.hpp"
#include "src/main/hud/resident.hpp"

typedef void (near pascal *near nearfunc_t_near)(void);
// Canonical .BB element: one bitmap byte encodes8 tiles, not an opaque record.
typedef unsigned char bb_tiles8_t;
extern bool bombing;
extern unsigned char bomb_frame;
extern signed char bombs;
extern bool bombing_disabled;
extern unsigned char miss_time;
extern unsigned char player_is_hit;
extern unsigned char player_respawn_motion_time;
extern unsigned char player_invincibility_time;
extern unsigned char bullet_clear_time;
extern bool items_pull_to_player;
extern unsigned char dream;
extern nearfunc_t_near bg_render_bombing;
extern nearfunc_t_near bg_render_bombing_func;
extern bb_tiles8_t __seg *bb_playchar_seg;
extern bb_tiles8_t __seg *tiles_bb_seg;

static const unsigned char BOMB_RUNTIME_MISS_FRAMES = 32;
static const unsigned char BOMB_RUNTIME_BOSS_HP_FILL = 0;

#pragma codeseg SHARED
extern "C" void pascal far snd_se_play(int effect);
#pragma codeseg BOMB_RUNTIME_FOREIGN_TEXT main_01
extern "C" void pascal near nullfunc_near(void);
void pascal near tiles_bb_put_raw(int cel);
void far hud_bombs_put(void);
int pascal far select_for_playchar(int reimu, int marisa, int mima, int yuuka);
extern "C" {
    void pascal far playperf_lower(char delta);
    void pascal far hud_dream_put(void);
}
// Only genuine foreign far callees share CS. They retain their far ABI.
// The maintained bomb donor has hud_bombs_put; accepted miss.hpp corroborates
// the HUDdream/playperf protocol; both selector RETF8 and native CS are verified.
// No locally defined function receives this annotation.
#pragma samecodeseg hud_bombs_put
#pragma samecodeseg select_for_playchar
#pragma samecodeseg playperf_lower
#pragma samecodeseg hud_dream_put

#pragma codeseg BOMB_RUNTIME_TEXT main_01
void near bomb_reset(void);
extern "C" void pascal near player_bomb(void);
extern "C" void pascal near bb_playchar_put(int cel);
void near bomb_dream_decay(void);
#pragma codeseg

typedef char bomb_runtime_boss_is_24[(sizeof(boss_stuff_t) == 24) ? 1 : -1];
typedef char bomb_runtime_phase_at_15[(offsetof(boss_stuff_t, phase) == 15) ? 1 : -1];
typedef char bomb_runtime_resident_is_128[(sizeof(resident_t) == 128) ? 1 : -1];
typedef char bomb_runtime_bombs_used_at_28[(offsetof(resident_t, bombs_used) == 28) ? 1 : -1];
typedef char bomb_runtime_callback_is_2[(sizeof(nearfunc_t_near) == 2) ? 1 : -1];
typedef char bomb_runtime_bb_element_is_1[(sizeof(bb_tiles8_t) == 1) ? 1 : -1];
typedef char bomb_runtime_bb_segment_is_2[(sizeof(bb_playchar_seg) == 2) ? 1 : -1];
typedef char bomb_runtime_tile_segment_is_2[(sizeof(tiles_bb_seg) == 2) ? 1 : -1];
#endif
