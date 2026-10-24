// TH05 stage-two orbit and attack interfaces, original-target reviewed.
#ifndef TH05_MAIN_MIDBOSS_STAGE2_PATTERNS_HPP
#define TH05_MAIN_MIDBOSS_STAGE2_PATTERNS_HPP
#pragma codeseg B4_UPDATE_TEXT main_03
#include "src/main/midboss/stage2.hpp"
#pragma codeseg SHARED
extern "C" void pascal far vector2_at(SPPoint near &ret,
    subpixel_t origin_x, subpixel_t origin_y, subpixel_t length, int angle);
#pragma codeseg B4_UPDATE_TEXT main_03
extern unsigned char stage_frame_mod16;
extern unsigned char stage_frame_mod4;
typedef void (near pascal *near Midboss2BulletTuning)(void);
extern Midboss2BulletTuning bullet_template_tune;
extern "C" void near bullets_add_regular(void);
#pragma codeseg
typedef char midboss2_orbit_center_is_4[(sizeof(midboss2_orbit_center) == 4) ? 1 : -1];
typedef char midboss2_tuning_pointer_is_2[(sizeof(Midboss2BulletTuning) == 2) ? 1 : -1];
#endif
