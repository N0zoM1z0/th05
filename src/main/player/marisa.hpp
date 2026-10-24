// Candidate Marisa-specific controls, adapted from nmlgc/ReC98@b6ba5b0a529edbb3
// th05/main/player/shot.hpp. Reuse the existing complete Shot/Iterator types.
#ifndef TH05_MAIN_PLAYER_MARISA_HPP
#define TH05_MAIN_PLAYER_MARISA_HPP

#include "src/main/player/reimu.hpp"

#define TO_SP(value) ((value) << 4)

inline subpixel_t to_sp(float pixel_v) {
    return static_cast<subpixel_t>(pixel_v * 16);
}

#define OPT_L shot->from_option_l()
#define OPT_R shot->from_option_r()
#define MISSILE_L shot->type = ST_MISSILE_LEFT
#define MISSILE_R shot->type = ST_MISSILE_RIGHT
#define MISSILE_S shot->type = ST_MISSILE_STRAIGHT

// Expand the original Subpixel::set(float) into an identical signed Q12.4
// assignment here, without changing any accepted shared class definition.
#define VELOCITY_X(screen_x) shot->pos.velocity.x.v = static_cast<subpixel_t>((screen_x) * 16);
#define VELOCITY_Y(screen_y) shot->pos.velocity.y.v = static_cast<subpixel_t>((screen_y) * 16);
#define VELOCITY_XY(screen_x, screen_y) \
    VELOCITY_X(screen_x); \
    VELOCITY_Y(screen_y);
#define VELOCITY_YX(screen_y, screen_x) \
    VELOCITY_Y(screen_y); \
    VELOCITY_X(screen_x);

extern "C" {
    void pascal near shot_marisa_l2(void);
    void pascal near shot_marisa_l3(void);
    void pascal near shot_marisa_l4(void);
    void pascal near shot_marisa_l5(void);
    void pascal near shot_marisa_l6(void);
    void pascal near shot_marisa_l7(void);
    void pascal near shot_marisa_l8(void);
    void pascal near shot_marisa_l9(void);
}

#endif
