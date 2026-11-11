// Louise's original sixteen Boss scratch bytes, shared across charge patterns.
// These fields are phase-specific views of existing storage, not new globals.
#ifndef TH05_MAIN_BOSS_LOUISE_SCRATCH_HPP
#define TH05_MAIN_BOSS_LOUISE_SCRATCH_HPP
#include <stddef.h>
struct LouiseScratch {
    unsigned char other_state[10];
    // First spread charge speed, reinitialized for the laser/ring phase.
    unsigned char charge_speed;
    unsigned char other_state_after_speed[3];
    // Alternating second-phase laser/ring selection (0 and 1).
    unsigned char next_second_phase_pattern;
    // First-phase parity; overwritten by the laser sweep's direction choice.
    unsigned char spread_or_laser_direction;
};
typedef char louise_scratch_is_16[(sizeof(LouiseScratch) == 16) ? 1 : -1];
typedef char louise_charge_speed_at_10[(offsetof(LouiseScratch, charge_speed) == 10) ? 1 : -1];
typedef char louise_pattern_choice_at_14[(offsetof(LouiseScratch, next_second_phase_pattern) == 14) ? 1 : -1];
typedef char louise_direction_at_15[(offsetof(LouiseScratch, spread_or_laser_direction) == 15) ? 1 : -1];
#define louise_scratch (*reinterpret_cast<LouiseScratch near *>(boss_statebyte))
#endif
