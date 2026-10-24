// Natural Yumeko helpers and complete real sword overlays. ReC98
// b6ba5b0a529edbb31efdf8c0e939263804f8ee47: th05/main/bullet/sword.hpp,
// th04/main/custom.hpp; original target independently validates every operand.
#ifndef TH05_MAIN_BOSS_YUMEKO_PATTERNS_HPP
#define TH05_MAIN_BOSS_YUMEKO_PATTERNS_HPP
#pragma codeseg B5_UPDATE_TEXT main_03
#include "src/main/stage/setup.hpp"
#include "src/main/gather/gather.hpp"
#include "src/main/bullet/cheeto.hpp"

// Reuse the accepted complete custom_t; these are the actual stage overlays.
struct sword_t {
    entity_flag_t flag;
    unsigned char angle;
    PlayfieldMotion pos;
    unsigned int twirl_time;
    uint16_t unused_1;
    int patnum_tiny;
    int decay_frame;
    int unused_2;
    SubpixelLength8 speed;
    signed char padding;
};
struct sword_template_t {
    signed char unused_1;
    unsigned char angle;
    PlayfieldPoint origin;
    int unused_2[4];
    unsigned int twirl_time;
    int unused_3;
    int patnum_tiny;
    int unused_4[2];
    SubpixelLength8 speed;
};
#define sword_template (reinterpret_cast<sword_template_t &>(custom_entities[0]))
#define swords (reinterpret_cast<sword_t *>(&custom_entities[1]))
static const int SWORD_COUNT = 63;
static const int SWORD_W = 32;
static const int SWORD_H = 32;
static const unsigned char YUMEKO_SPRITE_STILL = 180;
static const unsigned char YUMEKO_SPRITE_CHARGE = 184;
static const unsigned char YUMEKO_SPRITE_MOVE = 188;
static const unsigned char YUMEKO_NO_DECELERATE = 0x10;
static const unsigned char YUMEKO_CLOUD_BACKWARDS = 0x03;
static const unsigned char YUMEKO_BALL_RED = 48;

extern nearfunc_t_near bullet_template_tune;
#pragma codeseg SHARED
extern "C" {
    void pascal far vector2(int far &x, int far &y,
        unsigned char angle, int length);
    void pascal far snd_se_play(int sound);
}
#pragma codeseg B5_UPDATE_TEXT main_03
extern "C" void pascal near swords_add(void);
void pascal near gather_add_only_3stack(int frame, vc2 first, vc2 other);
bool pascal near yumeko_flystep_bounce(subpixel_t length, int end_frame);
void near yumeko_pattern_sword_fan(void);
void near yumeko_pattern_red_ring(void);
#pragma codeseg

typedef char yumeko_boss_is_24[(sizeof(boss_stuff_t) == 24) ? 1 : -1];
typedef char yumeko_custom_is_26[(sizeof(custom_t) == 26) ? 1 : -1];
typedef char yumeko_sword_is_26[(sizeof(sword_t) == 26) ? 1 : -1];
typedef char yumeko_sword_template_is_25[(sizeof(sword_template_t) == 25) ? 1 : -1];
typedef char yumeko_sword_pool_fits[(sizeof(sword_t) * SWORD_COUNT <=
    sizeof(custom_entities) - sizeof(custom_t)) ? 1 : -1];
typedef char yumeko_sword_template_fits[(sizeof(sword_template_t) <= sizeof(custom_t)) ? 1 : -1];
typedef char yumeko_sword_angle_at_1[(offsetof(sword_t, angle) == 1) ? 1 : -1];
typedef char yumeko_sword_pos_at_2[(offsetof(sword_t, pos) == 2) ? 1 : -1];
typedef char yumeko_sword_twirl_at_14[(offsetof(sword_t, twirl_time) == 14) ? 1 : -1];
typedef char yumeko_sword_sprite_at_18[(offsetof(sword_t, patnum_tiny) == 18) ? 1 : -1];
typedef char yumeko_sword_decay_at_20[(offsetof(sword_t, decay_frame) == 20) ? 1 : -1];
typedef char yumeko_sword_speed_at_24[(offsetof(sword_t, speed) == 24) ? 1 : -1];
typedef char yumeko_sword_unused_at_25[(offsetof(sword_t, padding) == 25) ? 1 : -1];
typedef char yumeko_template_origin_at_2[(offsetof(sword_template_t, origin) == 2) ? 1 : -1];
typedef char yumeko_template_twirl_at_14[(offsetof(sword_template_t, twirl_time) == 14) ? 1 : -1];
typedef char yumeko_template_sprite_at_18[(offsetof(sword_template_t, patnum_tiny) == 18) ? 1 : -1];
typedef char yumeko_template_speed_at_24[(offsetof(sword_template_t, speed) == 24) ? 1 : -1];
#endif
