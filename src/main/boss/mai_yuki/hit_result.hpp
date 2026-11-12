// Original selector ABI shared by the live Mai/Yuki shot-hit leaf and
// the complete shared two-Boss controller. No independent state is created.
#ifndef TH05_MAI_YUKI_HIT_RESULT_HPP
#define TH05_MAI_YUKI_HIT_RESULT_HPP

enum MaiYukiHitResult {
    MY_HIT_NONE = 0,
    MY_HIT_MAI_DEFEATED = 1,
    MY_HIT_YUKI_DEFEATED = 2
};

// The defeat dialog stores the one-based hit result minus one in boss2's
// *existing* phase_state.patterns_seen byte; that is a 0/1 loser index.
static const int MY_HIT_TO_STORED_DEFEATED_INDEX = 1;
static const unsigned char MY_DEFEATED_MAI =
    MY_HIT_MAI_DEFEATED - MY_HIT_TO_STORED_DEFEATED_INDEX;
static const unsigned char MY_DEFEATED_YUKI =
    MY_HIT_YUKI_DEFEATED - MY_HIT_TO_STORED_DEFEATED_INDEX;

// Combat Yuki takes a tighter and differently sounded hit test from the
// shared-fight's invulnerable opening (24px with sound 10 there).
static const int MY_YUKI_COMBAT_HIT_RADIUS_PX = 24;
static const int MY_YUKI_COMBAT_HIT_SOUND = 4;

#endif
