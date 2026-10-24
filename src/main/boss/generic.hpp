// Generic TH05 boss interfaces. Reuse complete accepted boss/midboss/resident
// structures; this file supplies real interfaces, never helper implementations.
#ifndef TH05_MAIN_BOSS_GENERIC_HPP
#define TH05_MAIN_BOSS_GENERIC_HPP

#include <dos.h>

// These callbacks and far routines genuinely belong to main_01, independently
// of this owner's main_03 frame. Declare them before the shared setup surface.
#pragma codeseg GENERIC_BOSS_MAIN01_TEXT main_01
extern "C" void pascal near nullfunc_near(void);
void pascal near tiles_render_all(void);
void pascal near overlay_stage_leave_update_and_render(void);
int far shots_hittest(void);
void far dialog_animate(void);
void far end_game(void);
void far end_extra(void);
#pragma codeseg BOSS_TEXT main_03

#include "src/main/stage/setup.hpp"
#include "src/main/hud/resident.hpp"
#include "src/main/bullet/template.hpp"

#if GAME != 5 || BINARY != 'M'
#error This owner is the TH05 MAIN generic boss implementation
#endif

enum explosion_type_t {
    ET_NONE = -1, ET_CIRCLE = 0, ET_NW_SE = 1, ET_SW_NE = 2,
    ET_HORIZONTAL = 3, ET_VERTICAL = 4,
    _explosion_type_t_FORCE_INT16 = 0x7FFF
};
enum item_type_t {
    IT_NONE = -2, IT_ENEMY_DROP_NEXT = -1, IT_POWER = 0,
    IT_POINT = 1, IT_DREAM = 2, IT_BIGPOWER = 3, IT_BOMB = 4,
    IT_1UP = 5, IT_FULLPOWER = 6, IT_COUNT
};
union BulletZapState { bool active; uint8_t frame; };
extern BulletZapState bullet_zap;
extern unsigned char bullet_clear_time;
extern bool shots_hittest_against_boss;
extern SPPoint shot_hitbox_center;
extern SPPoint shot_hitbox_radius;
extern PlayfieldMotion player_pos;
extern unsigned char player_is_hit;
extern unsigned char player_invincibility_time;
extern unsigned char power;
extern unsigned char stage_frame_mod2;
extern unsigned char stage_frame_mod4;
extern unsigned char stage_id;
enum quit_t { Q_KEEP_RUNNING = 0, Q_QUIT_TO_OP = 1, Q_NEXT_STAGE = 2 };
extern quit_t quit;
extern bool bombing_disabled;
extern int playfield_shake_x;
extern int playfield_shake_y;
extern unsigned int slowdown_factor;
extern unsigned int PaletteTone;
extern bool palette_changed;
extern SPPoint homing_target;
extern score_lebcd_t score;
extern unsigned int stage_graze;
extern nearfunc_t_near bg_render_bombing_func;
extern nearfunc_t_near overlay1;

void pascal near boss_explode_small(explosion_type_t type);
void near boss_explode_big_circle(void);
void pascal near boss_score_bonus(unsigned int units);
void pascal near items_add(subpixel_t center_x, subpixel_t center_y, item_type_t type);
void near stage_clear_bonus(void);
void near stage_allclear_bonus(void);
extern "C" {
    void pascal far snd_se_play(int effect);
    int pascal far snd_kaja_interrupt(int ax);
}
void pascal far frame_delay(int frames);

static const pixel_t BOSS_W = 64;
static const pixel_t BOSS_H = 64;
static const int BOSS_DEFEAT_INVINCIBILITY_FRAMES = 255;
static const unsigned char PHASE_BOSS_EXPLODE_SMALL = 253;
static const unsigned char PHASE_BOSS_EXPLODE_BIG = 254;
static const unsigned char POWER_MAX = 128;
static const unsigned char STAGE_EXTRA = 6;
static const unsigned char PAT_ENEMY_KILL = 4;
static const unsigned char PAT_ENEMY_KILL_last = 11;
static const int KAJA_SONG_FADE = 2;
static const subpixel_t HOMING_TARGET_NONE = (-999 * 16);
enum boss_defeat_frames_t {
    BDF_SMALL_1 = 1, BDF_SMALL_2 = 16, BDF_BIG = 32,
    BDF_DIALOG = 1, BDF_FADEOUT = 416, BDF_NEXT_STAGE = 488
};
#define TO_SP(value) ((value) << 4)
#define bullets_clear() { if(bullet_clear_time < 20) { bullet_clear_time = 20; } }
#define palette_settone_deferred(tone) { PaletteTone = tone; palette_changed = true; }
#define overlay_stage_leave() (overlay1 = overlay_stage_leave_update_and_render)
#define snd_kaja_func(operation, parameter) \
    snd_kaja_interrupt(((operation) << 8) | static_cast<uint8_t>(parameter))
#define boss_defeat_explode_big(type, bonus_units) { \
    boss_explode_big_circle(); \
    boss.phase++; \
    bullet_zap.active = boss.phase_state.defeat_bonus; \
    if(boss.phase_state.defeat_bonus) { boss_score_bonus(bonus_units); } \
    boss.sprite = PAT_ENEMY_KILL; \
    boss.phase_frame = 0; \
}

inline int shots_hittest(const PlayfieldPoint &center,
    const subpixel_t &radius_x, const subpixel_t &radius_y) {
    shot_hitbox_radius.x.v = radius_x;
    shot_hitbox_radius.y.v = radius_y;
    shot_hitbox_center = center;
    return shots_hittest();
}
#define overlap_1d_inplace_fast(delta, extent) ( \
    (unsigned int)((delta) += (extent / 2), delta) <= (extent) \
)
#define overlap_wh_inplace_fast(delta_x, delta_y, w, h) ( \
    overlap_1d_inplace_fast(delta_x, w) && overlap_1d_inplace_fast(delta_y, h) \
)

typedef char th05_generic_item_type_is_1[(sizeof(item_type_t) == 1) ? 1 : -1];
typedef char th05_generic_explosion_type_is_2[(sizeof(explosion_type_t) == 2) ? 1 : -1];
typedef char th05_generic_bullet_zap_is_1[(sizeof(BulletZapState) == 1) ? 1 : -1];

#endif
