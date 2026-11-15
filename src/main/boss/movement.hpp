// Boss state, the random-number helpers used for boss movement, and the two
// shared flystep movement functions. Adapted from ReC98's th04/main/boss/
// boss.hpp, th05/main/boss/boss.hpp, th02/th03 randring.hpp and
// th04/math/vector.hpp.
#ifndef TH05_MAIN_BOSS_MOVEMENT_HPP
#define TH05_MAIN_BOSS_MOVEMENT_HPP

#include "src/shared/geometry.hpp"

// Turbo C++ 4.02 predates the built-in C++ bool type. The game uses one byte.
typedef unsigned char bool;
#define false 0
#define true 1

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

template <class TX, class TY> struct LRTB {
    TX left;
    TX right;
    TY top;
    TY bottom;
};

typedef enum {
    Y_ANY,
    Y_UP,
    Y_DOWN
} y_direction_t;

extern boss_stuff_t boss;
extern unsigned int boss_sprite_left;
extern unsigned int boss_sprite_right;
extern unsigned int boss_sprite_stay;
extern LRTB<Subpixel, Subpixel> boss_flystep_random_clamp;
extern y_direction_t boss_flystep_random_next_y_direction;

uint16_t near randring2_next16(void);
uint16_t pascal near randring2_next16_and(uint16_t mask);
uint16_t pascal near randring2_next16_mod(uint16_t divisor);
extern "C" void pascal near vector2_near(
    SPPoint near &ret, unsigned char angle, subpixel_t length
);

// Middle quarter of the 384-pixel playfield. A boss left of it starts its
// random flight towards the right, and vice versa.
static const subpixel_t BOSS_FLYSTEP_RANDOM_FIELD_LEFT = (144 << 4);
static const subpixel_t BOSS_FLYSTEP_RANDOM_FIELD_RIGHT = (240 << 4);
static const int BOSS_FLYSTEP_RANDOM_FRAMES = 28;

inline subpixel_t to_sp(float pixel_v) {
    return static_cast<subpixel_t>(pixel_v * 16);
}

template <class T> inline bool is_range_a_power_of_two(T min, T max) {
    return (((max - min) & ((max - min) - 1)) == 0);
}

inline uint8_t randring2_next8_and_ge_lt(uint8_t min, uint8_t max) {
    return (min + randring2_next16_and((max - min) - 1));
}

inline uint8_t randring2_next8_mod_ge_lt(uint8_t min, uint8_t max) {
    return (static_cast<char>(min) >= 0)
        ? (min + randring2_next16_mod(max - min))
        : (randring2_next16_mod(max + -static_cast<char>(min)) - (-min));
}

inline uint8_t randring2_next8_ge_lt(uint8_t min, uint8_t max) {
    if(is_range_a_power_of_two(min, max)) {
        return randring2_next8_and_ge_lt(min, max);
    }
    return randring2_next8_mod_ge_lt(min, max);
}

// Picks a random [boss.angle] on [frame] 0, based on the boss position and the
// directional latch, then flies into that direction at a [frame]-dependent,
// decreasing speed. Returns true once [frame] reaches
// BOSS_FLYSTEP_RANDOM_FRAMES. Does nothing for negative [frame]s, which the
// boss scripts rely on.
bool pascal near boss_flystep_random(int frame);

// Moves the boss by a fraction of the remaining distance to the target point.
// Returns true once it has reached that point in both dimensions.
bool pascal near boss_flystep_towards(subpixel_t target_x, subpixel_t target_y);

// Layout checks: these offsets are hardcoded in the original code.
typedef char th05_boss_state_is_24[(sizeof(boss_stuff_t) == 24) ? 1 : -1];
typedef char th05_boss_pos_at_0[(offsetof(boss_stuff_t, pos) == 0) ? 1 : -1];
typedef char th05_boss_hp_at_12[(offsetof(boss_stuff_t, hp) == 12) ? 1 : -1];
typedef char th05_boss_sprite_at_14[(offsetof(boss_stuff_t, sprite) == 14) ? 1 : -1];
typedef char th05_boss_phase_at_15[(offsetof(boss_stuff_t, phase) == 15) ? 1 : -1];
typedef char th05_boss_frame_at_16[(offsetof(boss_stuff_t, phase_frame) == 16) ? 1 : -1];
typedef char th05_boss_damage_at_18[(offsetof(boss_stuff_t, damage_this_frame) == 18) ? 1 : -1];
typedef char th05_boss_mode_at_19[(offsetof(boss_stuff_t, mode) == 19) ? 1 : -1];
typedef char th05_boss_angle_at_20[(offsetof(boss_stuff_t, angle) == 20) ? 1 : -1];
typedef char th05_boss_phase_state_at_21[(offsetof(boss_stuff_t, phase_state) == 21) ? 1 : -1];
typedef char th05_boss_end_hp_at_22[(offsetof(boss_stuff_t, phase_end_hp) == 22) ? 1 : -1];
typedef char th05_boss_direction_is_1[(sizeof(y_direction_t) == 1) ? 1 : -1];
typedef LRTB<Subpixel, Subpixel> BossMovementClamp;
typedef char th05_boss_clamp_is_8[(sizeof(BossMovementClamp) == 8) ? 1 : -1];
typedef char th05_boss_clamp_left_at_0[(offsetof(BossMovementClamp, left) == 0) ? 1 : -1];
typedef char th05_boss_clamp_right_at_2[(offsetof(BossMovementClamp, right) == 2) ? 1 : -1];
typedef char th05_boss_clamp_top_at_4[(offsetof(BossMovementClamp, top) == 4) ? 1 : -1];
typedef char th05_boss_clamp_bottom_at_6[(offsetof(BossMovementClamp, bottom) == 6) ? 1 : -1];

#endif
