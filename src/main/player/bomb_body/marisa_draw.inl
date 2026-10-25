void near marisa_bomb_draw(void)
{
    cdg_put_noalpha_8(112, 16, 0);
    marisa_bomb_backdrop_render();
    if(bomb_frame < 16) {
        PaletteTone = 196 - (bomb_frame * 6);
        palette_changed = true;
    } else {
        marisa_lasers_update_and_render();
        shot_time = SHOT_BLOCKED_FOR_THIS_FRAME;
    }
}
