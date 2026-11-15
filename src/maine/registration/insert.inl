// Inserts the score of the run that just ended into the loaded score table,
// setting [entered_place] to the new row or to 0xFF if the score is too low.
// Structured like TH04's version; ReC98 does not name this function.
void near score_insert(void)
{
    int compared_place;
    int digit_index;

    // Walk upward from the lowest table row, comparing from the most
    // significant digit. Stored scores are gaiji digits (gb_0 + 0..9), while
    // resident->score_last holds plain digits. Equal scores keep walking
    // upward, so the new score is placed above existing equal ones.
    for(
        compared_place = (SCOREDAT_PLACES - 1);
        compared_place >= 0;
        compared_place--
    ) {
        for(digit_index = (SCORE_DIGITS - 1); digit_index >= 0; digit_index--) {
            if(
                resident->score_last.digits[digit_index] >
                (hi.score.g_score[compared_place]
                    .digits[digit_index] - gb_0)
            ) {
                break;
            }
            if(
                resident->score_last.digits[digit_index] <
                (hi.score.g_score[compared_place]
                    .digits[digit_index] - gb_0)
            ) {
                goto lower_than_compared_place;
            }
        }
    }
    entered_place = 0;
    goto shift_lower_places;

lower_than_compared_place:
    if(compared_place == (SCOREDAT_PLACES - 1)) {
        // Lower than the last row: leave the table untouched. regist_menu()
        // checks for the resulting 0xFF.
        entered_place = -1;
        return;
    }
    entered_place = (compared_place + 1);

shift_lower_places:
    // Make room by moving the lower rows down. The ninth name byte is the
    // terminator written by scoredat_recreate(), so only the eight glyphs
    // need to move.
    for(
        compared_place = (SCOREDAT_PLACES - 2);
        compared_place >= entered_place;
        compared_place--
    ) {
        for(
            digit_index = (SCOREDAT_NAME_LEN - 1);
            digit_index >= 0;
            digit_index--
        ) {
            hi.score.g_name[compared_place + 1][digit_index] =
                hi.score.g_name[compared_place][digit_index];
        }
        for(digit_index = (SCORE_DIGITS - 1); digit_index >= 0; digit_index--) {
            hi.score.g_score[compared_place + 1]
                .digits[digit_index] = hi.score
                .g_score[compared_place].digits[digit_index];
        }
        hi.score.g_stage[compared_place + 1] =
            hi.score.g_stage[compared_place];
    }

    // Clear the new name, convert the score to gaiji digits, and store either
    // the reached stage or the "All" marker for the endings (end_sequence >=
    // ES_EXTRA).
    for(digit_index = (SCOREDAT_NAME_LEN - 1); digit_index >= 0; digit_index--) {
        hi.score.g_name[entered_place][digit_index] =
            gs_DOT;
    }
    for(digit_index = (SCORE_DIGITS - 1); digit_index >= 0; digit_index--) {
        hi.score.g_score[entered_place]
            .digits[digit_index] = (
                resident->score_last.digits[digit_index] + gb_0
            );
    }
    if(resident->end_sequence >= REG_INSERT_EXTRA) {
        hi.score.g_stage[entered_place] = REG_INSERT_ALL;
    } else if(rank < RANK_EXTRA) {
        hi.score.g_stage[entered_place] = (
            resident->stage + gb_1
        );
    } else {
        hi.score.g_stage[entered_place] = gb_1;
    }
}
