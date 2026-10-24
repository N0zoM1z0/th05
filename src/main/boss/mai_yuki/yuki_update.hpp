// Full Yuki solo callback and real foreign near/far interfaces.
#ifndef TH05_MAIN_BOSS_MAI_YUKI_YUKI_UPDATE_HPP
#define TH05_MAIN_BOSS_MAI_YUKI_YUKI_UPDATE_HPP

#pragma codeseg BOSS_BG_TEXT main_01
void pascal near mai_yuki_bg_render(void);
extern "C" void pascal near nullfunc_near(void);
#pragma codeseg YUKI_UPDATE_TEXT main_03
extern "C" void pascal far yuki_update(void);
#include "src/main/boss/mai_yuki/b4ball.hpp"

// Complete canonical enum from generic.hpp; importing that broader header
// after mai_yuki.hpp would collide with its BOSS_W/PLAYFIELD_W macros.
enum explosion_type_t {
    ET_NONE = -1, ET_CIRCLE = 0, ET_NW_SE = 1, ET_SW_NE = 2,
    ET_HORIZONTAL = 3, ET_VERTICAL = 4,
    _explosion_type_t_FORCE_INT16 = 0x7FFF
};
extern SPPoint homing_target;
extern nearfunc_t_near bg_render_bombing_func;
// Both surviving bosses use this one DS4438 slot; shared Yuki dispatch is DS4430.
extern MaiYukiPattern boss_solo_pattern_current;
extern MaiYukiPattern yuki_solo_pattern_pair1[2];
extern MaiYukiPattern yuki_solo_pattern_pair2[2];
extern MaiYukiPattern yuki_solo_pattern_final[5];

#pragma codeseg MAIN_035_TEXT main_03
bool near yuki_solo_ring_sweep(void);
bool near yuki_solo_random_rings(void);
bool near yuki_solo_snow_cross(void);
bool near yuki_solo_speedup(void);

#pragma codeseg CIRCLE_TEXT main_01
void pascal far circles_add_growing(subpixel_t x, subpixel_t y);
#pragma codeseg BOSS_TEXT main_03
bool near boss_hittest_shots(void);
void near boss_hittest_shots_invincible(void);
void pascal near boss_score_bonus(unsigned int units);
void pascal near boss_explode_small(explosion_type_t type);
void pascal near boss_phase_next(explosion_type_t type, int next_end_hp);
void pascal near boss_defeat_update(unsigned int units);
void pascal near hud_hp_update_and_render(int hp, int total);
#pragma codeseg YUKI_UPDATE_TEXT main_03
typedef char yuki_explosion_enum_is_full_16[(sizeof(explosion_type_t) == 2) ? 1 : -1];
#endif
