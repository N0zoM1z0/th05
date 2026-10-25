// Complete TH05 registration state; ReC98 b6ba5b0a529edbb31efdf8c0e939263804f8ee47
// th05/regist.cpp and original th05_maine.asm glyphball_t/allocated pool.
#ifndef TH05_MREG_GLYPHBALL_HPP
#define TH05_MREG_GLYPHBALL_HPP
#include "src/shared/geometry.hpp"
#if GAME != 5 || BINARY != 'E'
#error This owner requires TH05 MAINE
#endif

enum glyphball_phase_t {
    GBP_FREE = 0,
    GBP_CLOUD_AT_ORIGIN = 1,
    GBP_FLOAT_TO_TARGET = 2,
    GBP_SPLASH_AT_TARGET = 3,
    GBP_DONE = 4,
    GBP_REMOVE_REQUEST = 5,
    _glyphball_phase_t_FORCE_UINT8 = 0xFF
};

struct glyphball_t {
    glyphball_phase_t phase;
    uint8_t glyph; // Encoded gaiji byte; original gaiji_th04_t has this full byte domain.
    MotionBase<SPPoint> pos;
    SPPoint target;
    uint8_t angle;
    SubpixelLength8 speed;
    int phase_frame;
    signed char unused[6]; // Six genuine unused bytes in the original 28-byte entity.
};

static const int REGISTRATION_NAME_LENGTH = 8;
static const int REGISTRATION_GLYPHBALL_COUNT = REGISTRATION_NAME_LENGTH + 1;
static const int REGISTRATION_ALPHABET_ROWS = 3;
static const int REGISTRATION_ALPHABET_COLS = 17;
extern glyphball_t glyphballs[REGISTRATION_GLYPHBALL_COUNT];
extern uint8_t gALPHABET[REGISTRATION_ALPHABET_ROWS * REGISTRATION_ALPHABET_COLS];

typedef char reg_phase_is_byte[(sizeof(glyphball_phase_t) == 1) ? 1 : -1];
typedef char reg_motion_is_12[(sizeof(MotionBase<SPPoint>) == 12) ? 1 : -1];
typedef char reg_ball_is_28[(sizeof(glyphball_t) == 28) ? 1 : -1];
typedef char reg_ball_phase_at_0[(offsetof(glyphball_t, phase) == 0) ? 1 : -1];
typedef char reg_ball_glyph_at_1[(offsetof(glyphball_t, glyph) == 1) ? 1 : -1];
typedef char reg_ball_pos_at_2[(offsetof(glyphball_t, pos) == 2) ? 1 : -1];
typedef char reg_ball_target_at_14[(offsetof(glyphball_t, target) == 14) ? 1 : -1];
typedef char reg_ball_angle_at_18[(offsetof(glyphball_t, angle) == 18) ? 1 : -1];
typedef char reg_ball_speed_at_19[(offsetof(glyphball_t, speed) == 19) ? 1 : -1];
typedef char reg_ball_frame_at_20[(offsetof(glyphball_t, phase_frame) == 20) ? 1 : -1];
typedef char reg_ball_unused_at_22[(offsetof(glyphball_t, unused) == 22) ? 1 : -1];
typedef char reg_ball_pool_is_252[(sizeof(glyphballs) == 252) ? 1 : -1];
typedef char reg_alphabet_is_51[(sizeof(gALPHABET) == 51) ? 1 : -1];
#endif
