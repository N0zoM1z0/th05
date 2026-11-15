// Phases and geometry of staff_image_update_a() and staff_image_update_b().
//
// Phases 0-1: Draw the picture onto both VRAM pages (one page per frame), and
//             cover it with black text cells.
// Phases 2-3: Reveal the picture with a text-layer wipe.
// Phase 4:    Wait for the given BGM measure, then hide the picture with a
//             wipe in the opposite direction, ending with a black box on the
//             current page.
// Phase 5:    Black out the other page as well, and finish.
#ifndef TH05_STAFF_IMAGE_REVEAL_CHOREOGRAPHY_HPP
#define TH05_STAFF_IMAGE_REVEAL_CHOREOGRAPHY_HPP

#define STIMG_PHASE_DRAW_LAST 1
#define STIMG_PHASE_REVEAL_LAST 3
#define STIMG_PHASE_HIDE 4
#define STIMG_CELL_WIDTH_PX 16
#define STIMG_CELL_HEIGHT_PX 16
#define STIMG_TEXT_BYTE_WIDTH 8
#define STIMG_SCREEN_TEXT_COLS 80

// Starting the wipe this many cells beyond the picture width keeps every cell
// covered at first, with the 7-cel fade gradient just outside the picture.
#define STIMG_WIPE_PREPARE_LEAD 7
#define STIMG_WIPE_STEP_FRAMES 4
#define STIMG_WIPE_REVEAL_DIRECTION 1
#define STIMG_WIPE_HIDE_DIRECTION (-1)

// staff_text_wipe() results; see StaffWipeStatus in wipe.hpp.
#define STIMG_WIPE_REVEALED 1
#define STIMG_WIPE_HIDDEN 2

// Larger than any picture, so that the wipe immediately fills the box.
#define STIMG_WIPE_FULL_EXTENT 128

#endif
