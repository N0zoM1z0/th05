// HP thresholds, phase durations, positions and sound/score values used by
// yumeko_update().
#ifndef TH05_YUMEKO_PHASE_TIMING_HPP
#define TH05_YUMEKO_PHASE_TIMING_HPP

// HP at which each phase ends, passed to boss_phase_next().
enum YumekoHealthGates {
    YUMEKO_HP_AFTER_SETUP = 7500,
    YUMEKO_HP_AFTER_MOBILE_FIRST = 5700,
    YUMEKO_HP_AFTER_STATIONARY_FIRST = 4500,
    YUMEKO_HP_AFTER_MOBILE_SECOND = 2700,
    YUMEKO_HP_AFTER_STATIONARY_SECOND = 1200,
    YUMEKO_HP_AFTER_SWEEP = 0
};

enum YumekoPhaseClocks {
    YUMEKO_INITIAL_FRAME = 1,
    YUMEKO_ENTER_INVINCIBLE_END_FRAME = 64,
    YUMEKO_READY_END_FRAME = 64,
    YUMEKO_MOBILE_REPOSITION_FRAMES = 64,
    YUMEKO_STATIONARY_TIMEOUT_FRAMES = 2000,
    YUMEKO_FINAL_RING_TIMEOUT_FRAMES = 1200
};

enum YumekoVisualGeometry {
    // Sprites converted to tiny 32x32 sprites for the swords.
    YUMEKO_TINY_SPRITE_FIRST = 193,
    YUMEKO_TINY_SPRITE_AFTER_LAST = 229,

    YUMEKO_GATHER_RADIUS_PX = 64,
    YUMEKO_GATHER_ANGLE_DELTA = 2,
    YUMEKO_GATHER_RING_POINTS = 8,
    YUMEKO_INITIAL_VELOCITY_X_PX = 4,

    // During the entrance, the gate at [boss2] (sprite 192, see
    // yumeko_fg_render()) moves up until it is 32 pixels above the playfield.
    // Shots hitting it only play a sound.
    YUMEKO_GATE_EXIT_Y_PX = 32,
    YUMEKO_GATE_SPEED_PX = 1,
    YUMEKO_GATE_HITBOX_RADIUS_PX = 24,

    YUMEKO_ENTER_MOVE_X_STEP_PX = 2,
    YUMEKO_ARENA_CENTER_X_PX = 192,
    YUMEKO_WAVE_APPROACH_Y_PX = 64,
    YUMEKO_FINAL_APPROACH_Y_PX = 96,
    YUMEKO_BOUNCE_SPEED_PX = 2
};

enum YumekoFightEffects {
    YUMEKO_PATTERN_BONUS = 10,
    YUMEKO_DEFEAT_BONUS = 65,
    YUMEKO_ENTRANCE_END_SE = 13, // Yumeko has slid into the center.
    YUMEKO_GATE_HIT_SE = 10 // A shot hit the departing gate.
};

#endif
