// Complete TH05 custom-ball ABI, from ReC98 b6ba5b0a
// th05/main/bullet/b4ball.hpp and actual original allocator/update operands.
#ifndef TH05_MAIN_BOSS_MAI_YUKI_B4BALL_HPP
#define TH05_MAIN_BOSS_MAI_YUKI_B4BALL_HPP
#pragma codeseg MAIN_035_TEXT main_03
#include "src/main/boss/mai_yuki/initial_patterns.hpp"
#include "src/main/bullet/cheeto.hpp"
#pragma codeseg MAIN_035_TEXT main_03

typedef int bool16;
static const int B4BALL_COUNT = 63;
static const int B4BALL_W = 32;
static const int B4BALL_H = 32;
struct b4ball_t {
    unsigned char flag;
    unsigned char angle;
    PlayfieldMotion pos;
    unsigned int age;
    bool16 revenge;
    int patnum_tiny_base;
    int hp;
    int damaged_this_frame;
    SubpixelLength8 speed;
    signed char padding;
};
struct b4ball_template_t {
    signed char _unused_1;
    unsigned char angle;
    PlayfieldPoint origin;
    int _unused_2[5];
    bool16 revenge;
    int patnum_tiny_base;
    int hp;
    int _unused_3;
    SubpixelLength8 speed;
};
#define b4ball_template (reinterpret_cast<b4ball_template_t &>(custom_entities[0]))
#define b4balls (reinterpret_cast<b4ball_t *>(&custom_entities[1]))

#pragma codeseg YUKI_SOLO_RENDER_TEXT main_01
extern "C" void pascal near b4balls_render(void);
#pragma codeseg MAIN_035_TEXT main_03
extern "C" {
    void pascal near b4balls_reset(void);
    void pascal near b4balls_add(void);
    void pascal near b4balls_update(void);
}
#pragma codeseg

typedef char b4ball_bool16_is_2[(sizeof(bool16) == 2) ? 1 : -1];
typedef char b4ball_custom_is_26[(sizeof(custom_t) == 26) ? 1 : -1];
typedef char b4ball_record_is_26[(sizeof(b4ball_t) == 26) ? 1 : -1];
typedef char b4ball_template_is_25[(sizeof(b4ball_template_t) == 25) ? 1 : -1];
typedef char b4ball_template_fits[(sizeof(b4ball_template_t) <= sizeof(custom_t)) ? 1 : -1];
typedef char b4ball_pool_fits[(sizeof(b4ball_t) * B4BALL_COUNT ==
    sizeof(custom_entities) - sizeof(custom_t)) ? 1 : -1];
typedef char b4ball_pos_at_2[(offsetof(b4ball_t, pos) == 2) ? 1 : -1];
typedef char b4ball_age_at_14[(offsetof(b4ball_t, age) == 14) ? 1 : -1];
typedef char b4ball_revenge_at_16[(offsetof(b4ball_t, revenge) == 16) ? 1 : -1];
typedef char b4ball_sprite_at_18[(offsetof(b4ball_t, patnum_tiny_base) == 18) ? 1 : -1];
typedef char b4ball_hp_at_20[(offsetof(b4ball_t, hp) == 20) ? 1 : -1];
typedef char b4ball_damage_at_22[(offsetof(b4ball_t, damaged_this_frame) == 22) ? 1 : -1];
typedef char b4ball_speed_at_24[(offsetof(b4ball_t, speed) == 24) ? 1 : -1];
typedef char b4ball_unused_at_25[(offsetof(b4ball_t, padding) == 25) ? 1 : -1];
typedef char b4ball_origin_at_2[(offsetof(b4ball_template_t, origin) == 2) ? 1 : -1];
typedef char b4ball_template_revenge_at_16[(offsetof(b4ball_template_t, revenge) == 16) ? 1 : -1];
typedef char b4ball_template_sprite_at_18[(offsetof(b4ball_template_t, patnum_tiny_base) == 18) ? 1 : -1];
typedef char b4ball_template_hp_at_20[(offsetof(b4ball_template_t, hp) == 20) ? 1 : -1];
typedef char b4ball_template_speed_at_24[(offsetof(b4ball_template_t, speed) == 24) ? 1 : -1];
#endif
