// Second image slot of the staff roll, which can be shown alongside the
// first one. Same algorithm as staff_image_update_a(), with its own state.
#ifndef TH05_MAINE_STAFF_REVEAL_B_HPP
#define TH05_MAINE_STAFF_REVEAL_B_HPP
#include "src/maine/staff/image_phase.hpp"
extern int staff_image_phase_b;
extern int staff_image_wipe_extent_b;
extern int staff_image_wipe_frame_b;
// Defined in image_cover_strings.c.
extern "C" char staff_image_cover_b[3];
#ifdef TH05_STAFF_FULL_FAMILY
#pragma codeseg STAFF_FULL_TEXT group_01
#else
#pragma codeseg STAFF_IMAGE_B_TEXT group_01
#endif
int pascal near staff_image_update_b(int center_x, int center_y,
    int slot, int measure);
#endif
