#include "src/maine/verdict/bonus_scoring_rules.hpp"
void near verdict_apply_bonus(void)
{
    long bonus;
    random_seed = resident->rand;
    switch(resident->credit_lives) {
    case VBR_LIVES_ONE: bonus = VBR_LIFE_BONUS_ONE; break;
    case VBR_LIVES_TWO: bonus = VBR_LIFE_BONUS_TWO; break;
    case VBR_LIVES_THREE: bonus = VBR_LIFE_BONUS_THREE; break;
    case VBR_LIVES_FOUR: bonus = VBR_LIFE_BONUS_FOUR; break;
    case VBR_LIVES_FIVE: bonus = VBR_LIFE_BONUS_FIVE; break;
    case VBR_LIVES_SIX: bonus = VBR_LIFE_BONUS_SIX; break;
    }
    switch(resident->credit_bombs) {
    case VBR_BOMBS_ZERO: bonus += VBR_BOMB_BONUS_ZERO; break;
    case VBR_BOMBS_ONE: bonus += VBR_BOMB_BONUS_ONE; break;
    case VBR_BOMBS_TWO: bonus += VBR_BOMB_BONUS_TWO; break;
    }
    if(resident->turbo_mode) {
        bonus += VBR_TURBO_MODE_BONUS;
    }
    if(resident->graze) {
        bonus += (resident->graze * VBR_GRAZE_PER_GRAZE);
    }
    bonus += ((resident->miss_count - resident->bombs_used) * VBR_MISS_MINUS_BOMB_FACTOR);
    if(bonus < VBR_BONUS_MIN) {
        bonus = VBR_BONUS_MIN;
    } else if(bonus > VBR_BONUS_MAX) {
        bonus = VBR_BONUS_MAX;
    }
    bonus *= VBR_BONUS_DISPLAY_SCALE;
    skill += bonus;
    graph_fraction_of_million_put(verdict_text_left + 176,
        verdict_text_top + 216, bonus);
    graph_putsa_fx(verdict_text_left + 272, verdict_text_top + 216,
        verdict_text_color, verdict_bonus_percent_sign);
}
