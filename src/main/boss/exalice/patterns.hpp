// Declarations for EX-Alice's charged attacks.
#ifndef TH05_MAIN_BOSS_EXALICE_PATTERNS_HPP
#define TH05_MAIN_BOSS_EXALICE_PATTERNS_HPP
#pragma codeseg EXALICE_PAT_TEXT main_03
#include "src/main/stage/setup.hpp"
#include "src/main/bullet/template.hpp"

// Same definition as in bullet/update.hpp, which can't be included here: its
// HUD part defines its own to_sp().
union BulletSpecialState {
    unsigned char turns_max;
    SubpixelLength8 speed_delta;
};
extern BulletSpecialState bullet_special;
extern BulletTemplate bullet_template;
static const unsigned char EXALICE_PAT_V_RED = 84;

#pragma codeseg SHARED
extern "C" void pascal far snd_se_play(int sound);
#pragma codeseg EXALICE_PAT_TEXT main_03
void pascal near gather_add_only_3stack(int frame,
    unsigned int first_color, unsigned int other_color);
extern "C" void near bullets_add_regular(void);
extern "C" void near bullets_add_special(void);
typedef bool (near *near exalice_pattern_t)(void);
extern exalice_pattern_t exalice_pattern;
bool near exalice_charge_update(void);
bool near exalice_pattern_random_fan(void);
bool near exalice_pattern_turning_rings(void);

inline void exalice_set_spread(unsigned char count, unsigned char delta) {
    reinterpret_cast<uint16_t &>(bullet_template.spread) = count | (delta << 8);
}
#endif
