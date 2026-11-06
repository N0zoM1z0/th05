void pascal near registration_stage_put(int place, int pc, int glyph)
{
    int y;
    unsigned char color;
    register int place_r = place;
    register int x;

    color = (((entered_place == place_r) &&
        (pc == static_cast<unsigned char>(playchar))) ? 7 : 2);
    switch(pc) {
    case PLAYCHAR_REIMU:
        x = 294;
        y = ((place_r == 0) ? 88 : ((place_r * 16) + 96));
        break;
    case PLAYCHAR_MARISA:
        x = 614;
        y = ((place_r == 0) ? 88 : ((place_r * 16) + 96));
        break;
    case PLAYCHAR_MIMA:
        x = 294;
        y = ((place_r == 0) ? 224 : ((place_r * 16) + 232));
        break;
    case PLAYCHAR_YUUKA:
        x = 614;
        y = ((place_r == 0) ? 224 : ((place_r * 16) + 232));
        break;
    }
    graph_gaiji_putc((x + 2), (y + 2), glyph, 14);
    graph_gaiji_putc(x, y, glyph, color);
}
