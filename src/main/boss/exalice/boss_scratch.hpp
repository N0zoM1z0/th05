// The 16 original per-Boss scratch bytes are reused across EX-Alice attacks.
// These names describe the update dispatcher, not independent global storage.
#ifndef TH05_MAIN_BOSS_EXALICE_BOSS_SCRATCH_HPP
#define TH05_MAIN_BOSS_EXALICE_BOSS_SCRATCH_HPP

// The last physical Boss byte is reused by several mutually exclusive
// EX-Alice attack callbacks. Keep the names together without resetting the
// value when the dispatcher changes patterns.
union ExAlicePatternByte15 {
    // Assigned at the ready-to-wave transition; no later consumer is assumed.
    unsigned char initial_fan_substate;
    unsigned char turning_ring_direction;
    unsigned char sweeping_laser_direction;
    unsigned char firewave_aim_angle;
    unsigned char diamond_ring_direction;
    unsigned char spiral_angle_offset;
    unsigned char final_fan_angle;
};
typedef char exalice_pattern_byte15_is_1[(sizeof(ExAlicePatternByte15) == 1) ? 1 : -1];
typedef char exalice_initial_fan_state_at_zero[(offsetof(ExAlicePatternByte15, initial_fan_substate) == 0) ? 1 : -1];
typedef char exalice_turning_ring_direction_at_zero[(offsetof(ExAlicePatternByte15, turning_ring_direction) == 0) ? 1 : -1];
typedef char exalice_sweep_direction_at_zero[(offsetof(ExAlicePatternByte15, sweeping_laser_direction) == 0) ? 1 : -1];
typedef char exalice_firewave_angle_at_zero[(offsetof(ExAlicePatternByte15, firewave_aim_angle) == 0) ? 1 : -1];
typedef char exalice_diamond_direction_at_zero[(offsetof(ExAlicePatternByte15, diamond_ring_direction) == 0) ? 1 : -1];
typedef char exalice_spiral_angle_at_zero[(offsetof(ExAlicePatternByte15, spiral_angle_offset) == 0) ? 1 : -1];
typedef char exalice_final_fan_angle_at_zero[(offsetof(ExAlicePatternByte15, final_fan_angle) == 0) ? 1 : -1];

struct ExAliceBossScratch {
    unsigned char earlier_pattern_state[9];
    // The four complete regular and charge wave pairs share this index.
    unsigned char wave_index;
    // During the final fan this becomes a three-step palette controller.
    unsigned char palette_step;
    unsigned char later_pattern_state[4];
    ExAlicePatternByte15 pattern_byte15;
};
typedef char exalice_scratch_is_16[(sizeof(ExAliceBossScratch) == 16) ? 1 : -1];
typedef char exalice_wave_index_at_9[(offsetof(ExAliceBossScratch, wave_index) == 9) ? 1 : -1];
typedef char exalice_palette_step_at_10[(offsetof(ExAliceBossScratch, palette_step) == 10) ? 1 : -1];
typedef char exalice_pattern_byte15_at_15[(offsetof(ExAliceBossScratch, pattern_byte15) == 15) ? 1 : -1];

// These are only the existing FINAL_FAN palette states: first drain green,
// then brighten RGB, then dim RGB until it begins brightening again.
static const unsigned char EXALICE_PALETTE_DRAIN_GREEN = 0;
static const unsigned char EXALICE_PALETTE_BRIGHTEN = 1;
static const unsigned char EXALICE_PALETTE_DIM = 2;
#define exalice_boss_scratch (*reinterpret_cast<ExAliceBossScratch near *>(boss_statebyte))

#endif
