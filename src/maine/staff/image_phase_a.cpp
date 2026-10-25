// Natural staff image reveal/hold/hide state machine, original DD01..DE79.
// ReC98 b6ba5b0a529edbb31efdf8c0e939263804f8ee47 th05_maine.asm sub_DCFC
// supplies semantic corroboration; the original decoded image determines ABI.
#pragma option -zCSTAFF_IMAGE_A_TEXT -zPgroup_01
#include "src/maine/staff/image_phase.hpp"
#pragma codeseg STAFF_IMAGE_A_TEXT group_01

int pascal near staff_image_update_a(int center_x, int center_y,
    int slot, int measure)
{
    int top = center_y;
    CDG near *image = &cdg_slots[slot];
    int row;
    int column;

    center_x -= (image->pixel_w / 2);
    top -= (image->pixel_h / 2);
    if(staff_image_phase_a <= 1) {
        staff_image_wipe_extent_a = ((image->pixel_w / 16) + 7);
        staff_image_wipe_frame_a = 0;
        staff_image_phase_a++;
        cdg_put_noalpha_8(center_x, top, slot);
        for(row = 0; row <= image->pixel_h; (row += 16, top += 16)) {
            for(column = 0; column <= image->pixel_w; column += 16) {
                if(((center_x / 8) + (column / 8)) < 80) {
                    text_putsa((center_x / 8) + (column / 8), top / 16,
                        staff_image_cover_a, STAFF_TEXT_BLACK + STAFF_TEXT_REVERSE);
                }
            }
        }
    } else if(staff_image_phase_a <= 3) {
        staff_image_wipe_frame_a++;
        if((staff_image_wipe_frame_a % 4) == 0) {
            staff_image_wipe_extent_a--;
        }
        if(staff_text_wipe(center_x, top, image->pixel_w, image->pixel_h,
            staff_image_wipe_extent_a, 1) == 1) {
            staff_image_phase_a++;
            staff_image_wipe_extent_a = 0;
            staff_image_wipe_frame_a = 0;
        }
    } else if((staff_bgm_measure >= measure) &&
        (measure != STAFF_IMAGE_HOLD_MEASURE)) {
        if(staff_image_phase_a == 4) {
            staff_image_wipe_frame_a++;
            if((staff_image_wipe_frame_a % 4) == 0) {
                staff_image_wipe_extent_a++;
            }
            if(staff_text_wipe(center_x, top, image->pixel_w, image->pixel_h,
                staff_image_wipe_extent_a, -1) == 2) {
                staff_image_phase_a++;
            }
        } else {
            staff_text_wipe(center_x, top, image->pixel_w, image->pixel_h, 128, -1);
            staff_image_phase_a = 0;
            staff_text_clear_requested = 1;
            return 1;
        }
    }
    return 0;
}
