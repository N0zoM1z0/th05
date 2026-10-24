// TH05 Extra midboss ABI; original target independently reviewed.
#ifndef TH05_MAIN_MIDBOSS_EXTRASTAGE_HPP
#define TH05_MAIN_MIDBOSS_EXTRASTAGE_HPP
#pragma codeseg MIDBOSSX_TEXT main_03
void pascal far midbossx_update(void);
#pragma codeseg MAI_TEXT main_01
#include "src/main/stage/setup.hpp"
#pragma codeseg MIDBOSSX_TEXT main_03
#include "src/main/boss/generic.hpp"
#include "src/main/gather/gather.hpp"
#pragma codeseg MIDBOSSX_TEXT main_03

// The original movement helper preserves its own frame and returns bool in AL.
bool pascal near midbossx_dash_update(int frame);
bool near midbossx_pattern_spread(void);
typedef bool (near *near MidbossXPattern)(void);
extern MidbossXPattern midbossx_pattern;
extern MidbossXPattern midbossx_patterns[3][2];
extern const unsigned char midbossx_dash_angles[8];
int pascal near midboss_hittest_shots_damage(subpixel_t radius_x,
    subpixel_t radius_y, int sound);
void pascal near midboss_score_bonus(unsigned int units);
void near midboss_defeat_update(void);
void pascal near hud_hp_update_and_render(int hp, int total);
void pascal near sparks_add_circle(Subpixel x, Subpixel y,
    subpixel_t radius, int count);
#pragma codeseg

typedef char midbossx_state_is_22[(sizeof(midboss_stuff_t) == 22) ? 1 : -1];
typedef char midbossx_pattern_pointer_is_2[(sizeof(MidbossXPattern) == 2) ? 1 : -1];
typedef char midbossx_pattern_array_is_12[(sizeof(midbossx_patterns) == 12) ? 1 : -1];
typedef char midbossx_gather_template_is_14[(sizeof(gather_template_t) == 14) ? 1 : -1];
#endif
