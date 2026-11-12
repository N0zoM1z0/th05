// Original phase-ten Devil projectile settings; compile-time behavior only.
// All physical Boss/laser/bullet state remains in the canonical game structs.
#ifndef TH05_SHINKI_DEVIL_BALLISTICS_HPP
#define TH05_SHINKI_DEVIL_BALLISTICS_HPP
#include "src/main/boss/shinki/wing_hitboxes.hpp"

#define SHINKI_DEVIL_LASER_WIDTH_PX 6
#define SHINKI_DEVIL_LASER_INITIAL_ANGLE 0x40
#define SHINKI_DEVIL_LASER_COLOR 0x0E
#define SHINKI_DEVIL_INITIAL_INNER_BULLET_ANGLE 0x20
#define SHINKI_DEVIL_INITIAL_OUTER_BULLET_ANGLE 0x00
// This compiler has a 31-character preprocessor identifier significance
// limit. Keep all eight per-rank names distinct before that boundary;
// long common prefixes collapse all four parameters to Lunatic values.
#define DEVIL_BALL_START_EASY 64
#define DEVIL_BALL_START_NORMAL 40
#define DEVIL_BALL_START_HARD 32
#define DEVIL_BALL_START_LUNATIC 28
#define DEVIL_BALL_FAST_EASY 52
#define DEVIL_BALL_FAST_NORMAL 20
#define DEVIL_BALL_FAST_HARD 16
#define DEVIL_BALL_FAST_LUNATIC 12
#define SHINKI_DEVIL_PRELUDE_BULLET_COUNT 1
#define SHINKI_DEVIL_FULL_BULLET_COUNT 3
#define SHINKI_DEVIL_SPREAD_ARC_ANGLE 0x30
#define SHINKI_DEVIL_BULLET_SPEED_PX 7.0f
#define SHINKI_DEVIL_MIRROR_ANGLE 0x80
#define SHINKI_DEVIL_DECORATIVE_PELLET_PATNUM 0
#define SHINKI_DEVIL_AIMED_BALL_SPEED_PX 3.75f
#define SHINKI_DEVIL_VOLLEY_SOUND 3

#endif
