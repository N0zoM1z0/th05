// Score-page navigation is a true three-state word protocol, not a bool.
// HOLD is preserved until an input edge; forward/backward motion clamps to
// the bitmap boundaries and resets the same state to HOLD.
enum StaffVerdictScrollMode {
    STAFF_SCROLL_HOLD = 0,
    STAFF_SCROLL_FORWARD = 1,
    STAFF_SCROLL_BACKWARD = 2,
};
// Original music-measure gates and deliberate input/score presentation times.
static const unsigned int STAFF_ORB_GATHER_MEASURE = 30;
static const unsigned int STAFF_ORB_OPEN_MEASURE = 48;
static const int STAFF_SCORE_PAGE_INPUT_FRAME = 400;
static const int STAFF_SCORE_SNAPSHOT_FRAME = 350;
static const int STAFF_SCORE_FIRST_VERDICT_FRAME = 256;
static const int STAFF_SCORE_FIRST_COMMENT_FRAME = 320;

void near staffroll_animate(void)
{
    int frame;
    int transition_done;
    size_t bitmap_offset;
    int slide_direction;

    verdict_text_left = 32;
    verdict_text_color = 13;
    verdict_comment_color = 13;
    verdict_text_top = 16;
    PaletteTone = 0;
    palette_show();
    grcg_setcolor(STAFF_GRCG_RMW, 1);
    outportb(0xA6, 0);
    grcg_byteboxfill_x(0, 0, (640 - 1) / 8, 400 - 1);
    outportb(0x7C, 0);
    verdict_stage_scores_put();
    verdict_bitmap_snap(STAFF_VERDICT_SCREEN_SIZE);
    grcg_setcolor(STAFF_GRCG_RMW, 1);
    grcg_byteboxfill_x(0, 0, (640 - 1) / 8, 400 - 1);
    outportb(0xA6, 1);
    grcg_byteboxfill_x(0, 0, (640 - 1) / 8, 400 - 1);
    outportb(0x7C, 0);
    snd_load(staff_bgm_filename, SND_LOAD_SONG);
    snd_kaja_interrupt(STAFF_KAJA_SONG_PLAY << 8);
    cdg_load_all_noalpha(0, staff_cdg_00_filename);
    cdg_load_all_noalpha(1, staff_cdg_01_filename);
    cdg_load_all_noalpha(2, staff_cdg_02_filename);
    cdg_load_all_noalpha(3, staff_cdg_03_filename);
    cdg_load_all_noalpha(4, staff_cdg_04_filename);
    cdg_load_all_noalpha(5, staff_cdg_05_filename);
    cdg_load_all_noalpha(6, staff_cdg_06_filename);
    cdg_load_all_noalpha(7, staff_cdg_07_filename);
    cdg_load_all_noalpha(8, staff_cdg_08_filename);
    cdg_load_all_noalpha(9, staff_cdg_09_filename);
    cdg_load_all_noalpha(10, staff_cdg_10_filename);
    super_entry_bfnt(staff_bfnt_01_filename);
    super_entry_bfnt(staff_bfnt_00_filename);
    for(frame = 0; frame < 8; frame++) {
        super_convert_tiny(frame);
    }
    Palettes.colors[0].c.b = 48;
    staff_particles_init();
    frame = 0;
    staff_frame = 0;
    do {
        if(frame <= 100) {
            PaletteTone = frame;
            palette_show();
        }
        staff_frame_advance();
        frame++;
    } while(staff_bgm_measure < STAFF_ORB_GATHER_MEASURE);
    staff_particles_gather();
    for(frame = 0; frame < 32; frame++) {
        staff_orb_particles_age();
        staff_frame_advance();
    }
    staff_particles_clear();
    do {
        frame = staff_orb_opening_update();
        staff_frame_advance();
    } while((frame == 0) || (staff_bgm_measure < STAFF_ORB_OPEN_MEASURE));

    frame = 0;
    transition_done = 0;
    do {
        staff_orb_opening_update();
        if((frame > 128) && staff_image_update_b(528, 240, 1, 76)) {
            frame = 0;
        }
        transition_done = staff_image_update_a(464, 192, 0, 76);
        staff_frame_advance();
        frame++;
    } while(transition_done == 0);
    transition_done = 0;
    do {
        staff_orb_opening_update();
        transition_done = staff_image_update_a(464, 200, 2, 92);
        staff_frame_advance();
    } while(transition_done == 0);
    frame = 0;
    transition_done = 0;
    do {
        staff_orb_opening_update();
        if((frame > 256) && staff_image_update_b(464, 224, 4, 120)) {
            frame = 0;
        }
        transition_done = staff_image_update_a(464, 176, 3, 120);
        staff_frame_advance();
        frame++;
    } while(transition_done == 0);
    staff_particles_scatter();
    do {
        frame = staff_rain_update();
        staff_frame_advance();
    } while(frame == 0);
    transition_done = 0;
    do {
        staff_rain_update();
        transition_done = staff_image_update_a(176, 200, 5, 172);
        staff_frame_advance();
    } while(transition_done == 0);
    do {
        staff_rain_update();
        transition_done = staff_image_update_a(176, 200, 6, 188);
        staff_frame_advance();
    } while(transition_done == 0);
    do {
        staff_rain_update();
        transition_done = staff_image_update_a(176, 200, 7, 204);
        staff_frame_advance();
    } while(transition_done == 0);
    do {
        staff_rain_update();
        transition_done = staff_image_update_a(176, 200, 8, 220);
        staff_frame_advance();
    } while(transition_done == 0);
    do {
        staff_rain_update();
        transition_done = staff_image_update_a(176, 200, 9, 236);
        staff_frame_advance();
    } while(transition_done == 0);

    frame = 0;
    bitmap_offset = 0;
    slide_direction = STAFF_SCROLL_HOLD;
    for(;;) {
        input_reset_sense_held();
        if((frame == STAFF_SCORE_FIRST_VERDICT_FRAME) || (frame == (STAFF_SCORE_FIRST_VERDICT_FRAME + 1))) {
            verdict_main();
        } else if((frame == STAFF_SCORE_FIRST_COMMENT_FRAME) || (frame == (STAFF_SCORE_FIRST_COMMENT_FRAME + 1))) {
            verdict_comments_put();
        } else if(frame == STAFF_SCORE_SNAPSHOT_FRAME) {
            verdict_bitmap_snap(0);
        }
        staff_rain_update();
        staff_image_update_a(176, 368, 10, STAFF_IMAGE_HOLD_MEASURE);
        frame++;
        if(frame >= STAFF_SCORE_PAGE_INPUT_FRAME) {
            if((key_det & STAFF_INPUT_CANCEL) || (key_det & STAFF_INPUT_BOMB)) {
                staff_frame_advance();
                break;
            }
            if(slide_direction == STAFF_SCROLL_HOLD) {
                if((key_det & STAFF_INPUT_SHOT) || (key_det & STAFF_INPUT_OK)) {
                    if(bitmap_offset == 0) {
                        slide_direction = STAFF_SCROLL_FORWARD;
                    } else {
                        staff_frame_advance();
                        break;
                    }
                }
                if((key_det & STAFF_INPUT_DOWN) && (bitmap_offset == 0)) {
                    slide_direction = STAFF_SCROLL_FORWARD;
                }
                if((key_det & STAFF_INPUT_UP) &&
                    (bitmap_offset == STAFF_VERDICT_SCREEN_SIZE)) {
                    slide_direction = STAFF_SCROLL_BACKWARD;
                }
            }
            if(slide_direction == STAFF_SCROLL_FORWARD) {
                bitmap_offset += STAFF_VERDICT_SCROLL_STEP;
                if(bitmap_offset > STAFF_VERDICT_SCREEN_SIZE) {
                    bitmap_offset = STAFF_VERDICT_SCREEN_SIZE;
                    slide_direction = STAFF_SCROLL_HOLD;
                }
                verdict_bitmap_put(bitmap_offset);
            } else if(slide_direction == STAFF_SCROLL_BACKWARD) {
                bitmap_offset -= STAFF_VERDICT_SCROLL_STEP;
                if(static_cast<int>(bitmap_offset) < 0) {
                    bitmap_offset = 0;
                    slide_direction = STAFF_SCROLL_HOLD;
                }
                verdict_bitmap_put(bitmap_offset);
            }
        }
        staff_frame_advance();
    }
    snd_kaja_interrupt((STAFF_KAJA_SONG_FADE << 8) | 4);
    frame = 100;
    do {
        PaletteTone = frame;
        palette_show();
        staff_rain_update();
        staff_frame_advance();
        frame--;
    } while(frame > 0);
    cdg_free_all();
    super_free();
    grc_setclip(0, 0, 640 - 1, 400 - 1);
}
