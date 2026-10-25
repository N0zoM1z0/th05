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
