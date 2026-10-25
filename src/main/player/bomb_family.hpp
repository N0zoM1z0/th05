// One genuine consecutive bomb family; standalone interfaces stay unchanged.
#ifndef TH05_BOMB_FAMILY_HPP
#define TH05_BOMB_FAMILY_HPP
#pragma codeseg BOMB_FAMILY_TEXT main_01
// Capture actual local first declarations before importing foreign interfaces.
void near bomb_reset(void);
extern "C" void pascal near player_bomb(void);
extern "C" void pascal near bb_playchar_put(int cel);
void near bomb_dream_decay(void);
void near reimu_stars_update_and_render(void);
void near reimu_bomb_draw(void);
void pascal near bomb_reimu(void);
void near marisa_lasers_update_and_render(void);
void near marisa_bomb_draw(void);
void pascal near bomb_marisa(void);
void near mima_circles_update_and_render(void);
void near mima_bomb_draw(void);
void pascal near bomb_mima(void);
#include <dos.h>
#include "src/main/player/bombanim.hpp"
#include "src/main/player/player.hpp"
#include "src/main/player/bomb_draw.hpp"
#include "src/main/player/long_bomb_control.hpp"
#include "src/main/player/mima_bomb.hpp"
// Actual AE1:347A provider retains its far Pascal RETF4 interface.
// Explicit same-CS context preserves the original relaxed call at FD03.
#pragma samecodeseg circles_add_growing

// Complete canonical ODR definition from boss/movement.hpp, with no shortening.
struct boss_stuff_t {
    PlayfieldMotion pos;
    int hp;
    unsigned char sprite;
    unsigned char phase;
    int phase_frame;
    unsigned char damage_this_frame;
    unsigned char mode;
    unsigned char angle;
    union {
        unsigned char patterns_seen;
        bool defeat_bonus;
    } phase_state;
    int phase_end_hp;
};
extern boss_stuff_t boss;
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


#pragma codeseg _TEXT
extern "C" void pascal far grcg_boxfill(int left, int top, int right, int bottom);
#pragma codeseg MAIN_BOMB_SPARKS main_03
void far bomb_sparks_add_at_player(void);
#pragma codeseg BOMB_FAMILY_TEXT main_01
void near marisa_bomb_backdrop_render(void);
extern unsigned char shot_time;
static const unsigned char SHOT_BLOCKED_FOR_THIS_FRAME = 0xFF;
typedef char bomb_family_boss_is_24[(sizeof(boss_stuff_t) == 24) ? 1 : -1];
typedef char bomb_family_boss_phase_at_15[(offsetof(boss_stuff_t, phase) == 15) ? 1 : -1];
#endif
