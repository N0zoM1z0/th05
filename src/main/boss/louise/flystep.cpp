// Complete natural reflecting random movement, original MAIN1D8BE..1D938.
#include "src/main/boss/louise/flystep.hpp"
#include "src/main/boss/louise/flystep_bounds.hpp"

bool pascal near louise_flystep(subpixel_t speed, int end_frame)
{
    unsigned char angle;
    if(boss.phase_frame == LOUISE_FLYSTEP_FIRST_FRAME) {
        angle = randring2_next16();
        vector2(boss.pos.velocity.x.v, boss.pos.velocity.y.v, angle, speed);
    }
    boss.pos.cur.x.v += boss.pos.velocity.x.v;
    boss.pos.cur.y.v += boss.pos.velocity.y.v;
    if((boss.pos.cur.x.v <= to_sp(LOUISE_BOUNCE_LEFT_PX)) || (boss.pos.cur.x.v >= to_sp(LOUISE_BOUNCE_RIGHT_PX))) {
        boss.pos.velocity.x.v *= -1;
    }
    if((boss.pos.cur.y.v <= to_sp(LOUISE_BOUNCE_TOP_PX)) || (boss.pos.cur.y.v >= to_sp(LOUISE_BOUNCE_BOTTOM_PX))) {
        boss.pos.velocity.y.v *= -1;
    }
    if(boss.phase_frame >= end_frame) {
        return true;
    }
    return false;
}
