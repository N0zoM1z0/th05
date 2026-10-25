// Complete stage-two particle initializer; only ordinary scalar rvalue scaling.
#ifndef TH05_STAGE2_BG_COMBINED
#pragma option -zCSTAGE2_TEXT -zPmain_01
#endif
#include "src/main/stage/background2.hpp"
#pragma codeseg STAGE2_TEXT main_01

void pascal near stage2_particle_init(s2particle_t near &particle)
{
    int frame = stage_frame & 4095;
    int angle_base;
    if(frame < 1000) {
        particle.angle = randring1_next16_mod(0x20) + 0x30;
        particle.pos.cur.x.v = TO_SP((0x50 - particle.angle) * 8) + TO_SP(64);
    } else if(frame < 1128) {
        frame -= 1000;
        angle_base = (frame / 8) + 0x30;
        particle.angle = randring1_next16_mod(0x20) + angle_base;
        frame = frame * 8;
        particle.pos.cur.x.v = TO_SP((angle_base + 0x20 - particle.angle) * 8) + frame + TO_SP(64);
    } else if(frame < 2000) {
        particle.angle = randring1_next16_mod(0x20) + 0x40;
        particle.pos.cur.x.v = TO_SP((0x60 - particle.angle) * 8) + TO_SP(128);
    } else if(frame < 2128) {
        frame -= 2000;
        angle_base = 0x40 - (frame / 8);
        particle.angle = randring1_next16_mod(0x20) + angle_base;
        frame = frame * 8;
        particle.pos.cur.x.v = TO_SP((angle_base + 0x20 - particle.angle) * 8) + (TO_SP(128) - frame);
    } else if(frame < 3000) {
        particle.angle = randring1_next16_mod(0x20) + 0x30;
        particle.pos.cur.x.v = TO_SP((0x50 - particle.angle) * 8) + TO_SP(64);
    } else if(frame < 3128) {
        frame -= 3000;
        angle_base = 0x30 - (frame / 8);
        particle.angle = randring1_next16_mod(0x20) + angle_base;
        frame = frame * 8;
        particle.pos.cur.x.v = TO_SP((angle_base + 0x20 - particle.angle) * 8) + (TO_SP(64) - frame);
    } else if(frame < 3968) {
        particle.angle = randring1_next16_mod(0x20) + 0x20;
        particle.pos.cur.x.v = TO_SP((0x40 - particle.angle) * 8);
    } else {
        frame -= 3968;
        angle_base = (frame / 8) + 0x20;
        particle.angle = randring1_next16_mod(0x20) + angle_base;
        frame = frame * 8;
        particle.pos.cur.x.v = TO_SP((angle_base + 0x20 - particle.angle) * 8) + frame;
    }
    particle.pos.cur.x.v += (IRand() % 8) * 16;
    particle.zoom = 8;
    particle.pos.cur.y.v = 0;
    vector2(particle.pos.velocity.x.v, particle.pos.velocity.y.v,
        particle.angle, TO_SP(8));
}
