// The player's aim-angle helper.
#ifndef TH05_MAIN_PLAYER_PLAYER_HPP
#define TH05_MAIN_PLAYER_PLAYER_HPP

#include "src/shared/geometry.hpp"

extern PlayfieldMotion player_pos;

// The library angle routine is a far Pascal call in the large memory model.
extern "C" int far pascal iatan2(int y, int x);

unsigned char pascal near player_angle_from(
    Subpixel x, Subpixel y, unsigned char plus_angle = 0
);

#endif
