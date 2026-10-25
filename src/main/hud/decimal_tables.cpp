// Decimal divisors, highest place first; ordinary semantic number tables.
#pragma option -zCDECIMAL_TABLE_DATA_TEXT -zPmain_01
#include "src/main/hud/decimal_tables.hpp"

const uint32_t near SEVEN_DIGIT_POWERS_OF_10[7] = {
    1000000UL, 100000UL, 10000UL, 1000UL, 100UL, 10UL, 1UL
};
const uint16_t near FIVE_DIGIT_POWERS_OF_10[5] = {
    10000, 1000, 100, 10, 1
};
