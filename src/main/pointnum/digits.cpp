// Natural C++ recovery; source semantics and native exactness are separate.
#pragma option -zCPOINTNUM_DIGITS_TEXT -zPmain_03 -k-
#include "src/main/pointnum/digits.hpp"

extern "C" unsigned int pascal near pointnum_digits_set(
    unsigned char near *last_digit, uint16_t points
)
{
    unsigned int first_nonzero = 0;
    const uint16_t near *power = FIVE_DIGIT_POWERS_OF_10;
    unsigned int remaining = 4;
    do {
        unsigned int digit = points / *power;
        points %= *power;
        *last_digit = digit;
        if(digit && !first_nonzero) {
            first_nonzero = remaining;
        }
        last_digit--;
        power++;
    } while(--remaining);
    *last_digit = points;
    // One units digit and the implicit trailing zero are always displayed.
    return (first_nonzero + 2) * 8;
}
