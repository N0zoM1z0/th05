// Physical Staff CDG image reveal stages, scan geometry, and wipe timing.
// Compile-time UI protocol only; the real 16-bit phase/extent/frame state
// remains in the existing MAINE global objects.
#ifndef TH05_STAFF_IMAGE_REVEAL_CHOREOGRAPHY_HPP
#define TH05_STAFF_IMAGE_REVEAL_CHOREOGRAPHY_HPP

#define STIMG_PHASE_PREPARE_LAST 1
#define STIMG_PHASE_COVER_LAST 3
#define STIMG_PHASE_UNCOVER 4
#define STIMG_CELL_WIDTH_PX 16
#define STIMG_CELL_HEIGHT_PX 16
#define STIMG_TEXT_BYTE_WIDTH 8
#define STIMG_SCREEN_TEXT_COLS 80
#define STIMG_WIPE_PREPARE_LEAD 7
#define STIMG_WIPE_STEP_FRAMES 4
#define STIMG_WIPE_COVER_DIRECTION 1
#define STIMG_WIPE_UNCOVER_DIRECTION (-1)
#define STIMG_WIPE_COVERED_RESULT 1
#define STIMG_WIPE_UNCOVERED_RESULT 2
#define STIMG_WIPE_FULL_EXTENT 128

#endif
