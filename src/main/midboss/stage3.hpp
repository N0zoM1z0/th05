// TH05 stage-three midboss: real shared layouts and foreign helper interfaces.
#ifndef TH05_MAIN_MIDBOSS_STAGE3_HPP
#define TH05_MAIN_MIDBOSS_STAGE3_HPP

#pragma codeseg B4_UPDATE_TEXT main_03
#include "src/main/stage/setup.hpp"
#include "src/main/gather/gather.hpp"

#if GAME != 5 || BINARY != 'M'
#error This owner requires TH05 MAIN
#endif

enum item_type_t {
    IT_NONE = -2, IT_ENEMY_DROP_NEXT = -1, IT_POWER = 0,
    IT_POINT = 1, IT_DREAM = 2, IT_BIGPOWER = 3, IT_BOMB = 4,
    IT_1UP = 5, IT_FULLPOWER = 6, IT_COUNT
};
union BulletZapState { bool active; unsigned char frame; };
extern BulletZapState bullet_zap;
extern SPPoint homing_target;

static const int MIDBOSS3_HP_TOTAL = 1400;
static const unsigned char MIDBOSS3_PATTERNS_MAX = 12;
static const unsigned char MIDBOSS3_SPRITE_INVINCIBLE = 212;
static const unsigned char MIDBOSS3_PHASE_EXPLODE_BIG = 254;
static const unsigned char MIDBOSS3_SPRITE_EXPLODE = 4;

#pragma codeseg SHARED
extern "C" void pascal far snd_se_play(int sound);
#pragma codeseg B4_UPDATE_TEXT main_03
void near midboss3_pattern_1(void);
void near midboss3_pattern_2(void);
void near midboss3_pattern_3(void);
int pascal near midboss_hittest_shots_damage(
    subpixel_t radius_x, subpixel_t radius_y, int sound);
void pascal near midboss_score_bonus(unsigned int units);
void near midboss_defeat_update(void);
void pascal near hud_hp_update_and_render(int hp, int total);
void pascal near sparks_add_circle(Subpixel x, Subpixel y,
    subpixel_t radius, int count);
void pascal near items_add(subpixel_t x, subpixel_t y, item_type_t type);
void pascal far midboss3_update(void);

inline void stage3_midboss_hittest_shots(subpixel_t radius_x, subpixel_t radius_y) {
    midboss.damage_this_frame = midboss_hittest_shots_damage(radius_x, radius_y, 4);
    midboss.hp -= midboss.damage_this_frame;
}

#endif
