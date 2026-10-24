// TH05 Sara interfaces and real laser ABI from natural ReC98
// b6ba5b0a529edbb31efdf8c0e939263804f8ee47: boss/b1.cpp, bullet/laser.hpp,
// th04/main/boss/boss.hpp, bullet/bullet.hpp, gather.hpp and pattern.hpp.
#ifndef TH05_MAIN_BOSS_SARA_HPP
#define TH05_MAIN_BOSS_SARA_HPP

#include "src/main/boss/movement.hpp"
#include "src/main/gather/gather.hpp"

#if GAME != 5 || BINARY != 'M'
#error This owner is the TH05 MAIN Sara update implementation
#endif

typedef char int8_t;
typedef void (near *near pattern_loop_func_t)(void);
typedef void (near pascal *near nearfunc_t_near)(void);

static const int RES_X = 640;
static const int BOSS_W = 64;
static const int HUD_HP_FILL_FRAMES = 128;
static const int ENTRANCE_BB_TRANSITION_FRAMES_PER_CEL = 2;
static const int TILES_BB_CELS = 16;
static const unsigned char PHASE_HP_FILL = 0;
static const unsigned char PHASE_BOSS_ENTRANCE_BB = 1;
static const unsigned char PHASE_BOSS_EXPLODE_SMALL = 253;
// Used constants retain the original complete main sprite enum's true word
// domain. The owner does not redefine the accepted update.hpp enum/type.
enum sara_main_patnum_t {
    PAT_BULLET16_N_BALL_BLUE = 44, PAT_BULLET16_N_BALL_RED = 48,
    PAT_SARA_STAY = 180, PAT_SARA_SPIN = 188, PAT_SARA_SPIN_last = 191,
    PAT_STAGE_last = 319, PAT_MAX = 320,
    _sara_main_patnum_t_FORCE_INT16 = 0x7FFF
};
#define BST_CLOUD_FORWARDS 0x02
#define BST_CLOUD_BACKWARDS 0x03
#define BST_NO_DECELERATE 0x10

enum x_direction_t { X_RIGHT = 0, X_LEFT = 1 };
enum explosion_type_t {
    ET_NONE = -1, ET_CIRCLE = 0, ET_NW_SE = 1, ET_SW_NE = 2,
    ET_HORIZONTAL = 3, ET_VERTICAL = 4,
    _explosion_type_t_FORCE_INT16 = 0x7FFF
};
enum laser_flag_t {
    LF_FREE = 0, LF_SHOOTOUT = 1, LF_FIXED_WAIT_TO_GROW = 2,
    LF_FIXED_GROW = 3, LF_FIXED_ACTIVE = 4, LF_FIXED_SHRINK = 5,
    LF_FIXED_SHRINK_AND_WAIT_TO_GROW = 6, LF_SHOOTOUT_DECAY = 7,
    _laser_flag_t_FORCE_UINT8 = 0xFF
};
struct laser_coords_t {
    PlayfieldPoint origin;
    Subpixel starts_at_distance;
    Subpixel ends_at_distance;
    unsigned char angle;
    union { char shrink; unsigned char nonshrink; } width;
};
struct Laser {
    laser_flag_t flag;
    vc_t col;
    laser_coords_t coords;
    Subpixel shootout_speed;
    int age;
    union { int grow; int moveout; } active_at_age;
    int shrink_at_age;
    unsigned char grow_to_width;
    // Genuine3byte unused tail present in laser.hpp/laser.inc, not invented
    // padding to fit an operand. All24bytes of every original slot remain.
    uint8_t padding[3];

    void fixed_init(const PlayfieldPoint &origin) {
        flag = LF_FIXED_WAIT_TO_GROW;
        coords.origin = origin;
        coords.starts_at_distance.v = to_sp(16.0f);
        coords.ends_at_distance.v = to_sp(550.0f);
        age = 0;
    }
};

extern unsigned char boss_statebyte[16];
extern SPPoint homing_target;
extern unsigned char stage_frame_mod16;
extern Laser lasers[32];
extern Laser laser_template;
extern nearfunc_t_near bullet_template_tune;
extern nearfunc_t_near bg_render_bombing_func;

// The callback's first declaration must carry its actual main_01 frame.
#pragma codeseg BOSS_BG_TEXT main_01
void pascal near sara_bg_render(void);
#pragma codeseg LASER_SC_TEXT main_03
void pascal near laser_manual_fixed_spawn(int slot);
void pascal near laser_manual_grow(int slot);
void pascal near laser_stop(int slot);
#pragma codeseg

void near gather_add_only(void);
void pascal near gather_add_only_3stack(int frame, vc2 first, vc2 other);
bool near boss_hittest_shots(void);
void near boss_hittest_shots_invincible(void);
void pascal near boss_score_bonus(unsigned int units);
void pascal near boss_phase_next(explosion_type_t type, int next_end_hp);
void pascal near boss_defeat_update(unsigned int bonus_units);
void pascal near hud_hp_update_and_render(int hp, int total);
extern "C" {
    void pascal far snd_se_play(int new_se);
    int pascal far select_for_rank(int easy, int normal, int hard, int lunatic);
}

inline subpixel_length_8_t sara_to_sp8(float value) {
    return static_cast<subpixel_length_8_t>(value * 16);
}
inline subpixel_t sara_rand_speed(float min, float max) {
    return randring2_next8_and_ge_lt(sara_to_sp8(min), sara_to_sp8(max));
}
// These are the reference's natural little-endian packed-field setters, kept
// as owner-local inline functions rather than changing the accepted class.
// Actual adjoining fields and all widths are asserted in template.hpp.
inline void sara_set_spread(unsigned char count, unsigned char angle_delta) {
    reinterpret_cast<uint16_t &>(bullet_template.spread) =
        (count | (angle_delta << 8));
}
inline void sara_set_stack(unsigned char count, float speed_delta) {
    reinterpret_cast<uint16_t &>(bullet_template.stack) =
        (count | (sara_to_sp8(speed_delta) << 8));
}
inline void sara_set_spread_stack(unsigned char count, unsigned char delta,
    unsigned char stack, float speed_delta) {
    reinterpret_cast<uint32_t &>(bullet_template.spread) =
        (count | (delta << 8) | (static_cast<uint32_t>(stack) << 16) |
        (static_cast<uint32_t>(sara_to_sp8(speed_delta)) << 24));
}
inline void sara_set_spread_for_rank(unsigned char count_e, unsigned char delta_e,
    unsigned char count_n, unsigned char delta_n,
    unsigned char count_h, unsigned char delta_h,
    unsigned char count_l, unsigned char delta_l) {
    reinterpret_cast<uint16_t &>(bullet_template.spread) = select_for_rank(
        (count_e | (delta_e << 8)), (count_n | (delta_n << 8)),
        (count_h | (delta_h << 8)), (count_l | (delta_l << 8)));
}

void pascal far sara_update(void);
typedef char sara_pattern_callback_is_2[(sizeof(pattern_loop_func_t) == 2) ? 1 : -1];
typedef char sara_sprite_domain_is_2[(sizeof(sara_main_patnum_t) == 2) ? 1 : -1];
typedef char sara_tuning_callback_is_2[(sizeof(nearfunc_t_near) == 2) ? 1 : -1];
typedef char sara_laser_coordinates_are_10[(sizeof(laser_coords_t) == 10) ? 1 : -1];
typedef char sara_laser_is_24[(sizeof(Laser) == 24) ? 1 : -1];
typedef char sara_laser_color_at_1[(offsetof(Laser, col) == 1) ? 1 : -1];
typedef char sara_laser_origin_at_2[(offsetof(Laser, coords.origin) == 2) ? 1 : -1];
typedef char sara_laser_start_at_6[(offsetof(Laser, coords.starts_at_distance) == 6) ? 1 : -1];
typedef char sara_laser_end_at_8[(offsetof(Laser, coords.ends_at_distance) == 8) ? 1 : -1];
typedef char sara_laser_angle_at_10[(offsetof(Laser, coords.angle) == 10) ? 1 : -1];
typedef char sara_laser_width_at_11[(offsetof(Laser, coords.width) == 11) ? 1 : -1];
typedef char sara_laser_speed_at_12[(offsetof(Laser, shootout_speed) == 12) ? 1 : -1];
typedef char sara_laser_age_at_14[(offsetof(Laser, age) == 14) ? 1 : -1];
typedef char sara_laser_active_at_16[(offsetof(Laser, active_at_age) == 16) ? 1 : -1];
typedef char sara_laser_shrink_at_18[(offsetof(Laser, shrink_at_age) == 18) ? 1 : -1];
typedef char sara_laser_growth_width_at_20[(offsetof(Laser, grow_to_width) == 20) ? 1 : -1];
typedef char sara_laser_unused_at_21[(offsetof(Laser, padding) == 21) ? 1 : -1];

#endif
