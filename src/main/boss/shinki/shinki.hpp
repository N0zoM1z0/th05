// Real TH05 Shinki interfaces, adapting natural ReC98
// b6ba5b0a529edbb31efdf8c0e939263804f8ee47: boss/b6.cpp, bullet/b6ball.hpp,
// pc98.h, custom.hpp, score/palette/player and bullet-control headers.
#ifndef TH05_MAIN_BOSS_SHINKI_HPP
#define TH05_MAIN_BOSS_SHINKI_HPP

// Capture all owned entry declarations under their explicit contribution and
// shared main_03 frame before any transitively included declarations.
#pragma codeseg B6_BALLS_TEXT main_03
void near b6balls_add(void);
void near b6balls_update(void);
#pragma codeseg B6_UPDATE_TEXT main_03
void pascal far shinki_update(void);
#pragma codeseg

// Reuse one complete physical definition of Boss, Laser, BulletTemplate,
// gather, motion and custom entities; no accepted/shared header is changed.
#include "src/main/boss/sara/sara.hpp"
#include "src/main/bullet/cheeto.hpp"

typedef int bool16;
typedef bool (near *near pattern_oneshot_func_t)(void);
#pragma codeseg B6_PATTERN_A_TEXT main_03
bool near pattern_curved_rings(void);
bool near pattern_dualspeed_rings(void);
#pragma codeseg
static const int PLAYFIELD_W = 384;
static const int PLAYFIELD_H = 368;
static const int BOSS_H = 64;
static const int BOSS_HITBOX_DEFAULT_W = 24;
static const int SHINKI_WING_W = 256;
static const int SHINKI_WING_H = 96;
static const int ENTRANCE_BB_FRAMES_PER_CEL = 4;
enum clock_direction_t { CLOCKWISE = 0, COUNTERCLOCKWISE = 1 };
enum shinki_main_patnum_t {
    PAT_BULLET16_N_OUTLINED_BALL_BLUE = 45,
    PAT_BULLET16_D_BLUE = 52, PAT_BULLET16_V_RED = 84,
    PAT_BULLET16_V_BLUE = 116,
    PAT_SHINKI_STILL = 180, PAT_SHINKI_CAST = 181,
    PAT_SHINKI_RIGHT = 182, PAT_SHINKI_LEFT = 183,
    PAT_SHINKI_WINGS_WHITE = 184, PAT_SHINKI_WINGS_PURPLE = 192,
    TINY_B6BALL_START = 200, PAT_B6BALL_BLUE_1 = 200,
    PAT_B6BALL_PURPLE = 201, PAT_DECAY_B6BALL = 204,
    PAT_DECAY_B6BALL_last = 207, TINY_B6BALL_END = 208,
    _shinki_main_patnum_t_FORCE_INT16 = 0x7FFF
};

#define B6BALL_COUNT 63
#define B6BALL_W 32
#define B6BALL_H 32
enum b6ball_flag_t {
    B6BF_FREE = 0, B6BF_CLOUD = 1, B6BF_ALIVE = 2, B6BF_DECAY = 3,
    _b6ball_flag_t_FORCE_UINT8 = 0xFF
};
struct b6ball_t {
    b6ball_flag_t flag;
    char unused_1;
    PlayfieldMotion pos;
    unsigned int age;
    Subpixel cloud_radius;
    int patnum_tiny;
    int decay_frame;
    char unused_2[4];
};
struct b6ball_template_t {
    char _unused_1;
    unsigned char angle;
    PlayfieldPoint origin;
    int _unused_2[6];
    int patnum_tiny;
    int _unused_3[2];
    SubpixelLength8 speed;
};
#define b6ball_template (reinterpret_cast<b6ball_template_t &>(custom_entities[0]))
#define b6balls (reinterpret_cast<b6ball_t *>(&custom_entities[1]))

// Identical canonical union definition to accepted update.hpp; includes of
// update.hpp and gather.hpp together would duplicate their entity_flag enum.
// This union's full definition/tokens and external object type stay unchanged.
union BulletZapState { bool active; uint8_t frame; };
extern BulletZapState bullet_zap;
extern unsigned char bullet_clear_time;
extern unsigned char stage_frame_mod4;
extern unsigned char stage_frame_mod8;
extern int playfield_shake_anim_time;
extern bool bombing;
extern bool palette_changed;
extern SPPoint boss_hitbox_radius;
extern nearfunc_t_near boss_custombullets_render;

#define COLOR_COUNT 16
#define COMPONENT_COUNT 3
template <class ComponentType, int Range> union RGB {
    struct { ComponentType r, g, b; } c;
    ComponentType v[COMPONENT_COUNT];
    static ComponentType min() { return 0; }
    static ComponentType max() { return Range - 1; }
    void set(ComponentType r, ComponentType g, ComponentType b) {
        this->c.r = r; this->c.g = g; this->c.b = b;
    }
};
template <class RGBType> struct Palette {
    RGBType colors[COLOR_COUNT];
    static int range() { return RGBType::Range; }
    RGBType& operator [](vc2 col) { return colors[col]; }
    const RGBType& operator [](vc2 col) const { return colors[col]; }
};
typedef RGB<uint8_t, 256> RGB8;
typedef Palette<RGB8> Palette8;
extern "C" {
    extern Palette8 __cdecl Palettes;
    extern unsigned int __cdecl PaletteTone;
    int pascal far super_convert_tiny(int num);
    void near bullets_add_regular_fixedspeed(void);
}
int pascal far select_for_playchar(int reimu, int marisa, int mima, int yuuka);
#define palette_settone_deferred(value) { PaletteTone = value; palette_changed = true; }
#pragma codeseg MAIN_0_TEXT main_01
void pascal near shinki_custombullets_render(void);
#pragma codeseg BOSS_BG_TEXT main_01
void pascal near shinki_bg_render(void);
#pragma codeseg BULLET_A_TEXT main_03
extern "C" subpixel_length_8_t __fastcall near playperf_speedtune(subpixel_length_8_t speed);
#pragma codeseg
void pascal near boss_explode_small(explosion_type_t type);

inline void shinki_gather_template_init(void) {
    gather_template.radius.v = to_sp(64.0f);
    gather_template.angle_delta = 2;
    gather_template.ring_points = 8;
}
inline subpixel_t shinki_rand_speed16(float min, float max) {
    return to_sp(min) + randring2_next16_mod(to_sp(max) - to_sp(min));
}
static inline pixel_t shinki_playfield_fraction_y(float fraction = 1.0f) {
    return static_cast<pixel_t>(PLAYFIELD_H * fraction + 0.0001f);
}
inline void shinki_set_stack_for_rank(unsigned char count_e, float delta_e,
    unsigned char count_n, float delta_n, unsigned char count_h, float delta_h,
    unsigned char count_l, float delta_l) {
    reinterpret_cast<uint16_t &>(bullet_template.stack) = select_for_rank(
        count_e | (sara_to_sp8(delta_e) << 8), count_n | (sara_to_sp8(delta_n) << 8),
        count_h | (sara_to_sp8(delta_h) << 8), count_l | (sara_to_sp8(delta_l) << 8));
}
#define b6balls_load() { \
    for(int sprite = TINY_B6BALL_START; sprite < TINY_B6BALL_END; sprite++) { \
        super_convert_tiny(sprite); \
    } \
}
#define playfield_encloses(center_x, center_y, width_value, height_value) ( \
    static_cast<subpixel_t>(center_x) > to_sp(0 - (width_value / 2)) && \
    static_cast<subpixel_t>(center_x) < to_sp(PLAYFIELD_W + (width_value / 2)) && \
    static_cast<subpixel_t>(center_y) > to_sp(0 - (height_value / 2)) && \
    static_cast<subpixel_t>(center_y) < to_sp(PLAYFIELD_H + (height_value / 2)) \
)

typedef char shinki_b6ball_is_26[(sizeof(b6ball_t) == 26) ? 1 : -1];
typedef char shinki_b6ball_motion_at_2[(offsetof(b6ball_t, pos) == 2) ? 1 : -1];
typedef char shinki_b6ball_age_at_14[(offsetof(b6ball_t, age) == 14) ? 1 : -1];
typedef char shinki_b6ball_cloud_at_16[(offsetof(b6ball_t, cloud_radius) == 16) ? 1 : -1];
typedef char shinki_b6ball_sprite_at_18[(offsetof(b6ball_t, patnum_tiny) == 18) ? 1 : -1];
typedef char shinki_b6ball_decay_at_20[(offsetof(b6ball_t, decay_frame) == 20) ? 1 : -1];
typedef char shinki_b6ball_unused_at_22[(offsetof(b6ball_t, unused_2) == 22) ? 1 : -1];
typedef char shinki_template_is_25[(sizeof(b6ball_template_t) == 25) ? 1 : -1];
typedef char shinki_template_speed_at_24[(offsetof(b6ball_template_t, speed) == 24) ? 1 : -1];
typedef char shinki_template_fits_slot[(sizeof(b6ball_template_t) <= sizeof(custom_t)) ? 1 : -1];
typedef char shinki_slots_fit_exactly[
    ((1 + B6BALL_COUNT) * sizeof(b6ball_t) == sizeof(custom_entities)) ? 1 : -1];
typedef char shinki_rgb_is_3[(sizeof(RGB8) == 3) ? 1 : -1];
typedef char shinki_palette_is_48[(sizeof(Palette8) == 48) ? 1 : -1];
typedef char shinki_zap_is_1[(sizeof(BulletZapState) == 1) ? 1 : -1];

#pragma codeseg

#endif
