// Seven complete Yuki solo attacks; canonical shared interfaces stay frozen.
#ifndef TH05_MAIN_BOSS_MAI_YUKI_YUKI_PATTERNS_HPP
#define TH05_MAIN_BOSS_MAI_YUKI_YUKI_PATTERNS_HPP
#pragma codeseg MAIN_035_TEXT main_03
#include "src/main/boss/mai_yuki/b4ball.hpp"
#pragma codeseg MAIN_035_TEXT main_03
// Full canonical definition from accepted bullet/update.hpp.
union BulletSpecialState {
    unsigned char turns_max;
    SubpixelLength8 speed_delta;
};
extern BulletSpecialState bullet_special;
extern unsigned char rank;
static const unsigned char YUKI_SOLO_SPRITE_FIRE = 208;
static const unsigned char YUKI_SOLO_SMALL_BALL_RED = 50;
static const unsigned char YUKI_SOLO_BALL_RED = 48;
static const unsigned char YUKI_SOLO_VECTOR_RED = 84;
bool near yuki_solo_ring_sweep(void);
bool near yuki_solo_random_spreads(void);
bool near yuki_solo_random_rings(void);
bool near yuki_solo_snow_fan(void);
bool near yuki_solo_snow_cross(void);
bool near yuki_solo_vector_stacks(void);
bool near yuki_solo_speedup(void);
#pragma codeseg
typedef char yuki_solo_special_is_1[(sizeof(BulletSpecialState) == 1) ? 1 : -1];
#endif
