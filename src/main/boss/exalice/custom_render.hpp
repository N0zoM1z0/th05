// Complete firewave storage and authentic polar/PC-98 sprite interfaces.
#ifndef TH05_EXALICE_CUSTOM_RENDER_HPP
#define TH05_EXALICE_CUSTOM_RENDER_HPP

#pragma codeseg SHARED
// Real far Pascal implementation, declared before the canonical graphics header.
int far pascal polar(int center, int radius, int ratio);
#pragma codeseg EX_CUSTOM_TEXT main_01
#include <dos.h>
#include "src/main/boss/explosion.hpp"
#include "src/main/player/player.hpp"

typedef int vram_y_t;
// Literal full ODR definition from the frozen natural firewaves.cpp owner.
struct near firewave_t {
    bool alive;
    bool is_right;
    vram_y_t bottom;
    pixel_t amp;
};
static const int EX_FIREWAVE_COUNT = 2;
static const int EX_FIREWAVE_PAT_LEFT = 168;
static const int EX_FIREWAVE_BAND_H = 16;
static const int EX_FIREWAVE_PLAYFIELD_LEFT = 32;
static const int EX_FIREWAVE_PLAYFIELD_TOP = 16;
static const int EX_FIREWAVE_PLAYFIELD_RIGHT = EX_FIREWAVE_PLAYFIELD_LEFT + 384;
static const int EX_FIREWAVE_PLAYFIELD_BOTTOM = EX_FIREWAVE_PLAYFIELD_TOP + 368;
extern firewave_t firewaves[EX_FIREWAVE_COUNT];
extern unsigned char player_is_hit;

#pragma codeseg _TEXT
extern "C" void pascal far grcg_byteboxfill_x(int left_byte, int top,
    int right_byte, int bottom);
#pragma codeseg EX_CUSTOM_TEXT main_01
void pascal near cheetos_render(void);
extern "C" void pascal near exalice_custombullets_render(void);

typedef char ex_firewave_full_6[(sizeof(firewave_t) == 6) ? 1 : -1];
typedef char ex_firewave_bottom_2[(offsetof(firewave_t, bottom) == 2) ? 1 : -1];
typedef char ex_firewave_amp_4[(offsetof(firewave_t, amp) == 4) ? 1 : -1];
#endif
