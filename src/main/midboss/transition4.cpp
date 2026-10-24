// Natural movement algorithm from MAIN 1527:0D04 / reference sub_1AFD4.
#pragma option -zCB4_UPDATE_TEXT -zPmain_03
#include "src/main/midboss/transition4.hpp"

bool near midboss4_pattern_transition(void)
{
    int frame;
    if(midboss.phase_frame >= 16) {
        frame = midboss.phase_frame - 16;
        if(frame < 32) {
            if(frame == 0) {
                boss_statebyte[15] = 0;
                snd_se_play(13);
                midboss4_transition_center_x = midboss.pos.cur.x.v;
            }
            midboss.pos.cur.x.v = midboss4_transition_center_x;
            if(frame > 20) {
                frame = 20 + ((frame - 20) / 2);
            }
            if(stage_frame_mod2) {
                midboss.pos.cur.x.v += frame * 32;
            } else {
                midboss.pos.cur.x.v -= frame * 32;
            }
        } else if(frame == 32) {
            midboss4_transition_center_x = randring2_next16_mod(to_sp(256)) + to_sp(64);
            midboss.pos.cur.y.v = randring2_next16_mod(to_sp(32)) + to_sp(64);
        } else {
            frame = 64 - frame;
            if(frame > 20) {
                frame = 20 + ((frame - 20) / 2);
            }
            midboss.pos.cur.x.v = midboss4_transition_center_x;
            if(stage_frame_mod2) {
                midboss.pos.cur.x.v += frame * 32;
            } else {
                midboss.pos.cur.x.v -= frame * 32;
            }
            if(frame == 0) {
                boss_statebyte[15] = 1;
                return true;
            }
        }
    }
    return false;
}
