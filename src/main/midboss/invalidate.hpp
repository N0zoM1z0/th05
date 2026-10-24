// Real GAME5 midboss/point definitions reused read-only from accepted owners.
// Natural provenance: ReC98 b6ba5b0a, midboss/inv.cpp and tile/tile.hpp.
#ifndef TH05_MAIN_MIDBOSS_INVALIDATE_HPP
#define TH05_MAIN_MIDBOSS_INVALIDATE_HPP
#include "src/main/stage/setup.hpp"
// The full two-word point definition is identical to overlay.hpp. Keeping this
// actual interface local avoids combining unrelated producer-local to_sp helpers.
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
// Use the same actual two-word Pascal ASM entry declaration as the accepted
// overlay owner. The reference's four-byte SPPoint by-value view has exactly
// this stack layout; explicit y/x fields avoid introducing another signature.
extern "C" void pascal near tiles_invalidate_around(subpixel_t y, subpixel_t x);
typedef char invalidate_midboss_is_22[(sizeof(midboss_stuff_t) == 22) ? 1 : -1];
typedef char invalidate_point_is_4[(sizeof(point_t) == 4) ? 1 : -1];
#endif
