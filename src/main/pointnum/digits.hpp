// Five little-endian decimal digits; the trailing zero is rendered separately.
#ifndef TH05_POINTNUM_DIGITS_HPP
#define TH05_POINTNUM_DIGITS_HPP
#include "src/main/hud/decimal_tables.hpp"
#pragma codeseg POINTNUM_DIGITS_TEXT main_03
extern "C" unsigned int pascal near pointnum_digits_set(
    unsigned char near *last_digit, uint16_t points
);
#endif
