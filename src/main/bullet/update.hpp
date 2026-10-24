// TH05 bullet update ABI, adapted from natural C++ in nmlgc/ReC98
// b6ba5b0a529edbb31efdf8c0e939263804f8ee47: th04/main/bullet/bullet.hpp,
// pellet_r.hpp, clearzap.hpp, spark.hpp, and th04/main/item/item.hpp.
#ifndef TH05_MAIN_BULLET_UPDATE_HPP
#define TH05_MAIN_BULLET_UPDATE_HPP

#include "src/main/bullet/template.hpp"
#include "src/main/player/reimu.hpp"
#include "src/main/player/player.hpp"
// The popup callback is a near address in main_01, even when assigned by
// main_03 update code. Its first declaration must retain the actual frame.
#pragma codeseg HUD_OVRL_TEXT main_01
void pascal near overlay_popup_update_and_render(void);
#pragma codeseg
#include "src/main/hud/overlay.hpp"

#define BULLET_CLOUD_CELS 4
#define BULLET_DECAY_CELS 4
#define BULLET_ZAP_CELS 4
#define BULLET_D_CELS 16
#define BULLET_V_CELS 32
#define PELLET_COUNT 180
#define BULLET16_COUNT 220
#define BULLET_COUNT (PELLET_COUNT + BULLET16_COUNT)
#define PELLET_W 8
#define PELLET_H 8
#define BULLET16_W 16
#define BULLET16_H 16
#define BMF_DECELERATE_FRAMES 32
static const int BMF_DECAY_FRAMES_PER_CEL = 4;

enum bullet_spawn_flag_t {
    BSF_GRAZEABLE = 0, BSF_GRAZED = 1, BSF_ACTIVE = 2,
    BSF_CLOUD_BACKWARDS = 3, BSF_CLOUD_FORWARDS = 4,
    BSF_CLOUD_END = (BSF_CLOUD_FORWARDS + BULLET_CLOUD_CELS * 4),
    _bullet_spawn_flag_t_FORCE_UINT8 = 0xFF
};
enum bullet_move_flag_t {
    BMF_DECELERATE = 0, BMF_SPECIAL = 1, BMF_REGULAR = 2,
    BMF_DECAY = 4,
    BMF_DECAY_END = (BMF_DECAY + BULLET_DECAY_CELS * BMF_DECAY_FRAMES_PER_CEL),
    _bullet_move_flag_t_FORCE_UINT8 = 0xFF
};
union bullet_special_angle_t {
    unsigned char turn_by;
    char target;
    signed char v;
};
struct bullet_t {
    entity_flag_t flag;
    char age;
    PlayfieldMotion pos;
    unsigned char from_group;
    signed char unused;
    SubpixelLength8 speed_cur;
    unsigned char angle;
    bullet_spawn_flag_t spawn_flag;
    bullet_move_flag_t move_flag;
    bullet_special_motion_t special_motion;
    SubpixelLength8 speed_final;
    union {
        unsigned char decelerate_time;
        unsigned char turns_done;
    } u1;
    union {
        SubpixelLength8 decelerate_speed_delta;
        bullet_special_angle_t angle;
    } u2;
    int patnum;
    SPPoint origin;
    Subpixel distance;
};
union BulletSpecialState {
    unsigned char turns_max;
    SubpixelLength8 speed_delta;
};
extern BulletSpecialState bullet_special;
extern bullet_t bullets[BULLET_COUNT];
extern bool bullet_zap_drop_point_items;

union pellet_render_t {
    struct { int left; int top; } top;
    struct { unsigned int vram_offset; uint16_t sprite_offset; } bottom;
};
extern int pellet_clouds_render_count;
extern bullet_t near *pellet_clouds_render[PELLET_COUNT];
extern int pellets_render_count;
extern pellet_render_t pellets_render[PELLET_COUNT];
union BulletZapState {
    bool active;
    uint8_t frame;
};
extern BulletZapState bullet_zap;
extern unsigned char bullet_clear_time;
extern unsigned char player_is_hit;
extern unsigned char player_invincibility_time;
extern unsigned char stage_frame_mod2;
extern unsigned char rank;
extern bool turbo_mode;
extern unsigned int slowdown_factor;
extern bool slowdown_caused_by_bullets;
extern unsigned long score_delta;
extern unsigned int stage_graze;
extern unsigned int graze_score;
extern PlayfieldPoint drawpoint;

static const unsigned int STAGE_GRAZE_CAP = 999;
static const subpixel_t BULLET_KILLBOX_W = TO_SP(8);
static const subpixel_t BULLET_KILLBOX_H = TO_SP(8);
static const int BULLET_ZAP_FRAMES_PER_CEL = 4;
static const unsigned char RANK_EXTRA = 4;

typedef enum {
    PAT_BULLET16_D = 52,
    PAT_BULLET16_D_BLUE = 52,
    PAT_BULLET16_D_BLUE_last = 67,
    PAT_BULLET16_D_GREEN = 68,
    PAT_BULLET16_D_GREEN_last = 83,
    PAT_BULLET16_V_RED = 84,
    PAT_BULLET16_V_RED_last = 115,
    PAT_BULLET16_V_BLUE = 116,
    PAT_BULLET_ZAP = 152,
    PAT_DECAY_PELLET = 156,
    PAT_DECAY_BULLET16 = 160,
    // Real full sprite-domain bounds from th05/sprites/main_pat.h. Keeping
    // only the currently used low constants incorrectly narrows this enum.
    PAT_STAGE_last = 319,
    PAT_MAX = 320,
    _main_patnum_t_FORCE_INT16 = 0x7FFF
} main_patnum_t;

enum item_type_t {
    IT_NONE = -2, IT_ENEMY_DROP_NEXT = -1, IT_POWER = 0,
    IT_POINT = 1, IT_DREAM = 2, IT_BIGPOWER = 3, IT_BOMB = 4,
    IT_1UP = 5, IT_FULLPOWER = 6, IT_COUNT
};

extern "C" {
    void pascal near vector2_near(SPPoint near &ret,
        unsigned char angle, subpixel_t length);
    void pascal far vector2_at(SPPoint near &ret, subpixel_t origin_x,
        subpixel_t origin_y, subpixel_t length, int angle);
    vram_y_t pascal near scroll_subpixel_y_to_vram_seg3(subpixel_t y);
    int pascal far select_for_rank(int easy, int normal, int hard, int lunatic);
}
unsigned char pascal near bullet_patnum_for_angle(
    unsigned int patnum_base, unsigned char angle);
void pascal far sparks_add_random(Subpixel center_x, Subpixel center_y,
    subpixel_t radius_min, int count);
void far hud_graze_put(void);
void pascal near pointnums_add_white(subpixel_t center_x,
    subpixel_t center_y, uint16_t points);
void pascal near items_add(subpixel_t center_x, subpixel_t center_y,
    item_type_t type);

void pascal near bullet_update_patnum(bullet_t near &bullet);
void pascal near bullet_turn_x(bullet_t near &bullet);
void pascal near bullet_turn_y(bullet_t near &bullet);
void pascal near bullet_update_special(bullet_t near &bullet);
void far bullets_update(void);

inline subpixel_length_8_t to_sp8(float pixel_value) {
    return static_cast<subpixel_length_8_t>(pixel_value * 16);
}

#define overlap_offcenter_1d_inplace_fast(delta, dist_edge1, dist_edge2) ( \
	(unsigned int)((delta) += dist_edge1, delta) <= (dist_edge1 + dist_edge2) \
)

#define overlap_offcenter_inplace_fast( \
	delta_x, delta_y, dist_to_left, dist_to_top, dist_to_right, dist_to_bottom \
) ( \
	overlap_offcenter_1d_inplace_fast(delta_x, dist_to_left, dist_to_right) && \
	overlap_offcenter_1d_inplace_fast(delta_y, dist_to_top, dist_to_bottom) \
)

#define overlap_1d_inplace_fast(delta, extent) ( \
	(unsigned int)((delta) += (extent / 2), delta) <= (extent) \
)

#define overlap_wh_inplace_fast(delta_x, delta_y, w, h) ( \
	overlap_1d_inplace_fast(delta_x, w) && overlap_1d_inplace_fast(delta_y, h) \
)


#define playfield_encloses_yx_lt_ge(center_x, center_y, w, h) ( \
	/* Casting the center coordinate allows this macro to easily be used */ \
	/* with the _AX and _DX pseudoregisters after motion_update(). */ \
	(static_cast<subpixel_t>(center_y) >= to_sp(0 - (h  / 2))) && \
	(static_cast<subpixel_t>(center_y) < to_sp(PLAYFIELD_H + (h / 2))) && \
	(static_cast<subpixel_t>(center_x) >= to_sp(0 - (w / 2))) && \
	(static_cast<subpixel_t>(center_x) < to_sp(PLAYFIELD_W + (w / 2))) \
)

#define playfield_encloses(center_x, center_y, w, h) ( \
	/* Casting the center coordinate allows this macro to easily be used */ \
	/* with the _AX and _DX pseudoregisters after motion_update(). */ \
	(static_cast<subpixel_t>(center_x) > to_sp(0 - (w / 2))) && \
	(static_cast<subpixel_t>(center_x) < to_sp(PLAYFIELD_W + (w / 2))) && \
	(static_cast<subpixel_t>(center_y) > to_sp(0 - (h  / 2))) && \
	(static_cast<subpixel_t>(center_y) < to_sp(PLAYFIELD_H + (h / 2))) \
)


typedef char th05_update_main_patnum_is_2[(sizeof(main_patnum_t) == 2) ? 1 : -1];

typedef char th05_update_bullet_is_32[(sizeof(bullet_t) == 32) ? 1 : -1];
typedef char th05_update_bullet_flag_offset[(offsetof(bullet_t, flag) == 0) ? 1 : -1];
typedef char th05_update_bullet_age_offset[(offsetof(bullet_t, age) == 1) ? 1 : -1];
typedef char th05_update_bullet_pos_offset[(offsetof(bullet_t, pos) == 2) ? 1 : -1];
typedef char th05_update_bullet_from_group_offset[(offsetof(bullet_t, from_group) == 14) ? 1 : -1];
typedef char th05_update_bullet_unused_offset[(offsetof(bullet_t, unused) == 15) ? 1 : -1];
typedef char th05_update_bullet_speed_cur_offset[(offsetof(bullet_t, speed_cur) == 16) ? 1 : -1];
typedef char th05_update_bullet_angle_offset[(offsetof(bullet_t, angle) == 17) ? 1 : -1];
typedef char th05_update_bullet_spawn_flag_offset[(offsetof(bullet_t, spawn_flag) == 18) ? 1 : -1];
typedef char th05_update_bullet_move_flag_offset[(offsetof(bullet_t, move_flag) == 19) ? 1 : -1];
typedef char th05_update_bullet_special_motion_offset[(offsetof(bullet_t, special_motion) == 20) ? 1 : -1];
typedef char th05_update_bullet_speed_final_offset[(offsetof(bullet_t, speed_final) == 21) ? 1 : -1];
typedef char th05_update_bullet_u1_offset[(offsetof(bullet_t, u1) == 22) ? 1 : -1];
typedef char th05_update_bullet_u2_offset[(offsetof(bullet_t, u2) == 23) ? 1 : -1];
typedef char th05_update_bullet_patnum_offset[(offsetof(bullet_t, patnum) == 24) ? 1 : -1];
typedef char th05_update_bullet_origin_offset[(offsetof(bullet_t, origin) == 26) ? 1 : -1];
typedef char th05_update_bullet_distance_offset[(offsetof(bullet_t, distance) == 30) ? 1 : -1];
typedef char th05_update_spawn_flag_is_1[(sizeof(bullet_spawn_flag_t) == 1) ? 1 : -1];
typedef char th05_update_move_flag_is_1[(sizeof(bullet_move_flag_t) == 1) ? 1 : -1];
typedef char th05_update_special_angle_is_1[(sizeof(bullet_special_angle_t) == 1) ? 1 : -1];
typedef char th05_update_special_state_is_1[(sizeof(BulletSpecialState) == 1) ? 1 : -1];
typedef char th05_update_u1_is_1[(sizeof(((bullet_t *)0)->u1) == 1) ? 1 : -1];
typedef char th05_update_u2_is_1[(sizeof(((bullet_t *)0)->u2) == 1) ? 1 : -1];
typedef char th05_update_zap_state_is_1[(sizeof(BulletZapState) == 1) ? 1 : -1];
typedef char th05_update_pellet_render_is_4[(sizeof(pellet_render_t) == 4) ? 1 : -1];
typedef char th05_update_near_bullet_pointer_is_2[(sizeof(bullet_t near *) == 2) ? 1 : -1];
typedef char th05_update_item_type_is_1[(sizeof(item_type_t) == 1) ? 1 : -1];

#endif
