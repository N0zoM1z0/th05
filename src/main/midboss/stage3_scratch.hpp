// Stage 3 midboss: two-phase controller and all five attack/movement helpers
// share the real sixteen-byte Boss scratch region, without new state storage.
#ifndef TH05_MAIN_MIDBOSS_STAGE3_SCRATCH_HPP
#define TH05_MAIN_MIDBOSS_STAGE3_SCRATCH_HPP
#include <stddef.h>
struct Midboss3Scratch {
    unsigned char preceding_pattern_state[13];
    unsigned char patterns_finished;
    unsigned char active_attack;
    // First half of the vertical sprite approach vs the returning half.
    unsigned char reposition_returning;
};
typedef char midboss3_scratch_is_16[(sizeof(Midboss3Scratch) == 16) ? 1 : -1];
typedef char midboss3_completed_at_13[(offsetof(Midboss3Scratch, patterns_finished) == 13) ? 1 : -1];
typedef char midboss3_attack_at_14[(offsetof(Midboss3Scratch, active_attack) == 14) ? 1 : -1];
typedef char midboss3_reposition_at_15[(offsetof(Midboss3Scratch, reposition_returning) == 15) ? 1 : -1];
#define midboss3_scratch (*reinterpret_cast<Midboss3Scratch near *>(boss_statebyte))

static const unsigned char MIDBOSS3_PHASE_ENTRANCE = 0;
static const unsigned char MIDBOSS3_PHASE_ATTACKS = 1;
static const unsigned char MIDBOSS3_ATTACK_REPOSITION = 0;
static const unsigned char MIDBOSS3_ATTACK_SPREAD_STACKS = 1;
static const unsigned char MIDBOSS3_ATTACK_AIMED_STACKS = 2;
static const unsigned char MIDBOSS3_ATTACK_DIAMOND_SPREADS = 3;
static const int MIDBOSS3_REPOSITION_TRANSITION_FRAMES = 32;
static const int MIDBOSS3_CHARGE_FRAMES = 32;
static const int MIDBOSS3_VOLLEY_FIRST_FRAME = 32;
static const int MIDBOSS3_VOLLEY_SECOND_FRAME = 48;
static const int MIDBOSS3_VOLLEY_THIRD_FRAME = 64;
static const int MIDBOSS3_PATTERN_REPOSITION_FRAME = 96;
#endif
