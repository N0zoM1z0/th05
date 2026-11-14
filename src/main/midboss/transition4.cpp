// Natural movement algorithm from MAIN 1527:0D04 / reference sub_1AFD4.
#pragma option -zCB4_UPDATE_TEXT -zPmain_03
#include "src/main/midboss/transition4.hpp"
#include "src/main/midboss/stage4_scratch.hpp"

bool near midboss4_pattern_transition(void)
{
    enum {
        MIDBOSS4_TRANSITION_START_FRAME = 16,
        MIDBOSS4_TRANSITION_HALF_FRAMES = 32,
        MIDBOSS4_TRANSITION_SLOWDOWN_FRAME = 20,
        MIDBOSS4_TRANSITION_END_FRAME = 64,
        MIDBOSS4_TRANSITION_SLOWDOWN_DIVISOR = 2,
        MIDBOSS4_TRANSITION_X_STEP_SP = 32,
        MIDBOSS4_TRANSITION_CENTER_X_RANGE_PX = 256,
        MIDBOSS4_TRANSITION_CENTER_X_MIN_PX = 64,
        MIDBOSS4_TRANSITION_CENTER_Y_RANGE_PX = 32,
        MIDBOSS4_TRANSITION_CENTER_Y_MIN_PX = 64,
    };
    int frame;
    if(midboss.phase_frame >= MIDBOSS4_TRANSITION_START_FRAME) {
        frame = midboss.phase_frame - MIDBOSS4_TRANSITION_START_FRAME;
        if(frame < MIDBOSS4_TRANSITION_HALF_FRAMES) {
            if(frame == 0) {
                midboss4_scratch.shot_vulnerable = 0;
                snd_se_play(13);
                midboss4_transition_center_x = midboss.pos.cur.x.v;
            }
            midboss.pos.cur.x.v = midboss4_transition_center_x;
            if(frame > MIDBOSS4_TRANSITION_SLOWDOWN_FRAME) {
                frame = MIDBOSS4_TRANSITION_SLOWDOWN_FRAME + ((frame - MIDBOSS4_TRANSITION_SLOWDOWN_FRAME) / MIDBOSS4_TRANSITION_SLOWDOWN_DIVISOR);
            }
            if(stage_frame_mod2) {
                midboss.pos.cur.x.v += frame * MIDBOSS4_TRANSITION_X_STEP_SP;
            } else {
                midboss.pos.cur.x.v -= frame * MIDBOSS4_TRANSITION_X_STEP_SP;
            }
        } else if(frame == MIDBOSS4_TRANSITION_HALF_FRAMES) {
            midboss4_transition_center_x = randring2_next16_mod(to_sp(MIDBOSS4_TRANSITION_CENTER_X_RANGE_PX)) + to_sp(MIDBOSS4_TRANSITION_CENTER_X_MIN_PX);
            midboss.pos.cur.y.v = randring2_next16_mod(to_sp(MIDBOSS4_TRANSITION_CENTER_Y_RANGE_PX)) + to_sp(MIDBOSS4_TRANSITION_CENTER_Y_MIN_PX);
        } else {
            frame = MIDBOSS4_TRANSITION_END_FRAME - frame;
            if(frame > MIDBOSS4_TRANSITION_SLOWDOWN_FRAME) {
                frame = MIDBOSS4_TRANSITION_SLOWDOWN_FRAME + ((frame - MIDBOSS4_TRANSITION_SLOWDOWN_FRAME) / MIDBOSS4_TRANSITION_SLOWDOWN_DIVISOR);
            }
            midboss.pos.cur.x.v = midboss4_transition_center_x;
            if(stage_frame_mod2) {
                midboss.pos.cur.x.v += frame * MIDBOSS4_TRANSITION_X_STEP_SP;
            } else {
                midboss.pos.cur.x.v -= frame * MIDBOSS4_TRANSITION_X_STEP_SP;
            }
            if(frame == 0) {
                midboss4_scratch.shot_vulnerable = 1;
                return true;
            }
        }
    }
    return false;
}
