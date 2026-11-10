// Exact TH05 item motion and collection loop adapted from maintained TH04 C++.
// The native 32-bit Motion result remains in AX:DX; two genuine register
// subtraction primitives use the source-level Turbo C++ inline assembler.
#pragma option -zCITEM_UPDATE_TEXT -zPmain_03
#include <dos.h>
#include "src/main/item/update.hpp"
#pragma codeseg ITEM_UPDATE_TEXT main_03

extern "C" void pascal far items_update(void)
{
    unsigned char pull_angle;
    register item_t near *item;
    register int i;
    item = items;
    i = 0;
    for(; i < ITEM_COUNT; (i++, item++)) {
        if(item->flag == F_FREE) {
            continue;
        }
        if(item->flag == F_REMOVE) {
            item->flag = F_FREE;
            continue;
        }
        if(items_pull_to_player) {
            pointnum_times_2 = true;
            item->pulled_to_player = true;
            pull_angle = iatan2(player_pos.cur.y.v - item->pos.cur.y.v,
                player_pos.cur.x.v - item->pos.cur.x.v);
            vector2_near(item->pos.velocity, pull_angle, TO_SP(ITEM_PULL_SPEED));
        } else if(item->pulled_to_player) {
            item->pos.velocity.x.v = 0;
            item->pos.velocity.y.v = 0;
            item->pulled_to_player = false;
        }
        // Return value remains in the original AX:DX registers through pickup.
        item->pos.update_seg3();
        if((static_cast<subpixel_t>(_AX) <= -TO_SP(ITEM_W / 2)) ||
            (static_cast<subpixel_t>(_AX) >= TO_SP(PLAYFIELD_W + ITEM_W / 2)) ||
            (static_cast<subpixel_t>(_DX) >= TO_SP(PLAYFIELD_H + ITEM_H / 2))) {
            item->flag = F_REMOVE;
            item_miss_penalty(item);
            continue;
        }
        if(static_cast<subpixel_t>(_DX) < -TO_SP(ITEM_H / 2)) {
            item->pos.cur.y.v = -TO_SP(ITEM_H / 2);
        }
        if(item->pos.velocity.y.v >= 0) {
            item->pos.velocity.x.v = 0;
        }
        if(miss_time == 0) {
            _BX = player_pos.cur.x.v;
            _BX += TO_SP(24);
            asm { sub bx, ax; }
            if(static_cast<unsigned int>(_BX) > TO_SP(48)) {
                goto no_collect;
            }
            _BX = player_pos.cur.y.v;
            _BX += TO_SP(24);
            asm { sub bx, dx; }
            if(static_cast<unsigned int>(_BX) > TO_SP(38)) {
                goto no_collect;
            }
            item_collect(item);
            snd_se_play(11);
            item->flag = F_REMOVE;
            continue;
        }
    no_collect:
        item->pos.velocity.y.v++;
    }
    item_splashes_update();
    pointnum_times_2 = false;
}
