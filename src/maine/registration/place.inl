void pascal near registration_place_put(int place, int pc)
{
    int x;
    register int place_r = place;
    register int y;

    switch(pc) {
    case PLAYCHAR_REIMU:
        x = 8;
        y = ((place_r == 0) ? 88 : ((place_r * 16) + 96));
        break;
    case PLAYCHAR_MARISA:
        x = 328;
        y = ((place_r == 0) ? 88 : ((place_r * 16) + 96));
        break;
    case PLAYCHAR_MIMA:
        x = 8;
        y = ((place_r == 0) ? 224 : ((place_r * 16) + 232));
        break;
    case PLAYCHAR_YUUKA:
        x = 328;
        y = ((place_r == 0) ? 224 : ((place_r * 16) + 232));
        break;
    }
    registration_score_put(place_r, pc);
    registration_stage_put(place_r, pc, hi.score.g_stage[place_r]);
    if((static_cast<unsigned char>(playchar) != pc) || (entered_place != place_r)) {
        graph_gaiji_puts(
            (x + 2), (y + 2), GAIJI_W,
            reinterpret_cast<const char *>(hi.score.g_name[place_r]), 14
        );
        graph_gaiji_puts(
            x, y, GAIJI_W,
            reinterpret_cast<const char *>(hi.score.g_name[place_r]), 2
        );
    }
}
