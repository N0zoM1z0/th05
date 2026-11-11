// The 16 original per-Boss scratch bytes are reused across EX-Alice attacks.
// These names describe the update dispatcher, not independent global storage.
#ifndef TH05_MAIN_BOSS_EXALICE_BOSS_SCRATCH_HPP
#define TH05_MAIN_BOSS_EXALICE_BOSS_SCRATCH_HPP

struct ExAliceBossScratch {
    unsigned char earlier_pattern_state[9];
    // The four complete regular and charge wave pairs share this index.
    unsigned char wave_index;
    // During the final fan this becomes a three-step palette controller.
    unsigned char palette_step;
    unsigned char later_pattern_state[4];
    // Reused by the initial random fan (not a persistent wave counter).
    unsigned char initial_fan_substate;
};
typedef char exalice_scratch_is_16[(sizeof(ExAliceBossScratch) == 16) ? 1 : -1];
typedef char exalice_wave_index_at_9[(offsetof(ExAliceBossScratch, wave_index) == 9) ? 1 : -1];
typedef char exalice_palette_step_at_10[(offsetof(ExAliceBossScratch, palette_step) == 10) ? 1 : -1];
typedef char exalice_fan_substate_at_15[(offsetof(ExAliceBossScratch, initial_fan_substate) == 15) ? 1 : -1];

// These are only the existing FINAL_FAN palette states: first drain green,
// then brighten RGB, then dim RGB until it begins brightening again.
static const unsigned char EXALICE_PALETTE_DRAIN_GREEN = 0;
static const unsigned char EXALICE_PALETTE_BRIGHTEN = 1;
static const unsigned char EXALICE_PALETTE_DIM = 2;
#define exalice_boss_scratch (*reinterpret_cast<ExAliceBossScratch near *>(boss_statebyte))

#endif
