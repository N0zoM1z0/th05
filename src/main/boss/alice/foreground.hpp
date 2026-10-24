// Alice's real puppet and boss foreground sprite/charge rendering interfaces.
#ifndef TH05_ALICE_FOREGROUND_HPP
#define TH05_ALICE_FOREGROUND_HPP

// Capture the real main_01 callback before the canonical setup declarations.
void pascal near alice_fg_render(void);
extern "C" void pascal near puppets_render(void);
#include <dos.h>
#include "src/main/boss/alice/beam.hpp"

extern unsigned int stage_frame;
extern unsigned char stage_frame_mod2;
extern unsigned char stage_frame_mod8;
extern unsigned char stage_frame_mod16;

static const int ALICE_FG_PUPPET_COUNT = 2;
static const int ALICE_FG_PUPPET_W = 32;
static const int ALICE_FG_PUPPET_H = 32;
static const int ALICE_FG_PLAYFIELD_LEFT = 32;
static const int ALICE_FG_PLAYFIELD_TOP = 16;
static const int ALICE_FG_RMW = 0xC0;
static const unsigned int ALICE_FG_PUT_PLANES = 0xFF00 | ALICE_FG_RMW;
static const unsigned char ALICE_FG_PHASE_EXPLODE_BIG = 254;
static const int ALICE_FG_PAT_STAY = 180;
static const int ALICE_FG_PAT_ATTACK = 184;
#define alice_fg_puppets (reinterpret_cast<AlicePuppet near *>(custom_entities))

// Actual master.lib far Pascal APIs, including both real one-plane arguments.
#pragma codeseg _TEXT
extern "C" {
    void pascal far super_roll_put(int left, int top, int patnum);
    void pascal far super_put(int left, int top, int patnum);
    void pascal far super_large_put(int left, int top, int patnum);
    void pascal far super_put_1plane(int left, int top, int patnum,
        int pattern_plane, unsigned int put_plane);
    void pascal far grcg_setcolor(int mode, unsigned int color);
    void pascal far grcg_circle(int center_x, int center_y, unsigned int radius);
    void pascal far grcg_circlefill(int center_x, int center_y, unsigned int radius);
    void pascal far grcg_hline(int left, int right, int y);
}
#pragma codeseg ALICE_FG_TEXT main_01
void near explosions_small_update_and_render(void);
void near explosions_big_update_and_render(void);

typedef char alice_fg_full_puppet[(sizeof(AlicePuppet) == 26) ? 1 : -1];
typedef char alice_fg_real_patnum[(offsetof(AlicePuppet, patnum) == 18) ? 1 : -1];
typedef char alice_fg_real_damage[(offsetof(AlicePuppet, damage_this_frame) == 22) ? 1 : -1];
#endif
