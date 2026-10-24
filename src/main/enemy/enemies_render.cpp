// Natural C++ algorithm reused from the maintained TH04 reconstruction:
// src/main/enemy/enemies_render.cpp, SHA-256
// 738af3eb931e3b355b527f556f670f1086555779da3a4d1172d534f872d95a0b.
// TH05 uses its own complete enemy layout; TH04 acceptance does not transfer.
#pragma option -zCMAIN__TEXT -zPmain_01
#include <dos.h>
#include "src/main/enemy/enemy.hpp"

static const unsigned int PLANE_ALL_PUT = (0xFF00 | ENEMY_GRCG_RMW | ENEMY_GRCG_ALL_PLANES);
static const int ENEMY_W = 32;
static const int ENEMY_H = 32;

void pascal near enemies_render(void)
{
    int i;
    vram_y_t top;
    unsigned char patnum;
    register enemy_t near *enemy;
    register screen_x_t left;

    enemy = enemies;
    i = 0;
    for(; i < ENEMY_COUNT; (i++, enemy++)) {
        if((enemy->flag != EF_ALIVE) && (enemy->flag < EF_KILL_ANIM)) {
            continue;
        }
        if(enemy->pos.prev.y.v <= TO_SP(-(ENEMY_H / 2))) {
            continue;
        }
        if(enemy->pos.prev.y.v >= TO_SP(PLAYFIELD_H + (ENEMY_H / 2))) {
            continue;
        }
        patnum = enemy->patnum_base;
        if(enemy->anim_cels > 1) {
            if((enemy->age % enemy->anim_frames_per_cel) == 0) {
                enemy->anim_cur_cel++;
                if(enemy->anim_cur_cel >= enemy->anim_cels) {
                    enemy->anim_cur_cel = 0;
                }
            }
            patnum += enemy->anim_cur_cel;
        }
        left = ((enemy->pos.cur.x.v >> 4) + (PLAYFIELD_LEFT - (ENEMY_W / 2)));
        top = scroll_subpixel_y_to_vram_seg1(enemy->pos.cur.y.v);
        if(left <= 0) {
            continue;
        }
        if(left >= PLAYFIELD_RIGHT) {
            continue;
        }
        if(enemy->pos.cur.y.v <= TO_SP(-(ENEMY_H / 2))) {
            continue;
        }
        if(enemy->pos.cur.y.v >= TO_SP(PLAYFIELD_H + (ENEMY_H / 2))) {
            continue;
        }
        if(!enemy->damaged_this_frame) {
            // AX still holds the scroll conversion result in this branch.
            super_roll_put(left, _AX, patnum);
        } else {
            super_roll_put_1plane(left, top, patnum, 0, PLANE_ALL_PUT);
            enemy->damaged_this_frame = false;
        }
    }
}
