// Views of the 16 [boss_statebyte] bytes as used by stage5_setup() and each of
// Yumeko's attacks.
#ifndef TH05_MAIN_BOSS_YUMEKO_FINAL_RING_SCRATCH_HPP
#define TH05_MAIN_BOSS_YUMEKO_FINAL_RING_SCRATCH_HPP

#include <stddef.h>

// Bytes 13-15 have a different meaning in each attack.
union YumekoPatternByte13 {
    unsigned char aimed_swords_accelerated;
    unsigned char laser_swords_accelerated;
    unsigned char sweep_round;
};
union YumekoPatternByte14 {
    unsigned char paired_angle_b;
    unsigned char sweep_side;
    unsigned char final_ring_angle;
};
union YumekoPatternByte15 {
    unsigned char sword_pattern_angle_a;
    unsigned char fan_mirrored_side;
    unsigned char sweep_spacing;
    unsigned char final_ring_count;
};
typedef char yumeko_pattern_byte13_is_1[(sizeof(YumekoPatternByte13) == 1) ? 1 : -1];
typedef char yumeko_pattern_byte14_is_1[(sizeof(YumekoPatternByte14) == 1) ? 1 : -1];
typedef char yumeko_pattern_byte15_is_1[(sizeof(YumekoPatternByte15) == 1) ? 1 : -1];
typedef char yumeko_sword_angle_a_at_zero[(offsetof(YumekoPatternByte15, sword_pattern_angle_a) == 0) ? 1 : -1];
typedef char yumeko_fan_mirror_at_zero[(offsetof(YumekoPatternByte15, fan_mirrored_side) == 0) ? 1 : -1];
typedef char yumeko_sweep_spacing_at_zero[(offsetof(YumekoPatternByte15, sweep_spacing) == 0) ? 1 : -1];
typedef char yumeko_final_ring_count_at_zero[(offsetof(YumekoPatternByte15, final_ring_count) == 0) ? 1 : -1];

// stage5_setup() initializes the spawn intervals of the two stationary attacks.
struct YumekoStage5SetupScratch {
    unsigned char sword_spawn_interval; // byte 0: aimed-sword cadence
    unsigned char laser_spawn_interval; // byte 1: laser cadence
    unsigned char unused_2_to_15[14];
};

// The aimed-sword attack uses the sword interval set by stage5_setup() until
// it speeds up.
struct YumekoAimedSwordsScratch {
    unsigned char sword_spawn_interval; // byte 0
    unsigned char unused_1_to_11[11];
    unsigned char volley_frames; // byte 12
    YumekoPatternByte13 pattern_byte13; // byte 13
    YumekoPatternByte14 pattern_byte14; // byte 14
    YumekoPatternByte15 pattern_byte15; // byte 15
};

// The laser/sword attack uses the laser interval set by stage5_setup() until
// it speeds up. Bytes 12-15 are used just like in the aimed-sword attack.
struct YumekoLaserSwordsScratch {
    unsigned char unused_0;
    unsigned char laser_spawn_interval; // byte 1
    unsigned char unused_2_to_11[10];
    unsigned char volley_frames; // byte 12
    YumekoPatternByte13 pattern_byte13; // byte 13
    YumekoPatternByte14 pattern_byte14; // byte 14
    YumekoPatternByte15 pattern_byte15; // byte 15
};

// Both spread attacks keep their two angles in bytes 14 and 15.
struct YumekoSpreadScratch {
    unsigned char unused_0_to_13[14];
    YumekoPatternByte14 pattern_byte14; // byte 14
    YumekoPatternByte15 pattern_byte15; // byte 15
};

// The sword sweep's round counter, side angle and sword spacing.
struct YumekoSweepScratch {
    unsigned char unused_0_to_12[13];
    YumekoPatternByte13 pattern_byte13; // byte 13
    YumekoPatternByte14 pattern_byte14; // byte 14
    YumekoPatternByte15 pattern_byte15; // byte 15
};

// The final ring's angle and ring counter.
struct YumekoFinalRingScratch {
    unsigned char earlier_phase_state[14];
    YumekoPatternByte14 pattern_byte14; // byte 14
    YumekoPatternByte15 pattern_byte15; // byte 15
};

// The sword fan's mirrored-side flag.
struct YumekoPatternScratch {
    unsigned char earlier_phase_state[15];
    YumekoPatternByte15 pattern_byte15; // byte 15
};

union YumekoBossScratch {
    YumekoStage5SetupScratch stage5_setup;
    YumekoAimedSwordsScratch aimed_swords;
    YumekoLaserSwordsScratch laser_swords;
    YumekoSpreadScratch spreads;
    YumekoSweepScratch sweep;
    YumekoFinalRingScratch final_ring;
    YumekoPatternScratch pattern;
};

typedef char yumeko_stage5_scratch_is_16[(sizeof(YumekoStage5SetupScratch) == 16) ? 1 : -1];
typedef char yumeko_aimed_scratch_is_16[(sizeof(YumekoAimedSwordsScratch) == 16) ? 1 : -1];
typedef char yumeko_laser_scratch_is_16[(sizeof(YumekoLaserSwordsScratch) == 16) ? 1 : -1];
typedef char yumeko_spread_scratch_is_16[(sizeof(YumekoSpreadScratch) == 16) ? 1 : -1];
typedef char yumeko_sweep_scratch_is_16[(sizeof(YumekoSweepScratch) == 16) ? 1 : -1];
typedef char yumeko_final_scratch_is_16[(sizeof(YumekoFinalRingScratch) == 16) ? 1 : -1];
typedef char yumeko_pattern_scratch_is_16[(sizeof(YumekoPatternScratch) == 16) ? 1 : -1];
typedef char yumeko_boss_scratch_is_16[(sizeof(YumekoBossScratch) == 16) ? 1 : -1];

typedef char yumeko_stage5_sword_interval_at_0[(offsetof(YumekoStage5SetupScratch, sword_spawn_interval) == 0) ? 1 : -1];
typedef char yumeko_stage5_laser_interval_at_1[(offsetof(YumekoStage5SetupScratch, laser_spawn_interval) == 1) ? 1 : -1];
typedef char yumeko_aimed_sword_interval_at_0[(offsetof(YumekoAimedSwordsScratch, sword_spawn_interval) == 0) ? 1 : -1];
typedef char yumeko_aimed_volley_frames_at_12[(offsetof(YumekoAimedSwordsScratch, volley_frames) == 12) ? 1 : -1];
typedef char yumeko_aimed_byte13_at_13[(offsetof(YumekoAimedSwordsScratch, pattern_byte13) == 13) ? 1 : -1];
typedef char yumeko_aimed_byte14_at_14[(offsetof(YumekoAimedSwordsScratch, pattern_byte14) == 14) ? 1 : -1];
typedef char yumeko_aimed_byte15_at_15[(offsetof(YumekoAimedSwordsScratch, pattern_byte15) == 15) ? 1 : -1];
typedef char yumeko_laser_interval_at_1[(offsetof(YumekoLaserSwordsScratch, laser_spawn_interval) == 1) ? 1 : -1];
typedef char yumeko_laser_volley_frames_at_12[(offsetof(YumekoLaserSwordsScratch, volley_frames) == 12) ? 1 : -1];
typedef char yumeko_laser_byte13_at_13[(offsetof(YumekoLaserSwordsScratch, pattern_byte13) == 13) ? 1 : -1];
typedef char yumeko_laser_byte14_at_14[(offsetof(YumekoLaserSwordsScratch, pattern_byte14) == 14) ? 1 : -1];
typedef char yumeko_laser_byte15_at_15[(offsetof(YumekoLaserSwordsScratch, pattern_byte15) == 15) ? 1 : -1];
typedef char yumeko_spread_byte14_at_14[(offsetof(YumekoSpreadScratch, pattern_byte14) == 14) ? 1 : -1];
typedef char yumeko_spread_byte15_at_15[(offsetof(YumekoSpreadScratch, pattern_byte15) == 15) ? 1 : -1];
typedef char yumeko_sweep_byte13_at_13[(offsetof(YumekoSweepScratch, pattern_byte13) == 13) ? 1 : -1];
typedef char yumeko_sweep_byte14_at_14[(offsetof(YumekoSweepScratch, pattern_byte14) == 14) ? 1 : -1];
typedef char yumeko_sweep_byte15_at_15[(offsetof(YumekoSweepScratch, pattern_byte15) == 15) ? 1 : -1];
typedef char yumeko_final_byte14_at_14[(offsetof(YumekoFinalRingScratch, pattern_byte14) == 14) ? 1 : -1];
typedef char yumeko_final_byte15_at_15[(offsetof(YumekoFinalRingScratch, pattern_byte15) == 15) ? 1 : -1];
typedef char yumeko_pattern_byte15_at_15[(offsetof(YumekoPatternScratch, pattern_byte15) == 15) ? 1 : -1];

typedef char yumeko_stage5_view_at_zero[(offsetof(YumekoBossScratch, stage5_setup) == 0) ? 1 : -1];
typedef char yumeko_aimed_view_at_zero[(offsetof(YumekoBossScratch, aimed_swords) == 0) ? 1 : -1];
typedef char yumeko_laser_view_at_zero[(offsetof(YumekoBossScratch, laser_swords) == 0) ? 1 : -1];
typedef char yumeko_spread_view_at_zero[(offsetof(YumekoBossScratch, spreads) == 0) ? 1 : -1];
typedef char yumeko_sweep_view_at_zero[(offsetof(YumekoBossScratch, sweep) == 0) ? 1 : -1];
typedef char yumeko_final_view_at_zero[(offsetof(YumekoBossScratch, final_ring) == 0) ? 1 : -1];
typedef char yumeko_pattern_view_at_zero[(offsetof(YumekoBossScratch, pattern) == 0) ? 1 : -1];

#define yumeko_boss_scratch (*reinterpret_cast<YumekoBossScratch near *>(boss_statebyte))
#define yumeko_final_scratch yumeko_boss_scratch.final_ring
#define yumeko_pattern_scratch yumeko_boss_scratch.pattern

// Values of [boss.mode] in the mobile waves.
static const unsigned char YUMEKO_MODE_REPOSITION = 0;
static const unsigned char YUMEKO_MODE_ATTACK = 1;

static const unsigned char YUMEKO_FAN_NORMAL_SIDE = 0;
static const unsigned char YUMEKO_FAN_MIRRORED_SIDE = 1;

// Number of attacks in each mobile wave.
static const unsigned char YUMEKO_WAVE_PATTERN_LIMIT = 20;

#endif
