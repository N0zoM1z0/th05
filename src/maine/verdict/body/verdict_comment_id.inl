// Returns the record index of the second comment line, which comments on the
// way the game was played rather than on the skill value.
uint8_t near verdict_comment_id(void)
{
    if((resident->end_sequence == VERDICT_ES_GOOD) ||
        (resident->end_sequence == VERDICT_ES_EXTRA)) {
        if(resident->rank == 0) {
            return 4;
        }
        if(resident->score_last.digits[SCORE_DIGITS - 1] <= 7) {
            return 1;
        }
        if(resident->miss_count >= 6) {
            return 7;
        }
        // The purpose of this resident byte is not known. The original
        // compares it as unsigned.
        if(static_cast<uint8_t>(resident->unknown) >= 15) {
            return 8;
        }
        return 0;
    }
    if(resident->end_sequence == VERDICT_ES_BAD) {
        return 2;
    }
    if(resident->bombs_used <= (resident->miss_count * 2)) {
        return 5;
    }
    if((resident->stage >= 4) && (resident->point_items_collected <= 350)) {
        return 6;
    }
    return 3;
}
