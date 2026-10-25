int pascal near staff_image_update_b(int center_x, int center_y,
    int slot, int measure)
{
    int top = center_y;
    CDG near *image = &cdg_slots[slot];
    int row;
    int column;

    center_x -= (image->pixel_w / 2);
    top -= (image->pixel_h / 2);
    if(staff_image_phase_b <= 1) {
        staff_image_wipe_extent_b = (image->pixel_w / 16) + 7;
        staff_image_wipe_frame_b = 0;
        staff_image_phase_b++;
        cdg_put_noalpha_8(center_x, top, slot);
        for(row = 0; row <= image->pixel_h; row += 16, top += 16) {
            for(column = 0; column <= image->pixel_w; column += 16) {
                if((center_x / 8) + (column / 8) < 80) {
                    text_putsa((center_x / 8) + (column / 8), top / 16,
                        staff_image_cover_b, STAFF_TEXT_BLACK + STAFF_TEXT_REVERSE);
                }
            }
        }
    } else if(staff_image_phase_b <= 3) {
        if((++staff_image_wipe_frame_b % 4) == 0) {
            staff_image_wipe_extent_b--;
        }
        if(staff_text_wipe(center_x, top, image->pixel_w, image->pixel_h,
            staff_image_wipe_extent_b, 1) == 1) {
            staff_image_phase_b++;
            staff_image_wipe_extent_b = 0;
            staff_image_wipe_frame_b = 0;
        }
    } else if((staff_bgm_measure >= measure) &&
        (measure != STAFF_IMAGE_HOLD_MEASURE)) {
        if(staff_image_phase_b == 4) {
            if((++staff_image_wipe_frame_b % 4) == 0) {
                staff_image_wipe_extent_b++;
            }
            if(staff_text_wipe(center_x, top, image->pixel_w, image->pixel_h,
                staff_image_wipe_extent_b, -1) == 2) {
                staff_image_phase_b++;
            }
        } else {
            staff_text_wipe(center_x, top, image->pixel_w, image->pixel_h, 128, -1);
            staff_image_phase_b = 0;
            staff_text_clear_requested = 1;
            return 1;
        }
    }
    return 0;
}
