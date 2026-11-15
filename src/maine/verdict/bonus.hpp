// Verdict bonus calculation and the selection of the second comment line.
#ifndef TH05_MAINE_VERDICT_BONUS_HPP
#define TH05_MAINE_VERDICT_BONUS_HPP
#include "src/maine/verdict/format.hpp"

// Values of resident->end_sequence.
enum verdict_end_sequence_t {
    VERDICT_ES_GOOD = 0xFF,
    VERDICT_ES_BAD = 0xFE,
    VERDICT_ES_EXTRA = 0xFD,
    VERDICT_ES_INGAME = 0x37,
    VERDICT_ES_SCORE = 0
};
extern long random_seed;
extern screen_x_t verdict_text_left;
extern screen_y_t verdict_text_top;
// A separate "％" object from verdict_percent_sign. Defined in metric_ui_data.cpp.
extern const shiftjis_t near verdict_bonus_percent_sign[];

#ifdef TH05_VERDICT_FULL_FAMILY
#pragma codeseg VERDICT_FULL_TEXT group_01
#else
#pragma codeseg VERDICT_LOGIC_TEXT group_01
#endif
void near verdict_apply_bonus(void);
uint8_t near verdict_comment_id(void);
#endif
