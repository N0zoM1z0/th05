// Mima-local velocity operations; Shot and ShotAddIterator have one shared ABI.
// Natural-source provenance: nmlgc/ReC98@b6ba5b0a529edbb31efdf8c0e939263804f8ee47,
// th05/p_mima.cpp and th05/main/player/shot.hpp.
#ifndef TH05_MAIN_PLAYER_MIMA_HPP
#define TH05_MAIN_PLAYER_MIMA_HPP

#include "src/main/player/reimu.hpp"

// Assign signed Q12.4 velocities without adding methods to the shared class.
#define MIMA_VELOCITY_X(velocity_x) \
    shot->pos.velocity.x.v = static_cast<subpixel_t>((velocity_x) * 16)
#define MIMA_VELOCITY_Y(velocity_y) \
    shot->pos.velocity.y.v = static_cast<subpixel_t>((velocity_y) * 16)
#define MIMA_VELOCITY_XY(velocity_x, velocity_y) \
    MIMA_VELOCITY_X(velocity_x); MIMA_VELOCITY_Y(velocity_y)

extern "C" {
    void pascal near shot_mima_l2(void);
    void pascal near shot_mima_l3(void);
    void pascal near shot_mima_l4(void);
    void pascal near shot_mima_l5(void);
    void pascal near shot_mima_l6(void);
    void pascal near shot_mima_l7(void);
    void pascal near shot_mima_l8(void);
    void pascal near shot_mima_l9(void);
}

#endif
