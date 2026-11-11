// The real sixteen-byte Boss scratch array is shared across Alice's four
// attack waves, three puppet beams and the stationary charge patterns.
#ifndef TH05_MAIN_BOSS_ALICE_SCRATCH_HPP
#define TH05_MAIN_BOSS_ALICE_SCRATCH_HPP
#include <stddef.h>

struct AliceScratch {
    unsigned char earlier_state[7];
    // Advances only when a complete regular pattern wave ends (0..3).
    unsigned char attack_wave;
    // Puppet beam emits a sprite base during the 64+ frame beam animation.
    unsigned char beam_sprite_patnum;
    // The same beam lifecycle state is read by both puppet render/motion.
    unsigned char beam_phase;
    // The ready state writes 24 here; other owners may reuse this byte.
    // Its wider meaning is not proven, so do not infer a timer or reset.
    unsigned char ready_seed;
    unsigned char unrelated_state[4];
    // Separate paired-stack and rotating-ring charge patterns reinitialize
    // this angle to 8 or 0; it is not persistent across attack families.
    unsigned char charge_angle;
};
typedef char alice_scratch_is_16[(sizeof(AliceScratch) == 16) ? 1 : -1];
typedef char alice_attack_wave_at_7[(offsetof(AliceScratch, attack_wave) == 7) ? 1 : -1];
typedef char alice_beam_sprite_at_8[(offsetof(AliceScratch, beam_sprite_patnum) == 8) ? 1 : -1];
typedef char alice_beam_phase_at_9[(offsetof(AliceScratch, beam_phase) == 9) ? 1 : -1];
typedef char alice_ready_seed_at_10[(offsetof(AliceScratch, ready_seed) == 10) ? 1 : -1];
typedef char alice_charge_angle_at_15[(offsetof(AliceScratch, charge_angle) == 15) ? 1 : -1];

#define alice_scratch (*reinterpret_cast<AliceScratch near *>(boss_statebyte))
#endif
