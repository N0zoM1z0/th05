// The 16 original per-Boss scratch bytes are reused across EX-Alice attacks.
// These names describe the update dispatcher, not independent global storage.
#ifndef TH05_MAIN_BOSS_EXALICE_BOSS_SCRATCH_HPP
#define TH05_MAIN_BOSS_EXALICE_BOSS_SCRATCH_HPP

// The last physical Boss byte is reused by several mutually exclusive
// EX-Alice attack callbacks. Keep the names together without resetting the
// value when the dispatcher changes patterns.
union ExAlicePatternByte15 {
    // Ready seeds this byte; the first consumer is the turning-ring direction.
    unsigned char ready_direction_seed;
    unsigned char turning_ring_direction;
    unsigned char sweeping_laser_direction;
    unsigned char firewave_aim_angle;
    unsigned char diamond_ring_direction;
    unsigned char spiral_angle_offset;
    unsigned char final_fan_angle;
};
typedef char exalice_pattern_byte15_is_1[(sizeof(ExAlicePatternByte15) == 1) ? 1 : -1];
typedef char exalice_ready_direction_seed_at_zero[(offsetof(ExAlicePatternByte15, ready_direction_seed) == 0) ? 1 : -1];
typedef char exalice_turning_ring_direction_at_zero[(offsetof(ExAlicePatternByte15, turning_ring_direction) == 0) ? 1 : -1];
typedef char exalice_sweep_direction_at_zero[(offsetof(ExAlicePatternByte15, sweeping_laser_direction) == 0) ? 1 : -1];
typedef char exalice_firewave_angle_at_zero[(offsetof(ExAlicePatternByte15, firewave_aim_angle) == 0) ? 1 : -1];
typedef char exalice_diamond_direction_at_zero[(offsetof(ExAlicePatternByte15, diamond_ring_direction) == 0) ? 1 : -1];
typedef char exalice_spiral_angle_at_zero[(offsetof(ExAlicePatternByte15, spiral_angle_offset) == 0) ? 1 : -1];
typedef char exalice_final_fan_angle_at_zero[(offsetof(ExAlicePatternByte15, final_fan_angle) == 0) ? 1 : -1];

// The later firewave and spiral attacks reuse bytes 13/14 as a two-stage
// turn controller plus an attack-specific angle/acceleration value.
struct ExAliceFirewaveState {
    unsigned char byte_11;
    unsigned char byte_12;
    unsigned char turn_phase;
    unsigned char angle;
};
struct ExAliceSpiralState {
    unsigned char byte_11;
    unsigned char byte_12;
    unsigned char turn_phase;
    unsigned char acceleration_step;
};
union ExAliceLaterPatternState {
    unsigned char bytes[4];
    ExAliceFirewaveState firewave;
    ExAliceSpiralState spiral;
};
typedef char exalice_firewave_state_is_4[(sizeof(ExAliceFirewaveState) == 4) ? 1 : -1];
typedef char exalice_spiral_state_is_4[(sizeof(ExAliceSpiralState) == 4) ? 1 : -1];
typedef char exalice_later_state_is_4[(sizeof(ExAliceLaterPatternState) == 4) ? 1 : -1];
typedef char exalice_firewave_turn_phase_at_2[(offsetof(ExAliceFirewaveState, turn_phase) == 2) ? 1 : -1];
typedef char exalice_firewave_angle_at_3[(offsetof(ExAliceFirewaveState, angle) == 3) ? 1 : -1];
typedef char exalice_spiral_turn_phase_at_2[(offsetof(ExAliceSpiralState, turn_phase) == 2) ? 1 : -1];
typedef char exalice_spiral_acceleration_step_at_3[(offsetof(ExAliceSpiralState, acceleration_step) == 3) ? 1 : -1];

struct ExAliceBossScratch {
    unsigned char earlier_pattern_state[9];
    // The four complete regular and charge wave pairs share this index.
    unsigned char wave_index;
    // During the final fan this becomes a three-step palette controller.
    unsigned char palette_step;
    ExAliceLaterPatternState later_pattern_state;
    ExAlicePatternByte15 pattern_byte15;
};
typedef char exalice_scratch_is_16[(sizeof(ExAliceBossScratch) == 16) ? 1 : -1];
typedef char exalice_wave_index_at_9[(offsetof(ExAliceBossScratch, wave_index) == 9) ? 1 : -1];
typedef char exalice_palette_step_at_10[(offsetof(ExAliceBossScratch, palette_step) == 10) ? 1 : -1];
typedef char exalice_later_pattern_state_at_11[(offsetof(ExAliceBossScratch, later_pattern_state) == 11) ? 1 : -1];
typedef char exalice_firewave_turn_phase_at_13[(offsetof(ExAliceBossScratch, later_pattern_state) + offsetof(ExAliceFirewaveState, turn_phase)) == 13 ? 1 : -1];
typedef char exalice_firewave_angle_at_14[(offsetof(ExAliceBossScratch, later_pattern_state) + offsetof(ExAliceFirewaveState, angle)) == 14 ? 1 : -1];
typedef char exalice_spiral_acceleration_step_at_14[(offsetof(ExAliceBossScratch, later_pattern_state) + offsetof(ExAliceSpiralState, acceleration_step)) == 14 ? 1 : -1];
typedef char exalice_pattern_byte15_at_15[(offsetof(ExAliceBossScratch, pattern_byte15) == 15) ? 1 : -1];

// These are only the existing FINAL_FAN palette states: first drain green,
// then brighten RGB, then dim RGB until it begins brightening again.
static const unsigned char EXALICE_PALETTE_DRAIN_GREEN = 0;
static const unsigned char EXALICE_PALETTE_BRIGHTEN = 1;
static const unsigned char EXALICE_PALETTE_DIM = 2;
#define exalice_boss_scratch (*reinterpret_cast<ExAliceBossScratch near *>(boss_statebyte))

#endif
