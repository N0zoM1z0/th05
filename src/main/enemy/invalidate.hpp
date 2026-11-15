// enemies_invalidate() declarations: marks the tiles behind every enemy for
// redrawing.
#ifndef TH05_MAIN_ENEMY_INVALIDATE_HPP
#define TH05_MAIN_ENEMY_INVALIDATE_HPP
#include "src/main/enemy/enemy.hpp"
static const int ENEMY_W = 32;
static const int ENEMY_H = 32;
// Takes the center point; declared with y first because Pascal pushes the
// arguments left to right, so x ends up at the lower address.
extern "C" void pascal near tiles_invalidate_around(subpixel_t y, subpixel_t x);
#endif
