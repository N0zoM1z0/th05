// Real TH05 stage-four midboss interfaces and complete canonical layouts.
#ifndef TH05_MAIN_MIDBOSS_STAGE4_HPP
#define TH05_MAIN_MIDBOSS_STAGE4_HPP

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
extern nearfunc_t_near bullet_template_tune;

static const int MIDBOSS4_HP_TOTAL = 1100;
static const unsigned char MIDBOSS4_SPRITE_STILL = 208;
static const unsigned char MIDBOSS4_SPRITE_CAST = 212;
static const unsigned char MIDBOSS4_PHASE_EXPLODE_BIG = 254;
static const unsigned char MIDBOSS4_SPRITE_EXPLODE = 4;
static const unsigned char MIDBOSS4_PATTERN_BUDGET = 16;
static const unsigned char MIDBOSS4_CLOUD_FORWARDS = 0x02;
static const unsigned char MIDBOSS4_NO_DECELERATE = 0x10;
static const unsigned char MIDBOSS4_BALL_BLUE = 44;
static const unsigned char MIDBOSS4_V_RED = 84;
static const unsigned char MIDBOSS4_V_BLUE = 116;

#pragma codeseg SHARED
extern "C" void pascal far snd_se_play(int sound);
#pragma codeseg B4_UPDATE_TEXT main_03
unsigned int pascal near randring2_next16_mod(unsigned int divisor);
extern "C" void near bullets_add_regular_fixedspeed(void);

// The preceding real transition helper returns its completion in AL.
bool near midboss4_pattern_transition(void);
void near midboss4_pattern_random_clouds(void);
void near midboss4_pattern_spiral_rings(void);
void near midboss4_pattern_aimed_stacks(void);
int pascal near midboss_hittest_shots_damage(
    subpixel_t radius_x, subpixel_t radius_y, int sound);
void pascal near midboss_score_bonus(unsigned int units);
void near midboss_defeat_update(void);
void pascal near hud_hp_update_and_render(int hp, int total);
void pascal near sparks_add_circle(Subpixel x, Subpixel y,
    subpixel_t radius, int count);
void pascal near items_add(subpixel_t x, subpixel_t y, item_type_t type);
void pascal far midboss4_update(void);

inline void stage4_midboss_hittest_shots(subpixel_t radius_x, subpixel_t radius_y) {
    midboss.damage_this_frame = midboss_hittest_shots_damage(radius_x, radius_y, 4);
    midboss.hp -= midboss.damage_this_frame;
}

typedef char stage4_spread_group_is_four_bytes[
    ((offsetof(BulletTemplate, stack_speed_delta) - offsetof(BulletTemplate, spread)) == 3) ? 1 : -1];

#endif
