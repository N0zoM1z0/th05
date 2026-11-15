// The balls that carry each entered glyph from the keyboard to the name
// field, and the keyboard layout. From ReC98's th05/regist.cpp.
#ifndef TH05_MREG_GLYPHBALL_HPP
#define TH05_MREG_GLYPHBALL_HPP
#include "src/shared/geometry.hpp"
#if GAME != 5 || BINARY != 'E'
#error This header is for TH05's MAINE.EXE only
#endif

enum glyphball_phase_t {
    GBP_FREE = 0,
    GBP_CLOUD_AT_ORIGIN = 1,

    // Also writes [glyph] to the high score structure once it reached
    // [target], immediately before advancing to the next phase.
    GBP_FLOAT_TO_TARGET = 2,

    GBP_SPLASH_AT_TARGET = 3,
    GBP_DONE = 4,

    // Non-[GBP_FREE] glyph ball should be removed
    GBP_REMOVE_REQUEST = 5,

    _glyphball_phase_t_FORCE_UINT8 = 0xFF
};

struct glyphball_t {
    glyphball_phase_t phase;
    uint8_t glyph; // gaiji_th04_t in ReC98
    MotionBase<SPPoint> pos; // Relative to the top-left corner of the screen.
    SPPoint target;
    uint8_t angle;
    SubpixelLength8 speed;
    int phase_frame;
    signed char unused[6];
};

static const int REGISTRATION_NAME_LENGTH = 8;
static const int REGISTRATION_GLYPHBALL_COUNT = REGISTRATION_NAME_LENGTH + 1;
static const int REGISTRATION_ALPHABET_ROWS = 3;
static const int REGISTRATION_ALPHABET_COLS = 17;
// 1 additional unused one, for some reason?
extern glyphball_t glyphballs[REGISTRATION_GLYPHBALL_COUNT];
extern uint8_t gALPHABET[REGISTRATION_ALPHABET_ROWS * REGISTRATION_ALPHABET_COLS];

#endif
