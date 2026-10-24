// Natural stage-five movement/pattern prefix. Reuse the frozen callback ABI.
#ifndef TH05_MAIN_MIDBOSS_STAGE5_PATTERNS_HPP
#define TH05_MAIN_MIDBOSS_STAGE5_PATTERNS_HPP

#pragma codeseg MAIN_036_TEXT main_03
#include "src/main/midboss/stage5.hpp"
#include "src/main/player/player.hpp"

#pragma codeseg MAIN_036_TEXT main_03
bool near midboss5_pattern_green_rings(void);
bool near midboss5_pattern_aimed_stacks(void);
void pascal near gather_add_only_3stack(int frame, vc2 first, vc2 other);

static const unsigned char MIDBOSS5_PAT_BULLET_V_BLUE = 116;
static const unsigned char MIDBOSS5_PAT_BULLET_D_GREEN = 68;
static const unsigned char MIDBOSS5_SPRITE_CHARGE = 212;
static const unsigned char MIDBOSS5_SPRITE_SHOOT_LAST = 219;
static const unsigned char MIDBOSS5_SPAWN_NO_DECELERATE = 0x10;
static const unsigned char MIDBOSS5_SPAWN_CLOUD_FORWARDS = 0x02;

// The genuine BulletTemplate setters combine its adjacent semantic fields,
// as in ReC98 bullet.hpp and the accepted Sara owner. They emit no opcodes.
inline unsigned char midboss5_speed(float value) {
    return static_cast<unsigned char>(value * 16);
}
inline void midboss5_set_spread(unsigned char count, unsigned char delta) {
    reinterpret_cast<uint16_t &>(bullet_template.spread) = count | (delta << 8);
}
inline void midboss5_set_spread_stack(unsigned char count, unsigned char delta,
    unsigned char stack, float speed_delta) {
    reinterpret_cast<uint32_t &>(bullet_template.spread) =
        (count | (delta << 8) | (static_cast<uint32_t>(stack) << 16) |
        (static_cast<uint32_t>(midboss5_speed(speed_delta)) << 24));
}

#endif
