// Complete natural reflecting random movement, original MAIN1D8BE..1D938.
#include "src/main/boss/louise/flystep.hpp"

bool pascal near louise_flystep(subpixel_t speed, int end_frame)
{
    unsigned char angle;
    if(boss.phase_frame == 1) {
        angle = randring2_next16();
        vector2(boss.pos.velocity.x.v, boss.pos.velocity.y.v, angle, speed);
    }
    boss.pos.cur.x.v += boss.pos.velocity.x.v;
    boss.pos.cur.y.v += boss.pos.velocity.y.v;
    if((boss.pos.cur.x.v <= to_sp(48)) || (boss.pos.cur.x.v >= to_sp(336))) {
        boss.pos.velocity.x.v *= -1;
    }
    if((boss.pos.cur.y.v <= to_sp(48)) || (boss.pos.cur.y.v >= to_sp(96))) {
        boss.pos.velocity.y.v *= -1;
    }
    if(boss.phase_frame >= end_frame) {
        return true;
    }
    return false;
}
