// Complete stage-two particle initializer; only ordinary scalar rvalue scaling.
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
        particle.angle = randring1_next16_mod(S2T_PARTICLE_INITIAL_ANGLE_MASK) + S2T_PARTICLE_INITIAL_ANGLE_BIAS;
        particle.pos.cur.x.v = TO_SP((S2T_PARTICLE_X_REF_ANGLE - particle.angle) * S2T_PARTICLE_X_SLOPE) + TO_SP(S2T_PARTICLE_SPAWN_X_BIAS_PX);
    } else if(frame < S2T_PARTICLE_PHASE_A_TURN_END) {
        frame -= S2T_PARTICLE_PHASE_A_END;
        angle_base = (frame / S2T_PARTICLE_TURN_FRAMES) + S2T_PARTICLE_INITIAL_ANGLE_BIAS;
        particle.angle = randring1_next16_mod(S2T_PARTICLE_INITIAL_ANGLE_MASK) + angle_base;
        frame = frame * S2T_PARTICLE_TURN_X_SCALE;
        particle.pos.cur.x.v = TO_SP((angle_base + S2T_PARTICLE_TURN_BYTE_STEP - particle.angle) * S2T_PARTICLE_X_SLOPE) + frame + TO_SP(S2T_PARTICLE_SPAWN_X_BIAS_PX);
    } else if(frame < S2T_PARTICLE_PHASE_B_END) {
        particle.angle = randring1_next16_mod(S2T_PARTICLE_INITIAL_ANGLE_MASK) + S2T_PARTICLE_MIDDLE_ANGLE;
        particle.pos.cur.x.v = TO_SP((S2T_PARTICLE_LATE_ANGLE - particle.angle) * S2T_PARTICLE_X_SLOPE) + TO_SP(S2T_PARTICLE_MIDDLE_X_PX);
    } else if(frame < S2T_PARTICLE_PHASE_B_TURN_END) {
        frame -= S2T_PARTICLE_PHASE_B_END;
        angle_base = S2T_PARTICLE_MIDDLE_ANGLE - (frame / S2T_PARTICLE_TURN_FRAMES);
        particle.angle = randring1_next16_mod(S2T_PARTICLE_INITIAL_ANGLE_MASK) + angle_base;
        frame = frame * S2T_PARTICLE_TURN_X_SCALE;
        particle.pos.cur.x.v = TO_SP((angle_base + S2T_PARTICLE_TURN_BYTE_STEP - particle.angle) * S2T_PARTICLE_X_SLOPE) + (TO_SP(S2T_PARTICLE_MIDDLE_X_PX) - frame);
    } else if(frame < S2T_PARTICLE_PHASE_C_END) {
        particle.angle = randring1_next16_mod(S2T_PARTICLE_INITIAL_ANGLE_MASK) + S2T_PARTICLE_INITIAL_ANGLE_BIAS;
        particle.pos.cur.x.v = TO_SP((S2T_PARTICLE_X_REF_ANGLE - particle.angle) * S2T_PARTICLE_X_SLOPE) + TO_SP(S2T_PARTICLE_SPAWN_X_BIAS_PX);
    } else if(frame < S2T_PARTICLE_PHASE_C_TURN_END) {
        frame -= S2T_PARTICLE_PHASE_C_END;
        angle_base = S2T_PARTICLE_INITIAL_ANGLE_BIAS - (frame / S2T_PARTICLE_TURN_FRAMES);
        particle.angle = randring1_next16_mod(S2T_PARTICLE_INITIAL_ANGLE_MASK) + angle_base;
        frame = frame * S2T_PARTICLE_TURN_X_SCALE;
        particle.pos.cur.x.v = TO_SP((angle_base + S2T_PARTICLE_TURN_BYTE_STEP - particle.angle) * S2T_PARTICLE_X_SLOPE) + (TO_SP(S2T_PARTICLE_SPAWN_X_BIAS_PX) - frame);
    } else if(frame < S2T_PARTICLE_PHASE_D_END) {
        particle.angle = randring1_next16_mod(S2T_PARTICLE_INITIAL_ANGLE_MASK) + S2T_PARTICLE_TURN_BYTE_STEP;
        particle.pos.cur.x.v = TO_SP((S2T_PARTICLE_MIDDLE_ANGLE - particle.angle) * S2T_PARTICLE_X_SLOPE);
    } else {
        frame -= S2T_PARTICLE_PHASE_D_END;
        angle_base = (frame / S2T_PARTICLE_TURN_FRAMES) + S2T_PARTICLE_TURN_BYTE_STEP;
        particle.angle = randring1_next16_mod(S2T_PARTICLE_INITIAL_ANGLE_MASK) + angle_base;
        frame = frame * S2T_PARTICLE_TURN_X_SCALE;
        particle.pos.cur.x.v = TO_SP((angle_base + S2T_PARTICLE_TURN_BYTE_STEP - particle.angle) * S2T_PARTICLE_X_SLOPE) + frame;
    }
    particle.pos.cur.x.v += (IRand() % S2T_PARTICLE_JITTER_SPAN) * S2T_PARTICLE_SUBPIXELS_PER_PX;
    particle.zoom = S2T_PARTICLE_INITIAL_ZOOM;
    particle.pos.cur.y.v = 0;
    vector2(particle.pos.velocity.x.v, particle.pos.velocity.y.v,
        particle.angle, TO_SP(S2T_PARTICLE_SPAWN_SPEED_PX));
}
