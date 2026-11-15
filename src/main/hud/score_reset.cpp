// score_reset(): carries a beaten high score over into the resident structure
// and clears the current score. TH04's version only clears the digits.
#pragma option -G -zCSCORE_RESET_TEXT -zPmain_01
#include "src/main/hud/score_reset.hpp"

// States of the digit-by-digit comparison against the resident high score.
#define HISCORE_KEPT 0
#define HISCORE_UNDECIDED 1
#define HISCORE_BEATEN 2

// Saves the current score as the new high score if it is higher, then clears
// the score and the pending score deltas.
void near score_reset(void)
{
    int record = HISCORE_UNDECIDED;
    register int i;
    for(i = SCORE_DIGITS - 1; i > 0; i--) {
        if(record == HISCORE_UNDECIDED) {
            if(resident->score_highest.digits[i] < score.digits[i]) {
                record = HISCORE_BEATEN;
            } else if(resident->score_highest.digits[i] > score.digits[i]) {
                record = HISCORE_KEPT;
            }
        }
        if(record == HISCORE_BEATEN) {
            resident->score_highest.digits[i] = score.digits[i];
        }
        // Digit 0 counts the continues used. It is neither compared, copied
        // nor cleared here.
        score.digits[i] = 0;
    }
    score_delta = 0;
    score_delta_frame = 0;
    hiscore_popup_shown = 0;
}

#undef HISCORE_BEATEN
#undef HISCORE_UNDECIDED
#undef HISCORE_KEPT
