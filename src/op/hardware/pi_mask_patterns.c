/* The four masks that pi_put_masked_8() uses for the title screen's fade-in,
 * from sparse single pixels to almost full coverage. See ReC98
 * th03/formats/pi_put_masked[data].asm. */
#pragma option -zCOP_PI_MASK_DATA_TEXT -zPop_01
#ifdef __cplusplus
#error Compile this file as C
#endif
#include "src/shared/abi.hpp"

/* Each mask row repeats a 4-pixel pattern across 16 pixels. */
#define OP_PI_ROW(nibble) ((unsigned int)((nibble) * 0x1111U))
enum OpPiCoverage {
    OP_PI_NONE = 0,
    OP_PI_BIT_0 = 1,
    OP_PI_BIT_1 = 2,
    OP_PI_BIT_2 = 4,
    OP_PI_BIT_3 = 8,
    OP_PI_CHECKER_A = OP_PI_BIT_3 | OP_PI_BIT_1,
    OP_PI_CHECKER_B = OP_PI_BIT_2 | OP_PI_BIT_0,
    OP_PI_ALMOST_A = OP_PI_CHECKER_A | OP_PI_BIT_2,
    OP_PI_ALMOST_B = OP_PI_CHECKER_B | OP_PI_BIT_1,
    OP_PI_ALMOST_C = OP_PI_CHECKER_A | OP_PI_BIT_0,
    OP_PI_ALMOST_D = OP_PI_CHECKER_B | OP_PI_BIT_3
};

const unsigned int near PI_MASKS[4][4] = {
    { OP_PI_ROW(OP_PI_NONE), OP_PI_ROW(OP_PI_BIT_0),
      OP_PI_ROW(OP_PI_NONE), OP_PI_ROW(OP_PI_BIT_2) },
    { OP_PI_ROW(OP_PI_BIT_3), OP_PI_ROW(OP_PI_BIT_0),
      OP_PI_ROW(OP_PI_BIT_1), OP_PI_ROW(OP_PI_BIT_2) },
    { OP_PI_ROW(OP_PI_CHECKER_A), OP_PI_ROW(OP_PI_CHECKER_B),
      OP_PI_ROW(OP_PI_CHECKER_A), OP_PI_ROW(OP_PI_CHECKER_B) },
    { OP_PI_ROW(OP_PI_ALMOST_A), OP_PI_ROW(OP_PI_ALMOST_B),
      OP_PI_ROW(OP_PI_ALMOST_C), OP_PI_ROW(OP_PI_ALMOST_D) }
};

#undef OP_PI_ROW
