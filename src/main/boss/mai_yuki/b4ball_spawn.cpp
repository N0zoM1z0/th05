// Natural B4Ball pool lifecycle from original TH05 behavior. ReC98 b6ba5b0a
// b4balls_add.asm is disassembly evidence, not an instruction template.
#pragma option -zCMAIN_035_TEXT -zPmain_03
#include "src/main/boss/mai_yuki/b4ball_spawn.hpp"
#pragma codeseg MAIN_035_TEXT main_03

extern "C" void pascal near b4balls_reset(void)
{
    b4ball_t near *ball;
    int i;
    for((ball = b4balls, i = 1); i < (1 + B4BALL_COUNT); (i++, ball++)) {
        ball->flag = F_FREE;
    }
}

extern "C" void pascal near b4balls_add(void)
{
    subpixel_t speed;
    b4ball_t near *ball;
    int i;
    speed = playperf_speedtune(b4ball_template.speed.v);
    for((ball = b4balls, i = 1); i < (1 + B4BALL_COUNT); (i++, ball++)) {
        if(ball->flag != F_FREE) {
            continue;
        }
        ball->flag = F_ALIVE;
        ball->pos.cur = b4ball_template.origin;
        vector2_near(ball->pos.velocity, b4ball_template.angle, speed);
        ball->angle = b4ball_template.angle;
        // The actual allocator stores raw template speed, despite using the
        // performance-adjusted word speed to construct the initial velocity.
        ball->speed.v = b4ball_template.speed.v;
        ball->patnum_tiny_base = b4ball_template.patnum_tiny_base;
        ball->hp = b4ball_template.hp;
        ball->damaged_this_frame = 0;
        ball->revenge = b4ball_template.revenge;
        break;
    }
}
