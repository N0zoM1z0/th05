// Original selector ABI shared by the live Mai/Yuki shot-hit leaf and
// the complete shared two-Boss controller. No independent state is created.
#ifndef TH05_MAI_YUKI_HIT_RESULT_HPP
#define TH05_MAI_YUKI_HIT_RESULT_HPP
#include <stddef.h>

enum MaiYukiHitResult {
    MY_HIT_NONE = 0,
    MY_HIT_MAI_DEFEATED = 1,
    MY_HIT_YUKI_DEFEATED = 2
};

// The survivor handoff reuses boss2's one-byte pattern counter as a loser
// identity. Keep that lifetime distinct from the ordinary pattern-count view.
union MaiYukiDefeatCharacterState {
    unsigned char pattern_count;
    unsigned char defeated_character;
};
typedef char mai_yuki_defeat_character_state_is_1[
    (sizeof(MaiYukiDefeatCharacterState) == 1) ? 1 : -1
];
typedef char mai_yuki_defeated_character_at_zero[
    (offsetof(MaiYukiDefeatCharacterState, defeated_character) == 0) ? 1 : -1
];
#define MY_DEFEATED_CHARACTER(phase_state_lvalue) \
    (reinterpret_cast<MaiYukiDefeatCharacterState near *>(&(phase_state_lvalue))->defeated_character)

// The defeat dialog stores the one-based hit result minus one in boss2's
// *existing* phase_state.patterns_seen byte; that is a 0/1 loser index.
static const int MY_HIT_TO_STORED_DEFEATED_INDEX = 1;
static const unsigned char MY_DEFEATED_MAI =
    MY_HIT_MAI_DEFEATED - MY_HIT_TO_STORED_DEFEATED_INDEX;
static const unsigned char MY_DEFEATED_YUKI =
    MY_HIT_YUKI_DEFEATED - MY_HIT_TO_STORED_DEFEATED_INDEX;
typedef char mai_yuki_defeated_indices_are_distinct[
    (MY_DEFEATED_MAI != MY_DEFEATED_YUKI) ? 1 : -1
];
typedef char mai_yuki_defeated_indices_fit_byte[
    (MY_DEFEATED_YUKI <= 0xFF) ? 1 : -1
];

// Combat Yuki takes a tighter and differently sounded hit test from the
// shared-fight's invulnerable opening (24px with sound 10 there).
static const int MY_YUKI_COMBAT_HIT_RADIUS_PX = 24;
static const int MY_YUKI_COMBAT_HIT_SOUND = 4;

#endif
