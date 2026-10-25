// Complete resident/score and the accepted foreign formatting interfaces.
#ifndef TH05_MAINE_VERDICT_BONUS_HPP
#define TH05_MAINE_VERDICT_BONUS_HPP
#include "src/maine/verdict/format.hpp"

// The full resident end-sequence domain, shared with the actual MAINE entry.
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
// A distinct original percent object at DS:1620; no new initialized DATA.
extern const shiftjis_t near verdict_bonus_percent_sign[];

#pragma codeseg VERDICT_LOGIC_TEXT group_01
void near verdict_apply_bonus(void);
uint8_t near verdict_comment_id(void);
#endif
