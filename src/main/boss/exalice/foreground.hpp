// Full EX-Alice foreground callback with canonical Boss and real sprite APIs.
#ifndef TH05_EXALICE_FG_HPP
#define TH05_EXALICE_FG_HPP
#include "src/main/boss/movement.hpp"

extern unsigned char exalice_bomb_invincibility;
extern int exalice_backdrop_patnum;
extern unsigned char stage_frame_mod16;
static const unsigned char EX_FG_PHASE_EXPLODE_BIG = 254;
static const unsigned int EX_FG_PUT_PLANES = 0xFF00 | 0xC0;

#pragma codeseg _TEXT
extern "C" {
    void pascal far super_large_put(int left, int top, int patnum);
    void pascal far super_put(int left, int top, int patnum);
    void pascal far super_put_1plane(int left, int top, int patnum,
        int pattern_plane, unsigned int put_plane);
}
#pragma codeseg EXALICE_FG_TEXT main_01
void near explosions_small_update_and_render(void);
void near explosions_big_update_and_render(void);
void pascal near exalice_fg_render(void);

typedef char ex_fg_full_boss[(sizeof(boss_stuff_t) == 24) ? 1 : -1];
#endif
