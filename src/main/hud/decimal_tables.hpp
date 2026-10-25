// Complete decimal-place factor arrays used by the native number formatters.
#ifndef TH05_HUD_DECIMAL_TABLES_HPP
#define TH05_HUD_DECIMAL_TABLES_HPP
#include "src/shared/abi.hpp"
#if GAME != 5 || BINARY != 'M'
#error These decimal-place tables belong to TH05 MAIN
#endif

extern "C" {
    extern const uint32_t near SEVEN_DIGIT_POWERS_OF_10[7];
    extern const uint16_t near FIVE_DIGIT_POWERS_OF_10[5];
}
typedef char hud_decimal_long_table_is_28[(sizeof(SEVEN_DIGIT_POWERS_OF_10) == 28) ? 1 : -1];
typedef char hud_decimal_word_table_is_10[(sizeof(FIVE_DIGIT_POWERS_OF_10) == 10) ? 1 : -1];
#endif
