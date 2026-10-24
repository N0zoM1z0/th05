// Natural TH05 stage1 midboss ABI. ReC98 b6ba5b0a529edbb31efdf8c0e939263804f8ee47
// th05/main/midboss/m1.cpp; original operands and calls independently reviewed.
#ifndef TH05_MAIN_MIDBOSS_STAGE1_HPP
#define TH05_MAIN_MIDBOSS_STAGE1_HPP

// Capture the real owning frame before stage/setup.hpp declares callbacks.
#pragma codeseg MIDBOSS1_TEXT main_03
void near midboss1_move(void);
void near midboss1_pattern(void);
void pascal far midboss1_update(void);
// The stage header is rendered in main_01, but RNG belongs to main_03.
unsigned int near randring2_next16(void);
unsigned int pascal near randring2_next16_and(unsigned int mask);
unsigned int pascal near randring2_next16_mod(unsigned int divisor);
#pragma codeseg MAI_TEXT main_01
#include "src/main/stage/setup.hpp"
#pragma codeseg MIDBOSS1_TEXT main_03
#include "src/main/boss/generic.hpp"
#pragma codeseg MIDBOSS1_TEXT main_03

static const subpixel_t MIDBOSS1_W = 32 * 16;
static const subpixel_t MIDBOSS1_H = 32 * 16;
static const int MIDBOSS1_HP_TOTAL = 1000;
static const int MIDBOSS1_HP_FILL_FRAMES = 128;
static const unsigned char MIDBOSS1_PHASE_EXPLODE_BIG = 254;
static const int MIDBOSS1_SPRITE = 204;
static const int MIDBOSS1_BLUE_BALL = 44;
static const unsigned char MIDBOSS1_KILL_PATTERN = 4;
static const unsigned char MIDBOSS1_SPAWN_NORMAL = 0;
static const unsigned char MIDBOSS1_SPAWN_CLOUD_FORWARDS = 2;

extern const short SinTable8[256];
extern const short CosTable8[256];
int pascal far polar(int center, int radius, int ratio);
extern BulletTemplate bullet_template;
typedef void (near pascal *near Midboss1BulletTuning)(void);
extern Midboss1BulletTuning bullet_template_tune;
extern SPPoint homing_target;
extern "C" {
    void near bullets_add_regular(void);
    void near bullets_add_special(void);
    void pascal far snd_se_play(int effect);
}
void pascal near sparks_add_circle(Subpixel center_x, Subpixel center_y,
    subpixel_t radius, int count);
int pascal near midboss_hittest_shots_damage(subpixel_t radius_x,
    subpixel_t radius_y, int sound);
void pascal near midboss_score_bonus(unsigned int units);
void near midboss_defeat_update(void);
void pascal near hud_hp_update_and_render(int hp, int total);
#pragma codeseg

typedef char midboss1_state_is_22[(sizeof(midboss_stuff_t) == 22) ? 1 : -1];
typedef char midboss1_boss_is_24[(sizeof(boss_stuff_t) == 24) ? 1 : -1];
typedef char midboss1_radius_at_8[(offsetof(midboss_stuff_t, pos) +
    offsetof(PlayfieldMotion, velocity) == 8) ? 1 : -1];
typedef char midboss1_angle_at_21[(offsetof(midboss_stuff_t, angle) == 21) ? 1 : -1];
typedef char midboss1_bullet_angle_at_20[(offsetof(boss_stuff_t, angle) == 20) ? 1 : -1];
typedef char midboss1_template_is_14[(sizeof(BulletTemplate) == 14) ? 1 : -1];
typedef char midboss1_tuning_pointer_is_2[(sizeof(bullet_template_tune) == 2) ? 1 : -1];
typedef char midboss1_trig_word_is_2[(sizeof(SinTable8[0]) == 2) ? 1 : -1];
#endif
