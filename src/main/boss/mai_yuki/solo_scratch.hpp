// The same original 16 Boss scratch bytes are reinterpreted by Mai and Yuki
// only after the survivor is chosen. This header adds no independent storage.
#ifndef TH05_MAIN_BOSS_MAI_YUKI_SOLO_SCRATCH_HPP
#define TH05_MAIN_BOSS_MAI_YUKI_SOLO_SCRATCH_HPP
#include <stddef.h>

// Byte 15 is one physical Boss scratch cell with sequential attack roles.
// The shared paired fight and the later survivor attacks reuse it rather than
// carrying independent angle/direction state across phase transitions.
union MaiYukiPatternByte15 {
    unsigned char mai_paired_sweeping_pellet_angle;
    unsigned char mai_solo_turning_stack_angle;
    unsigned char mai_solo_laser_direction;
    unsigned char mai_shared_reversing_ring_angle;
    unsigned char yuki_solo_snow_angle;
};
typedef char mai_yuki_pattern_byte15_is_1[(sizeof(MaiYukiPatternByte15) == 1) ? 1 : -1];
typedef char mai_paired_sweep_angle_at_zero[(offsetof(MaiYukiPatternByte15, mai_paired_sweeping_pellet_angle) == 0) ? 1 : -1];
typedef char mai_solo_turning_angle_at_zero[(offsetof(MaiYukiPatternByte15, mai_solo_turning_stack_angle) == 0) ? 1 : -1];
typedef char mai_solo_laser_direction_at_zero[(offsetof(MaiYukiPatternByte15, mai_solo_laser_direction) == 0) ? 1 : -1];
typedef char mai_shared_ring_angle_at_zero[(offsetof(MaiYukiPatternByte15, mai_shared_reversing_ring_angle) == 0) ? 1 : -1];
typedef char yuki_solo_snow_angle_at_zero[(offsetof(MaiYukiPatternByte15, yuki_solo_snow_angle) == 0) ? 1 : -1];

struct MaiSoloScratch {
    unsigned char prior_phase_state[10];
    // Mai's revenge snow angle/step are initialized by the approach phase;
    // they are consumed by mai_solo_revenge_snow(), not every solo pattern.
    unsigned char revenge_snow_angle;
    unsigned char revenge_snow_step;
    unsigned char unrelated_state;
    // Mai's later laser bounce volley reinitializes this byte to -8.
    unsigned char laser_bounce_angle;
    unsigned char later_state;
    MaiYukiPatternByte15 pattern_byte15;
};
struct YukiSoloScratch {
    unsigned char prior_phase_state[13];
    // Reinitialized before the final snow cross; a different pattern can
    // use these bytes in earlier phases without preserving their values.
    unsigned char snow_step;
    unsigned char snow_angle_step;
    MaiYukiPatternByte15 pattern_byte15;
};

typedef char mai_solo_scratch_is_16[(sizeof(MaiSoloScratch) == 16) ? 1 : -1];
typedef char mai_revenge_angle_at_10[(offsetof(MaiSoloScratch, revenge_snow_angle) == 10) ? 1 : -1];
typedef char mai_revenge_step_at_11[(offsetof(MaiSoloScratch, revenge_snow_step) == 11) ? 1 : -1];
typedef char mai_bounce_angle_at_13[(offsetof(MaiSoloScratch, laser_bounce_angle) == 13) ? 1 : -1];
typedef char mai_pattern_byte15_at_15[(offsetof(MaiSoloScratch, pattern_byte15) == 15) ? 1 : -1];
typedef char yuki_solo_scratch_is_16[(sizeof(YukiSoloScratch) == 16) ? 1 : -1];
typedef char yuki_snow_step_at_13[(offsetof(YukiSoloScratch, snow_step) == 13) ? 1 : -1];
typedef char yuki_angle_step_at_14[(offsetof(YukiSoloScratch, snow_angle_step) == 14) ? 1 : -1];
typedef char yuki_pattern_byte15_at_15[(offsetof(YukiSoloScratch, pattern_byte15) == 15) ? 1 : -1];

// Paired combat also uses the same physical16 bytes: the final four bytes
// are two independent character-specific angle/step pairs at offsets12..15.
struct MaiYukiPatternScratch {
    unsigned char prior_phase_state[12];
    unsigned char mai_reversing_ring_step;
    unsigned char yuki_reversing_ring_step;
    unsigned char yuki_reversing_ring_angle;
    MaiYukiPatternByte15 pattern_byte15;
};
typedef char mai_yuki_pattern_scratch_is_16[(sizeof(MaiYukiPatternScratch) == 16) ? 1 : -1];
typedef char mai_reversing_ring_step_at_12[(offsetof(MaiYukiPatternScratch, mai_reversing_ring_step) == 12) ? 1 : -1];
typedef char yuki_reversing_ring_step_at_13[(offsetof(MaiYukiPatternScratch, yuki_reversing_ring_step) == 13) ? 1 : -1];
typedef char yuki_reversing_ring_angle_at_14[(offsetof(MaiYukiPatternScratch, yuki_reversing_ring_angle) == 14) ? 1 : -1];
typedef char paired_pattern_byte15_at_15[(offsetof(MaiYukiPatternScratch, pattern_byte15) == 15) ? 1 : -1];

#define mai_solo_scratch (*reinterpret_cast<MaiSoloScratch near *>(boss_statebyte))
#define yuki_solo_scratch (*reinterpret_cast<YukiSoloScratch near *>(boss_statebyte))
#define mai_yuki_pattern_scratch (*reinterpret_cast<MaiYukiPatternScratch near *>(boss_statebyte))
#endif
