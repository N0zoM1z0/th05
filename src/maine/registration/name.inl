void pascal near reg_name_put(int place, playchar_t pc, uint8_t cursor)
{
    register int x;
    register int y;

    switch(pc) {
    case PLAYCHAR_REIMU:
        x = 8;
        y = ((place == 0) ? 88 : ((place * 16) + 96));
        break;
    case PLAYCHAR_MARISA:
        x = 328;
        y = ((place == 0) ? 88 : ((place * 16) + 96));
        break;
    case PLAYCHAR_MIMA:
        x = 8;
        y = ((place == 0) ? 224 : ((place * 16) + 232));
        break;
    case PLAYCHAR_YUUKA:
        x = 328;
        y = ((place == 0) ? 224 : ((place * 16) + 232));
        break;
    }
    bgimage_put_rect_16(x, y, 130, 18);
    graph_gaiji_puts(
        (x + 2), (y + 2), GAIJI_W,
        reinterpret_cast<const char *>(hi.score.g_name[place]), 14
    );
    graph_gaiji_puts(
        x, y, GAIJI_W,
        reinterpret_cast<const char *>(hi.score.g_name[place]), 6
    );
    graph_gaiji_putc((x + (cursor * 16)), y,
        hi.score.g_name[place][cursor], 7);
    grcg_setcolor(GC_RMW, 7);
    grcg_hline((x + (cursor * 16)), (x + (cursor * 16) + 16), (y + 15));
    grcg_vline((x - 2), (y - 1), (y + 16));
    grcg_vline((x + 306), (y - 1), (y + 16));
    grcg_hline((x - 2), (x + 306), (y - 1));
    grcg_hline((x - 2), (x + 306), (y + 16));
    outportb(0x7C, 0);
}
