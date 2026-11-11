// Observed shared animation state for Alice's two-puppet beam.
#ifndef TH05_MAIN_BOSS_ALICE_BEAM_PHASE_HPP
#define TH05_MAIN_BOSS_ALICE_BEAM_PHASE_HPP

// State lives in the existing Boss byte array; this header owns no storage.
static const int ALICE_BEAM_PHASE_SLOT = 9;
static const int ALICE_BEAM_PATTERN_SLOT = 8;
enum AliceBeamPhase {
    ALICE_BEAM_INACTIVE = 0,
    ALICE_BEAM_CHARGE_CIRCLES = 1,
    ALICE_BEAM_CONTRACTING = 2,
    ALICE_BEAM_SPRITES = 3
};

// Milestones of alice_beam_frame, not the global stage timer.
static const int ALICE_BEAM_CHARGE_START = 16;
static const int ALICE_BEAM_CONTRACT_START = 32;
static const int ALICE_BEAM_SPRITES_START = 64;
static const int ALICE_BEAM_FIRE_START = 80;

#endif
