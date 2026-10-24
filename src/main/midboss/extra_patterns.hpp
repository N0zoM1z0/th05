// Natural Extra midboss movement and pattern interfaces.
#ifndef TH05_MAIN_MIDBOSS_EXTRA_PATTERNS_HPP
#define TH05_MAIN_MIDBOSS_EXTRA_PATTERNS_HPP
#pragma codeseg MIDBOSSX_TEXT main_03
#include "src/shared/geometry.hpp"
// First declarations preserve the genuine main_03 near frame before setup.
unsigned int pascal near randring2_next16_and(unsigned int mask);
extern "C" void pascal near vector2_near(SPPoint near &ret,
    unsigned char angle, subpixel_t length);
#include "src/main/midboss/extra.hpp"
#pragma codeseg MIDBOSSX_TEXT main_03
bool near midbossx_pattern_wait(void);
bool near midbossx_pattern_random(void);
bool near midbossx_pattern_decelerate(void);
extern "C" {
    void near bullets_add_regular(void);
    void near bullets_add_special(void);
}
extern unsigned char page_back;
// Complete canonical definitions verbatim from accepted bullet/update.hpp.
// Identical ODR definitions in these independent TUs preserve real ABI;
// future consolidation requires a separate affected-evidence replay.
union bullet_special_angle_t {
    unsigned char turn_by;
    char target;
    signed char v;
};
union BulletSpecialState {
    unsigned char turns_max;
    SubpixelLength8 speed_delta;
};
extern BulletSpecialState bullet_special;
extern bullet_special_angle_t bullet_template_special_angle;
#pragma codeseg
typedef char midbossx_special_state_is_1[(sizeof(BulletSpecialState) == 1) ? 1 : -1];
typedef char midbossx_special_angle_is_1[(sizeof(bullet_special_angle_t) == 1) ? 1 : -1];
#endif
