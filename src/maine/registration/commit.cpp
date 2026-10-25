// Natural typed lifecycle semantics from original TH05 sub_C16C.
// Reference: ReC98 b6ba5b0a529edbb31efdf8c0e939263804f8ee47 th05_maine.asm.
#pragma option -zCREG_COMMIT_TEXT -zPGROUP_01
#include "src/maine/registration/commit.hpp"
#pragma codeseg REG_COMMIT_TEXT GROUP_01

void near glyphballs_commit_and_wait(void)
{
    unsigned char pending = 0;
    glyphball_t near *ball;
    int i;

    snd_se_play(11);
    for((ball = glyphballs, i = 0); i < REGISTRATION_NAME_LENGTH; (i++, ball++)) {
        if(ball->phase == GBP_CLOUD_AT_ORIGIN) {
            ball->phase = GBP_FLOAT_TO_TARGET;
        }
        if(ball->phase == GBP_FLOAT_TO_TARGET) {
            ball->angle = iatan2(
                ball->target.y - ball->pos.cur.y,
                ball->target.x - ball->pos.cur.x
            );
            ball->speed.v = 6 * 16;
        }
    }
    do {
        pending = 0;
        for((i = 0, ball = glyphballs); i < REGISTRATION_NAME_LENGTH; (i++, ball++)) {
            if(ball->phase != GBP_FREE) {
                pending++;
            }
        }
        registration_frame();
    } while(pending != 0);
}
