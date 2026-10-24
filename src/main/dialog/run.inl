void near dialog_run(void)
{
    uint8_t c;
    uint8_t speedup_cycle;
    shiftjis_t far *kanji_str = dialog_kanji_buf;
    while(1) {
        c = *(dialog_p++);
        if(c == DIALOG_END) {
            break;
        } else if(c == DIALOG_BOX_BEGIN) {
            if(dialog_side == SIDE_PLAYCHAR) {
                dialog_cursor.x = to_dialog_x(TEXT_PLAYCHAR_LEFT);
                dialog_cursor.y = to_dialog_y(TEXT_PLAYCHAR_TOP);
            } else {
                dialog_cursor.x = to_dialog_x(TEXT_BOSS_LEFT);
                dialog_cursor.y = to_dialog_y(TEXT_BOSS_TOP);
            }
            text_boxfilla(to_tram_x(to_dialog_x(TEXT_PLAYCHAR_LEFT)),
                to_tram_y(to_dialog_y(TEXT_PLAYCHAR_TOP)),
                to_tram_x(to_dialog_x(TEXT_PLAYCHAR_LEFT + TEXT_W)),
                to_tram_y(to_dialog_y(TEXT_PLAYCHAR_TOP + BOX_H)), TX_BLUE);
            text_boxfilla(to_tram_x(to_dialog_x(TEXT_BOSS_LEFT)),
                to_tram_y(to_dialog_y(TEXT_BOSS_TOP)),
                to_tram_x(to_dialog_x(TEXT_BOSS_LEFT + TEXT_W)),
                to_tram_y(to_dialog_y(TEXT_BOSS_TOP + BOX_H)), TX_BLUE);
            dialog_box_wipe(dialog_cursor.x, dialog_cursor.y);
            speedup_cycle = 0;
            while(1) {
                input_reset_sense();
                c = *(dialog_p++);
                if(c == DIALOG_END) {
                    input_wait_for_change(0);
                    break;
                } else if(!dialog_op(c)) {
                    kanji_str[0] = c;
                    kanji_str[1] = *(dialog_p++);
                    dialog_text_put(kanji_str);
                    input_sense();
                    dialog_delay(speedup_cycle);
                }
            }
        } else {
            dialog_op(c);
        }
    }
    overlay_wipe();
}
