// Genuine complete TH05 pools used by the stage reset, never storage aliases.
// Canonical headers are unchanged; custom/gather full records below repeat
// their canonical definitions to avoid unrelated macro/entity-enum collisions.
#ifndef TH05_STAGE_STATE_INIT_HPP
#define TH05_STAGE_STATE_INIT_HPP
#include "src/main/enemy/enemy.hpp"
#include "src/main/player/shot_runtime.hpp"
#include "src/main/item/item.hpp"
#include "src/main/bullet/laser.hpp"
#include "src/main/effects/spark/lifecycle.hpp"
#include "src/main/effects/circles.hpp"

// Complete canonical definition: src/main/bullet/cheeto.hpp
struct custom_t {
    uint8_t flag;
    uint8_t angle;
    PlayfieldMotion pos;
    uint16_t val1;
    uint16_t val2;
    int sprite;
    int val3;
    int damage;
    SubpixelLength8 speed;
    signed char padding; // Actual unused scalar at byte 25 in every slot.
};
// Complete canonical definition: src/main/gather/gather.hpp
struct gather_t {
    entity_flag_t flag;
    vc_t col;
    PlayfieldMotion center;
    Subpixel radius_cur;
    int ring_points;
    unsigned char angle_cur;
    unsigned char angle_delta;
    Subpixel radius_prev;
    Subpixel radius_delta;
    BulletTemplate bullet_template;
};
// Complete canonical definition: src/main/gather/gather.hpp
struct gather_template_t {
    PlayfieldPoint center;
    PlayfieldPoint velocity;
    Subpixel radius;
    int ring_points;
    vc_t col;
    unsigned char angle_delta;
};

static const int STATE_CUSTOM_COUNT = 64;
static const int STATE_GATHER_COUNT = 16;
extern custom_t custom_entities[STATE_CUSTOM_COUNT];
extern gather_t gather_circles[STATE_GATHER_COUNT];
extern gather_template_t gather_template;

// Selected GAME5 record from th04/main/pointnum/pointnum.hpp and its BSS.
// All five digits and the actual final unused byte are retained.
typedef unsigned int upixel_t;
struct pointnum_t {
    char flag;
    unsigned char age;
    SPPoint center_cur;
    Subpixel center_prev_y;
    upixel_t width;
    unsigned char digits_lebcd[5];
    signed char padding;
};
static const int STATE_POINTNUM_WHITE_COUNT = 200;
static const int STATE_POINTNUM_YELLOW_COUNT = 80;
static const int STATE_POINTNUM_COUNT = STATE_POINTNUM_WHITE_COUNT + STATE_POINTNUM_YELLOW_COUNT;
extern pointnum_t pointnums[STATE_POINTNUM_COUNT];

// Complete same quit domain as the accepted generic-boss/runtime declarations.
enum quit_t { Q_KEEP_RUNNING = 0, Q_QUIT_TO_OP = 1, Q_NEXT_STAGE = 2 };
extern quit_t quit;
extern unsigned int hitshot_next_free_id;
extern unsigned long frames_unused;
extern unsigned int stage_frame;
extern unsigned char stage_frame_mod16;
extern unsigned char stage_frame_mod8;
extern unsigned char stage_frame_mod4;
extern unsigned char stage_frame_mod2;
extern bool palette_changed;

#pragma codeseg _TEXT
extern "C" void pascal far grc_setclip(int left, int top, int right, int bottom);
#pragma codeseg STAGE_STATE_CLEAR_TEXT main_01
// True foreign buffer helper: stack arguments are a near offset and a word
// count of DWORDs, Pascal RET4. No carry/scalar result is invented.
extern "C" void pascal near clear_dwords(void near *dest, unsigned int dwords);
#pragma codeseg STAGE_STATE_TEXT main_01
extern "C" void near stage_state_init(void);
#pragma codeseg

typedef char state_hitshots_clear_336[(sizeof(hitshots) == 336) ? 1 : -1];
typedef char state_lasers_clear_768[(sizeof(lasers) == 768) ? 1 : -1];
typedef char state_shots_clear_1152[(sizeof(shots) == 1152) ? 1 : -1];
typedef char state_enemies_clear_2048[(sizeof(enemies) == 2048) ? 1 : -1];
typedef char state_sparks_clear_1024[(sizeof(sparks) == 1024) ? 1 : -1];
typedef char state_bullets_clear_12800[(sizeof(bullets) == 12800) ? 1 : -1];
typedef char state_custom_clear_1664[(sizeof(custom_entities) == 1664) ? 1 : -1];
typedef char state_circles_clear_80[(sizeof(circles) == 80) ? 1 : -1];
typedef char state_items_clear_800[(sizeof(items) == 800) ? 1 : -1];
typedef char state_pointnums_clear_4480[(sizeof(pointnums) == 4480) ? 1 : -1];
typedef char state_gather_clear_608[(sizeof(gather_circles) == 608) ? 1 : -1];
typedef char state_custom_record_26[(sizeof(custom_t) == 26) ? 1 : -1];
typedef char state_gather_record_38[(sizeof(gather_t) == 38) ? 1 : -1];
typedef char state_gather_template_14[(sizeof(gather_template_t) == 14) ? 1 : -1];
typedef char state_pointnum_record_16[(sizeof(pointnum_t) == 16) ? 1 : -1];
typedef char state_pointnum_center_2[(offsetof(pointnum_t, center_cur) == 2) ? 1 : -1];
typedef char state_pointnum_previous_6[(offsetof(pointnum_t, center_prev_y) == 6) ? 1 : -1];
typedef char state_pointnum_width_8[(offsetof(pointnum_t, width) == 8) ? 1 : -1];
typedef char state_pointnum_digits_10[(offsetof(pointnum_t, digits_lebcd) == 10) ? 1 : -1];
typedef char state_pointnum_unused_15[(offsetof(pointnum_t, padding) == 15) ? 1 : -1];
typedef char state_quit_is_1[(sizeof(quit_t) == 1) ? 1 : -1];
typedef char state_unused_frames_is_4[(sizeof(frames_unused) == 4) ? 1 : -1];
typedef char state_clear_near_pointer_is_2[(sizeof(void near *) == 2) ? 1 : -1];
#endif
