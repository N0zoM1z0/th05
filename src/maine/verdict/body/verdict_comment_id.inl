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
        // This resident byte is still named unknown in the canonical ABI.
        // The original comparison interprets its full unsigned byte domain.
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
