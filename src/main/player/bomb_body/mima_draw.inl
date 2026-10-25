void near mima_bomb_draw(void)
{
    int radius;
    cdg_put_noalpha_8(64, 64, 0);
    mima_bomb_backdrop_render();
    grcg_setcolor(MIMA_BOMB_GRCG_RMW, 7);
    grcg_vline(209, PLAYFIELD_TOP, PLAYFIELD_TOP + 47);
    grcg_vline(209, 336, PLAYFIELD_BOTTOM - 1);
    grcg_vline(238, PLAYFIELD_TOP, PLAYFIELD_TOP + 47);
    grcg_vline(238, 336, PLAYFIELD_BOTTOM - 1);

    // AH is the genuine existing GRCG color API's register input.
    _AH = 6;
    grcg_setcolor_direct_raw();
    grcg_vline(208, PLAYFIELD_TOP, PLAYFIELD_TOP + 47);
    grcg_vline(208, 336, PLAYFIELD_BOTTOM - 1);
    grcg_vline(239, PLAYFIELD_TOP, PLAYFIELD_TOP + 47);
    grcg_vline(239, 336, PLAYFIELD_BOTTOM - 1);
    _AH = V_WHITE;
    grcg_setcolor_direct_raw();
    mima_circles_update_and_render();
    radius = 224 - bomb_frame;
    if(radius > 0) {
        grcg_circle(224, 117, radius);
    }
    outportb(0x7C, 0);
    PaletteTone = 100 + bomb_frame;
    palette_changed = true;
}

