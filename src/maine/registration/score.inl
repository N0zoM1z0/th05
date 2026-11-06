void pascal near registration_score_put(int place, int pc)
{
    int digit;
    int y;
    register int place_r = place;
    register int x;

    switch(pc) {
    case PLAYCHAR_REIMU:
        x = 174;
        y = ((place_r == 0) ? 88 : ((place_r * 16) + 96));
        break;
    case PLAYCHAR_MARISA:
        x = 494;
        y = ((place_r == 0) ? 88 : ((place_r * 16) + 96));
        break;
    case PLAYCHAR_MIMA:
        x = 174;
        y = ((place_r == 0) ? 224 : ((place_r * 16) + 232));
        break;
    case PLAYCHAR_YUUKA:
        x = 494;
        y = ((place_r == 0) ? 224 : ((place_r * 16) + 232));
        break;
    }
    pc = (((entered_place == place_r) &&
        (pc == static_cast<unsigned char>(playchar))) ? 10 : 0);

    if((hi.score.g_score[place_r].digits[SCORE_DIGITS - 1] - gb_0) >= 10) {
        super_put(
            (x - 32), y,
            (((hi.score.g_score[place_r].digits[SCORE_DIGITS - 1] - gb_0) / 10) + pc)
        );
    }
    super_put(
        (x - 16), y,
        (((hi.score.g_score[place_r].digits[SCORE_DIGITS - 1] - gb_0) % 10) + pc)
    );
    for(digit = 6; digit >= 0; digit--, x += 16) {
        super_put(x, y, (hi.score.g_score[place_r].digits[digit] + pc - gb_0));
    }
}
