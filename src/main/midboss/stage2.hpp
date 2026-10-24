// TH05 stage-two midboss update: complete real interfaces, no helper bodies.
#ifndef TH05_MAIN_MIDBOSS_STAGE2_HPP
#define TH05_MAIN_MIDBOSS_STAGE2_HPP

#pragma codeseg B4_UPDATE_TEXT main_03
#include "src/main/stage/setup.hpp"
#include "src/main/bullet/template.hpp"

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
extern unsigned char bullet_clear_time;
extern BulletTemplate bullet_template;
extern SPPoint homing_target;
static const int MIDBOSS2_HP_TOTAL = 1400;
static const unsigned char MIDBOSS2_SPRITE_DAMAGED = 206;
static const unsigned char MIDBOSS2_PHASE_EXPLODE_BIG = 254;
static const unsigned char MIDBOSS2_SPRITE_EXPLODE = 4;
// This is the full four-byte point used by the orbit movement helper.
extern SPPoint midboss2_orbit_center;

#pragma codeseg SHARED
extern "C" {
    void pascal far snd_se_play(int sound);
    void pascal far vector2_between_plus(int x1, int y1, int x2, int y2,
        unsigned char plus_angle, int &ret_x, int &ret_y, int length);
}
#pragma codeseg B4_UPDATE_TEXT main_03
void near midboss2_move(void);
void near midboss2_pattern(void);
void near midboss2_pattern_final(void);
int pascal near midboss_hittest_shots_damage(
    subpixel_t radius_x, subpixel_t radius_y, int sound);
void pascal near midboss_score_bonus(unsigned int units);
void near midboss_defeat_update(void);
void pascal near hud_hp_update_and_render(int hp, int total);
void pascal near sparks_add_circle(Subpixel x, Subpixel y,
    subpixel_t radius, int count);
void pascal near items_add(subpixel_t x, subpixel_t y, item_type_t type);
void pascal far midboss2_update(void);

inline void stage2_midboss_hittest_shots(subpixel_t radius_x, subpixel_t radius_y) {
    midboss.damage_this_frame = midboss_hittest_shots_damage(radius_x, radius_y, 4);
    midboss.hp -= midboss.damage_this_frame;
}

#endif
