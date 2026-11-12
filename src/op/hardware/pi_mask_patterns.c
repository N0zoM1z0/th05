/* Four actual PC-98 PI fade mask phases used by the TH05 OP title fade. */
#pragma option -zCOP_PI_MASK_DATA_TEXT -zPop_01
#ifdef __cplusplus
#error OP PI-mask DATA requires a C compiler producer
#endif
#include "src/shared/abi.hpp"

/* A 4-pixel nibble repeats across each of the four 16-bit scanlines. */
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

typedef char op_pi_mask_word_is_two[(sizeof(unsigned int) == 2) ? 1 : -1];
typedef char op_pi_mask_row_is_eight[(sizeof(PI_MASKS[0]) == 8) ? 1 : -1];
typedef char op_pi_mask_bank_is_thirtytwo[(sizeof(PI_MASKS) == 32) ? 1 : -1];
#undef OP_PI_ROW
