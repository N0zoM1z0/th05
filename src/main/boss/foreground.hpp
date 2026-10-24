// Sara/Louise foreground callbacks with the full canonical Boss and sprite ABI.
#ifndef TH05_SARA_LOUISE_FG_HPP
#define TH05_SARA_LOUISE_FG_HPP
#pragma codeseg BOSS_FG_TEXT main_01
void pascal near sara_fg_render(void);
void pascal near louise_fg_render(void);
#include "src/main/boss/movement.hpp"

extern unsigned char stage_frame_mod8;
extern unsigned char stage_frame_mod16;
static const unsigned char BOSS_FG_PHASE_EXPLODE_BIG = 254;
static const int SARA_FG_PAT_STAY = 180;
static const int SARA_FG_PAT_RIGHT = 184;
static const int SARA_FG_PAT_LEFT = 186;
static const int BOSS_FG_ANIMATION_FRAMES = 4;
static const unsigned int BOSS_FG_PUT_PLANES = 0xFF00 | 0xC0;

#pragma codeseg _TEXT
extern "C" {
    void pascal far super_large_put(int left, int top, int patnum);
    void pascal far super_put(int left, int top, int patnum);
    void pascal far super_put_1plane(int left, int top, int patnum,
        int pattern_plane, unsigned int put_plane);
}
#pragma codeseg BOSS_FG_TEXT main_01
void near explosions_small_update_and_render(void);
void near explosions_big_update_and_render(void);
#endif
