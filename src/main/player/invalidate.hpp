// Natural player invalidation ABI. TH04 maintained donor and ReC98 b6ba5b0a
// player geometry corroboration; actual TH05 fields/clip bounds reviewed.
#ifndef TH05_MAIN_PLAYER_INVALIDATE_HPP
#define TH05_MAIN_PLAYER_INVALIDATE_HPP
#include "src/main/player/player.hpp"
#include "src/main/hud/overlay.hpp"

static const int PLAYER_SPRITE_W = 32;
static const int PLAYER_SPRITE_H = 48;
static const int PLAYER_OPTION_SPRITE_W = 16;
static const int PLAYER_OPTION_SPRITE_H = 16;
static const unsigned char MISS_EXPLOSION_COUNT = 8;
static const int MISS_EXPLOSION_W = 48;
static const int MISS_EXPLOSION_H = 48;
static const unsigned int MISS_EXPLOSION_RADIUS_VELOCITY = 7 * 16;
static const unsigned char MISS_EXPLOSION_ANGLE_VELOCITY = 8;

extern unsigned char miss_time;
extern unsigned int miss_explosion_radius;
extern unsigned char miss_explosion_angle;
extern SPPoint player_option_pos_prev;
extern SPPoint drawpoint;
extern "C" void pascal far vector2_at(SPPoint near &ret,
    subpixel_t origin_x, subpixel_t origin_y, subpixel_t length, int angle);
// Genuine legacy four-byte near Pascal point frame of the EXISTING entry.
// No field-level drawpoint aliases or new function/address are introduced.
typedef void (near pascal *near PlayerPointInvalidator)(const SPPoint center);
void near player_invalidate(void);

typedef char player_invalidate_point_is_4[(sizeof(SPPoint) == 4) ? 1 : -1];
typedef char player_invalidate_motion_is_12[(sizeof(player_pos) == 12) ? 1 : -1];
typedef char player_invalidate_radius_is_word[(sizeof(miss_explosion_radius) == 2) ? 1 : -1];
typedef char player_invalidate_point_call_is_near[(sizeof(PlayerPointInvalidator) == 2) ? 1 : -1];
#endif
