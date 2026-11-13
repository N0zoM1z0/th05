// Original 16-byte Boss scratch area, with byte 15 shared by Yumeko's
// sword, fan, sweep and final-ring attack lifetimes. No extra state is added.
#ifndef TH05_MAIN_BOSS_YUMEKO_FINAL_RING_SCRATCH_HPP
#define TH05_MAIN_BOSS_YUMEKO_FINAL_RING_SCRATCH_HPP

// The final byte is one physical cell with several sequential Yumeko roles.
// The final ring resets the previous pattern state before using it as a count.
union YumekoPatternByte15 {
    unsigned char sword_pattern_angle_a;
    unsigned char fan_mirrored_side;
    unsigned char sweep_spacing;
    unsigned char final_ring_count;
};
typedef char yumeko_pattern_byte15_is_1[(sizeof(YumekoPatternByte15) == 1) ? 1 : -1];
typedef char yumeko_sword_angle_a_at_zero[(offsetof(YumekoPatternByte15, sword_pattern_angle_a) == 0) ? 1 : -1];
typedef char yumeko_fan_mirror_at_zero[(offsetof(YumekoPatternByte15, fan_mirrored_side) == 0) ? 1 : -1];
typedef char yumeko_sweep_spacing_at_zero[(offsetof(YumekoPatternByte15, sweep_spacing) == 0) ? 1 : -1];
typedef char yumeko_final_ring_count_at_zero[(offsetof(YumekoPatternByte15, final_ring_count) == 0) ? 1 : -1];

struct YumekoFinalRingScratch {
    unsigned char earlier_phase_state[14];
    unsigned char advancing_angle;
    YumekoPatternByte15 pattern_byte15;
};
typedef char yumeko_final_scratch_is_16[(sizeof(YumekoFinalRingScratch) == 16) ? 1 : -1];
typedef char yumeko_final_angle_at_14[(offsetof(YumekoFinalRingScratch, advancing_angle) == 14) ? 1 : -1];
typedef char yumeko_final_rings_at_15[(offsetof(YumekoFinalRingScratch, pattern_byte15) == 15) ? 1 : -1];

typedef struct YumekoPatternScratch {
    unsigned char earlier_phase_state[15];
    YumekoPatternByte15 pattern_byte15;
} YumekoPatternScratch;
typedef char yumeko_pattern_scratch_is_16[(sizeof(YumekoPatternScratch) == 16) ? 1 : -1];
typedef char yumeko_pattern_byte15_at_15[(offsetof(YumekoPatternScratch, pattern_byte15) == 15) ? 1 : -1];

#define yumeko_final_scratch (*reinterpret_cast<YumekoFinalRingScratch near *>(boss_statebyte))
#define yumeko_pattern_scratch (*reinterpret_cast<YumekoPatternScratch near *>(boss_statebyte))
// Compatibility name for the original fan-specific source view.
#define yumeko_fan_scratch yumeko_pattern_scratch

// Movement/reposition vs active callback are original Boss mode values.
static const unsigned char YUMEKO_MODE_REPOSITION = 0;
static const unsigned char YUMEKO_MODE_ATTACK = 1;
static const unsigned char YUMEKO_FAN_NORMAL_SIDE = 0;
static const unsigned char YUMEKO_FAN_MIRRORED_SIDE = 1;
static const unsigned char YUMEKO_WAVE_PATTERN_LIMIT = 20;

#endif
