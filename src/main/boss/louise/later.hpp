// Declarations for Louise's later patterns.
#ifndef TH05_MAIN_BOSS_LOUISE_LATER_HPP
#define TH05_MAIN_BOSS_LOUISE_LATER_HPP

#include "src/main/boss/louise/patterns.hpp"
#include "src/main/bullet/laser.hpp"
#pragma codeseg B4_UPDATE_TEXT main_03

// Same as in src/main/bullet/update.hpp, which declares too much else to be
// included here.
union BulletSpecialState {
    unsigned char turns_max;
    SubpixelLength8 speed_delta;
};
union bullet_special_angle_t {
    unsigned char turn_by;
    char target;
    signed char v;
};
extern BulletSpecialState bullet_special;
extern bullet_special_angle_t bullet_template_special_angle;
typedef char louise_special_state_is_1[(sizeof(BulletSpecialState) == 1) ? 1 : -1];
typedef char louise_special_angle_is_1[(sizeof(bullet_special_angle_t) == 1) ? 1 : -1];

static const unsigned char LOUISE_SPAWN_CLOUD_BACKWARDS = 3;

void near louise_pattern_mirrored_fans(void);
void near louise_pattern_sweeping_lasers(void);
void near louise_pattern_turning_rings(void);
void near louise_pattern_aimed_pellets(void);

inline void louise_set_spread_stack(unsigned char count, unsigned char delta,
    unsigned char stack, float speed_delta) {
    reinterpret_cast<uint32_t &>(bullet_template.spread) =
        (count | (delta << 8) | (static_cast<uint32_t>(stack) << 16) |
        (static_cast<uint32_t>(louise_speed(speed_delta)) << 24));
}

#endif
