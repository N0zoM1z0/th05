// Verdict number punctuation and counter units. The original has two "．"
// and two "回" objects; grouping the strings into structs keeps the compiler
// from merging these identical strings. (The structs are a reconstruction
// device; the code addresses each string by its own symbol.)
#ifndef TH05_MAINE_VERDICT_FORMAT_TEXT_C_H
#define TH05_MAINE_VERDICT_FORMAT_TEXT_C_H

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
#endif
