// Complete Yumeko callback interfaces; accepted layouts stay unchanged.
#ifndef TH05_MAIN_BOSS_YUMEKO_UPDATE_HPP
#define TH05_MAIN_BOSS_YUMEKO_UPDATE_HPP
// These genuine near rendering pointers use main_01, before setup repeats them.
#pragma codeseg YUMEKO_UPDATE_MAIN01_TEXT main_01
void pascal near yumeko_bg_render(void);
extern "C" {
    void pascal near nullfunc_near(void);
    void pascal near swords_render(void);
}
#pragma codeseg B5_UPDATE_TEXT main_03
void pascal far yumeko_update(void);
void near yumeko_pattern_final_ring(void);
#include "src/main/boss/yumeko/phase_patterns.hpp"
#pragma codeseg B5_UPDATE_TEXT main_03

// Complete canonical definitions verbatim from accepted bullet/update.hpp.
// Preserve one external object type across independent TUs, without reduced views.
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
extern "C" {
    int pascal far super_convert_tiny(int num);
    void near bullets_add_special_fixedspeed(void);
    void pascal near swords_update(void);
}

typedef void (near *near yumeko_pattern_func_t)(void);
extern yumeko_pattern_func_t yumeko_pattern;
extern yumeko_pattern_func_t yumeko_patterns_phase2[4];
extern yumeko_pattern_func_t yumeko_patterns_phase5[4];
void near yumeko_pattern_laser_swords(void); // Real foreign phase-seven body.
void near yumeko_pattern_sword_sweep(void); // Real foreign phase-eight body.

#pragma codeseg BOSS_TEXT main_03
bool near boss_hittest_shots(void);
void near boss_hittest_shots_invincible(void);
void pascal near boss_score_bonus(unsigned int units);
void pascal near boss_phase_next(explosion_type_t type, int next_end_hp);
void pascal near boss_defeat_update(unsigned int bonus_units);
void pascal near hud_hp_update_and_render(int hp, int total);
#pragma codeseg

typedef char yumeko_update_special_is_1[(sizeof(BulletSpecialState) == 1) ? 1 : -1];
typedef char yumeko_update_angle_is_1[(sizeof(bullet_special_angle_t) == 1) ? 1 : -1];
typedef char yumeko_update_pattern_is_2[(sizeof(yumeko_pattern_func_t) == 2) ? 1 : -1];
typedef char yumeko_update_pattern_bank_is_8[(sizeof(yumeko_patterns_phase2) == 8) ? 1 : -1];
#endif
