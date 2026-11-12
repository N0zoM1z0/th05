// Observed EX-Alice sprite slots and phase-linked visual transitions.
#ifndef TH05_EXALICE_VISUAL_PHASE_HPP
#define TH05_EXALICE_VISUAL_PHASE_HPP

// Setup switches the Boss's three movement sprites, then preconverts the
// sixteen consecutive tiny projectile sprites used by the attack phases.
enum ExAliceVisualSlots {
    EXALICE_SPRITE_STILL = 180,
    EXALICE_SPRITE_MOVE_RIGHT = 184,
    EXALICE_SPRITE_MOVE_LEFT = 186,
    EXALICE_BACKDROP_INITIAL = 196,
    EXALICE_BACKDROP_CHARGE = 200,
    EXALICE_ATTACK_TINY_FIRST = 204,
    EXALICE_ATTACK_TINY_END = 220
};

// RGB thresholds for the four wave approaches and the final fan's
// brighten/dim oscillation. The strict comparisons are intentional.
enum ExAlicePaletteLimits {
    EXALICE_APPROACH_RED_LIMIT = 96,
    EXALICE_APPROACH_BLUE_LIMIT = 96,
    EXALICE_APPROACH_WAVE3_RED_LIMIT = 48,
    EXALICE_APPROACH_WAVE4_GREEN_LIMIT = 64,
    EXALICE_FINAL_FAN_RED_PEAK = 128,
    EXALICE_POST_CHARGE_PELLET_BOTTOM_COL = 9
};

#endif
