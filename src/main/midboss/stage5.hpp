// TH05 stage-five midboss state-machine interfaces; all helper bodies external.
#ifndef TH05_MAIN_MIDBOSS_STAGE5_HPP
#define TH05_MAIN_MIDBOSS_STAGE5_HPP

#pragma codeseg MAIN_036_TEXT main_03
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

// Real two-byte near CODE pointers, with the completion truth value in AL.
// The original consumer calls the selected pattern and tests AL directly.
typedef bool (near *near midboss5_pattern_func_t)(void);
extern midboss5_pattern_func_t midboss5_pattern_func;
extern const midboss5_pattern_func_t MIDBOSS5_PATTERNS[3];

typedef char midboss5_pattern_pointer_is_2[
    (sizeof(midboss5_pattern_func_t) == 2) ? 1 : -1];
typedef char midboss5_pattern_table_is_6[
    (sizeof(MIDBOSS5_PATTERNS) == 6) ? 1 : -1];

static const int MIDBOSS5_HP_TOTAL = 1550;
static const unsigned char MIDBOSS5_PATTERNS_MAX = 16;
static const unsigned char MIDBOSS5_PHASE_EXPLODE_BIG = 254;
static const unsigned char MIDBOSS5_SPRITE_EXPLODE = 4;

#pragma codeseg SHARED
extern "C" void pascal far snd_se_play(int sound);
#pragma codeseg MAIN_036_TEXT main_03
bool near midboss5_flystep(void);
void near midboss5_pattern_update(void);
bool near midboss5_pattern_blue_spread(void);
int pascal near midboss_hittest_shots_damage(
    subpixel_t radius_x, subpixel_t radius_y, int sound);
void pascal near midboss_score_bonus(unsigned int units);
void near midboss_defeat_update(void);
void pascal near hud_hp_update_and_render(int hp, int total);
void pascal near sparks_add_circle(Subpixel x, Subpixel y,
    subpixel_t radius, int count);
void pascal near items_add(subpixel_t x, subpixel_t y, item_type_t type);
void pascal far midboss5_update(void);

inline void stage5_midboss_hittest_shots(subpixel_t radius_x, subpixel_t radius_y) {
    midboss.damage_this_frame = midboss_hittest_shots_damage(radius_x, radius_y, 4);
    midboss.hp -= midboss.damage_this_frame;
}

#endif
