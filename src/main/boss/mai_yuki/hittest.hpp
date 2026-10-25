// Complete canonical Boss/Point state and real shot-hit wrapper interfaces.
#ifndef TH05_MAIN_MAI_YUKI_HITTEST_HPP
#define TH05_MAIN_MAI_YUKI_HITTEST_HPP

#pragma codeseg SHOT_HIT_TEXT main_01
int far shots_hittest(void);
#pragma codeseg MAIN_035_TEXT main_03
#include "src/main/boss/mai_yuki.hpp"

extern bool shots_hittest_against_boss;
extern SPPoint shot_hitbox_center;
extern SPPoint shot_hitbox_radius;

#pragma codeseg SHARED
extern "C" void pascal far snd_se_play(int sound);
#pragma codeseg BOSS_TEXT main_03
bool near boss_hittest_shots(void);
#pragma codeseg MAIN_035_TEXT main_03
int pascal near yuki_hittest_shots_damage(subpixel_t radius_x,
    subpixel_t radius_y, int effect);
unsigned char near mai_yuki_hittest_shots(void);

enum MaiYukiHitResult {
    MY_HIT_NONE = 0,
    MY_HIT_MAI_DEFEATED = 1,
    MY_HIT_YUKI_DEFEATED = 2
};

typedef char my_hit_boss_is_full_24[(sizeof(boss_stuff_t) == 24) ? 1 : -1];
typedef char my_hit_point_is_full_4[(sizeof(SPPoint) == 4) ? 1 : -1];
typedef char my_hit_damage_is_1[(sizeof(boss2.damage_this_frame) == 1) ? 1 : -1];

#endif
