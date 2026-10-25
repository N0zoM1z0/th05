// Natural complete TH05 verdict bonus and comment selection, C8AE..CA9B.
#pragma option -zCVERDICT_LOGIC_TEXT -zPgroup_01
#include "src/maine/verdict/bonus.hpp"

void near verdict_apply_bonus(void)
{
    long bonus;
    random_seed = resident->rand;
    switch(resident->credit_lives) {
    case 1: bonus = 2500; break;
    case 2: bonus = 2000; break;
    case 3: bonus = 1500; break;
    case 4: bonus = 1000; break;
    case 5: bonus = 500; break;
    case 6: bonus = 0; break;
    }
    switch(resident->credit_bombs) {
    case 0: bonus += 2500; break;
    case 1: bonus += 1500; break;
    case 2: bonus += 1000; break;
    }
    if(resident->turbo_mode) {
        bonus += 2000;
    }
    if(resident->graze) {
        bonus += (resident->graze * 3);
    }
    bonus += ((resident->miss_count - resident->bombs_used) * 200L);
    if(bonus < 0) {
        bonus = 0;
    } else if(bonus > 10000) {
        bonus = 10000;
    }
    bonus *= 100;
    skill += bonus;
    graph_fraction_of_million_put(verdict_text_left + 176,
        verdict_text_top + 216, bonus);
    graph_putsa_fx(verdict_text_left + 272, verdict_text_top + 216,
        verdict_text_color, verdict_bonus_percent_sign);
}

// Returns the byte index into the separate commentary section of _ude.txt.
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
