// C semantic banks of complete UI strings; not historical struct declarations.
#ifndef TH05_MAINE_VERDICT_FORMAT_TEXT_C_H
#define TH05_MAINE_VERDICT_FORMAT_TEXT_C_H
#include <stddef.h>

typedef struct VerdictPunctuation {
    const unsigned char points_unit[3];
    const unsigned char decimal_point[3];
    const unsigned char percent_sign[3];
    const unsigned char fraction_point[3];
} VerdictPunctuation;
typedef struct VerdictCounterUnits {
    const unsigned char miss_times[3];
    const unsigned char bomb_times[3];
} VerdictCounterUnits;

extern const VerdictPunctuation near verdict_punctuation;
extern const VerdictCounterUnits near verdict_counter_units;
typedef char verdict_punctuation_size_check[(sizeof(VerdictPunctuation) == 12) ? 1 : -1];
typedef char verdict_punctuation_point_check[(offsetof(VerdictPunctuation, decimal_point) == 3) ? 1 : -1];
typedef char verdict_punctuation_percent_check[(offsetof(VerdictPunctuation, percent_sign) == 6) ? 1 : -1];
typedef char verdict_punctuation_fraction_check[(offsetof(VerdictPunctuation, fraction_point) == 9) ? 1 : -1];
typedef char verdict_counter_size_check[(sizeof(VerdictCounterUnits) == 6) ? 1 : -1];
typedef char verdict_counter_bomb_check[(offsetof(VerdictCounterUnits, bomb_times) == 3) ? 1 : -1];
#endif
