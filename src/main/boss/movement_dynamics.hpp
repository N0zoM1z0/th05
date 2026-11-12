// Original Boss random-flight and exact-target approach motion.
// Compile-time physical movement rules, not a substitute Boss state.
#ifndef TH05_BOSS_MOVEMENT_DYNAMICS_HPP
#define TH05_BOSS_MOVEMENT_DYNAMICS_HPP

#define BMD_FIRST_MOTION_FRAME 0
#define BMD_RAND_LEFT_MIN_ANGLE (-0x30)
#define BMD_RAND_LEFT_MAX_ANGLE (+0x30)
#define BMD_RAND_RIGHT_MIN_ANGLE (+0x30)
#define BMD_RAND_RIGHT_MAX_ANGLE (+0x91)
#define BMD_VERTICAL_SPLIT_ANGLE 0x80
#define BMD_INITIAL_RANDOM_SPEED_PX 4.0f
#define BMD_RANDOM_DECEL_SUBPX 2
#define BMD_TOWARDS_DIVISOR 16
#define BMD_TOWARDS_DEFAULT_SPEED 1
#define BMD_TOWARDS_FINE_X_SPEED 4
#define BMD_TOWARDS_FINE_Y_SPEED 8
#define BMD_REACHED_DIMENSIONS 2
#define BMD_SUBPIXEL_SHIFT 4

#endif
