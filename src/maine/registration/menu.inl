// Both Backspace and the left command remove the current and preceding balls.
#define REGISTRATION_BACKSPACE() { \
    hi.score.g_name[entered_place][entered_name_cursor] = REG_EMPTY_GLYPH; \
    if(glyphballs[entered_name_cursor].phase != GBP_FREE) { \
        glyphballs[entered_name_cursor].phase = GBP_REMOVE_REQUEST; \
    } \
    if(entered_name_cursor > 0) { \
        entered_name_cursor--; \
    } \
    if(glyphballs[entered_name_cursor].phase != GBP_FREE) { \
        glyphballs[entered_name_cursor].phase = GBP_REMOVE_REQUEST; \
    } \
    snd_se_play(4); \
}

void near regist_menu(void)
{
    register int col;
    register int row;
    uint16_t input_lock;
    int draw_row;
    int draw_col;
    uint8_t repeat_frames = 0;
    uint8_t selected_glyph;

    graph_accesspage(0);
    outportb(0xA4, 0);
    PaletteTone = 0;
    palette_show();
    graph_accesspage(1);
    pi_load(0, registration_bg_fn);
    pi_palette_apply(0);
    pi_put_8(0, 0, 0);
    pi_free(0);
    graph_copy_page(0);
    super_entry_bfnt(registration_score_font);
    super_entry_bfnt(registration_cloud_font);
    super_entry_bfnt(registration_ball_font);

    rank = (resident->stage == STAGE_EXTRA) ? RANK_EXTRA : resident->rank;
    playchar = static_cast<playchar_t>(resident->playchar);
    for(draw_row = 0; draw_row < PLAYCHAR_COUNT; draw_row++) {
        if(playchar != draw_row) {
            hiscore_scoredat_load_for(draw_row);
            places_put(draw_row);
        }
    }
    hiscore_scoredat_load_for(playchar);
    if(resident->turbo_mode || rank == RANK_EXTRA) {
        score_insert();
        places_put(playchar);
    } else {
        entered_place = REG_NO_ENTRY;
        places_put(playchar);
        graph_putsa_fx(124, 196, 9, registration_turbo_warning_shadow);
        graph_putsa_fx(120, 192, 2, registration_turbo_warning);
    }
    bgimage_snap();
    if(resident->end_sequence >= REG_END_EXTRA &&
            resident->score_last.continues_used == 0) {
        hi.score.cleared = SCOREDAT_CLEARED;
    }
    graph_copy_page(1);
    bgimage_snap();
    snd_kaja_func(KAJA_SONG_STOP, 0);
    snd_load(registration_bgm_fn, SND_LOAD_SONG);
    snd_kaja_func(KAJA_SONG_PLAY, 0);
    palette_black_in(2);

    if(entered_place == REG_NO_ENTRY) {
        goto save_without_name;
    }
    reg_name_put(entered_place, playchar, 0);
    graph_accesspage(0);
    reg_name_put(entered_place, playchar, 0);
    graph_accesspage(1);
    for(draw_row = 0; draw_row < REGISTRATION_ALPHABET_ROWS; draw_row++) {
        for(draw_col = 0; draw_col < REGISTRATION_ALPHABET_COLS; draw_col++) {
            gaiji_putca(draw_col * 2 + 23, draw_row + 21,
                gALPHABET[draw_row * REGISTRATION_ALPHABET_COLS + draw_col],
                REG_ATTR_WHITE);
        }
    }
    gaiji_putca(23, 21, gALPHABET[0], REG_ATTR_HIGHLIGHT);
    col = 0;
    row = 0;
    input_lock = 1;
    while(1) {
        input_reset_sense_held();
        if(input_lock == 0) {
            if(static_cast<uint8_t>(key_det) & 0x0F) {
                alphabet_cursor_put(col, row, REG_ATTR_WHITE);
                if(key_det & INPUT_UP) {
                    row--;
                }
                if(key_det & INPUT_DOWN) {
                    row++;
                }
                if(key_det & INPUT_LEFT) {
                    col--;
                }
                if(key_det & INPUT_RIGHT) {
                    col++;
                }
                if(row < 0) {
                    row = REGISTRATION_ALPHABET_ROWS - 1;
                } else if(row > REGISTRATION_ALPHABET_ROWS - 1) {
                    row = 0;
                }
                if(col < 0) {
                    col = REGISTRATION_ALPHABET_COLS - 1;
                } else if(col > REGISTRATION_ALPHABET_COLS - 1) {
                    col = 0;
                }
                alphabet_cursor_put(col, row, REG_ATTR_HIGHLIGHT);
                snd_se_play(1);
            }
            if((key_det & INPUT_SHOT) || (key_det & INPUT_OK)) {
                selected_glyph = gALPHABET[row * REGISTRATION_ALPHABET_COLS + col];
                switch(selected_glyph) {
                case RA_ARROW_LEFT:
                    REGISTRATION_BACKSPACE();
                    break;
                case RA_ARROW_RIGHT:
                    snd_se_play(11);
                    if(entered_name_cursor < REGISTRATION_NAME_LENGTH - 1) {
                        entered_name_cursor++;
                    }
                    break;
                case RA_END:
                    glyphballs_commit_and_wait();
                    goto save_and_exit;
                default:
                    snd_se_play(11);
                    glyphball_spawn(col, row, entered_place, playchar, entered_name_cursor);
                    if(entered_name_cursor == REGISTRATION_NAME_LENGTH - 1) {
                        alphabet_cursor_put(col, row, REG_ATTR_WHITE);
                        col = REGISTRATION_ALPHABET_COLS - 1;
                        row = REGISTRATION_ALPHABET_ROWS - 1;
                        alphabet_cursor_put(col, row, REG_ATTR_HIGHLIGHT);
                    }
                    if(entered_name_cursor < REGISTRATION_NAME_LENGTH - 1) {
                        entered_name_cursor++;
                    }
                }
            }
            if(key_det & REG_INPUT_BOMB) {
                REGISTRATION_BACKSPACE();
            }
            if(key_det & INPUT_CANCEL) {
                glyphballs_commit_and_wait();
                goto save_and_exit;
            }
            input_lock = key_det;
        } else {
            if(key_det == input_lock) {
                repeat_frames++;
                if(repeat_frames > REG_REPEAT_DELAY && (repeat_frames & 1) == 0) {
                    input_lock = 0;
                }
            } else {
                if(key_det == INPUT_NONE) {
                    input_lock = INPUT_NONE;
                }
                repeat_frames = 0;
            }
        }
        registration_frame();
    }
save_and_exit:
    hiscore_scoredat_save();
    goto release_resources;
save_without_name:
    hiscore_scoredat_save();
    input_wait_for_change(0);
release_resources:
    bgimage_free();
    super_free();
    text_clear();
    palette_black_out(1);
}

#undef REGISTRATION_BACKSPACE
