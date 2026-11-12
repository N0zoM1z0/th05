/* Four 16-bit planar coverage masks used by the cutscene PI quarter wipe. */
#pragma option -zCCUTSCENE_PI_MASK_DATA_TEXT -zPgroup_01
#ifdef __cplusplus
#error This semantic planar-mask DATA must have a C producer
#endif
#include "src/shared/abi.hpp"

/* Source-level periodic 4-pixel coverage, not a stored image asset. */
#define PI_REPEAT_PIXELS(nibble) ((unsigned int)((nibble) * 0x1111U))

enum PiCoverageBit {
    PI_COVER_NONE = 0,
    PI_COVER_BIT_0 = 1,
    PI_COVER_BIT_1 = 2,
    PI_COVER_BIT_2 = 4,
    PI_COVER_BIT_3 = 8,
    PI_COVER_STAGGER_A = PI_COVER_BIT_3 | PI_COVER_BIT_1,
    PI_COVER_STAGGER_B = PI_COVER_BIT_2 | PI_COVER_BIT_0,
    PI_COVER_FINAL_TOP = PI_COVER_STAGGER_A | PI_COVER_BIT_2,
    PI_COVER_FINAL_SECOND = PI_COVER_STAGGER_B | PI_COVER_BIT_1,
    PI_COVER_FINAL_THIRD = PI_COVER_STAGGER_A | PI_COVER_BIT_0,
    PI_COVER_FINAL_FOURTH = PI_COVER_STAGGER_B | PI_COVER_BIT_3
};

const unsigned int near PI_MASKS[4][4] = {
    { PI_REPEAT_PIXELS(PI_COVER_NONE), PI_REPEAT_PIXELS(PI_COVER_BIT_0),
      PI_REPEAT_PIXELS(PI_COVER_NONE), PI_REPEAT_PIXELS(PI_COVER_BIT_2) },
    { PI_REPEAT_PIXELS(PI_COVER_BIT_3), PI_REPEAT_PIXELS(PI_COVER_BIT_0),
      PI_REPEAT_PIXELS(PI_COVER_BIT_1), PI_REPEAT_PIXELS(PI_COVER_BIT_2) },
    { PI_REPEAT_PIXELS(PI_COVER_STAGGER_A), PI_REPEAT_PIXELS(PI_COVER_STAGGER_B),
      PI_REPEAT_PIXELS(PI_COVER_STAGGER_A), PI_REPEAT_PIXELS(PI_COVER_STAGGER_B) },
    { PI_REPEAT_PIXELS(PI_COVER_FINAL_TOP), PI_REPEAT_PIXELS(PI_COVER_FINAL_SECOND),
      PI_REPEAT_PIXELS(PI_COVER_FINAL_THIRD), PI_REPEAT_PIXELS(PI_COVER_FINAL_FOURTH) }
};

typedef char pi_mask_word_size[(sizeof(unsigned int) == 2) ? 1 : -1];
typedef char pi_mask_row_size[(sizeof(PI_MASKS[0]) == 8) ? 1 : -1];
typedef char pi_mask_bank_size[(sizeof(PI_MASKS) == 32) ? 1 : -1];
#undef PI_REPEAT_PIXELS
