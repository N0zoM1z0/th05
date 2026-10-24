// Mai's complete solo state machine and its actual foreign interfaces.
#ifndef TH05_MAIN_BOSS_MAI_YUKI_MAI_UPDATE_HPP
#define TH05_MAIN_BOSS_MAI_YUKI_MAI_UPDATE_HPP

#pragma codeseg BOSS_BG_TEXT main_01
void pascal near mai_yuki_bg_render(void);
extern "C" void pascal near nullfunc_near(void);
#pragma codeseg MAI_UPDATE_TEXT main_03
extern "C" void pascal far mai_update(void);
#include "src/main/boss/mai_yuki/b4ball.hpp"
#include "src/main/boss/mai_yuki/mai_solo_patterns.hpp"
#include "src/main/bullet/laser.hpp"

// Complete canonical enum; the broader generic header conflicts with the
// existing Mai/Yuki playfield and sprite macros.
enum explosion_type_t {
    ET_NONE = -1, ET_CIRCLE = 0, ET_NW_SE = 1, ET_SW_NE = 2,
    ET_HORIZONTAL = 3, ET_VERTICAL = 4,
    _explosion_type_t_FORCE_INT16 = 0x7FFF
};
extern SPPoint homing_target;
extern nearfunc_t_near bg_render_bombing_func;
extern MaiYukiPattern boss_solo_pattern_current;
extern MaiYukiPattern mai_solo_pattern_pair_first[2];
extern MaiYukiPattern mai_solo_pattern_pair_middle[2];
extern MaiYukiPattern mai_solo_pattern_pair_final[2];

#pragma codeseg MAIN_035_TEXT main_03
// The distinct original provider at load1935E, after the accepted advanced
// attack cohort. This is not mai_solo_laser_bounce at load19250.
bool near mai_solo_laser_cycle(void);
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
#pragma codeseg MAI_UPDATE_TEXT main_03
typedef char mai_update_explosion_enum_is_16[(sizeof(explosion_type_t) == 2) ? 1 : -1];
#endif
