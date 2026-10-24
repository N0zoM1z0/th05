// Natural Louise charging and alternating first-phase bullet patterns.
#ifndef TH05_MAIN_BOSS_LOUISE_PATTERNS_HPP
#define TH05_MAIN_BOSS_LOUISE_PATTERNS_HPP

#pragma codeseg LOUISE_MAIN01_CONTEXT main_01
extern "C" int pascal far select_for_rank(int easy, int normal, int hard, int lunatic);
#pragma codeseg B4_UPDATE_TEXT main_03
#include "src/main/stage/setup.hpp"
#include "src/main/gather/gather.hpp"

#if GAME != 5 || BINARY != 'M'
#error This owner requires TH05 MAIN
#endif

// The complete original helper returns these four distinct states in AL.
// The state machine is recovered here together with both actual consumers.
enum louise_charge_state_t {
    LOUISE_CHARGE_INACTIVE = 0,
    LOUISE_CHARGE_INITIALIZE = 1,
    LOUISE_CHARGE_FIRE = 2,
    LOUISE_CHARGE_FINISH = 3,
    _louise_charge_state_t_FORCE_UINT8 = 0xff
};
typedef char louise_charge_state_is_byte[(sizeof(louise_charge_state_t) == 1) ? 1 : -1];

extern nearfunc_t_near bullet_template_tune;
static const unsigned char LOUISE_SPAWN_CLOUD_FORWARDS = 0x02;
static const unsigned char LOUISE_SPAWN_NO_DECELERATE = 0x10;
static const unsigned char LOUISE_PAT_BALL_BLUE = 44;
static const unsigned char LOUISE_PAT_V_RED = 84;
static const unsigned char LOUISE_SPRITE_STILL = 180;
static const unsigned char LOUISE_SPRITE_CHARGE = 184;
static const unsigned char LOUISE_SPRITE_FIRE = 188;

#pragma codeseg SHARED
extern "C" void pascal far snd_se_play(int sound);
#pragma codeseg B4_UPDATE_TEXT main_03
void pascal near gather_add_only_3stack(int frame, vc2 first, vc2 other);
louise_charge_state_t pascal near louise_charge_update(int end_frame);
void near louise_pattern_blue_spreads(void);
void near louise_pattern_red_stacks(void);

inline unsigned char louise_speed(float value) {
    return static_cast<unsigned char>(value * 16);
}
inline void louise_set_spread(unsigned char count, unsigned char delta) {
    reinterpret_cast<uint16_t &>(bullet_template.spread) = count | (delta << 8);
}
inline void louise_set_stack_for_rank(unsigned char count_e, float speed_e,
    unsigned char count_n, float speed_n, unsigned char count_h, float speed_h,
    unsigned char count_l, float speed_l) {
    reinterpret_cast<uint16_t &>(bullet_template.stack) = select_for_rank(
        count_e | (louise_speed(speed_e) << 8), count_n | (louise_speed(speed_n) << 8),
        count_h | (louise_speed(speed_h) << 8), count_l | (louise_speed(speed_l) << 8));
}

#endif
