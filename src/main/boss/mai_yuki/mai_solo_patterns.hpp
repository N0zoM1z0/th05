// Mai's independent phase patterns, retaining complete shared game types.
#ifndef TH05_MAI_SOLO_PATTERNS_HPP
#define TH05_MAI_SOLO_PATTERNS_HPP
#include "src/main/boss/mai_yuki/initial_patterns.hpp"

// Full canonical ODR definitions from the accepted bullet updater.
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
extern unsigned char rank;

#pragma codeseg MAIN_035_TEXT main_03
bool near mai_solo_widening_fans(void);
bool near mai_solo_turning_stacks(void);
void near mai_solo_rotating_fans(void);
#endif
