/* The five masks of the text box crossfade (box_1_to_0_masked()), from sparse
 * to fully opaque, four rows each. Also defines the color map entry count,
 * which sits right before them in the original. */
#pragma option -zCCUTSCENE_BOX_MASK_DATA_TEXT -zPgroup_01 -a2
#ifdef __cplusplus
#error This file is compiled as C
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

/* Number of color map entries defined by the running cutscene script. */
unsigned char colmap_count = 0;

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

#undef EGC_REPEAT_NIBBLE
