// Preserve the original command-return bug: only line break, gaiji and
// box-begin return true; other executed commands may also print control glyphs
// when called from the text box loop.
bool pascal near dialog_op(uint8_t c)
{
    screen_x_t left;
    screen_y_t top;
    const unsigned char far *fn;
    switch(c) {
    case DIALOG_SIDE_PLAYCHAR:
        dialog_cursor.x = to_dialog_x(TEXT_PLAYCHAR_LEFT);
        dialog_cursor.y = to_dialog_y(TEXT_PLAYCHAR_TOP);
        dialog_side = SIDE_PLAYCHAR;
        break;
    case DIALOG_SIDE_BOSS:
        dialog_cursor.x = to_dialog_x(TEXT_BOSS_LEFT);
        dialog_cursor.y = to_dialog_y(TEXT_BOSS_TOP);
        dialog_side = SIDE_BOSS;
        break;
    case DIALOG_FACE:
        c = *(dialog_p++);
        frame_delay(1);
        if(dialog_side == SIDE_PLAYCHAR) {
            dialog_face_load_unput_put_free_8(FACE_PLAYCHAR_LEFT, FACE_PLAYCHAR_TOP, c);
        } else {
            dialog_face_load_unput_put_free_8(FACE_BOSS_LEFT, FACE_BOSS_TOP, c);
        }
        break;
    case DIALOG_LOAD_SPRITES:
        fn = reinterpret_cast<const unsigned char far *>(dialog_p);
        super_entry_bfnt(reinterpret_cast<const char far *>(fn));
        dialog_p += (strlen(reinterpret_cast<const char far *>(fn)) + 1);
        break;
    case DIALOG_CLEAR_STAGE_SPRITES:
        if(stage_id != STAGE_EXTRA) {
            dialog_op_super_clean_stage();
        } else {
            main_pat_exalice_override_and_super_clean_stage();
        }
        break;
    case DIALOG_MUSIC:
        fn = reinterpret_cast<const unsigned char far *>(dialog_p);
        if(fn[0] == '$') {
            snd_kaja_func(KAJA_SONG_STOP, 0);
        } else {
            snd_load(reinterpret_cast<const char far *>(fn), SND_LOAD_SONG);
            snd_kaja_func(KAJA_SONG_PLAY, 0);
        }
        dialog_p += (strlen(reinterpret_cast<const char far *>(fn)) + 1);
        break;
    case DIALOG_PUT_SPRITE:
        left = reinterpret_cast<tx2_op_06_params far *>(dialog_p)->left;
        top = reinterpret_cast<tx2_op_06_params far *>(dialog_p)->top;
        c = reinterpret_cast<tx2_op_06_params far *>(dialog_p)->patnum;
        dialog_p += sizeof(tx2_op_06_params);
        super_roll_put(left, top, c);
        break;
    case DIALOG_WHITE_OUT:
        dialog_box_wipe(to_dialog_x(TEXT_BOSS_LEFT), to_dialog_y(TEXT_BOSS_TOP));
        dialog_box_wipe(to_dialog_x(TEXT_PLAYCHAR_LEFT), to_dialog_y(TEXT_PLAYCHAR_TOP));
        c = *(dialog_p++);
        palette_white_out(c);
        break;
    case DIALOG_WHITE_IN:
        c = *(dialog_p++);
        palette_white_in(c);
        break;
    case DIALOG_LINEBREAK:
        dialog_op_linebreak();
        return true;
    case DIALOG_GAIJI:
        c = *(dialog_p++);
        dialog_op_gaiji(c);
        return true;
    case DIALOG_BOX_BEGIN:
        return true;
    case DIALOG_BOX_WIPE:
        dialog_box_wipe(dialog_cursor.x, dialog_cursor.y);
        break;
    }
    return false;
}
