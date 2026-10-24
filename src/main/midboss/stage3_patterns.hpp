// Natural stage-three movement/pattern prefix, with the frozen callback ABI.
#ifndef TH05_MAIN_MIDBOSS_STAGE3_PATTERNS_HPP
#define TH05_MAIN_MIDBOSS_STAGE3_PATTERNS_HPP

// The real rank selector is far in main_01. Its first declaration must retain
// that frame before the shared stage header repeats its canonical interface.
#pragma codeseg MIDBOSS3_PAT_MAIN01_CONTEXT main_01
extern "C" int pascal far select_for_rank(int easy, int normal, int hard, int lunatic);
#pragma codeseg B4_UPDATE_TEXT main_03
#include "src/main/midboss/stage3.hpp"
#include "src/main/player/player.hpp"

#pragma codeseg B4_UPDATE_TEXT main_03
void near midboss3_reposition(void);
void near midboss3_gather_charge(void);
void pascal near gather_add_only_3stack(int frame, vc2 first, vc2 other);
extern nearfunc_t_near bullet_template_tune;

static const unsigned char MIDBOSS3_PAT_BALL_BLUE = 44;
static const unsigned char MIDBOSS3_PAT_BALL_RED = 48;
static const unsigned char MIDBOSS3_PAT_DIAMOND_BLUE = 52;
static const unsigned char MIDBOSS3_SPAWN_CLOUD_FORWARDS = 0x02;
static const unsigned char MIDBOSS3_SPAWN_NO_DECELERATE = 0x10;

inline unsigned char midboss3_speed(float value) {
    return static_cast<unsigned char>(value * 16);
}
// Real reference BulletTemplate packed setters, applied to its asserted
// adjacent semantic fields without changing the canonical class declaration.
inline void midboss3_set_stack(unsigned char count, float speed_delta) {
    reinterpret_cast<uint16_t &>(bullet_template.stack) =
        count | (midboss3_speed(speed_delta) << 8);
}
inline void midboss3_set_spread_stack(unsigned char count, unsigned char delta,
    unsigned char stack, float speed_delta) {
    reinterpret_cast<uint32_t &>(bullet_template.spread) =
        (count | (delta << 8) | (static_cast<uint32_t>(stack) << 16) |
        (static_cast<uint32_t>(midboss3_speed(speed_delta)) << 24));
}
inline void midboss3_set_spread_for_rank(unsigned char count_e, unsigned char delta_e,
    unsigned char count_n, unsigned char delta_n, unsigned char count_h,
    unsigned char delta_h, unsigned char count_l, unsigned char delta_l) {
    reinterpret_cast<uint16_t &>(bullet_template.spread) = select_for_rank(
        count_e | (delta_e << 8), count_n | (delta_n << 8),
        count_h | (delta_h << 8), count_l | (delta_l << 8));
}

#endif
