// Stage 2 background: (re)spawns one particle at the top of the playfield,
// following the stream direction for the current point of the 4096-frame
// cycle (see stage2_transition_rules.hpp).
//
// The "frame = frame * ..." assignments have to stay in this form: a compound
// "frame <<= 3" compiles to a shorter in-place shift, which is not what the
// original code does.
#ifndef TH05_STAGE2_BG_COMBINED
#pragma option -zCSTAGE2_TEXT -zPmain_01
#endif
#include "src/main/stage/background2.hpp"
#include "src/main/stage/stage2_transition_rules.hpp"
#pragma codeseg STAGE2_TEXT main_01

void pascal near stage2_particle_init(s2particle_t near &particle)
{
    int frame = stage_frame & S2T_PARTICLE_CYCLE_MASK;
    int angle_base;
    if(frame < S2T_PARTICLE_PHASE_A_END) {
        particle.angle = randring1_next16_mod(S2T_PARTICLE_ANGLE_RANGE) + S2T_PARTICLE_ANGLE_DOWN;
        particle.pos.cur.x.v = TO_SP((S2T_PARTICLE_ANGLE_DOWN + S2T_PARTICLE_ANGLE_RANGE - particle.angle) * S2T_PARTICLE_X_PER_ANGLE) + TO_SP(S2T_PARTICLE_X_DOWN_PX);
    } else if(frame < S2T_PARTICLE_PHASE_A_TURN_END) {
        frame -= S2T_PARTICLE_PHASE_A_END;
        angle_base = (frame / S2T_PARTICLE_TURN_FRAMES_PER_ANGLE) + S2T_PARTICLE_ANGLE_DOWN;
        particle.angle = randring1_next16_mod(S2T_PARTICLE_ANGLE_RANGE) + angle_base;
        frame = frame * S2T_PARTICLE_TURN_X_SUBPIXELS_PER_FRAME;
        particle.pos.cur.x.v = TO_SP((angle_base + S2T_PARTICLE_ANGLE_RANGE - particle.angle) * S2T_PARTICLE_X_PER_ANGLE) + frame + TO_SP(S2T_PARTICLE_X_DOWN_PX);
    } else if(frame < S2T_PARTICLE_PHASE_B_END) {
        particle.angle = randring1_next16_mod(S2T_PARTICLE_ANGLE_RANGE) + S2T_PARTICLE_ANGLE_DOWN_LEFT;
        particle.pos.cur.x.v = TO_SP((S2T_PARTICLE_ANGLE_DOWN_LEFT + S2T_PARTICLE_ANGLE_RANGE - particle.angle) * S2T_PARTICLE_X_PER_ANGLE) + TO_SP(S2T_PARTICLE_X_DOWN_LEFT_PX);
    } else if(frame < S2T_PARTICLE_PHASE_B_TURN_END) {
        frame -= S2T_PARTICLE_PHASE_B_END;
        angle_base = S2T_PARTICLE_ANGLE_DOWN_LEFT - (frame / S2T_PARTICLE_TURN_FRAMES_PER_ANGLE);
        particle.angle = randring1_next16_mod(S2T_PARTICLE_ANGLE_RANGE) + angle_base;
        frame = frame * S2T_PARTICLE_TURN_X_SUBPIXELS_PER_FRAME;
        particle.pos.cur.x.v = TO_SP((angle_base + S2T_PARTICLE_ANGLE_RANGE - particle.angle) * S2T_PARTICLE_X_PER_ANGLE) + (TO_SP(S2T_PARTICLE_X_DOWN_LEFT_PX) - frame);
    } else if(frame < S2T_PARTICLE_PHASE_C_END) {
        particle.angle = randring1_next16_mod(S2T_PARTICLE_ANGLE_RANGE) + S2T_PARTICLE_ANGLE_DOWN;
        particle.pos.cur.x.v = TO_SP((S2T_PARTICLE_ANGLE_DOWN + S2T_PARTICLE_ANGLE_RANGE - particle.angle) * S2T_PARTICLE_X_PER_ANGLE) + TO_SP(S2T_PARTICLE_X_DOWN_PX);
    } else if(frame < S2T_PARTICLE_PHASE_C_TURN_END) {
        frame -= S2T_PARTICLE_PHASE_C_END;
        angle_base = S2T_PARTICLE_ANGLE_DOWN - (frame / S2T_PARTICLE_TURN_FRAMES_PER_ANGLE);
        particle.angle = randring1_next16_mod(S2T_PARTICLE_ANGLE_RANGE) + angle_base;
        frame = frame * S2T_PARTICLE_TURN_X_SUBPIXELS_PER_FRAME;
        particle.pos.cur.x.v = TO_SP((angle_base + S2T_PARTICLE_ANGLE_RANGE - particle.angle) * S2T_PARTICLE_X_PER_ANGLE) + (TO_SP(S2T_PARTICLE_X_DOWN_PX) - frame);
    } else if(frame < S2T_PARTICLE_PHASE_D_END) {
        particle.angle = randring1_next16_mod(S2T_PARTICLE_ANGLE_RANGE) + S2T_PARTICLE_ANGLE_DOWN_RIGHT;
        particle.pos.cur.x.v = TO_SP((S2T_PARTICLE_ANGLE_DOWN_RIGHT + S2T_PARTICLE_ANGLE_RANGE - particle.angle) * S2T_PARTICLE_X_PER_ANGLE);
    } else {
        frame -= S2T_PARTICLE_PHASE_D_END;
        angle_base = (frame / S2T_PARTICLE_TURN_FRAMES_PER_ANGLE) + S2T_PARTICLE_ANGLE_DOWN_RIGHT;
        particle.angle = randring1_next16_mod(S2T_PARTICLE_ANGLE_RANGE) + angle_base;
        frame = frame * S2T_PARTICLE_TURN_X_SUBPIXELS_PER_FRAME;
        particle.pos.cur.x.v = TO_SP((angle_base + S2T_PARTICLE_ANGLE_RANGE - particle.angle) * S2T_PARTICLE_X_PER_ANGLE) + frame;
    }
    particle.pos.cur.x.v += (IRand() % S2T_PARTICLE_JITTER_SPAN) * S2T_PARTICLE_SUBPIXELS_PER_PX;
    particle.zoom = S2T_PARTICLE_INITIAL_ZOOM;
    particle.pos.cur.y.v = 0;
    vector2(particle.pos.velocity.x.v, particle.pos.velocity.y.v,
        particle.angle, TO_SP(S2T_PARTICLE_SPAWN_SPEED_PX));
}
