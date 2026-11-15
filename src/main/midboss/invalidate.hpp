// Declarations for midboss tile invalidation (ReC98 midboss/inv.cpp,
// tile/tile.hpp).
#ifndef TH05_MAIN_MIDBOSS_INVALIDATE_HPP
#define TH05_MAIN_MIDBOSS_INVALIDATE_HPP
#include "src/main/stage/setup.hpp"
// Same point type as in overlay.hpp, defined here to avoid pulling in that
// header's other helpers.
struct point_t {
    pixel_t x;
    pixel_t y;
};
extern point_t tile_invalidate_box;

static const pixel_t MIDBOSS_W_MAX = 64;
static const pixel_t MIDBOSS_H_MAX = 64;
static const pixel_t ENEMY_KILL_W = 32;
static const pixel_t ENEMY_KILL_H = 32;
static const unsigned char PHASE_EXPLODE_BIG = 254;
// The assembly routine takes y and x as two Pascal stack words, the same
// layout as ReC98's SPPoint by value.
extern "C" void pascal near tiles_invalidate_around(subpixel_t y, subpixel_t x);
typedef char invalidate_midboss_is_22[(sizeof(midboss_stuff_t) == 22) ? 1 : -1];
typedef char invalidate_point_is_4[(sizeof(point_t) == 4) ? 1 : -1];
#endif
