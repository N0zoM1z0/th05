// Complete Mai/Yuki foreground owner and the actual near Pascal sprite helper.
#ifndef TH05_MY_FOREGROUND_HPP
#define TH05_MY_FOREGROUND_HPP
#include "src/main/boss/mai_yuki.hpp"

extern unsigned char stage_frame_mod8;
static const unsigned char MY_FG_PHASE_EXPLODE_SMALL = 253;
static const unsigned char MY_FG_PHASE_EXPLODE_BIG = 254;
static const int MY_FG_CELS = 16;
static const int MY_FG_PAT_MAI_ANIMATED = 184;
static const int MY_FG_PAT_YUKI_ANIMATED = MY_FG_PAT_MAI_ANIMATED + MY_FG_CELS;
static const unsigned int MY_FG_PUT_PLANES = 0xFF00 | 0xC0;

#pragma codeseg _TEXT
extern "C" {
    void pascal far super_large_put(int left, int top, int patnum);
    void pascal far super_put(int left, int top, int patnum);
    void pascal far super_put_1plane(int left, int top, int patnum,
        int pattern_plane, unsigned int put_plane);
}
#pragma codeseg MY_FG_TEXT main_01
void near explosions_small_update_and_render(void);
void near explosions_big_update_and_render(void);
void pascal near mai_yuki_sprite_put(int left, int top, int patnum, int damaged);
void pascal near mai_yuki_fg_render(void);

typedef char my_fg_full_boss[(sizeof(boss_stuff_t) == 24) ? 1 : -1];
typedef char my_fg_phase_state[(offsetof(boss_stuff_t, phase_state) == 21) ? 1 : -1];
#endif
