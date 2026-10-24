// Cheeto state and collision interfaces adapted from natural C++ in
// nmlgc/ReC98@b6ba5b0a529edbb31efdf8c0e939263804f8ee47:
// th05/main/bullet/cheeto.hpp, th04/main/custom.hpp, th01/math/overlap.hpp.
#ifndef TH05_MAIN_BULLET_CHEETO_HPP
#define TH05_MAIN_BULLET_CHEETO_HPP

#include "src/main/player/player.hpp"

#define CHEETO_W 32
#define CHEETO_H 32
#define CHEETO_TRAIL_NODE_COUNT 16
#define CHEETO_COUNT 7
#define CUSTOM_COUNT 64
#define TO_SP(pixel_value) ((pixel_value) << 4)

// Real general-purpose custom-entity slot; head/template are overlays of it.
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

enum cheeto_flag_t {
    CF_FREE = 0,
    CF_DECELERATE = 1,
    CF_SPEEDUP = 2,
    _cheeto_flag_t_FORCE_UINT8 = 0xFF
};

struct cheeto_template_t {
    signed char unused_flag;
    unsigned char angle;
    PlayfieldPoint origin;
    // Original six-word unused overlay: prev, velocity, val1 and val2.
    int unused_motion_and_values[6];
    unsigned int col;
    long unused_collision_values;
    SubpixelLength8 speed;
};

struct cheeto_head_t {
    cheeto_flag_t flag;
    unsigned char angle;
    PlayfieldMotion pos;
    unsigned int age;
    int unused_val2;
    int sprite;
    long unused_collision_values;
    SubpixelLength8 speed;
    signed char padding; // Real scalar field retained from custom_t.
};

struct cheeto_trail_t {
    cheeto_flag_t flag;
    char col;
    PlayfieldPoint node_pos[CHEETO_TRAIL_NODE_COUNT];
    unsigned char node_sprite[CHEETO_TRAIL_NODE_COUNT];
};

extern custom_t custom_entities[CUSTOM_COUNT];
extern cheeto_trail_t cheeto_trails[CHEETO_COUNT + 1];
#define cheeto_template (reinterpret_cast<cheeto_template_t &>(custom_entities[0]))
#define cheeto_heads (reinterpret_cast<cheeto_head_t *>(&custom_entities[1]))

extern unsigned char player_is_hit;
extern unsigned char stage_frame_mod2;
extern "C" void pascal near vector2_near(
    SPPoint near &ret, unsigned char angle, subpixel_t length);
unsigned char pascal near bullet_patnum_for_angle(
    unsigned int patnum_base, unsigned char angle);
void near cheetos_add(void);
void near cheetos_update(void);

// Preserve inclusive unsigned wraparound collision tests. The point form uses
// the accepted Subpixel subtraction operator, not widened floating arithmetic.
#define overlap_1d_inplace_fast(delta_value, extent_value) ( \
    (unsigned int)((delta_value) += (extent_value / 2), delta_value) <= (extent_value) \
)
#define overlap_wh_inplace_fast(delta_x_value, delta_y_value, width_value, height_value) ( \
    overlap_1d_inplace_fast(delta_x_value, width_value) && \
    overlap_1d_inplace_fast(delta_y_value, height_value) \
)
#define overlap_points_wh_fast(point1, point2, width_value, height_value) ( \
    ((unsigned int)((point1.x - point2.x) + (width_value / 2)) <= (width_value)) && \
    ((unsigned int)((point1.y - point2.y) + (height_value / 2)) <= (height_value)) \
)
inline subpixel_t cheeto_to_sp(float pixel_value) {
    return static_cast<subpixel_t>(pixel_value * 16);
}
#define playfield_encloses_point(point_value, width_value, height_value) ( \
    (static_cast<subpixel_t>(point_value.x) > cheeto_to_sp(0 - (width_value / 2))) && \
    (static_cast<subpixel_t>(point_value.x) < cheeto_to_sp(384 + (width_value / 2))) && \
    (static_cast<subpixel_t>(point_value.y) > cheeto_to_sp(0 - (height_value / 2))) && \
    (static_cast<subpixel_t>(point_value.y) < cheeto_to_sp(368 + (height_value / 2))) \
)

typedef char th05_custom_t_size[(sizeof(custom_t) == 26) ? 1 : -1];
typedef char th05_custom_t_flag_offset[(offsetof(custom_t, flag) == 0) ? 1 : -1];
typedef char th05_custom_t_angle_offset[(offsetof(custom_t, angle) == 1) ? 1 : -1];
typedef char th05_custom_t_pos_offset[(offsetof(custom_t, pos) == 2) ? 1 : -1];
typedef char th05_custom_t_val1_offset[(offsetof(custom_t, val1) == 14) ? 1 : -1];
typedef char th05_custom_t_val2_offset[(offsetof(custom_t, val2) == 16) ? 1 : -1];
typedef char th05_custom_t_sprite_offset[(offsetof(custom_t, sprite) == 18) ? 1 : -1];
typedef char th05_custom_t_val3_offset[(offsetof(custom_t, val3) == 20) ? 1 : -1];
typedef char th05_custom_t_damage_offset[(offsetof(custom_t, damage) == 22) ? 1 : -1];
typedef char th05_custom_t_speed_offset[(offsetof(custom_t, speed) == 24) ? 1 : -1];
typedef char th05_custom_t_padding_offset[(offsetof(custom_t, padding) == 25) ? 1 : -1];
typedef char th05_cheeto_template_t_size[(sizeof(cheeto_template_t) == 25) ? 1 : -1];
typedef char th05_cheeto_template_t_unused_flag_offset[(offsetof(cheeto_template_t, unused_flag) == 0) ? 1 : -1];
typedef char th05_cheeto_template_t_angle_offset[(offsetof(cheeto_template_t, angle) == 1) ? 1 : -1];
typedef char th05_cheeto_template_t_origin_offset[(offsetof(cheeto_template_t, origin) == 2) ? 1 : -1];
typedef char th05_cheeto_template_t_unused_motion_and_values_offset[(offsetof(cheeto_template_t, unused_motion_and_values) == 6) ? 1 : -1];
typedef char th05_cheeto_template_t_col_offset[(offsetof(cheeto_template_t, col) == 18) ? 1 : -1];
typedef char th05_cheeto_template_t_unused_collision_values_offset[(offsetof(cheeto_template_t, unused_collision_values) == 20) ? 1 : -1];
typedef char th05_cheeto_template_t_speed_offset[(offsetof(cheeto_template_t, speed) == 24) ? 1 : -1];
typedef char th05_cheeto_head_t_size[(sizeof(cheeto_head_t) == 26) ? 1 : -1];
typedef char th05_cheeto_head_t_flag_offset[(offsetof(cheeto_head_t, flag) == 0) ? 1 : -1];
typedef char th05_cheeto_head_t_angle_offset[(offsetof(cheeto_head_t, angle) == 1) ? 1 : -1];
typedef char th05_cheeto_head_t_pos_offset[(offsetof(cheeto_head_t, pos) == 2) ? 1 : -1];
typedef char th05_cheeto_head_t_age_offset[(offsetof(cheeto_head_t, age) == 14) ? 1 : -1];
typedef char th05_cheeto_head_t_unused_val2_offset[(offsetof(cheeto_head_t, unused_val2) == 16) ? 1 : -1];
typedef char th05_cheeto_head_t_sprite_offset[(offsetof(cheeto_head_t, sprite) == 18) ? 1 : -1];
typedef char th05_cheeto_head_t_unused_collision_values_offset[(offsetof(cheeto_head_t, unused_collision_values) == 20) ? 1 : -1];
typedef char th05_cheeto_head_t_speed_offset[(offsetof(cheeto_head_t, speed) == 24) ? 1 : -1];
typedef char th05_cheeto_head_t_padding_offset[(offsetof(cheeto_head_t, padding) == 25) ? 1 : -1];
typedef char th05_cheeto_trail_t_size[(sizeof(cheeto_trail_t) == 82) ? 1 : -1];
typedef char th05_cheeto_trail_t_flag_offset[(offsetof(cheeto_trail_t, flag) == 0) ? 1 : -1];
typedef char th05_cheeto_trail_t_col_offset[(offsetof(cheeto_trail_t, col) == 1) ? 1 : -1];
typedef char th05_cheeto_trail_t_node_pos_offset[(offsetof(cheeto_trail_t, node_pos) == 2) ? 1 : -1];
typedef char th05_cheeto_trail_t_node_sprite_offset[(offsetof(cheeto_trail_t, node_sprite) == 66) ? 1 : -1];
typedef char th05_cheeto_flag_is_1[(sizeof(cheeto_flag_t) == 1) ? 1 : -1];
typedef char th05_cheeto_head_near_pointer_is_2[(sizeof(cheeto_head_t near *) == 2) ? 1 : -1];
typedef char th05_cheeto_trail_near_pointer_is_2[(sizeof(cheeto_trail_t near *) == 2) ? 1 : -1];
typedef char th05_cheeto_head_fits_custom_slot[(sizeof(cheeto_head_t) == sizeof(custom_t)) ? 1 : -1];
typedef char th05_cheeto_template_fits_custom_slot[(sizeof(cheeto_template_t) <= sizeof(custom_t)) ? 1 : -1];

#endif
