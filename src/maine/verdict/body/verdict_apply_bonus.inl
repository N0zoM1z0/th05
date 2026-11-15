// The bonus constants are deliberately `int`: spelling them as long literals
// changes the generated code. Only the miss/bomb factor is a long.
#define VBR_TURBO_MODE_BONUS 2000

// Calculates the "気合い" bonus from the starting lives/bombs settings, the
// game speed, grazes, and the difference of misses and bombs. Adds it to
// [skill] and renders it as a percentage.
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
        bonus += VBR_TURBO_MODE_BONUS;
    }
    if(resident->graze) {
        bonus += (resident->graze * 3);
    }
    // +200 for every miss, -200 for every bomb.
    bonus += ((resident->miss_count - resident->bombs_used) * 200L);
    if(bonus < 0) {
        bonus = 0;
    } else if(bonus > 10000) {
        bonus = 10000;
    }
    bonus *= 100; // Up to 100.00%, in millionths
    skill += bonus;
    graph_fraction_of_million_put(verdict_text_left + 176,
        verdict_text_top + 216, bonus);
    graph_putsa_fx(verdict_text_left + 272, verdict_text_top + 216,
        verdict_text_color, verdict_bonus_percent_sign);
}
