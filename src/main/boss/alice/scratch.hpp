// Alice's view of [boss_statebyte].
#ifndef TH05_MAIN_BOSS_ALICE_SCRATCH_HPP
#define TH05_MAIN_BOSS_ALICE_SCRATCH_HPP
#include <stddef.h>

struct AliceScratch {
    unsigned char earlier_state[7];
    // Index of the current pattern wave (0-3). Incremented at the end of each
    // wave, so it ends up at 4, but nothing reads it after the fourth wave.
    unsigned char attack_wave;
    // Sprite of the puppet beam, from frame 64 of the beam pattern on.
    unsigned char beam_sprite_patnum;
    // AliceBeamPhase. Read by the puppet renderer and the puppet movement.
    unsigned char beam_phase;
    // Set to 24 when the fight starts, but never read by Alice's code.
    unsigned char ready_phase_store_only;
    unsigned char unrelated_state[4];
    // Angle of the paired stacks (starting at 8) and rotating rings (at 0).
    unsigned char charge_angle;
};
typedef char alice_scratch_is_16[(sizeof(AliceScratch) == 16) ? 1 : -1];
typedef char alice_attack_wave_at_7[(offsetof(AliceScratch, attack_wave) == 7) ? 1 : -1];
typedef char alice_beam_sprite_at_8[(offsetof(AliceScratch, beam_sprite_patnum) == 8) ? 1 : -1];
typedef char alice_beam_phase_at_9[(offsetof(AliceScratch, beam_phase) == 9) ? 1 : -1];
typedef char alice_ready_phase_store_only_at_10[(offsetof(AliceScratch, ready_phase_store_only) == 10) ? 1 : -1];
typedef char alice_charge_angle_at_15[(offsetof(AliceScratch, charge_angle) == 15) ? 1 : -1];

#define alice_scratch (*reinterpret_cast<AliceScratch near *>(boss_statebyte))
#endif
