// Complete TH05 enemy layout corroborated by nmlgc/ReC98
// b6ba5b0a529edbb31efdf8c0e939263804f8ee47: th05/main/enemy/enemy.hpp.
// Rendering algorithm provenance is the maintained TH04 natural C++ owner.
#ifndef TH05_MAIN_ENEMY_ENEMY_HPP
#define TH05_MAIN_ENEMY_ENEMY_HPP

// Reuse the one canonical item enum, BulletTemplate and geometry definitions.
#include "src/main/bullet/update.hpp"

typedef int screen_x_t;

#define ENEMY_COUNT 32

static const unsigned int ENEMY_GRCG_RMW = 0xC0;
static const unsigned int ENEMY_GRCG_ALL_PLANES = 0x00;

enum enemy_flag_t {
    EF_FREE = 0,
    EF_ALIVE = 1,
    EF_KILLED = 2,
    EF_ALIVE_FIRST_FRAME = 3,
    EF_KILL_ANIM = 0x80,
    EF_KILL_ANIM_last = (EF_KILL_ANIM + 4 - 1)
};

struct enemy_t {
    unsigned char flag;
    unsigned char age;
    PlayfieldMotion pos;
    int hp;
    int score;
    unsigned char near *script;
    int script_ip;
    SubpixelLength8 speed;
    unsigned char patnum_base;
    unsigned char cur_instr_frame;
    unsigned char loop_i;
    unsigned char angle;
    unsigned char angle_delta;
    unsigned char anim_cels;
    unsigned char anim_frames_per_cel;
    unsigned char anim_cur_cel;
    char clip;
    item_type_t item;
    bool damaged_this_frame;
    bool can_be_damaged;
    bool autofire;
    bool kills_player_on_collision;
    bool spawned_in_left_half;
    unsigned char autofire_cur_frame;
    unsigned char autofire_interval;
    BulletTemplate bullet_template;
    unsigned char subtype;
    signed char unused_1;
    int unused_2;
    signed char unused_3;
    // Genuine five-byte unused tail in the original enemy record, retained
    // from its full declaration; not inserted to force a selected field offset.
    signed char padding[5];
};
extern enemy_t enemies[ENEMY_COUNT];

extern "C" {
    void pascal far super_roll_put(int x, int y, int patnum);
    void pascal far super_roll_put_1plane(int x, int y, int patnum,
        int pattern_plane, unsigned int put_plane);
}
void pascal near enemies_render(void);

typedef char th05_enemy_is_64[(sizeof(enemy_t) == 64) ? 1 : -1];
typedef char th05_enemy_flag_offset[(offsetof(enemy_t, flag) == 0) ? 1 : -1];
typedef char th05_enemy_age_offset[(offsetof(enemy_t, age) == 1) ? 1 : -1];
typedef char th05_enemy_pos_offset[(offsetof(enemy_t, pos) == 2) ? 1 : -1];
typedef char th05_enemy_hp_offset[(offsetof(enemy_t, hp) == 14) ? 1 : -1];
typedef char th05_enemy_score_offset[(offsetof(enemy_t, score) == 16) ? 1 : -1];
typedef char th05_enemy_script_offset[(offsetof(enemy_t, script) == 18) ? 1 : -1];
typedef char th05_enemy_script_ip_offset[(offsetof(enemy_t, script_ip) == 20) ? 1 : -1];
typedef char th05_enemy_speed_offset[(offsetof(enemy_t, speed) == 22) ? 1 : -1];
typedef char th05_enemy_patnum_base_offset[(offsetof(enemy_t, patnum_base) == 23) ? 1 : -1];
typedef char th05_enemy_cur_instr_frame_offset[(offsetof(enemy_t, cur_instr_frame) == 24) ? 1 : -1];
typedef char th05_enemy_loop_i_offset[(offsetof(enemy_t, loop_i) == 25) ? 1 : -1];
typedef char th05_enemy_angle_offset[(offsetof(enemy_t, angle) == 26) ? 1 : -1];
typedef char th05_enemy_angle_delta_offset[(offsetof(enemy_t, angle_delta) == 27) ? 1 : -1];
typedef char th05_enemy_anim_cels_offset[(offsetof(enemy_t, anim_cels) == 28) ? 1 : -1];
typedef char th05_enemy_anim_frames_per_cel_offset[(offsetof(enemy_t, anim_frames_per_cel) == 29) ? 1 : -1];
typedef char th05_enemy_anim_cur_cel_offset[(offsetof(enemy_t, anim_cur_cel) == 30) ? 1 : -1];
typedef char th05_enemy_clip_offset[(offsetof(enemy_t, clip) == 31) ? 1 : -1];
typedef char th05_enemy_item_offset[(offsetof(enemy_t, item) == 32) ? 1 : -1];
typedef char th05_enemy_damaged_this_frame_offset[(offsetof(enemy_t, damaged_this_frame) == 33) ? 1 : -1];
typedef char th05_enemy_can_be_damaged_offset[(offsetof(enemy_t, can_be_damaged) == 34) ? 1 : -1];
typedef char th05_enemy_autofire_offset[(offsetof(enemy_t, autofire) == 35) ? 1 : -1];
typedef char th05_enemy_kills_player_on_collision_offset[(offsetof(enemy_t, kills_player_on_collision) == 36) ? 1 : -1];
typedef char th05_enemy_spawned_in_left_half_offset[(offsetof(enemy_t, spawned_in_left_half) == 37) ? 1 : -1];
typedef char th05_enemy_autofire_cur_frame_offset[(offsetof(enemy_t, autofire_cur_frame) == 38) ? 1 : -1];
typedef char th05_enemy_autofire_interval_offset[(offsetof(enemy_t, autofire_interval) == 39) ? 1 : -1];
typedef char th05_enemy_bullet_template_offset[(offsetof(enemy_t, bullet_template) == 40) ? 1 : -1];
typedef char th05_enemy_subtype_offset[(offsetof(enemy_t, subtype) == 54) ? 1 : -1];
typedef char th05_enemy_unused_1_offset[(offsetof(enemy_t, unused_1) == 55) ? 1 : -1];
typedef char th05_enemy_unused_2_offset[(offsetof(enemy_t, unused_2) == 56) ? 1 : -1];
typedef char th05_enemy_unused_3_offset[(offsetof(enemy_t, unused_3) == 58) ? 1 : -1];
typedef char th05_enemy_padding_offset[(offsetof(enemy_t, padding) == 59) ? 1 : -1];
typedef char th05_enemy_script_pointer_is_2[(sizeof(((enemy_t *)0)->script) == 2) ? 1 : -1];
typedef char th05_enemy_near_pointer_is_2[(sizeof(enemy_t near *) == 2) ? 1 : -1];

#endif
