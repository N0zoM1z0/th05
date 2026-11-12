/* Five levels of 16-pixel EGC text-box transition coverage, four rows each. */
#pragma option -zCCUTSCENE_BOX_MASK_DATA_TEXT -zPgroup_01
#ifdef __cplusplus
#error This semantic mask bank uses the original C initializer lane
#endif
#include "src/shared/abi.hpp"

/* The EGC repeats each four-pixel nibble across an entire 16-pixel word. */
#define EGC_REPEAT_NIBBLE(n) ((unsigned int)((n) * 0x1111U))

enum BoxMaskNibble {
    BOX_MASK_NONE = 0,
    BOX_MASK_BIT_0 = 1,
    BOX_MASK_BIT_1 = 2,
    BOX_MASK_BIT_2 = 4,
    BOX_MASK_BIT_3 = 8,
    BOX_MASK_ALTERNATING = 0xA,
    BOX_MASK_COMPLEMENT = 0x5,
    BOX_MASK_ALL = 0xF
};

const unsigned int near BOX_MASKS[5][4] = {
    { EGC_REPEAT_NIBBLE(BOX_MASK_BIT_3), EGC_REPEAT_NIBBLE(BOX_MASK_NONE),
      EGC_REPEAT_NIBBLE(BOX_MASK_BIT_1), EGC_REPEAT_NIBBLE(BOX_MASK_NONE) },
    { EGC_REPEAT_NIBBLE(BOX_MASK_BIT_3), EGC_REPEAT_NIBBLE(BOX_MASK_BIT_2),
      EGC_REPEAT_NIBBLE(BOX_MASK_BIT_1), EGC_REPEAT_NIBBLE(BOX_MASK_BIT_0) },
    { EGC_REPEAT_NIBBLE(BOX_MASK_ALTERNATING), EGC_REPEAT_NIBBLE(BOX_MASK_BIT_2),
      EGC_REPEAT_NIBBLE(BOX_MASK_ALTERNATING), EGC_REPEAT_NIBBLE(BOX_MASK_BIT_0) },
    { EGC_REPEAT_NIBBLE(BOX_MASK_ALTERNATING), EGC_REPEAT_NIBBLE(BOX_MASK_BIT_2),
      EGC_REPEAT_NIBBLE(BOX_MASK_ALTERNATING), EGC_REPEAT_NIBBLE(BOX_MASK_COMPLEMENT) },
    { EGC_REPEAT_NIBBLE(BOX_MASK_ALL), EGC_REPEAT_NIBBLE(BOX_MASK_ALL),
      EGC_REPEAT_NIBBLE(BOX_MASK_ALL), EGC_REPEAT_NIBBLE(BOX_MASK_ALL) }
};

typedef char box_mask_words_are_two[(sizeof(unsigned int) == 2) ? 1 : -1];
typedef char box_mask_rows_are_eight[(sizeof(BOX_MASKS[0]) == 8) ? 1 : -1];
typedef char box_mask_bank_is_forty[(sizeof(BOX_MASKS) == 40) ? 1 : -1];
#undef EGC_REPEAT_NIBBLE
