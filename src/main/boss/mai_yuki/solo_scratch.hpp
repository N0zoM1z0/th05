// The same original 16 Boss scratch bytes are reinterpreted by Mai and Yuki
// only after the survivor is chosen. This header adds no independent storage.
#ifndef TH05_MAIN_BOSS_MAI_YUKI_SOLO_SCRATCH_HPP
#define TH05_MAIN_BOSS_MAI_YUKI_SOLO_SCRATCH_HPP
#include <stddef.h>

struct MaiSoloScratch {
    unsigned char prior_phase_state[10];
    // Mai's revenge snow angle/step are initialized by the approach phase;
    // they are consumed by mai_solo_revenge_snow(), not every solo pattern.
    unsigned char revenge_snow_angle;
    unsigned char revenge_snow_step;
    unsigned char unrelated_state;
    // Mai's later laser bounce volley reinitializes this byte to -8.
    unsigned char laser_bounce_angle;
    unsigned char later_state[2];
};
struct YukiSoloScratch {
    unsigned char prior_phase_state[13];
    // Reinitialized before the final snow cross; a different pattern can
    // use these bytes in earlier phases without preserving their values.
    unsigned char snow_step;
    unsigned char snow_angle_step;
    unsigned char snow_angle;
};

typedef char mai_solo_scratch_is_16[(sizeof(MaiSoloScratch) == 16) ? 1 : -1];
typedef char mai_revenge_angle_at_10[(offsetof(MaiSoloScratch, revenge_snow_angle) == 10) ? 1 : -1];
typedef char mai_revenge_step_at_11[(offsetof(MaiSoloScratch, revenge_snow_step) == 11) ? 1 : -1];
typedef char mai_bounce_angle_at_13[(offsetof(MaiSoloScratch, laser_bounce_angle) == 13) ? 1 : -1];
typedef char yuki_solo_scratch_is_16[(sizeof(YukiSoloScratch) == 16) ? 1 : -1];
typedef char yuki_snow_step_at_13[(offsetof(YukiSoloScratch, snow_step) == 13) ? 1 : -1];
typedef char yuki_angle_step_at_14[(offsetof(YukiSoloScratch, snow_angle_step) == 14) ? 1 : -1];
typedef char yuki_angle_at_15[(offsetof(YukiSoloScratch, snow_angle) == 15) ? 1 : -1];

#define mai_solo_scratch (*reinterpret_cast<MaiSoloScratch near *>(boss_statebyte))
#define yuki_solo_scratch (*reinterpret_cast<YukiSoloScratch near *>(boss_statebyte))
#endif
