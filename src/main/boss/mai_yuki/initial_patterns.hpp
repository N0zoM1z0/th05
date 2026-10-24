// Natural shared Mai/Yuki charge dispatch and the first Mai attack patterns.
#ifndef TH05_MAIN_BOSS_MAI_YUKI_INITIAL_PATTERNS_HPP
#define TH05_MAIN_BOSS_MAI_YUKI_INITIAL_PATTERNS_HPP

#pragma codeseg MAIN_035_TEXT main_03
#include "src/main/boss/mai_yuki.hpp"
#include "src/main/stage/setup.hpp"
#include "src/main/gather/gather.hpp"

#if GAME != 5 || BINARY != 'M'
#error This owner requires TH05 MAIN
#endif

// Real no-argument near CODE callbacks, with completion truth in AL.
typedef bool (near *near MaiYukiPattern)(void);
extern MaiYukiPattern mai_pattern_current;
extern MaiYukiPattern yuki_pattern_current;
extern nearfunc_t_near bullet_template_tune;
typedef char mai_yuki_pattern_pointer_is_2[(sizeof(MaiYukiPattern) == 2) ? 1 : -1];

static const unsigned char MY_SPRITE_CHARGE = 183;
static const unsigned char MY_SPRITE_FIRE = 184;
static const unsigned char MY_SPAWN_CLOUD_FORWARDS = 0x02;
static const unsigned char MY_SPAWN_NO_DECELERATE = 0x10;
static const unsigned char MY_PAT_CROSS_BLUE = 47;
static const unsigned char MY_PAT_SMALL_BALL_BLUE = 46;
static const unsigned char MY_PAT_V_BLUE = 116;

#pragma codeseg SHARED
extern "C" void pascal far snd_se_play(int sound);
#pragma codeseg MAIN_035_TEXT main_03
void pascal near gather_add_only_3stack(int frame, vc2 first, vc2 other);
extern "C" {
    void near bullets_add_regular_fixedspeed(void);
    void near bullets_add_special_fixedspeed(void);
}
void near mai_pattern_update(void);
void near yuki_pattern_update(void);
bool near mai_pattern_random_crosses(void);
bool near mai_pattern_turning_fan(void);
bool near mai_pattern_sweeping_pellets(void);
bool near mai_pattern_small_ball_fan(void);

inline unsigned char mai_yuki_speed(float value) {
    return static_cast<unsigned char>(value * 16);
}
inline void mai_yuki_set_spread(unsigned char count, unsigned char delta) {
    reinterpret_cast<uint16_t &>(bullet_template.spread) = count | (delta << 8);
}
inline void mai_yuki_set_stack(unsigned char count, float speed_delta) {
    reinterpret_cast<uint16_t &>(bullet_template.stack) =
        count | (mai_yuki_speed(speed_delta) << 8);
}

#endif
