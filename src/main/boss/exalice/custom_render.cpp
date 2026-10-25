// Real firewave fill/sprite bands and collision tests, followed by cheeto draw.
#pragma option -zCEX_CUSTOM_TEXT -zPmain_01
#include "src/main/boss/exalice/custom_render.hpp"

extern "C" void pascal near exalice_custombullets_render(void)
{
    int i;
    int angle;
    int x;
    int patnum;
    int left;
    int top;
    firewave_t near *wave;

    wave = firewaves;
    for(i = 0; i < EX_FIREWAVE_COUNT; i++, wave++) {
        if(wave->alive) {
            top = wave->bottom;
            angle = (top & 0x0F) / 2;
            top &= 0xFFF0;
            patnum = wave->is_right + EX_FIREWAVE_PAT_LEFT;
            for(; top >= EX_FIREWAVE_PLAYFIELD_TOP && angle < 0x80;
                top -= EX_FIREWAVE_BAND_H, angle += 8) {
                if(top < EX_FIREWAVE_PLAYFIELD_BOTTOM) {
                    x = polar_y(0, wave->amp, angle);
                    if(wave->is_right == 0) {
                        x += 16;
                    } else {
                        x = EX_FIREWAVE_PLAYFIELD_RIGHT - x;
                    }
                    left = x;
                    if(wave->is_right == 0) {
                        if(x > EX_FIREWAVE_PLAYFIELD_LEFT) {
                            grcg_byteboxfill_x(EX_FIREWAVE_PLAYFIELD_LEFT / 8, top,
                                (x - 1) / 8, top + EX_FIREWAVE_BAND_H - 1);
                        }
                        if(static_cast<unsigned int>((player_pos.cur.y.v / 16) - top) < 16 &&
                            (player_pos.cur.x.v / 16) < x - EX_FIREWAVE_PLAYFIELD_LEFT) {
                            player_is_hit = 1;
                        }
                    } else {
                        x += 16;
                        if(x < EX_FIREWAVE_PLAYFIELD_RIGHT) {
                            grcg_byteboxfill_x(x / 8, top,
                                EX_FIREWAVE_PLAYFIELD_RIGHT / 8 - 1,
                                top + EX_FIREWAVE_BAND_H - 1);
                        }
                        if(static_cast<unsigned int>((player_pos.cur.y.v / 16) - top) < 16 &&
                            (player_pos.cur.x.v / 16) > x - EX_FIREWAVE_PLAYFIELD_LEFT) {
                            player_is_hit = 1;
                        }
                    }
                    // Genuine existing renderer ABI: ES=VRAM, AX=left, DX=top.
                    _ES = SEG_PLANE_B;
                    z_super_roll_put_tiny_16x16(left, top, patnum);
                }
            }
        }
    }
    cheetos_render();
}
