// Complete player render state and existing real graphics interfaces.
#ifndef TH05_MAIN_PLAYER_RENDER_HPP
#define TH05_MAIN_PLAYER_RENDER_HPP
#include <dos.h>
#include "src/main/player/invalidate.hpp"

typedef pixel_t screen_x_t;
static const unsigned char MISS_ANIM_FRAMES = 32;
static const unsigned char MISS_ANIM_EXPLODE_UNTIL = 31;
static const int PLAYER_W = 32;
static const int PLAYER_H = 48;
static const int PLAYER_OPTION_H = 16;
static const int PLAYER_OPTION_TO_OPTION_DISTANCE = 48;
static const int PAT_OPTION = 26;
static const unsigned int PLANE_ALL_PUT = 0xFF00 | 0xC0;
extern unsigned char player_invincibility_time;
extern unsigned char shot_level;
extern unsigned char stage_frame_mod4;
extern SPPoint player_option_pos_cur;

#pragma codeseg _TEXT
extern "C" {
    void pascal far super_roll_put(int left, int top, int patnum);
    void pascal far super_roll_put_1plane(int left, int top, int patnum,
        int pattern_plane, unsigned int put_plane);
}
#pragma codeseg PLAYER_RENDER_TEXT main_01
void near grcg_setmode_rmw(void);
extern "C" {
    int pascal near scroll_subpixel_y_to_vram_seg1(subpixel_t y);
    // Native hybrid ABI: AX=left, DX=top, ES=A800; one Pascal word, RET2.
    // This caller preserves the original ES/DF preconditions.
    void pascal near z_super_roll_put_tiny_16x16_raw(int patnum);
    void pascal near player_render(void);
}

typedef char player_render_motion_is_12[(sizeof(player_pos) == 12) ? 1 : -1];
typedef char player_render_option_point_is_4[(sizeof(player_option_pos_cur) == 4) ? 1 : -1];
typedef char player_render_radius_is_word[(sizeof(miss_explosion_radius) == 2) ? 1 : -1];
#endif
