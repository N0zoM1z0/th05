// Complete Boss and real sprite APIs for late-game foreground callbacks.
#ifndef TH05_LATE_FOREGROUND_HPP
#define TH05_LATE_FOREGROUND_HPP
#pragma codeseg YUMEKO_FG_TEXT main_01
void pascal near yumeko_fg_render(void);
#pragma codeseg SHINKI_FG_TEXT main_01
void pascal near shinki_fg_render(void);
#include "src/main/boss/movement.hpp"

extern boss_stuff_t boss2;
extern unsigned char stage_frame_mod16;
static const unsigned char LATE_FG_PHASE_HP_FILL = 0;
static const unsigned char LATE_FG_PHASE_EXPLODE_BIG = 254;
static const unsigned int LATE_FG_PUT_PLANES = 0xFF00 | 0xC0;
static const int YUMEKO_FG_ENTRANCE_PATNUM = 192;
static const int SHINKI_FG_WING_FIRST = 184;
static const int SHINKI_FG_WING_W = 256;
static const int SHINKI_FG_PART_W = 64;
static const int SHINKI_FG_PART_COUNT = SHINKI_FG_WING_W / SHINKI_FG_PART_W;

#pragma codeseg _TEXT
extern "C" {
    void pascal far super_large_put(int left, int top, int patnum);
    void pascal far super_put(int left, int top, int patnum);
    void pascal far super_put_1plane(int left, int top, int patnum,
        int pattern_plane, unsigned int put_plane);
    void pascal far super_put_rect(int left, int top, int patnum);
    void pascal far super_put_8(int left, int top, int patnum);
}
#pragma codeseg LATE_FG_CONTEXT main_01
void near explosions_small_update_and_render(void);
void near explosions_big_update_and_render(void);
#pragma codeseg
#endif
