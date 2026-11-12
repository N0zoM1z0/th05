#include "src/maine/staff/image_reveal_choreography.hpp"
int pascal near staff_image_update_a(int center_x, int center_y,
    int slot, int measure)
{
    int top = center_y;
    CDG near *image = &cdg_slots[slot];
    int row;
    int column;

    center_x -= (image->pixel_w / 2);
    top -= (image->pixel_h / 2);
    if(staff_image_phase_a <= STIMG_PHASE_PREPARE_LAST) {
        staff_image_wipe_extent_a = ((image->pixel_w / STIMG_CELL_WIDTH_PX) + STIMG_WIPE_PREPARE_LEAD);
        staff_image_wipe_frame_a = 0;
        staff_image_phase_a++;
        cdg_put_noalpha_8(center_x, top, slot);
        for(row = 0; row <= image->pixel_h; (row += STIMG_CELL_HEIGHT_PX, top += STIMG_CELL_HEIGHT_PX)) {
            for(column = 0; column <= image->pixel_w; column += STIMG_CELL_WIDTH_PX) {
                if(((center_x / STIMG_TEXT_BYTE_WIDTH) + (column / STIMG_TEXT_BYTE_WIDTH)) < STIMG_SCREEN_TEXT_COLS) {
                    text_putsa((center_x / STIMG_TEXT_BYTE_WIDTH) + (column / STIMG_TEXT_BYTE_WIDTH), top / STIMG_CELL_HEIGHT_PX,
                        staff_image_cover_a, STAFF_TEXT_BLACK + STAFF_TEXT_REVERSE);
                }
            }
        }
    } else if(staff_image_phase_a <= STIMG_PHASE_COVER_LAST) {
        staff_image_wipe_frame_a++;
        if((staff_image_wipe_frame_a % STIMG_WIPE_STEP_FRAMES) == 0) {
            staff_image_wipe_extent_a--;
        }
        if(staff_text_wipe(center_x, top, image->pixel_w, image->pixel_h,
            staff_image_wipe_extent_a, STIMG_WIPE_COVER_DIRECTION) == STIMG_WIPE_COVERED_RESULT) {
            staff_image_phase_a++;
            staff_image_wipe_extent_a = 0;
            staff_image_wipe_frame_a = 0;
        }
    } else if((staff_bgm_measure >= measure) &&
        (measure != STAFF_IMAGE_HOLD_MEASURE)) {
        if(staff_image_phase_a == STIMG_PHASE_UNCOVER) {
            staff_image_wipe_frame_a++;
            if((staff_image_wipe_frame_a % STIMG_WIPE_STEP_FRAMES) == 0) {
                staff_image_wipe_extent_a++;
            }
            if(staff_text_wipe(center_x, top, image->pixel_w, image->pixel_h,
                staff_image_wipe_extent_a, STIMG_WIPE_UNCOVER_DIRECTION) == STIMG_WIPE_UNCOVERED_RESULT) {
                staff_image_phase_a++;
            }
        } else {
            staff_text_wipe(center_x, top, image->pixel_w, image->pixel_h, STIMG_WIPE_FULL_EXTENT, STIMG_WIPE_UNCOVER_DIRECTION);
            staff_image_phase_a = 0;
            staff_text_clear_requested = 1;
            return 1;
        }
    }
    return 0;
}
