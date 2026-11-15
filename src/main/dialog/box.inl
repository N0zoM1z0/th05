// Dialog box text wipe and fade-in. Included by box.cpp, runtime.cpp and
// opcode_full_context.cpp.

// Clears the text of the box whose text area starts at (left, top).
void pascal near dialog_box_wipe(dialog_x_t left, dialog_y_t top)
{
    for(dialog_y_t y = top; y < (top + to_dialog_y(BOX_H)); y++) {
        for(dialog_x_t x = left; x < (left + to_dialog_x(TEXT_W)); x++) {
            text_putca(x, y, ' ', TX_WHITE);
        }
    }
}

// Fades in both boxes over three tile stages, 12 frames each.
void near dialog_box_fade_in_animate(void)
{
    vsync_Count1 = 0;   // ZUN bloat: frame_delay() already does this
    for(int i = 0; i < BOX_TILE_COUNT; i++) {
        dialog_box_put(BOX_BOSS_LEFT, BOX_BOSS_TOP, i);
        dialog_box_put(BOX_PLAYCHAR_LEFT, BOX_PLAYCHAR_TOP, i);
        frame_delay(12);
    }
}

