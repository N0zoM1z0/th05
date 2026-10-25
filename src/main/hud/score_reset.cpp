// Natural TH05 high-score preservation plus score clearing. The TH04 HUD
// donor supplies the ordinary digit loop; TH05's record comparison and
// distinct reset behavior are independently reconstructed from original MAIN.
#pragma option -G -zCSCORE_RESET_TEXT -zPmain_01
#include "src/main/hud/score_reset.hpp"

void near score_reset(void)
{
    int record = 1;
    register int i;
    for(i = SCORE_DIGITS - 1; i > 0; i--) {
        if(record == 1) {
            if(resident->score_highest.digits[i] < score.digits[i]) {
                record = 2;
            } else if(resident->score_highest.digits[i] > score.digits[i]) {
                record = 0;
            }
        }
        if(record == 2) {
            resident->score_highest.digits[i] = score.digits[i];
        }
        // Digit0 retains the continuation-count/least-significant slot.
        score.digits[i] = 0;
    }
    score_delta = 0;
    score_delta_frame = 0;
    hiscore_popup_shown = 0;
}
