// Natural TH04 invalidation algorithm, adapted to the canonical TH05 enemy.
#ifndef TH05_MAIN_ENEMY_INVALIDATE_HPP
#define TH05_MAIN_ENEMY_INVALIDATE_HPP
#include "src/main/enemy/enemy.hpp"
static const int ENEMY_W = 32;
static const int ENEMY_H = 32;
// Match the existing overlay owner's genuine four-byte Pascal y/x protocol.
extern "C" void pascal near tiles_invalidate_around(subpixel_t y, subpixel_t x);
#endif
