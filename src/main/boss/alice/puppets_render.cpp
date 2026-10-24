// Complete real puppet-renderer owner; also included by the coherent foreground TU.
#ifndef TH05_ALICE_FG_COMBINED
#pragma option -zCALICE_FG_TEXT -zPmain_01
#include "src/main/boss/alice/foreground.hpp"
#endif

extern "C" void pascal near puppets_render(void)
{
    int i;
    int left;
    int patnum;
    int center_x[ALICE_FG_PUPPET_COUNT];
    int top;
    AlicePuppet near *puppet;

    puppet = alice_fg_puppets;
    for(i = 0; i < ALICE_FG_PUPPET_COUNT; i++, puppet++) {
        if(puppet->flag != 0) {
            left = (puppet->pos.cur.x.v >> 4) +
                ALICE_FG_PLAYFIELD_LEFT - (ALICE_FG_PUPPET_W / 2);
            if(left > 0 && left < PLAYFIELD_W + ALICE_FG_PUPPET_W) {
                top = puppet->pos.cur.y.v >> 4;
                if(top > -ALICE_FG_PUPPET_H / 2 &&
                    top < PLAYFIELD_H + (ALICE_FG_PUPPET_H / 2)) {
                    top += (((stage_frame & 0x1F) < 16)
                        ? stage_frame_mod16 : (16 - stage_frame_mod16)) / 2;
                    patnum = puppet->patnum;
                    if(puppet->flag == 1) {
                        patnum += stage_frame_mod2;
                    }
                    if(puppet->damage_this_frame == 0) {
                        super_roll_put(left, top, patnum);
                    } else {
                        super_put_1plane(left, top, patnum, 0, ALICE_FG_PUT_PLANES);
                    }
                    top = (puppet->pos.cur.y.v >> 4) + ALICE_FG_PLAYFIELD_TOP;
                    if(boss_statebyte[9] == 1) {
                        if(stage_frame_mod2 != 0) {
                            grcg_setcolor(ALICE_FG_RMW, 15);
                            grcg_circle(left + (ALICE_FG_PUPPET_W / 2), top,
                                puppet->radius.radius_gather);
                            outportb(0x7C, 0);
                        }
                    } else if(boss_statebyte[9] == 2) {
                        grcg_setcolor(ALICE_FG_RMW, 15);
                        grcg_circlefill(left + (ALICE_FG_PUPPET_W / 2), top,
                            puppet->radius.radius_gather);
                        outportb(0x7C, 0);
                    }
                    center_x[i] = left + (ALICE_FG_PUPPET_W / 2);
                }
            }
        }
    }
    if(boss_statebyte[9] == 2) {
        grcg_setcolor(ALICE_FG_RMW, 9);
        grcg_hline(center_x[0], center_x[1], top);
        outportb(0x7C, 0);
    } else if(boss_statebyte[9] == 3) {
        super_put(center_x[0], top, boss_statebyte[8]);
        super_put(center_x[0] + 64, top, boss_statebyte[8] + 1);
    }
}
